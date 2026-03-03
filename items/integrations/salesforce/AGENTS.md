# Salesforce Integration

CLI tool for querying and managing Salesforce records via SOQL and REST API.

## Usage

```bash
# Execute a SOQL query
python scripts/integrations/salesforce/salesforce_cli.py query --soql "SELECT Id, Name FROM Account LIMIT 10"

# Get a record
python scripts/integrations/salesforce/salesforce_cli.py get-record --sobject Account --id 001xx000003DGbYAAW

# Create a record
python scripts/integrations/salesforce/salesforce_cli.py create-record --sobject Account --data-json '{"Name": "Acme Corp"}'

# Update a record
python scripts/integrations/salesforce/salesforce_cli.py update-record --sobject Account --id 001xx000003DGbYAAW --data-json '{"Name": "Acme Corp Updated"}'

# Describe an sObject
python scripts/integrations/salesforce/salesforce_cli.py describe --sobject Account
```

## Environment Variables

- `SALESFORCE_INSTANCE_URL` (required): Salesforce instance URL (e.g., `https://your-org.my.salesforce.com`)
- `SALESFORCE_ACCESS_TOKEN` (required): Salesforce OAuth access token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
