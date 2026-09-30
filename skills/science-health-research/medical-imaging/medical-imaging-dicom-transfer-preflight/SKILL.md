---
name: medical-imaging-dicom-transfer-preflight
description: "Use when preparing an approved DICOM transfer for engineering or research evaluation, to confirm both the destination and the receiving pipeline's supported object classes to produce a DICOM transfer preflight covering approval, endpoint, protocol, recipient, retention, modality, SOP Class UID, and unknown-object handling. Success means the route is authorized and protected, every proposed object class has a supported or explicit reject/review path, and a synthetic transfer reconciles without silent drops. This supports technical work only; it is not clinical decision support and does not authorize patient-data access."
---

# Medical Imaging DICOM Transfer Preflight

## Overview

This skill applies when preparing an approved DICOM transfer for engineering or research evaluation, to confirm both the destination and the receiving pipeline's supported object classes. Its intended outcome is to produce a DICOM transfer preflight covering approval, endpoint, protocol, recipient, retention, modality, SOP Class UID, and unknown-object handling.

## When to Use

### Preserved source section: When to Use

Use this workflow before routing DICOM objects to an engineering pipeline or approved research environment. Confirm both that the destination is authorized and that the receiver supports the intended modalities and SOP Classes; do not treat a successful network transfer as proof of compatibility.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use this workflow before routing DICOM objects to an engineering pipeline or approved research environment. Confirm both that the destination is authorized and that the receiver supports the intended modalities and SOP Classes; do not treat a successful network transfer as proof of compatibility.

### Source boundary statements from: Inputs and Boundaries

Record non-clinical intended use, data-use approval, destination owner and environment, recipients, encryption/protocol, modality, SOP Class UIDs, transfer syntaxes, pipeline version, retention policy, site/population scope, and technical owner. Prefer synthetic or approved de-identified fixtures; do not access patient data without the required lawful basis and review.

### Source boundary statements from: Workflow

5. **Reconcile the result.** Compare submitted, accepted, rejected, and quarantined counts. Preserve non-identifying technical evidence, object-class coverage, pipeline version, and unresolved exceptions. Do not include patient-level data in the report.

### Source boundary statements from: Safety and Stop Conditions

Never route identifiable or restricted DICOM data to an unapproved endpoint or third-party service. Do not assume every file described as DICOM is a supported image instance. Never diagnose, triage, recommend treatment, or make a patient-care decision. Stop if approval, endpoint ownership, object support, lawful basis, or data handling is uncertain.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record non-clinical intended use, data-use approval, destination owner and environment, recipients, encryption/protocol, modality, SOP Class UIDs, transfer syntaxes, pipeline version, retention policy, site/population scope, and technical owner. Prefer synthetic or approved de-identified fixtures; do not access patient data without the required lawful basis and review.

## Instructions

### Preserved source section: Workflow

1. **Confirm scope and approval.** Identify whether the work is research, engineering, usability evaluation, or an approved product-lifecycle task. Verify the governing approval, permitted data, recipients, and endpoint before any transfer.
2. **Validate the destination.** Confirm endpoint identity, protocol, encryption, access controls, authorized recipient, storage region, retention period, and deletion path. Check for public endpoints, shared workspaces, duplicate send routes, and metadata exposure in logs.
3. **Inventory object compatibility.** Use an approved sample to enumerate modality, SOP Class UID, transfer syntax, and required metadata. Compare every class with the receiving pipeline's declared support; assign unknown or unsupported objects to an explicit reject or human-review path rather than silently dropping them.
4. **Test with synthetic objects.** Exercise representative supported and unsupported classes, secondary captures, presentation states, enhanced objects, structured reports, encapsulated documents, and vendor-specific extensions as relevant. Verify both route controls and receiver handling.
5. **Reconcile the result.** Compare submitted, accepted, rejected, and quarantined counts. Preserve non-identifying technical evidence, object-class coverage, pipeline version, and unresolved exceptions. Do not include patient-level data in the report.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Stop Conditions

Never route identifiable or restricted DICOM data to an unapproved endpoint or third-party service. Do not assume every file described as DICOM is a supported image instance. Never diagnose, triage, recommend treatment, or make a patient-care decision. Stop if approval, endpoint ownership, object support, lawful basis, or data handling is uncertain.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The public standard below informed topic discovery and technical reference only; no upstream skill text, clinical protocol, code, model, prompt, example, or dataset was copied. Verify the current edition and local governance.

- [DICOM PS3.15 Security and System Management Profiles](https://dicom.nema.org/medical/dicom/current/output/pdf/part15.pdf)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

5. **Reconcile the result.** Compare submitted, accepted, rejected, and quarantined counts. Preserve non-identifying technical evidence, object-class coverage, pipeline version, and unresolved exceptions. Do not include patient-level data in the report.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Never route identifiable or restricted DICOM data to an unapproved endpoint or third-party service. Do not assume every file described as DICOM is a supported image instance. Never diagnose, triage, recommend treatment, or make a patient-care decision. Stop if approval, endpoint ownership, object support, lawful basis, or data handling is uncertain.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

A reviewer can trace approval, endpoint, recipient, protocol, data class, object-type support, test results, and retention/disposal. All counts reconcile or discrepancies have an owner and next action; unsupported classes are visible and are not silently discarded.
