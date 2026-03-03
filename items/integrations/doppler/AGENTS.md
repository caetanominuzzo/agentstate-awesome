# Doppler Integration

CLI tool for managing projects, configs, and secrets in Doppler.

## Usage

```bash
# List all projects
python scripts/integrations/doppler/doppler_cli.py list-projects

# List configs for a project
python scripts/integrations/doppler/doppler_cli.py list-configs --project "my-project"

# Get all secrets for a project config
python scripts/integrations/doppler/doppler_cli.py get-secrets --project "my-project" --config "production"

# Get a single secret
python scripts/integrations/doppler/doppler_cli.py get-secret --project "my-project" --config "production" --name "DATABASE_URL"
```

## Environment Variables

- `DOPPLER_TOKEN` (required): Doppler service token or personal token for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
