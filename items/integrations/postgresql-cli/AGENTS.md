# PostgreSQL CLI Integration

CLI tool for querying and managing PostgreSQL databases.

## Usage

```bash
# Execute a SQL query
python scripts/integrations/postgresql-cli/postgresql_cli.py query --sql "SELECT * FROM users LIMIT 10"

# List all tables
python scripts/integrations/postgresql-cli/postgresql_cli.py list-tables

# Describe a table
python scripts/integrations/postgresql-cli/postgresql_cli.py describe-table --table users

# List all databases
python scripts/integrations/postgresql-cli/postgresql_cli.py list-databases
```

## Environment Variables

- `POSTGRES_URL` (required): PostgreSQL connection URL (e.g., `postgresql://user:pass@host:5432/db`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
