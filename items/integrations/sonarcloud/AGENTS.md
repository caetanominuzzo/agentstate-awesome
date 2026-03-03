# SonarCloud Integration

CLI tool for listing projects, retrieving code quality measures, and searching issues in SonarCloud.

## Usage

```bash
# List all projects
python scripts/integrations/sonarcloud/sonarcloud_cli.py list-projects

# Get measures for a project
python scripts/integrations/sonarcloud/sonarcloud_cli.py get-measures --project-key "my-project" --metrics "coverage,bugs,vulnerabilities"

# List issues by severity
python scripts/integrations/sonarcloud/sonarcloud_cli.py list-issues --project-key "my-project" --severities "BLOCKER,CRITICAL"

# Search issues with a query
python scripts/integrations/sonarcloud/sonarcloud_cli.py search-issues --project-key "my-project" --query "null pointer"
```

## Environment Variables

- `SONAR_TOKEN` (required): SonarCloud authentication token
- `SONAR_ORG` (required): SonarCloud organization key

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
