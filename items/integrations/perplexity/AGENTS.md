# Perplexity Integration

CLI tool for searching and chatting with Perplexity AI models.

## Usage

```bash
# Search with Perplexity
python scripts/integrations/perplexity/perplexity_cli.py search --query "What is the latest in AI research?"

# Chat with a single message
python scripts/integrations/perplexity/perplexity_cli.py chat --message "Explain transformer architecture"

# Chat with multi-turn conversation
python scripts/integrations/perplexity/perplexity_cli.py chat --messages-json '[{"role":"user","content":"What is Rust?"},{"role":"assistant","content":"Rust is a systems programming language."},{"role":"user","content":"What are its main features?"}]'
```

## Environment Variables

- `PERPLEXITY_API_KEY` (required): Perplexity API key for authentication
- `PERPLEXITY_MODEL` (optional): Model to use for completions (default: `sonar`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
