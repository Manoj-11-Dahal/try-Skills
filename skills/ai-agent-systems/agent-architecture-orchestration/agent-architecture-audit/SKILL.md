---
name: agent-architecture-audit
description: "Use when an agent or LLM application behaves inconsistently, misses tool calls, regresses after wrapper changes, contaminates memory, or fails between model output and UI/API delivery to trace inputs through context, planning, tools, state, recovery, and rendering; isolate the failing stage with evidence. Trigger before broad prompt rewrites or blind retries."
---

# Agent Architecture Audit

## Overview

This skill applies when an agent or LLM application behaves inconsistently, misses tool calls, regresses after wrapper changes, contaminates memory, or fails between model output and UI/API delivery. Its intended outcome is to trace inputs through context, planning, tools, state, recovery, and rendering; isolate the failing stage with evidence.

## When to Use

### Preserved source section: When to Use

Use when an agent's behavior is unreliable, quality degrades after a system change, a tool call is claimed but not observed, or the same model behaves differently in a wrapper, platform, or deployment.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Audit Guardrails

- Do not expose secrets in traces or send sensitive prompts to third-party debugging tools.
- Do not treat model self-report as proof that a tool was called or a state changed.
- Avoid simultaneous changes across prompts, tools, memory, and UI; they obscure causal evidence.
- If the failure cannot be reproduced, label the diagnosis provisional and gather more telemetry.

### Source boundary statements from: Procedure

3. **Find the earliest divergence.** Compare the expected and observed state at each boundary. Do not start with a broad prompt rewrite when the failure may be in a tool, transport, or stale cache.
6. **Inspect recovery and state.** Look for silent retries, hidden fallback agents, duplicated writes, stale checkpoints, cross-session contamination, or success flags that do not correspond to verified state.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- A minimal reproducible task and expected result.
- System, developer, and user instructions relevant to the failing run.
- Model/version, wrapper or host version, tool configuration, memory source, and recent changes.
- Logs or traces with secrets and personal data removed.

## Instructions

### Preserved source section: Procedure

1. **Reproduce and baseline.** Record the failing input, environment, output, and expected behavior. Compare with a known-good run where available.
2. **Map the request path.** Trace input parsing, instruction assembly, context retrieval, planning/routing, tool selection, tool execution, result interpretation, state persistence, retries/repairs, and final rendering.
3. **Find the earliest divergence.** Compare the expected and observed state at each boundary. Do not start with a broad prompt rewrite when the failure may be in a tool, transport, or stale cache.
4. **Inspect context integrity.** Check for contradictory rules, stale memory, missing project context, untrusted content treated as authority, truncation, and summarization that changed decision-critical details.
5. **Inspect tool discipline.** Verify tool availability, schemas, permissions, routing, actual invocation, returned output, and whether the agent interpreted the observation correctly.
6. **Inspect recovery and state.** Look for silent retries, hidden fallback agents, duplicated writes, stale checkpoints, cross-session contamination, or success flags that do not correspond to verified state.
7. **Inspect output delivery.** Compare the model response with wrapper transformations, serialization, filters, UI rendering, API responses, or client-side post-processing.
8. **Isolate one layer.** Change one variable at a time, preserve the baseline, and rerun the minimal test plus a regression set.
9. **Rank findings.** State severity, evidence, affected boundary, likely cause, confidence, and the narrowest testable fix. Separate confirmed defects from hypotheses.
10. **Verify remediation.** Re-run the same reproduction and checks at the affected boundary; verify no new regression or unauthorized side effect.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

3. **Find the earliest divergence.** Compare the expected and observed state at each boundary. Do not start with a broad prompt rewrite when the failure may be in a tool, transport, or stale cache.

### Source conditional guidance from: Output and Acceptance

Produce an audit report with system map, reproduction, earliest failing boundary, evidence, ranked findings, fixes, and verification status. The audit is acceptable when each confirmed finding is traceable to an observation and each fix has a specific validation check.

### Source conditional guidance from: Audit Guardrails

- If the failure cannot be reproduced, label the diagnosis provisional and gather more telemetry.

## Output Format

### Preserved source section: Output and Acceptance

Produce an audit report with system map, reproduction, earliest failing boundary, evidence, ranked findings, fixes, and verification status. The audit is acceptable when each confirmed finding is traceable to an observation and each fix has a specific validation check.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- System, developer, and user instructions relevant to the failing run.

### Source edge/failure guidance from: Procedure

1. **Reproduce and baseline.** Record the failing input, environment, output, and expected behavior. Compare with a known-good run where available.
2. **Map the request path.** Trace input parsing, instruction assembly, context retrieval, planning/routing, tool selection, tool execution, result interpretation, state persistence, retries/repairs, and final rendering.
3. **Find the earliest divergence.** Compare the expected and observed state at each boundary. Do not start with a broad prompt rewrite when the failure may be in a tool, transport, or stale cache.
6. **Inspect recovery and state.** Look for silent retries, hidden fallback agents, duplicated writes, stale checkpoints, cross-session contamination, or success flags that do not correspond to verified state.
8. **Isolate one layer.** Change one variable at a time, preserve the baseline, and rerun the minimal test plus a regression set.
10. **Verify remediation.** Re-run the same reproduction and checks at the affected boundary; verify no new regression or unauthorized side effect.

### Source edge/failure guidance from: Output and Acceptance

Produce an audit report with system map, reproduction, earliest failing boundary, evidence, ranked findings, fixes, and verification status. The audit is acceptable when each confirmed finding is traceable to an observation and each fix has a specific validation check.

### Source edge/failure guidance from: Audit Guardrails

- If the failure cannot be reproduced, label the diagnosis provisional and gather more telemetry.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Produce an audit report with system map, reproduction, earliest failing boundary, evidence, ranked findings, fixes, and verification status. The audit is acceptable when each confirmed finding is traceable to an observation and each fix has a specific validation check.
