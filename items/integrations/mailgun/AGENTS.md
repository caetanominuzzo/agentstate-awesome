# Mailgun Integration

CLI tool for sending emails and listing events via Mailgun.

## Usage

```bash
# Send a plain text email
python scripts/integrations/mailgun/mailgun_cli.py send --to "user@example.com" --from "agent@mg.example.com" --subject "Alert" --text "This is a notification"

# Send an HTML email
python scripts/integrations/mailgun/mailgun_cli.py send --to "user@example.com" --from "agent@mg.example.com" --subject "Report" --html "<h1>Report</h1><p>Details here</p>"

# List recent events
python scripts/integrations/mailgun/mailgun_cli.py list-events --limit 50
```

## Environment Variables

- `MAILGUN_API_KEY` (required): Mailgun API key
- `MAILGUN_DOMAIN` (required): Mailgun sending domain (e.g., `mg.example.com`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
