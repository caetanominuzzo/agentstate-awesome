# PostHog Integration

CLI tool for capturing events, running queries, and listing feature flags in PostHog.

## Usage

```bash
# Capture an event
python scripts/integrations/posthog/posthog_cli.py capture --event "page_view" --distinct-id "user-123" --properties-json '{"url":"/home"}'

# Run a HogQL query
python scripts/integrations/posthog/posthog_cli.py query --query-json '{"kind":"HogQLQuery","query":"SELECT count() FROM events WHERE event = '\''page_view'\''"}'

# List feature flags
python scripts/integrations/posthog/posthog_cli.py list-feature-flags
```

## Environment Variables

- `POSTHOG_API_KEY` (required): PostHog personal API key
- `POSTHOG_HOST` (optional): PostHog instance URL (default: https://app.posthog.com)

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
