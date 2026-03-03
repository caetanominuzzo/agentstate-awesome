# Grafana Integration

CLI tool for managing Grafana dashboards, alerts, and datasource queries.

## Usage

```bash
# List dashboards
python scripts/integrations/grafana/grafana_cli.py list-dashboards

# Get dashboard by UID
python scripts/integrations/grafana/grafana_cli.py get-dashboard --uid abc123

# List alerts
python scripts/integrations/grafana/grafana_cli.py list-alerts

# Query a datasource
python scripts/integrations/grafana/grafana_cli.py query-datasource --datasource-id 1 --query-json '{"refId": "A", "expr": "up"}'
```

## Environment Variables

- `GRAFANA_URL` (required): Grafana instance URL (e.g., `https://your-grafana.example.com`)
- `GRAFANA_API_KEY` (required): Grafana API key or service account token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
