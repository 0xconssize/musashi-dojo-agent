# Security Policy

Musashi Dojo is a testnet, but the host is not disposable. Protect the host environment above replaceable testnet credentials.

## Data classes

The registered complete chain database for a Musashi testnet node is disposable experimental state. It may be removed and rebuilt only after confirming the exact single-node path, a stopped writer, a compatible restoration source, and isolation from protected data. Preserve a viable recovery route; do not retain disposable database copies by default.

Configuration, topology/genesis files, keys, credentials, operational certificates, `.musashi/` state, reports, and all non-database host data are protected static material. Never include them in database reloads; preserve or back them up whenever the selected operation requires it.

## Sensitive material

Credentials, keys, tokens, SSH metadata, certificates, generated scripts, logs, and private reports belong under `.musashi/` or an operator-managed secret store. Never commit them or print complete signing keys in chat, issues, or reports.

Do not assume a credential is testnet-only without checking its context. If mainnet material is detected, stop and switch to the stricter policy.

## Impact classes

- **Observation:** inspect and record without mutating the node.
- **Modification:** constrain to the requested outcome, verify scope and prerequisites, preserve recovery for protected state, then independently validate.

## Safe handling

Inspect downloaded artifacts before execution. Verify sources where possible. Use least privilege, avoid broad wildcards and recursive operations, and preserve rollback or backup paths whenever protected state or a rollback requirement is affected.

Use only connection and execution mechanisms supplied by the agent runtime or operator. Do not implement transports, embed credentials in plans, or treat a registered connection reference as a secret store.

Generated commands, scripts, and results belong under `.musashi/`. Review them before execution, sanitize recorded output, and never use a download-and-execute pipeline. Re-evaluate scope and safety when a command or target changes; no plan digest or routine challenge is needed.

Diagnostic reports and issue drafts must minimize evidence and remove credentials, keys, tokens, unnecessary usernames, private addresses, unrelated services, and private paths. Creating a local draft grants no permission to publish it or upload attachments.

Campaign definitions and runs are shared coordination metadata, not a secret store. Keep participant-specific paths, identities, evidence, key material, credentials, and raw logs under `.musashi/campaigns/` or an operator-managed secret store. A campaign cannot reduce key-handling, transaction, host-safety, or publication safeguards.
