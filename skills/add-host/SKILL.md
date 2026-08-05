---
name: add-host
description: "Register or update a local or remote host in the private Musashi inventory without connecting to or modifying the host."
---

# Add host

Register host metadata only. Do not connect to, inspect, install on, or modify the host.

## Inputs

Collect or confirm:

- Unique lowercase host ID using letters, digits, and hyphens.
- Optional display name.
- Type: `local` or `remote`.
- Hostname or address for a remote host.
- Access method and non-secret connection metadata.
- Verified runtime capabilities; unknown capabilities remain false or null.
- Operating system when known.
- Dedicated/shared status, shared services, and constraints.

Never infer credentials, capabilities, system requirements, or mutable testnet values.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, `.musashi/inventory.yaml`, and this skill's `metadata.yaml`.
2. If `.musashi/` is absent, stop and complete onboarding first.
3. Recheck the official source when metadata is stale, obsolete, or its supported release differs from the current source. Registration may continue with operator-supplied facts, but do not present unverified requirements as current.
4. Reject unsafe IDs, duplicate IDs, and paths escaping `.musashi/hosts/<host-id>/`.
5. Show the normalized record and ask the operator to resolve conflicts. Updating an existing host requires explicit confirmation.
6. Create or update, from existing templates:
   - `.musashi/hosts/<host-id>/profile.yaml`
   - `.musashi/hosts/<host-id>/connection.yaml`
   - `.musashi/hosts/<host-id>/state.yaml`
   - `.musashi/hosts/<host-id>/memory.md`
7. Add the host ID once to `.musashi/inventory.yaml`. Preserve every other host and node.
8. Cross-check both directions: every node listed by the host must exist and reference this host; otherwise leave the association unchanged and report the inconsistency.
9. Validate the profile, connection, state, and inventory against their schemas.
10. Report files changed, unknown fields, and whether this host is now the active read-only context.

## Scope and safety

- Output is private local state under `.musashi/`; never commit it.
- Store connection metadata, not passwords, keys, tokens, or secret material.
- Host registration grants no execution authority.
- Do not make a host active silently when another active context exists.
- Any later modifying operation must state the exact host and affected nodes, including nodes sharing the host.

## Success

The host has one valid inventory entry, isolated local files, no unresolved referential conflict, and no host-side change was attempted.
