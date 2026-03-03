# CircleCI Integration

CLI tool for managing CircleCI pipelines, workflows, and jobs.

## Usage

```bash
# List pipelines for a project
python scripts/integrations/circleci/circleci_cli.py list-pipelines --project-slug gh/my-org/my-repo

# Get pipeline details
python scripts/integrations/circleci/circleci_cli.py get-pipeline --pipeline-id 12345678-abcd-1234-abcd-123456789abc

# List workflows for a pipeline
python scripts/integrations/circleci/circleci_cli.py list-workflows --pipeline-id 12345678-abcd-1234-abcd-123456789abc

# Trigger a new pipeline
python scripts/integrations/circleci/circleci_cli.py trigger-pipeline --project-slug gh/my-org/my-repo --branch main

# List jobs for a workflow
python scripts/integrations/circleci/circleci_cli.py list-jobs --workflow-id 12345678-abcd-1234-abcd-123456789abc
```

## Environment Variables

- `CIRCLECI_TOKEN` (required): CircleCI personal API token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
