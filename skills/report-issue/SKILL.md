---
name: report-issue
description: "Prepare a sanitized, reproducible Musashi issue report from diagnostic evidence without publishing it automatically."
---

# Report issue

Create a local issue draft. Sending it to GitHub, Discord, or another external service requires a separate explicit operator instruction.

## Inputs and scope

Require a diagnostic or operation report, exact affected node scope, reproduction summary, observed and expected behavior, and consent boundaries for evidence. Risk is local-state-only. Outputs are a report and issue draft under `.musashi/`.

## Workflow

1. Read `SECURITY.md`, the source report, current network and release declarations, and `templates/github-issue.md`.
2. Verify report provenance and distinguish observations from assumptions.
3. Minimize and sanitize evidence: remove credentials, keys, tokens, usernames when unnecessary, private addresses, unrelated services, absolute private paths, and excessive logs.
4. Include environment, release provenance, installation method, exact bounded steps, timestamps, expected and observed behavior, sanitized excerpts, and checks already attempted.
5. Save the structured report and Markdown draft under `.musashi/reports/`. Never write operational evidence into Git.
6. Show the final draft and the evidence that would leave the machine. Do not publish, upload attachments, or contact maintainers automatically.

## Failure and success

Stop on unknown provenance, unsanitized evidence, or unclear publication scope. Success means a concise reproducible draft exists locally, contains no known secret or unrelated private data, and has not been transmitted.

## Memory and playbook

Record only the local report path and pending operator decision. Use `playbooks/collect-diagnostics.md` when evidence is incomplete.
