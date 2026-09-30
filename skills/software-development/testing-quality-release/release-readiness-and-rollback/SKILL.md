---
name: release-readiness-and-rollback
description: "Use when preparing a software change for a staged rollout, production release, or deployment decision to check required quality gates, compatibility, operational signals, approvals, and a credible rollback or recovery path. Trigger for release planning and go/no-go reviews; this skill does not itself authorize publishing or deployment."
---

# Release Readiness and Rollback

## Overview

This skill applies when preparing a software change for a staged rollout, production release, or deployment decision. Its intended outcome is to check required quality gates, compatibility, operational signals, approvals, and a credible rollback or recovery path.

## When to Use

### Preserved source section: When to Use

Use this skill to assess whether a release is prepared and how to limit impact if it fails. Apply it before a deployment decision, including changes with database migrations, external dependencies, security effects, or user-visible behavior.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Approval and Safety Boundaries

- Do not deploy, publish, change production settings, or trigger a release merely because the checklist is complete.
- Obtain explicit authorization for the specific environment and action before execution.
- Stop if rollback would risk data loss, user harm, or an irreversible external commitment that has not been reviewed.
- Report a blocked or conditional status honestly; do not convert missing evidence into a pass.

### Source boundary statements from: Procedure

4. **Plan exposure control.** Specify staged cohorts, feature-flag defaults, traffic or user thresholds, observation intervals, and who can pause expansion. Do not assume a flag is a rollback if it cannot reverse persisted side effects.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The release candidate, change summary, target environment, and intended audience.
- Required tests, security checks, approvals, and service-level expectations.
- Deployment method, feature flags, migration behavior, monitoring, and incident contacts.
- An explicit statement of who may execute or approve the release.

## Instructions

### Preserved source section: Procedure

1. **Define the release boundary.** Identify the exact artifact/version, environment, users affected, and intended time or rollout window. Separate readiness assessment from deployment execution.
2. **Check release evidence.** Review required tests, build/package integrity, configuration, dependency changes, security findings, documentation, and known limitations. Mark each gate pass, fail, blocked, or not applicable with evidence.
3. **Assess compatibility and data risk.** Examine API/client compatibility, schema changes, backfills, irreversible transformations, ordering constraints, and whether old and new versions can coexist during rollout.
4. **Plan exposure control.** Specify staged cohorts, feature-flag defaults, traffic or user thresholds, observation intervals, and who can pause expansion. Do not assume a flag is a rollback if it cannot reverse persisted side effects.
5. **Define health and abort signals.** Name the metrics, logs, user-visible symptoms, and thresholds that would pause or stop rollout. Ensure someone can observe them during the release window.
6. **Prove the recovery path.** Identify how to disable, roll back, or forward-fix the change; what data is preserved; and any manual recovery steps. Validate the plan in a safe environment when feasible.
7. **Make a go/no-go recommendation.** List blocking gaps, residual risks, required approvals, and the conditions for proceeding. If evidence is incomplete, recommend hold or explicitly conditional approval.
8. **Preserve post-release follow-up.** If release execution is authorized, track actual rollout state, health signals, incidents, and completion criteria; otherwise stop at the readiness report.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

4. **Plan exposure control.** Specify staged cohorts, feature-flag defaults, traffic or user thresholds, observation intervals, and who can pause expansion. Do not assume a flag is a rollback if it cannot reverse persisted side effects.
6. **Prove the recovery path.** Identify how to disable, roll back, or forward-fix the change; what data is preserved; and any manual recovery steps. Validate the plan in a safe environment when feasible.
7. **Make a go/no-go recommendation.** List blocking gaps, residual risks, required approvals, and the conditions for proceeding. If evidence is incomplete, recommend hold or explicitly conditional approval.
8. **Preserve post-release follow-up.** If release execution is authorized, track actual rollout state, health signals, incidents, and completion criteria; otherwise stop at the readiness report.

### Source conditional guidance from: Approval and Safety Boundaries

- Stop if rollback would risk data loss, user harm, or an irreversible external commitment that has not been reviewed.

## Output Format

### Preserved source section: Go/No-Go Output

Return the artifact/version and environment, gate checklist with evidence, rollout and monitoring plan, rollback/recovery steps, unresolved risks, decision owner, and recommendation. A go recommendation requires all mandatory gates to pass and a usable recovery path for material failure modes.

## Validation Checklist

Not specified in source skill.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Check release evidence.** Review required tests, build/package integrity, configuration, dependency changes, security findings, documentation, and known limitations. Mark each gate pass, fail, blocked, or not applicable with evidence.
6. **Prove the recovery path.** Identify how to disable, roll back, or forward-fix the change; what data is preserved; and any manual recovery steps. Validate the plan in a safe environment when feasible.

### Source edge/failure guidance from: Go/No-Go Output

Return the artifact/version and environment, gate checklist with evidence, rollout and monitoring plan, rollback/recovery steps, unresolved risks, decision owner, and recommendation. A go recommendation requires all mandatory gates to pass and a usable recovery path for material failure modes.

## Stop Conditions

### Source stop-related guidance from: Procedure

4. **Plan exposure control.** Specify staged cohorts, feature-flag defaults, traffic or user thresholds, observation intervals, and who can pause expansion. Do not assume a flag is a rollback if it cannot reverse persisted side effects.
5. **Define health and abort signals.** Name the metrics, logs, user-visible symptoms, and thresholds that would pause or stop rollout. Ensure someone can observe them during the release window.
8. **Preserve post-release follow-up.** If release execution is authorized, track actual rollout state, health signals, incidents, and completion criteria; otherwise stop at the readiness report.

### Source stop-related guidance from: Approval and Safety Boundaries

- Stop if rollback would risk data loss, user harm, or an irreversible external commitment that has not been reviewed.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

Not specified in source skill.
