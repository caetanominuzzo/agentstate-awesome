# npm Registry Integration

CLI tool for searching packages, listing versions, and getting download stats from the npm registry.

## Usage

```bash
# Search for packages
python scripts/integrations/npm-registry/npm_registry_cli.py search --query "react state management"

# Get package metadata
python scripts/integrations/npm-registry/npm_registry_cli.py get-package --name "express"

# List all versions of a package
python scripts/integrations/npm-registry/npm_registry_cli.py list-versions --name "express"

# Get download counts
python scripts/integrations/npm-registry/npm_registry_cli.py get-downloads --name "express" --period "last-month"
```

## Environment Variables

- `NPM_TOKEN` (optional): npm authentication token, only needed for private packages

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
