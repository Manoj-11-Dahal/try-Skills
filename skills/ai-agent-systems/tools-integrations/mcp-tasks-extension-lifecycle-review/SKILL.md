---
name: mcp-tasks-extension-lifecycle-review
description: "Use when deciding whether an MCP operation needs a durable task handle because it may run for a long time, pause for input, survive disconnects, or expose meaningful progress to review Tasks-extension negotiation, task creation, status transitions, polling, input updates, cancellation, retention, and side effects. Success means clients and servers opt in explicitly, task state is recoverable within its declared lifetime, and cancellation is not misrepresented as rollback or guaranteed stop."
---

# MCP Tasks Extension Lifecycle Review

## Overview

This skill applies when deciding whether an MCP operation needs a durable task handle because it may run for a long time, pause for input, survive disconnects, or expose meaningful progress. Its intended outcome is to review Tasks-extension negotiation, task creation, status transitions, polling, input updates, cancellation, retention, and side effects.

## When to Use

### Preserved source section: When to Use

Use this workflow when an MCP server or client is considering the optional Tasks extension for long-running or resumable work. Do not use it for an ordinary request that can complete synchronously without useful progress or recovery needs.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use this workflow when an MCP server or client is considering the optional Tasks extension for long-running or resumable work. Do not use it for an ordinary request that can complete synchronously without useful progress or recovery needs.

### Source boundary statements from: Workflow

2. **Verify explicit opt-in.** Confirm the client advertises `io.modelcontextprotocol/tasks` in request capabilities and the server advertises the extension through `server/discover`. The server must not return a task result to a client that did not declare support; the client must handle either a normal result or a task result.
4. **Enforce the state machine.** Validate legal transitions among `working`, `input_required`, and terminal `completed`, `failed`, or `cancelled` states. Include the final result or error only for the appropriate terminal state; never silently rewrite a terminal status.

### Source boundary statements from: Safety and Stop Conditions

Do not expose one user’s task result to another authorization context. Do not retry non-idempotent work merely because a poll timed out. Stop if task ownership, TTL, access revocation, or the relationship between cancellation and external side effects is unspecified.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record protocol and extension revisions, client/server SDK versions, supported request methods, expected duration, job-system ID, status and result storage, TTL, suggested poll interval, authorization context, side effects, and cancellation owner. Use a non-production job or synthetic test to validate persistence and recovery.

## Instructions

### Preserved source section: Workflow

1. **Justify the task abstraction.** Identify why blocking is unsuitable: long processing, external job IDs, intermittent clients, meaningful progress, or a user-input pause. Define the synchronous result that should be produced when the job completes.
2. **Verify explicit opt-in.** Confirm the client advertises `io.modelcontextprotocol/tasks` in request capabilities and the server advertises the extension through `server/discover`. The server must not return a task result to a client that did not declare support; the client must handle either a normal result or a task result.
3. **Design durable creation.** Persist the task record and authorization context before returning a handle. Define an unguessable task ID, owner/access check, TTL, poll interval, status message limits, and behavior after process or client restart.
4. **Enforce the state machine.** Validate legal transitions among `working`, `input_required`, and terminal `completed`, `failed`, or `cancelled` states. Include the final result or error only for the appropriate terminal state; never silently rewrite a terminal status.
5. **Handle input and polling.** Keep task IDs bound to the initiating principal and request. Process `input_required` responses through the extension’s update operation, validate response keys, and make retries idempotent. Respect the polling hint; use notifications only if the extension and client support them.
6. **Specify cancellation honestly.** Define how `tasks/cancel` is acknowledged and when the worker notices it. Cancellation is cooperative: it may not stop an external job or undo an already completed side effect. Report actual job status and provide a separate authorized rollback path when available.
7. **Test recovery and expiry.** Cover duplicate submissions, lost connections, process restart, stale task IDs, expired records, authorization changes, repeated polling, cancellation races, and partial completion. Ensure logs and retained results meet the data-retention policy.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

1. **Justify the task abstraction.** Identify why blocking is unsuitable: long processing, external job IDs, intermittent clients, meaningful progress, or a user-input pause. Define the synchronous result that should be produced when the job completes.
5. **Handle input and polling.** Keep task IDs bound to the initiating principal and request. Process `input_required` responses through the extension’s update operation, validate response keys, and make retries idempotent. Respect the polling hint; use notifications only if the extension and client support them.
6. **Specify cancellation honestly.** Define how `tasks/cancel` is acknowledged and when the worker notices it. Cancellation is cooperative: it may not stop an external job or undo an already completed side effect. Report actual job status and provide a separate authorized rollback path when available.

### Source conditional guidance from: Safety and Stop Conditions

Do not expose one user’s task result to another authorization context. Do not retry non-idempotent work merely because a poll timed out. Stop if task ownership, TTL, access revocation, or the relationship between cancellation and external side effects is unspecified.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The current MCP Tasks extension and versioning references below informed topic discovery; no upstream skill text or examples were copied. Confirm host support before designing around an optional extension.

- [MCP Tasks Extension overview](https://modelcontextprotocol.io/extensions/tasks/overview)
- [MCP versioning and extension negotiation](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
- [MCP extension repository](https://github.com/modelcontextprotocol/ext-tasks)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs and Boundaries

Record protocol and extension revisions, client/server SDK versions, supported request methods, expected duration, job-system ID, status and result storage, TTL, suggested poll interval, authorization context, side effects, and cancellation owner. Use a non-production job or synthetic test to validate persistence and recovery.

### Source edge/failure guidance from: Workflow

4. **Enforce the state machine.** Validate legal transitions among `working`, `input_required`, and terminal `completed`, `failed`, or `cancelled` states. Include the final result or error only for the appropriate terminal state; never silently rewrite a terminal status.
5. **Handle input and polling.** Keep task IDs bound to the initiating principal and request. Process `input_required` responses through the extension’s update operation, validate response keys, and make retries idempotent. Respect the polling hint; use notifications only if the extension and client support them.
7. **Test recovery and expiry.** Cover duplicate submissions, lost connections, process restart, stale task IDs, expired records, authorization changes, repeated polling, cancellation races, and partial completion. Ensure logs and retained results meet the data-retention policy.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not expose one user’s task result to another authorization context. Do not retry non-idempotent work merely because a poll timed out. Stop if task ownership, TTL, access revocation, or the relationship between cancellation and external side effects is unspecified.

### Source stop-related guidance from: Workflow

1. **Justify the task abstraction.** Identify why blocking is unsuitable: long processing, external job IDs, intermittent clients, meaningful progress, or a user-input pause. Define the synchronous result that should be produced when the job completes.
6. **Specify cancellation honestly.** Define how `tasks/cancel` is acknowledged and when the worker notices it. Cancellation is cooperative: it may not stop an external job or undo an already completed side effect. Report actual job status and provide a separate authorized rollback path when available.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The result includes the extension negotiation, durable task lifecycle, state transition tests, per-principal access controls, retention/TTL behavior, progress strategy, and cancellation semantics. A returned task ID is not proof that a job will complete or that cancellation reverses its effects.
