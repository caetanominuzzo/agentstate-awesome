# GitLab Integration

CLI tool for managing GitLab projects, merge requests, issues, and pipelines.

## Usage

```bash
# List accessible projects
python scripts/integrations/gitlab/gitlab_cli.py list-projects

# Get project details
python scripts/integrations/gitlab/gitlab_cli.py get-project --project-id 12345

# List merge requests
python scripts/integrations/gitlab/gitlab_cli.py list-merge-requests --project-id 12345 --state opened

# Create an issue
python scripts/integrations/gitlab/gitlab_cli.py create-issue --project-id 12345 --title "Bug report" --description "Details here"

# List pipelines
python scripts/integrations/gitlab/gitlab_cli.py list-pipelines --project-id 12345
```

## Environment Variables

- `GITLAB_TOKEN` (required): GitLab personal access token
- `GITLAB_BASE_URL` (optional): GitLab instance URL (default: `https://gitlab.com`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
