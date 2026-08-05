---
name: add-node
description: "Register or update a logical Leios node on an existing host in the private Musashi inventory without installing, starting, or modifying it."
---

# Add node

Register logical node metadata only. Do not install, start, stop, connect to, or modify the node or host.

## Inputs

Collect or confirm:

- Unique lowercase node ID using letters, digits, and hyphens.
- Optional display name.
- Role; use `relay` or `block-producer` only when supplied or verified.
- Environment; do not infer mutable network values.
- Existing host ID.
- Installation method and runtime type when known.
- Service, process, or container identity when known.
- Data, configuration, and workspace paths when known.
- Enabled state.

Unknown values remain null. Never copy defaults from stale documentation or supplementary scripts.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, `.musashi/inventory.yaml`, the referenced host profile, and this skill's `metadata.yaml`.
2. If `.musashi/` is absent, stop and complete onboarding first.
3. Recheck the official source when metadata is stale, obsolete, or its supported release differs from the current source. Registration may continue with operator-supplied facts, but do not present unverified testnet facts as current.
4. Require an existing host ID. Do not create a host implicitly.
5. Reject unsafe IDs, duplicate IDs, and paths escaping `.musashi/nodes/<node-id>/`.
6. Show the normalized record and ask the operator to resolve conflicts. Updating an existing node or moving it between hosts requires explicit confirmation.
7. Create or update, from existing templates:
   - `.musashi/nodes/<node-id>/profile.yaml`
   - `.musashi/nodes/<node-id>/state.yaml`
   - `.musashi/nodes/<node-id>/memory.md`
8. Add the node ID once to `.musashi/inventory.yaml` and to the selected host profile. On an approved host move, remove it from the old host profile. Preserve all unrelated entries.
9. Validate the node profile, state, host profile, and inventory against their schemas.
10. Report files changed, unknown fields, shared-host nodes, and whether this node is now the active read-only context.

## Scope and safety

- Output is private local state under `.musashi/`; never commit it.
- Node registration grants no execution authority.
- Do not generate keys, credentials, configuration, services, containers, or commands.
- Do not make a node active silently when another active context exists.
- Before any later modifying operation, state node ID, host ID, role, access method, runtime identity, relevant paths, other nodes sharing the host, and expected impact.

## Success

The node and host references agree in both directions, all records validate, node memory is isolated, unrelated inventory entries remain unchanged, and no node- or host-side action was attempted.
