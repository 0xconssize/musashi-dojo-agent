---
name: bootstrap-node-database
description: "Bootstrap a Musashi Leios relay or block-producer node from a checksum-verified database snapshot served by a fully synced relay."
---

# Bootstrap node database

Use this skill to bootstrap a new node or to reload a diagnosed invalid chain database. For an existing invalid database larger than **200,000,000 bytes (200 MB)**, prefer a verified HTTP(S) snapshot over replaying the chain through the node. Size alone never diagnoses corruption or authorizes replacement; at or below the threshold, choose recovery on evidence rather than forcing a snapshot.

`reload-leios-db.sh` is an operator example to inspect, **not a script to run verbatim**: it stops a user service, refreshes configuration, removes `leios.*` and `db`, downloads `leios.tar.zst` with `leios.tar.zst.sha256` from `https://leios1-rel-a-1.play.dev.cardano.org/`, extracts into `tmp-testnet`, and starts the service. Adapt only its verified snapshot source, checksum and archive layout to the registered node; never inherit its relative paths, broad deletions, config overwrite, or fixed service name. Recheck the live script and endpoint before each use.

This replaces disposable experimental chain state only after the registered chain-database boundary in `execute-node-plan` is validated. It never changes keys, operational certificates, configuration, topology/genesis files, `.musashi/` state, or unrelated nodes.

## Preconditions

Require and record:

- one node ID, host ID, role, runtime identity, working directory, and database path;
- an exact absolute `chain_database_directory` registered in the node profile, plus declared protected static paths;
- the exact service/process/container stop and start operations;
- a trusted source relay FQDN or URL, confirmed fully synced (`syncProgress: "100.00"`);
- matching Musashi network incarnation, node version, config/topology/genesis hashes, and database layout;
- sufficient free disk for archive, extracted database, and temporary data;
- bounded diagnostic evidence that a complete chain database replacement is appropriate.
- for an existing invalid database, a read-only byte count of the **exact registered chain database directory** before stopping or deleting it; record whether it exceeds 200,000,000 bytes. Do not measure the whole working directory or count keys/configuration. If the directory is missing, record size as unknown and use the diagnosed recovery path without inventing a threshold result.

Measure apparent bytes on the verified host with the exact resolved directory (for example `du --apparent-size --block-size=1 --summarize -- "$CHAIN_DATABASE_DIRECTORY"` after rejecting a symlink or mount). The threshold is strictly **greater than** 200,000,000, not greater than or equal. If the release also requires resetting a separate `leios.db` SQLite file, diagnose and register its exact path separately; the script's `leios.*` wildcard is not authority to delete it.

Stop on an ambiguous path, running writer, untrusted or unsynced source, missing checksum, network mismatch, insufficient disk, unknown archive layout, or a database path that overlaps protected static material. Revalidate official sources before use; the example source repository may lag the current testnet.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, the node profile/state/memory, `network/current.yaml`, and this skill's `metadata.yaml`. Inspect the target process, service, paths, owner, permissions, ports, and other nodes on the host.
2. Confirm the source relay is fully synced and serves the same network, protocol incarnation, node version, and snapshot format. For an invalid database over 200 MB, select the HTTP(S) snapshot flow unless source, compatibility, integrity, or disk checks fail. Record its observed tip, archive URL, checksum URL, and measured size. Never substitute a hardcoded endpoint for source verification.
3. Resolve all paths to absolute paths. Put archive, checksum, and a fresh extraction directory outside the final database path, under the declared node working directory. Leave the node running during the potentially long transfer when safe.
4. Download the snapshot and checksum with fail-closed HTTP behavior, retries, and bounded timeouts. Resume only when the partial archive belongs to the same verified source and ETag/version; otherwise start a fresh staged download. Never pipe a download to a shell or execute archive contents.
5. Verify the checksum against the exact archive before extraction. Stop on a mismatch, HTML/error response, missing manifest entry, or ambiguous filename.
6. Inspect the archive listing and reject absolute paths, `../` traversal, unexpected archive types, or unrelated files. Extract into a fresh temporary directory; never extract over the live database.
7. Identify the contained database directory explicitly. The repository example extracts `db-leios` and comments a rename to `db`; do not assume that mapping without checking the current node command and layout. Validate the extracted layout, ownership, free space, and write permissions.
8. Recheck snapshot freshness and target identity, then use `stop-node` after verifying it affects no shared services or other nodes. Capture status and bounded logs; verify a stopped writer and resolve the exact registered database path again.
9. Only now remove that directory; never use a wildcard, parent target, or working directory. Never touch keys, configuration, certificates, topology/genesis, `.musashi/`, or protected static paths. Do not back up or rename the previous chain database.
10. Move the verified staging database into the now-empty declared path. Keep the verified archive until post-start checks complete so a failed install has a usable replacement source.
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
ARCHIVE="$DOWNLOAD_DIR/leios.tar.zst"
CHECKSUM="$DOWNLOAD_DIR/leios.tar.zst.sha256"
EXTRACT_DIR="$DOWNLOAD_DIR/extracted"
SOURCE_BASE="https://leios1-rel-a-1.play.dev.cardano.org" # example only: verify current source and network

mkdir -p "$DOWNLOAD_DIR"
# Verify EXTRACT_DIR is absent, beneath the registered working directory, and not a symlink or mount.
mkdir "$EXTRACT_DIR"
curl --fail --location --retry 10 --retry-connrefused --retry-delay 10 \
  --connect-timeout 15 --max-time 3600 \
  --output "$ARCHIVE" "$SOURCE_BASE/leios.tar.zst"
curl --fail --location --retry 5 --retry-delay 5 \
  --connect-timeout 15 --max-time 120 \
  --output "$CHECKSUM" "$SOURCE_BASE/leios.tar.zst.sha256"

# Check that the manifest has exactly one expected basename and a valid digest before using it.
(cd "$DOWNLOAD_DIR" && sha256sum -c "$(basename "$CHECKSUM")")
tar --list --file "$ARCHIVE" >/dev/null
tar --extract --file "$ARCHIVE" --directory "$EXTRACT_DIR"
```

Before extraction, review the full `tar --list` output and validate every member path. Ensure the checksum manifest names exactly the selected archive basename; inspect source network/version and layout. Do not delete the archive until post-start validation succeeds and the retention decision is recorded. This is a procedure example, not permission to run against a live node without target-specific preflight.

## Failure and success

Stop and report evidence on checksum failure, source mismatch, path traversal, unexpected contents, permission errors, failed extraction, insufficient disk, failed startup, or a non-progressing tip. Do not retry a failed replacement blindly.

Success means a checksum-verified snapshot from a trusted fully synced relay is installed at the declared database path, protected static material is intact, the node starts through the normal lifecycle workflow, and observations show the expected node identity with a progressing tip.

## Sources

- `https://github.com/0xconssize/leios/blob/main/reload-leios-db.sh`
- `https://github.com/0xconssize/leios/blob/main/README.md`
- `https://leios.cardano-scaling.org/docs/testnet/getting-started/`
- `https://github.com/input-output-hk/ouroboros-leios/releases`
