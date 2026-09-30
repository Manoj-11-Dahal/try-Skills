---
name: code-review-and-diff-audit
description: "Use when reviewing a code or configuration change for correctness, regressions, security, maintainability, and compatibility before it is accepted or merged to inspect the actual diff against its intended behavior and report only actionable, evidence-backed findings. Trigger for requested reviews, pull requests, or high-impact changes; do not silently rewrite the implementation during a review."
---

# Code Review and Diff Audit

## Overview

This skill applies when reviewing a code or configuration change for correctness, regressions, security, maintainability, and compatibility before it is accepted or merged. Its intended outcome is to inspect the actual diff against its intended behavior and report only actionable, evidence-backed findings.

## When to Use

### Preserved source section: When to Use

Use this skill when the task is to assess a proposed change rather than implement it. For cross-layer agent-system design, use `agent-architecture-audit`; for application security threats, add `application-security-review`.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Review Boundaries

- Do not modify files, approve, merge, commit, or deploy unless the user separately authorizes that exact action.
- Do not report unrelated pre-existing problems as regressions introduced by the diff; label them separately if they materially affect the requested review.
- When context is missing, say what could not be assessed and what evidence would resolve it.

### Source boundary statements from: Procedure

1. **Establish the review surface.** Confirm the base, changed files, and working-tree state. Read the task description and relevant surrounding code; do not infer intent from the diff alone.
4. **Verify suspicious claims.** Run targeted, non-destructive checks only when permitted and useful. Do not mark a concern as confirmed based solely on naming or style; distinguish evidence from inference.

### Source boundary statements from: Finding Standard

A finding should identify a reproducible defect or credible risk in the changed code, explain when it occurs, and point to the narrowest relevant location. If no actionable defect is established, do not invent one to fill a quota. Put optional style suggestions in a separate, clearly non-blocking section or omit them.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The exact diff and its base revision or expected prior state.
- The change request, acceptance criteria, and repository conventions.
- Relevant callers, tests, interfaces, migrations, and deployment assumptions.
- The requested review depth and any explicit scope limits.

## Instructions

### Preserved source section: Procedure

1. **Establish the review surface.** Confirm the base, changed files, and working-tree state. Read the task description and relevant surrounding code; do not infer intent from the diff alone.
2. **Trace behavior.** Follow changed paths through callers, state transitions, data boundaries, and error handling. Check both the expected case and plausible regressions.
3. **Review independent dimensions.** Assess correctness, backward compatibility, security/privacy, failure handling, concurrency, data integrity, tests, maintainability, and operational impact where relevant.
4. **Verify suspicious claims.** Run targeted, non-destructive checks only when permitted and useful. Do not mark a concern as confirmed based solely on naming or style; distinguish evidence from inference.
5. **Prioritize findings.** Report correctness and risk issues first. Give each finding a severity, exact location, triggering condition, impact, and actionable remedy. Avoid duplicate findings and speculative hypotheticals without a credible path.
6. **Check test adequacy.** Determine whether tests exercise the changed behavior and important failure cases. A passing suite does not by itself prove that the new behavior is covered.
7. **Return a review result.** State whether there are blocking findings, non-blocking concerns, or no issues found within the reviewed scope. Mention checks run and limits of inspection.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

4. **Verify suspicious claims.** Run targeted, non-destructive checks only when permitted and useful. Do not mark a concern as confirmed based solely on naming or style; distinguish evidence from inference.

### Source conditional guidance from: Finding Standard

A finding should identify a reproducible defect or credible risk in the changed code, explain when it occurs, and point to the narrowest relevant location. If no actionable defect is established, do not invent one to fill a quota. Put optional style suggestions in a separate, clearly non-blocking section or omit them.

### Source conditional guidance from: Review Boundaries

- Do not modify files, approve, merge, commit, or deploy unless the user separately authorizes that exact action.
- Do not report unrelated pre-existing problems as regressions introduced by the diff; label them separately if they materially affect the requested review.
- When context is missing, say what could not be assessed and what evidence would resolve it.

## Output Format

### Preserved source section: Finding Standard

A finding should identify a reproducible defect or credible risk in the changed code, explain when it occurs, and point to the narrowest relevant location. If no actionable defect is established, do not invent one to fill a quota. Put optional style suggestions in a separate, clearly non-blocking section or omit them.

## Validation Checklist

Not specified in source skill.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Trace behavior.** Follow changed paths through callers, state transitions, data boundaries, and error handling. Check both the expected case and plausible regressions.
3. **Review independent dimensions.** Assess correctness, backward compatibility, security/privacy, failure handling, concurrency, data integrity, tests, maintainability, and operational impact where relevant.
6. **Check test adequacy.** Determine whether tests exercise the changed behavior and important failure cases. A passing suite does not by itself prove that the new behavior is covered.

### Source edge/failure guidance from: Review Boundaries

- Do not report unrelated pre-existing problems as regressions introduced by the diff; label them separately if they materially affect the requested review.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

Not specified in source skill.
