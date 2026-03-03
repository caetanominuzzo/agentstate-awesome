# Cloudflare Integration

CLI tool for managing Cloudflare zones, DNS records, and Workers.

## Usage

```bash
# List all zones
python scripts/integrations/cloudflare/cloudflare_cli.py list-zones

# List DNS records for a zone
python scripts/integrations/cloudflare/cloudflare_cli.py list-dns-records --zone-id abc123

# Create a DNS record
python scripts/integrations/cloudflare/cloudflare_cli.py create-dns-record --zone-id abc123 --type A --name "api.example.com" --content "1.2.3.4"

# List Workers scripts
python scripts/integrations/cloudflare/cloudflare_cli.py list-workers
```

## Environment Variables

- `CLOUDFLARE_API_TOKEN` (required): Cloudflare API token with appropriate permissions

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
