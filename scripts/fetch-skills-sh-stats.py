#!/usr/bin/env python3
"""Fetch install stats from skills.sh for mirrored skills.

Reads collection.json, groups items by source repo, fetches each repo's
skills.sh page, parses install counts, and writes stats.json.

Usage:
    python scripts/fetch-skills-sh-stats.py
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path


def fetch_page(url: str) -> str:
    """Fetch a URL and return its text content."""
    req = urllib.request.Request(url, headers={"User-Agent": "agentstate-awesome/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


def parse_repo_stats(html: str, repo: str) -> dict[str, str]:
    """Extract skill install counts from a skills.sh repo page.

    The page is a Next.js SSR page. We try multiple patterns to be resilient
    against minor markup changes.

    Returns a dict of {skill_id: install_count_str}, e.g.:
        {"python-testing-patterns": "9.9K", "api-design-principles": "12.4K"}
    """
    stats = {}

    # Pattern 1: href links to skill pages followed by install count
    # e.g., href="/wshobson/agents/api-design-principles" ... 12.7K
    repo_escaped = re.escape(repo)
    for match in re.finditer(
        rf'/{repo_escaped}/([a-z0-9_-]+).*?([\d]+(?:\.\d+)?[KMB])',
        html,
        re.DOTALL,
    ):
        skill_id = match.group(1)
        installs = match.group(2).strip()
        # Only take the first (closest) count for each skill
        if skill_id not in stats:
            stats[skill_id] = installs

    # Pattern 2: Next.js JSON data embedded in script tags
    if not stats:
        for match in re.finditer(
            r'"slug"\s*:\s*"([a-z0-9_-]+)"[^}]*?"installs?(?:Count)?"\s*:\s*["\']?([\d]+(?:\.\d+)?[KMB]?)',
            html,
            re.IGNORECASE,
        ):
            stats[match.group(1)] = match.group(2)

    # Pattern 3: plain text — skill-name followed by count on nearby lines
    if not stats:
        for match in re.finditer(
            r'([a-z][a-z0-9]+-[a-z0-9-]+)\s+(\d+(?:\.\d+)?[KMB])',
            html,
        ):
            skill_id = match.group(1)
            installs = match.group(2)
            if skill_id not in stats:
                stats[skill_id] = installs

    return stats


def main():
    repo_root = Path(__file__).parent.parent
    collection_path = repo_root / "collection.json"

    if not collection_path.exists():
        print("ERROR: collection.json not found. Run build-index.py first.", file=sys.stderr)
        sys.exit(1)

    collection = json.loads(collection_path.read_text(encoding="utf-8"))

    # Group items by source repo
    repos: dict[str, list[str]] = {}
    for item in collection.get("items", []):
        url = item.get("skills_sh_url", "")
        source = item.get("source", {})
        if url and source.get("repo"):
            repo = source["repo"]
            repos.setdefault(repo, []).append(item["id"])

    if not repos:
        print("No mirrored skills with skills_sh_url found.")
        return

    print(f"Fetching stats for {sum(len(v) for v in repos.values())} skills across {len(repos)} repo(s)...")

    all_stats: dict[str, dict] = {}
    for repo, item_ids in repos.items():
        url = f"https://skills.sh/{repo}"
        print(f"  Fetching {url} ({len(item_ids)} skills)...")
        try:
            html = fetch_page(url)
            repo_stats = parse_repo_stats(html, repo)
            for item_id in item_ids:
                if item_id in repo_stats:
                    all_stats[item_id] = {"installs": repo_stats[item_id]}
                    print(f"    {item_id}: {repo_stats[item_id]}")
                else:
                    print(f"    {item_id}: not found on page")
        except Exception as e:
            print(f"  WARNING: Failed to fetch {url}: {e}", file=sys.stderr)

        # Be respectful: wait between repo requests
        if len(repos) > 1:
            time.sleep(2)

    output_path = repo_root / "stats.json"
    output_path.write_text(
        json.dumps(all_stats, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWritten {len(all_stats)} stats to {output_path}")


if __name__ == "__main__":
    main()
