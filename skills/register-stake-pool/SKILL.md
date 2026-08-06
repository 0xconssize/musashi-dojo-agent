---
name: register-stake-pool
description: "Register a Cardano stake pool on Musashi testnet with owners, relays, metadata, transaction review, and verification."
---

# Register a stake pool

Register a new pool on the Musashi/Leios testnet. This is an external on-chain
operation: it spends test ada, creates the stake-address and pool deposits, and
submits a transaction. It does not issue an operational certificate, delegate
stake, or start the block producer.

## Safety and prerequisites

- Read the repository safety instructions and get confirmation for the exact
  network, workspace, parameters, owners, relays, metadata, and signing keys.
  Get a second, fresh confirmation immediately before submission.
- Use only Musashi testnet magic 164. Never use `--mainnet` or silently inherit
  another network. Current examples use `cardano-cli dijkstra ...`; re-check
  `query tip` and CLI help if the era or release changes.
- Use a dedicated `$WORKING_DIR/keys`; never overwrite key, address,
  certificate, transaction-body, or signed-transaction files.
- A synced node and socket are required for UTxOs, protocol parameters,
  balancing, and verification. They are not required merely to create keys or
  certificates.
- Confirm `cardano-cli`, `jq`, payment/stake/cold/VRF/BLS files, and the testnet
  provenance of the keys. Keep `cold.skey` offline except for signing.

```bash
export WORKING_DIR=/path/to/musashi-workdir
export CARDANO_NODE_NETWORK_ID=164
export CARDANO_NODE_SOCKET_PATH="$WORKING_DIR/node.socket"
cd "$WORKING_DIR/keys"
command -v cardano-cli jq
test -e "$CARDANO_NODE_SOCKET_PATH"
TIP_JSON=$(cardano-cli query tip)
echo "$TIP_JSON" | jq '{block,epoch,slot,era,syncProgress}'
test "$(echo "$TIP_JSON" | jq -r .syncProgress)" = "100.00"
test "$(echo "$TIP_JSON" | jq -r .era)" = Dijkstra
```

Docker is valid as the CLI runtime. Use the restricted host-user, keys-only
mount pattern from `generate-cardano-keys`; pass the node socket/config
explicitly and do not use `--privileged`, host networking, the Docker socket,
or a broad host mount.

Build a payment-only faucet address without overwriting existing files. Use
this address for the official faucet and as the transaction change address:

```bash
cardano-cli dijkstra address build \
  --payment-verification-key-file payment.vkey \
  --testnet-magic 164 \
  --out-file faucet.addr
```

Fund `faucet.addr` via the official faucet, then inspect all UTxOs and select
an exact input. Never blindly use the first entry when there are multiple
UTxOs. Use `faucet.addr` as `--change-address`.

## Certificate options

The Dijkstra CLI accepts either files or inline keys for pool identity, VRF,
reward account, and owners. The usual file options are:

```text
--cold-verification-key-file cold.vkey
--vrf-verification-key-file vrf.vkey
--pool-reward-account-verification-key-file stake.vkey
--pool-owner-stake-verification-key-file stake.vkey
```

Use `--stake-pool-verification-key`, `--stake-pool-verification-extended-key`,
`--vrf-verification-key`, `--pool-reward-account-verification-key`, or
`--pool-owner-verification-key` for inline bech32/hex keys. Repeat the owner
option for every owner. Always set explicit `--pool-pledge` and `--pool-cost`
in lovelace and `--pool-margin` as a rational such as `0.05`; do not use
examples as defaults.

Relay forms can be combined and repeated:

```text
--pool-relay-ipv4 PUBLIC_IPV4 --pool-relay-port PORT
--pool-relay-ipv6 PUBLIC_IPV6 --pool-relay-port PORT
--single-host-pool-relay relay.example.org --pool-relay-port PORT
--multi-host-pool-relay _cardano._tcp.example.org
```

IPv4/IPv6 relays require a port; single-host DNS has an optional port; the
multi-host DNS SRV form must not have a port. Validate public DNS/reachability
and that the port matches the node and firewall.

## Metadata

Metadata is optional. If used, create and publish the exact JSON document, for
example `{"name":"Pool","description":"...","ticker":"TICK","homepage":"https://example.org"}`.
Respect the target network's schema/ticker policy and the maximum 128-character
metadata URL. Hash locally:

```bash
cardano-cli dijkstra stake-pool metadata-hash \
  --pool-metadata-file stake-pool-metadata.json \
  --out-file stake-pool-metadata.hash
METADATA_HASH=$(tr -d '[:space:]' < stake-pool-metadata.hash)
cardano-cli dijkstra stake-pool metadata-hash \
  --pool-metadata-url "$POOL_METADATA_URL" --expected-hash "$METADATA_HASH"
```

The hash command supports `file`, `http`, `https`, and `ipfs` sources. The
on-chain URL should be publicly retrievable. Include `--metadata-url` and
`--metadata-hash` together, or omit both. Use `--check-metadata-hash` on the
certificate command only when the selected CLI exposes it and fetching the URL
is intentional.

## Certificates and transaction

Read the current stake deposit; never hard-code it:

```bash
STAKE_DEPOSIT=$(cardano-cli dijkstra query gov-state | jq -er .currentPParams.stakeAddressDeposit)
cardano-cli dijkstra stake-address registration-certificate \
  --stake-verification-key-file stake.vkey \
  --key-reg-deposit-amt "$STAKE_DEPOSIT" --out-file stake-reg.cert
```

Create the pool certificate from the confirmed *complete* desired state. The
current Musashi command requires the BLS signing key even if the testnet
release does not yet use BLS for selection:

```bash
cardano-cli dijkstra stake-pool registration-certificate \
  --cold-verification-key-file cold.vkey \
  --vrf-verification-key-file vrf.vkey --bls-signing-key-file bls.skey \
  --pool-pledge "$POOL_PLEDGE_LOVELACE" --pool-cost "$POOL_COST_LOVELACE" \
  --pool-margin "$POOL_MARGIN" \
  --pool-reward-account-verification-key-file stake.vkey \
  --pool-owner-stake-verification-key-file stake.vkey \
  --pool-relay-ipv4 "$POOL_RELAY_IPV4" --pool-relay-port "$POOL_RELAY_PORT" \
  --metadata-url "$POOL_METADATA_URL" --metadata-hash "$METADATA_HASH" \
  --out-file pool-reg.cert
```

Adapt relay/metadata lines and repeat options as required. Build with the
selected exact input and change address so the CLI calculates fee/deposits:

```bash
cardano-cli dijkstra transaction build --tx-in "$TXIN" \
  --change-address "$(cat faucet.addr)" \
  --certificate-file stake-reg.cert --certificate-file pool-reg.cert \
  --out-file pool-reg-tx.raw
```

Before signing, show the operator network, input, change, certificates, fee,
deposits, pledge/cost/margin, every owner/relay, and metadata URL/hash. After
confirmation sign with payment, stake, and cold keys; never print key contents.
Verify the signed plan, obtain fresh submission confirmation, then submit.

```bash
cardano-cli dijkstra transaction sign --tx-body-file pool-reg-tx.raw \
  --signing-key-file payment.skey --signing-key-file stake.skey \
  --signing-key-file cold.skey --out-file pool-reg-tx.signed
cardano-cli dijkstra transaction submit --tx-file pool-reg-tx.signed
POOL_ID=$(cardano-cli dijkstra stake-pool id --output-format hex \
  --cold-verification-key-file cold.vkey)
cardano-cli dijkstra query pool-state --stake-pool-id "$POOL_ID"
```

Verify the stake address separately. Record only sanitized IDs, parameters,
certificate paths, transaction ID, and results; never record signing-key data.

## Sources

- https://leios.cardano-scaling.org/docs/testnet/register-stake-pool/
- https://github.com/0xconssize/leios
- https://github.com/IntersectMBO/cardano-cli
