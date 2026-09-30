---
name: test-driven-development-workflow
description: "Use when implementing new behavior, fixing a defect, or refactoring code where automated checks can describe the expected behavior to turn acceptance criteria into focused tests, observe a meaningful failing test, make the smallest change that passes, then refactor and re-verify. Trigger for feature work, bug fixes, and behavior-changing refactors; adapt the test form when automation is not practical."
---

# Test-Driven Development Workflow

## Overview

This skill applies when implementing new behavior, fixing a defect, or refactoring code where automated checks can describe the expected behavior. Its intended outcome is to turn acceptance criteria into focused tests, observe a meaningful failing test, make the smallest change that passes, then refactor and re-verify.

## When to Use

### Preserved source section: When to Use

Use this workflow when tests can capture the requested behavior or protect a defect fix. For a purely editorial change or an environment where tests are unavailable, choose an appropriate non-code check and state the limitation instead of manufacturing a test.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

- A test that passes before the change does not prove the change was needed; investigate whether it exercises the stated behavior.
- Do not claim RED when the test failed for unrelated setup or infrastructure reasons.
- Do not impose a universal coverage percentage without a project-defined reason; prioritize meaningful behavior and risk over raw line counts.
- Do not commit, push, or deploy as a side effect of completing the test cycle.

### Source boundary statements from: Procedure

1. **Inspect the local test contract.** Read project instructions and nearby tests. Determine the actual runner and smallest relevant command; do not assume a package manager or test framework.
4. **Make the smallest change.** Implement only what is needed to satisfy the failing assertion. Do not weaken the test, silence an error, or widen the change to avoid understanding a failure.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The requested behavior, constraints, and acceptance criteria.
- The repository's existing test conventions, runner, and relevant commands.
- A reproducible current behavior or a precise description of the intended change.
- Any explicit limits on edits, dependencies, test data, or external effects.

## Instructions

### Preserved source section: Procedure

1. **Inspect the local test contract.** Read project instructions and nearby tests. Determine the actual runner and smallest relevant command; do not assume a package manager or test framework.
2. **Write the behavior as an assertion.** Prefer a test through a public interface that captures a user-visible result, invariant, or regression. Include important boundaries and failure cases without encoding private implementation details.
3. **Observe RED.** Run the focused test before changing production code. Confirm it fails for the intended missing behavior, not because the test is malformed, setup is broken, or the environment is unavailable. Save the exact output.
4. **Make the smallest change.** Implement only what is needed to satisfy the failing assertion. Do not weaken the test, silence an error, or widen the change to avoid understanding a failure.
5. **Observe GREEN.** Run the focused test again and confirm it passes. Then run nearby regression tests and required type, lint, build, or integration checks according to project guidance.
6. **Refactor only after GREEN.** Improve structure while preserving the tested behavior. Re-run the relevant tests after every meaningful refactor.
7. **Review coverage gaps.** Check error paths, boundaries, compatibility, and side effects. Add a test only when it protects a real requirement or likely regression.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

7. **Review coverage gaps.** Check error paths, boundaries, compatibility, and side effects. Add a test only when it protects a real requirement or likely regression.

### Source conditional guidance from: Output and Acceptance

Report the behavior tested, the RED evidence, the implementation scope, the GREEN and regression commands, and any checks that could not run. The workflow passes when a meaningful test fails before the fix, passes after it, and the final required checks agree with the acceptance criteria.

### Source conditional guidance from: Guardrails

- Do not claim RED when the test failed for unrelated setup or infrastructure reasons.

## Output Format

### Preserved source section: Output and Acceptance

Report the behavior tested, the RED evidence, the implementation scope, the GREEN and regression commands, and any checks that could not run. The workflow passes when a meaningful test fails before the fix, passes after it, and the final required checks agree with the acceptance criteria.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Write the behavior as an assertion.** Prefer a test through a public interface that captures a user-visible result, invariant, or regression. Include important boundaries and failure cases without encoding private implementation details.
3. **Observe RED.** Run the focused test before changing production code. Confirm it fails for the intended missing behavior, not because the test is malformed, setup is broken, or the environment is unavailable. Save the exact output.
4. **Make the smallest change.** Implement only what is needed to satisfy the failing assertion. Do not weaken the test, silence an error, or widen the change to avoid understanding a failure.
5. **Observe GREEN.** Run the focused test again and confirm it passes. Then run nearby regression tests and required type, lint, build, or integration checks according to project guidance.
7. **Review coverage gaps.** Check error paths, boundaries, compatibility, and side effects. Add a test only when it protects a real requirement or likely regression.

### Source edge/failure guidance from: Output and Acceptance

Report the behavior tested, the RED evidence, the implementation scope, the GREEN and regression commands, and any checks that could not run. The workflow passes when a meaningful test fails before the fix, passes after it, and the final required checks agree with the acceptance criteria.

### Source edge/failure guidance from: Guardrails

- Do not claim RED when the test failed for unrelated setup or infrastructure reasons.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report the behavior tested, the RED evidence, the implementation scope, the GREEN and regression commands, and any checks that could not run. The workflow passes when a meaningful test fails before the fix, passes after it, and the final required checks agree with the acceptance criteria.
