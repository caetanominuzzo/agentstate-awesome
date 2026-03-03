# Slack Integration

CLI tool for sending messages and interacting with Slack channels.

## Usage

```bash
# Send a message to a channel
python scripts/integrations/slack/slack_cli.py send-message --channel "#general" --text "Hello from the agent!"

# List public channels
python scripts/integrations/slack/slack_cli.py list-channels

# Post a rich block message
python scripts/integrations/slack/slack_cli.py post-blocks --channel "#general" --blocks-json '[{"type":"section","text":{"type":"mrkdwn","text":"*Bold text*"}}]'
```

## Environment Variables

- `SLACK_BOT_TOKEN` (required): Slack Bot User OAuth Token (xoxb-...)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
