# Niten First-Run Onboarding

This document defines the runtime-neutral first-run flow. It describes state changes; the selected agent runtime supplies conversation, file operations, and optional execution.

## Before asking questions

Read, in order:

1. `AGENTS.md`
2. `AGENT.md`
3. `IDENTITY.md`
4. `PERSONALITY.md`
5. `SECURITY.md`
6. `HOST_SAFETY.md`
7. `templates/` and the relevant schemas

Check whether `.musashi/` exists. If it exists, inspect its state and do not overwrite it. If it does not exist, explain that Niten will initialize a private local operational workspace.

## Introduction

Present Niten using [`identity/introduction.md`](identity/introduction.md), adapting language and detail to the operator. State clearly that Niten assists the operator and does not replace their authorization or judgment.

## Information to collect

Collect only what is needed for the initial profile. A skipped answer remains `null` or an empty list; do not invent values.

### Operator

- Name and preferred form of address.
- Preferred language.
- Technical experience level.
- Goals in the Musashi Dojo network.
- Confirmation preferences for reversible, host-level, and destructive actions.

### Infrastructure

- Whether the operator already has hosts or nodes.
- Host identifiers and whether each host is local or remote.
- Intended node roles.
- Preferred installation methods.
- Desired execution mode: advisory, local execution, or remote execution.

### Presentation and branding

- Preferred tone, formality, and communication style.
- Whether dojo or ninja references should be prominent, subtle, or omitted.
- Operator or organization name, logo reference, colors, visual style, and public-facing identity when applicable.
- Stake-pool name and public branding, if applicable.
- Avatar preference and whether the runtime supports image generation.

Personality preferences customize presentation only. They never weaken security, confirmation, host-safety, or uncertainty rules.

## Initialization outputs

Create `.musashi/` and initialize from the versioned templates without overwriting existing files:

```text
.musashi/workspace.yaml
.musashi/operator.yaml
.musashi/execution.yaml
.musashi/agent-state.yaml
.musashi/inventory.yaml
.musashi/memory.md
.musashi/identity/IDENTITY.md
.musashi/identity/branding.yaml
.musashi/identity/avatar.yaml
.musashi/hosts/
.musashi/nodes/
.musashi/sessions/
.musashi/reports/
.musashi/generated/commands/
.musashi/generated/scripts/
.musashi/generated/plans/
```

The initial inventory must be valid and empty when no hosts or nodes were supplied. Operator, host, and node records must remain separate.

## Customized identity

Generate `.musashi/identity/IDENTITY.md` by combining:

- Stable facts from root `IDENTITY.md`.
- The operator's language and presentation preferences.
- Organization or stake-pool branding, when provided.
- The selected avatar metadata and pending-generation status.

Do not copy secrets, private keys, connection details, or unnecessary personal data into the identity document.

## Avatar flow

1. Read [`identity/ninja-avatar.md`](identity/ninja-avatar.md).
2. Combine the stable visual direction with the operator's approved branding.
3. If image generation is available and approved, generate the image outside Git at `.musashi/identity/niten-avatar.png` and record metadata in `.musashi/identity/avatar.yaml`.
4. Otherwise, set `generated: false`, record `pending_generation: true`, and preserve the textual specification for later.
5. Never commit the image, mutable identity document, branding metadata, or private operational state.

## Completion

Record onboarding completion in `.musashi/agent-state.yaml` with a timestamp, repository commit, execution mode, and the files initialized. Recommend the next skill based on the declared inventory and goals. Do not begin host modifications as part of onboarding.
