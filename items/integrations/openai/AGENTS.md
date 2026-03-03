# OpenAI Integration

CLI tool for interacting with OpenAI models via the official SDK.

## Usage

```bash
# Send a chat message
python scripts/integrations/openai/openai_cli.py chat --message "Explain Docker in one paragraph"

# Send a multi-turn conversation
python scripts/integrations/openai/openai_cli.py chat --messages-json '[{"role":"system","content":"You are helpful."},{"role":"user","content":"Hello"}]'

# Generate embeddings
python scripts/integrations/openai/openai_cli.py embed --text "The quick brown fox"

# List available models
python scripts/integrations/openai/openai_cli.py list-models
```

## Environment Variables

- `OPENAI_API_KEY` (required): OpenAI API key
- `OPENAI_MODEL` (optional): Default model to use (default: gpt-4o)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
