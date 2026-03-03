# Webhook Integration

CLI tool for sending data to arbitrary webhook URLs with optional HMAC-SHA256 signing.

## Usage

```bash
# Send JSON data
python scripts/integrations/webhook/webhook_cli.py send --json-data '{"event":"deploy","status":"success"}'

# Send plain text (wrapped in JSON as {"text": "..."})
python scripts/integrations/webhook/webhook_cli.py send --text "Deployment completed"

# Test webhook connectivity
python scripts/integrations/webhook/webhook_cli.py test
```

## Environment Variables

- `WEBHOOK_URL` (required): The webhook endpoint URL to send data to
- `WEBHOOK_SECRET` (optional): Secret key for HMAC-SHA256 signature (sent as X-Signature-256 header)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
