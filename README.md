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
- Compact skills for registering hosts and nodes without modifying them.
- Planned locations for current network knowledge, operational playbooks, and reports.

The repository contains no executable source code or custom execution engine. The selected agent runtime supplies reasoning, conversation, command execution, remote access, and file operations.

## Local operational state

Private and changing state belongs under `.musashi/`, including inventory, memory, connection metadata, generated commands, reports, and session history. `.gitignore` prevents accidental commits; it is not encryption or filesystem isolation.

## Getting started

1. Read [`AGENTS.md`](AGENTS.md), [`AGENT.md`](AGENT.md), [`SECURITY.md`](SECURITY.md), and [`HOST_SAFETY.md`](HOST_SAFETY.md).
2. Follow [`PLAN.md`](PLAN.md) for the project model and delivery phases.
3. Initialize local state from [`templates/`](templates/) only when needed.
4. Treat `network/` as the source of mutable testnet facts once it is populated and verified.

## Safety principle

> Operate the Dojo. Protect the host.

Observe before modifying, identify the exact target, explain impact, confirm host-level or destructive changes, execute incrementally, and validate the real outcome.
