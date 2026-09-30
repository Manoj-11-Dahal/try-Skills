---
name: emulator-and-virtual-machine-development
description: "Use when implementing an emulator, virtual machine, instruction interpreter, device model, or guest execution environment to choose a documented ISA and bounded machine model, then validate instruction semantics and isolation before running guest programs. Trigger for CPU emulation, bytecode execution, virtual devices, or VM snapshots."
---

# Emulator and Virtual Machine Development

## Overview

This skill applies when implementing an emulator, virtual machine, instruction interpreter, device model, or guest execution environment. Its intended outcome is to choose a documented ISA and bounded machine model, then validate instruction semantics and isolation before running guest programs.

## When to Use

### Preserved source section: When to Use

Use for a system that reproduces another machine's instruction or device behavior, or safely executes code inside a defined virtual machine. State the compatibility target and supported subset before coding.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

6. **Contain guest execution.** Treat guest binaries as untrusted. Enforce instruction, memory, file, and wall-time limits; never forward host filesystem or network access by default.

### Source boundary statements from: Safety and Acceptance

Run untrusted guests only in the intended sandbox or disposable VM. Do not claim isolation based on an interpreter alone if host APIs remain reachable. Accept an ISA feature only when edge cases and fault behavior match the documented subset and tests are reproducible.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- ISA or bytecode specification, target behavior, and allowed extensions.
- Memory map, register state, devices, interrupts, timing, and I/O expectations.
- Test programs, reference emulator or vectors, host platform, and guest trust level.

## Instructions

### Preserved source section: Procedure

1. **Define the machine.** Document registers, word sizes, endianness, address map, reset state, exceptions, and instruction encodings.
2. **Implement fetch-decode-execute incrementally.** Start with a few instructions and explicit program-counter rules. Keep instruction decoding separate from state mutation where practical.
3. **Model faults and devices.** Specify invalid opcode, alignment, privilege, interrupt, timer, and I/O behavior. Return bounded errors instead of hanging on malformed guest state.
4. **Preserve deterministic execution.** Control clocks, random input, and device events so tests can reproduce traces. Define snapshot format and compatibility before adding save states.
5. **Compare against references.** Use official or project test vectors, small hand-checked programs, instruction-by-instruction traces, and differential tests where a trusted reference exists.
6. **Contain guest execution.** Treat guest binaries as untrusted. Enforce instruction, memory, file, and wall-time limits; never forward host filesystem or network access by default.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Acceptance

Run untrusted guests only in the intended sandbox or disposable VM. Do not claim isolation based on an interpreter alone if host APIs remain reachable. Accept an ISA feature only when edge cases and fault behavior match the documented subset and tests are reproducible.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

1. **Define the machine.** Document registers, word sizes, endianness, address map, reset state, exceptions, and instruction encodings.
3. **Model faults and devices.** Specify invalid opcode, alignment, privilege, interrupt, timer, and I/O behavior. Return bounded errors instead of hanging on malformed guest state.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Run untrusted guests only in the intended sandbox or disposable VM. Do not claim isolation based on an interpreter alone if host APIs remain reachable. Accept an ISA feature only when edge cases and fault behavior match the documented subset and tests are reproducible.
