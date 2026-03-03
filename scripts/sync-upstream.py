#!/usr/bin/env python3
"""Sync mirrored skills from upstream GitHub repositories.

Reads all manifest.yaml files where source.type == "mirror",
fetches the latest SKILL.md from the upstream repo, and updates
the local copy if changed.

Usage:
    python scripts/sync-upstream.py
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml


def fetch_raw_github(repo, path):
    """Fetch a file from GitHub's raw content CDN."""
    url = f"https://raw.githubusercontent.com/{repo}/main/{path}"
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        return resp.text
    # Try master branch
    url = f"https://raw.githubusercontent.com/{repo}/master/{path}"
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        return resp.text
    return None


def sync_item(item_dir, manifest):
    """Sync a single mirrored item. Returns True if updated."""
    source = manifest.get("source", {})
    if source.get("type") != "mirror":
        return False

    repo = source.get("repo")
    path = source.get("path")
    if not repo or not path:
        print(f"  SKIP {item_dir.name}: missing repo or path in source")
        return False

    print(f"  Fetching {repo}/{path}...")
    content = fetch_raw_github(repo, path)
    if content is None:
        print(f"  WARNING: Could not fetch {repo}/{path}")
        return False

    # Determine local file to update (first file in files list)
    files = manifest.get("files", [])
    if not files:
        return False

    first_file = files[0]
    src = first_file.get("src", first_file) if isinstance(first_file, dict) else first_file
    local_path = item_dir / src

    # Check if content changed
    if local_path.exists():
        existing = local_path.read_text(encoding="utf-8")
        if existing == content:
            print(f"  OK {item_dir.name}: up to date")
            return False

    # Write updated content
    local_path.write_text(content, encoding="utf-8")

    # Update last_synced in manifest
    source["last_synced"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    manifest_path = item_dir / "manifest.yaml"
    manifest_path.write_text(yaml.dump(manifest, default_flow_style=False, sort_keys=False))

    print(f"  UPDATED {item_dir.name}")
    return True


def main():
    repo_root = Path(__file__).parent.parent
    items_root = repo_root / "items"

    if not items_root.exists():
        print("ERROR: items/ directory not found", file=sys.stderr)
        sys.exit(1)

    print("Syncing upstream skills...")
    updated = 0
    total = 0

    for manifest_path in items_root.rglob("manifest.yaml"):
        item_dir = manifest_path.parent
        try:
            manifest = yaml.safe_load(manifest_path.read_text())
        except Exception as e:
            print(f"  WARNING: Failed to parse {manifest_path}: {e}")
            continue

        if not manifest or manifest.get("source", {}).get("type") != "mirror":
            continue

        total += 1
        if sync_item(item_dir, manifest):
            updated += 1

    print(f"\nDone: {updated}/{total} mirrored items updated")


if __name__ == "__main__":
    main()
