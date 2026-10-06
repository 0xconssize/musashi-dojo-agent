---
name: recover-node
description: "Recover one failed Musashi node using an evidence-backed, release-specific, scoped operation."
---

# Recover node

Apply one diagnosed recovery action. Recovery is not permission to reset or rebuild broadly.

## Inputs and scope

Require one node ID, diagnostic report, selected failure, authoritative recovery instruction or preserved rollback, verified access, backups when protected state or rollback requires them, and validation criteria. Scope is `single-node`. Risk is variable and may be destructive. Output is an operation report and node state.

## Workflow

1. Revalidate release notes, guide procedures, configuration, and known issues for the observed failure.
2. Resolve the exact node, failed component, paths, data classes, shared-host nodes, and recovery point. If complete chain-database replacement is diagnosed, measure the exact registered database directory in bytes before changes. For more than 200,000,000 bytes, choose `bootstrap-node-database`'s verified HTTP(S) snapshot workflow instead of waiting for a full node replay, subject to source, compatibility, integrity, and space preflight; at or below that size, choose on evidence. Never replace a healthy database solely because it is large.
3. Refuse speculative recovery, unbounded deletion, missing backups where protected state or rollback requires them, or instructions for another release or network.
4. Build a schema-valid plan with pre-recovery evidence, measured database size when applicable, snapshot-versus-replay decision, backups, the narrowest action, exact affected paths, stop conditions, and validation. If the snapshot is unavailable or incompatible, preserve protected state and record the safe alternative rather than deleting first.
5. Verify exact targets, data class, protected-state recovery, and host impact before destructive action. Complete database replacement must pass the registered chain-database boundary in `execute-node-plan`. A diagnosis alone is not evidence that a reset is safe.
6. Execute through `execute-node-plan` in short steps. For current `w31a` certificate crashes, remove only volatile chain state and only after the post-update trigger is observed.
7. Validate process identity, configuration, database accessibility, tip progression, peers, and shared-host workloads. Do not repeat a failed recovery loop.
8. Record the report, evidence, any required backups, recovery decisions, and observed state.

## Failure and success

Stop when diagnosis, target, backup, or recovery boundary is uncertain. Success means the diagnosed fault is resolved with the narrowest safe action and preserved evidence, or execution stops without broadening damage.

## Memory and playbook

Record cause, exact recovery, data affected, backups, and outcome. Follow `playbooks/recover-failed-node.md`.
