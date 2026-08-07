---
name: update-stake-pool
description: "Update an existing Cardano stake pool registration on Musashi testnet, including parameters, owners, relays, metadata, and cold-key signing."
---

# Update a stake pool

Publish a replacement `stake-pool registration-certificate` for an existing
Musashi/Leios pool. It can change pledge, cost, margin, reward account, owners,
relays, and metadata. It does not register the stake address again, rotate the
cold key, issue an operational certificate, delegate stake, or start the node.

## Preconditions and safety

- Read repository safety instructions and obtain confirmation for the exact pool,
  full before/after state, network, input, and keys. Obtain a second fresh
  confirmation immediately before submission; any change invalidates it.
- Use Musashi magic 164 and the selected era (`dijkstra` in the current guide).
  Use a synced node for pool state, UTxOs, balancing, and verification. A node
  is not needed merely to create the replacement certificate.
- Require the *same* pool cold key and `cold.skey`; never generate a new cold
  key for an update. Keep the signing key offline otherwise.
- Re-query UTxOs after preceding transactions and select an exact input. Do not
  blindly use the first UTxO.
- Do not include `stake-address registration-certificate`; the stake address is
  already registered.

When operating against a running Nix node, load
`diagnose-node/references/nix-cardano-cli-discovery.md` and complete its exact
CLI and socket discovery. Set `CARDANO_CLI` to the verified path and pass the
resolved socket only to each query invocation. Do not change `PATH` or use the
SSH session's `command -v cardano-cli`. Non-Nix runtimes use their separately
verified CLI path.

```bash
export WORKING_DIR=/path/to/musashi-workdir
export CARDANO_NODE_NETWORK_ID=164
SOCKET_PATH=/path/to/resolved/node.socket
export CARDANO_CLI=/path/to/verified/cardano-cli
cd "$WORKING_DIR/keys"
POOL_ID=$("$CARDANO_CLI" dijkstra stake-pool id --output-format hex \
  --cold-verification-key-file cold.vkey)
CARDANO_NODE_SOCKET_PATH="$SOCKET_PATH" "$CARDANO_CLI" dijkstra query pool-state --stake-pool-id "$POOL_ID"
CARDANO_NODE_SOCKET_PATH="$SOCKET_PATH" "$CARDANO_CLI" dijkstra query utxo --address "$(cat payment.addr)"
```

Prepare a diff of the current and complete desired state. Omitted owners and
relays are not assumed to be preserved: the replacement certificate describes
the full new state. Treat missing metadata as removal only with explicit
confirmation. Validate new public relay DNS/reachability and firewall ports.

## Metadata and replacement certificate

Hash the exact local or hosted JSON and verify it before use:

```bash
"$CARDANO_CLI" dijkstra stake-pool metadata-hash \
  --pool-metadata-file "$POOL_METADATA_FILE" --out-file metadata.hash
METADATA_HASH=$(tr -d '[:space:]' < metadata.hash)
"$CARDANO_CLI" dijkstra stake-pool metadata-hash \
  --pool-metadata-url "$POOL_METADATA_URL" --expected-hash "$METADATA_HASH"
```

The on-chain metadata pair is all-or-nothing: include both `--metadata-url`
and `--metadata-hash`, or omit both to remove the anchor. Respect the 128
character URL limit. Use `--check-metadata-hash` only when supported by the
selected CLI and an intentional network fetch is allowed.

Create a new certificate with the same cold identity and the complete desired
state. Repeat owner and relay options as needed. Address relays require a port;
single-host DNS has an optional port; multi-host DNS SRV has no port:

```bash
"$CARDANO_CLI" dijkstra stake-pool registration-certificate \
  --cold-verification-key-file cold.vkey \
  --vrf-verification-key-file vrf.vkey --bls-signing-key-file bls.skey \
  --pool-pledge "$NEW_PLEDGE_LOVELACE" --pool-cost "$NEW_COST_LOVELACE" \
  --pool-margin "$NEW_MARGIN" \
  --pool-reward-account-verification-key-file stake.vkey \
  --pool-owner-stake-verification-key-file stake.vkey \
  --pool-relay-ipv4 "$NEW_RELAY_IPV4" --pool-relay-port "$NEW_RELAY_PORT" \
  --out-file pool-reg-update.cert
```

The current Musashi Dijkstra command requires BLS even when the selected
testnet release does not yet use it for selection. Revalidate CLI help before
execution. Do not reuse an old metadata hash for a changed document.

## Build, review, sign, submit, verify

Use `transaction build` so the selected release calculates fees and replacement
registration deposit/refund rules:

```bash
"$CARDANO_CLI" dijkstra transaction build --tx-in "$TXIN" \
  --change-address "$(cat payment.addr)" \
  --certificate-file pool-reg-update.cert --out-file pool-reg-update-tx.raw
```

Before signing show the before/after diff, unchanged pool ID, exact input,
change address, certificate, fee, and net deposit/refund. Confirm that no stake
registration certificate is present. After confirmation sign with payment and
cold keys (add stake signing key if required by the selected era), never print
keys, verify the signed plan, get fresh submission confirmation, and submit:

```bash
"$CARDANO_CLI" dijkstra transaction sign --tx-body-file pool-reg-update-tx.raw \
  --signing-key-file payment.skey --signing-key-file stake.skey \
  --signing-key-file cold.skey --out-file pool-reg-update-tx.signed
"$CARDANO_CLI" dijkstra transaction submit --tx-file pool-reg-update-tx.signed
```

After inclusion, verify the same pool ID and every intended parameter: pledge,
cost, margin, reward account, owners, relays, metadata URL/hash, and active
epoch. Do not resubmit blindly if activation is delayed. Report only sanitized
IDs, transaction ID, and before/after results.

## Sources

- https://github.com/0xconssize/leios
- https://leios.cardano-scaling.org/docs/testnet/register-stake-pool/
- https://github.com/IntersectMBO/cardano-cli
