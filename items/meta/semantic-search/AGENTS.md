# Semantic Search

Search tool for discovering available tools, skills, and knowledge in this repository.

## Usage

```bash
# Basic search
python scripts/meta/search.py "how to create a jira ticket"

# Filter by tag
python scripts/meta/search.py --tag python "testing patterns"

# Filter by category
python scripts/meta/search.py --category integrations "notification"

# Limit results
python scripts/meta/search.py --limit 5 "deployment"
```

## Output

JSON array of results ranked by relevance:

```json
[
  {"path": "scripts/integrations/jira/AGENTS.md", "score": 0.92, "snippet": "..."},
  {"path": "skills/curated/python-testing-patterns.md", "score": 0.67, "snippet": "..."}
]
```

## How It Works

- Indexes all .md, .json, .py, .yaml files in the repo
- Uses TF-IDF ranking for relevance scoring
- Caches index in `.agentstate-index.json` (auto-rebuilds when files change)
- No external dependencies (Python stdlib only)
