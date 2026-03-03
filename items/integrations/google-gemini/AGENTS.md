# Google Gemini Integration

CLI tool for chatting with Google Gemini models and listing available models.

## Usage

```bash
# Send a chat message
python scripts/integrations/google-gemini/google_gemini_cli.py chat --message "Explain machine learning"

# List available models
python scripts/integrations/google-gemini/google_gemini_cli.py list-models
```

## Environment Variables

- `GEMINI_API_KEY` (required): Google Gemini API key for authentication
- `GEMINI_MODEL` (optional): Model to use for generation (default: `gemini-2.0-flash`)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
