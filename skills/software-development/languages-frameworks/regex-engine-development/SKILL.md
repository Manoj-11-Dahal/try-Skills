---
name: regex-engine-development
description: "Use when implementing a regular-expression parser, matcher, or regex feature set to define syntax and matching semantics explicitly, choose an execution strategy with bounded worst-case behavior, and test edge cases before accepting untrusted patterns or text. Trigger for regex engine internals, compatibility, or ReDoS-sensitive matching."
---

# Regular-Expression Engine Development

## Overview

This skill applies when implementing a regular-expression parser, matcher, or regex feature set. Its intended outcome is to define syntax and matching semantics explicitly, choose an execution strategy with bounded worst-case behavior, and test edge cases before accepting untrusted patterns or text.

## When to Use

### Preserved source section: When to Use

Use for a regex engine or a new syntax feature, not simply for writing one application pattern. State the compatibility target and supported syntax subset.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Required operators, flags, Unicode behavior, capture semantics, and match-selection policy.
- Pattern and input size limits, timeout requirements, and trust level of both inputs.
- Reference implementation or conformance cases if compatibility is needed.

## Instructions

### Preserved source section: Procedure

1. **Specify the language.** Define precedence, escaping, character classes, anchors, quantifiers, groups, alternation, and unsupported syntax.
2. **Parse to an explicit representation.** Reject malformed patterns with location-aware errors. Keep parsing independent from matching and preserve enough structure for captures if required.
3. **Choose complexity deliberately.** Prefer an automaton-based approach or another bounded strategy for untrusted patterns. If using backtracking, enforce a real step/time budget and surface timeout distinctly from no match.
4. **Implement semantics in small steps.** Add literals, concatenation, alternation, repetition, anchors, classes, then captures only as required. Specify greedy/lazy behavior and empty-string progress.
5. **Test boundary behavior.** Cover empty patterns, empty matches, Unicode, escaping, nested quantifiers, long inputs, zero-width matches, and malformed syntax.
6. **Differential-test carefully.** Compare only the declared subset against a reference engine; explain intentional differences rather than claiming full compatibility.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs

- Reference implementation or conformance cases if compatibility is needed.

### Source conditional guidance from: Procedure

2. **Parse to an explicit representation.** Reject malformed patterns with location-aware errors. Keep parsing independent from matching and preserve enough structure for captures if required.
3. **Choose complexity deliberately.** Prefer an automaton-based approach or another bounded strategy for untrusted patterns. If using backtracking, enforce a real step/time budget and surface timeout distinctly from no match.

### Source conditional guidance from: Safety and Acceptance

Treat user-controlled patterns as potentially adversarial. Apply input limits and avoid catastrophic backtracking or provide enforceable budgets. Accept a feature only when semantic tests pass and worst-case execution remains bounded for its stated threat model.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Pattern and input size limits, timeout requirements, and trust level of both inputs.

### Source edge/failure guidance from: Procedure

2. **Parse to an explicit representation.** Reject malformed patterns with location-aware errors. Keep parsing independent from matching and preserve enough structure for captures if required.
3. **Choose complexity deliberately.** Prefer an automaton-based approach or another bounded strategy for untrusted patterns. If using backtracking, enforce a real step/time budget and surface timeout distinctly from no match.
5. **Test boundary behavior.** Cover empty patterns, empty matches, Unicode, escaping, nested quantifiers, long inputs, zero-width matches, and malformed syntax.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Treat user-controlled patterns as potentially adversarial. Apply input limits and avoid catastrophic backtracking or provide enforceable budgets. Accept a feature only when semantic tests pass and worst-case execution remains bounded for its stated threat model.
