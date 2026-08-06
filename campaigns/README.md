# Experimental campaigns

Campaigns coordinate a time-bounded instruction from the Musashi testnet team across existing skills. They are temporary operational plans, not a replacement for canonical knowledge and not a fleet scheduler.

## Lifecycle

1. **Proposed** — capture the instruction, authority, source, scope, release, expiry, and unknowns. Do not execute.
2. **Approved** — an operator confirms the source and the exact campaign scope.
3. **Pilot** — prepare and execute against one explicitly selected participant.
4. **Active** — continue only after pilot validation, tracking every participant independently.
5. **Completed, paused, cancelled, or expired** — preserve the history and stop new executions when the campaign ends or its authority becomes stale.

The agent must stop on unverified authority, incompatible release or capability, ambiguous target identity, conflicting sources, key overwrite risk, undeclared host impact, or any step that exceeds the campaign's declared mode. A failed pilot stops rollout.

## Authority and freshness

Every campaign must identify who issued the instruction, where it was published, when it was issued, which network and release it affects, and when it expires. A message without a stable source remains `unverified` until an operator confirms it. A newer official instruction must supersede the older campaign explicitly.

Temporary campaign instructions must not be copied into `network/current.yaml`, a skill, or a playbook without a separate reviewed repository change. Capture the lesson as a knowledge-feedback issue when the campaign reveals a durable correction.

## Security

Campaign state contains identifiers, statuses, hashes, paths, and sanitized evidence references only. Never store signing-key contents, credentials, tokens, private addresses, or raw operational logs in a campaign definition or shared campaign run.

Generating keys, signing transactions, submitting transactions, changing hosts, updating nodes, and recovery remain separate confirmation-controlled operations. A campaign can invoke an existing skill, but cannot weaken that skill's safety rules.

The runtime may schedule or invoke a campaign, but this repository provides no scheduler and no automatic campaign activation.
