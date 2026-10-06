---
name: execute-node-plan
description: "Execute a scoped, validated node operation through verified runtime capabilities."
---

# Execute node plan

Execute a validated, explicitly scoped operation. Concrete procedures belong to their operation skills. The execution record is for preflight, recovery, and audit, not for a digest-based approval ceremony.

## Inputs

Require:

- A plan conforming to `schemas/execution-plan.schema.json`.
- Current execution capability profile.
- Registered host and node records for every target.
- Verified connection profiles.
- A requested outcome covering the operation and a safe recovery route for any protected state at risk.

## Destructive database boundary

Complete chain-database replacement is allowed only when all of the following are observed and recorded:

- the operation replaces the complete chain database for exactly one registered node;
- the target profile declares an exact absolute `chain_database_directory` and relevant `protected_static_paths`;
- every destructive affected path resolves exactly to that database directory, is not a symlink or mount point, and is disjoint from protected static paths, configuration, workspace, and broader data roots;
- the target writer is verified stopped, the host identity and single-node scope are current, and the action has no shared-host or unrelated-service impact;
- diagnostic evidence supports a full database reload, and the replacement snapshot has passed source, checksum, and layout preflight checks outside the live database path.

Stop on ambiguity, protected-path overlap, broad targets, a running or unverified writer, multiple-node scope, shared-host impact, or missing preflight. A partial volatile-state deletion is a different recovery and needs its own evidence and exact paths. Never delete keys or other protected state to satisfy a recovery.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, `SECURITY.md`, network freshness declarations, execution profile, target records, and the operation-specific skill.
2. Refuse execution in advisory mode. Never claim a local or remote capability that has not been observed.
3. Validate the operation record and resolve every node to one registered host, access method, runtime identity, relevant path, and shared-host dependency. Apply the destructive database boundary when relevant.
4. Re-verify each modifying target with `connect-host` when evidence is missing, stale, or conflicting. Stop on identity conflict or broadened scope.
5. Inspect current state before modification. Revalidate Musashi sources whenever the plan contains a mutable network value, release asset, testnet command, or release-specific recovery action.
6. Save generated commands and scripts under `.musashi/generated/`. Inspect downloads, sources, affected paths, privileges, recursion, wildcards, and recovery before execution. Never download and immediately execute. Apply the generated-shell quality gate below.
7. Execute short steps through runtime-provided tools only. Bound each step below the caller or transport timeout; split longer observation windows into resumable read-only polls. Capture command, target, timestamps, exit status, sanitized output, and errors in a command-result record.
8. Mark mutation boundaries and irreversible external effects explicitly. After a service start, transaction, signed submission, or another externally visible effect, persist the observed commit point before auxiliary validation. A later rollback does not erase that effect.
9. Stop on unexpected output, target drift, failed precondition, denied capability, or failed validation. Diagnose and retry a bounded alternative or run a safe, scoped recovery within the requested outcome. After an interruption, reconcile exact remote state before retrying; never assume rollback ran.
10. Validate real state independently of exit status. Check the operation's declared success criteria and unaffected nodes or services sharing the host. Distinguish operation failure from validation-harness failure and inconclusive observation.
11. Record action, results, observations, validation, recovery outcome, irreversible effects, and final status under `.musashi/`. Update host or node state only from observed facts.

## Generated-shell quality gate

Before executing generated shell:

- Run the applicable shell syntax checker on every generated script and embedded shell body. Run `shellcheck` when already available; do not install it as part of the operation.
- Use strict mode deliberately. Declare or pass every variable before first use, and keep the same variable name across local assignments, remote environment maps, heredocs, validation, and rollback. Review all `set -u` paths, including failure traps.
- Validate embedded `jq`, regular expressions, quoting, and nested heredoc expansion against the actual bounded input or a sanitized fixture. Do not assume a string that is valid in one quoting layer survives another.
- Resolve executable paths from observed runtime evidence. Do not assume an interactive `PATH`, adjacency to another executable, or unprivileged readability of `/proc` and protected files.
- Exercise preflight and validation paths first. For modifying branches, use non-mutating fixtures or an isolated staging target to prove parsing, variable plumbing, ownership checks, and rollback predicates without touching the live destination.
- Put privileged reads, redirections, pipelines, and parsing wholly in the required privilege context. `sudo command > protected-file` and `sudo read | unprivileged-parser` do not elevate the shell redirection or parser.
- If a generated script changes after inspection, re-run its quality gate and re-evaluate scope and recovery.

## Source authority

For Musashi operations, official Ouroboros Leios releases determine the latest release, assets, compatibility, and release-specific actions. The Musashi getting-started guide determines testnet configuration and procedures. Never import Cardano mainnet assumptions.

## Success

Every step stayed within the requested and verified scope, evidence demonstrates the intended state, shared workloads remain unaffected, and the local audit record is complete.
