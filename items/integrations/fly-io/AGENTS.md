# Fly.io Integration

CLI tool for managing apps and machines on Fly.io.

## Usage

```bash
# List all apps
python scripts/integrations/fly-io/fly_io_cli.py list-apps

# Get app details
python scripts/integrations/fly-io/fly_io_cli.py get-app --app-name "my-app"

# List machines for an app
python scripts/integrations/fly-io/fly_io_cli.py list-machines --app-name "my-app"

# Get machine details
python scripts/integrations/fly-io/fly_io_cli.py get-machine --app-name "my-app" --machine-id "machine-uuid"
```

## Environment Variables

- `FLY_API_TOKEN` (required): Fly.io API token for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
