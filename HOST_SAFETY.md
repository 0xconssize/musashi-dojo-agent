# Host Safety

Niten must treat every target host as shared unless verified otherwise.

## Before modifying

- Resolve the exact host and node scope.
- Identify services, processes, containers, data directories, and configuration directories.
- Check other nodes and shared services on the host.
- Verify host identity using at least two independent signals when possible.
- Inspect current status, versions, disk, memory, ports, permissions, and recent logs.
- State expected disruption, required privileges, affected paths, validation, and recovery.

## Confirmation required

Require explicit confirmation before installing packages, writing system directories, changing systemd, users, permissions, firewall rules, exposed ports, shared networks, or deleting data. The same applies to actions that may affect multiple nodes or unrelated services.

## Validation

After a change, verify the intended service, version, ports, peers, synchronization, logs, and the continued operation of other nodes sharing the host. A successful exit status is not sufficient.

## Forbidden assumptions

Do not assume a host is dedicated, a node is the only node, a path is disposable, a credential is testnet-only, or a remembered network value is current.
