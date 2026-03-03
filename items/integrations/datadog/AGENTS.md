# Datadog Integration

CLI tool for querying metrics, listing monitors, and searching logs in Datadog.

## Usage

```bash
# Query metrics
python scripts/integrations/datadog/datadog_cli.py query-metrics --query "avg:system.cpu.user{*}" --from 1700000000 --to 1700003600

# List all monitors
python scripts/integrations/datadog/datadog_cli.py list-monitors

# Search logs
python scripts/integrations/datadog/datadog_cli.py search-logs --query "service:web status:error" --from "2024-01-01T00:00:00Z" --to "2024-01-02T00:00:00Z"
```

## Environment Variables

- `DATADOG_API_KEY` (required): Datadog API key
- `DATADOG_APP_KEY` (required): Datadog Application key
- `DATADOG_SITE` (optional): Datadog site (default: datadoghq.com)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
