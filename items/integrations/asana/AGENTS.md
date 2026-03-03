# Asana Integration

CLI tool for managing Asana workspaces, projects, and tasks.

## Usage

```bash
# List workspaces
python scripts/integrations/asana/asana_cli.py list-workspaces

# List projects in a workspace
python scripts/integrations/asana/asana_cli.py list-projects --workspace 1234567890

# Create a task
python scripts/integrations/asana/asana_cli.py create-task --project 1234567890 --name "New task" --notes "Task details"

# Get task details
python scripts/integrations/asana/asana_cli.py get-task --task-id 1234567890

# Mark task as completed
python scripts/integrations/asana/asana_cli.py update-task --task-id 1234567890 --completed true
```

## Environment Variables

- `ASANA_ACCESS_TOKEN` (required): Asana personal access token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
