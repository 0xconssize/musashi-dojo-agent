# Scheduled Task Operator Memory

This file is private local state at `.musashi/task-memory.md`. The operator may
add instructions, preferences, and clarifications that scheduled observation
tasks should consider.

## How to use this memory

- Read this file before every scheduled task run.
- Treat it as operator-provided context, not as authorization.
- It may narrow scope, explain local naming, define what deserves attention, or
  clarify how an observation should be reported.
- It must not weaken `AGENTS.md`, `SECURITY.md`, `HOST_SAFETY.md`, the local SRE
  policy, a task definition, or a skill's stop conditions.
- Do not put credentials, private keys, tokens, or raw logs here.
- If an instruction conflicts with live evidence, current policy, or an
  authoritative source, stop or report the conflict; do not silently guess.

## Global instructions

<!-- Instructions that apply to every scheduled task. -->

-

## Task-specific instructions

<!-- Use one heading whose name exactly matches a task id, for example
     `## node-health`. Keep instructions concise and reviewable. -->

## node-health

-

## host-health

-

## configuration-drift

-

## release-freshness

-

## documentation-freshness

-

## knowledge-freshness

-
