#!/usr/bin/env python3
"""Semantic search for agent-state repositories.

Indexes all files in the repo and supports keyword search with TF-IDF ranking.
No external dependencies required - uses Python stdlib only.

Usage:
    python scripts/meta/search.py "how to create a jira ticket"
    python scripts/meta/search.py --tag python "testing patterns"
    python scripts/meta/search.py --category integrations "notification"
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path


INDEXED_EXTENSIONS = {".md", ".json", ".py", ".yaml", ".yml", ".txt"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "workspace", ".agentstate-index.json"}
INDEX_FILE = ".agentstate-index.json"
MAX_SNIPPET_LEN = 200


def find_repo_root():
    """Find the root of the agent-state repo (walk up to find AGENTS.md or .git)."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "AGENTS.md").exists() or (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def should_index(path, root):
    """Check if a file should be indexed."""
    rel = path.relative_to(root)
    parts = rel.parts
    if any(p in SKIP_DIRS for p in parts):
        return False
    return path.suffix in INDEXED_EXTENSIONS and path.is_file()


def extract_text(filepath):
    """Extract searchable text from a file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

    if filepath.suffix == ".json":
        try:
            data = json.loads(content)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            return content

    return content


def tokenize(text):
    """Simple tokenization: lowercase, split on non-alphanumeric."""
    return re.findall(r"[a-z0-9]+", text.lower())


def build_index(root):
    """Build the search index from all files in the repo."""
    documents = []
    for path in sorted(root.rglob("*")):
        if not should_index(path, root):
            continue
        text = extract_text(path)
        if not text.strip():
            continue
        rel_path = str(path.relative_to(root))
        tokens = tokenize(text)
        documents.append({
            "path": rel_path,
            "content": text[:5000],  # cap stored content
            "tokens": tokens,
            "mtime": path.stat().st_mtime,
        })
    return documents


def load_or_build_index(root):
    """Load cached index or rebuild if stale."""
    index_path = root / INDEX_FILE
    if index_path.exists():
        try:
            cached = json.loads(index_path.read_text())
            # Check if any file has changed
            stale = False
            indexed_paths = {d["path"] for d in cached}
            for path in root.rglob("*"):
                if not should_index(path, root):
                    continue
                rel = str(path.relative_to(root))
                if rel not in indexed_paths:
                    stale = True
                    break
                mtime = path.stat().st_mtime
                doc = next((d for d in cached if d["path"] == rel), None)
                if doc and doc.get("mtime", 0) < mtime:
                    stale = True
                    break
            if not stale:
                return cached
        except (json.JSONDecodeError, KeyError):
            pass

    documents = build_index(root)
    # Save cache (without tokens to keep it small)
    cache_data = [
        {"path": d["path"], "mtime": d["mtime"], "content": d["content"]}
        for d in documents
    ]
    try:
        index_path.write_text(json.dumps(cache_data, indent=2))
    except Exception:
        pass  # Non-critical if caching fails

    return documents


def compute_tfidf(query_tokens, documents):
    """Compute TF-IDF scores for query against documents."""
    n_docs = len(documents)
    if n_docs == 0:
        return []

    # Document frequency for each term
    df = Counter()
    for doc in documents:
        unique_tokens = set(doc.get("tokens") or tokenize(doc.get("content", "")))
        for token in unique_tokens:
            df[token] += 1

    results = []
    for doc in documents:
        doc_tokens = doc.get("tokens") or tokenize(doc.get("content", ""))
        if not doc_tokens:
            continue
        tf = Counter(doc_tokens)
        doc_len = len(doc_tokens)

        score = 0.0
        for qt in query_tokens:
            if qt in tf:
                term_freq = tf[qt] / doc_len
                inv_doc_freq = math.log((n_docs + 1) / (df.get(qt, 0) + 1)) + 1
                score += term_freq * inv_doc_freq

        if score > 0:
            results.append((doc, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def extract_snippet(content, query_tokens, max_len=MAX_SNIPPET_LEN):
    """Extract a relevant snippet from content around query terms."""
    lower = content.lower()
    best_pos = 0
    best_count = 0

    for i in range(0, len(lower) - 50, 20):
        window = lower[i : i + max_len]
        count = sum(1 for t in query_tokens if t in window)
        if count > best_count:
            best_count = count
            best_pos = i

    snippet = content[best_pos : best_pos + max_len].strip()
    if best_pos > 0:
        snippet = "..." + snippet
    if best_pos + max_len < len(content):
        snippet = snippet + "..."
    return snippet.replace("\n", " ")


def search(query, root=None, tag_filter=None, category_filter=None, limit=10):
    """Search the agent-state repo."""
    if root is None:
        root = find_repo_root()

    documents = load_or_build_index(root)
    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    # Apply filters
    if category_filter:
        documents = [d for d in documents if category_filter in d["path"].split("/")[0:2]]
    if tag_filter:
        tag_lower = tag_filter.lower()
        documents = [
            d for d in documents
            if tag_lower in d.get("content", "").lower()
        ]

    results = compute_tfidf(query_tokens, documents)

    output = []
    for doc, score in results[:limit]:
        snippet = extract_snippet(doc.get("content", ""), query_tokens)
        output.append({
            "path": doc["path"],
            "score": round(score, 4),
            "snippet": snippet,
        })

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Search your agent-state repository"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--tag", default=None, help="Filter by tag/keyword in content")
    parser.add_argument("--category", default=None, help="Filter by top-level category")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")

    args = parser.parse_args()
    results = search(
        args.query,
        tag_filter=args.tag,
        category_filter=args.category,
        limit=args.limit,
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
