# Zendesk Integration

CLI tool for managing Zendesk tickets and searching support data.

## Usage

```bash
# List tickets
python scripts/integrations/zendesk/zendesk_cli.py list-tickets --status open

# Create a ticket
python scripts/integrations/zendesk/zendesk_cli.py create-ticket --subject "Login issue" --description "Users cannot log in" --priority high

# Update a ticket
python scripts/integrations/zendesk/zendesk_cli.py update-ticket --ticket-id 12345 --status solved --comment "Issue resolved"

# Get ticket details
python scripts/integrations/zendesk/zendesk_cli.py get-ticket --ticket-id 12345

# Search Zendesk
python scripts/integrations/zendesk/zendesk_cli.py search --query "type:ticket status:open"
```

## Environment Variables

- `ZENDESK_SUBDOMAIN` (required): Zendesk subdomain (e.g., `mycompany` for mycompany.zendesk.com)
- `ZENDESK_EMAIL` (required): Zendesk agent email address
- `ZENDESK_API_TOKEN` (required): Zendesk API token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
