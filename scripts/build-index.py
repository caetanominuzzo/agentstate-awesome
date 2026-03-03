#!/usr/bin/env python3
"""Build collection.json from all item manifests.

Walks items/ directory, reads each manifest.yaml, inlines file contents,
and generates the master collection.json used by the assembler site.

Usage:
    python scripts/build-index.py
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    # Fallback: minimal YAML parser for simple manifests
    yaml = None


def parse_yaml_simple(text):
    """Minimal YAML parser for flat/simple manifests when PyYAML is unavailable."""
    import re

    result = {}
    current_key = None
    current_list = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Multi-line string continuation
        if stripped.startswith("- ") and current_list is not None:
            item = stripped[2:].strip().strip('"').strip("'")
            # Check if it's a dict item (has ":" in it)
            if ": " in item and not item.startswith("http"):
                pass  # Skip complex nested items for simple parser
            current_list.append(item)
            continue

        # Key-value pair
        match = re.match(r"^(\w[\w_]*)\s*:\s*(.*)", stripped)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            if value == "" or value == ">":
                current_key = key
                current_list = None
                result[key] = ""
                continue

            if value == "[]":
                result[key] = []
                current_list = None
                continue

            if value.startswith("[") and value.endswith("]"):
                # Inline list
                items = value[1:-1].split(",")
                result[key] = [i.strip().strip('"').strip("'") for i in items if i.strip()]
                current_list = None
                continue

            # Boolean
            if value.lower() in ("true", "false"):
                result[key] = value.lower() == "true"
                current_list = None
                continue

            result[key] = value.strip('"').strip("'")
            current_list = None
            continue

        # List start
        if stripped.startswith("- "):
            if current_key and current_key not in result:
                result[current_key] = []
            if current_key and isinstance(result.get(current_key), list):
                current_list = result[current_key]
                item = stripped[2:].strip().strip('"').strip("'")
                current_list.append(item)

    return result


def load_yaml(filepath):
    """Load a YAML file."""
    text = filepath.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text)
    return parse_yaml_simple(text)


def load_manifest(item_dir):
    """Load and validate a manifest.yaml from an item directory."""
    manifest_path = item_dir / "manifest.yaml"
    if not manifest_path.exists():
        return None

    try:
        data = load_yaml(manifest_path)
    except Exception as e:
        print(f"  WARNING: Failed to parse {manifest_path}: {e}", file=sys.stderr)
        return None

    # Ensure required fields
    required = ["id", "name", "description", "category", "files"]
    for field in required:
        if field not in data:
            print(
                f"  WARNING: {manifest_path} missing required field: {field}",
                file=sys.stderr,
            )
            return None

    return data


def inline_file_contents(item_dir, manifest):
    """Read file contents and inline them into the manifest."""
    files_with_content = []
    for file_entry in manifest.get("files", []):
        src = file_entry.get("src", "") if isinstance(file_entry, dict) else file_entry
        dest = file_entry.get("dest", src) if isinstance(file_entry, dict) else file_entry
        src_path = item_dir / src

        content = ""
        if src_path.exists():
            try:
                content = src_path.read_text(encoding="utf-8")
            except Exception:
                content = ""

        files_with_content.append(
            {"src": src, "dest": dest, "content": content}
        )

    return files_with_content


def build_collection(items_root):
    """Build the full collection from all items."""
    items = []
    categories_seen = set()

    for category_dir in sorted(items_root.iterdir()):
        if not category_dir.is_dir():
            continue

        for item_dir in sorted(category_dir.rglob("manifest.yaml")):
            item_dir = item_dir.parent
            manifest = load_manifest(item_dir)
            if manifest is None:
                continue

            print(f"  + {manifest['id']}")
            categories_seen.add(manifest["category"])

            # Inline file contents
            manifest["files"] = inline_file_contents(item_dir, manifest)

            # Ensure optional fields have defaults
            manifest.setdefault("subcategory", "")
            manifest.setdefault("tags", [])
            manifest.setdefault("tech_tags", [])
            manifest.setdefault("compatible_agents", ["any"])
            manifest.setdefault("depends_on", [])
            manifest.setdefault("python_dependencies", [])
            manifest.setdefault("env_vars", [])
            manifest.setdefault("featured", False)
            manifest.setdefault("source", {"type": "original"})

            items.append(manifest)

    # Build category metadata
    category_meta = {
        "skills": {
            "id": "skills",
            "name": "Agent Skills",
            "description": "Reusable procedural knowledge from the agents.sh ecosystem",
        },
        "integrations": {
            "id": "integrations",
            "name": "Integrations",
            "description": "Scripts connecting agents to external services",
        },
        "modes": {
            "id": "modes",
            "name": "Behavioral Modes",
            "description": "Behavior profiles that change how agents operate",
        },
        "orchestration": {
            "id": "orchestration",
            "name": "Orchestration",
            "description": "Multi-agent coordination and handoff patterns",
        },
        "knowledge": {
            "id": "knowledge",
            "name": "Knowledge Templates",
            "description": "Organizational context and memory templates",
        },
        "meta": {
            "id": "meta",
            "name": "Meta Tools",
            "description": "Tools for the agent-state repo itself",
        },
    }

    categories = [
        category_meta[c] for c in sorted(categories_seen) if c in category_meta
    ]

    return {
        "version": "1.0.0",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo": "caetanominuzzo/agentstate-awesome",
        "items": items,
        "categories": categories,
    }


def main():
    repo_root = Path(__file__).parent.parent
    items_root = repo_root / "items"

    if not items_root.exists():
        print("ERROR: items/ directory not found", file=sys.stderr)
        sys.exit(1)

    print("Building collection index...")
    collection = build_collection(items_root)
    print(f"  Total items: {len(collection['items'])}")
    print(f"  Categories: {len(collection['categories'])}")

    output_path = repo_root / "collection.json"
    output_path.write_text(
        json.dumps(collection, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  Written to: {output_path}")


if __name__ == "__main__":
    main()
