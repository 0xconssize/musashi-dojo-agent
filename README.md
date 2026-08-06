# Musashi Dojo Agent

**Niten — the Musashi Dojo Ninja Agent**

> Two paths. One operator.

Musashi Dojo Agent is a portable, declarative repository that gives AI agents the identity, knowledge, procedures, safety rules, configuration conventions, and data contracts needed to help operators deploy and operate Cardano Leios Musashi Dojo testnet nodes.

Niten is the **Dojo Node Operator**: an assistant for human judgment, not a replacement for it.

## What this repository contains

- Runtime-neutral instructions and personality guidance.
- Host-focused safety and confirmation policies.
- Templates for operator, host, node, execution, and operational state.
- JSON Schema contracts for portable structured data.
- Compact skills for inventory, host assessment and access, relay installation and configuration, node lifecycle, diagnosis, update, recovery, reporting, and safe plan execution through runtime-provided tools.
- Read-only SRE task definitions for node and host health, configuration drift, release freshness, documentation freshness, and knowledge freshness.
- Versioned current Musashi network declarations with source and freshness records.
- Initial relay deployment, diagnostic, configuration-change, recovery, and evidence-collection playbooks.

The repository contains no executable source code or custom execution engine. The selected agent runtime supplies reasoning, conversation, command execution, remote access, and file operations.

## Local operational state

Private and changing state belongs under `.musashi/`, including inventory, memory, connection metadata, generated commands, reports, and session history. `.gitignore` prevents accidental commits; it is not encryption or filesystem isolation.

## Proposing improvements

If you find incorrect knowledge, an unclear skill, a misleading instruction, or a useful improvement, open a **Knowledge or skill feedback** issue. Include the affected repository path, current and expected behavior, a sanitized example, and the source or evidence when available.

For a reproducible host or node incident, use the local `report-issue` skill first. It creates a sanitized draft under `.musashi/`; publication and evidence uploads always require a separate explicit operator decision.

Accepted issues are resolved through a reviewed pull request. Shared knowledge changes are not made directly from an issue or from private operational state.

## Scheduled SRE checks

The declarative tasks under [`tasks/`](tasks/) run in observation mode only. An external scheduler supplied by the selected runtime may invoke [`sre-observe`](skills/sre-observe/SKILL.md) for an explicitly configured host, node, or source set. Results belong under `.musashi/task-runs/` and are local operational state.

The release and documentation checks compare installed versions, official release metadata, source retrieval dates, content hashes, relevant sections, and repository declarations. A detected change or stale source creates a local review signal; it does not update a node, accept a source as authoritative, or publish an issue automatically. Use [`templates/sre-policy.yaml`](templates/sre-policy.yaml) and [`templates/schedules.yaml`](templates/schedules.yaml) as starting points for local runtime configuration.

## Getting started

1. Read [`AGENTS.md`](AGENTS.md), [`AGENT.md`](AGENT.md), [`SECURITY.md`](SECURITY.md), and [`HOST_SAFETY.md`](HOST_SAFETY.md).
2. Follow [`PLAN.md`](PLAN.md) for the project model and delivery phases.
3. Initialize local state from [`templates/`](templates/) only when needed.
4. Treat [`network/current.yaml`](network/current.yaml) as the source of mutable Musashi facts only while its freshness record is current, and read [`network/known-issues.yaml`](network/known-issues.yaml) before operational use.

Musashi's official getting-started guide and its linked official resources are the only authority. The official releases repository determines the latest version; getting-started determines configuration and operational procedures. Cardano mainnet documentation must not supply defaults or fill gaps.

## Safety principle

> Operate the Dojo. Protect the host.

Observe before modifying, identify the exact target, explain impact, confirm host-level or destructive changes, execute incrementally, and validate the real outcome.
