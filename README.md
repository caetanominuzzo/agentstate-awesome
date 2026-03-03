# agentstate-awesome

A curated collection of tools, skills, integrations, and knowledge templates for [Agent State](https://agentstate.tech) repositories.

Browse and select items at **[agentstate.tech](https://agentstate.tech)** to assemble your own agent-state repo.

## What's Inside

| Category | Description |
|----------|-------------|
| **Skills** | Reusable procedural knowledge from the agents.sh ecosystem |
| **Integrations** | Scripts connecting agents to external services (Jira, Telegram, Devin, Notion) |
| **Modes** | Behavioral profiles that change how agents operate |
| **Orchestration** | Multi-agent coordination, handoff, and session management patterns |
| **Knowledge** | Organizational context templates and memory structures |
| **Meta** | Tools for the agent-state repo itself (search, indexing) |

## How It Works

1. Visit [agentstate.tech](https://agentstate.tech)
2. Select the tools and skills you want
3. Download as ZIP or create a GitHub repo directly
4. Run `setup.sh` to configure your environment variables
5. Tell your agents about the repo via AGENTS.md

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new items to this collection.

## Structure

Each item lives in `items/<category>/<item-name>/` with a `manifest.yaml` describing its metadata, dependencies, and required environment variables. The `collection.json` at the root is auto-generated from all manifests.

## License

MIT
