# Sentry Integration

CLI tool for listing, inspecting, and resolving Sentry issues and projects.

## Usage

```bash
# List unresolved issues for a project
python scripts/integrations/sentry/sentry_cli.py list-issues --project my-project

# Get issue details
python scripts/integrations/sentry/sentry_cli.py get-issue --issue-id 123456

# List all projects in the organization
python scripts/integrations/sentry/sentry_cli.py list-projects

# Resolve an issue
python scripts/integrations/sentry/sentry_cli.py resolve-issue --issue-id 123456
```

## Environment Variables

- `SENTRY_AUTH_TOKEN` (required): Sentry authentication token
- `SENTRY_ORG` (required): Sentry organization slug
- `SENTRY_PROJECT` (optional): Default project slug (used when --project is not specified)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
