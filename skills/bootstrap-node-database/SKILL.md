---
name: bootstrap-node-database
description: "Bootstrap a Musashi Leios relay or block-producer node from a checksum-verified database snapshot served by a fully synced relay."
---

# Bootstrap node database

Use this skill when a new relay or block producer would otherwise need to replay the complete chain from genesis. It replaces only the node database with a snapshot from a trusted, fully synced relay, then hands the node back to the normal lifecycle workflow.

This replaces disposable experimental chain state. When the disposable chain-database exemption is validated by `execute-node-plan`, it requires no operator confirmation. It never changes keys, operational certificates, configuration, topology/genesis files, `.musashi/` state, or unrelated nodes.

## Preconditions

Require and record:

- one node ID, host ID, role, runtime identity, working directory, and database path;
- an exact absolute `chain_database_directory` registered in the node profile, plus declared protected static paths;
- the exact service/process/container stop and start operations;
- a trusted source relay FQDN or URL, confirmed fully synced (`syncProgress: "100.00"`);
- matching Musashi network incarnation, node version, config/topology/genesis hashes, and database layout;
- sufficient free disk for archive, extracted database, and temporary data;
- bounded diagnostic evidence that a complete chain database replacement is appropriate.

Stop on an ambiguous path, running writer, untrusted or unsynced source, missing checksum, network mismatch, insufficient disk, unknown archive layout, or a database path that overlaps protected static material. Revalidate official sources before use; the example source repository may lag the current testnet.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, the node profile/state/memory, `network/current.yaml`, and this skill's `metadata.yaml`. Inspect the target process, service, paths, owner, permissions, ports, and other nodes on the host.
2. Confirm the source relay is fully synced and serves the same network, protocol incarnation, node version, and snapshot format. Record its observed tip and source URL.
3. Use `stop-node` to stop the target. The disposable-chain-database exemption covers this node-local stop only after confirming it affects no shared services or other nodes. Capture status and bounded logs before changing state.
4. Resolve all paths to absolute paths. Put archive, checksum, and extraction directory outside the final database path, under the declared node working directory.
5. Verify the stopped writer and resolve the database path again. Remove only the exact registered `chain_database_directory`; never use a wildcard, recursive parent target, or remove the working directory. Never touch `keys/`, `config/`, `state/`, `.musashi/`, topology/genesis files, or any declared protected static path. Do not back up or rename the previous chain database.
6. Download the snapshot and checksum with fail-closed HTTP behavior, retries, bounded timeouts, and resume support. Never pipe a download to a shell or execute archive contents.
7. Verify the checksum against the exact archive before extraction. Stop on a mismatch, HTML/error response, missing manifest entry, or ambiguous filename.
8. Inspect the archive listing and reject absolute paths, `../` traversal, unexpected archive types, or unrelated files. Extract into a fresh temporary directory; never extract over the live database.
9. Identify the contained database directory explicitly. The repository example extracts `db-leios` and comments a rename to `db`; do not assume that mapping without checking the current node command and layout.
10. Validate the extracted layout, ownership, free space, and write permissions. Move it into the declared database path only after confirming the previous database was removed and no protected path is affected.
11. Verify configuration, topology, genesis files, keys, certificates, permissions, and service command are unchanged. Ensure private keys remain protected.
12. Use `start-node` to start the node. Validate process identity, socket/API availability, peers, expected network, and advancing tip/sync progress. A snapshot accelerates synchronization; it is not proof of synchronization.
13. Record diagnostic evidence, source URL/FQDN, source tip/sync status, archive and checksum, verification result, target path, extraction mapping, node version, and post-start observations in the node memory/report. Do not record or retain a chain database backup.

## Download and verification shape

Adapt only after paths and source are confirmed; execute through `execute-node-plan`:

```bash
set -euo pipefail
umask 077

WORKING_DIR=/absolute/path/to/node
DOWNLOAD_DIR="$WORKING_DIR/.bootstrap"
ARCHIVE="$DOWNLOAD_DIR/leios.full.tar.zst"
CHECKSUM="$DOWNLOAD_DIR/leios.full.tar.zst.sha256"
EXTRACT_DIR="$DOWNLOAD_DIR/extracted"
SOURCE_BASE="https://<trusted-fully-synced-relay>"

mkdir -p "$DOWNLOAD_DIR" "$EXTRACT_DIR"
curl --fail --location --retry 10 --retry-connrefused --retry-delay 10 \
  --connect-timeout 15 --max-time 3600 --continue-at - \
  --output "$ARCHIVE" "$SOURCE_BASE/leios.full.tar.zst"
curl --fail --location --retry 5 --retry-delay 5 \
  --connect-timeout 15 --max-time 120 \
  --output "$CHECKSUM" "$SOURCE_BASE/leios.full.tar.zst.sha256"

(cd "$DOWNLOAD_DIR" && sha256sum -c "$(basename "$CHECKSUM")")
tar --list --file "$ARCHIVE" >/dev/null
tar --extract --file "$ARCHIVE" --directory "$EXTRACT_DIR"
```

Before extraction, review the full `tar --list` output and validate every member path. Do not delete the archive until post-start validation succeeds and the retention decision is recorded.

## Failure and success

Stop and report evidence on checksum failure, source mismatch, path traversal, unexpected contents, permission errors, failed extraction, insufficient disk, failed startup, or a non-progressing tip. Do not retry a failed replacement blindly.

Success means a checksum-verified snapshot from a trusted fully synced relay is installed at the declared database path, protected static material is intact, the node starts through the normal lifecycle workflow, and observations show the expected node identity with a progressing tip.

## Sources

- `https://github.com/0xconssize/leios/blob/main/reload-leios-db.sh`
- `https://github.com/0xconssize/leios/blob/main/README.md`
- `https://leios.cardano-scaling.org/docs/testnet/getting-started/`
- `https://github.com/input-output-hk/ouroboros-leios/releases`
