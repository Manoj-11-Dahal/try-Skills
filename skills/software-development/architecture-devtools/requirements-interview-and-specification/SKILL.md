---
name: requirements-interview-and-specification
description: "Use when a feature request is ambiguous, consequential, or large enough that different interpretations would produce materially different results to clarify user goals and constraints, ask only decision-changing questions, then write a compact, testable specification. Trigger before planning implementation when essential behavior, actors, scope, or acceptance conditions are missing."
---

# Requirements Interview and Specification

## Overview

This skill applies when a feature request is ambiguous, consequential, or large enough that different interpretations would produce materially different results. Its intended outcome is to clarify user goals and constraints, ask only decision-changing questions, then write a compact, testable specification.

## When to Use

### Preserved source section: When to Use

Use this workflow when unanswered product or behavior decisions could change the implementation, risk, or acceptance result. Skip the interview for small, reversible tasks with an obvious interpretation; state a reasonable assumption and proceed.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

3. **Ask focused questions.** Ask one decision-changing question at a time when possible. Offer concrete, neutral choices and a sensible default where useful. Do not ask again for facts already supplied.
6. **Check consistency.** Look for conflicting requirements, hidden dependencies, and acceptance criteria that cannot be observed. Resolve material conflicts before planning work.
7. **Hand off to planning.** Once the specification is sufficient, use `task-decomposition-and-planning` to sequence implementation and verification. Do not duplicate the plan inside the spec.

### Source boundary statements from: Stop Conditions

- Do not treat a draft, interview answer, or generated specification as permission to make external changes.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The user's request, known constraints, and any prior decisions.
- Existing product behavior, repository conventions, and relevant documentation.
- The decisions that would materially affect scope, safety, compatibility, or user experience.

## Instructions

### Preserved source section: Procedure

1. **Restate the outcome.** Summarize the goal in one sentence without quietly adding features. Separate the user’s desired result from a proposed implementation.
2. **Identify decision gaps.** List only missing facts that could change the result: actor, trigger, success behavior, failure behavior, permissions, data handling, compatibility, or out-of-scope areas.
3. **Ask focused questions.** Ask one decision-changing question at a time when possible. Offer concrete, neutral choices and a sensible default where useful. Do not ask again for facts already supplied.
4. **Bound the scope.** Make explicit what is included, excluded, and deferred. Record assumptions and distinguish user-confirmed decisions from agent-proposed defaults.
5. **Write testable requirements.** Express key behavior as observable acceptance criteria. Include important negative cases, permissions, error handling, and constraints that affect implementation.
6. **Check consistency.** Look for conflicting requirements, hidden dependencies, and acceptance criteria that cannot be observed. Resolve material conflicts before planning work.
7. **Hand off to planning.** Once the specification is sufficient, use `task-decomposition-and-planning` to sequence implementation and verification. Do not duplicate the plan inside the spec.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

3. **Ask focused questions.** Ask one decision-changing question at a time when possible. Offer concrete, neutral choices and a sensible default where useful. Do not ask again for facts already supplied.

### Source conditional guidance from: Stop Conditions

- Ask the user when a material choice has no safe, reversible default.

## Output Format

### Preserved source section: Specification Shape

Keep the artifact proportional to the task. For a substantial feature, include: objective, actors, primary flow, acceptance criteria, constraints, non-goals, open questions, and approval boundaries. For a small change, a short checklist is enough.

## Validation Checklist

Not specified in source skill.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Identify decision gaps.** List only missing facts that could change the result: actor, trigger, success behavior, failure behavior, permissions, data handling, compatibility, or out-of-scope areas.
5. **Write testable requirements.** Express key behavior as observable acceptance criteria. Include important negative cases, permissions, error handling, and constraints that affect implementation.

## Stop Conditions

### Preserved source section: Stop Conditions

- Ask the user when a material choice has no safe, reversible default.
- Mark unresolved questions rather than inventing decisions.
- Do not treat a draft, interview answer, or generated specification as permission to make external changes.
- Stop clarifying once the remaining uncertainty no longer changes the agreed outcome or implementation risk.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

Not specified in source skill.
