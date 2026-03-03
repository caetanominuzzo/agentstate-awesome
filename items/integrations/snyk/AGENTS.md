# Snyk Integration

CLI tool for listing organizations, projects, and security issues in Snyk.

## Usage

```bash
# List all organizations
python scripts/integrations/snyk/snyk_cli.py list-orgs

# List projects in an organization
python scripts/integrations/snyk/snyk_cli.py list-projects --org-id "org-uuid-here"

# List issues for a project
python scripts/integrations/snyk/snyk_cli.py list-issues --org-id "org-uuid-here" --project-id "project-uuid-here"

# Test a project
python scripts/integrations/snyk/snyk_cli.py test-project --org-id "org-uuid-here" --project-id "project-uuid-here"
```

## Environment Variables

- `SNYK_TOKEN` (required): Snyk API token for authentication
- `SNYK_ORG_ID` (optional): Default Snyk organization ID

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
