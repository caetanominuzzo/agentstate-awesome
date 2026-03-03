# Devin API Integration

Spawn and monitor Devin sessions and manage knowledge notes (breadcrumbs) via the Devin API.

## Scripts

### devin_api_client.py

Shared HTTP client library for the Devin API. Provides `DevinAPIClient` with methods:

- `spawn_session(repo, task, context=None)` - Start a new Devin coding session.
- `get_session_status(session_id)` - Check the status of a running session.

This module is intended to be imported by other scripts:

```python
from devin_api_client import DevinAPIClient

client = DevinAPIClient()
result = client.spawn_session("org/repo", "Fix the login bug")
status = client.get_session_status(result["session_id"])
```

### manage_knowledge.py

CLI for managing Devin knowledge notes (breadcrumbs).

```bash
# List all knowledge notes
python scripts/integrations/devin/manage_knowledge.py list

# Get a specific knowledge note
python scripts/integrations/devin/manage_knowledge.py get --id NOTE_ID

# Create a new knowledge note
python scripts/integrations/devin/manage_knowledge.py create \
  --title "Coding Standards" \
  --content "Always use type hints in Python." \
  --trigger-type keyword \
  --trigger "python"

# Update an existing knowledge note
python scripts/integrations/devin/manage_knowledge.py update \
  --id NOTE_ID \
  --content "Updated content here."

# Update multiple breadcrumb notes at once
python scripts/integrations/devin/manage_knowledge.py breadcrumbs \
  --targets "ID_1,ID_2,ID_3" \
  --content "Shared breadcrumb content."
```

## Environment Variables

- `DEVIN_API` (required): Bearer token for the Devin API.

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
