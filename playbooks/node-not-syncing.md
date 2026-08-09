# Node not syncing

Diagnose an apparently stalled relay without treating normal early-testnet pauses as failure.

## Evidence

1. Resolve one node and verify its host and runtime identity.
2. Record at least two time-separated tip, block, slot, or sync-progress observations using the node's supported interface.
3. Record process state, bounded fatal logs, peer evidence, disk headroom, clock health, release provenance, network-identity projection, and topology/genesis hashes.
4. Compare observations with `network/known-issues.yaml`; Musashi sync may be slow and bursty because few relays serve blocks and catch-up is not optimized.

## Classification

- `progressing`: values advance within the evidence window, even in bursts.
- `stalled`: repeated observations do not advance and corroborating evidence identifies a likely constraint.
- `unavailable`: the node interface cannot provide observations.
- `unknown`: evidence is insufficient or contradictory.

## Next action

- For `progressing`, continue observation without modification.
- For an isolated runtime failure, prepare a bounded `restart-node` plan.
- For outdated or conflicting provenance, use `update-node` only after validating the upgrade path.
- For a release-specific failure, use `recover-node` only with the exact documented trigger and separate confirmation.
- When the cause remains unknown, create a sanitized diagnostic report and issue draft rather than deleting state.

Never infer that a stalled display requires a database wipe, configuration replacement, or repeated restart loop.
