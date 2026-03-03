# Airtable Integration

CLI tool for interacting with Airtable bases and records.

## Usage

```bash
# List records from a table
python scripts/integrations/airtable/airtable_cli.py list-records --table "Tasks"

# Get a specific record
python scripts/integrations/airtable/airtable_cli.py get-record --table "Tasks" --record-id "recXXXXXXXXXXXXXX"

# Create a new record
python scripts/integrations/airtable/airtable_cli.py create-record --table "Tasks" --fields-json '{"Name": "New Task", "Status": "Todo"}'

# Update a record
python scripts/integrations/airtable/airtable_cli.py update-record --table "Tasks" --record-id "recXXXXXXXXXXXXXX" --fields-json '{"Status": "Done"}'
```

## Environment Variables

- `AIRTABLE_API_KEY` (required): Airtable personal access token or API key
- `AIRTABLE_BASE_ID` (required): The ID of your Airtable base (e.g., `appXXXXXXXXXXXXXX`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
