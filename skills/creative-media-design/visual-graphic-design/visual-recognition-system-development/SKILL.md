---
name: visual-recognition-system-development
description: "Use when building or modifying a system that classifies, detects, segments, tracks, or otherwise interprets images or video to define the task, dataset rights, evaluation slices, and operating limits before choosing a model, and test against held-out data without overstating accuracy. Trigger for camera, image, or visual perception workflows."
---

# Visual Recognition System Development

## Overview

This skill applies when building or modifying a system that classifies, detects, segments, tracks, or otherwise interprets images or video. Its intended outcome is to define the task, dataset rights, evaluation slices, and operating limits before choosing a model, and test against held-out data without overstating accuracy.

## When to Use

### Preserved source section: When to Use

Use for image or video perception systems. Separate data capture, preprocessing, model inference, post-processing, and user-facing decisions so each can be evaluated independently.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Safety and Acceptance

Do not treat benchmark scores as proof of fairness, identity, intent, or safe operation. Obtain domain and privacy review for surveillance or high-impact use. Accept only for a clearly bounded task with held-out evaluation and explicit uncertainty behavior.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Task definition, labels, target population, deployment environment, and decision consequences.
- Dataset provenance, consent, licenses, retention, annotation quality, and class coverage.
- Accuracy, latency, calibration, privacy, and human-review requirements.

## Instructions

### Preserved source section: Procedure

1. **Define the decision.** Specify the unit of prediction, labels, thresholds, confidence behavior, and what the system should do when uncertain or out of distribution.
2. **Audit the data.** Check rights, duplicates, label consistency, class imbalance, subject overlap, and train/test leakage. Keep sensitive imagery out of logs and checkpoints unless explicitly approved.
3. **Establish a baseline.** Use a simple model or existing validated method; record preprocessing, model version, seeds, and evaluation split.
4. **Evaluate by slice.** Report confusion patterns, false-positive and false-negative impact, relevant demographic or environmental slices where lawful and appropriate, and confidence calibration.
5. **Test the deployment path.** Check camera changes, resolution, lighting, motion blur, compression, latency, memory, and failure when inputs are missing or corrupted.
6. **Gate consequential use.** Keep human review for uncertain or high-impact decisions, document limitations, and provide a way to correct or contest outputs.
7. **Monitor drift responsibly.** Define privacy-preserving metrics and a review process for model, data, and threshold changes.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

1. **Define the decision.** Specify the unit of prediction, labels, thresholds, confidence behavior, and what the system should do when uncertain or out of distribution.
2. **Audit the data.** Check rights, duplicates, label consistency, class imbalance, subject overlap, and train/test leakage. Keep sensitive imagery out of logs and checkpoints unless explicitly approved.
5. **Test the deployment path.** Check camera changes, resolution, lighting, motion blur, compression, latency, memory, and failure when inputs are missing or corrupted.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

5. **Test the deployment path.** Check camera changes, resolution, lighting, motion blur, compression, latency, memory, and failure when inputs are missing or corrupted.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Do not treat benchmark scores as proof of fairness, identity, intent, or safe operation. Obtain domain and privacy review for surveillance or high-impact use. Accept only for a clearly bounded task with held-out evaluation and explicit uncertainty behavior.
