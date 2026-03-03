# Confluence Integration

CLI tool for searching, creating, and updating Confluence pages and spaces.

## Usage

```bash
# Search with CQL
python scripts/integrations/confluence/confluence_cli.py search --cql "type=page AND space=DEV"

# Get page by ID
python scripts/integrations/confluence/confluence_cli.py get-page --page-id 123456

# Create a page
python scripts/integrations/confluence/confluence_cli.py create-page --space-key DEV --title "New Page" --body "<p>Page content</p>"

# Update a page
python scripts/integrations/confluence/confluence_cli.py update-page --page-id 123456 --title "Updated Title" --body "<p>New content</p>" --version 2

# List spaces
python scripts/integrations/confluence/confluence_cli.py list-spaces
```

## Environment Variables

- `CONFLUENCE_BASE_URL` (required): Your Confluence instance URL (e.g., `https://your-org.atlassian.net`)
- `CONFLUENCE_EMAIL` (required): Email address for authentication
- `CONFLUENCE_API_TOKEN` (required): API token for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
