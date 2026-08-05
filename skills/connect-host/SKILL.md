---
name: connect-host
description: "Verify access to a registered local or remote Musashi host before inspection or modification."
---

# Connect host

Establish verified runtime access only. Do not install, start, stop, or modify nodes or hosts.

## Inputs

Require:

- One registered host ID.
- Requested execution mode: `advisory`, `local-execution`, or `remote-execution`.
- Host profile and connection profile.
- Current runtime capabilities and operator authorization.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, `SECURITY.md`, `.musashi/execution.yaml`, inventory, and the selected host files.
2. Resolve exactly one registered host. Active context is a convenience, never authority.
3. Match the mode to observed runtime capabilities:
   - `advisory`: describe checks but do not connect.
   - `local-execution`: verify the runtime is on the registered local host.
   - `remote-execution`: use only an operator-provided runtime connection mechanism.
4. Keep unverified capabilities false or unknown. Never build a custom transport or infer credentials.
5. Perform read-only identity checks before any later modification. For a remote host, compare at least two independent signals where available: inventory endpoint, host-reported hostname, remote user, OS identity, host key or alias, cloud instance ID, expected runtime identity, or expected node path.
6. Stop on missing, duplicate, or conflicting identity. Ask the operator to reconcile inventory; do not silently rewrite it.
7. Record the observed endpoint, user, connection type, identity signals, timestamp, and verification outcome in the host connection profile. Store no secret material.
8. Report available privileges and capabilities without escalating privileges or changing the host.

## Safety

- Registration and successful connection do not authorize modification.
- Do not expose keys, tokens, SSH configuration, sockets, or credentials.
- Treat every host as shared until verified otherwise.
- Never use Cardano mainnet procedures to fill a Musashi gap.

## Success

The target is unambiguous, runtime access is represented accurately, identity verification passes with sufficient evidence, and no host-side change was attempted.
