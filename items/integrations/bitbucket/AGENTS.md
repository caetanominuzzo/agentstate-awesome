# Bitbucket Integration

CLI tool for managing Bitbucket repositories and pull requests.

## Usage

```bash
# List repositories in a workspace
python scripts/integrations/bitbucket/bitbucket_cli.py list-repos --workspace my-workspace

# Get repository details
python scripts/integrations/bitbucket/bitbucket_cli.py get-repo --workspace my-workspace --repo-slug my-repo

# List pull requests
python scripts/integrations/bitbucket/bitbucket_cli.py list-prs --workspace my-workspace --repo-slug my-repo --state OPEN

# Create a pull request
python scripts/integrations/bitbucket/bitbucket_cli.py create-pr --workspace my-workspace --repo-slug my-repo --title "Feature branch" --source-branch feature/new --dest-branch main
```

## Environment Variables

- `BITBUCKET_USERNAME` (required): Bitbucket username
- `BITBUCKET_APP_PASSWORD` (required): Bitbucket app password
- `BITBUCKET_WORKSPACE` (optional): Default Bitbucket workspace slug

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
