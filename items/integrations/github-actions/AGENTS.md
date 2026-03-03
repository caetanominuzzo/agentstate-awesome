# GitHub Actions Integration

CLI tool for managing GitHub Actions workflows and runs.

## Usage

```bash
# List workflows
python scripts/integrations/github-actions/github_actions_cli.py list-workflows --repo owner/repo

# List workflow runs
python scripts/integrations/github-actions/github_actions_cli.py list-runs --repo owner/repo
python scripts/integrations/github-actions/github_actions_cli.py list-runs --repo owner/repo --workflow-id ci.yml

# Trigger a workflow dispatch
python scripts/integrations/github-actions/github_actions_cli.py trigger-workflow --repo owner/repo --workflow-id ci.yml --ref main

# Get run details
python scripts/integrations/github-actions/github_actions_cli.py get-run --repo owner/repo --run-id 123456

# Cancel a run
python scripts/integrations/github-actions/github_actions_cli.py cancel-run --repo owner/repo --run-id 123456

# List jobs for a run
python scripts/integrations/github-actions/github_actions_cli.py list-run-jobs --repo owner/repo --run-id 123456
```

## Environment Variables

- `GITHUB_TOKEN` (required): GitHub Personal Access Token with actions scope

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
