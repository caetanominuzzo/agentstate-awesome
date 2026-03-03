# Elasticsearch Integration

CLI tool for searching, indexing, and managing Elasticsearch indices and documents.

## Usage

```bash
# Search an index
python scripts/integrations/elasticsearch/elasticsearch_cli.py search --index my-index --query-json '{"query": {"match": {"title": "hello"}}}'

# List all indices
python scripts/integrations/elasticsearch/elasticsearch_cli.py list-indices

# Get a document by ID
python scripts/integrations/elasticsearch/elasticsearch_cli.py get-document --index my-index --id doc123

# Index a document
python scripts/integrations/elasticsearch/elasticsearch_cli.py index-document --index my-index --id doc123 --body-json '{"title": "Hello", "content": "World"}'
```

## Environment Variables

- `ELASTICSEARCH_URL` (required): Elasticsearch cluster URL (e.g., `https://localhost:9200`)
- `ELASTICSEARCH_API_KEY` (optional): Elasticsearch API key for authentication

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
