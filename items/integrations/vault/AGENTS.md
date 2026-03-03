# HashiCorp Vault Integration

CLI tool for reading, writing, listing, and deleting secrets in HashiCorp Vault.

## Usage

```bash
# Read a secret
python scripts/integrations/vault/vault_cli.py read --path "secret/data/myapp"

# Write a secret
python scripts/integrations/vault/vault_cli.py write --path "secret/data/myapp" --data-json '{"data": {"username": "admin", "password": "s3cret"}}'

# List secrets at a path
python scripts/integrations/vault/vault_cli.py list --path "secret/metadata/"

# Delete a secret
python scripts/integrations/vault/vault_cli.py delete --path "secret/data/myapp"
```

## Environment Variables

- `VAULT_ADDR` (required): Vault server address (e.g., `https://vault.example.com`)
- `VAULT_TOKEN` (required): Vault authentication token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
