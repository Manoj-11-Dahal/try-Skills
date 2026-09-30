---
name: skill-authoring-and-maintenance
description: "Use when creating or revising a reusable agent skill for a recurring workflow to define a narrow trigger, expected inputs, ordered procedure, safety constraints, outputs, and acceptance checks; keep prose concise, separate supporting references, validate metadata and links, and check source licenses before reusing content. Trigger when instructions are repeatedly re-explained or a workflow needs consistent execution."
---

# Skill Authoring and Maintenance

## Overview

This skill applies when creating or revising a reusable agent skill for a recurring workflow. Its intended outcome is to define a narrow trigger, expected inputs, ordered procedure, safety constraints, outputs, and acceptance checks; keep prose concise, separate supporting references, validate metadata and links, and check source licenses before reusing content.

## When to Use

### Preserved source section: When to Use

Use when a repeated task would benefit from reusable instructions, an existing skill has weak triggers or unclear steps, or a skill needs maintenance after tool, policy, or platform changes.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

4. **Specify inputs and boundaries.** Identify required context, tools, permissions, trust boundaries, and approval gates. Do not imply capabilities the agent does not have.

### Source boundary statements from: Maintenance Rules

- Do not add metadata or dependencies unsupported by the target host.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The recurring task, users, context, and observed failure modes.
- Trigger phrases or conditions that distinguish when the skill applies.
- Required tools, data, constraints, acceptance criteria, and examples.
- Existing skills, repository conventions, source provenance, and license terms.

## Instructions

### Preserved source section: Procedure

1. **Confirm a real repeated need.** Identify the task the skill will improve and the cost of not having reusable guidance.
2. **Choose a narrow scope.** State what the skill does, when it applies, and when it does not. Split unrelated workflows rather than creating a broad catch-all.
3. **Write trigger metadata.** Use a descriptive, stable name and a description that states both capability and activation conditions in vocabulary users actually use.
4. **Specify inputs and boundaries.** Identify required context, tools, permissions, trust boundaries, and approval gates. Do not imply capabilities the agent does not have.
5. **Write an ordered procedure.** Make each step actionable and evidence-oriented. Include stop, escalation, and recovery paths for likely failures.
6. **Define output and acceptance.** Say what artifact or report is expected and how another person or tool can verify it.
7. **Add examples only when useful.** Use small examples that clarify ambiguous decisions; avoid duplicating the whole procedure in examples.
8. **Separate references and assets.** Keep the main skill focused. Link only to existing support files and avoid deep chains of references.
9. **Check provenance and licensing.** Write original instructions where possible. Verify permission before copying upstream material; if permission is absent or unclear, record the source and reason instead of mirroring it.
10. **Validate and maintain.** Check metadata, directory/name match, triggers, readability, size, links, tests, and real activations. Reassess stale tools, links, assumptions, and safety rules after changes.

### Preserved source section: Maintenance Rules

- Prefer small, reviewable updates over rewriting working guidance without evidence.
- Do not add metadata or dependencies unsupported by the target host.
- Preserve working user content and existing skills; use an explicit update process for replacements.
- Keep evaluation cases aligned with the actual trigger and acceptance criteria.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs

- Trigger phrases or conditions that distinguish when the skill applies.

### Source conditional guidance from: Procedure

2. **Choose a narrow scope.** State what the skill does, when it applies, and when it does not. Split unrelated workflows rather than creating a broad catch-all.
7. **Add examples only when useful.** Use small examples that clarify ambiguous decisions; avoid duplicating the whole procedure in examples.
9. **Check provenance and licensing.** Write original instructions where possible. Verify permission before copying upstream material; if permission is absent or unclear, record the source and reason instead of mirroring it.

### Source conditional guidance from: Output and Acceptance

Deliver a standalone skill with clear activation, inputs, procedure, output, and safety criteria, plus source notes for any external material. The skill is acceptable when its trigger is distinguishable from neighboring skills, its steps can be followed, its internal links work, and its claims and dependencies are current.

## Output Format

### Preserved source section: Output and Acceptance

Deliver a standalone skill with clear activation, inputs, procedure, output, and safety criteria, plus source notes for any external material. The skill is acceptable when its trigger is distinguishable from neighboring skills, its steps can be followed, its internal links work, and its claims and dependencies are current.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- The recurring task, users, context, and observed failure modes.

### Source edge/failure guidance from: Procedure

5. **Write an ordered procedure.** Make each step actionable and evidence-oriented. Include stop, escalation, and recovery paths for likely failures.

## Stop Conditions

### Source stop-related guidance from: Procedure

5. **Write an ordered procedure.** Make each step actionable and evidence-oriented. Include stop, escalation, and recovery paths for likely failures.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Deliver a standalone skill with clear activation, inputs, procedure, output, and safety criteria, plus source notes for any external material. The skill is acceptable when its trigger is distinguishable from neighboring skills, its steps can be followed, its internal links work, and its claims and dependencies are current.
