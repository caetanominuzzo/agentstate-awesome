# PyPI Integration

CLI tool for searching packages, listing versions, and getting release data from PyPI.

## Usage

```bash
# Get package metadata
python scripts/integrations/pypi/pypi_cli.py get-package --name "requests"

# Search for packages
python scripts/integrations/pypi/pypi_cli.py search --query "requests"

# List all versions of a package
python scripts/integrations/pypi/pypi_cli.py list-versions --name "requests"

# Get release data for a specific version
python scripts/integrations/pypi/pypi_cli.py get-release --name "requests" --version "2.31.0"
```

## Environment Variables

No environment variables are required. PyPI is a public API.

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
