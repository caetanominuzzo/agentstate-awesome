# Linear Integration

CLI tool for managing Linear issues via the GraphQL API.

## Usage

```bash
# List all issues
python scripts/integrations/linear/linear_cli.py list-issues

# List issues for a specific team
python scripts/integrations/linear/linear_cli.py list-issues --team ENG

# Create an issue
python scripts/integrations/linear/linear_cli.py create-issue --team ENG --title "Bug fix" --description "Fix the login bug"

# Update an issue
python scripts/integrations/linear/linear_cli.py update-issue --issue-id abc123 --state "In Progress"
python scripts/integrations/linear/linear_cli.py update-issue --issue-id abc123 --title "New title"

# Get issue details
python scripts/integrations/linear/linear_cli.py get-issue --issue-id abc123
```

## Environment Variables

- `LINEAR_API_KEY` (required): Linear personal API key

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
