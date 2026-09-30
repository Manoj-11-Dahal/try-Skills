---
name: continuous-learning-and-pattern-curation
description: "Use when a user asks to preserve a lesson, repeated correction, or successful workflow as reusable guidance for future tasks to turn observed evidence into a small, scoped candidate pattern, distinguish confidence from fact, and obtain approval before persistent or cross-project storage. Trigger for explicit learning, memory curation, or pattern promotion requests."
---

# Continuous Learning and Pattern Curation

## Overview

This skill applies when a user asks to preserve a lesson, repeated correction, or successful workflow as reusable guidance for future tasks. Its intended outcome is to turn observed evidence into a small, scoped candidate pattern, distinguish confidence from fact, and obtain approval before persistent or cross-project storage.

## When to Use

### Preserved source section: When to Use

Use when the user requests a durable lesson or a recurring behavior is worth proposing for future sessions. Do not silently convert ordinary conversation, personal data, or one-off assumptions into persistent memory.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

- Do not imply that a platform supports automatic memory or observation unless the current tools actually provide it.
- Never persist secrets or hidden user information.
- Do not treat one correction as universal unless the user explicitly says it is a standing preference.

### Source boundary statements from: When to Use

Use when the user requests a durable lesson or a recurring behavior is worth proposing for future sessions. Do not silently convert ordinary conversation, personal data, or one-off assumptions into persistent memory.

### Source boundary statements from: Procedure

3. **Assess repeatability and confidence.** Look for independent repetitions or explicit confirmation. Mark tentative patterns as tentative; do not turn a guess into a hard rule.
5. **Check privacy and safety.** Remove secrets, personal data, customer content, and proprietary details unless retention is explicitly authorized and necessary. Do not store raw conversation logs as a shortcut.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The observed correction, repeated workflow, or outcome and its source context.
- The intended scope: one task, one repository, a user preference, or a reusable general practice.
- The storage location, retention policy, sharing boundary, and user approval requirements.

## Instructions

### Preserved source section: Procedure

1. **Collect evidence narrowly.** Quote or summarize only relevant observations. Distinguish direct user instruction from inferred preference and from a one-time exception.
2. **Propose one atomic pattern.** State a trigger and a single action. Include an example or counterexample only if needed to disambiguate the behavior.
3. **Assess repeatability and confidence.** Look for independent repetitions or explicit confirmation. Mark tentative patterns as tentative; do not turn a guess into a hard rule.
4. **Choose the smallest scope.** Default project-specific conventions to that project. Promote a pattern globally only when it is genuinely general, useful in multiple contexts, and approved for that scope.
5. **Check privacy and safety.** Remove secrets, personal data, customer content, and proprietary details unless retention is explicitly authorized and necessary. Do not store raw conversation logs as a shortcut.
6. **Ask before persistence.** Show the proposed text, destination, scope, and retention effect. Write only after required approval; preserve unrelated memory and include provenance or review date where supported.
7. **Review and retire.** Re-check patterns when contradicted, stale, or no longer useful. Lower confidence, narrow scope, or remove them through the storage system's approved process.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

2. **Propose one atomic pattern.** State a trigger and a single action. Include an example or counterexample only if needed to disambiguate the behavior.
4. **Choose the smallest scope.** Default project-specific conventions to that project. Promote a pattern globally only when it is genuinely general, useful in multiple contexts, and approved for that scope.
5. **Check privacy and safety.** Remove secrets, personal data, customer content, and proprietary details unless retention is explicitly authorized and necessary. Do not store raw conversation logs as a shortcut.
7. **Review and retire.** Re-check patterns when contradicted, stale, or no longer useful. Lower confidence, narrow scope, or remove them through the storage system's approved process.

### Source conditional guidance from: Output and Acceptance

Return the candidate pattern, evidence basis, confidence, scope, proposed destination, and approval status. A learning is accepted only when it is useful, non-sensitive, scoped correctly, user-approved where required, and stored without changing unrelated memory.

### Source conditional guidance from: Guardrails

- Do not imply that a platform supports automatic memory or observation unless the current tools actually provide it.
- Do not treat one correction as universal unless the user explicitly says it is a standing preference.

## Output Format

### Preserved source section: Output and Acceptance

Return the candidate pattern, evidence basis, confidence, scope, proposed destination, and approval status. A learning is accepted only when it is useful, non-sensitive, scoped correctly, user-approved where required, and stored without changing unrelated memory.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

1. **Collect evidence narrowly.** Quote or summarize only relevant observations. Distinguish direct user instruction from inferred preference and from a one-time exception.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return the candidate pattern, evidence basis, confidence, scope, proposed destination, and approval status. A learning is accepted only when it is useful, non-sensitive, scoped correctly, user-approved where required, and stored without changing unrelated memory.
