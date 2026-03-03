# Resend Integration

CLI tool for sending emails and listing sent emails via the Resend API.

## Usage

```bash
# Send a plain text email
python scripts/integrations/resend/resend_cli.py send --to user@example.com --from noreply@yourdomain.com --subject "Hello" --text "Body text"

# Send an HTML email
python scripts/integrations/resend/resend_cli.py send --to user@example.com --from noreply@yourdomain.com --subject "Hello" --html "<h1>Hello</h1>"

# List recently sent emails
python scripts/integrations/resend/resend_cli.py list-emails
```

## Environment Variables

- `RESEND_API_KEY` (required): Resend API key (re_...)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
