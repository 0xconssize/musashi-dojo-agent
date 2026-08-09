---
name: join-testnet
description: "Configure one installed relay to join the current Musashi testnet using verified network declarations."
---

# Join testnet

Prepare and, when authorized, apply Musashi configuration to one installed stopped relay. Starting the node belongs to `start-node`.

## Inputs and scope

Require one relay node ID, installed release provenance, installation method, verified host access, configuration destination, and current network declarations. Scope is `single-node`. Risk is node-local reversible unless paths or networking make it host-level. Output is an operation report.

## Workflow

1. Revalidate `network/current.yaml`, known issues, topology/genesis hashes, the network-identity projection, and official operational sources.
2. Resolve the node, host, runtime identity, paths, and shared-host nodes; refuse non-relay roles in this phase.
3. Inspect existing configuration and node state. Back up replaced configuration under `.musashi/` before modification.
4. Build a schema-valid plan that retrieves configuration without immediate execution, verifies content hashes, stages files, checks paths and ownership, and atomically places validated configuration.
5. Require confirmation for host-level paths, permissions, firewall, or shared-network changes.
6. Execute with `execute-node-plan` only through runtime tools.
7. Validate network magic, era, topology and bootstrap data, file integrity, and unaffected shared workloads. Do not claim network membership until `start-node` observes the running node.
8. Record the report and observed state.

## Failure and success

Stop on stale or mismatched configuration, unverified downloads, ambiguous paths, or a running writer. Success means the stopped relay has verified current Musashi configuration, preserved recovery material, and no unapproved host-level change.

## Memory and playbook

Record configuration provenance and durable path decisions in node memory. Follow `playbooks/first-node-deployment.md` for the complete relay sequence.
