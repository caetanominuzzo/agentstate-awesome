# Vercel Integration

CLI tool for managing Vercel projects and deployments.

## Usage

```bash
# List all projects
python scripts/integrations/vercel/vercel_cli.py list-projects

# List deployments
python scripts/integrations/vercel/vercel_cli.py list-deployments --project my-project

# Get deployment details
python scripts/integrations/vercel/vercel_cli.py get-deployment --deployment-id dpl_xxxxx

# Trigger a new deployment
python scripts/integrations/vercel/vercel_cli.py trigger-deploy --project my-project
```

## Environment Variables

- `VERCEL_TOKEN` (required): Vercel authentication token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
