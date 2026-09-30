---
name: accessibility-audit-and-remediation
description: "Use when auditing or improving a web or application interface for accessibility, including keyboard access, focus behavior, semantics, text alternatives, forms, and assistive-technology compatibility to select the applicable standard and user flows, combine automated checks with manual testing, and report evidence and gaps. Trigger for accessibility reviews or inclusive UI changes."
---

# Accessibility Audit and Remediation

## Overview

This skill applies when auditing or improving a web or application interface for accessibility, including keyboard access, focus behavior, semantics, text alternatives, forms, and assistive-technology compatibility. Its intended outcome is to select the applicable standard and user flows, combine automated checks with manual testing, and report evidence and gaps.

## When to Use

### Preserved source section: When to Use

Use when accessibility itself is a goal, a release requirement, or a concern raised by users. For general framework implementation, use the project's domain skill and add this audit when a focused accessibility evaluation is needed.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Safety and Respect

Do not infer a person's abilities from a diagnosis or use assistive-technology simulation as a substitute for user research. Avoid sharing identifiable user testing data. When legal or contractual conformance is claimed, recommend qualified accessibility review and retain the evidence required by that program.

### Source boundary statements from: Procedure

1. **Define scope and criteria.** Record the pages, states, components, platforms, and success criteria to assess. Do not imply a full-site audit after inspecting a sample.
2. **Run automated checks.** Use a recognized accessibility scanner where available and preserve tool/version and page state. Treat findings as leads; automated checks cannot establish full conformance.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Product, representative pages and flows, platforms, and target user needs.
- Applicable standard/version and conformance target, such as WCAG 2.2 AA for web content.
- Available browser, keyboard, screen-reader, automated scanner, and assistive-technology tools.
- Known limitations, third-party components, and remediation scope.

## Instructions

### Preserved source section: Procedure

1. **Define scope and criteria.** Record the pages, states, components, platforms, and success criteria to assess. Do not imply a full-site audit after inspecting a sample.
2. **Run automated checks.** Use a recognized accessibility scanner where available and preserve tool/version and page state. Treat findings as leads; automated checks cannot establish full conformance.
3. **Test keyboard and focus manually.** Navigate without a pointer, verify logical order, visible focus, operable controls, modal containment and escape, and recovery after dynamic updates.
4. **Inspect semantics and announcements.** Check native element choice, accessible name/role/state, headings, landmarks, labels, instructions, error association, status announcements, and meaningful alternatives for non-text content.
5. **Check visual and cognitive access.** Evaluate text and non-text contrast against the chosen criterion, zoom/reflow, text resizing, motion preferences, timing, consistency, and whether instructions rely only on color, position, or sound.
6. **Use assistive technology proportionately.** Test representative high-risk flows with at least one relevant screen reader or platform accessibility inspector when available. Record the actual configuration and limits.
7. **Prioritize remediation.** Describe affected users, barrier, reproducible steps, criterion, and suggested fix. Fix shared root causes before isolated symptoms; re-test the flow after changes.
8. **Report conformance honestly.** Separate verified criteria, failures, not-applicable criteria, and untested areas. An automated scan score is not a conformance certificate.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

6. **Use assistive technology proportionately.** Test representative high-risk flows with at least one relevant screen reader or platform accessibility inspector when available. Record the actual configuration and limits.

### Source conditional guidance from: Output and Acceptance

Provide scope, standard/version, tools and manual methods, findings by impact and criterion, remediation order, retest evidence, and untested areas. Accept a remediation only when the affected interaction works with the relevant input method and no new barrier was introduced.

### Source conditional guidance from: Safety and Respect

Do not infer a person's abilities from a diagnosis or use assistive-technology simulation as a substitute for user research. Avoid sharing identifiable user testing data. When legal or contractual conformance is claimed, recommend qualified accessibility review and retain the evidence required by that program.

## Output Format

### Preserved source section: Output and Acceptance

Provide scope, standard/version, tools and manual methods, findings by impact and criterion, remediation order, retest evidence, and untested areas. Accept a remediation only when the affected interaction works with the relevant input method and no new barrier was introduced.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

3. **Test keyboard and focus manually.** Navigate without a pointer, verify logical order, visible focus, operable controls, modal containment and escape, and recovery after dynamic updates.
4. **Inspect semantics and announcements.** Check native element choice, accessible name/role/state, headings, landmarks, labels, instructions, error association, status announcements, and meaningful alternatives for non-text content.
8. **Report conformance honestly.** Separate verified criteria, failures, not-applicable criteria, and untested areas. An automated scan score is not a conformance certificate.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Provide scope, standard/version, tools and manual methods, findings by impact and criterion, remediation order, retest evidence, and untested areas. Accept a remediation only when the affected interaction works with the relevant input method and no new barrier was introduced.
