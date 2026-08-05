---
name: assess-host
description: "Assess whether a registered host can safely support a Musashi relay without modifying the host."
---

# Assess host

Inspect one registered host and produce a host-assessment operation report. Remain advisory when runtime access is unavailable.

## Inputs and scope

Require one host ID, intended installation method, intended node role, and current runtime capabilities. Scope is one host and its registered nodes. Risk is read-only; output is an operation report plus observed host state.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, network requirements and freshness, inventory, and host records.
2. Revalidate official sources before using requirements.
3. Use `connect-host` when execution is available; otherwise identify operator-supplied evidence.
4. Inspect OS and architecture, CPU, memory, free SSD space, clock health, required tools, port conflicts, privileges, and shared workloads.
5. Compare observations with `network/requirements.yaml`. Keep unknowns explicit and do not run stress tests, install packages, or change networking.
6. Record evidence, limits, conflicts, and a `suitable`, `conditional`, `unsuitable`, or `inconclusive` outcome.
7. Update host state only from observations and save a sanitized report under `.musashi/reports/`.

## Failure and success

Stop on ambiguous identity, stale requirements, unsafe inspection, or insufficient evidence. Success means the exact host and shared-host impact are known, every conclusion cites evidence, and no host modification occurred.

## Memory

Record durable host constraints and conflicts in host memory; do not copy transient utilization samples into memory.
