---
name: recover-node
description: "Recover one failed Musashi node using an evidence-backed, release-specific, explicitly approved plan."
---

# Recover node

Apply one diagnosed recovery action. Recovery is not permission to reset or rebuild broadly.

## Inputs and scope

Require one node ID, diagnostic report, selected failure, authoritative recovery instruction or preserved rollback, verified access, backups, and validation criteria. Scope is `single-node`. Risk is variable and may be destructive. Output is an operation report and node state.

## Workflow

1. Revalidate release notes, guide procedures, configuration, and known issues for the observed failure.
2. Resolve the exact node, failed component, paths, data classes, shared-host nodes, and recovery point.
3. Refuse speculative recovery, unbounded deletion, missing backups where rollback is required, or instructions for another release or network.
4. Build a schema-valid plan with pre-recovery evidence, backups, the narrowest action, explicit affected paths, stop conditions, and validation.
5. Require confirmation for host-level actions and every destructive step. A prior diagnostic or update confirmation does not authorize recovery.
6. Execute through `execute-node-plan` in short steps. For current `w31a` certificate crashes, remove only volatile chain state and only after the post-update trigger is observed.
7. Validate process identity, configuration, database accessibility, tip progression, peers, and shared-host workloads. Do not repeat a failed recovery loop.
8. Record the report, evidence, backups, and observed state.

## Failure and success

Stop when diagnosis, authority, target, backup, or recovery boundary is uncertain. Success means the diagnosed fault is resolved with the narrowest authorized action and preserved evidence, or execution stops without broadening damage.

## Memory and playbook

Record cause, exact recovery, data affected, backups, and outcome. Follow `playbooks/recover-failed-node.md`.
