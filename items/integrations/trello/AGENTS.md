# Trello Integration

CLI tool for managing Trello boards, lists, and cards.

## Usage

```bash
# List boards
python scripts/integrations/trello/trello_cli.py list-boards

# List lists on a board
python scripts/integrations/trello/trello_cli.py list-lists --board-id abc123

# List cards in a list
python scripts/integrations/trello/trello_cli.py list-cards --list-id def456

# Create a card
python scripts/integrations/trello/trello_cli.py create-card --list-id def456 --name "New card" --desc "Card description"

# Update a card
python scripts/integrations/trello/trello_cli.py update-card --card-id ghi789 --name "Updated name" --closed true
```

## Environment Variables

- `TRELLO_API_KEY` (required): Trello API key
- `TRELLO_TOKEN` (required): Trello authorization token

## Output

All commands output JSON to stdout. Errors output JSON to stderr with exit code 1.
