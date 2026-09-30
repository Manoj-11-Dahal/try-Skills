---
name: programming-language-development
description: "Use when designing or implementing a programming language, interpreter, compiler, bytecode format, or language tooling to define a small grammar and observable semantics first, then validate parsing, evaluation, diagnostics, and resource limits with a conformance suite. Trigger for language syntax, type rules, compiler passes, or runtime behavior."
---

# Programming Language Development

## Overview

This skill applies when designing or implementing a programming language, interpreter, compiler, bytecode format, or language tooling. Its intended outcome is to define a small grammar and observable semantics first, then validate parsing, evaluation, diagnostics, and resource limits with a conformance suite.

## When to Use

### Preserved source section: When to Use

Use for a new language or a substantial language implementation. Begin with a tiny, coherent language core; defer macros, optimization, and advanced type systems until basic semantics are testable.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

4. **Keep evaluation contained.** Do not pass source text to the host language's `eval` or shell. Restrict filesystem, network, reflection, and native calls unless explicitly part of the language contract.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Language goals, target users, syntax, execution model, and compatibility expectations.
- Grammar, type rules, runtime model, error format, and host integration boundaries.
- Test programs, expected outputs, and resource/security requirements.

## Instructions

### Preserved source section: Procedure

1. **Write semantic examples.** Define small programs and their exact results before choosing parser or compiler architecture.
2. **Build front to back.** Implement lexer, parser, AST, semantic checks, and interpreter or code generation as separate stages with inspectable outputs.
3. **Specify errors.** Preserve source locations and distinguish syntax, type, runtime, and resource-limit errors. Reject unsupported constructs clearly.
4. **Keep evaluation contained.** Do not pass source text to the host language's `eval` or shell. Restrict filesystem, network, reflection, and native calls unless explicitly part of the language contract.
5. **Test conformance.** Include valid and invalid programs, precedence, scope, types, control flow, errors, and edge cases. Add property or fuzz testing for parsers with strict time and memory limits.
6. **Version the language.** Document grammar and compatibility changes; use golden tests for programs that should retain their meaning.
7. **Optimize after profiling.** Preserve an understandable reference interpreter or intermediate representation for differential tests.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

4. **Keep evaluation contained.** Do not pass source text to the host language's `eval` or shell. Restrict filesystem, network, reflection, and native calls unless explicitly part of the language contract.

### Source conditional guidance from: Output and Acceptance

Report the supported grammar and semantics, execution boundary, diagnostics, tests, and omitted features. Accept a language slice only when its examples parse and behave as specified and malformed input terminates with bounded, useful errors.

## Output Format

### Preserved source section: Output and Acceptance

Report the supported grammar and semantics, execution boundary, diagnostics, tests, and omitted features. Accept a language slice only when its examples parse and behave as specified and malformed input terminates with bounded, useful errors.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Grammar, type rules, runtime model, error format, and host integration boundaries.

### Source edge/failure guidance from: Procedure

3. **Specify errors.** Preserve source locations and distinguish syntax, type, runtime, and resource-limit errors. Reject unsupported constructs clearly.
5. **Test conformance.** Include valid and invalid programs, precedence, scope, types, control flow, errors, and edge cases. Add property or fuzz testing for parsers with strict time and memory limits.

### Source edge/failure guidance from: Output and Acceptance

Report the supported grammar and semantics, execution boundary, diagnostics, tests, and omitted features. Accept a language slice only when its examples parse and behave as specified and malformed input terminates with bounded, useful errors.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report the supported grammar and semantics, execution boundary, diagnostics, tests, and omitted features. Accept a language slice only when its examples parse and behave as specified and malformed input terminates with bounded, useful errors.
