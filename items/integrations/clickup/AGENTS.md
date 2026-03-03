# ClickUp Integration

CLI tool for managing ClickUp teams, spaces, and tasks.

## Usage

```bash
# List teams
python scripts/integrations/clickup/clickup_cli.py list-teams

# List spaces in a team
python scripts/integrations/clickup/clickup_cli.py list-spaces --team-id 1234567

# List tasks in a list
python scripts/integrations/clickup/clickup_cli.py list-tasks --list-id 7654321

# Create a task
python scripts/integrations/clickup/clickup_cli.py create-task --list-id 7654321 --name "New task" --description "Task details"

# Update a task status
python scripts/integrations/clickup/clickup_cli.py update-task --task-id abc123 --status "in progress"
```

## Environment Variables

- `CLICKUP_API_TOKEN` (required): ClickUp personal API token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
