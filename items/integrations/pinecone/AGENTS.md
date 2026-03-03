# Pinecone Integration

CLI tool for managing Pinecone vector database indexes and vectors.

## Usage

```bash
# List all indexes
python scripts/integrations/pinecone/pinecone_cli.py list-indexes

# Describe an index
python scripts/integrations/pinecone/pinecone_cli.py describe-index --index "my-index"

# Query an index with a vector
python scripts/integrations/pinecone/pinecone_cli.py query --index "my-index" --vector-json "[0.1, 0.2, 0.3]" --top-k 5

# Upsert vectors
python scripts/integrations/pinecone/pinecone_cli.py upsert --index "my-index" --vectors-json '[{"id":"v1","values":[0.1,0.2,0.3]}]'

# Delete vectors by IDs
python scripts/integrations/pinecone/pinecone_cli.py delete --index "my-index" --ids-json '["v1","v2"]'
```

## Environment Variables

- `PINECONE_API_KEY` (required): Pinecone API key for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
