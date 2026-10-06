# Metsuke integration modes

Use this reference only after `configure-metsuke` has resolved one exact block producer and observed its real runtime. Select one mode explicitly; never infer a fallback from a failed preflight.

## Own unit: metrics only

- Source template: the current official minimal configuration.
- Runtime template: the current official hardened standalone service.
- Preconditions: the node's Prometheus endpoint is reachable over IP-literal loopback from the planned service context.
- Isolation: Metsuke has its own system service and lifecycle and receives no journal-reading group.
- Limitation: no trace lines are collected. Record the resulting rewards-program state as conditional or incomplete according to current service documentation.
- Handoff: `start-metsuke` may activate the standalone service.

Use this as a bounded pilot or fallback, not as an implicit replacement for a requested trace-collecting mode.

## Own unit: journald

- Source template: the current official journald configuration.
- Runtime template: the current official hardened journald service.
- Preconditions: the node runs as an exact systemd unit, emits the required machine-format traces to a journal readable from the planned service context, and the absolute `journalctl` executable is verified.
- Privilege: the published unit grants journal-reading access that can expose entries from other units on the host. Assess this host-level impact before applying the configuration.
- Required rendering: set the exact node unit and exact `journalctl` path; a nonexistent unit may otherwise yield a running Metsuke process with no trace submissions.
- Isolation: Metsuke has its own service and can restart without restarting the node.
- Handoff: `start-metsuke` may activate the standalone service.

Do not select this mode for a per-user systemd unit merely because its logs are visible to the operator. Prove the planned Metsuke service identity can follow that exact journal stream.

## Node unit: pipe

- Source template: the current official pipe configuration.
- Runtime template: the current official node-unit drop-in.
- Preconditions: the exact node unit, effective command, output mode, user, groups, sandbox, service type, watchdog, reload command, restart behavior, state directories, and systemd specifiers are known and compatible. The node must be stopped before the live drop-in is placed.
- Privilege: Metsuke inherits the node unit's identity, groups, and sandbox. The signing credential becomes readable to every process in that unit. Accept only the selected block producer's existing Leios key.
- Lifecycle: systemd supervises the pipeline shell rather than `cardano-node`; the process topology and health checks therefore differ from a normal node unit.
- Handoff: activation starts the node and Metsuke together and belongs to a separate `start-node` plan. `start-metsuke` must not restart the node.

Refuse pipe mode when the node is running, when quoting or `%` expansion is unresolved, when readiness/watchdog/reload semantics remain incompatible, when the supervisor cannot validate both children, or when the change would broaden key exposure.

## Unsupported in this MVP

Container entrypoints, shell sessions, non-systemd supervisors, NixOS modules, relays, multiple Metsuke instances sharing a spool, and host-side access through a container runtime are advisory only. Do not render or apply them with this skill.
