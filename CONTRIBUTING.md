# Contributing to agentstate-awesome

We welcome contributions! Add new tools, integrations, skills, or knowledge templates that help AI agents work better.

## Adding a New Item

1. **Fork this repository**

2. **Create a directory** under the appropriate category:
   ```
   items/<category>/<your-item-name>/
   ```
   Categories: `skills`, `integrations`, `modes`, `orchestration`, `knowledge`, `meta`

3. **Add a `manifest.yaml`** with the required fields (see schema below)

4. **Add your files** (scripts, markdown, JSON, etc.)

5. **Validate locally**:
   ```bash
   python scripts/validate-item.py items/<category>/<your-item-name>/
   ```

6. **Open a Pull Request** — CI will validate your item automatically

## manifest.yaml Schema

```yaml
# Required fields
id: my-item-name              # Must match directory name, URL-safe
name: My Item Name            # Human-readable display name
description: >                # What this item does (1-3 sentences)
  Short description of the item.
category: integrations        # skills | integrations | modes | orchestration | knowledge | meta

# Where files go in the generated repo
files:
  - src: my_script.py                           # Path relative to this item's directory
    dest: scripts/integrations/my/my_script.py   # Path in the generated repo

# Optional fields
subcategory: ""               # For UI grouping within a category
tags: []                      # Searchable tags
tech_tags: []                 # Technology/language tags (python, typescript, sql, etc.)
compatible_agents:            # Which agent platforms this works with
  - any                       # Special value meaning universal. Others: devin, claude-code, cursor, windsurf
depends_on: []                # IDs of other items this depends on
python_dependencies: []       # pip packages (e.g., "requests>=2.31.0")
env_vars: []                  # Environment variables needed (see below)
featured: false               # Highlighted in the UI
source:
  type: original              # "original" or "mirror" (for upstream skills)
```

### Environment Variables

```yaml
env_vars:
  - name: MY_API_KEY
    description: "API key for the service"
    required: true
  - name: MY_OPTIONAL_VAR
    description: "Optional configuration"
    required: false
    alternative: "Use MY_OTHER_VAR instead"
```

## Guidelines

- **One item per directory** — keep items self-contained
- **Genericize** — remove org-specific references (URLs, team names, etc.)
- **Document env vars** — every secret your script needs must be listed in the manifest
- **JSON output** — scripts should output JSON to stdout, errors to stderr
- **Non-interactive** — scripts must work without user input (no prompts, no interactive modes)
- **Proper exit codes** — 0 for success, 1 for errors
- **Include an AGENTS.md** — if your item has scripts, include an AGENTS.md explaining usage

## Mirroring Upstream Skills

To add a skill from the agents.sh ecosystem:

1. Create the directory under `items/skills/<subcategory>/`
2. Copy the `SKILL.md` from the upstream repo
3. Set `source.type: mirror` in the manifest with upstream coordinates:

```yaml
source:
  type: mirror
  repo: "owner/repo"
  path: "path/to/SKILL.md"
  last_synced: "2026-03-03"
```

The weekly sync workflow will keep mirrored skills up to date.
