# Groq Integration

CLI tool for chatting with Groq-hosted LLMs and listing available models.

## Usage

```bash
# Send a chat message
python scripts/integrations/groq/groq_cli.py chat --message "Explain quantum computing in simple terms"

# Send a multi-turn conversation
python scripts/integrations/groq/groq_cli.py chat --messages-json '[{"role":"system","content":"You are helpful."},{"role":"user","content":"Hi"}]'

# List available models
python scripts/integrations/groq/groq_cli.py list-models
```

## Environment Variables

- `GROQ_API_KEY` (required): Groq API key for authentication
- `GROQ_MODEL` (optional): Model to use for chat completions (default: `llama-3.3-70b-versatile`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
