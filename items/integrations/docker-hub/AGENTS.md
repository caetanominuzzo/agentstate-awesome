# Docker Hub Integration

CLI tool for listing repositories, tags, and searching images on Docker Hub.

## Usage

```bash
# List repositories
python scripts/integrations/docker-hub/docker_hub_cli.py list-repos --namespace "myorg"

# List tags for a repository
python scripts/integrations/docker-hub/docker_hub_cli.py list-tags --repo "library/nginx"

# Get repository details
python scripts/integrations/docker-hub/docker_hub_cli.py get-repo --repo "library/nginx"

# Search for images
python scripts/integrations/docker-hub/docker_hub_cli.py search --query "python"
```

## Environment Variables

- `DOCKERHUB_USERNAME` (required): Docker Hub username for authentication
- `DOCKERHUB_TOKEN` (required): Docker Hub personal access token or password

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
