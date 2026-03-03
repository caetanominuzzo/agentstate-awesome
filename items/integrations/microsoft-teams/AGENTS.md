# Microsoft Teams Integration

CLI tool for sending messages and adaptive cards to Microsoft Teams channels via webhooks.

## Usage

```bash
# Send a plain text message
python scripts/integrations/microsoft-teams/microsoft_teams_cli.py send --text "Deployment completed successfully"

# Send an adaptive card
python scripts/integrations/microsoft-teams/microsoft_teams_cli.py send-card --title "Build Status" --text "All tests passed" --color "00FF00"
```

## Environment Variables

- `TEAMS_WEBHOOK_URL` (required): Microsoft Teams incoming webhook URL

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
