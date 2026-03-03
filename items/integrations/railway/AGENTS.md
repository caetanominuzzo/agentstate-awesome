# Railway Integration

CLI tool for managing projects, services, and deployments on Railway.

## Usage

```bash
# List all projects
python scripts/integrations/railway/railway_cli.py list-projects

# Get project details
python scripts/integrations/railway/railway_cli.py get-project --project-id "project-uuid"

# List services in a project
python scripts/integrations/railway/railway_cli.py list-services --project-id "project-uuid"

# List deployments
python scripts/integrations/railway/railway_cli.py list-deployments --project-id "project-uuid"

# Get deployment details
python scripts/integrations/railway/railway_cli.py get-deployment --deployment-id "deploy-uuid"
```

## Environment Variables

- `RAILWAY_TOKEN` (required): Railway API token for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
