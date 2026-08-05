# Security Policy

Musashi Dojo is a testnet, but the host is not disposable. Protect the host environment above replaceable testnet credentials.

## Sensitive material

Credentials, keys, tokens, SSH metadata, certificates, generated scripts, logs, and private reports belong under `.musashi/` or an operator-managed secret store. Never commit them or print complete signing keys in chat, issues, or reports.

Do not assume a credential is testnet-only without checking its context. If mainnet material is detected, stop and switch to the stricter policy.

## Impact classes

- **Read-only:** normally safe without extra confirmation.
- **Node-local reversible:** explain before execution and validate afterward.
- **Host-level:** explicit confirmation required.
- **Destructive or broad:** explicit, clearly scoped confirmation required.

## Safe handling

Inspect downloaded artifacts before execution. Verify sources where possible. Use least privilege, avoid broad wildcards and recursive operations, and preserve rollback or backup paths for changes.

Use only connection and execution mechanisms supplied by the agent runtime or operator. Do not implement transports, embed credentials in plans, or treat a registered connection reference as a secret store.

Generated plans, commands, scripts, and command results belong under `.musashi/`. Review them before execution, sanitize recorded output, and never use a download-and-execute pipeline. Required confirmation is invalid after any material plan or scope change.
