# Changelog

## Unreleased

### Changed

- Stake-pool registration now treats a respin as a new network incarnation and requires current-chain verification before handing off to producer setup.

- Nix node diagnostics now rediscover and validate `cardano-cli` and the exact node socket from the running process, independently of the SSH session `PATH`.

### Added

- A separate operational-certificate workflow that recalculates the KES period from the current tip, preserves prior certificates, and advances opcert.counter monotonically.
- A known issue documenting stale operational certificates after a Musashi respin, plus provenance and BLS gates for block-producer installation.

- Private operator memory for scheduled-task instructions and clarifications, with task-run provenance.
- Phase 1 repository foundation.
- Niten identity, agent instructions, personality, memory policy, and safety policies.
- Initial templates and JSON Schema contracts.
- Phase 2 reduced to one temporary `ONBOARDING.md`; it is deleted after successful onboarding and does not introduce an onboarding skill or new repository folders.
- Phase 3 multi-host and multi-node registration with compact `add-host` and `add-node` skills, bidirectional inventory rules, explicit active context, stricter contracts, and source-freshness metadata.
- Phase 4 current Musashi network declarations covering the latest official release, live configuration snapshot, bootstrap data, requirements, release history, known issues, and source precedence.
- Phase 5 execution modes, verified local and remote host access, structured plans and command results, generated-artifact policy, and compact `connect-host` and `execute-node-plan` skills.
- Phase 6 initial operations: host assessment; relay installation and Musashi configuration; node start, stop, restart, diagnosis, update, recovery, and local issue drafting; six supporting playbooks; diagnostic rules; and strengthened operation and diagnostic report contracts.
- GitHub issue intake for sanitized operational problems and collaborative feedback on knowledge, skills, playbooks, and documentation, with an issue-to-reviewed-PR workflow.
- Read-only SRE observation package with scheduled task definitions for node and host health, configuration drift, release freshness, documentation freshness, and knowledge freshness, plus task, source, and release observation schemas.
- Experimental campaign model with authority and expiry metadata, pilot gates, participant run tracking, campaign schemas, and a non-active BLS key-enrollment example.
