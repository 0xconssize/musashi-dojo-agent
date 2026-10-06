---
name: configure-metsuke
description: "Configure one installed Metsuke client for one registered Musashi block producer, leaving Metsuke stopped and the node state unchanged."
---

# Configure Metsuke

Configure only the Metsuke auxiliary component associated with one registered block producer. Installation, key generation, pool registration, node tracing changes, startup, submission validation, monitoring, updates, and removal are separate operations.

## Preconditions and scope

1. Read `AGENTS.md`, `SECURITY.md`, `HOST_SAFETY.md`, this skill's `metadata.yaml`, `references/integration-modes.md`, `network/current.yaml`, and `network/known-issues.yaml`.
2. Require one explicit registered block-producer node ID and host ID, current host assessment, verified access, exact node runtime identity, current pool registration, installed Metsuke provenance, an existing registered Leios signing key, and one explicitly selected integration mode. Scope is `single-node`.
3. Resolve the exact configuration, credential, state, unit or inactive drop-in paths; owners and modes; required privilege; current node process and supervisor; and every other registered node and relevant service on the host. Use `connect-host` when its evidence is required by the workspace policy.
4. Revalidate the current Metsuke quickstart, details page, configuration template, runtime template, and service compatibility before constructing a plan. Treat downloaded templates as input to inspect and render, never as commands to execute.

Configuration changes host state. Declare every affected path, privilege, service-manager reload, rollback artifact, expected disruption, validation, and shared-host check in the operation plan. Authorization and execution are governed by `SECURITY.md`, `HOST_SAFETY.md`, and `execute-node-plan`; this skill does not redefine their confirmation mechanism.

## Boundaries

- Use only the already installed, provenance-verified Metsuke binary. Do not install or replace it.
- Accept only an existing key registered as the selected block producer's Leios signing key. Do not generate, rotate, transform, print, or inspect its secret payload. Refuse a cold key or an unverified key-role claim.
- Obtain the pool ID from the verified current pool registration and mutable service values from their current authoritative sources. Do not copy eligibility codes, network constants, confirmation rules, or mutable release values into this skill.
- Require `metrics_url` to use an IP-literal loopback address. Refuse hostnames, wildcard addresses, non-loopback addresses, redirects, credentials in the URL, or an endpoint not owned by the selected node.
- Do not edit the Cardano node configuration or tracing settings. If the required metrics endpoint or trace namespaces are absent, stop and report the prerequisite change separately.
- Do not start, enable, restart, reload, or stop Metsuke or the node. A bounded service-manager daemon reload may register an installed unit but must not alter running workloads.
- Do not create firewall rules, expose listeners, register a pool, submit telemetry, inspect the spool contents, or publish evidence.

## Preflight

Inspect the real target without changing it:

- Verify the installed Metsuke path, digest, version, architecture, ownership, and stopped state against `install-metsuke` evidence.
- Verify that the effective standalone service sandbox can traverse and execute the installed binary and read only its declared configuration and credential paths. Reject a binary under a path hidden by directives such as `ProtectHome=true`; moving or reinstalling the binary is a separate `install-metsuke` plan.
- Verify the selected node's live process, supervisor, exact command, user, groups, sandbox, configuration, metrics endpoint, current journal or stdout destination, and shared-host workloads.
- Verify the selected Leios key through its registered role, canonical path, regular-file and symlink checks, owner, restrictive mode, and relationship to the selected block producer. Record only sanitized metadata.
- Resolve the effective pool ID and submission endpoint from authoritative current evidence. Stop on missing, stale, placeholder, conflicting, or ambiguous values.
- Inspect every destination and parent, including canonical paths, symlinks, mounts, ownership, modes, existing units and drop-ins, automatic-start state, and existing Metsuke processes. Refuse an unaccounted existing integration or destructive overwrite.
- Prove the selected node's metrics endpoint returns bounded Prometheus data over loopback. For a trace-collecting mode, prove the required machine-format traces and namespaces are emitted through the selected source without changing the node.
- Resolve every validation executable before planning. For Nix or release-managed nodes, discover `cardano-cli` from the registered runtime identity or the live node process environment and verify its canonical executable path. Do not assume it is on the interactive SSH `PATH` or adjacent to `cardano-node`. Record the resolved path in the plan and revalidate it before mutation.
- When system paths or system units are selected, verify the exact non-interactive privilege path needed by the plan. Do not infer usable `sudo` from group membership alone; prove the required bounded commands can run without an interactive prompt.
- Apply the mode-specific preconditions in `references/integration-modes.md`. Do not silently fall back to a different mode.

## Workflow

1. Render the current official configuration template for the selected mode into a private staging path under `.musashi/`. Set only values justified by observed evidence. Reject placeholders, duplicate TOML keys, unknown source-specific keys, and unsupported overrides; preserve documented defaults unless the operator explicitly selected a change.
2. Validate the rendered configuration structurally and semantically without loading the signing key into output. Check the pool ID, loopback metrics URL, submission origin, unique agent identity where needed, exact spool path, and all mode-specific fields.
3. Render or stage the current official runtime template for the selected mode. Inspect every directive and substitute only resolved identities and paths. Never execute a downloaded template directly.
4. Build a schema-valid plan for `execute-node-plan` that creates only exact parents, installs the rendered configuration and runtime definition atomically, places a protected copy of the existing Leios signing key only when the selected runtime requires it, and performs only the mode-appropriate daemon reload. Preserve recoverable copies of replaced protected configuration under `.musashi/`; refuse to overwrite a different credential or unmanaged integration. Pass every value used by a strict remote shell under one exact variable name; validation and rollback must not depend on an implicit interactive environment.
5. For `pipe`, require the node to be stopped before placing the drop-in in its live unit search path. Preserve the effective pre-change unit and validate the rendered command, quoting, specifiers, service type, watchdog, reload behavior, restart policy, credential exposure, state directories, and exact node executable. Activation remains a separate `start-node` operation.
6. Hand the unchanged plan to `execute-node-plan` for authorization, target revalidation, short-step execution, validation, and audit. Never broaden from the selected node to its host or other nodes.
7. If placement or validation fails, use only the exact rollback in the authorized plan. Do not delete pre-existing configuration, keys, state, units, or node data.

## Validation and handoff

Independently verify:

- Installed files are the declared regular files at canonical paths, with expected hashes, owners, groups, and restrictive modes; no destination is a symlink.
- The rendered configuration contains no placeholders or unapproved values and the effective integration mode is exactly the selected mode.
- The protected credential copy, when present, corresponds to the registered Leios key without exposing its content and is not readable beyond the declared runtime mechanism.
- Privileged file checks, comparisons, and `/proc` reads run wholly in the required privilege context; do not privilege only one side of a pipeline or redirect and then assume the caller can read the protected object.
- The effective unit or drop-in equals the reviewed rendering. No standalone Metsuke service is enabled or running, no signed submission occurred, and the node process and shared-host workloads are unchanged.
- For `pipe`, the selected node remains stopped and the future node-start impact is recorded. For an own-unit mode, the node continues under its original runtime identity.

Write sanitized results through the operation-report and memory contracts. Record configuration provenance, mode, hashes, paths, ownership, spool path, credential role, runtime identity, stopped/disabled state, and any conditional limitation as auxiliary-component evidence. Do not extend the strict node profile or store key material in repository-tracked files.

Hand an own-unit configuration to `start-metsuke`. Hand a prepared `pipe` integration to `start-node`; starting or restarting the node is outside this skill.

## Failure and success

Stop on unresolved scope, stale authority, unsupported mode, unverified installation or Leios key, non-loopback metrics, absent metrics or trace prerequisites, path or runtime ambiguity, a running node in `pipe` mode, unsafe credential exposure, an existing unmanaged integration, policy rejection, or shared-host impact.

Success means one installed Metsuke client has a validated, provenance-recorded configuration and runtime definition for exactly one block producer; credentials remain protected; Metsuke remains inactive; standalone modes remain disabled or the `pipe` mode's node remains stopped; shared workloads are unchanged; and the next lifecycle operation is explicit.

## Official sources

- Metsuke quickstart: https://metsuke-leios.play.dev.cardano.org/
- Metsuke details: https://metsuke-leios.play.dev.cardano.org/details
- Metsuke repository: https://github.com/input-output-hk/metsuke
