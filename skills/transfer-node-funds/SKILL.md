---
name: "transfer-node-funds"
description: "Sweep available Musashi testnet funds between verified registered node payment addresses."
---

# Transfer node funds

Transfer the spendable balance owned by one registered Musashi node to the verified payment address of one other registered node. This is an external on-chain operation. It does not transfer unreturned pool deposits, rewards, stake credentials, pool ownership, keys, node data, or service ownership.

## Preconditions and scope

- Read repository safety policy, current network declarations, execution profile, source/destination node and host records, and this skill.
- Resolve exactly one source node and one destination node. State both node IDs, host IDs, roles, access methods, runtime identities, workspaces, sockets, payment key paths, payment addresses, and every shared-host node.
- Use `connect-host` for each remote host. Require at least two matching identity signals and stop on ambiguity or conflict.
- Use only Musashi testnet magic 164 and Dijkstra. Require current official network declarations and live tips with `syncProgress == 100.00`.
- For Nix nodes, use the Nix CLI discovery reference. Resolve the exact CLI and socket; never inherit `PATH` or a guessed socket.
- Treat “all funds” as all currently spendable UTxOs controlled by the source payment key, minus the verified fee and minimum output requirements. Exclude pending/unreturned pool deposits, rewards, stake deposits, collateral belonging to another workflow, and funds not proven to be source-owned.

## Verify ownership and funding

- Derive the source address from the source `payment.vkey`; require an exact match with every selected UTxO address.
- Derive the destination address from the destination `payment.vkey`; do not accept a remembered, copied, or merely operator-labelled address.
- Query every UTxO at the verified source address. Select only exact UTxOs observed immediately before preparation; never select the first result blindly.
- Query the destination address before preparation and record its baseline balance.
- Report the total selected input, excluded funds, expected fee, destination output, source remainder, and whether any source UTxO is intentionally retained.
- If the verified Dijkstra CLI cannot represent a deterministic sweep to the destination through its current `transaction build` interface, stop in advisory mode.

## Prepare and review

- Use non-existing operation-specific paths under the source workspace. Never overwrite a transaction body or signed transaction.
- Inspect the live Dijkstra `transaction build`, `sign`, `submit`, `txid`, and debug-view interfaces before freezing commands.
- Build an unsigned transaction using every approved source input and the verified destination as the explicit change address. Do not add certificates, withdrawals, minting, metadata, scripts, governance actions, collateral, or unrelated outputs.
- Inspect the unsigned body and require exactly the approved inputs, one destination-owned output, the reviewed fee, no source output unless explicitly approved, and no extra action.
- Create a schema-valid plan under `.musashi/generated/` containing exact commands, inputs and values, destination, fee, output, keys by path, affected chain state, shared-host nodes, validation, recovery, and a SHA-256 digest.
- Explicit digest-bound confirmation is required before signing. Any change to source, destination, input, output, fee, path, key, command, network, privilege, disruption, or scope invalidates confirmation.

## Sign, confirm, and submit

- Sign only with the source `payment.skey`. Never print, copy, or move key contents.
- After signing, record the signed SHA-256 and txid; re-query source inputs, source/destination balances, tips, and any relevant pending pool state.
- Require a second fresh digest-bound confirmation immediately before one submission attempt.
- Submit once through the explicitly verified source socket. Never resubmit blindly.

## Validation and recovery

- Poll boundedly until every selected source input is consumed and the exact txid output appears at the destination address.
- Verify the destination balance increased by the reviewed output, accounting only for the transaction’s exact UTxO.
- Verify source and destination nodes plus all shared-host nodes remain running, synced, and listening on their registered ports.
- If signing fails, preserve private artifacts and stop.
- If submission status is uncertain, query every exact input, the destination output, and txid where supported; do not rebuild or resubmit without a new plan.
- Do not claim transfer completion from exit status alone.
- Moving a later pool-deposit refund, withdrawing rewards, stopping nodes, or deleting keys/data requires a separate operation and fresh authorization.
