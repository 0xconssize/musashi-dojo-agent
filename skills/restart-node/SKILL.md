---
name: restart-node
description: "Restart one registered Musashi node safely and verify recovery, progress, and shared-host isolation."
---

# Restart node

Restart exactly one node as a planned stop/start sequence.

## Inputs and scope

Require one node ID, verified host access, runtime identity, current state, and validation criteria. Scope is `single-node`. Risk is node-local reversible with disruption. Output is an operation report and node state.

## Workflow

1. Resolve the exact node and inspect its current state, dependencies, shared-host nodes, disk, ports, and configuration freshness.
2. Build one schema-valid plan with graceful stop, observed stopped state, start, and bounded validation.
3. Explain downtime and require confirmation when dependencies, shared services, or host-level resources may be affected.
4. Execute through `execute-node-plan`. Never replace restart with destructive recreation or repeated unbounded retries.
5. Validate process identity, socket or endpoint ownership, fatal logs, tip progression when applicable, peer evidence, and unaffected shared workloads.
6. On failure, stop the plan and preserve evidence; invoke `recover-node` only after diagnosis and a new approved plan.
7. Record the report and state.

## Failure and success

Stop on target drift, unsafe dependency impact, or any failed validation. Success means the same registered node returns to a validated running state within the declared window and no other workload changes.

## Memory

Record the reason, unexpected behavior, and durable recovery decision; keep current status in node state.
