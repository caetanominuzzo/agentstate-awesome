# Telegram Notifications

Send notifications and formatted alerts via Telegram Bot API.

## Usage

```bash
# Send a plain text message
python scripts/integrations/telegram/telegram_notify.py send --text "Deployment complete"

# Send with HTML formatting
python scripts/integrations/telegram/telegram_notify.py send --text "<b>Done</b>" --parse-mode HTML

# Send a formatted alert with severity
python scripts/integrations/telegram/telegram_notify.py alert \
  --title "High CPU Usage" \
  --fields '{"Host": "prod-1", "CPU": "95%", "Duration": "10m"}' \
  --severity WARNING

# Send a critical alert with extra context
python scripts/integrations/telegram/telegram_notify.py alert \
  --title "Service Down" \
  --fields '{"Service": "api-gateway", "Region": "us-east-1"}' \
  --severity CRITICAL \
  --context "On-call engineer has been paged."

# Verify bot connectivity
python scripts/integrations/telegram/telegram_notify.py info
```

## Environment Variables

- `TELEGRAM_BOT_TOKEN` (required): Bot token obtained from @BotFather.
- `TELEGRAM_CHAT_ID` (required): Target chat, group, or channel ID for notifications.

## Commands

| Command | Description |
|---------|-------------|
| `send`  | Send a plain text message. Supports optional `--parse-mode` (HTML, Markdown, MarkdownV2). |
| `alert` | Send a structured alert with `--title`, `--fields` (JSON), `--severity` (INFO/WARNING/CRITICAL), and optional `--context`. |
| `info`  | Call `getMe` to verify the bot token is valid and the bot is reachable. |

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
