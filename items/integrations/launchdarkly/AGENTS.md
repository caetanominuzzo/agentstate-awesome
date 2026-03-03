# LaunchDarkly Integration

CLI tool for managing feature flags, environments, and flag toggles in LaunchDarkly.

## Usage

```bash
# List all feature flags
python scripts/integrations/launchdarkly/launchdarkly_cli.py list-flags --project-key "my-project"

# Get a specific feature flag
python scripts/integrations/launchdarkly/launchdarkly_cli.py get-flag --project-key "my-project" --flag-key "my-flag"

# Turn a flag on
python scripts/integrations/launchdarkly/launchdarkly_cli.py toggle-flag --project-key "my-project" --flag-key "my-flag" --environment "production" --on

# Turn a flag off
python scripts/integrations/launchdarkly/launchdarkly_cli.py toggle-flag --project-key "my-project" --flag-key "my-flag" --environment "production" --off

# List environments
python scripts/integrations/launchdarkly/launchdarkly_cli.py list-environments --project-key "my-project"
```

## Environment Variables

- `LAUNCHDARKLY_API_KEY` (required): LaunchDarkly API access token
- `LAUNCHDARKLY_PROJECT_KEY` (optional): Default project key (default: `default`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
