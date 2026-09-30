---
name: agent-loop-budgeting-and-observability
description: "Use when an agent loop can consume variable time, tool calls, money, tokens, or external quota to set explicit limits and progress signals, monitor them per iteration, detect churn or plateau, and stop or ask before crossing budgets. Trigger for unattended, recurring, multi-agent, or open-ended tasks where cost or runaway behavior matters."
---

# Agent Loop Budgeting and Observability

## Overview

This skill applies when an agent loop can consume variable time, tool calls, money, tokens, or external quota. Its intended outcome is to set explicit limits and progress signals, monitor them per iteration, detect churn or plateau, and stop or ask before crossing budgets.

## When to Use

### Preserved source section: When to Use

Use before starting unattended, recurring, multi-agent, or open-ended work whose time, tool usage, financial cost, or external quota could grow unpredictably.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

8. **Review after the run.** Compare expected and actual cost, time, and progress. Tune future limits only with evidence; do not weaken acceptance checks just to fit a budget.

### Source boundary statements from: Stop Conditions

- Never hide a budget overrun or report activity as progress without evidence.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Objective, artifact, feedback signal, and success threshold.
- Available budget for time, iterations, tool calls, tokens, money, or API quota.
- Progress indicators and logs that can be collected safely.
- Conditions that require a pause, approval, or escalation.

## Instructions

### Preserved source section: Procedure

1. **Set hard limits.** Define maximum elapsed time, iterations, tool calls, and spend where measurable. Add a safety margin for cleanup and verification.
2. **Choose leading indicators.** Track useful changes per iteration, not just activity. Examples include passing checks, verified claims, completed subtasks, or artifact quality against a fixed rubric.
3. **Instrument each cycle.** Record start/end time, action, result, budget consumed, progress signal, and remaining allowance. Avoid logging secrets or unnecessary personal data.
4. **Check for churn.** Detect repeated errors, no-op edits, unchanged scores, growing scope, duplicated agent work, or rising cost without corresponding progress.
5. **Adjust safely.** Reduce parallelism, narrow scope, lower frequency, or switch to a cheaper diagnostic when the progress signal stalls.
6. **Warn before thresholds.** Notify the user or controller before a soft budget is reached. Stop before a hard budget or external quota is exceeded.
7. **Reserve exit capacity.** Keep enough budget to save state, run final checks, undo unsafe changes, and report accurately.
8. **Review after the run.** Compare expected and actual cost, time, and progress. Tune future limits only with evidence; do not weaken acceptance checks just to fit a budget.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

5. **Adjust safely.** Reduce parallelism, narrow scope, lower frequency, or switch to a cheaper diagnostic when the progress signal stalls.

### Source conditional guidance from: Output and Acceptance

Return a budget contract, progress metrics, alert thresholds, hard stop rules, and a short run summary showing consumption and verified progress. The loop is acceptable when it can halt before exhaustion and leave the artifact in a safe, inspectable state.

### Source conditional guidance from: Stop Conditions

- Stop early when the objective is verified or the progress signal plateaus beyond the agreed threshold.
- Pause for approval if scope or spending changes materially.

## Output Format

### Preserved source section: Output and Acceptance

Return a budget contract, progress metrics, alert thresholds, hard stop rules, and a short run summary showing consumption and verified progress. The loop is acceptable when it can halt before exhaustion and leave the artifact in a safe, inspectable state.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

4. **Check for churn.** Detect repeated errors, no-op edits, unchanged scores, growing scope, duplicated agent work, or rising cost without corresponding progress.

## Stop Conditions

### Preserved source section: Stop Conditions

- Stop at the hard time, cost, iteration, or tool-call limit.
- Stop early when the objective is verified or the progress signal plateaus beyond the agreed threshold.
- Pause for approval if scope or spending changes materially.
- Never hide a budget overrun or report activity as progress without evidence.

### Source stop-related guidance from: Inputs

- Conditions that require a pause, approval, or escalation.

### Source stop-related guidance from: Procedure

6. **Warn before thresholds.** Notify the user or controller before a soft budget is reached. Stop before a hard budget or external quota is exceeded.

### Source stop-related guidance from: Output and Acceptance

Return a budget contract, progress metrics, alert thresholds, hard stop rules, and a short run summary showing consumption and verified progress. The loop is acceptable when it can halt before exhaustion and leave the artifact in a safe, inspectable state.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return a budget contract, progress metrics, alert thresholds, hard stop rules, and a short run summary showing consumption and verified progress. The loop is acceptable when it can halt before exhaustion and leave the artifact in a safe, inspectable state.
