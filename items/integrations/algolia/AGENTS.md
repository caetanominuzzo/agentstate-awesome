# Algolia Integration

CLI tool for searching indices, listing indices, and managing objects in Algolia.

## Usage

```bash
# Search an index
python scripts/integrations/algolia/algolia_cli.py search --index "products" --query "laptop"

# List all indices
python scripts/integrations/algolia/algolia_cli.py list-indices

# Get an object by ID
python scripts/integrations/algolia/algolia_cli.py get-object --index "products" --object-id "product-123"

# Add an object to an index
python scripts/integrations/algolia/algolia_cli.py add-object --index "products" --body-json '{"name": "Laptop", "price": 999}'
```

## Environment Variables

- `ALGOLIA_APP_ID` (required): Algolia application ID
- `ALGOLIA_API_KEY` (required): Algolia API key (admin or search key depending on operation)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
