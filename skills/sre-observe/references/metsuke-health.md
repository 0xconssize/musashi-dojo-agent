# Metsuke health checks

Apply this reference only to one exact registered Metsuke auxiliary component associated with the task's single node. The task must explicitly request Metsuke checks. Observation is read-only: do not start, stop, restart, enable, reconfigure, rotate, vacuum, repair, update, drain, replay, or submit anything.

## Evidence rules

- Prefer exact registered runtime identities and canonical paths. Refuse broad process matching, filename globs, guessed services, and unbounded logs.
- Read only bounded, sanitized service status, `/proc` metadata, file metadata, effective non-secret configuration, loopback metrics responses, and logs. Never read a signing-key payload or raw spooled telemetry.
- Derive cadences, limits, destinations, selected namespaces, and validation windows from the observed effective configuration and current official documentation. Do not embed mutable defaults in a task or infer them from an old run.
- Treat exit status as one observation. Correlate supervisor, PID, executable, command, configuration, source endpoint, submissions, spool, and associated-node state.
- Sanitize pool IDs, agent IDs, payload identifiers, private hostnames, private addresses, usernames, paths, and telemetry content. Preserve only the minimum evidence needed to classify the check.
- If a required capability, path, source, timestamp, or baseline is absent or ambiguous, return `unknown`; do not turn missing evidence into health.

## Check IDs and classifications

### `metsuke-process-state`

For a standalone systemd service, require the exact unit to be loaded and active/running, `MainPID` to match the Metsuke PID, `/proc/<pid>/exe` to resolve to the registered binary, command-line arguments to name the registered configuration and runtime credential path, and the PID to belong to the expected cgroup and service identity. Verify the binary digest and `--version` evidence against installed provenance without executing an untrusted path.

For `pipe`, the unit `MainPID` may be the pipeline shell. Require the exact cgroup to contain one expected shell, one expected `cardano-node`, and one expected Metsuke child with verified executables and arguments. Verify the node's expected socket or listener belongs to the node child. Extra, missing, reparented, or ambiguous children make the result `failed` or `unknown`; an active shell alone is not healthy.

Classify a matching stable topology as `healthy`, an intentionally stopped registered component as `degraded` only when the task policy expects it to run, a contradictory or crash-looping topology as `failed`, and insufficient evidence as `unknown`.

### `metsuke-metrics-source`

Parse the effective configuration without secrets. Require an IP-literal loopback `metrics_url`, prove that the endpoint belongs to the associated node, and make a bounded read that returns structurally plausible Prometheus data. Do not follow redirects or use credentials. A reachable unrelated endpoint is a conflict, not health.

Classify a verified source as `healthy`, an unavailable or malformed expected source as `failed`, and ambiguous ownership or unavailable inspection capability as `unknown`.

### `metsuke-submission-progress`

Read bounded sanitized logs since the previous observation or component start, whichever is later. Require accepted metrics submissions to advance according to the observed effective scrape and upload behavior. Record rejection reasons only after sanitization. Distinguish destination rejection, signing failure, transport failure, retry/backoff, and lack of eligible data.

An advancing accepted-submission signal is `healthy`; repeated rejection, signing failure, or no progress beyond the derived window is `failed`; transient retry within policy may be `degraded`; and an observation made before enough time or without reliable timestamps is `unknown`.

### `metsuke-trace-progress`

Apply only to a trace-collecting mode. Verify the configured source is alive and bound to the exact associated node. For `journald`, verify the exact follower process and unit selection and confirm eligible machine-format namespaces are present in bounded node logs. For `pipe`, verify the process topology and passthrough path without consuming or replaying the stream.

Require accepted trace submissions only after the effective upload window has elapsed and eligible lines have accumulated. Before then, report `unknown` with the reason; never mark an early absence as failure. Metrics-only mode is also `unknown` for this check, with its functional limitation recorded as evidence.

### `metsuke-spool-state`

Inspect only the registered spool path's canonical file metadata and size trend across observations. Require one component per spool, a regular non-symlink target, expected ownership and restrictive access, available filesystem headroom, and no client-reported write, busy, corruption, cap-drop, or acknowledgement errors. Do not open the database in a mode that may create journals, checkpoints, locks, or other writes, and do not extract payloads.

A stable or draining spool with accepted submissions is `healthy`; bounded growth during documented transient retry may be `degraded`; persistent growth, cap drops, corruption, or write failure is `failed`; and a single observation without sufficient log evidence is `unknown`.

### `metsuke-release-status`

Resolve the running binary and version from exact process and installed provenance. Query the official Metsuke releases source and select the current supported non-draft `client-v*` release according to `install-metsuke`; separately check the version supported by the deployed service documentation. Do not use an unrelated release family or assume newest means compatible.

Classify verified equality and compatibility as `current`, a newer compatible client as `update-available`, conflicting service and release authority as `conflict`, unreachable authority as `source-unreachable`, and missing provenance or compatibility as `unknown`.

### `metsuke-node-isolation`

Compare the associated node and other registered shared-host workloads with their baselines. Require stable runtime identities, continued node progress, expected sockets and ports, and no unexpected resource, group, supervisor, or process-topology drift attributable to Metsuke. In `pipe`, use the registered post-integration topology rather than the normal direct-`MainPID` rule.

Classify unaffected progressing workloads as `healthy`, material degradation as `failed`, a bounded resource concern without lost progress as `degraded`, and missing baseline or ambiguous attribution as `unknown`.

## Overall outcome

Do not collapse independent checks into a false green. Use the task policy to aggregate, with any `failed` operational check producing a failed outcome, `unknown` remaining visible, and a metrics-only trace limitation remaining explicit. An available release is not an operational failure by itself. Write only schema-valid sanitized evidence under `.musashi/task-runs/`; never write observed secrets or raw logs into the repository.
