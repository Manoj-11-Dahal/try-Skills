---
name: evaluation-harness-design
description: "Use when measuring whether an agent, prompt, tool pipeline, or skill is reliable across repeated cases to define representative tasks, reference outcomes, metrics, graders, calibration checks, regression thresholds, and a reproducible report before tuning. Trigger before release, after model or prompt changes, or when subjective impressions are driving quality decisions."
---

# Evaluation Harness Design

## Overview

This skill applies when measuring whether an agent, prompt, tool pipeline, or skill is reliable across repeated cases. Its intended outcome is to define representative tasks, reference outcomes, metrics, graders, calibration checks, regression thresholds, and a reproducible report before tuning.

## When to Use

### Preserved source section: When to Use

Use before releasing an agent workflow, comparing prompt or model changes, improving a reusable skill, or investigating inconsistent quality across repeated tasks.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Evaluation Guardrails

- Do not use the same examples to tune and claim final performance.
- Do not treat an LLM judge score as objective truth without calibration.
- Do not report only an aggregate when important subgroups differ.
- Do not weaken acceptance criteria after a failed result without documenting the decision and its impact.

### Source boundary statements from: Procedure

4. **Choose metrics.** Prefer deterministic checks for structure, calculations, tool effects, and pass/fail requirements. Use human or model judges only for qualities that cannot be checked deterministically.
5. **Separate tuning and holdout data.** Do not repeatedly optimize against the final benchmark. Keep a frozen set for regression measurement.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The capability under evaluation and its intended use conditions.
- Representative user tasks, edge cases, risk level, and expected behavior.
- Candidate metrics, reference answers or acceptable ranges, graders, and compute budget.
- Version information for prompts, models, tools, dependencies, and test data.

## Instructions

### Preserved source section: Procedure

1. **Define the claim.** State what capability the evaluation should demonstrate and what it does not prove.
2. **Sample real tasks.** Include ordinary cases, boundary cases, ambiguous inputs, tool failures, and safety-relevant cases. Avoid a test set made only of easy demonstrations.
3. **Create references.** Write expected answers, acceptable ranges, or explicit rubrics. Record disagreements and allow multiple correct responses where appropriate.
4. **Choose metrics.** Prefer deterministic checks for structure, calculations, tool effects, and pass/fail requirements. Use human or model judges only for qualities that cannot be checked deterministically.
5. **Separate tuning and holdout data.** Do not repeatedly optimize against the final benchmark. Keep a frozen set for regression measurement.
6. **Calibrate graders.** Compare judge decisions against human-labeled examples, measure disagreement, inspect false positives/negatives, and revise vague rubric language before trusting scores.
7. **Run reproducibly.** Pin model, prompt, tool versions, seed or sampling settings where possible, and evaluation data. Log raw outputs securely and preserve provenance.
8. **Analyze slices.** Report performance by task category, risk, ambiguity, tool use, and failure type; aggregate scores can hide critical regressions.
9. **Set release thresholds.** Define minimum quality, maximum regression, safety gates, and confidence requirements before seeing candidate results.
10. **Compare and decide.** Report improvements and regressions with uncertainty. Promote a change only when it meets the threshold without unacceptable safety or reliability loss.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

10. **Compare and decide.** Report improvements and regressions with uncertainty. Promote a change only when it meets the threshold without unacceptable safety or reliability loss.

### Source conditional guidance from: Output and Acceptance

Produce an evaluation plan or report containing the claim, dataset design, metrics, rubric, grader calibration, version record, thresholds, results, uncertainty, and release recommendation. Accept it only when another evaluator can reproduce the run and understand what the score does and does not establish.

### Source conditional guidance from: Evaluation Guardrails

- Do not report only an aggregate when important subgroups differ.

## Output Format

### Preserved source section: Output and Acceptance

Produce an evaluation plan or report containing the claim, dataset design, metrics, rubric, grader calibration, version record, thresholds, results, uncertainty, and release recommendation. Accept it only when another evaluator can reproduce the run and understand what the score does and does not establish.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Sample real tasks.** Include ordinary cases, boundary cases, ambiguous inputs, tool failures, and safety-relevant cases. Avoid a test set made only of easy demonstrations.
4. **Choose metrics.** Prefer deterministic checks for structure, calculations, tool effects, and pass/fail requirements. Use human or model judges only for qualities that cannot be checked deterministically.
5. **Separate tuning and holdout data.** Do not repeatedly optimize against the final benchmark. Keep a frozen set for regression measurement.
8. **Analyze slices.** Report performance by task category, risk, ambiguity, tool use, and failure type; aggregate scores can hide critical regressions.
9. **Set release thresholds.** Define minimum quality, maximum regression, safety gates, and confidence requirements before seeing candidate results.
10. **Compare and decide.** Report improvements and regressions with uncertainty. Promote a change only when it meets the threshold without unacceptable safety or reliability loss.

### Source edge/failure guidance from: Evaluation Guardrails

- Do not weaken acceptance criteria after a failed result without documenting the decision and its impact.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Produce an evaluation plan or report containing the claim, dataset design, metrics, rubric, grader calibration, version record, thresholds, results, uncertainty, and release recommendation. Accept it only when another evaluator can reproduce the run and understand what the score does and does not establish.
