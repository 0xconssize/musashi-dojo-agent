---
name: register-stake-pool
description: "Register a Cardano stake pool on the Musashi Dojo Leios testnet using payment, stake, cold, VRF, and BLS keys, with explicit confirmation before signing and submitting the on-chain transaction."
---

# Register a stake pool

Register one stake pool on the Musashi Dojo Leios testnet. This is an on-chain operation: it consumes test ada, creates a stake-address deposit and pool deposit, and submits a transaction. It does not delegate external stake, issue an operational certificate, or restart a block producer.

## Preconditions and scope

1. Read `AGENTS.md`, `SECURITY.md`, and `HOST_SAFETY.md`.
2. Obtain explicit operator confirmation for this exact scope: pool registration on Musashi testnet, the selected workspace, pool parameters, relay endpoint, and the use of the named signing keys.
3. Confirm that the target is Musashi testnet (`network magic 164`), never mainnet or another network.
4. Confirm the selected release and current era from the repository's `network/current.yaml` and the official sources. The guide currently uses `cardano-cli dijkstra ...`; revalidate before execution if the network advances.
5. Confirm `cardano-cli` and `jq` are available. Docker may be used as the CLI runtime; follow the restricted mount pattern from `generate-cardano-keys` and provide the node socket and required working files explicitly.
6. Confirm a synced node socket and a dedicated `$WORKING_DIR`. Registration queries the node for UTxOs, protocol parameters, and the chain tip.
7. Confirm the following files exist under `$WORKING_DIR/keys/`, were generated for this testnet, and are not mainnet material:
   - `payment.vkey`, `payment.skey`
   - `stake.vkey`, `stake.skey`
   - `cold.vkey`, `cold.skey`
   - `vrf.vkey`, `bls.skey`
8. Require the operator to supply or verify the public relay IPv4 address and port. Never infer a public endpoint from a local interface.

Registration requires two separate confirmations:

- before signing the prepared transaction with `payment.skey`, `stake.skey`, and `cold.skey`;
- immediately before submitting the signed transaction to the network.

Any change to target, keys, input UTxO, certificates, parameters, fee, command, or scope invalidates the prior confirmation.

## Environment and node checks

Set the network and socket explicitly. Do not use `--mainnet` or silently fall back to another network:

```bash
export WORKING_DIR=/path/to/musashi-workdir
export CARDANO_NODE_NETWORK_ID=164
export CARDANO_NODE_SOCKET_PATH="$WORKING_DIR/node.socket"
cd "$WORKING_DIR/keys"

command -v cardano-cli
command -v jq
cardano-cli --version
test -S "$CARDANO_NODE_SOCKET_PATH" || test -e "$CARDANO_NODE_SOCKET_PATH"
TIP_JSON=$(cardano-cli query tip)
echo "$TIP_JSON" | jq '{block, epoch, era, syncProgress}'
test "$(echo "$TIP_JSON" | jq -r '.syncProgress')" = "100.00"
test "$(echo "$TIP_JSON" | jq -r '.era')" = "Dijkstra"
```

If the node is not fully synced or the era is not Dijkstra, stop and revalidate the official procedure. Do not register against a stale or ambiguous chain.

## Build and fund the payment address

If `payment.addr` does not exist, build it without overwriting any existing address:

```bash
test ! -e payment.addr || {
  echo "payment.addr already exists; verify it instead of overwriting it" >&2
  exit 1
}

cardano-cli dijkstra address build \
  --payment-verification-key-file payment.vkey \
  --stake-verification-key-file stake.vkey \
  --out-file payment.addr
cat payment.addr
```

The operator must fund this address through the official Musashi faucet before continuing. Do not request faucet funds or contact the faucet without separate explicit instruction. Verify the balance:

```bash
PAYMENT_ADDR=$(cat payment.addr)
cardano-cli dijkstra query utxo --address "$PAYMENT_ADDR"
```

The guide's example assumes one faucet UTxO. If more than one UTxO is returned, stop and require the operator to select an exact input; never choose arbitrarily.

## Build registration certificates

Require explicit values for the pool parameters and relay endpoint. The guide's examples are 1,000,000,000 lovelace pledge, 170,000,000 lovelace cost, 0.05 margin, and port 3010; these are examples, not silent defaults:

```bash
: "${POOL_PLEDGE_LOVELACE:?set the confirmed pool pledge in lovelace}"
: "${POOL_COST_LOVELACE:?set the confirmed pool cost in lovelace}"
: "${POOL_MARGIN:?set the confirmed pool margin}"
: "${POOL_RELAY_IPV4:?set the confirmed public relay IPv4 address}"
: "${POOL_RELAY_PORT:?set the confirmed public relay port}"

STAKE_DEPOSIT=$(cardano-cli dijkstra query gov-state \
  | jq -r '.currentPParams.stakeAddressDeposit')
test "$STAKE_DEPOSIT" != "null" && test -n "$STAKE_DEPOSIT"

cardano-cli dijkstra stake-address registration-certificate \
  --stake-verification-key-file stake.vkey \
  --key-reg-deposit-amt "$STAKE_DEPOSIT" \
  --out-file stake-reg.cert

cardano-cli dijkstra stake-pool registration-certificate \
  --cold-verification-key-file cold.vkey \
  --vrf-verification-key-file vrf.vkey \
  --bls-signing-key-file bls.skey \
  --pool-pledge "$POOL_PLEDGE_LOVELACE" \
  --pool-cost "$POOL_COST_LOVELACE" \
  --pool-margin "$POOL_MARGIN" \
  --pool-reward-account-verification-key-file stake.vkey \
  --pool-owner-stake-verification-key-file stake.vkey \
  --pool-relay-ipv4 "$POOL_RELAY_IPV4" \
  --pool-relay-port "$POOL_RELAY_PORT" \
  --out-file pool-reg.cert
```

The BLS key is required by the current registration command. The official guide notes that BLS is accepted but was not yet active in the testnet at that revision; revalidate this against the selected release.

## Build and inspect the transaction

Select an exact funded input. The following is safe only when the query returns exactly one UTxO:

```bash
UTXO_JSON=$(cardano-cli dijkstra query utxo --address "$PAYMENT_ADDR")
test "$(echo "$UTXO_JSON" | jq 'length')" -eq 1 || {
  echo "Multiple or missing UTxOs; select an exact input before continuing" >&2
  exit 1
}
TXIN=$(echo "$UTXO_JSON" | jq -r 'keys[0]')
test -n "$TXIN" && test "$TXIN" != "null"

cardano-cli dijkstra transaction build \
  --tx-in "$TXIN" \
  --change-address "$PAYMENT_ADDR" \
  --certificate-file stake-reg.cert \
  --certificate-file pool-reg.cert \
  --out-file pool-reg-tx.raw
```

Before signing, inspect the prepared transaction and present the operator with the exact input, certificate paths, change address, pool parameters, relay endpoint, and any reported fee/deposit details. Do not sign until the operator confirms this unchanged plan.

## Sign and submit

After the signing confirmation, sign locally. Do not print the keys or signed transaction contents:

```bash
cardano-cli dijkstra transaction sign \
  --tx-body-file pool-reg-tx.raw \
  --signing-key-file payment.skey \
  --signing-key-file stake.skey \
  --signing-key-file cold.skey \
  --out-file pool-reg-tx.signed
```

Verify that the signed file exists and that the target, transaction body, and signing keys have not changed. Request a fresh, immediate confirmation before the external submission:

```bash
test -s pool-reg-tx.signed
cardano-cli dijkstra transaction submit \
  --tx-file pool-reg-tx.signed
```

Submission is an external state change. A successful CLI exit is not sufficient proof; independently verify the transaction and registration on-chain.

## Verify registration

```bash
POOL_ID=$(cardano-cli dijkstra stake-pool id \
  --cold-verification-key-file cold.vkey \
  --output-format hex)
STAKE_ADDR=$(cardano-cli dijkstra stake-address build \
  --stake-verification-key-file stake.vkey)

echo "pool id: $POOL_ID"
echo "stake address: $STAKE_ADDR"
cardano-cli dijkstra query pool-state --stake-pool-id "$POOL_ID"
cardano-cli dijkstra query stake-address-info --address "$STAKE_ADDR"
```

Record only sanitized results under `.musashi/`. Never record signing-key contents, full sensitive command output, or credentials.

## Out of scope

This skill does not delegate external stake, request faucet funds, issue the operational certificate, copy keys to a remote host, configure/restart `cardano-node`, or publish the pool ID. Those are separate operations requiring their own scope and confirmation.

## Official sources

- Musashi Network: https://www.musashi.network/
- Musashi getting started: https://leios.cardano-scaling.org/docs/testnet/getting-started/
- Musashi stake-pool registration: https://leios.cardano-scaling.org/docs/testnet/register-stake-pool/
