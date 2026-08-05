# No peer connections

Determine why one relay has no observed peers while protecting shared networking.

## Checks

1. Verify the exact node, host, runtime identity, network magic, configuration hashes, and topology provenance.
2. Confirm the node is running and its declared socket or endpoint belongs to it.
3. Inspect bounded node logs or telemetry for peer-selection and connection evidence.
4. Compare configured bootstrap data with `network/bootstrap-peers.json` and current topology hashes.
5. Observe name resolution, route reachability, listening ownership, and host clock using read-only checks supplied by the runtime.
6. Identify containers, networks, firewalls, proxies, and sibling nodes that share the relevant port or network namespace.

## Decisions

- Reapply configuration only through `join-testnet` when the current files are proven stale or inconsistent.
- Restart only when evidence points to a runtime state issue and the target identity is unambiguous.
- Treat firewall, port exposure, route, shared container network, and system resolver changes as host-level modifications requiring explicit confirmation.
- Do not substitute Cardano mainnet peers, ports, topology, or network values.

## Completion

Success requires observed peer evidence and continuing node progress. A listening port or successful configuration write alone is insufficient.
