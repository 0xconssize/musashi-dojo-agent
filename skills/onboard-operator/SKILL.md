# Skill: Onboard Operator

## Purpose

Create the initial private `.musashi/` workspace, learn the operator's goals and presentation preferences, and establish a safe baseline for future node operations.

## Activation

Use when `.musashi/` does not exist, when the operator explicitly requests onboarding, or when the workspace is present but lacks a completed onboarding state. If the workspace is partially initialized, reconcile it without overwriting existing files.

## Required reading

- `AGENTS.md`
- `AGENT.md`
- `IDENTITY.md`
- `PERSONALITY.md`
- `ONBOARDING.md`
- `SECURITY.md`
- `HOST_SAFETY.md`
- `templates/`
- `schemas/`

## Inputs

- Operator name and preferred language.
- Experience level and goals.
- Existing hosts and nodes, if any.
- Intended node roles and installation methods.
- Execution mode and verified capabilities.
- Confirmation preferences.
- Optional organization or stake-pool branding.
- Optional personality and avatar preferences.

## Procedure

1. Inspect the repository commit and whether `.musashi/` exists.
2. Introduce Niten using the appropriate language from `identity/introduction.md`.
3. Collect the minimum operator, infrastructure, execution, and branding inputs defined in `ONBOARDING.md`.
4. Explain that `.musashi/` is local operational state and is ignored by Git, not encrypted.
5. Create missing workspace directories and initialize missing files from `templates/`.
6. Create or update the operator profile and execution profile without overwriting unrelated local fields.
7. Create an empty inventory when no hosts or nodes are known; otherwise record each host and node separately.
8. Generate `.musashi/identity/IDENTITY.md` from stable Niten identity plus approved operator preferences.
9. Record branding in `.musashi/identity/branding.yaml` and avatar status in `.musashi/identity/avatar.yaml`.
10. Offer avatar generation only when the runtime supports it and the operator approves it. Store generated output outside Git.
11. Record repository commit, execution mode, initialized paths, and completion timestamp in `.musashi/agent-state.yaml`.
12. Recommend the next relevant skill. Do not modify a host during onboarding.

## Safety and confirmation

Onboarding is local state initialization. It must not install packages, connect to remote hosts, change services, inspect private credentials, or alter node state unless a later, separately scoped operation is explicitly requested and confirmed.

Never let branding or personality preferences override security policies, host-safety rules, confirmation requirements, or the obligation to state uncertainty.

## Success criteria

- `.musashi/` exists with the required private directories and files.
- Operator profile and execution mode are recorded.
- Inventory is valid and distinguishes hosts from nodes.
- Customized `.musashi/identity/IDENTITY.md` exists.
- Branding and avatar metadata are recorded without generated images in Git.
- Onboarding completion is recorded with repository commit and timestamp.

## Failure conditions

- Existing local state would be overwritten.
- Required inputs are invented rather than left unknown.
- Runtime capabilities are claimed without verification.
- The requested avatar or branding would imitate protected identity or imply official Cardano affiliation.
- Onboarding would require host modification.

## Outputs

- Initialized or reconciled `.musashi/` workspace.
- Operator profile.
- Execution capability profile.
- Empty or populated inventory.
- Customized local identity document.
- Branding and avatar metadata.
- Onboarding record and recommended next skill.

## Memory updates

Record durable operator preferences and decisions in `.musashi/memory.md`. Keep host-specific and node-specific details in their dedicated memory files. Do not record secrets.
