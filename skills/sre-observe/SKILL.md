---
name: sre-observe
description: "Run scheduled, read-only SRE checks for registered Musashi hosts, nodes, releases, and knowledge sources."
---

# SRE observe

Run a declarative SRE task in observation mode. This skill produces a validated local task run and sanitized evidence; it does not restart, update, recover, reconfigure, publish, or delete anything.

## Inputs and scope

Require a schema-valid task definition, an explicit single-node or single-host target, the runtime capabilities actually available, the repository commit, and any source-freshness policy. A task may inspect one registered target at a time. Do not infer fleet scope from a selector or from a scheduler invocation.

## Workflow

1. Read `AGENTS.md`, `SECURITY.md`, `HOST_SAFETY.md`, the task definition, the local SRE policy, and the relevant target records.
2. Resolve the exact host or node and stop on missing, duplicate, stale, or conflicting identity data.
3. For node checks, use the read-only checks and evidence rules from `diagnose-node`. For host checks, use `assess-host` without applying its plan.
4. For release checks, inspect the official non-draft release source, assets, checksums, compatibility, and release notes. Never treat an unverified asset or draft as an update recommendation.
5. For documentation checks, fetch only declared sources through runtime-provided capabilities, record retrieval time and content hash, and compare relevant sections with repository declarations and skill metadata.
6. Classify each check as `healthy`, `degraded`, `failed`, `unknown`, `current`, `update-available`, `stale`, or `source-unreachable` as applicable.
7. Write a schema-valid task run and sanitized evidence under `.musashi/task-runs/`. Do not write external source content or private logs into the Git repository.
8. Apply the task's alert and deduplication policy locally. A knowledge issue may be prepared as a draft, but publication is never part of this skill.

## Stop conditions

Stop on target drift, stale authority, unavailable capability, unknown release provenance, failed sanitization, source contradiction, or an action outside observation mode. Escalate with evidence rather than improvising a repair.

## Success

Success means the declared checks ran against the exact target or source set, every result has evidence or an explicit unknown, a schema-valid local task run exists, and no external or host state was modified.
