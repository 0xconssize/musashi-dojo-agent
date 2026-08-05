# Recover a failed node

Recover one diagnosed failure without broadening the action.

## Preconditions

- A current diagnostic report identifies the failure or keeps it explicitly unknown.
- The selected recovery comes from applicable official release notes, current Musashi procedures, or a verified local rollback.
- Target identity, paths, data classes, backups, shared-host nodes, and validation criteria are explicit.

## Sequence

1. Preserve bounded pre-recovery evidence and record the current node and host state.
2. Revalidate the recovery authority against the installed and selected releases.
3. Build a schema-valid recovery plan containing the narrowest action, exact paths, privileges, impact, stop conditions, validation, and recovery-of-recovery.
4. Obtain a new confirmation for every host-level or destructive step. Earlier install, update, or diagnostic approval is not reusable.
5. Execute short steps through `execute-node-plan`; stop after any unexpected result.
6. Validate runtime identity, configuration integrity, database accessibility, bounded logs, tip progression, peers, and shared workloads.
7. Record affected data, backups, evidence, and outcome.

## Current narrow exception

For `prototype-2026w31a`, the official release notes permit deleting only volatile chain state when invalid Leios certificate crashes persist after updating. Confirm the exact trigger and path, preserve evidence, and require destructive confirmation. This does not authorize deleting the full database.

## Stop conditions

Stop on unknown cause, non-applicable instructions, missing target identity, unbounded wildcard or recursive deletion, absent required backup, or repeated recovery failure. Prepare an issue report instead of improvising.
