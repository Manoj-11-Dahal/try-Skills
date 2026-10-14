---
name: operating-system-development
description: "Use when building or modifying an operating-system kernel, boot path, scheduler, memory manager, system call layer, or basic device support to work in a documented emulator or disposable machine, implement one kernel boundary at a time, and keep host-system changes out of the development loop. Trigger for OS, kernel, or low-level boot projects."
---

# Operating System Development

## Overview

This skill applies when building or modifying an operating-system kernel, boot path, scheduler, memory manager, system call layer, or basic device support. Its intended outcome is to work in a documented emulator or disposable machine, implement one kernel boundary at a time, and keep host-system changes out of the development loop.

## When to Use

### Preserved source section: When to Use

Use for kernel and operating-system internals. State the target architecture and whether the project is a teaching kernel, research prototype, or system expected to boot on hardware.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

6. **Keep user programs contained.** Apply privilege separation and resource limits; never treat a teaching kernel as a secure sandbox without a threat analysis.

### Source boundary statements from: Safety and Acceptance

Do not flash firmware, change bootloaders, repartition disks, or run privileged host commands as an implicit test. Accept a slice only when it boots reproducibly in the declared environment and its invariants and failure behavior are covered by observable tests.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- CPU architecture, boot protocol, toolchain, emulator, and debug interface.
- Memory map, privilege model, interrupts, scheduling, system calls, and device goals.
- Build, test, and recovery method for the virtual machine or target hardware.

## Instructions

### Preserved source section: Procedure

1. **Create a reproducible boot path.** Pin toolchain versions, produce a minimal image, and capture emulator output. Keep boot and kernel initialization failures observable.
2. **Define machine boundaries.** Document privilege levels, address spaces, interrupt handling, calling conventions, and ownership of memory and devices.
3. **Add one primitive at a time.** Establish console output, exceptions, physical memory management, virtual memory, scheduling, and system calls in a sequence that preserves a known-good boot checkpoint.
4. **Enforce invariants.** Check alignment, ownership, permissions, stack bounds, locking, and cleanup at subsystem boundaries. Fail visibly instead of continuing with corrupted kernel state.
5. **Test with emulation and fault cases.** Exercise invalid system calls, allocation failure, interrupts, concurrent tasks, and restart behavior in the emulator. Use hardware only with explicit approval and recovery access.
6. **Keep user programs contained.** Apply privilege separation and resource limits; never treat a teaching kernel as a secure sandbox without a threat analysis.
7. **Record compatibility.** State which architecture, boot path, devices, and system-call subset are supported.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Acceptance

Do not flash firmware, change bootloaders, repartition disks, or run privileged host commands as an implicit test. Accept a slice only when it boots reproducibly in the declared environment and its invariants and failure behavior are covered by observable tests.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Build, test, and recovery method for the virtual machine or target hardware.

### Source edge/failure guidance from: Procedure

1. **Create a reproducible boot path.** Pin toolchain versions, produce a minimal image, and capture emulator output. Keep boot and kernel initialization failures observable.
3. **Add one primitive at a time.** Establish console output, exceptions, physical memory management, virtual memory, scheduling, and system calls in a sequence that preserves a known-good boot checkpoint.
4. **Enforce invariants.** Check alignment, ownership, permissions, stack bounds, locking, and cleanup at subsystem boundaries. Fail visibly instead of continuing with corrupted kernel state.
5. **Test with emulation and fault cases.** Exercise invalid system calls, allocation failure, interrupts, concurrent tasks, and restart behavior in the emulator. Use hardware only with explicit approval and recovery access.

### Source edge/failure guidance from: Safety and Acceptance

Do not flash firmware, change bootloaders, repartition disks, or run privileged host commands as an implicit test. Accept a slice only when it boots reproducibly in the declared environment and its invariants and failure behavior are covered by observable tests.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Do not flash firmware, change bootloaders, repartition disks, or run privileged host commands as an implicit test. Accept a slice only when it boots reproducibly in the declared environment and its invariants and failure behavior are covered by observable tests.
