---
name: architecture-decision-records
description: "Use when a durable technical decision changes architecture, platform, data, security, API, or operational constraints and future maintainers will need its rationale to capture context, alternatives, decision, consequences, status, and owner in the repository's existing ADR format. Trigger for material trade-offs, not routine implementation details."
---

# Architecture Decision Records

## Overview

This skill applies when a durable technical decision changes architecture, platform, data, security, API, or operational constraints and future maintainers will need its rationale. Its intended outcome is to capture context, alternatives, decision, consequences, status, and owner in the repository's existing ADR format.

## When to Use

### Preserved source section: When to Use

Use when a decision is consequential, hard to reverse, likely to be questioned later, or affects more than one component or team. Do not create an ADR for every code choice or routine refactor.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use when a decision is consequential, hard to reverse, likely to be questioned later, or affects more than one component or team. Do not create an ADR for every code choice or routine refactor.

### Source boundary statements from: Procedure

2. **Separate facts from proposals.** Record context and constraints as evidence-backed statements. Label unknowns and do not attribute a decision to a person who has not approved it.
5. **Request confirmation when needed.** If the decision is still open or the user has not authorized a durable write, present the draft and wait. A discussion or generated recommendation is not itself acceptance.
7. **Maintain lifecycle links.** Mark outdated decisions deprecated or superseded and link the replacement. Do not silently rewrite history to imply the new choice was always in effect.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The decision and the problem or constraint that makes it necessary.
- Confirmed requirements, context, alternatives considered, and relevant evidence.
- Existing ADR location, numbering scheme, naming convention, and approval process.
- Whether the user has authorized creation or modification of decision records.

## Instructions

### Preserved source section: Procedure

1. **Check existing records first.** Search the repository's ADR index and relevant project docs. If the decision is already documented, update or supersede it rather than creating a duplicate.
2. **Separate facts from proposals.** Record context and constraints as evidence-backed statements. Label unknowns and do not attribute a decision to a person who has not approved it.
3. **Draft the decision.** Use the repository's format; at minimum include title, status, date, context, decision, alternatives and reasons, consequences, and links to evidence.
4. **Capture trade-offs honestly.** Include operational, security, migration, maintenance, and compatibility costs, not only expected benefits.
5. **Request confirmation when needed.** If the decision is still open or the user has not authorized a durable write, present the draft and wait. A discussion or generated recommendation is not itself acceptance.
6. **Write safely.** Preserve existing files, assign the next valid identifier, create the record in the established location, and update the index only after approval.
7. **Maintain lifecycle links.** Mark outdated decisions deprecated or superseded and link the replacement. Do not silently rewrite history to imply the new choice was always in effect.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

1. **Check existing records first.** Search the repository's ADR index and relevant project docs. If the decision is already documented, update or supersede it rather than creating a duplicate.
5. **Request confirmation when needed.** If the decision is still open or the user has not authorized a durable write, present the draft and wait. A discussion or generated recommendation is not itself acceptance.

### Source conditional guidance from: ADR Shape

Keep the record concise enough to scan. A lightweight form is: title and status; date and decision owners; context; decision; alternatives considered; consequences and risks; references; and superseding record if applicable.

### Source conditional guidance from: Output and Acceptance

Return the draft or written path, decision status, approvals, alternatives, consequences, and index update. Accept only when the record reflects the agreed decision, preserves the existing repository convention, and does not present an unapproved proposal as accepted.

## Output Format

### Preserved source section: ADR Shape

Keep the record concise enough to scan. A lightweight form is: title and status; date and decision owners; context; decision; alternatives considered; consequences and risks; references; and superseding record if applicable.

### Preserved source section: Output and Acceptance

Return the draft or written path, decision status, approvals, alternatives, consequences, and index update. Accept only when the record reflects the agreed decision, preserves the existing repository convention, and does not present an unapproved proposal as accepted.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return the draft or written path, decision status, approvals, alternatives, consequences, and index update. Accept only when the record reflects the agreed decision, preserves the existing repository convention, and does not present an unapproved proposal as accepted.
