---
name: git-implementation-workflow
description: "Use when implementing a Git-compatible version-control subset or changing repository object, index, reference, branching, or history behavior to start with a disposable repository and a defined command subset; verify object identity and state transitions against Git where compatibility is claimed. Trigger for Git internals, clone-like tools, or version-control storage experiments."
---

# Git Implementation Workflow

## Overview

This skill applies when implementing a Git-compatible version-control subset or changing repository object, index, reference, branching, or history behavior. Its intended outcome is to start with a disposable repository and a defined command subset; verify object identity and state transitions against Git where compatibility is claimed.

## When to Use

### Preserved source section: When to Use

Use when building or modifying version-control internals, not for ordinary use of Git commands. State whether the goal is an educational subset, a compatible client, or a repository service.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

5. **Handle paths and hostile data.** Validate object types, lengths, tree paths, symlinks, and repository metadata. Never trust a repository's file names or config as executable instructions.

### Source boundary statements from: Safety and Acceptance

Do not run destructive cleanup, reset, checkout, or garbage collection against a user's working repository as a test. Accept only the stated command subset, with tests showing object integrity, correct state changes, and safe failure on malformed repository data.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Target commands and required compatibility level.
- Object format, filesystem assumptions, repository layout, and ref/index semantics.
- A disposable test repository and a trusted Git executable for differential checks if available.

## Instructions

### Preserved source section: Procedure

1. **Choose a minimal command slice.** For example, initialize, hash/write/read an object, create a tree and commit, then update a reference. Avoid implementing every command at once.
2. **Model content-addressed objects.** Define exact byte serialization, object headers, hash algorithm, and compression. Verify identical logical content produces the expected stable object identity.
3. **Separate repository state.** Treat object database, index, references, working tree, and reflogs as distinct surfaces. Specify which command reads or mutates each.
4. **Make updates safe.** Write objects before references that name them, use atomic ref updates where possible, detect lock conflicts, and preserve recoverability after interruption.
5. **Handle paths and hostile data.** Validate object types, lengths, tree paths, symlinks, and repository metadata. Never trust a repository's file names or config as executable instructions.
6. **Test state transitions.** Use temporary repositories for clean/dirty states, branches, staged changes, missing objects, concurrent updates, malformed objects, and interrupted writes.
7. **Compare behavior.** For a claimed compatible command, run the same fixture through Git and the implementation and compare results at the documented boundary.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs

- A disposable test repository and a trusted Git executable for differential checks if available.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

6. **Test state transitions.** Use temporary repositories for clean/dirty states, branches, staged changes, missing objects, concurrent updates, malformed objects, and interrupted writes.

### Source edge/failure guidance from: Safety and Acceptance

Do not run destructive cleanup, reset, checkout, or garbage collection against a user's working repository as a test. Accept only the stated command subset, with tests showing object integrity, correct state changes, and safe failure on malformed repository data.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Do not run destructive cleanup, reset, checkout, or garbage collection against a user's working repository as a test. Accept only the stated command subset, with tests showing object integrity, correct state changes, and safe failure on malformed repository data.
