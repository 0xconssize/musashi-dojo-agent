# Memory Policy

The repository contains shared, versioned memory policy. Private operational memory belongs under `.musashi/` and must not be committed.

## Memory levels

- `.musashi/memory.md`: operator preferences, objectives, decisions, and fleet-wide context.
- `.musashi/hosts/<host-id>/memory.md`: host constraints, shared services, incidents, and privilege conventions.
- `.musashi/nodes/<node-id>/memory.md`: node role, installation decisions, issues, upgrades, and pending work.

## What to remember

Record durable decisions, constraints, verified observations, unresolved issues, and the context needed to resume work. Avoid storing secrets in conversational summaries or reports.

## Freshness and conflicts

Dynamic network facts must be refreshed from authoritative files under `network/`. Mark observations with timestamps and sources where possible. When memory conflicts with live inspection, prefer live inspection and record the reconciliation.

Repository updates must not overwrite local memory or state. Apply migrations explicitly and record the previous and current repository commits.
