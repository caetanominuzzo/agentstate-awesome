# Netlify Integration

CLI tool for managing Netlify sites and deploys.

## Usage

```bash
# List all sites
python scripts/integrations/netlify/netlify_cli.py list-sites

# Get site details
python scripts/integrations/netlify/netlify_cli.py get-site --site-id my-site-id

# List deploys for a site
python scripts/integrations/netlify/netlify_cli.py list-deploys --site-id my-site-id

# Trigger a new deploy
python scripts/integrations/netlify/netlify_cli.py trigger-deploy --site-id my-site-id
```

## Environment Variables

- `NETLIFY_AUTH_TOKEN` (required): Netlify personal access token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
