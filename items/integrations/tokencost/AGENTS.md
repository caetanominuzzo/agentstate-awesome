# Token Cost — LLM Pricing CLI

Query LLM token pricing from OpenRouter (300+ models, all major vendors). No API key needed.

## Commands

```bash
# Get pricing for a specific model
python tokencost_cli.py get anthropic/claude-sonnet-4

# Calculate cost for a workload
python tokencost_cli.py cost anthropic/claude-sonnet-4 --input-tokens 10000 --output-tokens 2000

# Compare cheapest models for a workload
python tokencost_cli.py compare --input-tokens 10000 --output-tokens 2000 --top 10

# Compare only specific vendors
python tokencost_cli.py compare --input-tokens 10000 --output-tokens 2000 --vendor openai,anthropic,google

# List all models from a vendor, sorted by input price
python tokencost_cli.py list --vendor anthropic --sort-by input

# Dump full normalized pricing JSON (all models)
python tokencost_cli.py dump
```

## Output format

All output is JSON. Prices are normalized to **USD per 1M tokens**.

## Data source

OpenRouter API (`https://openrouter.ai/api/v1/models`) — no auth required, updated continuously.
