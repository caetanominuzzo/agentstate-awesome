# PagerDuty Integration

CLI tool for managing PagerDuty incidents.

## Usage

```bash
# List all incidents
python scripts/integrations/pagerduty/pagerduty_cli.py list-incidents

# List triggered incidents only
python scripts/integrations/pagerduty/pagerduty_cli.py list-incidents --status triggered

# Create an incident
python scripts/integrations/pagerduty/pagerduty_cli.py create-incident --service-id PXXXXXX --title "Database CPU high"

# Acknowledge an incident
python scripts/integrations/pagerduty/pagerduty_cli.py acknowledge --incident-id PXXXXXX

# Resolve an incident
python scripts/integrations/pagerduty/pagerduty_cli.py resolve --incident-id PXXXXXX
```

## Environment Variables

- `PAGERDUTY_API_KEY` (required): PagerDuty REST API key (v2)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
