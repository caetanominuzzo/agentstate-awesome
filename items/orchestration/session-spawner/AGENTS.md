# Session Spawner & Monitor

Scripts for spawning and monitoring Devin sessions.

## Usage

```bash
# Spawn a new session
python scripts/orchestration/spawn_session.py --repo org/my-repo --task "Implement feature X"

# Spawn with context
python scripts/orchestration/spawn_session.py --repo org/my-repo --task "Continue work" --context "Previous PR: #123"

# Monitor a session
python scripts/orchestration/monitor_session.py <session-id>
```

## Environment Variables

- `DEVIN_API` (required): Bearer token for the Devin API
