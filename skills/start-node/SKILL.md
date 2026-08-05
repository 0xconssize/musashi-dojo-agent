---
name: start-node
description: "Start one installed Musashi node through its registered runtime identity and validate real node progress."
---

# Start node

Start exactly one installed, configured node.

## Inputs and scope

Require one node ID, verified host access, registered runtime identity, paths, current configuration, and execution capability. Scope is `single-node`. Risk is node-local reversible unless the plan changes host resources. Output is an operation report and node state.

## Workflow

1. Resolve node, host, service or container identity, paths, ports, and shared-host nodes.
2. Inspect current state, configuration freshness, disk headroom, port ownership, and whether the node is already running.
3. Build a schema-valid plan using the registered runtime manager; never invent a service or process identity.
4. Explain expected resource use and disruption. Confirm any host-level change or altered shared resource.
5. Execute with `execute-node-plan`.
6. Validate independently: the process or service remains running, the expected socket or endpoint belongs to the node, logs show no fatal startup error, tip observations progress when applicable, and shared-host workloads remain healthy.
7. Stop and report rather than looping on repeated failures.
8. Save the report and update state only from observations.

## Failure and success

Stop on stale configuration, occupied ports, identity drift, insufficient resources, or failed validation. Success requires evidence that the intended node is running under the registered identity and its independent health checks pass.

## Memory

Record only durable startup constraints or incidents; keep live status in node state.
