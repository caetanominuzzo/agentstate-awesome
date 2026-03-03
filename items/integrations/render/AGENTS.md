# Render Integration

CLI tool for managing services, deployments, and environment variables on Render.

## Usage

```bash
# List all services
python scripts/integrations/render/render_cli.py list-services

# Get service details
python scripts/integrations/render/render_cli.py get-service --service-id "srv-xxxxxxxxxxxxx"

# List deploys for a service
python scripts/integrations/render/render_cli.py list-deploys --service-id "srv-xxxxxxxxxxxxx"

# Trigger a new deploy
python scripts/integrations/render/render_cli.py trigger-deploy --service-id "srv-xxxxxxxxxxxxx"

# List environment variables
python scripts/integrations/render/render_cli.py list-envs --service-id "srv-xxxxxxxxxxxxx"
```

## Environment Variables

- `RENDER_API_KEY` (required): Render API key for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
