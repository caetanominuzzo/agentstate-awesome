# MySQL CLI Integration

CLI tool for querying and managing MySQL databases.

## Usage

```bash
# Execute a SQL query
python scripts/integrations/mysql-cli/mysql_cli.py query --sql "SELECT * FROM users LIMIT 10"

# List all tables
python scripts/integrations/mysql-cli/mysql_cli.py list-tables

# Describe a table
python scripts/integrations/mysql-cli/mysql_cli.py describe-table --table users

# List all databases
python scripts/integrations/mysql-cli/mysql_cli.py list-databases
```

## Environment Variables

- `MYSQL_HOST` (required): MySQL server hostname
- `MYSQL_USER` (required): MySQL username
- `MYSQL_PASSWORD` (required): MySQL password
- `MYSQL_DATABASE` (required): MySQL database name
- `MYSQL_PORT` (optional): MySQL port (default: 3306)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
