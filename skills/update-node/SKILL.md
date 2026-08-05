---
name: update-node
description: "Update one registered Musashi node to the selected official release with verified assets and bounded recovery."
---

# Update node

Update one node. Fleet rollouts belong to Phase 7.

## Inputs and scope

Require one node ID, installed release provenance, target release, installation method, verified access, backups, and validation criteria. Scope is `single-node`. Risk is variable and disruptive. Output is an operation report and node state.

## Workflow

1. Revalidate the latest release, assets, checksums, compatibility, intermediate release notes, guide procedures, configuration, and known issues.
2. Inspect current version and provenance, node health, data and configuration paths, free space, shared-host nodes, and rollback feasibility.
3. Stop if the installed release cannot be identified or if the authoritative upgrade path is incomplete.
4. Build a schema-valid plan to acquire and inspect assets under `.musashi/generated/`, verify checksums, back up configuration and recovery metadata, stop, replace only declared artifacts, start, and validate.
5. Require confirmation for host-level changes and any state deletion or irreversible migration. Never infer a database wipe.
6. Execute through `execute-node-plan`. Apply release-specific recovery only when its exact trigger is observed and separately authorized.
7. Validate artifact provenance, running identity, configuration integrity, fatal logs, tip progression, peers, and shared-host workloads.
8. Record the report, upgrade history, and observed state.

## Failure and success

Stop on unverified assets, missing release notes, failed backup, incompatible method, or validation failure. Success means the single node runs the selected release with verified provenance and health evidence, or stops safely with preserved recovery material.

## Memory and playbook

Record release transition, provenance, compatibility decisions, and outcome in node memory. Use `playbooks/configuration-changed.md` when configuration also changed.
