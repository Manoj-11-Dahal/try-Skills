---
name: docker-runtime-development
description: "Use when building an educational container runtime or implementing container-image and process-isolation behavior inspired by Docker or OCI formats to define the supported subset and isolation assumptions, then test only in disposable environments without privileged host changes. Trigger for image layers, namespaces, container launch, or container-runtime internals."
---

# Docker-Style Runtime Development

## Overview

This skill applies when building an educational container runtime or implementing container-image and process-isolation behavior inspired by Docker or OCI formats. Its intended outcome is to define the supported subset and isolation assumptions, then test only in disposable environments without privileged host changes.

## When to Use

### Preserved source section: When to Use

Use when the objective is to understand or prototype container-runtime internals, not merely to write a Dockerfile or package an application. Explicitly separate image-format handling from process isolation.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

1. **Constrain the prototype.** Pick one image format and a minimal process-launch path. Document unsupported features and do not claim OCI or Docker compatibility without conformance evidence.
5. **Use least privilege.** Prefer rootless execution and disposable VMs. Do not disable host security controls or run privileged container commands without explicit approval.

### Source boundary statements from: Safety and Acceptance

Never execute arbitrary downloaded images on the host as a test shortcut. Use a disposable VM or similarly isolated environment and require approval for privileged setup. Accept only the explicitly tested runtime subset; report residual host-kernel exposure and unsupported security properties.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Target operating system, kernel features, architecture, and runtime privileges.
- Supported image/config subset, filesystem behavior, namespaces, resource controls, and networking.
- Disposable test environment and permitted commands or system changes.

## Instructions

### Preserved source section: Procedure

1. **Constrain the prototype.** Pick one image format and a minimal process-launch path. Document unsupported features and do not claim OCI or Docker compatibility without conformance evidence.
2. **Inspect untrusted images safely.** Bound archive size, file count, path length, and decompression ratio. Reject path traversal, unsafe links, unexpected device nodes, and malformed metadata.
3. **Separate host setup from runtime logic.** Test parsers and layer application in temporary directories. Keep privileged operations behind explicit, reviewable boundaries.
4. **Model isolation honestly.** Identify which namespaces, cgroups, capabilities, seccomp rules, mounts, and user mappings exist. A namespace or chroot alone is not a security sandbox.
5. **Use least privilege.** Prefer rootless execution and disposable VMs. Do not disable host security controls or run privileged container commands without explicit approval.
6. **Verify cleanup and resource bounds.** Check process termination, mount cleanup, CPU/memory limits, filesystem visibility, and behavior after errors or interruption.
7. **Test adversarial inputs.** Cover malformed archives, duplicate paths, symlink escapes, huge layers, permission errors, and concurrent launch/cleanup races.

## Decision Rules

Not specified in source skill.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Inspect untrusted images safely.** Bound archive size, file count, path length, and decompression ratio. Reject path traversal, unsafe links, unexpected device nodes, and malformed metadata.
6. **Verify cleanup and resource bounds.** Check process termination, mount cleanup, CPU/memory limits, filesystem visibility, and behavior after errors or interruption.
7. **Test adversarial inputs.** Cover malformed archives, duplicate paths, symlink escapes, huge layers, permission errors, and concurrent launch/cleanup races.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Never execute arbitrary downloaded images on the host as a test shortcut. Use a disposable VM or similarly isolated environment and require approval for privileged setup. Accept only the explicitly tested runtime subset; report residual host-kernel exposure and unsupported security properties.
