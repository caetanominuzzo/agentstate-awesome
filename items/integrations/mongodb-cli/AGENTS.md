# MongoDB CLI Integration

CLI tool for querying and managing MongoDB databases and collections.

## Usage

```bash
# List databases
python scripts/integrations/mongodb-cli/mongodb_cli.py list-databases

# List collections in a database
python scripts/integrations/mongodb-cli/mongodb_cli.py list-collections --database mydb

# Find documents
python scripts/integrations/mongodb-cli/mongodb_cli.py find --database mydb --collection users --filter-json '{"active": true}' --limit 10

# Count documents
python scripts/integrations/mongodb-cli/mongodb_cli.py count --database mydb --collection users --filter-json '{"active": true}'
```

## Environment Variables

- `MONGODB_URI` (required): MongoDB connection URI (e.g., `mongodb://user:pass@host:27017`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
