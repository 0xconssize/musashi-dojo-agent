# Recover a failed node

Recover one diagnosed failure without broadening the action.

## Preconditions

- A current diagnostic report identifies the failure or keeps it explicitly unknown.
- The selected recovery comes from applicable official release notes, current Musashi procedures, or a verified local rollback.
- Target identity, paths, data classes, backups, shared-host nodes, and validation criteria are explicit.

## Sequence

1. Preserve bounded pre-recovery evidence and record the current node and host state.
2. Revalidate the recovery authority against the installed and selected releases.
3. Build a schema-valid recovery plan containing the narrowest action, exact paths, privileges, impact, stop conditions, validation, and recovery-of-recovery. For a diagnosed invalid complete database, record the exact database size and, when it exceeds 200,000,000 bytes, use `bootstrap-node-database` to stage and verify the HTTP(S) snapshot before stopping or removing database state. Never use size alone as a reason to delete data.
4. Before host-level or destructive steps, verify exact targets, protected-state recovery, and shared-host isolation. A complete chain-database replacement must pass the registered database boundary in `execute-node-plan`.
5. Execute short steps through `execute-node-plan`; stop after any unexpected result.
6. Validate runtime identity, configuration integrity, database accessibility, bounded logs, tip progression, peers, and shared workloads.
7. Record affected data, backups, evidence, and outcome.

## Current narrow exception

For `prototype-2026w31a`, the official release notes permit deleting only volatile chain state when invalid Leios certificate crashes persist after updating. Verify the exact trigger and path, preserve evidence, and verify a viable recovery route. This partial-state action is not a complete chain-database reload.

## Stop conditions

Stop on unknown cause, non-applicable instructions, missing target identity, unbounded wildcard or recursive deletion, missing protected-state or rollback backup, or repeated recovery failure. Prepare an issue report instead of improvising.
