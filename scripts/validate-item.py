#!/usr/bin/env python3
"""Validate an item's manifest.yaml and file structure.

Usage:
    python scripts/validate-item.py items/integrations/jira/
    python scripts/validate-item.py items/skills/workflow/systematic-debugging/
"""
import json
import sys
from pathlib import Path

try:
    import yaml

    def load_yaml(path):
        return yaml.safe_load(path.read_text())

except ImportError:
    yaml = None

    def load_yaml(path):
        # Import the simple parser from build-index
        sys.path.insert(0, str(Path(__file__).parent))
        from importlib import import_module

        build = import_module("build-index")
        return build.parse_yaml_simple(path.read_text())


VALID_CATEGORIES = {"skills", "integrations", "modes", "orchestration", "knowledge", "meta"}
REQUIRED_FIELDS = ["id", "name", "description", "category", "files"]


def validate_item(item_dir):
    """Validate an item directory. Returns list of errors."""
    errors = []
    item_dir = Path(item_dir)

    if not item_dir.is_dir():
        return [f"Not a directory: {item_dir}"]

    manifest_path = item_dir / "manifest.yaml"
    if not manifest_path.exists():
        return [f"Missing manifest.yaml in {item_dir}"]

    try:
        manifest = load_yaml(manifest_path)
    except Exception as e:
        return [f"Failed to parse manifest.yaml: {e}"]

    if manifest is None:
        return [f"manifest.yaml is empty"]

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    # ID matches directory name
    if manifest["id"] != item_dir.name:
        errors.append(
            f"ID '{manifest['id']}' does not match directory name '{item_dir.name}'"
        )

    # Category is valid
    if manifest["category"] not in VALID_CATEGORIES:
        errors.append(
            f"Invalid category '{manifest['category']}'. Must be one of: {VALID_CATEGORIES}"
        )

    # Files exist
    files = manifest.get("files", [])
    if not files:
        errors.append("No files listed in manifest")
    else:
        for f in files:
            src = f.get("src", f) if isinstance(f, dict) else f
            src_path = item_dir / src
            if not src_path.exists():
                errors.append(f"Referenced file does not exist: {src}")

    # Env vars structure
    for env in manifest.get("env_vars", []):
        if isinstance(env, dict):
            if "name" not in env:
                errors.append(f"env_var entry missing 'name' field")
            if "description" not in env:
                errors.append(f"env_var '{env.get('name', '?')}' missing 'description'")

    # Python dependencies are valid pip specifiers
    for dep in manifest.get("python_dependencies", []):
        if not isinstance(dep, str):
            errors.append(f"Invalid python_dependency: {dep}")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-item.py <item-directory>")
        sys.exit(1)

    item_dir = sys.argv[1]
    errors = validate_item(item_dir)

    if errors:
        print(f"FAILED: {item_dir}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"OK: {item_dir}")
        sys.exit(0)


if __name__ == "__main__":
    main()
