# GitHub Integration

CLI tool for managing GitHub repositories, issues, and pull requests.

## Usage

```bash
# List repositories for an org
python scripts/integrations/github/github_cli.py list-repos --org my-org

# List repositories for a user
python scripts/integrations/github/github_cli.py list-repos --user octocat

# Get repository details
python scripts/integrations/github/github_cli.py get-repo --repo owner/repo

# Create an issue
python scripts/integrations/github/github_cli.py create-issue --repo owner/repo --title "Bug report" --body "Details here"

# List pull requests
python scripts/integrations/github/github_cli.py list-prs --repo owner/repo --state open

# Create a pull request
python scripts/integrations/github/github_cli.py create-pr --repo owner/repo --title "Feature X" --body "Description" --head feature-branch --base main

# Get pull request details
python scripts/integrations/github/github_cli.py get-pr --repo owner/repo --number 42
```

## Environment Variables

- `GITHUB_TOKEN` (required): GitHub Personal Access Token or fine-grained token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
