---
name: start-metsuke
description: "Start one configured standalone Metsuke client and validate process health and its first signed submission without changing the associated node."
---

# Start Metsuke

Start only one installed and configured standalone Metsuke auxiliary component. This skill does not install or configure Metsuke, alter or restart the node, repair failures, update software, or monitor it continuously.

## Preconditions and scope

1. Read `AGENTS.md`, `SECURITY.md`, `HOST_SAFETY.md`, this skill's `metadata.yaml`, the selected node and component records, `network/current.yaml`, and `network/known-issues.yaml`.
2. Require one explicit registered block-producer node ID and host ID, current host assessment, verified access, exact standalone Metsuke runtime identity, configuration provenance, registered Leios-key role, selected integration mode, and validation criteria. Scope is `single-node`.
3. Accept only the standalone `metrics-only` or `journald` integration modes prepared by `configure-metsuke`. A `pipe` integration starts with the node and must be activated through `start-node`; containers, shells, and other supervisors are outside this MVP.
4. Revalidate the current service documentation and selected client compatibility before planning. Resolve all other nodes and relevant services on the host and use `connect-host` when required by workspace policy.

Starting Metsuke creates outbound signed submissions and changes host state. Verify the exact service, paths, privileges, destination, data classes, timing, rollback, node impact, and shared-host health. Start signed transmission only when the requested outcome includes it; reconcile any accepted submission before retrying.

## Preflight

Inspect without changing state:

- Verify the installed binary's canonical path, release provenance, digest, version, architecture, owner, and executable mode.
- Verify the exact configuration, effective unit and drop-ins, credential role and metadata, state directory, spool path, ownership model, service disabled/inactive state, and absence of another Metsuke process or listener. Never read or print secret key material.
- Parse and validate the effective configuration. Reject placeholders, source-mode disagreement, non-loopback metrics, unapproved submission origin, duplicate spool use, or values that differ from the recorded configured state.
- Require current evidence that the selected pool is eligible to submit to the configured service. Delegate the eligibility rules and mutable registration values to their authoritative source; do not reproduce their format here.
- Verify the node is already running under its registered identity, owns the configured metrics endpoint, returns bounded Prometheus data, and remains healthy. For `journald`, verify the exact unit emits the expected machine-format trace namespaces and that the planned Metsuke identity can follow them.
- From the target host, resolve the configured submission hostname and verify bounded TLS/HTTPS reachability to the documented service origin before enabling anything. Treat DNS, TCP, TLS, and HTTP failures as distinct preflight evidence. Retry only within a small declared read-only budget; an endpoint failure stops before host modification.
- Capture baseline node progress, exact process identities, service states, ports, spool metadata, and shared-host workload health.

If the service is already active, do not restart it. Validate it using the checks below and report an observed no-op or a conflict.

## Workflow

1. Build a schema-valid `execute-node-plan` plan that names only the exact standalone Metsuke service and the enable/start operations supported by its registered system manager. Include bounded observations for startup, the first scrape submission, process stability, node continuity, and shared-host isolation. Use the service invocation ID or an equivalent exact cursor so validation cannot count submissions from an earlier attempt.
2. Hand the validated operation to `execute-node-plan` for target revalidation, short-step execution, and audit. Do not use broad process matching or invent a runtime identity.
3. Enable and start only the selected Metsuke service. Do not daemon-reload unless the reviewed plan explicitly requires it because the already configured unit has not been loaded; any changed unit or configuration invalidates this startup plan and must return to `configure-metsuke`.
4. Keep activation and observation as short, explicit phases. The activation phase may enable/start and wait only for service stability plus the first accepted submission. Run process inspection, node progress, and shared-host continuity as separate read-only observations whose individual duration fits the execution transport. Do not place a long polling loop behind an `EXIT` trap that can stop a healthy service merely because the caller timed out.
5. Treat the first accepted signed submission as an irreversible commit point. Record it immediately. A later rollback can stop future submissions but cannot undo the accepted one, and any retry requires first reconciling the exact service state and logs so it does not create an unnecessary additional submission.
6. Roll back a newly activated service only for an activation-critical failure or observed Metsuke-caused node/shared-host degradation, after checking impact. If submission was accepted and a later auxiliary check fails because of observer permissions, quoting, transport timeout, or inconclusive node progress, do not automatically stop or restart Metsuke. Reconcile state, report partial validation, and diagnose with read-only checks. Preserve configuration, credential, spool, and node state; do not loop restarts or improvise recovery.

## Validation

Independently verify:

- The exact service is enabled as planned and remains active under its registered supervisor; its main PID, `/proc` executable, command line, binary digest, user, groups, cgroup, and invocation ID agree with the configured runtime. On hosts restricting `/proc`, perform the complete read, redirection, and parsing operation under the declared privilege; partial `sudo` around only one command is insufficient.
- The node-owned loopback metrics endpoint remains reachable and the first metrics scrape produces an accepted signed submission within the bounded documented startup window.
- No rejection, signing error, repeated retry, spool write failure, crash loop, unsupported-version warning, or unexpected destination appears in bounded sanitized logs.
- In `journald` mode, the journal follower remains alive and the configured source matches the selected node unit. Trace-submission status is `conditional` until the effective upload window has elapsed and eligible lines have accumulated; absence before then is not failure.
- Spool metadata is consistent with successful acknowledgement or a bounded queued state. Do not inspect or mutate spool payloads.
- The associated node retains its process and runtime identity and continues making progress; all other registered nodes and shared-host workloads remain unaffected.

Write a sanitized operation report, recording observed auxiliary-component state through the existing report and memory contracts. Record the runtime identity, start time, process evidence, effective mode, binary version and digest, submission result, spool metadata, trace validation state, node continuity, and any conditional result. Do not record signing-key content or raw telemetry.

## Failure and success

Stop on target drift, unsupported mode, stale or conflicting configuration, an unverified credential role, non-loopback metrics, unexpected service state, occupied or shared paths, submission to an unapproved destination, rejected first submission, repeated failure, policy rejection, node degradation, or shared-host impact.

Success means the exact standalone Metsuke service remains enabled and running under its verified runtime identity, its first metrics submission is accepted, the node and shared workloads remain healthy, and trace status is evidenced or explicitly conditional according to the effective configured window. Process activity alone is not success.

## Official sources

- Metsuke quickstart: https://metsuke-leios.play.dev.cardano.org/
- Metsuke details: https://metsuke-leios.play.dev.cardano.org/details
- Official Metsuke releases: https://github.com/input-output-hk/metsuke/releases
