---
name: performance-benchmarking-and-regression-detection
description: "Use when measuring application, service, build, or browser performance; investigating a slowdown; or comparing a change against a baseline to define representative workloads, environmental controls, metrics, and acceptable variance before optimizing. Trigger for performance investigations and regression gates, not speculative micro-optimization."
---

# Performance Benchmarking and Regression Detection

## Overview

This skill applies when measuring application, service, build, or browser performance; investigating a slowdown; or comparing a change against a baseline. Its intended outcome is to define representative workloads, environmental controls, metrics, and acceptable variance before optimizing.

## When to Use

### Preserved source section: When to Use

Use when performance is a requirement, a reported problem, or a suspected regression. Separate browser-user experience, service latency/throughput, build feedback time, and resource consumption; each needs different measurements.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

- Do not state universal performance thresholds without a product or standard basis.
- Do not compare measurements collected under materially different conditions as if they were equivalent.
- Do not use a single run or one aggregate score to claim a reliable improvement.

### Source boundary statements from: Procedure

5. **Make one targeted change.** Preserve correctness tests and a comparison run. Do not optimize a synthetic benchmark at the expense of representative user work.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- User-visible or operational performance goal and affected workload.
- Baseline build, target environment, dependencies, data size, hardware, and run conditions.
- Relevant measurements, sampling tools, acceptable variance, and decision thresholds.

## Instructions

### Preserved source section: Procedure

1. **Define the question.** State which operation is slow or at risk, for whom, and what outcome matters. Choose a metric that reflects that question rather than a convenient proxy.
2. **Establish a reproducible baseline.** Fix or record software version, machine, data, cache state, concurrency, browser, network, and tool versions. Repeat measurements enough to understand variance.
3. **Measure the full path.** Collect relevant latency percentiles, throughput, CPU, memory, I/O, bundle or transfer size, or browser field/lab metrics. Keep real-user observations distinct from controlled lab runs.
4. **Localize with profiling.** Use traces, profiles, query plans, or flame graphs to find the dominant cost. Avoid changing multiple variables before identifying a likely cause.
5. **Make one targeted change.** Preserve correctness tests and a comparison run. Do not optimize a synthetic benchmark at the expense of representative user work.
6. **Compare fairly.** Run baseline and candidate under equivalent conditions, report absolute values and deltas, and account for noise, warm-up, and outliers. Apply only project-approved thresholds.
7. **Check trade-offs and regressions.** Review memory, cost, complexity, tail latency, accessibility, and other affected dimensions. Keep a rollback or revert path for risky performance changes.
8. **Preserve the result.** Record measurement commands, inputs, environment, raw outputs, interpretation, and follow-up owner.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Return the question, baseline and candidate conditions, measurements, variance, bottleneck evidence, change tested, trade-offs, and decision. Accept an optimization only when the representative metric improves beyond measurement noise and required correctness and resource constraints still pass.

### Source conditional guidance from: Guardrails

- Do not compare measurements collected under materially different conditions as if they were equivalent.

## Output Format

### Preserved source section: Output and Acceptance

Return the question, baseline and candidate conditions, measurements, variance, bottleneck evidence, change tested, trade-offs, and decision. Accept an optimization only when the representative metric improves beyond measurement noise and required correctness and resource constraints still pass.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

7. **Check trade-offs and regressions.** Review memory, cost, complexity, tail latency, accessibility, and other affected dimensions. Keep a rollback or revert path for risky performance changes.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return the question, baseline and candidate conditions, measurements, variance, bottleneck evidence, change tested, trade-offs, and decision. Accept an optimization only when the representative metric improves beyond measurement noise and required correctness and resource constraints still pass.
