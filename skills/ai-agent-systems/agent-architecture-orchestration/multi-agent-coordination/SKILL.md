---
name: multi-agent-coordination
description: "Use when two or more agents, subagents, or workers must contribute to a shared objective to define bounded roles, artifact ownership, interfaces, isolated work areas, message cadence, integration checks, and a responsible coordinator. Trigger for parallel research or implementation; do not parallelize tightly coupled edits without explicit ownership and merge rules."
---

# Multi-Agent Coordination

## Overview

This skill applies when two or more agents, subagents, or workers must contribute to a shared objective. Its intended outcome is to define bounded roles, artifact ownership, interfaces, isolated work areas, message cadence, integration checks, and a responsible coordinator.

## When to Use

### Preserved source section: When to Use

Use when work can benefit from parallel expertise or independent investigation. Do not add agents to a small task whose coordination overhead is likely to exceed the work itself.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use when work can benefit from parallel expertise or independent investigation. Do not add agents to a small task whose coordination overhead is likely to exceed the work itself.

### Source boundary statements from: Procedure

5. **Share only necessary context.** Provide authoritative instructions and task-specific inputs. Do not expose secrets or unrelated personal data.
7. **Integrate explicitly.** The coordinator reviews outputs, resolves conflicts, checks compatibility, and runs end-to-end verification. Do not merge based only on agent confidence.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Shared goal and acceptance criteria.
- Candidate subtasks, dependencies, and expected deliverables.
- Available agents, tools, context, and execution boundaries.
- Shared files, systems, and any approval or confidentiality rules.

## Instructions

### Preserved source section: Procedure

1. **Choose parallelism deliberately.** Split only work with separable inputs or independently verifiable outcomes. Keep tightly coupled decisions with one owner.
2. **Assign bounded roles.** Give each agent one objective, scope, output format, and explicit non-goals. Avoid vague assignments such as “look into everything.”
3. **Set artifact ownership.** Name the files, branches, data, or resources each worker may change. Use isolated worktrees or separate copies for concurrent writes.
4. **Define interfaces first.** Specify assumptions, schemas, naming, and handoff format so parallel results can fit together.
5. **Share only necessary context.** Provide authoritative instructions and task-specific inputs. Do not expose secrets or unrelated personal data.
6. **Set checkpoints.** Request concise status at agreed milestones: completed, evidence, blockers, next step, and any changed assumptions.
7. **Integrate explicitly.** The coordinator reviews outputs, resolves conflicts, checks compatibility, and runs end-to-end verification. Do not merge based only on agent confidence.
8. **Use independent review.** For consequential work, assign a reviewer who did not author the change and give them the acceptance criteria, not just the implementation summary.
9. **Stop and reassign when needed.** If a worker is blocked, duplicate, or over budget, narrow or reassign the task rather than allowing silent drift.
10. **Close the team.** Record ownership transfer, final evidence, unresolved items, and stop each worker when its contribution is complete.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

9. **Stop and reassign when needed.** If a worker is blocked, duplicate, or over budget, narrow or reassign the task rather than allowing silent drift.
10. **Close the team.** Record ownership transfer, final evidence, unresolved items, and stop each worker when its contribution is complete.

### Source conditional guidance from: Output and Acceptance

Provide a coordination plan with role assignments, ownership boundaries, interfaces, checkpoints, integration owner, and final checks. Accept the result only when the combined artifact passes its shared acceptance criteria and no unreviewed cross-agent conflict remains.

### Source conditional guidance from: Coordination Risks

- A coordinator treating parallel opinions as independent evidence when they share the same assumptions.

## Output Format

### Preserved source section: Output and Acceptance

Provide a coordination plan with role assignments, ownership boundaries, interfaces, checkpoints, integration owner, and final checks. Accept the result only when the combined artifact passes its shared acceptance criteria and no unreviewed cross-agent conflict remains.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Preserved source section: Coordination Risks

- Duplicate work caused by overlapping prompts.
- Conflicting writes to shared files or external systems.
- A coordinator treating parallel opinions as independent evidence when they share the same assumptions.
- Missing integration work after every individual subtask reports success.

## Stop Conditions

### Source stop-related guidance from: Procedure

9. **Stop and reassign when needed.** If a worker is blocked, duplicate, or over budget, narrow or reassign the task rather than allowing silent drift.
10. **Close the team.** Record ownership transfer, final evidence, unresolved items, and stop each worker when its contribution is complete.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Provide a coordination plan with role assignments, ownership boundaries, interfaces, checkpoints, integration owner, and final checks. Accept the result only when the combined artifact passes its shared acceptance criteria and no unreviewed cross-agent conflict remains.
