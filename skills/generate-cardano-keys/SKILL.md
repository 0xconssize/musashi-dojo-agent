---
name: generate-cardano-keys
description: "Generate and safely manage the Cardano payment, stake, cold, KES, VRF, and BLS keys required for a Musashi Dojo Leios testnet block producer."
---

# Generate Cardano keys

Generate local key material for a Musashi Dojo Leios testnet block producer. This skill does not register a pool, submit transactions, expose a node, or start a block producer.

## Preconditions

1. Read `AGENTS.md`, `SECURITY.md`, and `HOST_SAFETY.md`.
2. Confirm that the operator explicitly wants local key generation and identify one dedicated Musashi testnet working directory.
3. Confirm that the target is disposable testnet infrastructure, not a mainnet or production directory.
4. Verify `cardano-cli` and its version using the official Musashi Leios release or the `dev-testnet` Nix shell.
5. Stop if target key files already exist unless the operator explicitly chooses a new directory or confirms deliberate rotation.

Key generation is fully local and does not require a running node, a node socket, network access, or a synchronized chain. The current guide uses the `dijkstra` command group; revalidate that command group against the official guide before future operations if the network advances eras.

This offline flow is separate from SRE `observe`: when targeting a running Nix
node, use `diagnose-node`'s `nix-cardano-cli-discovery` reference and set a
verified `CARDANO_CLI` path. The offline `dev-testnet` Nix shell may still be
used here when explicitly selected; it must not be used to discover a running
node's runtime.

## Choose the CLI runtime

Use either a verified local `cardano-cli` or the official Musashi/Leios Docker image. The image tag currently shown in the getting-started guide is tied to the historical `prototype-2026w30` example; check the official releases and image availability before selecting a newer tag. Do not use `latest`.

For Docker, pull the explicitly selected image and mount only the dedicated keys directory. Do not use host networking, privileged mode, the Docker socket, or a broad workspace mount:

```bash
export MUSASHI_IMAGE=ghcr.io/input-output-hk/ouroboros-leios/cardano-node-testnet:prototype-2026w30
docker pull "$MUSASHI_IMAGE"
docker image inspect "$MUSASHI_IMAGE" >/dev/null
```

Run the generation commands inside the container as the host user so files do not become root-owned. Set `WORKING_DIR` and prepare the target directory on the host first, then run the key-generation block with `/keys` as the working directory:

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --entrypoint /bin/sh \
  --volume "$WORKING_DIR/keys:/keys" \
  --workdir /keys \
  "$MUSASHI_IMAGE" \
  -eu -c '
    umask 077
    cardano-cli --version
    cardano-cli dijkstra address key-gen \
      --verification-key-file payment.vkey \
      --signing-key-file payment.skey
    cardano-cli dijkstra stake-address key-gen \
      --verification-key-file stake.vkey \
      --signing-key-file stake.skey
    cardano-cli dijkstra node key-gen \
      --cold-verification-key-file cold.vkey \
      --cold-signing-key-file cold.skey \
      --operational-certificate-issue-counter-file opcert.counter
    cardano-cli dijkstra node key-gen-KES \
      --verification-key-file kes.vkey \
      --signing-key-file kes.skey
    cardano-cli dijkstra node key-gen-VRF \
      --verification-key-file vrf.vkey \
      --signing-key-file vrf.skey
    cardano-cli dijkstra node key-gen-BLS \
      --verification-key-file bls.vkey \
      --signing-key-file bls.skey
  '
```

The container must not receive the node socket or any directory containing unrelated credentials. If the image does not provide `/bin/sh`, use its documented shell entrypoint or run each `cardano-cli` command with the same restricted mount and user mapping.

## Key handling

- Use a dedicated `$WORKING_DIR/keys` directory under the Musashi workspace.
- Set `umask 077` before creating signing keys.
- Never print, paste, upload, commit, or record the contents of `*.skey`.
- Keep `cold.skey` offline and encrypted except when explicitly needed to issue an operational certificate or sign pool registration.
- Store generated keys and sanitized operation records under `.musashi/`; never place them in the versioned repository.
- Do not use generated testnet keys on mainnet.
- Explain the impact and confirm the exact target before writing private material.

## Prepare the target

With the operator-approved workspace in `$WORKING_DIR`:

```bash
umask 077
test -n "$WORKING_DIR"
mkdir -p "$WORKING_DIR/keys"
cd "$WORKING_DIR/keys"
test "$(pwd -P)" = "$(realpath "$WORKING_DIR/keys")"
for file in payment.vkey payment.skey stake.vkey stake.skey cold.vkey cold.skey \
  opcert.counter kes.vkey kes.skey vrf.vkey vrf.skey bls.vkey bls.skey; do
  test ! -e "$file" || {
    echo "Refusing to overwrite existing key material: $PWD/$file" >&2
    exit 1
  }
done
```

Before execution, state the exact target directory and files to be created. Require fresh confirmation if the directory, command, or scope changes.

## Generate payment and stake keys

```bash
cardano-cli dijkstra address key-gen \
  --verification-key-file payment.vkey \
  --signing-key-file payment.skey

cardano-cli dijkstra stake-address key-gen \
  --verification-key-file stake.vkey \
  --signing-key-file stake.skey
```

## Generate node operational keys

```bash
cardano-cli dijkstra node key-gen \
  --cold-verification-key-file cold.vkey \
  --cold-signing-key-file cold.skey \
  --operational-certificate-issue-counter-file opcert.counter

cardano-cli dijkstra node key-gen-KES \
  --verification-key-file kes.vkey \
  --signing-key-file kes.skey

cardano-cli dijkstra node key-gen-VRF \
  --verification-key-file vrf.vkey \
  --signing-key-file vrf.skey
```

## Generate Leios BLS keys

```bash
cardano-cli dijkstra node key-gen-BLS \
  --verification-key-file bls.vkey \
  --signing-key-file bls.skey
```

The Musashi stake-pool guide requires the BLS key in the pool-registration certificate. It notes that BLS is accepted but not yet active in the testnet at the time of that guide revision. Revalidate this before registration.

## Validate without exposing secrets

Validate only filenames, permissions, and public metadata:

```bash
chmod 700 "$WORKING_DIR/keys"
find "$WORKING_DIR/keys" -maxdepth 1 -type f -name '*.skey' -exec chmod 600 {} +
find "$WORKING_DIR/keys" -maxdepth 1 -type f -printf '%f %m\n' | sort
cardano-cli dijkstra stake-pool id \
  --cold-verification-key-file "$WORKING_DIR/keys/cold.vkey" \
  --output-bech32
```

Never run `cat`, `sed`, `jq`, or logging commands against signing-key files. Confirm every expected file exists and no unexpected key files were created; do not treat exit status alone as proof.

Expected files:

- Payment: `payment.vkey`, `payment.skey`
- Stake: `stake.vkey`, `stake.skey`
- Pool identity: `cold.vkey`, `cold.skey`, `opcert.counter`
- KES: `kes.vkey`, `kes.skey`
- VRF: `vrf.vkey`, `vrf.skey`
- Leios BLS: `bls.vkey`, `bls.skey`

Report only the target path, CLI runtime and version, public pool ID, and generated filenames. Never report private-key contents or secret-bearing command output.

## Out of scope

This skill does not create an address or request faucet funds, issue an operational certificate, build/sign/submit registration or delegation transactions, copy keys remotely, configure/restart `cardano-node`, or publish a pool ID.

Each later operation requires its own target verification, scope, and authorization.

## Official sources

- Musashi Network: https://www.musashi.network/
- Musashi getting started: https://leios.cardano-scaling.org/docs/testnet/getting-started/
- Musashi stake-pool registration: https://leios.cardano-scaling.org/docs/testnet/register-stake-pool/
