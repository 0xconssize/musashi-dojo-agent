---
name: install-block-producer
description: "Install a registered Musashi Dojo Leios block-producer node using Nix, verified prebuilt binaries, or Docker, while preserving keys and leaving startup to the lifecycle workflow."
---

# Install block producer

Install the selected `cardano-node` implementation and prepare one already-registered Musashi block producer. This skill covers acquisition, verification, paths, and configuration. It does not register the pool, generate keys, issue an operational certificate, start the node, create a service, or alter firewall rules.

## Preconditions and scope

1. Read `AGENTS.md`, `SECURITY.md`, and `HOST_SAFETY.md`.
2. Require one explicit node ID, one host, one installation method, declared paths, and a runtime identity. Scope is `single-node`.
3. Confirm the pool is already registered and the following local material exists under the declared keys path: `kes.skey`, `vrf.skey`, and a current `opcert.cert`. Keep `cold.skey` offline; this skill never needs it.
4. Revalidate `network/current.yaml`, the official Musashi guide, and the official Ouroboros Leios releases before selecting a release, platform, image, or command.
5. Confirm the host platform, available disk, ownership, existing processes/services/containers, port, and shared-host nodes. Refuse ambiguous paths or an existing installation that would be overwritten.
6. Confirm the Musashi configuration was pinned and verified separately. Required files are `config/config.json`, `config/topology.json`, and the relevant genesis files under the declared working directory.
7. The current network uses magic `164` and Dijkstra. These are network facts, not generic Cardano defaults; stop and revalidate if declarations or direct observation disagree.

Installation changes host state and requires explicit confirmation before package installation, directory creation outside the operator workspace, ownership changes, service definitions, firewall changes, or container creation. Execute in short steps and leave the node stopped. Use `start-node` only after installation validation.

## Common layout and validation

Use a dedicated working directory such as `$WORKING_DIR`, with no unrelated credentials inside it:

```text
$WORKING_DIR/
├── bin/       # prebuilt binaries, when that method is selected
├── config/    # pinned Musashi configuration and topology
├── db/        # node database
├── keys/      # kes.skey, vrf.skey, opcert.cert; restrictive permissions
└── state/     # socket and logs
```

Before installation, verify the exact target and expected files:

```bash
test -n "$WORKING_DIR"
test -f "$WORKING_DIR/config/config.json"
test -f "$WORKING_DIR/config/topology.json"
test -f "$WORKING_DIR/keys/kes.skey"
test -f "$WORKING_DIR/keys/vrf.skey"
test -f "$WORKING_DIR/keys/opcert.cert"
mkdir -p "$WORKING_DIR/db" "$WORKING_DIR/state"
chmod 700 "$WORKING_DIR/keys"
chmod 600 "$WORKING_DIR/keys/kes.skey" "$WORKING_DIR/keys/vrf.skey"
```

Do not copy or print signing keys. Inspect the opcert and public configuration without exposing private material. Confirm the key files are for this Musashi testnet and node; do not reuse mainnet credentials.

## Select an installation method

| Method | Use when | Important constraint |
| --- | --- | --- |
| Nix | Reproducible dependencies and a host with Nix flakes | The guide's `leios-testnet-relay` wrapper is relay-only; use the Leios dev shell and the producer invocation below. |
| Prebuilt binaries | A host needs a self-contained native install | Select the latest official non-draft release and verify its checksum before extraction. |
| Docker | The host already operates nodes as containers | Use a pinned verified image, explicit mounts, mapped port, and no privileged or host-network mode. |

Do not choose `latest`, an unverified image digest, an unofficial mirror, or a release older than the repository's selected release merely because the getting-started guide lags.

## Nix

Nix is the preferred dependency path when available. Enter the official Leios development shell from the selected release context:

```bash
nix develop github:input-output-hk/ouroboros-leios#dev-testnet
cardano-node --version
```

The shell provides `cardano-node` and `cardano-cli`; it does not authorize host service installation or start the node. Run the producer invocation only through the separately confirmed `start-node` workflow. Do not substitute `nix run ...#leios-testnet-relay`: that wrapper is for a non-producing relay.

## Prebuilt binaries

Use only assets from the selected official release and verify the matching checksum before extraction. The guide's historical example uses `prototype-2026w30`; the repository currently selects `prototype-2026w31a`, so revalidate exact asset names and checksums at execution time:

```bash
export RELEASE=prototype-2026w31a
export BASE="https://github.com/input-output-hk/ouroboros-leios/releases/download/$RELEASE"
export ARCHIVE=cardano-node-leios-x86_64-linux.tar.gz
export CHECKSUM=cardano-node-leios-x86_64-linux.sha256

mkdir -p "$WORKING_DIR/downloads"
cd "$WORKING_DIR/downloads"
curl --fail --location --remote-name "$BASE/$ARCHIVE"
curl --fail --location --remote-name "$BASE/$CHECKSUM"
sha256sum -c "$CHECKSUM"
tar -tzf "$ARCHIVE" >/dev/null
tar -xzf "$ARCHIVE" -C "$WORKING_DIR"
"$WORKING_DIR/bin/cardano-node" --version
```

Use the platform-specific official asset for Linux x86-64, Linux aarch64, or macOS aarch64. Do not execute a downloaded file before checksum verification and archive inspection. Keep the archive and checksum under `.musashi/generated/` or the operator's declared working directory, not in Git.

## Docker

The official guide documents a historical image:

```text
ghcr.io/input-output-hk/ouroboros-leios/cardano-node-testnet:prototype-2026w30
```

The repository warns that availability of a matching image for `prototype-2026w31a` is not confirmed. Select and verify an explicit image tag before use; never use `latest`:

```bash
export MUSASHI_IMAGE=ghcr.io/input-output-hk/ouroboros-leios/cardano-node-testnet:prototype-2026w30
docker pull "$MUSASHI_IMAGE"
docker image inspect "$MUSASHI_IMAGE" --format '{{.RepoDigests}}'
```

Create only the declared data directories and keep keys read-only inside the container:

```bash
mkdir -p "$WORKING_DIR/db" "$WORKING_DIR/state"
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --entrypoint cardano-node \
  --publish "$POOL_RELAY_PORT:$POOL_RELAY_PORT" \
  --volume "$WORKING_DIR/config:/data/config:ro" \
  --volume "$WORKING_DIR/db:/data/db" \
  --volume "$WORKING_DIR/state:/data/state" \
  --volume "$WORKING_DIR/keys:/data/keys:ro" \
  "$MUSASHI_IMAGE" run \
  --config /data/config/config.json \
  --topology /data/config/topology.json \
  --database-path /data/db \
  --socket-path /data/state/node.socket \
  --host-addr 0.0.0.0 \
  --port "$POOL_RELAY_PORT" \
  --shelley-kes-key /data/keys/kes.skey \
  --shelley-vrf-key /data/keys/vrf.skey \
  --shelley-operational-certificate /data/keys/opcert.cert
```

The command above is the runtime shape for `start-node`; installation itself should pull and inspect the image, create the declared directories, and leave the container stopped. Do not use `--privileged`, `--network host`, the Docker socket, or mounts containing unrelated host data. Verify that the selected user can write `db` and `state` while keys remain unreadable for writes.

## Handoff and validation

After the selected artifact is installed, but before startup:

1. Verify the installed `cardano-node --version` or image digest against the selected release.
2. Verify network-identity, genesis, and topology provenance and hashes.
3. Verify keys, opcert, database, state, and log paths and permissions.
4. Confirm no service, container, firewall, port binding, or existing shared-host workload was changed unexpectedly.
5. Record method, release, artifact/checksum or image digest, paths, runtime identity, and the stopped state under `.musashi/`.
6. Hand off to `start-node` for a separately scoped start and sync validation.

Success means the official selected implementation is installed and verifiable, required producer files are present, no private key was exposed, the node remains stopped, and shared workloads are unaffected.

## Official sources

- Musashi Network: https://www.musashi.network/
- Musashi getting started: https://leios.cardano-scaling.org/docs/testnet/getting-started/
- Musashi stake-pool registration: https://leios.cardano-scaling.org/docs/testnet/register-stake-pool/
- Official releases: https://github.com/input-output-hk/ouroboros-leios/releases
