# Discord Integration

CLI tool for sending messages and embeds to Discord via webhooks.

## Usage

```bash
# Send a text message
python scripts/integrations/discord/discord_cli.py send --text "Hello from the agent!"

# Send an embed
python scripts/integrations/discord/discord_cli.py send-embed --title "Alert" --description "Something happened" --color 16711680
```

## Environment Variables

- `DISCORD_WEBHOOK_URL` (required): Discord webhook URL for the target channel

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
