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
6. Save generated commands, scripts, and plans under `.musashi/generated/`. Inspect downloads, sources, affected paths, privileges, recursion, wildcards, and recovery before execution. Never download and immediately execute. Apply the generated-shell quality gate below before computing the final digest or requesting confirmation.
7. Execute short steps through runtime-provided tools only. Bound each step below the caller or transport timeout; split longer observation windows into resumable read-only polls. Capture command, target, timestamps, exit status, sanitized output, and errors in a command-result record.
8. Mark mutation boundaries and irreversible external effects explicitly. After a service start, transaction, signed submission, or another externally visible effect, persist the observed commit point before auxiliary validation. A later rollback does not erase that effect.
9. Stop on unexpected output, target drift, failed precondition, denied capability, or failed validation. Run recovery only when present, safe, and separately authorized. If the transport or executor is interrupted after a possible mutation, first reconcile the exact remote state; do not assume rollback ran, retry the action, or request confirmation for a replacement plan while state is unknown.
10. Validate real state independently of exit status. Check the operation's declared success criteria and unaffected nodes or services sharing the host. Distinguish operation failure from validation-harness failure and inconclusive observation.
11. Record plan, results, observations, validation, rollback outcome, irreversible effects, and final status under `.musashi/`. Update host or node state only from observed facts.

## Generated-shell quality gate

Before binding confirmation to a plan that executes generated shell:

- Run the applicable shell syntax checker on every generated script and embedded shell body. Run `shellcheck` when already available; do not install it as part of the operation.
- Use strict mode deliberately. Declare or pass every variable before first use, and keep the same variable name across local assignments, remote environment maps, heredocs, validation, and rollback. Review all `set -u` paths, including failure traps.
- Validate embedded `jq`, regular expressions, quoting, and nested heredoc expansion against the actual bounded input or a sanitized fixture. Do not assume a string that is valid in one quoting layer survives another.
- Resolve executable paths from observed runtime evidence. Do not assume an interactive `PATH`, adjacency to another executable, or unprivileged readability of `/proc` and protected files.
- Exercise the complete read-only preflight and validation paths before confirmation. For modifying branches, use non-mutating fixtures or an isolated staging target to prove parsing, variable plumbing, ownership checks, and rollback predicates without touching the live destination.
- Put privileged reads, redirections, pipelines, and parsing wholly in the required privilege context. `sudo command > protected-file` and `sudo read | unprivileged-parser` do not elevate the shell redirection or parser.
- Record the validated script digest in the plan and compare it again immediately before execution. Any script change invalidates the plan digest and confirmation.

## Source authority

For Musashi operations, official Ouroboros Leios releases determine the latest release, assets, compatibility, and release-specific actions. The Musashi getting-started guide determines testnet configuration and procedures. Never import Cardano mainnet assumptions.

## Success

Every executed step stayed within the approved scope, evidence demonstrates the intended state, shared workloads remain unaffected, and the local audit record is complete.
