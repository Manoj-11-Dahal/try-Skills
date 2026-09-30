---
name: task-decomposition-and-planning
description: "Use when a goal is too large or ambiguous to complete safely in one pass and must be broken into a sequence of verifiable tasks to identify dependencies, risks, owners, and acceptance checks; prioritize a thin path to evidence and keep scope controlled. Trigger at project starts, complex changes, or when parallel work needs a clear plan."
---

# Task Decomposition and Planning

## Overview

This skill applies when a goal is too large or ambiguous to complete safely in one pass and must be broken into a sequence of verifiable tasks. Its intended outcome is to identify dependencies, risks, owners, and acceptance checks; prioritize a thin path to evidence and keep scope controlled.

## When to Use

### Preserved source section: When to Use

Use this skill before acting on a large, multi-step, underspecified, or dependency-heavy request. It is also useful when several agents may work in parallel or when scope changes during execution.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Planning Guardrails

- Do not confuse a detailed task list with evidence of progress.
- Do not split work so finely that coordination costs exceed the benefit.
- Do not parallelize writes to a shared artifact without isolation and merge ownership.
- Revisit the plan when evidence changes; do not continue merely because work was scheduled.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- User's desired outcome, constraints, and deadlines.
- Current project state, relevant instructions, and known dependencies.
- Available tools, people or agents, and resource limits.
- Acceptance evidence for the final outcome and each important milestone.

## Instructions

### Preserved source section: Procedure

1. **Restate the outcome.** Describe what should be observably true at completion. Separate requirements from preferences and assumptions.
2. **Inspect the baseline.** Read the relevant project instructions and inspect the existing artifact before proposing large changes.
3. **Identify unknowns.** Ask only the questions that can change scope, safety, or architecture. For lower-risk gaps, state conservative assumptions.
4. **Decompose into vertical increments.** Make each task small enough to produce a testable artifact or decision. Avoid planning only by file or department when end-to-end outcomes are more useful.
5. **Map dependencies.** Represent prerequisites and shared resources. Mark tasks parallelizable only when their inputs and write ownership are independent.
6. **Attach acceptance checks.** For each task, specify a command, observation, citation, reviewer decision, or other evidence that can determine pass, fail, or blocked.
7. **Sequence by risk and learning.** Do reversible discovery early; delay irreversible or costly decisions until evidence is available.
8. **Set boundaries.** Define what is in scope, out of scope, delegated, approval-gated, and limited by budget or time.
9. **Publish the plan.** Show milestones, dependencies, owners, risks, and stop conditions. Ask for confirmation when a tradeoff or high-impact scope choice belongs to the user.
10. **Replan transparently.** When new evidence changes the plan, record why, preserve completed work, and update only affected dependencies.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

4. **Decompose into vertical increments.** Make each task small enough to produce a testable artifact or decision. Avoid planning only by file or department when end-to-end outcomes are more useful.
5. **Map dependencies.** Represent prerequisites and shared resources. Mark tasks parallelizable only when their inputs and write ownership are independent.
9. **Publish the plan.** Show milestones, dependencies, owners, risks, and stop conditions. Ask for confirmation when a tradeoff or high-impact scope choice belongs to the user.
10. **Replan transparently.** When new evidence changes the plan, record why, preserve completed work, and update only affected dependencies.

### Source conditional guidance from: Output and Acceptance

Return a prioritized plan with a testable outcome, ordered tasks, dependencies, owners or agents, acceptance checks, risks, budget, and stop conditions. The plan is acceptable when each task can be started and verified independently, parallel work has clear boundaries, and no hidden assumption changes the requested scope.

### Source conditional guidance from: Planning Guardrails

- Revisit the plan when evidence changes; do not continue merely because work was scheduled.

## Output Format

### Preserved source section: Output and Acceptance

Return a prioritized plan with a testable outcome, ordered tasks, dependencies, owners or agents, acceptance checks, risks, budget, and stop conditions. The plan is acceptable when each task can be started and verified independently, parallel work has clear boundaries, and no hidden assumption changes the requested scope.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

6. **Attach acceptance checks.** For each task, specify a command, observation, citation, reviewer decision, or other evidence that can determine pass, fail, or blocked.

## Stop Conditions

### Source stop-related guidance from: Procedure

9. **Publish the plan.** Show milestones, dependencies, owners, risks, and stop conditions. Ask for confirmation when a tradeoff or high-impact scope choice belongs to the user.

### Source stop-related guidance from: Output and Acceptance

Return a prioritized plan with a testable outcome, ordered tasks, dependencies, owners or agents, acceptance checks, risks, budget, and stop conditions. The plan is acceptable when each task can be started and verified independently, parallel work has clear boundaries, and no hidden assumption changes the requested scope.

### Source stop-related guidance from: Planning Guardrails

- Revisit the plan when evidence changes; do not continue merely because work was scheduled.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return a prioritized plan with a testable outcome, ordered tasks, dependencies, owners or agents, acceptance checks, risks, budget, and stop conditions. The plan is acceptable when each task can be started and verified independently, parallel work has clear boundaries, and no hidden assumption changes the requested scope.
