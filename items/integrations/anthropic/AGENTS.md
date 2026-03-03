# Anthropic Integration

CLI tool for interacting with Anthropic Claude models via the official SDK.

## Usage

```bash
# Send a chat message
python scripts/integrations/anthropic/anthropic_cli.py chat --message "Explain Kubernetes in one paragraph"

# Send a multi-turn conversation
python scripts/integrations/anthropic/anthropic_cli.py chat --messages-json '[{"role":"user","content":"What is Python?"},{"role":"assistant","content":"Python is a programming language."},{"role":"user","content":"What is it used for?"}]'

# Count tokens in text
python scripts/integrations/anthropic/anthropic_cli.py count-tokens --text "The quick brown fox jumps over the lazy dog"
```

## Environment Variables

- `ANTHROPIC_API_KEY` (required): Anthropic API key
- `ANTHROPIC_MODEL` (optional): Default model to use (default: claude-sonnet-4-20250514)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
