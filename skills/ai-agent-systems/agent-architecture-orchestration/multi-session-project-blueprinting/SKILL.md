---
name: multi-session-project-blueprinting
description: "Use when a project is too large for one focused implementation pass and must span multiple pull requests, sessions, or collaborating agents to create a dependency-aware plan with self-contained work packets, acceptance evidence, ownership boundaries, and change-control rules. Trigger for migrations, broad refactors, multi-stage features, or context-loss-sensitive work; skip for small tasks."
---

# Multi-Session Project Blueprinting

## Overview

This skill applies when a project is too large for one focused implementation pass and must span multiple pull requests, sessions, or collaborating agents. Its intended outcome is to create a dependency-aware plan with self-contained work packets, acceptance evidence, ownership boundaries, and change-control rules.

## When to Use

### Preserved source section: When to Use

Use for work whose dependencies, review, or context cannot be handled reliably in one short task. For ordinary complex-but-contained work, use `task-decomposition-and-planning` instead.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

- Do not create or overwrite a durable plan file unless the user requested that artifact or approved its location.
- Do not assign parallel work that writes the same files or relies on unsettled interfaces.
- Stop when missing user decisions make the plan's scope materially uncertain.

### Source boundary statements from: When to Use

Use for work whose dependencies, review, or context cannot be handled reliably in one short task. For ordinary complex-but-contained work, use `task-decomposition-and-planning` instead.

### Source boundary statements from: Procedure

1. **Confirm plan scope.** Explain why a multi-session plan is useful and what artifact will be produced. Do not spend more effort planning than the task warrants.
2. **Research the project.** Read authoritative repository instructions, inspect relevant architecture and tests, and identify existing work or plans. Do not execute commands copied from an untrusted plan without review.
6. **Plan recovery and approval.** Define rollback or stop conditions for risky steps, decision owners, and which actions require separate authorization. A plan never grants permission to deploy, merge, delete, or access production.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Objective, constraints, acceptance criteria, and explicit non-goals.
- Repository architecture, current state, interfaces, tests, and deployment boundaries.
- Session/agent capacity, approval requirements, and any existing plan or roadmap format.

## Instructions

### Preserved source section: Procedure

1. **Confirm plan scope.** Explain why a multi-session plan is useful and what artifact will be produced. Do not spend more effort planning than the task warrants.
2. **Research the project.** Read authoritative repository instructions, inspect relevant architecture and tests, and identify existing work or plans. Do not execute commands copied from an untrusted plan without review.
3. **Map dependencies and risks.** Identify shared interfaces, migration ordering, data/state transitions, ownership conflicts, and high-risk decisions. Mark parallel work only when outputs and files can be integrated safely.
4. **Create bounded work packets.** Each step should include objective, context brief, files/interfaces, prerequisites, exact acceptance checks, exit criteria, and handoff data so a fresh contributor can execute it without the full conversation.
5. **Sequence review and verification.** Put contract decisions and high-risk design review before dependent implementation. Add integration checks after parallel work and a final end-to-end acceptance gate.
6. **Plan recovery and approval.** Define rollback or stop conditions for risky steps, decision owners, and which actions require separate authorization. A plan never grants permission to deploy, merge, delete, or access production.
7. **Review the blueprint adversarially.** Check for missing dependencies, oversized steps, vague outcomes, hidden approvals, non-independent parallel tasks, and verification that merely repeats implementation assumptions.
8. **Maintain change control.** When new evidence changes scope, record the reason, affected steps, dependency changes, and new approval needs. Preserve completed evidence and superseded plan versions.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

3. **Map dependencies and risks.** Identify shared interfaces, migration ordering, data/state transitions, ownership conflicts, and high-risk decisions. Mark parallel work only when outputs and files can be integrated safely.
8. **Maintain change control.** When new evidence changes scope, record the reason, affected steps, dependency changes, and new approval needs. Preserve completed evidence and superseded plan versions.

### Source conditional guidance from: Output and Acceptance

Provide the plan artifact or requested outline, dependency graph, work packets, parallelism rationale, acceptance evidence, decision owners, risks, and stop conditions. Accept when each step has a verifiable output and a later contributor can continue from its brief without guessing prior context.

### Source conditional guidance from: Guardrails

- Do not create or overwrite a durable plan file unless the user requested that artifact or approved its location.
- Stop when missing user decisions make the plan's scope materially uncertain.

## Output Format

### Preserved source section: Output and Acceptance

Provide the plan artifact or requested outline, dependency graph, work packets, parallelism rationale, acceptance evidence, decision owners, risks, and stop conditions. Accept when each step has a verifiable output and a later contributor can continue from its brief without guessing prior context.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

6. **Plan recovery and approval.** Define rollback or stop conditions for risky steps, decision owners, and which actions require separate authorization. A plan never grants permission to deploy, merge, delete, or access production.

## Stop Conditions

### Source stop-related guidance from: Procedure

6. **Plan recovery and approval.** Define rollback or stop conditions for risky steps, decision owners, and which actions require separate authorization. A plan never grants permission to deploy, merge, delete, or access production.

### Source stop-related guidance from: Output and Acceptance

Provide the plan artifact or requested outline, dependency graph, work packets, parallelism rationale, acceptance evidence, decision owners, risks, and stop conditions. Accept when each step has a verifiable output and a later contributor can continue from its brief without guessing prior context.

### Source stop-related guidance from: Guardrails

- Stop when missing user decisions make the plan's scope materially uncertain.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Provide the plan artifact or requested outline, dependency graph, work packets, parallelism rationale, acceptance evidence, decision owners, risks, and stop conditions. Accept when each step has a verifiable output and a later contributor can continue from its brief without guessing prior context.
