# Jira Integration

CLI tool for interacting with Jira tickets.

## Usage

```bash
# Create a ticket
python scripts/integrations/jira/jira_cli.py create --project PROJ --summary "Title" --description "Details"

# Get ticket details
python scripts/integrations/jira/jira_cli.py get --issue-key PROJ-123

# Update a ticket
python scripts/integrations/jira/jira_cli.py update --issue-key PROJ-123 --summary "New title"

# Add a comment
python scripts/integrations/jira/jira_cli.py comment --issue-key PROJ-123 --comment "Comment text"

# Search with JQL
python scripts/integrations/jira/jira_cli.py search --jql "project = PROJ AND status = 'In Progress'"
```

## Environment Variables

- `JIRA_BASE_URL` (required): Your Jira instance URL (e.g., `https://your-org.atlassian.net`)
- `JIRA_AUTH`: Pre-computed Base64(email:token), OR use:
  - `JIRA_EMAIL` + `JIRA_API_TOKEN`

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
