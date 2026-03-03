# Resource Limit Enforcement & Automatic Handoff Protocol

Behavior profile that enforces session resource limits, triggers automatic handoff, and monitors continued usage.

---

## Trigger

This flow activates when a session is approaching or has exceeded the configured resource limit.

---

## Phase 1: Proactive Alert (at ~80% of limit)

When the session reaches approximately 80% of the resource limit:

1. **Alert the user** that the session is approaching the limit.
2. **Automatically spawn a new session** with full handoff context:
   - Original task description
   - Work completed so far
   - Open PRs and CI status
   - Current branch/repo
   - Pending items and next steps
3. **Share the new session link** with the user and suggest they continue work there.

---

## Phase 2: Post-Limit Warning

If the user sends any new message after the limit has been reached, warn them that continued usage will incur additional costs, and recommend switching to the new session.

---

## Phase 3: Continued Usage Monitoring

If the user continues after the warning:

1. Send a notification (e.g., via Telegram) documenting the over-limit usage.
2. Continue working on the request normally.
3. Repeat the warning cycle for every additional ~20% consumed beyond the limit.

---

## Key Principles

- The handoff session MUST be spawned automatically — do not just suggest it, actually create it.
- The warning must be sent before any other response when over limit.
- Notifications are mandatory for continued usage past the limit.
- This protocol applies to ALL sessions, regardless of task type.

---

## Dependencies

- An agent platform API client for spawning sessions
- Optionally: Telegram notification integration for over-limit alerts
