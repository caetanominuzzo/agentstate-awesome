# Monday.com Integration

CLI tool for managing boards, items, and groups on Monday.com.

## Usage

```bash
# List all boards
python scripts/integrations/monday/monday_cli.py list-boards

# Get board details
python scripts/integrations/monday/monday_cli.py get-board --board-id "123456789"

# List items on a board
python scripts/integrations/monday/monday_cli.py list-items --board-id "123456789"

# Create a new item
python scripts/integrations/monday/monday_cli.py create-item --board-id "123456789" --group-id "new_group" --name "My Task"

# Update an item's column values
python scripts/integrations/monday/monday_cli.py update-item --item-id "987654321" --board-id "123456789" --column-values-json '{"status": {"label": "Done"}}'
```

## Environment Variables

- `MONDAY_API_TOKEN` (required): Monday.com API token for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
