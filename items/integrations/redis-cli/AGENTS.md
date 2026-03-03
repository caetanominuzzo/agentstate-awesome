# Redis CLI Integration

CLI tool for interacting with Redis key-value store.

## Usage

```bash
# Get a value
python scripts/integrations/redis-cli/redis_cli_tool.py get --key mykey

# Set a value with optional TTL
python scripts/integrations/redis-cli/redis_cli_tool.py set --key mykey --value "hello" --ttl 3600

# Delete a key
python scripts/integrations/redis-cli/redis_cli_tool.py del --key mykey

# List keys matching a pattern
python scripts/integrations/redis-cli/redis_cli_tool.py keys --pattern "user:*"

# Get Redis server info
python scripts/integrations/redis-cli/redis_cli_tool.py info
```

## Environment Variables

- `REDIS_URL` (required): Redis connection URL (e.g., `redis://user:pass@host:6379/0`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
