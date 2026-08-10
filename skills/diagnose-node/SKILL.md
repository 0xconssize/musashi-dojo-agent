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
3. Inspect host capacity and clock, runtime identity, process state, release provenance, network-identity projection, topology/genesis hashes, socket or endpoint, bounded logs, tip trend, peer evidence, and shared-host impact. When `installation_method` is `nix`, load `references/nix-cardano-cli-discovery.md` and complete its runtime-tool and socket discovery before any CLI query. Invoke only the verified `CARDANO_CLI` path with the resolved socket passed to that invocation.
4. For `tip-progress`, make the first check at two minutes. If that first check is useful and conclusive in a positive way, finish the check without a second observation or an alert. If the first check is unusable or inconclusive, make a second check when five minutes have elapsed. Alert only if the second check fails; do not alert on the first check. Distinguish slow or bursty sync from a proven stall. If the CLI cannot be resolved or the socket is unknown, record `tip-progress: unknown` because the tool is unavailable; do not classify the node as `stalled`, `failed`, or down. Keep this result separate from process state, peer connectivity, and release provenance.
5. Sanitize logs and command output. Do not collect credentials, keys, full configuration secrets, or unrelated host data.
6. Rank findings by evidence and severity. Keep unresolved causes explicit; do not modify, restart, update, or delete state.
7. Save a schema-valid diagnostic report and update state only from observations.

## Failure and success

Stop any check that would modify the node or expose unrelated private data. Success means the report is reproducible, sanitized, evidence-based, and separates observations, likely causes, unknowns, and recommended next actions.

## Playbooks

Use `playbooks/node-not-syncing.md`, `playbooks/no-peer-connections.md`, `playbooks/configuration-changed.md`, and `playbooks/collect-diagnostics.md` as symptom-specific guides.
