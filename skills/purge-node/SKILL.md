---
name: "purge-node"
description: "Permanently remove one registered Musashi node, its exact workspace, private records, and durable local memory references."
---

# Purge node

Permanently remove one explicitly selected Musashi node. This is destructive and host-affecting. Never infer fleet scope, never erase blockchain history, and never claim indexed conversation transcripts can be removed.

## Inputs

Require:

- Exact node ID and host ID.
- Exact runtime identity, workspace, data, configuration, state, and key paths.
- Exact shared-host nodes and services outside scope.
- Requested local purge scope: inventory, node state, generated artifacts, reports, task runs, and durable memory files.
- Explicitly accepted losses, including unrecoverable keys, funds, deposits, rewards, and rollback.
- Remote-execution capability and current verified connection evidence.
- A schema-valid execution plan with a digest confirmed by the operator.

## Workflow

1. Read `AGENTS.md`, `AGENT.md`, `IDENTITY.md`, `SECURITY.md`, `HOST_SAFETY.md`, execution configuration, inventory, and target/host profiles.
2. Use `connect-host` for remote targets. Match at least two identity signals and stop on any conflict.
3. Resolve exactly one registered node. State its role, access method, runtime identity, exact paths, listening ports, shared-host nodes, expected disruption, privileges, and irreversible losses.
4. Observe the live host:
   - identify the exact target supervisor and child processes by full argv and parent relationship;
   - identify exact listeners owned by the target;
   - find autostart mechanisms referencing the exact runtime identity or workspace;
   - resolve workspace realpath, owner, filesystem, mount boundary, size, symlinks, and hard links;
   - enumerate secret keys and transaction artifacts without reading secret contents;
   - verify every shared-host workload independently.
5. Inspect chain-visible funds, rewards, deposits, and retirement state with the registered network and CLI when available. Do not require recovery if the operator explicitly accepts the named loss, but record that acceptance in the plan.
6. Build an explicit local-reference manifest using exact identifiers: node ID, workspace, runtime identity, pool ID, node-specific transaction IDs, and node-specific addresses. Classify each matching file as:
   - delete whole file because it belongs only to the target;
   - edit surgically because it also contains unrelated host/node data;
   - retain because policy requires a sanitized audit tombstone;
   - immutable/external and therefore not purgeable.
7. Prepare a schema-valid plan for `execute-node-plan`. Include:
   - an exact preflight that repeats identity and path-boundary checks;
   - graceful stop of the exact supervisor/runtime identity;
   - verification that the target process and listeners stopped while siblings remain healthy;
   - permanent deletion of only the validated workspace and exact target-owned autostart entries;
   - exact local manifest actions for node registration, profiles, state, generated artifacts, reports, task runs, and durable `memory/*.md` references;
   - surgical updates to shared inventory/host files;
   - one minimal sanitized tombstone recording that an authorized purge occurred, its scope, accepted losses, result, and timestamp;
   - independent post-delete checks.
8. Compute the digest from the immutable plan. Explain that confirmation authorizes permanent deletion and that no rollback is promised. Do nothing destructive until the operator confirms the exact digest.
9. Immediately before execution, rerun the preflight. Any changed PID ownership, realpath, scope, command, path, privilege, loss, or shared-host state invalidates confirmation.
10. Execute in short stages:
    - stop only the exact target supervisor;
    - validate isolation;
    - remove the exact workspace;
    - update local registration and reference manifest;
    - validate the final state.
11. Stop on any partial failure. Do not broaden deletion, guess a replacement path, or delete a shared file wholesale.
12. Record a sanitized operation result. Never include private key material, raw credentials, private addresses, or unrelated host details.

## Destructive safety

- Reject `/`, `~`, `$HOME`, a workspace root, a host root, an empty value, unresolved variables, globs, command substitutions, relative paths, symlink targets, and mount points as deletion targets.
- Require the workspace realpath to equal the registered absolute path exactly and to be owned by the registered remote user.
- Never reuse common system environment variables to hold targets.
- Do not use broad process matches. Signal only the verified supervisor/runtime identity and validate child termination.
- Do not delete a host profile or connection credential when another registered node shares that host.
- Do not delete generic skills, network declarations, schemas, or unrelated reports.
- Do not remove blockchain history or pretend that external/indexed session transcripts were erased.
- A request to purge memory permits removal of target-specific durable local memory references, not falsification of the minimal audit tombstone.
- A successful command exit is not proof of deletion.

## Success

- The exact target supervisor and child process are absent.
- Its former listeners are closed.
- Its exact workspace and target-owned autostart entries are absent.
- Inventory and host membership no longer register the node.
- Target-only local artifacts and durable memory references are gone, shared files retain unrelated records, and only the disclosed sanitized tombstone remains.
- Every shared-host node is independently healthy with its original runtime identity, path, and listeners.
