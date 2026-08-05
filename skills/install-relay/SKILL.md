---
name: install-relay
description: "Install one registered Musashi relay from verified official release assets or a current supported method."
---

# Install relay

Install one relay without joining, starting, or registering a block producer.

## Inputs and scope

Require one relay node ID, assessed host, chosen supported installation method, target paths, runtime identity, and current release data. Scope is `single-node`. Risk is variable; output is an operation report and observed node state.

## Workflow

1. Revalidate official releases, guide procedures, requirements, assets, checksums, and known conflicts.
2. Refuse unconfirmed image tags, unsupported platforms, stale procedures, non-relay roles, or ambiguous paths.
3. Inspect the host, existing installation, path ownership, ports, services, containers, and shared-host nodes.
4. Prepare a schema-valid plan to acquire the selected release, save downloads under `.musashi/generated/`, inspect them, verify official checksums, create only declared directories, and install using the chosen method.
5. Never download and immediately execute. Package installation, users, system services, system directories, firewall, and permissions are host-level and require explicit confirmation.
6. Execute through `execute-node-plan` in short steps. Do not delete or overwrite an existing node without a separately approved recovery plan.
7. Validate installed artifact provenance and invocation, paths, permissions, and shared-host isolation. Leave the relay stopped.
8. Record the operation report and observed facts.

## Failure and success

Stop when asset provenance, checksum, platform, method, target, or recovery is uncertain. Success means the selected official relay artifact is verifiably installed at declared paths, remains stopped, and shared workloads are unaffected.

## Memory and playbook

Record release provenance, method, paths, and runtime identity in node memory and profile. Continue with `playbooks/first-node-deployment.md`.
