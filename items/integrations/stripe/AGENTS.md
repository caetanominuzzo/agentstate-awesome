# Stripe Integration

CLI tool for managing Stripe customers, charges, subscriptions, and balance.

## Usage

```bash
# List customers
python scripts/integrations/stripe/stripe_cli.py list-customers

# Get customer details
python scripts/integrations/stripe/stripe_cli.py get-customer --customer-id cus_abc123

# List recent charges
python scripts/integrations/stripe/stripe_cli.py list-charges --limit 20

# List subscriptions for a customer
python scripts/integrations/stripe/stripe_cli.py list-subscriptions --customer-id cus_abc123

# Get current balance
python scripts/integrations/stripe/stripe_cli.py get-balance
```

## Environment Variables

- `STRIPE_SECRET_KEY` (required): Stripe secret API key (starts with `sk_`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
