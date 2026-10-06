---
name: install-metsuke
description: "Install one Metsuke client for one registered Musashi block producer from a checksum-verified official client release, leaving it stopped and unconfigured."
---

# Install Metsuke

Install only the Metsuke client binary beside one registered Musashi block producer. Treat Metsuke as an auxiliary component of that node, not as another node. Configuration, signing keys, services, trace integration, startup, submissions, monitoring, updates, and removal are separate operations.

## Preconditions and scope

1. Read `AGENTS.md`, `SECURITY.md`, `HOST_SAFETY.md`, this skill's `metadata.yaml`, `network/current.yaml`, and `network/known-issues.yaml`.
2. Require one explicit registered node ID, its host ID, a current host assessment, verified access, the node runtime identity, an exact absolute target path, observed host platform and architecture, and separate selected releases for the node and the Metsuke client. Scope is `single-node`.
3. This MVP supports one `block-producer` on Linux `x86_64` or `aarch64` using the official prebuilt static binary. Refuse relays, other operating systems or architectures, NixOS modules, source builds, containers, and fleet installation.
4. Use `network/current.yaml` only to verify the Musashi node's network identity, role, and node release. It is not authority for the Metsuke client release. Never substitute a node tag such as `prototype-*` for a Metsuke tag such as `client-v*`.
5. Resolve the node, host, access method, runtime identity, target and staging paths, required privilege, all other nodes and services on the host, and expected impact. Obtain verified access through `connect-host`; host identity, connection freshness, and shared-host policy remain governed by `AGENTS.md` and `HOST_SAFETY.md`.

Installation changes host state. Check the affected path, artifact, checksum, privileges, disruption, validation, recovery, and shared workloads under `SECURITY.md`, `HOST_SAFETY.md`, and `execute-node-plan`. Installation does not restart the node or Metsuke.

## Release and artifact selection

1. Revalidate the Metsuke quickstart, details page, and official GitHub releases immediately before planning an installation.
2. From the official `input-output-hk/metsuke` releases, select the most recently published non-draft release, including one marked as a prerelease by GitHub, whose tag matches `^client-v[0-9]+\.[0-9]+\.[0-9]+$`. Do not rely on `/releases/latest`, list order, or tags from the independent `fetch-v*` and `server-v*` release families.
3. Compare the selected client version with the version supported by the deployed Metsuke service documentation and review the selected release notes. Stop and record a source conflict if compatibility is not explicit.
4. Map only an observed Linux architecture to an exact asset pair:

   | Observed machine | Binary | Checksum sidecar |
   | --- | --- | --- |
   | `x86_64` | `metsuke-static-x86_64-linux` | `metsuke-static-x86_64-linux.sha256` |
   | `aarch64` or `arm64` | `metsuke-static-aarch64-linux` | `metsuke-static-aarch64-linux.sha256` |

5. Require both files as assets of the selected tagged release. Prefer the tag-specific GitHub release URLs. An unversioned `/files/` mirror may corroborate the release only when its computed digest and sidecar are identical to the selected release assets.
6. Require an official checksum independent of the downloaded binary. When the release API supplies an asset digest, require the sidecar, API digest, and computed digest to agree. Record available tag-verification evidence, but do not claim that the binary has a detached signature when none is published.

## Preflight

Inspect the real host without changing it:

- Verify OS and architecture independently, free space, target-parent ownership and mode, canonical paths, symlinks, mount boundaries, and the tools needed to inspect the binary. Do not install helper packages as part of this skill.
- Inspect the exact target, any registered Metsuke component state, exact processes, system and user units, containers, supervisors, and automatic launch mechanisms. Refuse a running or configured Metsuke workload because placing the binary could activate or alter an existing deployment.
- Refuse an ambiguous target, a symlink target, an unexpected canonical path, or an unrelated file. The documented target is `/usr/local/bin/metsuke`; any other target must be explicit and justified.
- Check the target against the intended configuration handoff. A standalone hardened system unit must be able to execute the binary under its effective sandbox. In particular, do not install under `/home` for a unit using `ProtectHome=true`; select a system path such as `/usr/local/bin/metsuke` in the original installation plan instead of requiring a later relocation. A user-local target is acceptable only when the operator explicitly selects a compatible non-system runtime and configuration remains a separate operation.
- If the target already contains the same official bytes and version, validate it and return a no-op success when ownership and mode are also correct. A metadata correction requires a separate modifying plan. Any different existing installation belongs to a future update workflow and must not be overwritten.
- Observe the block producer and shared-host workloads before installation so the same signals can be compared afterward.

## Workflow

1. Prepare the operation plan required by `execute-node-plan`. Declare the single node and host, exact staging and target paths, release tag, asset URLs, expected digests, owner, group, mode, privileges, absence of intended disruption, validation criteria, and exact rollback steps.
2. Hand the operation to `execute-node-plan` for target revalidation, execution, and audit.
3. During execution, stage the binary and sidecar in the versioned generated-artifact location required by `SECURITY.md`. Keep them non-executable until provenance and integrity checks pass. Never use a download-and-execute pipeline.
4. Inspect the sidecar before using it. Require exactly one SHA-256 entry whose basename is the selected binary; reject absolute paths, traversal, extra entries, malformed digests, and filename disagreement.
5. Verify the computed SHA-256 against the sidecar and, when published, the release API digest. Stop on any mismatch or missing evidence.
6. After checksum verification, inspect the locally staged artifact as a regular static Linux ELF and verify that its machine architecture matches the observed host. Accept both `file(1)` descriptions ending in `statically linked` and `static-pie linked`; static PIE is a valid static ELF form. Do not use that wording as a substitute for the ELF-header and checksum checks, and do not reject an artifact solely because `file(1)` uses the `static-pie linked` wording. This MVP does not extract archives or accept scripts.
7. For a remote target, use only a runtime-provided transfer capability to place those locally verified bytes at the plan's exact remote staging path, then recompute the digest and repeat the regular-file and ELF architecture checks on the target; this skill does not implement a transport. For a local target, retain the already verified staged artifact. Only then make that target-host artifact executable as declared in the scoped operation and invoke only the documented `--version` option. Require the first whitespace-delimited token of the reported output to equal the version suffix of the selected `client-v*` tag; allow trailing build metadata such as `0.2.1 (commit)`.
8. Recheck that the target is still absent, then install only the verified binary at the declared target with the declared owner, group, and mode `0755`. Do not create configuration, copy or inspect keys, create users or groups, define a service, reload systemd, alter a node command, expose a port, or start a Metsuke workload.
9. If validation fails after creating a previously absent target, use only the exact scoped rollback after checking current state. Never recurse or remove a pre-existing path. Remove a newly created parent directory only if it was recorded exactly and is still empty, unchanged, and neither a symlink nor a mount point.

Keep integrity, file-format, architecture, version, and placement checks as separate named results. A failed ELF wording or version parser is not a checksum mismatch. Report the observed and expected value for the failed check without weakening checks that already passed.

## Validation and handoff

Independently verify all of the following rather than relying on exit status:

- The installed target is the declared regular file, not a symlink, and its SHA-256 equals the selected official digest.
- Its ELF architecture, `--version` output, owner, group, and mode match the plan and selected release.
- No long-running Metsuke process, service, container, or listener was started or enabled; only the bounded, completed `--version` probe ran.
- The block producer retains the same runtime identity and continues making real progress; other registered nodes and shared-host workloads remain unaffected.
- No configuration, signing key, spool, node unit, firewall rule, or unrelated path changed.

Write sanitized results through the current operation-report and memory contracts. Record the Metsuke tag, source URL, asset, digest, platform, installed path, ownership, mode, and stopped/unconfigured state as auxiliary-component evidence. Do not overwrite or extend the node's strict profile, release, runtime identity, installation method, or state fields.

Hand off to `configure-metsuke` when that skill exists. Installation success grants no authority to configure or start the component.

## Failure and success

Stop on unresolved scope, stale or conflicting sources, unsupported role or platform, missing official checksum, unverified provenance, version mismatch, path ambiguity, existing different bytes, existing Metsuke runtime integration, insufficient inspection capability, rejection by the governing execution policy, or any shared-host impact.

Success means the selected official `client-v*` static binary is checksum-verified at the exact declared path with verified provenance, version, architecture, ownership, and mode; Metsuke remains stopped and unconfigured; and the node and shared-host workloads remain unaffected. An already-correct installation may satisfy this as an observed no-op.

## Official sources

- Metsuke quickstart: https://metsuke-leios.play.dev.cardano.org/
- Metsuke details: https://metsuke-leios.play.dev.cardano.org/details
- Official Metsuke releases: https://github.com/input-output-hk/metsuke/releases
