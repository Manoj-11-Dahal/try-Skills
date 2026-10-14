---
name: security-assessment-scope-authorization-register
description: "Use when preparing for and governing a bounded security assessment, to establish written authorization and maintain explicit in-scope assets, prohibited methods, and exclusions to produce a reviewable scope register linked to the approval packet. Success means each target, account, environment, date, test type, source address, data boundary, exclusion, owner, and expiry is explicit; aliases and redirects are checked against exclusions before activity. Public reachability or generic intent is not authorization. Do not perform active testing or production changes without owner approval."
---

# Security Assessment Scope and Authorization Register

## Overview

This skill applies when preparing for and governing a bounded security assessment, to establish written authorization and maintain explicit in-scope assets, prohibited methods, and exclusions. Its intended outcome is to produce a reviewable scope register linked to the approval packet.

## When to Use

### Preserved source section: When to Use

Use this workflow to prepare the written authorization packet and keep its boundaries enforceable during a security assessment. It is administrative scope control, not permission to probe, exploit, alter, or disclose any system beyond the named approval.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Workflow

1. **Verify authority.** Confirm written approval from the accountable owner, assessment purpose, permitted actions, start/end time, emergency stop contact, and revocation process. Never infer permission from public reachability, title, or a generic statement of intent.
4. **Resolve target ambiguity.** Check wildcard interpretation, DNS and asset aliases, redirects, acquired subsidiaries, shared cloud infrastructure, and third-party dependencies. Any target that cannot be resolved against the approval and exclusion set remains out of scope.

### Source boundary statements from: Safety and Stop Conditions

Do not treat an exclusion as optional or silently expand scope to neighboring assets. Do not execute untrusted binaries or remote scripts, access customer data, scan, modify, isolate, delete, or disclose a target without explicit authorization for that action and environment. Stop if ownership, authorization, scope, expiry, or recovery responsibility is unclear.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the organization, asset owner, exact targets, environment, authorized test types, dates and expiry, source addresses, permitted data, prohibited methods, escalation contact, recovery owner, and approving authority. Include explicit exclusions for hosts, paths, accounts, customer data, third-party services, and methods.

## Instructions

### Preserved source section: Workflow

1. **Verify authority.** Confirm written approval from the accountable owner, assessment purpose, permitted actions, start/end time, emergency stop contact, and revocation process. Never infer permission from public reachability, title, or a generic statement of intent.
2. **Build the in-scope register.** List exact domains, IP ranges, cloud accounts, APIs, applications, identity tenants, and physical boundaries. Link each permission to the system boundary it covers and name its owner.
3. **Record exclusions.** Create a human-readable and machine-readable exclusion list for out-of-scope hosts, paths, accounts, data classes, shared resources, and test methods. Mark exclusions as mandatory, not advisory.
4. **Resolve target ambiguity.** Check wildcard interpretation, DNS and asset aliases, redirects, acquired subsidiaries, shared cloud infrastructure, and third-party dependencies. Any target that cannot be resolved against the approval and exclusion set remains out of scope.
5. **Revalidate during the assessment.** Recheck expiry, ownership, asset changes, new redirects, and scope amendments before each active phase. Record who approved any change and which version of the register applies.
6. **Close and hand off.** Record tests performed, stop events, evidence location, cleanup, unresolved exceptions, and the next review date. Separate observations from approvals and decisions.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Stop Conditions

Do not treat an exclusion as optional or silently expand scope to neighboring assets. Do not execute untrusted binaries or remote scripts, access customer data, scan, modify, isolate, delete, or disclose a target without explicit authorization for that action and environment. Stop if ownership, authorization, scope, expiry, or recovery responsibility is unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The public project below informed topic discovery only; no upstream skill text, commands, exploit steps, prompts, examples, or diagrams were reused. Verify current organizational policy.

- [x-glacier Kali pentest topic catalog](https://github.com/x-glacier/kali-pentest)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs and Boundaries

Record the organization, asset owner, exact targets, environment, authorized test types, dates and expiry, source addresses, permitted data, prohibited methods, escalation contact, recovery owner, and approving authority. Include explicit exclusions for hosts, paths, accounts, customer data, third-party services, and methods.

### Source edge/failure guidance from: Workflow

6. **Close and hand off.** Record tests performed, stop events, evidence location, cleanup, unresolved exceptions, and the next review date. Separate observations from approvals and decisions.

### Source edge/failure guidance from: Safety and Stop Conditions

Do not treat an exclusion as optional or silently expand scope to neighboring assets. Do not execute untrusted binaries or remote scripts, access customer data, scan, modify, isolate, delete, or disclose a target without explicit authorization for that action and environment. Stop if ownership, authorization, scope, expiry, or recovery responsibility is unclear.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not treat an exclusion as optional or silently expand scope to neighboring assets. Do not execute untrusted binaries or remote scripts, access customer data, scan, modify, isolate, delete, or disclose a target without explicit authorization for that action and environment. Stop if ownership, authorization, scope, expiry, or recovery responsibility is unclear.

### Source stop-related guidance from: Inputs and Boundaries

Record the organization, asset owner, exact targets, environment, authorized test types, dates and expiry, source addresses, permitted data, prohibited methods, escalation contact, recovery owner, and approving authority. Include explicit exclusions for hosts, paths, accounts, customer data, third-party services, and methods.

### Source stop-related guidance from: Workflow

1. **Verify authority.** Confirm written approval from the accountable owner, assessment purpose, permitted actions, start/end time, emergency stop contact, and revocation process. Never infer permission from public reachability, title, or a generic statement of intent.
6. **Close and hand off.** Record tests performed, stop events, evidence location, cleanup, unresolved exceptions, and the next review date. Separate observations from approvals and decisions.

### Source stop-related guidance from: Acceptance Evidence

The packet contains a dated approval, named owner, exact scope, explicit exclusions, allowed and prohibited methods, expiry, escalation path, and version history. A reviewer can reproduce the target-selection decision without relying on informal assumptions.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The packet contains a dated approval, named owner, exact scope, explicit exclusions, allowed and prohibited methods, expiry, escalation path, and version history. A reviewer can reproduce the target-selection decision without relying on informal assumptions.
