---
name: neural-network-development
description: "Use when implementing a neural-network model, training loop, inference component, or learning algorithm to define tensor shapes, data provenance, objective, and evaluation before training; verify numerical behavior on small reproducible cases before using larger or sensitive datasets. Trigger for architecture, gradient, optimizer, or model-serving work."
---

# Neural Network Development

## Overview

This skill applies when implementing a neural-network model, training loop, inference component, or learning algorithm. Its intended outcome is to define tensor shapes, data provenance, objective, and evaluation before training; verify numerical behavior on small reproducible cases before using larger or sensitive datasets.

## When to Use

### Preserved source section: When to Use

Use for model computation and training workflows. Distinguish a learning exercise from a validated model intended to influence real decisions.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

6. **Evaluate generalization and risk.** Report performance on held-out data, relevant slices, calibration or uncertainty where needed, and known limitations. Do not optimize only the training score.

### Source boundary statements from: Safety and Acceptance

Do not present benchmark success as proof of real-world safety or fairness. Obtain domain review for high-impact use. Accept a prototype when computations are numerically sound, results are reproducible, data handling is documented, and evaluation matches the stated task.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Task, model inputs and outputs, tensor shapes, and intended use.
- Dataset provenance, consent, license, split policy, and sensitivity.
- Compute budget, seed policy, evaluation metrics, and deployment constraints.

## Instructions

### Preserved source section: Procedure

1. **Establish a baseline.** Define a simple model or non-neural baseline, metrics, and held-out evaluation split before tuning.
2. **Make shapes explicit.** Document batch, sequence, channel, and feature dimensions. Validate shapes and data types at module boundaries.
3. **Test the numerical core.** Check forward outputs, loss behavior, gradients, optimizer updates, and finite values on tiny hand-checkable examples. Use gradient checks for custom derivatives.
4. **Build the data path.** Prevent train/test leakage, record preprocessing, handle missing or imbalanced labels, and keep sensitive data out of logs and checkpoints unless explicitly authorized.
5. **Train reproducibly.** Set and record random seeds, data versions, model configuration, compute settings, checkpoints, and stopping criteria. Track more than one metric when tradeoffs matter.
6. **Evaluate generalization and risk.** Report performance on held-out data, relevant slices, calibration or uncertainty where needed, and known limitations. Do not optimize only the training score.
7. **Gate deployment separately.** Validate latency, resource use, rollback, monitoring, privacy, and human oversight for the actual intended use.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

4. **Build the data path.** Prevent train/test leakage, record preprocessing, handle missing or imbalanced labels, and keep sensitive data out of logs and checkpoints unless explicitly authorized.
5. **Train reproducibly.** Set and record random seeds, data versions, model configuration, compute settings, checkpoints, and stopping criteria. Track more than one metric when tradeoffs matter.

### Source conditional guidance from: Safety and Acceptance

Do not present benchmark success as proof of real-world safety or fairness. Obtain domain review for high-impact use. Accept a prototype when computations are numerically sound, results are reproducible, data handling is documented, and evaluation matches the stated task.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Stop Conditions

### Source stop-related guidance from: Procedure

5. **Train reproducibly.** Set and record random seeds, data versions, model configuration, compute settings, checkpoints, and stopping criteria. Track more than one metric when tradeoffs matter.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Do not present benchmark success as proof of real-world safety or fairness. Obtain domain review for high-impact use. Accept a prototype when computations are numerically sound, results are reproducible, data handling is documented, and evaluation matches the stated task.
