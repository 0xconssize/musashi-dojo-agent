# Collect diagnostics

Create a bounded, sanitized evidence set for one node.

## Collection set

- Repository commit, current network declaration, selected release, and installed artifact provenance.
- Node and host IDs, role, installation method, runtime identity, and execution mode.
- Timestamped host capacity and clock observations.
- Process or service state, configuration and topology hashes, socket or endpoint ownership.
- At least two time-separated tip or sync observations when available.
- Peer evidence and bounded logs around the reported event.
- Shared-host impact observations and checks already attempted.

## Privacy and bounds

- Collect only the time window and log lines needed to reproduce or explain the symptom.
- Remove credentials, keys, tokens, private key paths, unnecessary usernames, private addresses, unrelated services, and unrelated environment data.
- Do not copy complete configuration or credential directories.
- Store raw private evidence only under `.musashi/`; store sanitized excerpts in the diagnostic report.
- Mark operator-supplied, runtime-observed, and inferred statements distinctly.

## Output

Validate the result against `schemas/diagnostic-report.schema.json`. Include checks, findings, unknowns, recommendations, and a concise summary. `report-issue` may turn the report into a local draft, but no evidence leaves the machine without an explicit publication instruction.
