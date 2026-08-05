---
name: diagnose-node
description: "Diagnose one registered Musashi node with read-only checks, sanitized evidence, and current known-issue rules."
---

# Diagnose node

Collect evidence and identify likely problems without applying recovery.

## Inputs and scope

Require one node ID, current inventory and state, runtime capabilities, symptom or reason, and evidence window. Scope is `single-node`; selected nodes require separate independent reports. Risk is read-only. Output is a diagnostic report.

## Workflow

1. Read current network declarations, known issues, `diagnostic-rules.yaml`, and target records; revalidate sources when a rule depends on mutable facts.
2. Use `connect-host` when execution is available. Identify operator-supplied evidence in advisory mode.
3. Inspect host capacity and clock, runtime identity, process state, release provenance, configuration hashes, socket or endpoint, bounded logs, tip trend, peer evidence, and shared-host impact.
4. Use multiple time-separated observations before declaring sync stalled. Distinguish slow or bursty sync from a proven stall.
5. Sanitize logs and command output. Do not collect credentials, keys, full configuration secrets, or unrelated host data.
6. Rank findings by evidence and severity. Keep unresolved causes explicit; do not modify, restart, update, or delete state.
7. Save a schema-valid diagnostic report and update state only from observations.

## Failure and success

Stop any check that would modify the node or expose unrelated private data. Success means the report is reproducible, sanitized, evidence-based, and separates observations, likely causes, unknowns, and recommended next actions.

## Playbooks

Use `playbooks/node-not-syncing.md`, `playbooks/no-peer-connections.md`, `playbooks/configuration-changed.md`, and `playbooks/collect-diagnostics.md` as symptom-specific guides.
