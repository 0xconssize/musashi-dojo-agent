---
name: stop-node
description: "Stop one registered Musashi node gracefully and verify that no other host workload was stopped."
---

# Stop node

Stop exactly one node through its registered runtime manager.

## Inputs and scope

Require one node ID, verified host access, runtime identity, shutdown method, and current state. Scope is `single-node`. Risk is node-local reversible with service disruption. Output is an operation report and node state.

## Workflow

1. Resolve the exact node, host, runtime identity, shared processes, volumes, networks, and dependent nodes.
2. Inspect current state and refuse broad selectors, ambiguous process matches, or a shared identity.
3. Build a schema-valid plan for graceful shutdown, bounded waiting, and escalation only as a separately explained step.
4. Explain disruption. Require confirmation if stopping affects other nodes, shared services, or host-level resources.
5. Execute with `execute-node-plan`; do not kill by pattern or remove containers, data, volumes, or services.
6. Validate the registered process or service is stopped, no writer remains on node data, and unrelated workloads remain healthy.
7. Record the report and observed state.

## Failure and success

Stop on ambiguous identity, shared runtime ownership, or unexpected dependents. Success means only the intended node stopped cleanly, its persistent data remains intact, and shared workloads are unaffected.

## Memory

Record abnormal shutdowns and durable dependency findings in node or host memory.
