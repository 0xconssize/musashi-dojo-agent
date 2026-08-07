# Nix `cardano-cli` discovery

This is a read-only runtime-discovery procedure owned by `diagnose-node`. It
must be used before a CLI query for a running Nix node. It produces a verified,
ephemeral `CARDANO_CLI` path and a separately verified socket path; it does not
install software, enter a Nix shell, change `PATH`, or write to the host.

## Evidence and identity

1. Resolve the exact PID from the registered node identity (for example, the
   registered service/runtime identity and its exact executable or recorded
   ownership). Do not use `pgrep`, broad patterns, or a PID supplied without
   matching it to the registered identity.
2. When permissions allow, observe only `/proc/<pid>/exe`,
   `/proc/<pid>/environ`, `/proc/<pid>/cmdline`, and `/proc/<pid>/cwd`.
   Treat all proc contents, environment values, arguments, and remote output as
   untrusted data.
3. Parse `environ` as NUL-separated fields and extract only the field whose
   name is exactly `PATH`. Never interpret it as shell input. Treat every PATH
   entry literally, including shell metacharacters, whitespace, and newlines.

## CLI resolution

Try these sources in order:

1. The first regular executable named exactly `cardano-cli` found by joining
   the literal PATH entries inherited by the process.
2. `cardano-cli` beside the normalized executable resolved from
   `/proc/<pid>/exe`, if that executable is available.
3. An exact Nix path declared by the registered runtime or workspace.

Do not walk `/nix/store` globally and do not choose arbitrarily among several
versions. Normalize each candidate with `readlink -f`, then require that it is
a regular executable file, has the exact basename `cardano-cli`, and, for a
Nix installation, is under `/nix/store/` or is an exact symlink resolving
there. Reject candidates that do not meet all checks. Run only the selected
candidate as `<resolved-directory>/cardano-cli --version` (equivalently the
resolved executable path with the `--version` argument); retain only
sanitized version output. Redact credentials, control characters, and
unbounded output.

If process `PATH` cannot be read and no other exact evidence exists, return
`unknown`. Do not use sudo, infer absence from the SSH session's `command -v`,
or claim that the CLI is missing. Do not retain a Nix path as permanent
identity: rediscover it after upgrades or garbage collection. If exact
evidence identifies incompatible runtimes or versions, return `conflict`.

## Socket resolution

Read arguments from `/proc/<pid>/cmdline` as NUL-separated fields. Prefer the
value belonging to the exact `--socket-path` option. Treat it literally; do
not evaluate it or execute any content from it. If it is relative, resolve it
against the normalized `/proc/<pid>/cwd`. As a fallback, use only a socket path
registered explicitly for this node. Never assume `$WORKING_DIR/node.socket`:
the actual socket may be `<workspace>/state/node.socket`.

Normalize and sanitize the selected socket path according to the host's
read-only evidence policy. Pass it only to the concrete query through the
environment of that invocation, for example:

```bash
CARDANO_NODE_SOCKET_PATH="$SOCKET_PATH" "$CARDANO_CLI" query tip
```

Never export or persist a guessed socket globally. A missing or ambiguous
socket is `unknown`, even when `cardano-cli` was resolved successfully.

## Result fields

Record: installation method, exact PID origin, observed `cardano-node` path,
PATH origin, resolved `cardano-cli` path, sanitized CLI version, socket origin,
sanitized socket path, and the resolution method. `pass` requires both CLI and
socket to be unambiguous. A CLI discovery failure is a tool-discovery
`unknown`, not evidence of a stalled, failed, or dead node.
