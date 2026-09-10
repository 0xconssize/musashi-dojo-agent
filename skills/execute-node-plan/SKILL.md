---
name: execute-node-plan
description: "Safely execute an approved structured plan against registered Musashi nodes through verified runtime capabilities."
---

# Execute node plan

Execute only a validated, explicitly scoped plan. Concrete install, lifecycle, diagnosis, update, and recovery procedures belong to their operation skills.

## Inputs

Require:

- A plan conforming to `schemas/execution-plan.schema.json`.
- Current execution capability profile.
- Registered host and node records for every target.
- Verified connection profiles.
- A confirmation record valid for the exact plan and scope, unless the plan qualifies for the disposable chain-database exemption.

## Confirmation protocol

The canonical SHA-256 `plan_digest` remains the identity of the reviewed immutable plan. For every plan that requires confirmation, derive the displayed four-digit decimal challenge from the first eight hexadecimal characters of the recomputed digest: interpret them as an unsigned hexadecimal integer, take modulo `10000`, and zero-pad to four digits. Show the operation, node and host, affected paths, privileges, disruption, validation criteria, full digest, and challenge. Accept only that exact challenge for the recomputed digest immediately before execution.

The challenge is a phone-friendly acknowledgement, not a credential or security secret. Never use it to authorize a changed plan, and never omit the full digest from the local audit record. A changed command, target, path, privilege, disruption, scope, or plan content requires a fresh digest, challenge, and confirmation even if the four digits happen to repeat.

`confirmation.required: false` is permitted for a modifying plan only with `method: disposable-chain-database-exemption` and `exemption: disposable-chain-database-reload`. This exception is valid only when all of the following are observed and recorded:

- the operation replaces the complete chain database for exactly one registered node;
- the target profile declares an exact absolute `chain_database_directory` and relevant `protected_static_paths`;
- every destructive affected path resolves exactly to that database directory, is not a symlink or mount point, and is disjoint from protected static paths, configuration, workspace, and broader data roots;
- the target writer is verified stopped, the host identity and single-node scope are current, and the action has no shared-host or unrelated-service impact;
- diagnostic evidence supports a full database reload, and the replacement snapshot has passed source, checksum, and layout preflight checks outside the live database path.

Reject the exemption for any ambiguity, partial volatile-state deletion, protected-path overlap, broad or recursive target, running or unverified writer, multiple-node scope, host-level change, or missing preflight observation. Such a plan requires the normal four-digit confirmation.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, `SECURITY.md`, network freshness declarations, execution profile, target records, and the operation-specific skill.
2. Refuse execution in advisory mode. Never claim a local or remote capability that has not been observed.
3. Validate the plan and resolve every node to one registered host, access method, runtime identity, relevant path, and shared-host dependency. Recompute the canonical plan digest. For `four-digit-code`, recompute and verify the four-digit challenge; for the disposable-chain-database exemption, validate every exemption condition above.
4. Re-verify each modifying target with `connect-host`. Stop on identity conflict, stale connection evidence, broadened scope, or changed plan.
5. Inspect current state before modification. Revalidate Musashi sources whenever the plan contains a mutable network value, release asset, testnet command, or release-specific recovery action.
6. Save generated commands, scripts, and plans under `.musashi/generated/`. Inspect downloads, sources, affected paths, privileges, recursion, wildcards, and recovery before execution. Never download and immediately execute.
7. Execute short steps through runtime-provided tools only. Capture command, target, timestamps, exit status, sanitized output, and errors in a command-result record.
8. Stop on unexpected output, target drift, failed precondition, denied capability, or failed validation. Run recovery only when present, safe, and separately authorized.
9. Validate real state independently of exit status. Check the operation's declared success criteria and unaffected nodes or services sharing the host.
10. Record plan, results, observations, validation, and final status under `.musashi/`. Update host or node state only from observed facts.

## Source authority

For Musashi operations, official Ouroboros Leios releases determine the latest release, assets, compatibility, and release-specific actions. The Musashi getting-started guide determines testnet configuration and procedures. Never import Cardano mainnet assumptions.

## Success

Every executed step stayed within the approved scope, evidence demonstrates the intended state, shared workloads remain unaffected, and the local audit record is complete.
