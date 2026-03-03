# SendGrid Integration

CLI tool for sending emails via the SendGrid v3 API.

## Usage

```bash
# Send a plain text email
python scripts/integrations/sendgrid/sendgrid_cli.py send --to user@example.com --from noreply@example.com --subject "Hello" --text "Body text"

# Send an HTML email
python scripts/integrations/sendgrid/sendgrid_cli.py send --to user@example.com --from noreply@example.com --subject "Hello" --html "<h1>Hello</h1><p>Body</p>"
```

## Environment Variables

- `SENDGRID_API_KEY` (required): SendGrid API key for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
