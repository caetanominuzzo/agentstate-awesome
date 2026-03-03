# Figma Integration

CLI tool for interacting with Figma files, comments, and exports.

## Usage

```bash
# Get a Figma file
python scripts/integrations/figma/figma_cli.py get-file --file-key "abc123def456"

# List comments on a file
python scripts/integrations/figma/figma_cli.py list-comments --file-key "abc123def456"

# Export images from specific nodes
python scripts/integrations/figma/figma_cli.py export-images --file-key "abc123def456" --node-ids "1:2,3:4" --format png

# Get file version history
python scripts/integrations/figma/figma_cli.py get-file-versions --file-key "abc123def456"
```

## Environment Variables

- `FIGMA_ACCESS_TOKEN` (required): Figma personal access token for API authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
