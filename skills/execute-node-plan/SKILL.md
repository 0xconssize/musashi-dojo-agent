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
- Required confirmations recorded for the exact plan and scope.

## Workflow

1. Read `AGENTS.md`, `HOST_SAFETY.md`, `SECURITY.md`, network freshness declarations, execution profile, target records, and the operation-specific skill.
2. Refuse execution in advisory mode. Never claim a local or remote capability that has not been observed.
3. Validate the plan and resolve every node to one registered host, access method, runtime identity, relevant path, and shared-host dependency.
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
