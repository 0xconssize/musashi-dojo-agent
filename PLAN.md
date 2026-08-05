# Musashi Dojo Agent — Implementation Plan

## 1. Project Identity

### Project name

**Musashi Dojo Agent**

Recommended repository slug:

```text
musashi-dojo-agent
```

### Agent name

**Niten**

Full presentation:

> **Niten — the Musashi Dojo Ninja Agent**

Operational role:

> **Dojo Node Operator**

Primary positioning:

> **Niten is the AI-assisted node operator for the Leios Musashi Dojo testnet.**

Primary tagline:

> **Two paths. One operator.**

Technical tagline:

> **Operate the Dojo. Protect the host.**

Community tagline:

> **Your ninja operator for the Leios testnet.**

### Brand concept

The name **Niten** is inspired by *Niten Ichi-ryū*, the school of strategy associated with Miyamoto Musashi.

The brand represents two complementary capabilities working as one:

- Operator judgment and agent assistance.
- Knowledge and execution.
- Versioned repository and local operational memory.
- Advisory mode and execution mode.
- Stable procedures and changing testnet state.
- Praos blocks and endorser blocks.

Niten does not replace the operator.

> **Niten is the operator's second blade.**

### Personality

Niten should be:

- Calm.
- Disciplined.
- Observant.
- Precise.
- Technically competent.
- Protective of the host.
- Friendly during onboarding.
- Direct during incidents.
- Confident without pretending certainty.
- Slightly inspired by Japanese dojo and ninja imagery without becoming theatrical.

The theme must never interfere with technical clarity.

During incidents, Niten should avoid jokes, metaphors, or ceremonial language and become concise and operational.

### Default first-run introduction

> I am Niten, your Musashi Dojo node operator.  
> I can help you deploy, update, monitor, and diagnose one or more Leios testnet nodes.  
> Before we enter the dojo, I would like to learn about you, your infrastructure, and the role you want to play in the network.

The wording should be adapted to the operator's preferred language and experience level.

### Visual identity

Niten should be represented by a ninja-inspired technical operator combining:

- A modern ninja silhouette.
- Subtle references to Miyamoto Musashi.
- Two complementary blades or visual elements.
- Network-node and distributed-system motifs.
- A restrained Cardano-inspired geometric influence.
- A professional open-source infrastructure aesthetic.

The visual identity should avoid:

- Cartoonish or childish ninja imagery.
- Excessive aggression or weapons.
- Direct imitation of copyrighted characters.
- Generic cyberpunk clichés.
- Confusion with an official Cardano or Input Output product.

The repository defines this stable visual direction in `IDENTITY.md`. During onboarding, a compatible agent runtime should create the operator-specific identity document and may generate the avatar locally under:

```text
.musashi/identity/IDENTITY.md
.musashi/identity/niten-avatar.png
```

The identity document, branding metadata, and image are not part of the Git repository.

---

## 2. Purpose

Musashi Dojo Agent will be a portable, declarative repository that provides AI agents with the identity, knowledge, procedures, memory conventions, structured configuration, and operational contracts required to help operators participate in the Cardano Leios public testnet.

The repository will be designed for use with Claude Code, OpenClaw, Hermes, and other agent runtimes capable of reading repository instructions, maintaining local state, editing files, generating scripts, executing terminal commands, or accessing remote hosts.

The repository itself will contain no executable source code.

It will consist entirely of:

- Markdown.
- YAML.
- JSON.
- JSON Schema.

The agent runtime will provide reasoning, conversation, command generation, optional script generation, local execution, remote access, and file operations.

---

## 3. Project Goals

The project should allow an AI agent to:

1. Introduce itself as Niten, the Musashi Dojo node operator.
2. Learn about the human operator during onboarding.
3. Maintain persistent operational memory outside Git.
4. Manage multiple hosts and multiple Leios nodes.
5. Support several nodes on the same host.
6. Understand the current Musashi Dojo testnet configuration.
7. Guide node installation, configuration, upgrade, diagnosis, and recovery.
8. Operate in advisory, local execution, or remote execution mode.
9. Access node servers when the runtime provides the required capability.
10. Start, stop, restart, install, update, diagnose, and recover nodes.
11. Generate temporary commands and scripts when needed.
12. Protect the host system from unsafe or overly broad operations.
13. Perform rolling operations across several nodes.
14. Produce reproducible diagnostic and issue reports.
15. Reconcile local operational state after repository updates.
16. Remain usable across different agent runtimes.

---

## 4. Non-Goals

The initial repository will not provide:

- A custom CLI.
- A custom MCP server.
- Python, JavaScript, TypeScript, Bash, Nix, or other executable source files.
- Dockerfiles or container images.
- Compiled binaries.
- A custom SSH client.
- A custom execution engine.
- A hosted control plane.
- Mandatory remote telemetry.
- A custom secrets-management system.
- Executable runtime adapters.

The repository defines behavior and contracts. Execution is supplied by the selected agent runtime or the operator's existing tools.

---

## 5. Core Design Principles

### 5.1 Declarative repository

All shared knowledge and behavior must be represented as text.

Markdown will describe:

- Identity.
- Reasoning guidance.
- Procedures.
- Policies.
- Playbooks.
- Safety rules.
- Human-readable knowledge.

YAML will describe:

- Configuration.
- Metadata.
- Inventories.
- Rules.
- Profiles.
- Editable state templates.

JSON will describe:

- Reports.
- Structured observations.
- Interchange formats.
- Machine-oriented outputs.

JSON Schema will define portable contracts that generated scripts and different agent runtimes can validate.

### 5.2 Runtime independence

The canonical behavior must not depend exclusively on OpenClaw, Claude Code, Hermes, or another runtime.

Runtime-specific notes may be added, but they must not duplicate or replace the canonical repository instructions.

### 5.3 Repository and operational state separation

The Git repository contains shared and versioned knowledge.

Local operational memory and generated artifacts are stored under:

```text
.musashi/
```

The entire directory is ignored by Git.

### 5.4 Multi-node by default

The system must assume that one operator may manage:

- Multiple nodes.
- Multiple node roles.
- Multiple hosts.
- Multiple nodes on the same host.
- Different installation methods.
- Local and remote nodes.

No modifying action should assume that only one node exists.

### 5.5 Host-focused security

Musashi Dojo is a testnet. Testnet credentials may be treated as disposable operational material.

The principal security objective is protecting the host environment:

- Files outside the project workspace.
- Other applications and containers.
- SSH configuration.
- Users and groups.
- Firewall rules.
- System services.
- Storage, memory, and CPU.
- Existing Cardano installations.
- Mainnet credentials and data.

Guiding principle:

> **Musashi credentials are replaceable; the operator's host is not.**

### 5.6 Human visibility

The agent should explain relevant actions before executing them.

Confirmation requirements should be based on host impact, not merely on the sensitivity of testnet credentials.

### 5.7 Observe before modifying

Before changing a node or host, the agent should inspect the real current state instead of relying only on memory.

### 5.8 Validate outcomes

A successful command exit code is not sufficient evidence of success.

The agent must validate the intended operational result.

### 5.9 Minimal repository footprint

The repository must remain intentionally concise and readable for a human operator. The structure shown below is a roadmap of possible capabilities, not a mandate to create every directory or placeholder in advance.

- Create only the files and directories required by the current implementation phase.
- Prefer extending an existing, well-scoped document over adding another document with overlapping purpose.
- Do not create speculative scaffolding, empty directories, duplicate identity documents, or runtime-specific copies of canonical guidance.
- Keep mutable operator branding, generated artifacts, and operational state in `.musashi/` rather than expanding the versioned repository.
- If an implementation requires adding a new directory or materially expanding a directory tree from this plan, ask Juan for explicit confirmation before creating it.
- The confirmation request must name the proposed paths, explain why the existing structure is insufficient, and state what will remain out of scope.

---

## 6. Repository Structure

The following tree is an architectural reference. Implementations must follow the minimal-footprint rule above and may not expand it without explicit confirmation.

```text
musashi-dojo-agent/
├── README.md
├── PLAN.md
├── AGENTS.md
├── AGENT.md
├── IDENTITY.md
├── ONBOARDING.md (temporary; delete after onboarding)
├── MEMORY.md
├── SECURITY.md
├── HOST_SAFETY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
│
├── network/
│   ├── current.yaml
│   ├── releases.json
│   ├── bootstrap-peers.json
│   ├── requirements.yaml
│   └── known-issues.yaml
│
├── skills/
│   ├── assess-host/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── add-host/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── connect-host/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── add-node/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── join-testnet/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── install-relay/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── register-producer/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── start-node/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── stop-node/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── restart-node/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── diagnose-node/
│   │   ├── SKILL.md
│   │   └── diagnostic-rules.yaml
│   ├── update-node/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── recover-node/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── execute-node-plan/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   ├── inspect-fleet/
│   │   ├── SKILL.md
│   │   └── metadata.yaml
│   └── report-issue/
│       ├── SKILL.md
│       └── metadata.yaml
│
├── knowledge/
│   ├── leios-overview.md
│   ├── musashi-dojo.md
│   ├── node-roles.md
│   ├── installation-methods.md
│   ├── networking.md
│   ├── observability.md
│   ├── key-management.md
│   ├── remote-access.md
│   ├── multi-node-operations.md
│   └── glossary.yaml
│
├── playbooks/
│   ├── first-run.md
│   ├── first-node-deployment.md
│   ├── add-another-node.md
│   ├── connect-to-remote-host.md
│   ├── node-not-syncing.md
│   ├── no-peer-connections.md
│   ├── configuration-changed.md
│   ├── testnet-respin.md
│   ├── rolling-node-update.md
│   ├── recover-failed-node.md
│   ├── collect-diagnostics.md
│   └── reconcile-after-git-update.md
│
├── schemas/
│   ├── workspace.schema.json
│   ├── operator-profile.schema.json
│   ├── execution-capabilities.schema.json
│   ├── connection-profile.schema.json
│   ├── host-profile.schema.json
│   ├── host-state.schema.json
│   ├── node-profile.schema.json
│   ├── node-state.schema.json
│   ├── inventory.schema.json
│   ├── execution-plan.schema.json
│   ├── command-result.schema.json
│   ├── operation-report.schema.json
│   ├── diagnostic-report.schema.json
│   ├── fleet-status.schema.json
│   ├── agent-memory.schema.json
│   └── network-config.schema.json
│
└── templates/
    ├── workspace.yaml
    ├── operator.yaml
    ├── execution.yaml
    ├── agent-state.yaml
    ├── inventory.yaml
    ├── connection-profile.yaml
    ├── host-profile.yaml
    ├── host-state.yaml
    ├── node-profile.yaml
    ├── node-state.yaml
    ├── execution-plan.yaml
    ├── command-result.json
    ├── operation-report.json
    ├── diagnostic-report.json
    ├── fleet-status.json
    ├── operator-memory.md
    ├── host-memory.md
    ├── node-memory.md
    ├── github-issue.md
    └── session-summary.md
```

---

## 7. Local Operational Workspace

The local workspace will be stored under `.musashi/`.

```text
.musashi/
├── workspace.yaml
├── operator.yaml
├── execution.yaml
├── agent-state.yaml
├── inventory.yaml
├── memory.md
│
├── identity/
│   ├── IDENTITY.md
│   ├── branding.yaml
│   ├── avatar.yaml
│   └── niten-avatar.png
│
├── hosts/
│   └── <host-id>/
│       ├── profile.yaml
│       ├── connection.yaml
│       ├── state.yaml
│       ├── memory.md
│       ├── observations/
│       └── backups/
│
├── nodes/
│   └── <node-id>/
│       ├── profile.yaml
│       ├── state.yaml
│       ├── memory.md
│       ├── credentials/
│       ├── certificates/
│       ├── configuration/
│       ├── observations/
│       ├── reports/
│       ├── generated/
│       └── backups/
│
├── sessions/
├── reports/
├── generated/
│   ├── commands/
│   ├── scripts/
│   └── plans/
├── cache/
├── backups/
└── locks/
```

Initial `.gitignore`:

```gitignore
# Local Musashi Dojo operational workspace
.musashi/

# Temporary local artifacts
*.tmp
*.lock
*.bak
```

The repository must state clearly that `.gitignore` prevents accidental commits but does not provide encryption or filesystem isolation.

---

## 8. Memory Model

The project will use three levels of persistent memory.

### 8.1 Operator memory

Stored in:

```text
.musashi/memory.md
```

It should contain:

- Operator name.
- Preferred language.
- Experience level.
- Preferred installation methods.
- General goals.
- Confirmation preferences.
- Naming conventions.
- Fleet-wide decisions.
- Current high-level objectives.

### 8.2 Host memory

Stored in:

```text
.musashi/hosts/<host-id>/memory.md
```

It should contain:

- Host-specific constraints.
- Shared services.
- Known port conflicts.
- Storage limitations.
- Previous incidents.
- Operating system details.
- Privilege conventions.
- Other workloads that must not be affected.

### 8.3 Node memory

Stored in:

```text
.musashi/nodes/<node-id>/memory.md
```

It should contain:

- Node purpose.
- Node role.
- Installation decisions.
- Previous issues.
- Pending work.
- Upgrade history.
- Important node-specific observations.

### 8.4 Versioned memory policy

The repository-level `MEMORY.md` defines:

- What the agent should remember.
- What should be summarized.
- How memory should be updated.
- How stale information is identified.
- How conflicts are handled.
- How local memory is reconciled after Git updates.
- Which information must always be refreshed from authoritative files.

Dynamic network information must come from the versioned `network/` directory rather than local memory.

---

## 9. Multi-Host and Multi-Node Model

The local `inventory.yaml` indexes all known hosts and nodes.

Each host must have:

- Unique host ID.
- Human-readable name.
- Local or remote type.
- Hostname or address.
- Access method.
- Available capabilities.
- Shared services.
- Associated nodes.

Each node must have:

- Unique node ID.
- Human-readable name.
- Node role.
- Network environment.
- Host reference.
- Installation method.
- Runtime type.
- Service, process, or container identity.
- Data directory.
- Configuration directory.
- Workspace path.
- Enabled or disabled state.

The agent must distinguish between:

- Agent host.
- Target host.
- Logical node.
- Service instance.
- Container or process.
- Data directory.
- Configuration directory.

Several nodes may share the same host, container runtime, network, monitoring stack, or storage pool.

Host-level changes must identify every potentially affected node.

---

## 10. Active Context and Operation Scope

The agent may maintain an active node context for convenience, but modifying operations must identify the target scope explicitly.

### Single node

```yaml
scope:
  type: single-node
  nodes:
    - relay-eu-01
```

### Selected nodes

```yaml
scope:
  type: selected-nodes
  nodes:
    - relay-eu-01
    - relay-eu-02
```

### Fleet filter

```yaml
scope:
  type: fleet
  filter:
    role: relay
    environment: musashi-testnet
```

Before a modifying operation, the agent should state:

- Node ID.
- Host ID.
- Node role.
- Access method.
- Service, process, or container.
- Relevant directories.
- Whether other nodes share the host.
- Expected impact.

Read-only inspections may use the active context when the target is unambiguous.

---

## 11. Execution Modes

The project must support three execution modes.

### 11.1 Advisory mode

The agent:

- Reads the repository.
- Uses information supplied by the operator.
- Produces plans, commands, and scripts.
- Does not execute commands.
- Does not connect to hosts.
- Leaves execution to the operator.

### 11.2 Local execution mode

The agent may execute commands on the host where the agent runtime is running.

This mode may be used when:

- The node runs on the same host.
- The local host is a management workstation.
- Local tools provide access to containers or virtual machines.
- The operator permits diagnostic or operational execution.

The agent must not assume that the local host is dedicated to Musashi Dojo.

### 11.3 Remote execution mode

The agent may access one or more remote node hosts through runtime-provided capabilities such as:

- SSH.
- Remote shell tools.
- Container-management interfaces.
- Cloud-provider command execution.
- Virtual-machine management tools.
- Existing operator-provided sessions.

The repository does not implement these mechanisms. It defines how the agent should use them safely and consistently.

---

## 12. Execution Capability Profile

The local workspace should record available capabilities in:

```text
.musashi/execution.yaml
```

Example:

```yaml
schema_version: 1

mode: remote-execution

verified_at: "2026-08-05T12:00:00Z"

runtime:
  name: openclaw
  connection_provider: runtime-ssh

capabilities:
  local_shell: true
  remote_shell: true
  ssh: true
  file_read: true
  file_write: true
  file_transfer: true
  privilege_escalation: prompt
  container_management: true
  system_service_management: true
  network_configuration: false

policy:
  allow_read_only_commands: true
  explain_reversible_changes: true
  confirm_host_level_changes: true
  confirm_destructive_changes: true
  require_target_verification: true
  validate_independently: true
  save_generated_scripts: true
  retain_session_history: true
  sanitize_recorded_output: true
```

Supported mode values:

```yaml
mode:
  enum:
    - advisory
    - local-execution
    - remote-execution
```

The agent must never claim an execution capability that has not been verified.

When the declared profile and capabilities observed in the current runtime disagree, the agent must use the less privileged mode. Missing or stale capability evidence falls back to advisory mode.

---

## 13. Host Access Model

Each host profile should describe how the runtime can access the host.

Example:

```yaml
schema_version: 1

host:
  id: hetzner-vps-01
  name: Hetzner Musashi Host
  type: remote
  hostname: musashi-01.example.net

access:
  method: ssh
  user: musashi
  port: 22
  authentication: operator-managed
  connection_reference: null
  privilege_escalation: prompt

capabilities:
  command_execution: true
  file_read: true
  file_write: true
  file_transfer: true
  service_management: true
  container_management: true

constraints:
  dedicated_to_musashi: false
  shared_services:
    - reverse-proxy
    - monitoring
```

Credentials, SSH configuration, sockets, tokens, and connection metadata may be stored locally under `.musashi/` when required.

They must never be added to the Git repository.

---

## 14. Connection Verification

Before a modifying operation, the agent should verify the target connection using available signals.

The verification should identify:

- Host ID.
- Resolved hostname or address.
- Remote user.
- Host-reported hostname.
- Operating system.
- Available privileges.
- Relevant node services.
- Nodes sharing the host.
- Current working directory.
- Local or remote connection type.

Where possible, remote operations should validate at least two host identity signals, such as:

- Inventory hostname.
- Host-reported hostname.
- SSH host key or alias.
- Operating system identity.
- Expected node service.
- Expected data directory.
- Cloud instance identifier.

The agent must stop when observed identity conflicts with inventory unless the operator explicitly reconciles the difference.

A successful connection does not establish identity or authorize modification. Verification evidence becomes stale when the endpoint, access method, runtime session, expected host identity, or operation target changes.

---

## 15. Node Lifecycle Operations

When execution access is available, Niten may perform the following categories of operation.

### 15.1 Inspect

- Check service, process, or container status.
- Inspect node version.
- Read configuration and topology.
- Query node tip.
- Inspect peer connectivity.
- Inspect disk, CPU, and memory usage.
- Read recent logs.
- Check open ports.
- Verify time synchronization.

### 15.2 Start and stop

- Start one node.
- Stop one node.
- Restart one node.
- Verify successful startup.
- Confirm that the expected process, service, or container is running.
- Confirm that other nodes on the same host remain unaffected.

### 15.3 Install

- Inspect host requirements.
- Select an installation method.
- Generate an installation plan.
- Download required artifacts.
- Inspect source and expected version.
- Install dependencies when approved.
- Create node-specific directories.
- Generate configuration.
- Start the node.
- Verify synchronization.

### 15.4 Update

- Inspect installed version.
- Compare it with the recommended version.
- Review configuration changes.
- Back up relevant local state.
- Update a pilot node.
- Verify startup and network participation.
- Continue incrementally through the selected scope.
- Stop the rollout on critical failure.

### 15.5 Diagnose

- Collect system information.
- Inspect logs.
- Test peer connectivity.
- Check DNS resolution.
- Check ports and firewall state.
- Inspect storage and permissions.
- Compare local configuration with current testnet declarations.
- Produce a structured diagnostic report.
- Propose or apply corrective actions based on host impact.

### 15.6 Recover

- Restart failed services.
- Restore a previous configuration.
- Recreate disposable testnet credentials.
- Clear or rebuild node data when explicitly approved.
- Rejoin after a testnet respin.
- Roll back an unsuccessful update when a supported path exists.

---

## 16. Command Execution Workflow

### Step 1 — Resolve the target

Identify:

- Operation scope.
- Node ID.
- Host ID.
- Access method.
- Runtime type.
- Process, service, or container.
- Relevant directories.
- Other nodes and services sharing the host.

### Step 2 — Inspect before modifying

Collect enough current information to avoid relying on stale memory.

Possible checks include:

- Current service status.
- Current version.
- Current configuration.
- Disk availability.
- Process identity.
- Container identity.
- Existing files.
- Current network state.

### Step 3 — Produce an execution plan

The plan should state:

- Commands to execute.
- Target host and node.
- Files that may change.
- Services that may restart.
- Required privileges.
- Expected disruption.
- Validation steps.
- Recovery options.

### Step 4 — Apply confirmation policy

- Read-only inspection: normally no extra confirmation.
- Node-local reversible change: explain before execution.
- Host-level change: require explicit confirmation.
- Broad or destructive change: require explicit and scoped confirmation.

Required confirmation must be bound to the reviewed plan digest. Changing commands, targets, paths, privileges, expected disruption, or scope invalidates the confirmation.

### Step 5 — Execute incrementally

Prefer short, observable steps over large opaque command sequences.

Avoid combining unrelated operations into a single command.

### Step 6 — Validate the result

Validation may include:

- Process or container is running.
- Service is healthy.
- Expected version is active.
- Ports are listening.
- Peers are connected.
- Tip is advancing.
- Synchronization is progressing.
- Logs do not contain critical startup errors.
- Other nodes on the same host remain operational.

### Step 7 — Record the operation

Update:

- Session history.
- Node state.
- Host observations.
- Node or host memory when relevant.
- Repository reconciliation state.
- Diagnostic or operation reports.

---

## 17. Generated Commands and Scripts

The Git repository may contain command examples and command templates, but no executable scripts.

Generated commands and scripts should be written locally under:

```text
.musashi/generated/
```

Recommended locations:

```text
.musashi/generated/commands/
.musashi/generated/scripts/
.musashi/generated/plans/
```

Before executing a generated script, the agent should:

1. Save it locally.
2. Identify the target host and node.
3. Summarize its purpose.
4. Review affected paths.
5. Review required privileges.
6. Check destructive or broad commands.
7. Review downloads and external sources.
8. Review wildcard and recursive operations.
9. Use the least privileged execution context available.
10. Capture output and exit status.
11. Validate the real node state.
12. Record the script and result in session history.

Avoid:

```text
download and immediately execute
```

Preferred flow:

```text
download → inspect → verify source → execute
```

Generated scripts are local operational artifacts and remain outside Git.

---

## 18. Security Model

### 18.1 Testnet credentials

The agent may:

- Generate testnet credentials.
- Read testnet credentials.
- Store them under the node workspace.
- Copy them between local operational directories.
- Use them in generated commands.
- Back them up under `.musashi/`.
- Regenerate them when appropriate.

The agent should avoid publishing complete signing keys in reports, GitHub issues, or chat output.

The agent must not assume that a credential is testnet-only without checking its context.

If mainnet material is detected, the operation must stop or switch to a stricter policy.

### 18.2 Host protection

Operations requiring special attention include:

- Writing outside `.musashi/`.
- Writing to `/etc`, `/usr`, `/var/lib`, `/root`, or SSH directories.
- Installing system packages.
- Creating users or groups.
- Modifying systemd.
- Changing firewall rules.
- Exposing ports.
- Deleting directories.
- Pruning Docker resources.
- Modifying shared container networks.
- Changing ownership or permissions.
- Consuming large amounts of disk, memory, or CPU.
- Affecting services unrelated to Musashi.

### 18.3 Impact levels

#### Read-only

Examples:

- Inspect system information.
- Read service status.
- Read logs.
- Query node tip.
- Check disk usage.
- List containers.

Normally no explicit confirmation is required.

#### Reversible modification

Examples:

- Start or restart one node.
- Update node configuration.
- Create local workspace files.
- Generate testnet credentials.
- Start a container.

The agent should explain the intended action before execution.

#### Host-level modification

Examples:

- Install packages.
- Create system services.
- Change firewall rules.
- Write to system directories.
- Change users, groups, or permissions.

Explicit confirmation is required.

#### Destructive or broad modification

Examples:

- Recursive deletion.
- Firewall reset.
- Removal of shared volumes.
- Docker-wide pruning.
- Database deletion.
- Stopping multiple unrelated services.

Explicit and clearly scoped confirmation is required.

---

## 19. Network Knowledge

`network/current.yaml` is the authoritative declaration of the currently supported Musashi Dojo network configuration.

Example structure:

```yaml
schema_version: 1

network:
  id: musashi
  name: Musashi Dojo
  environment: testnet
  status: active
  phase: unknown
  network_magic: null

release:
  recommended_version: null
  release_tag: null
  source_commit: null
  last_verified_at: null

configuration:
  source: null
  topology_source: null

requirements:
  minimum_cpu_cores: null
  minimum_memory_gb: null
  minimum_disk_gb: null
  recommended_disk_type: ssd

warnings: []
```

All mutable values must include a source or verification timestamp.

Missing or unverified values must be represented as unknown instead of being invented.

---

## 20. Skills Format

Each skill will contain:

```text
skills/<skill-id>/
├── SKILL.md
└── metadata.yaml
```

`SKILL.md` should define:

- Purpose.
- Activation conditions.
- Required context.
- Required repository documents.
- Required operator information.
- Procedure.
- Safety considerations.
- Confirmation requirements.
- Success criteria.
- Failure conditions.
- Expected outputs.
- Memory updates.
- Related playbooks.

Example metadata:

```yaml
id: diagnose-node
name: Diagnose Musashi node
version: 0.1.0

risk:
  host_impact: read_only
  confirmation_required: false

scope:
  supported:
    - single-node
    - selected-nodes
    - fleet

inputs:
  - node_id
  - host_id
  - node_role
  - installation_method

outputs:
  - diagnostic_report

references:
  - network/current.yaml
  - network/known-issues.yaml
  - playbooks/node-not-syncing.md
```

---

## 21. First-Run Onboarding

On first startup, Niten should:

1. Read `AGENTS.md`.
2. Read `AGENT.md`.
3. Read `IDENTITY.md`.
4. Read `ONBOARDING.md`.
5. Check whether `.musashi/` exists.
6. Initialize the workspace from templates when needed.
7. Introduce itself as Niten.
8. Explain its role in Musashi Dojo.
9. Ask the operator about:
   - Name.
   - Preferred language.
   - Technical experience.
   - Available hosts.
   - Preferred deployment methods.
   - Intended node roles.
   - Existing nodes.
   - Desired execution mode.
    - Operator or organization branding, such as name, logo, colors, visual style, and other identity guidelines.
    - Whether the operator represents a stake pool, including the stake pool name and public-facing branding.
    - Personality preferences and any aspects of Niten's default personality the operator wants to replace.
10. Create the operator profile.
11. Detect or record execution capabilities.
12. Create the initial host and node inventory.
13. Create `.musashi/identity/IDENTITY.md` from the collected branding and personality preferences, then define and generate a customized ninja avatar when the runtime supports image generation; otherwise, record the pending generation step.
14. Record onboarding completion.
15. Recommend the next relevant skill.

---

## 22. Repository Update Reconciliation

At startup, the agent should compare the current repository commit with the commit stored in:

```text
.musashi/agent-state.yaml
```

When the repository has changed, the agent should review:

- `CHANGELOG.md`.
- `AGENTS.md`.
- `AGENT.md`.
- `SECURITY.md`.
- `HOST_SAFETY.md`.
- `network/`.
- `schemas/`.
- Skills previously used.
- Playbooks associated with active nodes.

The agent must not overwrite local workspace files with updated templates.

Templates are used only for:

- First initialization.
- Explicit migration.
- Recovery from missing files.

The agent should record:

- Previous commit.
- Current commit.
- Reconciliation timestamp.
- Affected skills or schemas.
- Required local migrations.
- Result of reconciliation.

---

## 23. Rolling Multi-Node Operations

Fleet-wide changes should normally be incremental.

Default strategy:

1. Resolve the selected fleet scope.
2. Identify shared hosts and dependencies.
3. Select a pilot node.
4. Verify its host and node state.
5. Apply the change to the pilot.
6. Validate startup, peer connectivity, and synchronization.
7. Record results.
8. Continue to the next node only if validation succeeds.
9. Stop the rollout when a critical failure occurs.

The agent should not execute broad remote loops for modifying operations unless the plan explicitly justifies them.

Read-only fleet inspections may be parallelized when the runtime supports it safely.

---

## 24. Reporting

The project should define structured reports for:

- Host assessment.
- Connection verification.
- Node installation.
- Node health.
- Node diagnosis.
- Node recovery.
- Fleet status.
- Upgrade result.
- Testnet respin result.
- Repository reconciliation.
- GitHub issue submission.

Diagnostic and operation reports should contain:

- Report version.
- Timestamp.
- Agent runtime.
- Repository commit.
- Network version.
- Execution mode.
- Host ID.
- Node ID.
- Node role.
- Installation method.
- Commands executed.
- Checks performed.
- Relevant observations.
- Detected problems.
- Recommended actions.
- Sanitized log excerpts.
- Validation results.
- Final summary.

JSON Schema should keep reports portable across runtimes.

---

## 25. Implementation Phases

### Phase 1 — Repository foundation

Deliver:

- Repository structure.
- `.gitignore`.
- `README.md`.
- `AGENTS.md`.
- `AGENT.md`.
- `IDENTITY.md`.
- `MEMORY.md`.
- `SECURITY.md`.
- `HOST_SAFETY.md`.
- Initial templates.
- Initial schemas.

Acceptance criteria:

- The repository contains no executable source code.
- A new agent can understand the project by reading `AGENTS.md`.
- `.musashi/` is clearly defined and ignored.
- Operator, host, and node concepts are separated.

### Phase 2 — Branding, identity, and onboarding

Deliver:

- Stable Niten identity defined in `IDENTITY.md`.
- Temporary `ONBOARDING.md` containing the complete onboarding and workspace initialization flow.
- Local `.musashi/identity/IDENTITY.md` generated from onboarding data.
- Cleanup step that deletes `ONBOARDING.md` after successful onboarding.

Acceptance criteria:

- An agent can conduct first-run onboarding.
- It can create an operator profile and empty inventory.
- It presents itself consistently as Niten.
- It creates `IDENTITY.md` and stores operator-specific branding and avatar metadata under `.musashi/identity/`.
- It allows the operator's personality preferences to replace any default personality aspect while preserving security and host-safety rules.
- It can offer an avatar-generation flow without storing the image or mutable identity data in Git.
- No onboarding skill, duplicate onboarding document, or permanent onboarding scaffolding is created.
- `ONBOARDING.md` is deleted after successful onboarding.

Phase implementations must first check whether the existing root `IDENTITY.md`, templates, and runtime instructions are sufficient. This phase is intentionally implemented in one temporary root document; any additional directory or substantial new file group requires the confirmation described in Section 5.9.

### Phase 3 — Multi-host and multi-node model

Authoritative operational source:

- All Leios Musashi Dojo testnet facts used to populate the Phase 3 skills and knowledge must be obtained from the official getting-started documentation: <https://leios.cardano-scaling.org/docs/testnet/getting-started/>.
- Treat that documentation and the official pages it links to as the source of truth for supported platforms, node releases, network parameters, bootstrap peers, configuration retrieval, ports, storage requirements, and operational procedures.
- The operator-maintained scripts repository <https://github.com/0xconssize/leios> may be consulted privately as design input for knowledge, skills, and playbooks. Do not reference, cite, copy, or integrate it in project deliverables outside this plan.
- Do not copy unverified values from prior sessions, local memory, examples, or third-party guides. Unknown or unavailable values remain explicit until verified from the official documentation.
- Before implementing or accepting a Phase 3 skill or knowledge entry, review the source for changes and record its retrieval date, relevant section or linked page, and the version/configuration it supports.
- A later review must be able to identify stale or obsolete skills and knowledge when the documentation changes; obsolete operational guidance must be marked for update or removal before it is used.

Deliver:

- Inventory schema.
- Host profile and state schemas.
- Node profile and state schemas.
- Host and node templates.
- Add-host skill.
- Add-node skill.
- Active-context rules.
- Operation-scope rules.
- Source-aware knowledge and skill metadata, including source URL, source section, retrieval date, and supported testnet/node version where applicable.
- A documentation-freshness review covering every Phase 3 operational skill and knowledge entry.

Acceptance criteria:

- One operator can register several hosts and nodes.
- Multiple nodes may reference the same host.
- The agent identifies the exact target before modifications.
- Node-specific and host-specific memory remain isolated.
- Every testnet-specific instruction and mutable value is traceable to the official documentation or an official page linked from it.
- A reviewer can determine whether each Phase 3 skill or knowledge entry is current, stale, or obsolete.
- The agent refuses to present stale or unverified testnet facts as current and directs the operator to the official documentation for re-verification.

### Phase 4 — Current testnet knowledge

Authoritative source policy:

- Use <https://leios.cardano-scaling.org/docs/testnet/getting-started/> as the authority for Musashi configuration and operational procedures.
- Use <https://github.com/input-output-hk/ouroboros-leios/releases> as the authority for the latest release, published assets, compatibility, and release-specific actions.
- Never fill gaps with Cardano mainnet documentation, defaults, commands, topology, ports, eras, key procedures, or operating assumptions.
- Select the most recently published non-draft official release even when the getting-started page lags, and mark versioned examples on the lagging page as stale.
- Apply the Phase 3 private-research boundary to all Phase 4 work.
- Record retrieval timestamps, exact source URLs, revisions or content hashes where available, explicit unknowns, internal source conflicts, and conditions that make each declaration stale.

Deliver:

- `network/current.yaml`.
- Release history.
- Bootstrap peer data.
- Requirements.
- Known issues.
- Source and verification conventions.

Acceptance criteria:

- Mutable network data is separated from stable documentation.
- Every current value has a source or verification timestamp.
- Unknown values are explicit.
- The agent does not rely on stale local memory for network facts.

### Phase 5 — Execution and server access

This phase inherits the Phase 4 source policy. Release selection, assets, compatibility, and release-specific actions come from the official releases repository; Musashi configuration and procedures come from the getting-started guide. Mainnet material must not fill gaps.

Deliver:

- Execution mode specification.
- Local execution policy.
- Remote execution policy.
- Execution capability schema.
- Connection profile schema.
- Execution plan schema.
- Command result schema.
- Host connection skill.
- Structured node-plan execution skill for lifecycle orchestration; concrete lifecycle procedures remain in Phase 6.
- Generated-script policy.
- Remote host identity checks.

Acceptance criteria:

- The agent determines advisory, local, or remote mode.
- It represents host access declaratively.
- It verifies the target before modifying it.
- It prepares a structured execution plan.
- It executes through runtime-provided tools.
- It validates results independently of exit status.
- It records actions in the local workspace.
- The repository still contains no executable source code.

### Phase 6 — Initial operational skills

Implementation boundary:

- Initial deployment covers the relay role only. Block-producer registration remains outside this phase.
- Installation, network configuration, and start are separate plans with independent validation; installation leaves the relay stopped.
- Lifecycle operations use the Phase 5 execution contracts and runtime-provided tools rather than embedded executors or transports.
- Diagnosis is read-only. Update and recovery are single-node operations; fleet rollout remains in Phase 7.
- Recovery must be tied to observed evidence and applicable official guidance. It never implies a full state reset.
- Issue reporting produces a sanitized local draft only; external publication requires a separate explicit operator instruction.

Deliver:

- Assess-host skill.
- Join-testnet skill.
- Install-relay skill.
- Start-node skill.
- Stop-node skill.
- Restart-node skill.
- Diagnose-node skill.
- Update-node skill.
- Recover-node skill.
- Report-issue skill.
- Supporting playbooks.

The minimal supporting set is `first-node-deployment.md`, `node-not-syncing.md`, `no-peer-connections.md`, `configuration-changed.md`, `recover-failed-node.md`, and `collect-diagnostics.md`. Fleet, rolling-update, testnet-respin, and repository-reconciliation playbooks remain in their later phases.

Acceptance criteria:

- Each skill declares inputs, scope, risks, outputs, and success criteria.
- Commands are documentation or templates only.
- Generated scripts are written under `.musashi/generated/`.
- Host-impacting actions have confirmation rules.

### Phase 7 — Fleet operations

Deliver:

- Inspect-fleet skill.
- Fleet-status schema.
- Rolling update playbook.
- Multi-node diagnostic workflow.
- Shared-host impact checks.

Acceptance criteria:

- The agent can inspect all registered nodes.
- It can filter by role, host, or status.
- It can plan a rolling update.
- It stops fleet operations when pilot validation fails.

### Phase 8 — Runtime compatibility validation

Validate with:

- Claude Code.
- OpenClaw.
- Hermes.
- At least one generic repository-aware agent.

For each runtime, document:

- How repository instructions are discovered.
- How skills are loaded.
- How local memory is maintained.
- How commands are executed.
- How remote hosts are accessed.
- Known incompatibilities.
- Recommended setup.

Acceptance criteria:

- The canonical repository remains runtime-neutral.
- Runtime-specific notes do not duplicate the full project logic.
- The same local schemas can be used across runtimes.

---

## 26. Initial MVP

The first usable release should support:

1. First-run onboarding.
2. Niten identity and personality.
3. Local workspace creation.
4. Operator profile creation.
5. Advisory, local, and remote execution modes.
6. Registration of several hosts.
7. Registration of several nodes.
8. Several nodes on one host.
9. Host access description and verification.
10. Host assessment.
11. Relay installation guidance.
12. Node start, stop, and restart.
13. Node health inspection.
14. Node diagnosis.
15. Scoped update execution.
16. Structured operation and issue reporting.
17. Repository update reconciliation.
18. Host-focused safety rules.

Block producer registration, BLS operations, advanced orchestration, and coordinated test campaigns may follow after the relay workflow is stable.

---

## 27. MVP Definition of Done

The MVP is complete when an operator can clone the repository and ask a compatible agent to:

1. Read the repository instructions.
2. Introduce itself as Niten.
3. Create `.musashi/`.
4. Onboard the operator.
5. Detect and record its execution mode.
6. Register two or more hosts or nodes.
7. Associate several nodes with one or more hosts.
8. Register host access information.
9. Verify that it is connected to the intended host.
10. Assess a target host.
11. Prepare an installation plan for one relay.
12. Generate required commands or scripts locally.
13. Explain host-level risks.
14. Execute only after the appropriate confirmation.
15. Start or restart one selected node.
16. Inspect the node after installation.
17. Validate the real operational result.
18. Store node-specific and host-specific memory.
19. Produce a structured diagnostic report.
20. Prepare and execute a scoped node update.
21. Avoid affecting other registered nodes on a shared host.
22. Fall back to advisory mode when execution is unavailable.
23. Detect a later Git update.
24. Reconcile local state without overwriting it.
25. Keep all generated scripts and private operational state outside Git.

---

## 28. Governance and Maintenance

Changes to the following files should receive extra review:

- `AGENTS.md`.
- `AGENT.md`.
- `IDENTITY.md`.
- `SECURITY.md`.
- `HOST_SAFETY.md`.
- `network/current.yaml`.
- `skills/`.
- `playbooks/`.
- `schemas/`.

Pull requests that add command templates should explain:

- Target operating systems.
- Required privileges.
- Affected paths.
- Possible impact on shared hosts.
- Validation steps.
- Rollback or recovery steps.
- Impact classification.

Updates to current testnet data should include:

- Source.
- Verification date.
- Relevant release or commit.
- Whether existing nodes require action.

Branding changes should preserve:

- **Musashi Dojo Agent** as the project name.
- **Niten** as the canonical agent name.
- **Dojo Node Operator** as the role.
- The principle of two complementary capabilities working as one.

---

## 29. Future Extensions

Possible future additions include:

- Block producer onboarding.
- BLS key procedures.
- Coordinated test campaigns.
- Reproducible benchmark definitions.
- Shared anonymized diagnostic datasets.
- Testnet topology recommendations.
- Cloud-provider-specific playbooks.
- Advanced remote-host onboarding.
- Agent-generated dashboard definitions.
- Declarative MCP mappings.
- Migration tools generated from schemas.
- Community-contributed personality variants.
- Multiple visual identity profiles.
- Fleet policy definitions.
- Scheduled health checks through runtime capabilities.
- Automated GitHub issue generation and submission.

All extensions should preserve the declarative nature of the repository.

---

## 30. Final Product Definition

Musashi Dojo Agent will be:

> **A portable, declarative repository of identity, operational memory conventions, testnet knowledge, skills, playbooks, configuration, and schemas that enables AI agents to advise on or directly operate one or more Cardano Leios testnet nodes.**

The repository supplies:

- Niten's identity and personality.
- Knowledge.
- Procedures.
- Safety rules.
- Data contracts.
- Execution plans.

The agent runtime may supply:

- Reasoning.
- Conversation.
- Local command execution.
- Remote server access.
- Script generation.
- File operations.
- Service and container management.

The local `.musashi/` workspace supplies:

- Operator memory.
- Host and node inventory.
- Connection profiles.
- Generated scripts.
- Execution plans.
- Session history.
- Reports.
- Continuity across repository updates and agent runtimes.

The final operating principle is:

> **Operate the Dojo. Protect the host.**
