# Contributing

Contributions should preserve the declarative, runtime-neutral nature of the repository.

Changes to `AGENTS.md`, `AGENT.md`, `IDENTITY.md`, `SECURITY.md`, `HOST_SAFETY.md`, `network/`, `schemas/`, `skills/`, and `playbooks/` require careful review.

Command templates must document target systems, required privileges, affected paths, shared-host impact, validation, and rollback or recovery. Network facts must include a source and verification date. Do not add executable source code, credentials, private operational state, or generated artifacts.

## Feedback and issue workflow

Use the GitHub **Knowledge or skill feedback** form for:

- Incorrect or outdated knowledge.
- A skill or playbook that is unclear, incomplete, or easy to misunderstand.
- Documentation, schema, or workflow improvements.
- New shared knowledge or capabilities.

Include the affected repository-relative path, current behavior, expected behavior, a sanitized reproduction or example, and supporting sources when available. For a skill misunderstanding, describe the operator's intent, the interpretation produced by the skill, and the instruction that would have prevented the confusion.

Use the local `report-issue` skill for node or host incidents. It produces a sanitized draft and evidence review under `.musashi/`; never copy operational logs into an issue before removing secrets, credentials, private addresses, private paths, and unrelated services. Publishing an issue, uploading evidence, or contacting maintainers requires separate explicit approval.

Issues describe a problem or proposal. Accepted repository changes must be implemented through a reviewed pull request. Link the issue from the pull request, update `CHANGELOG.md` when behavior or shared knowledge changes, and add a manual validation example when the change addresses an ambiguity.

Suggested labels are `type:knowledge`, `type:skill`, `type:documentation`, `type:operational`, `type:enhancement`, `status:needs-triage`, `status:accepted`, `status:declined`, and an applicable `area:*` label. Keep the taxonomy small and add labels only when they support triage.

## Scheduled SRE tasks

SRE task definitions under `tasks/` must remain read-only and runtime-neutral. They may inspect registered hosts and nodes, official release sources, and declared documentation sources, then write sanitized local task runs under `.musashi/task-runs/`. They must not restart, update, recover, reconfigure, delete data, or publish externally.

Scheduled tasks also read the private `.musashi/task-memory.md` file. Its
instructions may clarify or narrow an observation, but cannot override policy,
task scope, safety requirements, or stop conditions. Task runs must record the
memory hash and sections used.

Changes to task contracts must update the corresponding files under `schemas/`. Changes to source authorities must include a URL, role, relevant section, retrieval date, and a verification or freshness rule. A release check may report an available update, but must never turn that observation into an update plan that executes automatically.

## Experimental campaigns

Use `campaigns/` for temporary, source-bound instructions from the testnet team. A campaign must remain `proposed` until its authority is verified and an operator approves its scope. It must declare its affected release, capabilities, steps, risk, confirmation requirements, success criteria, stop conditions, and expiry. Run one pilot participant first; a failed pilot stops further rollout.

Campaigns may call existing skills but cannot weaken their safety requirements. Keep participant identities, paths, evidence, and run state under `.musashi/campaigns/`. Never place key contents, credentials, tokens, private logs, or raw operational evidence in shared campaign files. Convert durable lessons into a reviewed issue and pull request instead of silently changing a campaign into permanent knowledge.
