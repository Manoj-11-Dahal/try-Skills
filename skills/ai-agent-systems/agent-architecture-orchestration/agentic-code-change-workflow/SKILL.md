---
name: agentic-code-change-workflow
description: "Use when an agent is asked to modify code, add a feature, fix a bug, or change configuration in a repository to establish scope, inspect project conventions, plan a small change, implement with relevant tests, review the diff, and verify before reporting. Trigger for multi-file edits, behavior changes, or production-impacting fixes; gate commits and deployments separately."
---

# Agentic Code Change Workflow

## Overview

This skill applies when an agent is asked to modify code, add a feature, fix a bug, or change configuration in a repository. Its intended outcome is to establish scope, inspect project conventions, plan a small change, implement with relevant tests, review the diff, and verify before reporting.

## When to Use

### Preserved source section: When to Use

Use when an agent must change a codebase, configuration, tests, or documentation that affects software behavior. For a one-line typo with obvious scope, use only the relevant lightweight checks.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

1. **Inspect before editing.** Read applicable agent and project instructions, inspect the working tree, and locate the existing behavior. Do not overwrite unrelated user changes.
10. **Gate shipping actions.** Do not commit, push, publish, or deploy unless the user authorized that exact action and the relevant checks pass.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- User's requested behavior, constraints, and acceptance criteria.
- Repository instructions, architecture, current working-tree state, and relevant test/build commands.
- Files, APIs, dependencies, and environments that may be affected.
- Approval boundaries for commits, pushes, deployments, deletions, and external changes.

## Instructions

### Preserved source section: Procedure

1. **Inspect before editing.** Read applicable agent and project instructions, inspect the working tree, and locate the existing behavior. Do not overwrite unrelated user changes.
2. **Reproduce the issue or define the feature.** Capture the current behavior and create a focused acceptance check before broad implementation.
3. **Plan a thin slice.** Identify the smallest change that delivers the requested outcome. List affected components, risks, tests, and any needed user decision.
4. **Confirm write scope.** Keep edits limited to relevant files. Use an isolated worktree or branch when parallel agents or risky changes could collide.
5. **Implement incrementally.** Make one coherent change at a time, follow local patterns, and avoid unrelated refactors. Ground framework-specific choices in the project's versioned documentation when needed.
6. **Run focused checks.** Execute the narrowest relevant unit or integration tests first, then required lint, type, build, or end-to-end checks.
7. **Review the diff.** Inspect every changed file for unintended edits, secrets, generated artifacts, weakened checks, and missing documentation.
8. **Verify the outcome.** Compare actual behavior with the acceptance criteria and run regression checks for nearby behavior.
9. **Report precisely.** Summarize files changed, checks and results, known limitations, and follow-up work.
10. **Gate shipping actions.** Do not commit, push, publish, or deploy unless the user authorized that exact action and the relevant checks pass.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

4. **Confirm write scope.** Keep edits limited to relevant files. Use an isolated worktree or branch when parallel agents or risky changes could collide.
5. **Implement incrementally.** Make one coherent change at a time, follow local patterns, and avoid unrelated refactors. Ground framework-specific choices in the project's versioned documentation when needed.
10. **Gate shipping actions.** Do not commit, push, publish, or deploy unless the user authorized that exact action and the relevant checks pass.

### Source conditional guidance from: Output and Acceptance

Return a concise implementation summary, verification evidence, and any remaining risk. The change is acceptable when the requested behavior is implemented, relevant checks pass, unrelated working-tree state is preserved, and no unapproved external action was taken.

### Source conditional guidance from: Stop Conditions

Stop and ask when requirements conflict, the target files contain unrelated user work, the needed environment is unavailable, a check fails without a safe repair, or a requested change would expand scope materially.

## Output Format

### Preserved source section: Output and Acceptance

Return a concise implementation summary, verification evidence, and any remaining risk. The change is acceptable when the requested behavior is implemented, relevant checks pass, unrelated working-tree state is preserved, and no unapproved external action was taken.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

8. **Verify the outcome.** Compare actual behavior with the acceptance criteria and run regression checks for nearby behavior.

## Stop Conditions

### Preserved source section: Stop Conditions

Stop and ask when requirements conflict, the target files contain unrelated user work, the needed environment is unavailable, a check fails without a safe repair, or a requested change would expand scope materially.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return a concise implementation summary, verification evidence, and any remaining risk. The change is acceptable when the requested behavior is implemented, relevant checks pass, unrelated working-tree state is preserved, and no unapproved external action was taken.
