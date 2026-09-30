---
name: agentic-loop-design
description: "Use when a request spans multiple actions or tool calls and needs a reliable completion condition to design a bounded agent loop connecting a clear objective to an artifact, feedback signal, allowed actions, durable progress, and stopping rules. Trigger for autonomous, recurring, or multi-turn work; use a simpler single pass for small, reversible tasks."
---

# Agentic Loop Design

## Overview

This skill applies when a request spans multiple actions or tool calls and needs a reliable completion condition. Its intended outcome is to design a bounded agent loop connecting a clear objective to an artifact, feedback signal, allowed actions, durable progress, and stopping rules.

## When to Use

### Preserved source section: When to Use

Use this skill when work must make progress over several actions, evaluate intermediate results, and either continue, stop, or ask for help. Do not create a loop merely because an agent can call tools. A single response is usually better for a small, reversible task with a clear answer.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use this skill when work must make progress over several actions, evaluate intermediate results, and either continue, stop, or ask for help. Do not create a loop merely because an agent can call tools. A single response is usually better for a small, reversible task with a clear answer.

### Source boundary statements from: Procedure

4. **Observe before adapting.** After each action, inspect the actual result. Compare evidence with the signal; do not treat a successful tool exit code as proof of the objective.
7. **Apply gates and budgets.** Pause for required approval, stop on a terminal condition, and do not silently extend a retry or resource budget.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

Before designing the loop, collect or state:

- **Objective:** a user-visible outcome phrased so it can be checked.
- **Artifact:** the thing that will change or be produced, such as files, a report, a dataset, or a deployed state.
- **Feedback signal:** tests, a metric, a reviewer decision, or another observation that distinguishes better from worse.
- **Authority boundary:** actions the agent may take without further approval and actions that require a human gate.
- **Budget:** maximum iterations, time, tool calls, cost, or other resource limit.
- **State location:** where progress and evidence survive between steps or sessions.
- **Exit conditions:** success, failure, no progress, budget exhaustion, or a required approval.

If essential inputs are unknown, ask targeted questions or propose explicit safe defaults before acting.

## Instructions

### Preserved source section: Procedure

1. **Classify the work.** Decide whether it is a one-shot task, a bounded sequence, or a continuing automation. Use the least complex mode that can meet the objective.
2. **Write the loop contract.** State the objective, artifact, signal, authority boundary, budget, state location, and exit conditions in one compact plan.
3. **Make one step small.** Each iteration should produce one inspectable change or observation. Avoid combining unrelated changes because it makes the feedback hard to interpret.
4. **Observe before adapting.** After each action, inspect the actual result. Compare evidence with the signal; do not treat a successful tool exit code as proof of the objective.
5. **Keep or revert deliberately.** Retain a change only when the agreed signal supports it. Preserve the last known-good artifact when a step regresses.
6. **Record progress.** Save completed work, evidence, unresolved risks, and the next intended step in the durable state location.
7. **Apply gates and budgets.** Pause for required approval, stop on a terminal condition, and do not silently extend a retry or resource budget.
8. **Close the loop.** Summarize what changed, what was checked, what remains, and whether the exit condition was met.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs

If essential inputs are unknown, ask targeted questions or propose explicit safe defaults before acting.

### Source conditional guidance from: Procedure

5. **Keep or revert deliberately.** Retain a change only when the agreed signal supports it. Preserve the last known-good artifact when a step regresses.

### Source conditional guidance from: Output and Acceptance

Produce a short loop specification containing the objective, artifact, feedback signal, permitted actions, budget, state location, and stop rules. The design is acceptable when a different agent could follow it, each step yields an observable result, risky actions have a clear authorization boundary, and success can be determined from evidence rather than confidence.

## Output Format

### Preserved source section: Output and Acceptance

Produce a short loop specification containing the objective, artifact, feedback signal, permitted actions, budget, state location, and stop rules. The design is acceptable when a different agent could follow it, each step yields an observable result, risky actions have a clear authorization boundary, and success can be determined from evidence rather than confidence.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- **Exit conditions:** success, failure, no progress, budget exhaustion, or a required approval.

## Stop Conditions

### Source stop-related guidance from: When to Use

Use this skill when work must make progress over several actions, evaluate intermediate results, and either continue, stop, or ask for help. Do not create a loop merely because an agent can call tools. A single response is usually better for a small, reversible task with a clear answer.

### Source stop-related guidance from: Inputs

- **Exit conditions:** success, failure, no progress, budget exhaustion, or a required approval.

### Source stop-related guidance from: Procedure

2. **Write the loop contract.** State the objective, artifact, signal, authority boundary, budget, state location, and exit conditions in one compact plan.
7. **Apply gates and budgets.** Pause for required approval, stop on a terminal condition, and do not silently extend a retry or resource budget.
8. **Close the loop.** Summarize what changed, what was checked, what remains, and whether the exit condition was met.

### Source stop-related guidance from: Output and Acceptance

Produce a short loop specification containing the objective, artifact, feedback signal, permitted actions, budget, state location, and stop rules. The design is acceptable when a different agent could follow it, each step yields an observable result, risky actions have a clear authorization boundary, and success can be determined from evidence rather than confidence.

## Common Pitfalls

### Preserved source section: Common Failure Modes

- A vague objective such as “make it better” with no measurable signal.
- Repeating the same action without learning from its result.
- An unbounded loop with no cost, time, or iteration limit.
- Progress that exists only in conversational context and disappears on restart.
- Claiming completion because the final tool call succeeded, without checking the artifact.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Produce a short loop specification containing the objective, artifact, feedback signal, permitted actions, budget, state location, and stop rules. The design is acceptable when a different agent could follow it, each step yields an observable result, risky actions have a clear authorization boundary, and success can be determined from evidence rather than confidence.
