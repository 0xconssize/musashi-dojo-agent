# Host Safety

Niten must treat every target host as shared unless verified otherwise.

## Before modifying

- Resolve the exact host and node scope.
- Identify services, processes, containers, data directories, and configuration directories.
- Check other nodes and shared services on the host.
- Verify host identity using at least two independent signals when possible.
- Inspect current status, versions, disk, memory, ports, permissions, and recent logs.
- Determine expected disruption, required privileges, affected paths, validation, and recovery; report material impact concisely.

For remote access, compare the registered endpoint with host-reported identity, remote user, OS, runtime identity, expected node paths, host key or alias, or cloud instance ID. Stop on conflict. Connection success alone is not identity verification or authorization.

## Modification boundary

Apply only changes necessary for the requested outcome on verified targets. Prefer reversible, node-scoped actions; preserve recoverable copies of protected configuration before overwriting. If a destructive step lacks a proven exact target and viable recovery, stop and escalate. Never change unrelated services or expand to other nodes implicitly.

## Validation

After a change, verify the intended service, version, ports, peers, synchronization, logs, and the continued operation of other nodes sharing the host. A successful exit status is not sufficient.

If commands, targets, paths, privileges, or scope change, recheck identity, impact, and recovery before continuing.

## Forbidden assumptions

Do not assume a host is dedicated, a node is the only node, a path is disposable, a credential is testnet-only, or a remembered network value is current.

Do not select processes, containers, services, paths, or volumes with broad patterns. Stopping a node does not authorize removing it. Updating a node does not authorize deleting state merely because an update is requested; a verified release-required full reset may be included only after the exact registered chain-database replacement boundary and viable recovery route are established. Recovery must name the exact diagnosed component and data class. A release note permitting partial volatile-state removal does not justify deleting the full database; use only the validated registered chain-database reload workflow for that.
