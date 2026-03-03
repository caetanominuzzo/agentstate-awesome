# Notion Integration

Query and manage Notion pages and databases via the Notion API.

## Usage

```bash
# Search across all accessible pages and databases
python scripts/integrations/notion/notion_cli.py search --query "Project roadmap"

# Search for databases only
python scripts/integrations/notion/notion_cli.py search --query "Tasks" --filter-type database

# Get a specific page by ID
python scripts/integrations/notion/notion_cli.py get-page --page-id "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

# Get a database schema
python scripts/integrations/notion/notion_cli.py get-database --database-id "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

# Query a database (all rows)
python scripts/integrations/notion/notion_cli.py query-database --database-id "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

# Query a database with a filter
python scripts/integrations/notion/notion_cli.py query-database \
  --database-id "a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  --filter '{"property": "Status", "select": {"equals": "In Progress"}}'
```

## Environment Variables

- `NOTION_KEY` (required): Notion integration token (starts with `ntn_` or `secret_`).

## Commands

| Command          | Description |
|------------------|-------------|
| `search`         | Search pages and databases. Supports `--filter-type` (page/database) and `--page-size`. |
| `get-page`       | Retrieve a single page by its ID. |
| `get-database`   | Retrieve a database schema (properties, title) by its ID. |
| `query-database` | Query rows from a database. Supports `--filter` (Notion filter JSON) and `--page-size`. |

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
