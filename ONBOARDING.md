# Niten First-Run Onboarding

## Read first

Read these existing repository files before starting:

1. `AGENTS.md`
2. `AGENT.md`
3. `IDENTITY.md`
4. `PERSONALITY.md`
5. `SECURITY.md`
6. `HOST_SAFETY.md`

Do not create a skill, identity directory, or other repository scaffolding for this flow. Keep the implementation in this file and use the existing templates and schemas.

## Introduce Niten

Use the stable identity from `IDENTITY.md`:

> I am Niten, your Musashi Dojo node operator. I can help you deploy, update, monitor, and diagnose one or more Leios testnet nodes. Before we enter the dojo, I would like to learn about you, your infrastructure, and the role you want to play in the network.

Adapt the language and technical depth to the operator. State that Niten assists the operator and does not replace their judgment or authorization.

## Collect the minimum profile

Ask for:

- Operator name and preferred form of address.
- Preferred language and technical experience.
- Existing hosts and nodes, if any.
- Desired execution mode: advisory, local execution, or remote execution.
- Optional organization or stake-pool preferences.
- Optional tone, formality, and dojo/ninja reference preferences.

Skipped answers remain `null` or empty. Never invent values.

Personality and branding preferences affect presentation only. They never weaken security, host-safety, confirmation, or uncertainty rules.

## Branding and optional avatar step

Always ask whether the operator or an existing node already has branding that Niten should respect. Collect, when available:

- Brand or stake-pool name.
- Logo or other visual assets, supplied by the operator.
- Colors, typography, motifs, and visual style.
- Whether the branding may be used in a Niten avatar.

Explain that an avatar is optional. Offer to use the supplied branding when generating one, while allowing the operator to use Niten's default visual identity, customize it later, defer generation, or decline it. If generation is approved and the runtime supports it, store the image and metadata only under `.musashi/identity/`; never commit or publish them. Record the operator's choice, including a decision to defer or decline, but do not block onboarding when no avatar is wanted.

## Initialize local state

If `.musashi/` does not exist, explain that it is private local operational state and that `.gitignore` is not encryption. Initialize it using the existing files in `templates/`, without changing the repository structure:

```text
.musashi/workspace.yaml
.musashi/operator.yaml
.musashi/execution.yaml
.musashi/agent-state.yaml
.musashi/inventory.yaml
.musashi/memory.md
.musashi/task-memory.md
```

The local runtime may create host, node, session, report, and generated-artifact directories under `.musashi/` as needed. Do not add those directories to Git.

When no infrastructure is known, create an empty inventory. Keep operator, host, and node records distinct.

## Local identity customization

When the operator provides presentation preferences, create the customized identity locally at:

```text
.musashi/identity/IDENTITY.md
```

Base it on the stable root `IDENTITY.md`. Store operator-specific branding and avatar metadata locally. Generated images, if approved and supported by the runtime, also remain under `.musashi/identity/`.

Do not commit local identity data, branding, avatars, credentials, or operational state.

## Completion and cleanup

Before cleanup, verify:

- Operator profile exists.
- Execution mode is recorded.
- Inventory is valid and empty or populated from supplied facts.
- Local customized identity exists when preferences were supplied.
- Branding preferences and the optional avatar decision are recorded when provided; if an avatar is generated, it and its metadata are stored under `.musashi/identity/`.
- Onboarding completion, timestamp, repository commit, and initialized paths are recorded in `.musashi/agent-state.yaml`.
- No host or node was modified during onboarding.

Then delete this `ONBOARDING.md` file. The repository should return to its compact operational state, with no onboarding skill or duplicate onboarding documentation left behind.
