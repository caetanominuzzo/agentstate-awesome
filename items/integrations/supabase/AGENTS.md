# Supabase Integration

CLI tool for querying, inserting, and updating data in Supabase via PostgREST.

## Usage

```bash
# Query rows from a table
python scripts/integrations/supabase/supabase_cli.py query --table users --select "id,name,email"

# Query with a filter
python scripts/integrations/supabase/supabase_cli.py query --table users --filter "id=eq.5"

# Insert a row
python scripts/integrations/supabase/supabase_cli.py insert --table users --data-json '{"name":"Alice","email":"alice@example.com"}'

# Update rows matching a filter
python scripts/integrations/supabase/supabase_cli.py update --table users --data-json '{"name":"Bob"}' --filter "id=eq.5"

# List all tables
python scripts/integrations/supabase/supabase_cli.py list-tables
```

## Environment Variables

- `SUPABASE_URL` (required): Supabase project URL (e.g., https://xxxx.supabase.co)
- `SUPABASE_KEY` (required): Supabase anon or service role API key

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
