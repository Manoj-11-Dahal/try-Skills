---
name: failure-recovery-and-replanning
description: "Use when a tool call, test, or action fails, returns ambiguous output, or does not improve the artifact to diagnose the failure, preserve known-good state, change the next attempt, bound retries, and escalate when evidence remains insufficient. Trigger for recovery, replanning, partial completion, and repeated errors in autonomous or multi-turn workflows."
---

# Failure Recovery and Replanning

## Overview

This skill applies when a tool call, test, or action fails, returns ambiguous output, or does not improve the artifact. Its intended outcome is to diagnose the failure, preserve known-good state, change the next attempt, bound retries, and escalate when evidence remains insufficient.

## When to Use

### Preserved source section: When to Use

Use this skill when an action fails, the observed result differs from the expected result, the agent repeats itself without progress, or a long-running task becomes blocked. It applies to tool errors, test failures, environmental limits, and incorrect assumptions.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

1. **Freeze risky changes.** Do not immediately retry a write or external operation if its first attempt may have partially succeeded.
6. **Choose a bounded repair.** Change one relevant variable, reduce scope, or use a safer alternative. Do not repeat an identical failing action without new information.

### Source boundary statements from: Retry Guardrails

- Do not retry authorization failures as if they were network errors.
- Do not use repeated retries to conceal missing permissions or missing user input.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The last known-good artifact or state.
- The failed action, exact tool output, logs, and relevant environment facts.
- The original objective, acceptance checks, and remaining budget.
- Any side effects that may have occurred despite an error response.

## Instructions

### Preserved source section: Procedure

1. **Freeze risky changes.** Do not immediately retry a write or external operation if its first attempt may have partially succeeded.
2. **Preserve evidence.** Save the error, command, inputs, and current state. Keep a recoverable copy or rollback path for important artifacts.
3. **Classify the failure.** Distinguish invalid input, permission denial, missing dependency, environment or network failure, tool outage, logic defect, and a wrong objective assumption.
4. **Check for partial effects.** Query the target system or inspect the filesystem before deciding what to retry.
5. **Form a changed hypothesis.** State what is believed to have failed and what evidence would distinguish that cause from alternatives.
6. **Choose a bounded repair.** Change one relevant variable, reduce scope, or use a safer alternative. Do not repeat an identical failing action without new information.
7. **Set a retry budget.** Limit retries by count, time, and cost. After the limit, stop and ask for help or report the blocker.
8. **Re-verify.** Run the original acceptance check and any regression checks. Confirm that recovery did not damage previously working state.
9. **Update durable state.** Record the root cause, attempted repair, result, and next step for later turns.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

1. **Freeze risky changes.** Do not immediately retry a write or external operation if its first attempt may have partially succeeded.

### Source conditional guidance from: Output and Acceptance

Provide a concise incident note with the failure class, evidence, partial-effect check, repair attempted, retry count, and verification result. Recovery is acceptable only when the target behavior passes its acceptance check and the known-good state remains intact; otherwise report partial or blocked status.

### Source conditional guidance from: Retry Guardrails

- Do not retry authorization failures as if they were network errors.
- If the same hypothesis fails twice, stop and choose a materially different diagnostic step.

## Output Format

### Preserved source section: Output and Acceptance

Provide a concise incident note with the failure class, evidence, partial-effect check, repair attempted, retry count, and verification result. Recovery is acceptable only when the target behavior passes its acceptance check and the known-good state remains intact; otherwise report partial or blocked status.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Preserved source section: Retry Guardrails

- Use exponential backoff only for transient failures where retrying is safe.
- Do not retry authorization failures as if they were network errors.
- Do not use repeated retries to conceal missing permissions or missing user input.
- If the same hypothesis fails twice, stop and choose a materially different diagnostic step.

### Source edge/failure guidance from: Inputs

- The failed action, exact tool output, logs, and relevant environment facts.
- Any side effects that may have occurred despite an error response.

### Source edge/failure guidance from: Procedure

2. **Preserve evidence.** Save the error, command, inputs, and current state. Keep a recoverable copy or rollback path for important artifacts.
3. **Classify the failure.** Distinguish invalid input, permission denial, missing dependency, environment or network failure, tool outage, logic defect, and a wrong objective assumption.
5. **Form a changed hypothesis.** State what is believed to have failed and what evidence would distinguish that cause from alternatives.
6. **Choose a bounded repair.** Change one relevant variable, reduce scope, or use a safer alternative. Do not repeat an identical failing action without new information.
7. **Set a retry budget.** Limit retries by count, time, and cost. After the limit, stop and ask for help or report the blocker.
8. **Re-verify.** Run the original acceptance check and any regression checks. Confirm that recovery did not damage previously working state.

### Source edge/failure guidance from: Output and Acceptance

Provide a concise incident note with the failure class, evidence, partial-effect check, repair attempted, retry count, and verification result. Recovery is acceptable only when the target behavior passes its acceptance check and the known-good state remains intact; otherwise report partial or blocked status.

## Stop Conditions

### Source stop-related guidance from: Procedure

7. **Set a retry budget.** Limit retries by count, time, and cost. After the limit, stop and ask for help or report the blocker.

### Source stop-related guidance from: Retry Guardrails

- If the same hypothesis fails twice, stop and choose a materially different diagnostic step.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Provide a concise incident note with the failure class, evidence, partial-effect check, repair attempted, retry count, and verification result. Recovery is acceptable only when the target behavior passes its acceptance check and the known-good state remains intact; otherwise report partial or blocked status.
