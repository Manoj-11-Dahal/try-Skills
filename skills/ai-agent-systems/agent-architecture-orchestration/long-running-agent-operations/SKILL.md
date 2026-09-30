---
name: long-running-agent-operations
description: "Use when operating a cloud-hosted, scheduled, or continuously running agent service beyond a single interactive session to define lifecycle controls, least-privilege scopes, budgets, observability, incident actions, and rollout gates before enabling persistent autonomy. Trigger for always-on agents, background workers, or production agent fleets."
---

# Long-Running Agent Operations

## Overview

This skill applies when operating a cloud-hosted, scheduled, or continuously running agent service beyond a single interactive session. Its intended outcome is to define lifecycle controls, least-privilege scopes, budgets, observability, incident actions, and rollout gates before enabling persistent autonomy.

## When to Use

### Preserved source section: When to Use

Use for agents that run unattended, recur on schedules, serve multiple users, or retain state across tasks. A single successful CLI run does not establish operational readiness for a persistent service.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Safety Boundaries

- Never infer permission to run unattended from approval for one interactive task.
- Do not enable production credentials, public exposure, or continuous scheduling without explicit authorization.
- Treat logs, memory stores, and checkpoints as sensitive operational data.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Workload goals, runtime environment, schedule, tenant model, and service owner.
- Tool permissions, credentials, data retention, state storage, and human approval rules.
- Time/token/API budgets, retry policy, health signals, incident contacts, and rollback controls.

## Instructions

### Preserved source section: Procedure

1. **Define lifecycle authority.** Document who may start, pause, stop, restart, scale, or update the workload. Provide a tested kill switch and an owner for unattended actions.
2. **Constrain autonomy.** Use least-privilege credentials and scoped tools. Set hard limits for task duration, retries, spend, concurrency, and external writes; require approval for high-impact or ambiguous actions.
3. **Make runs recoverable.** Persist minimal task state with versioning, idempotency keys, and explicit checkpoints. Define duplicate delivery, resume, cancellation, and stale-state behavior.
4. **Instrument meaningful signals.** Record task outcomes, latency, failure classes, retries, cost, queue depth, and tool effects. Redact secrets and unnecessary user content; make traces accessible only to authorized operators.
5. **Manage change safely.** Use immutable release artifacts, staged rollout, compatibility checks for stored state, a rollback or pause plan, and explicit human sign-off for production changes.
6. **Prepare incident handling.** For a failure spike, pause expansion, capture representative traces, classify the failure, disable only the affected route when possible, apply the smallest safe fix, and resume gradually after regression checks.
7. **Run operational drills.** Test timeout, dependency outage, quota exhaustion, malformed input, repeated tool failures, stale state, and kill-switch behavior in a non-production environment.
8. **Review drift and cost.** Compare success, recovery time, retries, and cost per successful task against agreed limits. Retire capabilities or schedules that no longer provide justified value.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

6. **Prepare incident handling.** For a failure spike, pause expansion, capture representative traces, classify the failure, disable only the affected route when possible, apply the smallest safe fix, and resume gradually after regression checks.

### Source conditional guidance from: Output and Acceptance

Return the service boundary, lifecycle owner, permission map, budgets, monitoring, incident runbook, deployment gates, and drill evidence. Accept operation only when an operator can observe, pause, recover, and safely resume the workload without relying on undocumented agent behavior.

## Output Format

### Preserved source section: Output and Acceptance

Return the service boundary, lifecycle owner, permission map, budgets, monitoring, incident runbook, deployment gates, and drill evidence. Accept operation only when an operator can observe, pause, recover, and safely resume the workload without relying on undocumented agent behavior.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Constrain autonomy.** Use least-privilege credentials and scoped tools. Set hard limits for task duration, retries, spend, concurrency, and external writes; require approval for high-impact or ambiguous actions.
4. **Instrument meaningful signals.** Record task outcomes, latency, failure classes, retries, cost, queue depth, and tool effects. Redact secrets and unnecessary user content; make traces accessible only to authorized operators.
6. **Prepare incident handling.** For a failure spike, pause expansion, capture representative traces, classify the failure, disable only the affected route when possible, apply the smallest safe fix, and resume gradually after regression checks.
7. **Run operational drills.** Test timeout, dependency outage, quota exhaustion, malformed input, repeated tool failures, stale state, and kill-switch behavior in a non-production environment.
8. **Review drift and cost.** Compare success, recovery time, retries, and cost per successful task against agreed limits. Retire capabilities or schedules that no longer provide justified value.

### Source edge/failure guidance from: Output and Acceptance

Return the service boundary, lifecycle owner, permission map, budgets, monitoring, incident runbook, deployment gates, and drill evidence. Accept operation only when an operator can observe, pause, recover, and safely resume the workload without relying on undocumented agent behavior.

## Stop Conditions

### Source stop-related guidance from: Procedure

1. **Define lifecycle authority.** Document who may start, pause, stop, restart, scale, or update the workload. Provide a tested kill switch and an owner for unattended actions.
5. **Manage change safely.** Use immutable release artifacts, staged rollout, compatibility checks for stored state, a rollback or pause plan, and explicit human sign-off for production changes.
6. **Prepare incident handling.** For a failure spike, pause expansion, capture representative traces, classify the failure, disable only the affected route when possible, apply the smallest safe fix, and resume gradually after regression checks.

### Source stop-related guidance from: Output and Acceptance

Return the service boundary, lifecycle owner, permission map, budgets, monitoring, incident runbook, deployment gates, and drill evidence. Accept operation only when an operator can observe, pause, recover, and safely resume the workload without relying on undocumented agent behavior.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return the service boundary, lifecycle owner, permission map, budgets, monitoring, incident runbook, deployment gates, and drill evidence. Accept operation only when an operator can observe, pause, recover, and safely resume the workload without relying on undocumented agent behavior.
