# Upstash Integration

CLI tool for interacting with Upstash Redis via the REST API.

## Usage

```bash
# Get a key's value
python scripts/integrations/upstash/upstash_cli.py get --key "my-key"

# Set a key-value pair
python scripts/integrations/upstash/upstash_cli.py set --key "my-key" --value "my-value"

# Set a key with expiry (60 seconds)
python scripts/integrations/upstash/upstash_cli.py set --key "session" --value "data" --ex 60

# Delete a key
python scripts/integrations/upstash/upstash_cli.py del --key "my-key"

# List keys matching a pattern
python scripts/integrations/upstash/upstash_cli.py keys --pattern "user:*"

# Increment a counter
python scripts/integrations/upstash/upstash_cli.py incr --key "page-views"
```

## Environment Variables

- `UPSTASH_REDIS_REST_URL` (required): Upstash Redis REST URL
- `UPSTASH_REDIS_REST_TOKEN` (required): Upstash Redis REST token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
