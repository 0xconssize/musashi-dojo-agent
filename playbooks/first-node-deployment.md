# First relay deployment

Deploy one relay as four independently validated operations. Do not collapse the sequence into one opaque script.

## Preconditions

- Onboarding is complete and the host and relay are registered.
- Scope resolves to one relay and one host.
- `network/current.yaml`, requirements, known issues, release assets, and checksums have been revalidated.
- Execution mode and target identity are verified, or the operator accepts an advisory-only plan.

## Sequence

1. Run `assess-host`. Stop on `unsuitable` or `inconclusive`; resolve every `conditional` finding before modification.
2. Run `install-relay` with one supported method. Leave the relay stopped and validate artifact provenance.
3. Run `join-testnet`. Back up any replaced configuration and validate its network-identity projection, genesis hashes, network identity, and topology.
4. Run `start-node`. Validate the registered runtime identity, stable process state, socket or endpoint ownership, bounded logs, and time-separated tip progress.
5. Record the operation reports, node state, release provenance, configuration provenance, and durable decisions.

## Stop conditions

Stop on source staleness, target drift, unverified download, checksum failure, occupied path or port, missing confirmation, failed validation, or unexpected impact to a shared workload. Diagnose before attempting recovery; never retry a modifying step blindly.

## Completion

Deployment is complete only when all four operation reports succeed. Installation alone, a zero exit status, or one tip observation is not proof that the relay joined and is progressing.
