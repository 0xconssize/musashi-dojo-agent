# Musashi configuration changed

Reconcile one node after authoritative configuration or topology content changes.

## Preconditions

- Revalidate the live configuration source and update `network/current.yaml` through a reviewed repository change before operations rely on new hashes.
- Identify the exact node, installed release, configuration source, affected files, runtime identity, and shared-host nodes.
- Determine whether the release and configuration are compatible; stop when either authority is incomplete or conflicting.

## Sequence

1. Diagnose the current node and capture configuration hashes, running state, tip, peers, and bounded logs.
2. Save the existing configuration and provenance under `.musashi/backups/` or the node backup area.
3. Prepare a `join-testnet` plan that retrieves, inspects, verifies, stages, and atomically applies only the changed files.
4. Explain disruption and obtain confirmation for host-level paths, ownership, firewall, or shared-network changes.
5. Apply the plan while the node is stopped when the changed files are not safe for live replacement.
6. Start or restart the node only through its lifecycle skill.
7. Validate configuration hashes, network identity, runtime identity, bounded logs, tip progression, peers, and shared workloads.

## Recovery

If validation fails, stop and preserve evidence. Restore the prior configuration only when the prior release/network pairing remains authoritative and the rollback is an approved plan. Never merge genesis, topology, or protocol parameters from different network incarnations.
