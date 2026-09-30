---
name: template-engine-development
description: "Use when creating or modifying a template parser, renderer, layout system, or embedded expression language to define syntax and output context, escape untrusted values by default, and avoid executing template content as host code. Trigger for interpolation, includes, inheritance, filters, or compiled templates."
---

# Template Engine Development

## Overview

This skill applies when creating or modifying a template parser, renderer, layout system, or embedded expression language. Its intended outcome is to define syntax and output context, escape untrusted values by default, and avoid executing template content as host code.

## When to Use

### Preserved source section: When to Use

Use for a system that combines templates and data to produce HTML, text, configuration, or other output. Identify the output context because safe escaping differs by target format.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

4. **Restrict evaluation.** Expose a small data model and allowlisted filters. Do not use host-language `eval`, arbitrary reflection, or unrestricted file/network access.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Template syntax, supported expressions, control flow, and file/include behavior.
- Output format, trust level of templates and data, and compatibility requirements.
- Resource limits, caching behavior, and expected error reporting.

## Instructions

### Preserved source section: Procedure

1. **Define the grammar.** Specify delimiters, escaping, expressions, blocks, includes, inheritance, and how malformed templates fail.
2. **Parse rather than splice.** Convert templates into an AST or similarly explicit representation. Keep parsing separate from evaluation and rendering.
3. **Escape for the output context.** Escape text by default; use context-aware encoding for HTML attributes, URLs, JavaScript, CSS, or other formats. Make raw output an explicit, narrowly controlled capability.
4. **Restrict evaluation.** Expose a small data model and allowlisted filters. Do not use host-language `eval`, arbitrary reflection, or unrestricted file/network access.
5. **Bound dependencies and work.** Prevent include cycles, path traversal, excessive recursion, unbounded loops, and oversized output. Define caching invalidation and template version behavior.
6. **Test security and semantics.** Cover escaping, malformed syntax, nested blocks, missing variables, include boundaries, encoding, and adversarial template input.
7. **Report errors usefully.** Include template identity and source position without disclosing secrets or internal data.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Document grammar, output contexts, sandbox capabilities, limits, and supported constructs. Accept only when representative templates render deterministically, untrusted values remain safely encoded, and resource limits stop pathological input.

## Output Format

### Preserved source section: Output and Acceptance

Document grammar, output contexts, sandbox capabilities, limits, and supported constructs. Accept only when representative templates render deterministically, untrusted values remain safely encoded, and resource limits stop pathological input.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Resource limits, caching behavior, and expected error reporting.

### Source edge/failure guidance from: Procedure

1. **Define the grammar.** Specify delimiters, escaping, expressions, blocks, includes, inheritance, and how malformed templates fail.
6. **Test security and semantics.** Cover escaping, malformed syntax, nested blocks, missing variables, include boundaries, encoding, and adversarial template input.
7. **Report errors usefully.** Include template identity and source position without disclosing secrets or internal data.

## Stop Conditions

### Source stop-related guidance from: Output and Acceptance

Document grammar, output contexts, sandbox capabilities, limits, and supported constructs. Accept only when representative templates render deterministically, untrusted values remain safely encoded, and resource limits stop pathological input.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Document grammar, output contexts, sandbox capabilities, limits, and supported constructs. Accept only when representative templates render deterministically, untrusted values remain safely encoded, and resource limits stop pathological input.
