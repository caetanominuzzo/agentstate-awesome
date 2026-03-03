# Twilio Integration

CLI tool for sending SMS and WhatsApp messages via Twilio.

## Usage

```bash
# Send an SMS
python scripts/integrations/twilio/twilio_cli.py send-sms --to "+15559876543" --body "Hello from the agent!"

# Send a WhatsApp message
python scripts/integrations/twilio/twilio_cli.py send-whatsapp --to "+15559876543" --body "Hello from WhatsApp!"

# List recent messages
python scripts/integrations/twilio/twilio_cli.py list-messages --limit 10
```

## Environment Variables

- `TWILIO_ACCOUNT_SID` (required): Twilio Account SID
- `TWILIO_AUTH_TOKEN` (required): Twilio Auth Token
- `TWILIO_FROM_NUMBER` (required): Twilio phone number to send from (e.g., `+15551234567`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
