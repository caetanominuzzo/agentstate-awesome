# Deployment Guardrails

Rules for deploying applications, dashboards, frontends, and any user-facing systems.

---

## Rule: Use Your Organization's Standard Infrastructure

Agent-provided deployment services (e.g., built-in deploy features that create public URLs) must NOT be used to deploy production applications.

**Why**: These services are typically publicly accessible, have no authentication, sit outside your infrastructure, and bypass security, observability, and access control standards.

## What to Do Instead

When a user asks to create or deploy a new application:

1. **Do NOT use the agent's built-in deploy tool** (if it creates public-facing URLs).
2. **Direct the user to your organization's Internal Developer Platform** or standard deployment pipeline.
3. **Help the user prepare the code** (repo setup, Dockerfile, configuration, etc.) so it's ready to deploy through the standard pipeline.

## Acceptable Uses of Agent Resources

- Running local dev servers for testing during development (localhost)
- Running scripts, analysis, data processing on the agent's VM
- Using the agent's browser for manual testing
- Temporary local previews that are NOT shared externally

## Never Acceptable

- Deploying any app to agent-provided public URLs
- Sharing agent-hosted URLs as "the app" or "the dashboard"
- Bypassing your standard deployment provisioning for speed or convenience
