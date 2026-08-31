# Host Safety

Niten must treat every target host as shared unless verified otherwise.

## Before modifying

- Resolve the exact host and node scope.
- Identify services, processes, containers, data directories, and configuration directories.
- Check other nodes and shared services on the host.
- Verify host identity using at least two independent signals when possible.
- Inspect current status, versions, disk, memory, ports, permissions, and recent logs.
- State expected disruption, required privileges, affected paths, validation, and recovery.

For remote access, compare the registered endpoint with host-reported identity, remote user, OS, runtime identity, expected node paths, host key or alias, or cloud instance ID. Stop on conflict. Connection success alone is not identity verification or authorization.

## Confirmation required

Require explicit confirmation before installing packages, writing system directories, changing systemd, users, permissions, firewall rules, exposed ports, shared networks, or deleting data. The same applies to actions that may affect multiple nodes or unrelated services.

## Validation

After a change, verify the intended service, version, ports, peers, synchronization, logs, and the continued operation of other nodes sharing the host. A successful exit status is not sufficient.

Confirmation applies only to the exact reviewed plan. If its commands, targets, paths, privileges, disruption, or scope change, obtain confirmation again.

## Forbidden assumptions

Do not assume a host is dedicated, a node is the only node, a path is disposable, a credential is testnet-only, or a remembered network value is current.

Do not select processes, containers, services, paths, or volumes with broad patterns. Stopping a node does not authorize removing it. Updating a node does not authorize deleting state. Recovery must name the exact diagnosed component and data class; a release note that permits removing volatile state never permits deleting the full database.
