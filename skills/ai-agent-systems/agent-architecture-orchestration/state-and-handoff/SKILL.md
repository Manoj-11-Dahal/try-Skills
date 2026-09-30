---
name: state-and-handoff
description: "Use when work spans sessions, runs, agents, or context windows and progress must survive handoffs to record the objective, current state, decisions, evidence, unresolved risks, next action, and stopping rule in a durable artifact; verify freshness before resuming. Trigger for asynchronous, unattended, delegated, or long-running agent workflows."
---

# State and Handoff

## Overview

This skill applies when work spans sessions, runs, agents, or context windows and progress must survive handoffs. Its intended outcome is to record the objective, current state, decisions, evidence, unresolved risks, next action, and stopping rule in a durable artifact; verify freshness before resuming.

## When to Use

### Preserved source section: When to Use

Use this skill whenever the work may outlive the current turn, be delegated to another agent, resume after a failure, or depend on information that will not reliably remain in conversational context.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

4. **Keep a trace.** Append consequential actions and observations to an ordered ledger. Do not rewrite history to make an unsuccessful step appear successful.
7. **Handoff explicitly.** Tell the next agent what is safe to do, what requires approval, what must not be repeated, and which checks remain.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The current objective and success condition.
- The durable state location and any access or privacy constraints.
- Completed actions, artifacts, observations, and decisions.
- Pending actions, open questions, risks, and resource limits.

## Instructions

### Preserved source section: Procedure

1. **Read before resuming.** Load the existing checkpoint and verify that it belongs to the current task, target, and version of the artifact.
2. **Separate fact from intent.** Mark completed work with evidence. Keep proposed actions, assumptions, and unresolved questions in separate fields.
3. **Write a compact checkpoint.** Include objective, scope, current artifact locations, completed steps, verification results, decisions, blockers, remaining budget, next action, and stop conditions.
4. **Keep a trace.** Append consequential actions and observations to an ordered ledger. Do not rewrite history to make an unsuccessful step appear successful.
5. **Protect sensitive data.** Store only the minimum information needed. Redact secrets, tokens, personal data, and private payloads from summaries and logs.
6. **Update atomically.** Use a temporary file or transactional update when possible, then verify the saved checkpoint can be read back.
7. **Handoff explicitly.** Tell the next agent what is safe to do, what requires approval, what must not be repeated, and which checks remain.
8. **Revalidate freshness.** Before acting on an old checkpoint, inspect the target state for intervening changes and revise the plan if necessary.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

6. **Update atomically.** Use a temporary file or transactional update when possible, then verify the saved checkpoint can be read back.
8. **Revalidate freshness.** Before acting on an old checkpoint, inspect the target state for intervening changes and revise the plan if necessary.

### Source conditional guidance from: Output and Acceptance

Produce a concise durable checkpoint and a short handoff summary. The handoff is acceptable when another agent can identify the current objective, verified state, unresolved risks, next safe step, required approvals, and exact stopping conditions without relying on hidden conversational context.

## Output Format

### Preserved source section: Output and Acceptance

Produce a concise durable checkpoint and a short handoff summary. The handoff is acceptable when another agent can identify the current objective, verified state, unresolved risks, next safe step, required approvals, and exact stopping conditions without relying on hidden conversational context.

### Preserved source section: Checkpoint Template

Use a project-appropriate file with fields equivalent to:

- Objective and acceptance criteria
- Current artifact or target state
- Completed actions and evidence
- Decisions and assumptions
- Pending questions and risks
- Budget remaining
- Next safe action
- Human approvals required
- Stop conditions

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Stop Conditions

### Source stop-related guidance from: Procedure

3. **Write a compact checkpoint.** Include objective, scope, current artifact locations, completed steps, verification results, decisions, blockers, remaining budget, next action, and stop conditions.

### Source stop-related guidance from: Output and Acceptance

Produce a concise durable checkpoint and a short handoff summary. The handoff is acceptable when another agent can identify the current objective, verified state, unresolved risks, next safe step, required approvals, and exact stopping conditions without relying on hidden conversational context.

### Source stop-related guidance from: Checkpoint Template

- Stop conditions

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Produce a concise durable checkpoint and a short handoff summary. The handoff is acceptable when another agent can identify the current objective, verified state, unresolved risks, next safe step, required approvals, and exact stopping conditions without relying on hidden conversational context.
