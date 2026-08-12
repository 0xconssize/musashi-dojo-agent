---
name: "deregister-stake-pool"
description: "Retire a Musashi stake pool safely with epoch, funding, signing, confirmation, and verification."
---

# Deregister a stake pool

Schedule retirement of one existing Musashi/Leios stake pool by submitting a
Dijkstra stake-pool deregistration certificate. This is an external on-chain
operation. It does not stop the node, deregister the stake address, withdraw
rewards, delete keys or data, remove services, or reuse funds from another node.

## Preconditions and scope

- Read repository safety instructions, current network declarations, target
  host/node records, execution profile, and this skill.
- Resolve exactly one registered block producer, host, workspace, runtime
  identity, pool ID, cold key, payment key, transaction input, change address,
  socket, and retirement epoch. List every node sharing the host.
- Use `connect-host` before remote inspection and again if connection evidence
  is stale or inconsistent. Never broaden a pool retirement into node or host
  cleanup.
- Use only Musashi testnet magic 164. Query the live tip and require Dijkstra,
  `syncProgress == 100.00`, and a current network declaration. Stop if the
  chain, era, magic, or source freshness conflicts.
- For a Nix node, load
  `diagnose-node/references/nix-cardano-cli-discovery.md` and resolve the exact
  CLI matching the selected runtime. Pass the socket and testnet magic
  explicitly; do not inherit `PATH` or network environment.
- Derive the pool ID from `cold.vkey` and require an exact match with the
  requested on-chain pool. Query `pool-state`; stop if the pool is absent,
  already retired, has an unexpected pending retirement, or the key identity
  differs.
- Confirm the reward-account credential from current pool state and explain
  where the pool deposit will be returned at the retirement boundary. Do not
  imply that stake-address deregistration or reward withdrawal is included.

## Epoch and funding

Query the current epoch and `poolRetireMaxEpoch`. The retirement epoch must be
strictly greater than the current epoch and no later than
`currentEpoch + poolRetireMaxEpoch`. Present the exact epoch and estimated
wall-clock boundary to the operator; never choose a remembered or mainnet
default.

Query every UTxO at the target pool's confirmed payment addresses. Select one
exact input and verify its address is derived from the selected
`payment.vkey`. Never select the first UTxO blindly, use another node's funds,
or assume a previous transaction still has change. Use a target-owned address
as the explicit change address.

## Prepare a reviewable plan

Use non-existing, operation-specific paths under the target workspace. Never
overwrite a certificate, transaction body, or signed transaction. Keep signing
keys in place and never print or copy their contents.

The current Dijkstra certificate form is:

```bash
"$CARDANO_CLI" dijkstra stake-pool deregistration-certificate \
  --cold-verification-key-file "$COLD_VKEY" \
  --epoch "$RETIREMENT_EPOCH" \
  --out-file "$RETIREMENT_CERT"
```

Build a balanced unsigned body with the selected input, target-owned change
address, explicit socket, and explicit testnet magic:

```bash
"$CARDANO_CLI" dijkstra transaction build \
  --testnet-magic 164 --socket-path "$SOCKET_PATH" \
  --tx-in "$TXIN" --change-address "$CHANGE_ADDRESS" \
  --certificate-file "$RETIREMENT_CERT" \
  --out-file "$TX_BODY"
```

Create a schema-valid execution plan under `.musashi/generated/`. Include the
single-node scope, host and access identity, shared-host nodes, exact commands,
paths, CLI/socket, pool ID, current and retirement epochs, input and value,
change address, reward account, expected deposit refund, required signatures,
fee review, disruption, validation, recovery behavior, and a SHA-256 plan
digest. Generated artifacts are private and must not be committed.

Before signing, inspect the certificate and unsigned body with tools exposed by
the verified CLI. Show the operator the pool ID, epoch, input, change, fee,
certificate, deposit destination, exact signing keys by path, affected paths,
and plan digest. Any change to target, epoch, input, fee, command, path, key,
network, privilege, disruption, or scope invalidates confirmation.

## Confirm, sign, and submit

Require explicit digest-bound confirmation before signing. Signing requires only
the target payment key and pool cold key unless the verified era CLI proves
otherwise:

```bash
"$CARDANO_CLI" dijkstra transaction sign \
  --tx-body-file "$TX_BODY" --testnet-magic 164 \
  --signing-key-file "$PAYMENT_SKEY" \
  --signing-key-file "$COLD_SKEY" \
  --out-file "$SIGNED_TX"
```

After signing, calculate and present the transaction ID, re-query tip,
pool-state, and the selected input, and require a second fresh confirmation
immediately before submission. Do not submit if the input was spent, the pool
state or epoch changed incompatibly, the node lost sync, or signed transaction
inspection differs from the approved plan.

Submit once through the explicitly resolved socket:

```bash
"$CARDANO_CLI" dijkstra transaction submit \
  --testnet-magic 164 --socket-path "$SOCKET_PATH" \
  --tx-file "$SIGNED_TX"
```

A submission exit status is not proof of inclusion. Never resubmit blindly.

## Validation and recovery

- Poll boundedly until the selected input is consumed and `pool-state` reports
  the exact pending retirement epoch. Record the transaction ID and sanitized
  evidence.
- Verify the target node and every shared-host node remain running and
  progressing; retirement does not require a restart.
- At the retirement boundary, verify the pool leaves the active set and the
  deposit appears at the configured reward account before claiming completion.
- If preparation or signing fails, stop and preserve artifacts for review.
- If submission status is uncertain, query the input, transaction ID where
  supported, and pool state; do not rebuild or resubmit without a new plan.
- Cancelling or changing a scheduled retirement requires a separately reviewed
  pool re-registration/update workflow and fresh confirmation.
- Stopping the node, deregistering the stake address, withdrawing rewards, or
  deleting the workspace/keys are separate operations with separate authority.

## Sources

- https://leios.cardano-scaling.org/docs/testnet/register-stake-pool/
- https://github.com/IntersectMBO/cardano-cli
- Live `cardano-cli dijkstra stake-pool deregistration-certificate --help`
  from the target runtime
