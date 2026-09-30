---
name: verification-and-stopping
description: "Use when an agent must prove that a deliverable meets an objective before claiming completion to turn goals into observable checks, choose independent evidence, define pass and fail thresholds, and state explicit stop conditions. Trigger for code, research, data, documents, and long-running agent work where plausible output is not sufficient evidence."
---

# Verification and Stopping

## Overview

This skill applies when an agent must prove that a deliverable meets an objective before claiming completion. Its intended outcome is to turn goals into observable checks, choose independent evidence, define pass and fail thresholds, and state explicit stop conditions.

## When to Use

### Preserved source section: When to Use

Use this skill when the task has acceptance criteria, quality expectations, external effects, or multiple iterations. Apply it before reporting a task as complete, especially when the artifact can look plausible while still being incorrect.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

6. **Handle failures honestly.** Fix and re-check when safe. If a check cannot run, mark it blocked or unverified; do not silently treat it as passing.

### Source boundary statements from: Stopping Rules

- Stop on failure when continued attempts cannot change the evidence or would exceed the budget.
- Never extend a loop solely to make a score look better after the user-defined budget is exhausted.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The requested outcome and any explicit acceptance criteria.
- The artifact or system state to verify.
- Available tests, authoritative sources, independent reviewers, or other evidence.
- Known limitations, resource budgets, and any required human decision.

## Instructions

### Preserved source section: Procedure

1. **Translate the goal into checks.** Write each important requirement as an observable assertion. Separate mandatory checks from preferences.
2. **Choose evidence before acting.** Prefer deterministic tests, direct state inspection, and authoritative references. Use a second reviewer or independent check for high-impact work.
3. **Define thresholds.** Specify what counts as pass, fail, partial, or unknown. Avoid moving the threshold after seeing the result.
4. **Run the checks.** Execute or inspect the smallest relevant set of checks. Capture the exact commands, source references, output, and environment limitations.
5. **Evaluate the artifact, not the effort.** Compare actual behavior and content with the acceptance criteria. A completed plan, successful tool call, or plausible explanation is not itself proof.
6. **Handle failures honestly.** Fix and re-check when safe. If a check cannot run, mark it blocked or unverified; do not silently treat it as passing.
7. **Apply the stop rule.** Stop when all required criteria pass, a defined terminal failure occurs, a budget is reached, progress stalls, or a human decision is required.
8. **Report status precisely.** Distinguish verified completion from partial work, blocked checks, and assumptions.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

6. **Handle failures honestly.** Fix and re-check when safe. If a check cannot run, mark it blocked or unverified; do not silently treat it as passing.
7. **Apply the stop rule.** Stop when all required criteria pass, a defined terminal failure occurs, a budget is reached, progress stalls, or a human decision is required.

### Source conditional guidance from: Output and Acceptance

Return a checklist with each criterion, its evidence, and a pass/fail/blocked status. Completion is acceptable only when every mandatory criterion has passing evidence and no unreported blocking issue remains. If any required check is unavailable, say so and identify the next verification step.

### Source conditional guidance from: Stopping Rules

- Stop on failure when continued attempts cannot change the evidence or would exceed the budget.
- Stop and report uncertainty when the evidence is incomplete or contradictory.

## Output Format

### Preserved source section: Output and Acceptance

Return a checklist with each criterion, its evidence, and a pass/fail/blocked status. Completion is acceptable only when every mandatory criterion has passing evidence and no unreported blocking issue remains. If any required check is unavailable, say so and identify the next verification step.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

3. **Define thresholds.** Specify what counts as pass, fail, partial, or unknown. Avoid moving the threshold after seeing the result.
6. **Handle failures honestly.** Fix and re-check when safe. If a check cannot run, mark it blocked or unverified; do not silently treat it as passing.
7. **Apply the stop rule.** Stop when all required criteria pass, a defined terminal failure occurs, a budget is reached, progress stalls, or a human decision is required.

### Source edge/failure guidance from: Output and Acceptance

Return a checklist with each criterion, its evidence, and a pass/fail/blocked status. Completion is acceptable only when every mandatory criterion has passing evidence and no unreported blocking issue remains. If any required check is unavailable, say so and identify the next verification step.

### Source edge/failure guidance from: Stopping Rules

- Stop on failure when continued attempts cannot change the evidence or would exceed the budget.

## Stop Conditions

### Preserved source section: Stopping Rules

- Stop on success only after the agreed evidence passes.
- Stop on failure when continued attempts cannot change the evidence or would exceed the budget.
- Stop for approval before crossing a human gate.
- Stop and report uncertainty when the evidence is incomplete or contradictory.
- Never extend a loop solely to make a score look better after the user-defined budget is exhausted.

### Source stop-related guidance from: Procedure

7. **Apply the stop rule.** Stop when all required criteria pass, a defined terminal failure occurs, a budget is reached, progress stalls, or a human decision is required.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return a checklist with each criterion, its evidence, and a pass/fail/blocked status. Completion is acceptable only when every mandatory criterion has passing evidence and no unreported blocking issue remains. If any required check is unavailable, say so and identify the next verification step.
