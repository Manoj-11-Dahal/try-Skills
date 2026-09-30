---
name: security-evidence-lifecycle-governance
description: "Use when planning how security-control evidence and operational security logs are collected, protected, accessed, retained, and disposed to produce an evidence-lifecycle plan linking each control claim or log source to a minimal artifact, owner, classification, collection period, access rule, retention deadline, integrity check, and disposal path. Success means evidence is sufficient and traceable without collecting unrelated secrets or user records, access is least-privilege, backup and legal-hold exceptions are explicit, and disposal can be verified. This plan does not authorize testing, system changes, or disclosure."
---

# Security Evidence Lifecycle Governance

## Overview

This skill applies when planning how security-control evidence and operational security logs are collected, protected, accessed, retained, and disposed. Its intended outcome is to produce an evidence-lifecycle plan linking each control claim or log source to a minimal artifact, owner, classification, collection period, access rule, retention deadline, integrity check, and disposal path.

## When to Use

### Preserved source section: When to Use

Use this workflow for a defined security-control assessment or operational log review when the organization needs one coordinated plan for evidence collection and subsequent log/evidence handling. Keep evidence purpose, log integrity, access, retention, and disposal decisions tied to current policy and the named owner.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Workflow

2. **Plan minimal collection.** Translate each control claim into an observable artifact, owner, collection date, sample, reviewer, and integrity check. Prefer configuration exports and bounded test outcomes over unsupported attestation; do not collect secrets, unrelated records, or full system images when a smaller artifact is sufficient.
4. **Set storage and access controls.** Classify screenshots, logs, exports, packet captures, notes, and temporary credentials. Assign an approved location, least-privilege readers, encryption/integrity requirements, audit trail, and sharing restrictions. Do not store sensitive evidence in public issue trackers.
5. **Set retention and disposal.** Define purpose-based deadlines, legal-hold exceptions, backup and cache expiry, provider/support-log windows, and a verifiable disposal action. Require owner approval for exceptions; do not retain personal or content-level logs indefinitely without a policy basis.

### Source boundary statements from: Safety and Stop Conditions

Do not execute untrusted binaries or remote scripts, scan, access, modify, isolate, delete, or disclose systems without action-specific authorization. Do not reveal credentials, keys, personal data, confidential evidence, or unpatched vulnerability details to unauthorized audiences. Stop if retention authority, legal hold, data classification, log ownership, or disposal verification is unclear.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the approved organization, asset, environment, assessment or incident purpose, evidence owner, data class, relevant policy, collection period, log sources, storage systems, user roles, retention schedules, legal holds, backup behavior, and disposal method. Use read-only evidence review unless a separate authorization covers changes.

## Instructions

### Preserved source section: Workflow

1. **Confirm scope and policy.** Verify the authorization, control or incident question, applicable records schedule, data sensitivity, retention basis, and owner. Stop if evidence collection would exceed the approved purpose.
2. **Plan minimal collection.** Translate each control claim into an observable artifact, owner, collection date, sample, reviewer, and integrity check. Prefer configuration exports and bounded test outcomes over unsupported attestation; do not collect secrets, unrelated records, or full system images when a smaller artifact is sufficient.
3. **Inventory operational logs.** Document each log source, event coverage, retention duration, source clock, integrity control, storage location, access roles, provider defaults, and investigation use. Identify missing sources, excessive fields, and unapproved content-level logging.
4. **Set storage and access controls.** Classify screenshots, logs, exports, packet captures, notes, and temporary credentials. Assign an approved location, least-privilege readers, encryption/integrity requirements, audit trail, and sharing restrictions. Do not store sensitive evidence in public issue trackers.
5. **Set retention and disposal.** Define purpose-based deadlines, legal-hold exceptions, backup and cache expiry, provider/support-log windows, and a verifiable disposal action. Require owner approval for exceptions; do not retain personal or content-level logs indefinitely without a policy basis.
6. **Verify proportionately.** Check source authenticity, coverage period, sampled population, redactions, stale evidence, backup copies, collaboration links, report attachments, access history, and deletion evidence. Capture only the minimum proof needed to answer the approved question.
7. **Record and hand off.** Distinguish observed facts, assumptions, approved decisions, and unresolved policy questions. Name the reviewer and owner for each exception and schedule the next review.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs and Boundaries

Record the approved organization, asset, environment, assessment or incident purpose, evidence owner, data class, relevant policy, collection period, log sources, storage systems, user roles, retention schedules, legal holds, backup behavior, and disposal method. Use read-only evidence review unless a separate authorization covers changes.

### Source conditional guidance from: Workflow

1. **Confirm scope and policy.** Verify the authorization, control or incident question, applicable records schedule, data sensitivity, retention basis, and owner. Stop if evidence collection would exceed the approved purpose.
2. **Plan minimal collection.** Translate each control claim into an observable artifact, owner, collection date, sample, reviewer, and integrity check. Prefer configuration exports and bounded test outcomes over unsupported attestation; do not collect secrets, unrelated records, or full system images when a smaller artifact is sufficient.

### Source conditional guidance from: Safety and Stop Conditions

Do not execute untrusted binaries or remote scripts, scan, access, modify, isolate, delete, or disclose systems without action-specific authorization. Do not reveal credentials, keys, personal data, confidential evidence, or unpatched vulnerability details to unauthorized audiences. Stop if retention authority, legal hold, data classification, log ownership, or disposal verification is unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The public references below informed topic discovery only; no upstream skill text, code, commands, exploit steps, prompts, examples, or diagrams were reused. Verify current organizational policies and standards.

- [NIST SP 800-218 Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [x-glacier Kali pentest topic catalog](https://github.com/x-glacier/kali-pentest)
- [NIST Incident Response project](https://csrc.nist.gov/projects/incident-response)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

5. **Set retention and disposal.** Define purpose-based deadlines, legal-hold exceptions, backup and cache expiry, provider/support-log windows, and a verifiable disposal action. Require owner approval for exceptions; do not retain personal or content-level logs indefinitely without a policy basis.
7. **Record and hand off.** Distinguish observed facts, assumptions, approved decisions, and unresolved policy questions. Name the reviewer and owner for each exception and schedule the next review.

### Source edge/failure guidance from: Acceptance Evidence

The plan traces each control claim and log source from collection through protected storage, access, retention, and disposal. It states evidence sufficiency, integrity, access exceptions, legal holds, backup behavior, owners, and verification steps; missing evidence is not represented as proof.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not execute untrusted binaries or remote scripts, scan, access, modify, isolate, delete, or disclose systems without action-specific authorization. Do not reveal credentials, keys, personal data, confidential evidence, or unpatched vulnerability details to unauthorized audiences. Stop if retention authority, legal hold, data classification, log ownership, or disposal verification is unclear.

### Source stop-related guidance from: Workflow

1. **Confirm scope and policy.** Verify the authorization, control or incident question, applicable records schedule, data sensitivity, retention basis, and owner. Stop if evidence collection would exceed the approved purpose.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The plan traces each control claim and log source from collection through protected storage, access, retention, and disposal. It states evidence sufficiency, integrity, access exceptions, legal holds, backup behavior, owners, and verification steps; missing evidence is not represented as proof.
