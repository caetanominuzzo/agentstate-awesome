# HubSpot Integration

CLI tool for managing HubSpot contacts and deals.

## Usage

```bash
# List contacts
python scripts/integrations/hubspot/hubspot_cli.py list-contacts --limit 20

# Get contact details
python scripts/integrations/hubspot/hubspot_cli.py get-contact --contact-id 12345

# Create a contact
python scripts/integrations/hubspot/hubspot_cli.py create-contact --email "user@example.com" --firstname "John" --lastname "Doe"

# List deals
python scripts/integrations/hubspot/hubspot_cli.py list-deals --limit 20

# Create a deal
python scripts/integrations/hubspot/hubspot_cli.py create-deal --name "Enterprise Deal" --pipeline default --stage qualifiedtobuy
```

## Environment Variables

- `HUBSPOT_ACCESS_TOKEN` (required): HubSpot private app access token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
