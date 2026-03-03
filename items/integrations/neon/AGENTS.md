# Neon Integration

CLI tool for managing Neon serverless Postgres projects, branches, and endpoints.

## Usage

```bash
# List all projects
python scripts/integrations/neon/neon_cli.py list-projects

# Get project details
python scripts/integrations/neon/neon_cli.py get-project --project-id proj-abc123

# List branches for a project
python scripts/integrations/neon/neon_cli.py list-branches --project-id proj-abc123

# Create a new branch
python scripts/integrations/neon/neon_cli.py create-branch --project-id proj-abc123 --name "feature-x"

# List compute endpoints
python scripts/integrations/neon/neon_cli.py list-endpoints --project-id proj-abc123
```

## Environment Variables

- `NEON_API_KEY` (required): Neon API key

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
