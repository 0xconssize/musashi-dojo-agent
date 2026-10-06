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
2. Inspect current version and provenance, node health, data and configuration paths, free space, shared-host nodes, and rollback feasibility. Treat missing `chain_database_directory` or `protected_static_paths` in the profile as read-only discovery work, not an immediate reason to ask the operator: inspect the verified host's service command, working directory, path types, ownership and static files; reconcile the exact chain database path and disjoint protected paths against the running process. Record only observed absolute paths in the private node profile, then validate it. If these boundaries remain ambiguous after inspection, stop before mutation. If release notes require a complete database rebuild, measure the exact chain database before replacement; above 200,000,000 bytes, prefer the verified HTTP(S) snapshot flow in `bootstrap-node-database` over node replay, after compatibility and checksum preflight. A preferred snapshot is not a mandatory dependency of an update: if unavailable or incompatible, evaluate replay from genesis against measured free disk, network/source availability, expected duration, service impact, and release instructions. Use it only if a safe bounded plan and post-start validation are viable; otherwise report the specific failed checks.
3. Stop if the installed release cannot be identified or if the authoritative upgrade path is incomplete.
4. Build a schema-valid plan to acquire and inspect assets under `.musashi/generated/`, verify checksums, back up configuration and recovery metadata, stop, replace only declared artifacts, start, and validate.
5. Assess host impact, protect static material, and establish recovery before any migration or state deletion. Never infer a database wipe from size or a generic update request; verify the release-specific reset requirement and exact target. Keep the old database untouched while staging a replacement when feasible, and never remove it until source or replay recovery is demonstrably viable.
6. Execute through `execute-node-plan`. Apply release-specific recovery only when its exact trigger is observed and the recovery remains within the requested outcome.
7. Validate artifact provenance, running identity, configuration integrity, fatal logs, tip progression, peers, and shared-host workloads.
8. Record the report, upgrade history, and observed state.

## Failure and success

Stop on unverified assets, missing release notes, failed backup, incompatible method, or validation failure. Success means the single node runs the selected release with verified provenance and health evidence, or stops safely with preserved recovery material.

## Memory and playbook

Record release transition, provenance, compatibility decisions, and outcome in node memory. Use `playbooks/configuration-changed.md` when configuration also changed.
