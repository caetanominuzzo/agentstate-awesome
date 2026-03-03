# New Relic Integration

CLI tool for querying NRQL, listing applications, and managing alert policies in New Relic.

## Usage

```bash
# Execute a NRQL query
python scripts/integrations/new-relic/new_relic_cli.py query-nrql --nrql "SELECT count(*) FROM Transaction SINCE 1 hour ago"

# List all APM applications
python scripts/integrations/new-relic/new_relic_cli.py list-applications

# Get application details
python scripts/integrations/new-relic/new_relic_cli.py get-application --app-id "12345678"

# List all alert policies
python scripts/integrations/new-relic/new_relic_cli.py list-alert-policies
```

## Environment Variables

- `NEW_RELIC_API_KEY` (required): New Relic User API key for authentication
- `NEW_RELIC_ACCOUNT_ID` (required): New Relic account ID

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
