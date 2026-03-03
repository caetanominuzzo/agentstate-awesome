# Multi-Layer Orchestration Handoff Template

**Purpose**: Generic handoff template for multi-layer orchestration projects with Root -> L2 Orchestrators -> Agents architecture.

---

## Parameters (Replace Before Use)

```
{{REPO}}                    = Repository name
{{ROOT_FEATURE_BRANCH}}     = Root feature branch (e.g., feature/my-project)
{{AGENT_API_KEY}}           = Agent platform API key (env var name)
{{AGENT_API_BASE}}          = Agent platform API base URL
{{RESOURCE_HANDOFF}}        = Handoff threshold (e.g., 3.5 units)
{{STATE_FILE}}              = Path to state tracking file
```

---

## Roles & Reporting Chain

- **Agents** -> Report to **Level-2 Orchestrators (L2)**
- **L2 Orchestrators** -> Report to **Root Orchestrator**
- **Root Orchestrator** -> Only blocks on user if blocking question exists

---

## Branching & PR Flow (Feature-over-Feature)

1. Root creates `{{ROOT_FEATURE_BRANCH}}` from base branch
2. Each L2/Agent creates feature branch from `{{ROOT_FEATURE_BRANCH}}`
3. **All PRs target `{{ROOT_FEATURE_BRANCH}}`** (NOT main)
4. **Agents open PRs** -> **L2 reviews/approves** -> **Agents merge** when CI passes
5. Root creates final integration PR from `{{ROOT_FEATURE_BRANCH}}` -> main when complete

---

## Active Monitoring (60s, Non-Blocking)

Root & L2 orchestrators poll sub-sessions every 60 seconds.

**Rules**:
- Report progress **non-blocking** (don't wait for user response)
- Keep messages **minimal** (save resources)
- **Only block on user** if Root has a blocking question

---

## Event Schema (Upward Reporting)

Agents/L2 emit events to parent orchestrator:

```json
{
  "type": "milestone|status|blocker",
  "component": "{{component_name}}",
  "name": "{{event_name}}",
  "artifacts": {
    "pr_url": "https://github.com/...",
    "key": "value"
  },
  "timestamp": "2025-11-19T10:00:00Z",
  "next_steps": ["step1", "step2"],
  "session_id": "{{SUB_SESSION_ID}}"
}
```

---

## State File (Single Source of Truth)

**Path**: `{{STATE_FILE}}`

```json
{
  "sessions": [
    {
      "id": "{{SESSION_ID}}",
      "role": "agent|l2|root",
      "component": "{{component_name}}",
      "status": "active|completed|blocked",
      "pr_url": "https://github.com/..."
    }
  ],
  "milestones": [
    {
      "name": "{{milestone_name}}",
      "status": "pending|completed",
      "timestamp": "2025-11-19T10:00:00Z"
    }
  ],
  "last_update": "2025-11-19T10:00:00Z",
  "resources_used": 0.0
}
```

**Update after every significant event**.

---

## Handoff Policy (Root Only)

- **Only Root Orchestrator** performs handoff
- **Handoff when**: Resource usage >= `{{RESOURCE_HANDOFF}}`
- **Handoff includes**:
  - Current session ID
  - Open items and blockers
  - All PR links and CI status
  - Sub-session states (active/completed)
  - State file path
  - Next steps

---

## Messaging Policy

**DO**:
- Keep messages **shortest possible**
- Report **significant events only** (milestone, blocker, completion)
- Use **non-blocking messages** for progress updates

**DON'T**:
- Block on user unless Root has a **blocking question**
- Send verbose explanations or unnecessary updates
- Wait for user acknowledgment of progress reports

---

## Architecture Diagram

```
Root Orchestrator (this session)
    |-> L2 Orchestrator 1
    |       |-> Agent 1.1 (feature/component-a)
    |       |-> Agent 1.2 (feature/component-b)
    |
    |-> L2 Orchestrator 2
    |       |-> Agent 2.1 (feature/component-c)
    |       |-> Agent 2.2 (feature/component-d)
    |
    |-> L2 Orchestrator 3
            |-> Agent 3.1 (feature/component-e)

All PRs -> {{ROOT_FEATURE_BRANCH}}
Final PR: {{ROOT_FEATURE_BRANCH}} -> main
```

---

## Git & PR Guidelines

**PR Requirements**:
- Target: `{{ROOT_FEATURE_BRANCH}}`
- Include session link in description

**Git Rules**:
- NEVER force push
- NEVER skip hooks (--no-verify)
- NEVER amend commits
- NEVER push directly to main

---

## Checklists

### Immediate Actions (First 10 Minutes)
- [ ] Create `{{ROOT_FEATURE_BRANCH}}` from base
- [ ] Spawn L2 orchestrators
- [ ] L2 spawn Agents
- [ ] Initialize `{{STATE_FILE}}`
- [ ] Start 60-second monitoring loop

### Ongoing Operations
- [ ] Agents implement features -> open PRs to `{{ROOT_FEATURE_BRANCH}}`
- [ ] L2 reviews PRs -> Agents merge when CI passes
- [ ] Update `{{STATE_FILE}}` after each milestone
- [ ] Report concise progress (non-blocking)
- [ ] Monitor resource usage

### Handoff (Root Only)
- [ ] Document current session ID
- [ ] List all open PRs and CI status
- [ ] List all sub-session states
- [ ] Document blockers and next steps
- [ ] Create handoff document
- [ ] Spawn new Root Orchestrator

---

## Success Criteria

- [ ] All Agents completed their work
- [ ] All PRs merged to `{{ROOT_FEATURE_BRANCH}}`
- [ ] All CI checks passing
- [ ] All milestones achieved
- [ ] Documentation complete
- [ ] Final integration PR ready
