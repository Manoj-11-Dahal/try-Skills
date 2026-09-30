---
name: gh-aw-agent-context-lifecycle-review
description: "Use when reviewing which repository files, event payloads, and tool results an agent receives in a GitHub Actions workflow and what context is retained after it completes to produce a context-lifecycle review covering source selection, minimization, access, logging, artifacts, retention, and deletion evidence. Success means each source has a task purpose, trust boundary, owner, minimum necessary fields, approved destination, retention period, and verified disposal path or explicit exception. Use versioned configuration and synthetic or approved test data; do not modify workflows or send external data without authorization."
---

# GitHub Actions Agent Context Lifecycle Review

## Overview

This skill applies when reviewing which repository files, event payloads, and tool results an agent receives in a GitHub Actions workflow and what context is retained after it completes. Its intended outcome is to produce a context-lifecycle review covering source selection, minimization, access, logging, artifacts, retention, and deletion evidence.

## When to Use

### Preserved source section: When to Use

Use this workflow to review both sides of agent context: what enters a workflow before a run and what remains in logs, artifacts, caches, summaries, or provider systems afterward. It supports configuration review; it does not grant repository access or authorize external processing.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use this workflow to review both sides of agent context: what enters a workflow before a run and what remains in logs, artifacts, caches, summaries, or provider systems afterward. It supports configuration review; it does not grant repository access or authorize external processing.

### Source boundary statements from: Workflow

1. **Confirm authority and version.** Identify the workflow revision, event type, repository visibility, acting identity, and permitted operations. Read current configuration and authoritative documentation; do not infer effective permissions from a requested setting alone.

### Source boundary statements from: Safety and Stop Conditions

Do not upload private repository content or user-generated text to an unapproved model or service. Do not retain full repository snapshots indefinitely. Never install packages, run remote scripts, broaden permissions, expose credentials, modify production workflows, or publish external writes without explicit authorization. Stop if data ownership, legal hold, provider retention, or approval is unclear.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the workflow and action versions, repository and event scope, runtime identity, enabled tools, data classes, context sources, external model/provider destinations, retention controls, policy owner, and approval state. Keep read-only review separate from any proposed configuration change.

## Instructions

### Preserved source section: Workflow

1. **Confirm authority and version.** Identify the workflow revision, event type, repository visibility, acting identity, and permitted operations. Read current configuration and authoritative documentation; do not infer effective permissions from a requested setting alone.
2. **Map incoming context.** Inventory selected repository paths, diffs, event fields, prompts, comments, issue text, artifacts, and tool-provided records. For each source, record purpose, trust level, owner, sensitivity, and exact inclusion rule.
3. **Test minimization and boundaries.** Verify include/exclude patterns against synthetic secret-bearing, generated, binary, hidden, symlinked, oversized, and user-controlled files. Check private forks, pull-request events, untrusted branches, and path aliases without uploading private contents to an unapproved service.
4. **Trace runtime and output data.** Follow context into model requests, tool calls, logs, summaries, caches, support traces, and downloadable artifacts. Record who can read each copy, what fields are retained, and whether retries or partial runs create additional copies.
5. **Review retention and disposal.** Compare configured retention with organization policy for logs, artifacts, comments, caches, backups, provider-side records, and support data. Identify deletion windows, legal holds, backup expiry, and evidence that disposal completed.
6. **Exercise bounded failure cases.** In a test repository or synthetic fixture, confirm denied access, malformed events, timeouts, cancellations, and cleanup failures remain bounded. Preserve a concise evidence record and assign unresolved gaps to an owner.
7. **Report recommendations.** Separate observed settings, tested behavior, vendor-documented behavior, and assumptions. Propose the smallest change and obtain approval before editing or transmitting data.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Stop Conditions

Do not upload private repository content or user-generated text to an unapproved model or service. Do not retain full repository snapshots indefinitely. Never install packages, run remote scripts, broaden permissions, expose credentials, modify production workflows, or publish external writes without explicit authorization. Stop if data ownership, legal hold, provider retention, or approval is unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The public project below informed topic discovery only; no upstream skill text, code, examples, prompts, diagrams, or configuration was reused. Verify current vendor documentation and organizational policy.

- [GitHub gh-aw](https://github.com/github/gh-aw)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

4. **Trace runtime and output data.** Follow context into model requests, tool calls, logs, summaries, caches, support traces, and downloadable artifacts. Record who can read each copy, what fields are retained, and whether retries or partial runs create additional copies.
6. **Exercise bounded failure cases.** In a test repository or synthetic fixture, confirm denied access, malformed events, timeouts, cancellations, and cleanup failures remain bounded. Preserve a concise evidence record and assign unresolved gaps to an owner.

### Source edge/failure guidance from: Acceptance Evidence

The review maps each source from selection through runtime use to retention or deletion; cites the workflow revision and evidence; tests at least one denial or cleanup failure path; and names owners, exceptions, and open approvals. A successful example run alone does not prove isolation or deletion.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not upload private repository content or user-generated text to an unapproved model or service. Do not retain full repository snapshots indefinitely. Never install packages, run remote scripts, broaden permissions, expose credentials, modify production workflows, or publish external writes without explicit authorization. Stop if data ownership, legal hold, provider retention, or approval is unclear.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The review maps each source from selection through runtime use to retention or deletion; cites the workflow revision and evidence; tests at least one denial or cleanup failure path; and names owners, exceptions, and open approvals. A successful example run alone does not prove isolation or deletion.
