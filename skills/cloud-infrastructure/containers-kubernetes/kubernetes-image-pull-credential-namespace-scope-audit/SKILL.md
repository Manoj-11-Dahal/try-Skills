---
name: kubernetes-image-pull-credential-namespace-scope-audit
description: "Use when a task involves reviewing which Pods and namespaces can use credentials to pull private images to record Kubernetes server and client versions, cluster distribution and provider, API versions, namespace and workload owner, data sensitivity, evidence requirements, and maintenance window. Check current Kubernetes and provider documentation, begin with read-only evidence, and validate changes in an approved environment. Do not modify production resources, credentials, or persistent data without explicit owner approval."
---

# Kubernetes Image-Pull Credential Namespace-Scope Audit

## Overview

This skill applies when a task involves reviewing which Pods and namespaces can use credentials to pull private images. Its intended outcome is to record Kubernetes server and client versions, cluster distribution and provider, API versions, namespace and workload owner, data sensitivity, evidence requirements, and maintenance window.

## When to Use

### Preserved source section: When to Use

Use this skill when reviewing which Pods and namespaces can use credentials to pull private images. It is an operational checklist for an authorized Kubernetes cluster, repository, or staging environment; it does not itself authorize cluster access, changes, or incident response.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

Do not reveal, decode, or rotate registry credentials during this audit.
- Never print or export bearer tokens, Secret data, private keys, cloud credentials, or sensitive workload payloads.
- Do not mutate shared or production clusters, evict workloads, rotate credentials, delete storage, or alter network exposure without explicit authorization from the responsible owner.
- Do not bypass admission, Pod Security, RBAC, NetworkPolicy, TLS, or provider safeguards to make a test pass.
- Stop when resource ownership, data retention, failure impact, provider responsibility, or recovery authority is unclear.

### Source boundary statements from: Topic Provenance

This workflow is independently authored for this repository using public Kubernetes documentation for topic discovery and technical reference. No upstream skill prose, code, scripts, commands, examples, prompts, or assets were copied. Kubernetes behavior and feature support vary by version and distribution; verify the effective behavior of the target cluster. This document does not grant authority to operate a cluster.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record cluster identity, server and client versions, distribution/provider, API versions, namespace, resource owner, intended outcome, maintenance window, data sensitivity, and stop condition. Separate read-only investigation from an applied change. Prefer synthetic data and disposable namespaces for tests.

## Instructions

### Preserved source section: Workflow

1. **Set the boundary.** Name the target resources, accountable owner, allowed read/write scope, success condition, rollback path, and actions that require separate approval.
2. **Establish evidence.** Preserve the smallest useful manifest, status, event, metric, or provider-configuration snapshot. Redact tokens, secret values, user data, and internal addresses before sharing.
3. **Apply the focused method.** Inventory imagePullSecrets, service-account references, registry hosts, and namespace distribution without decoding credential data. Trace which principals can create Pods that reference each credential.
4. **Verify a bounded result.** Check copied secrets, default service accounts, cross-namespace assumptions, rotation ownership, and accidental credential exposure in manifests. Compare against a known baseline or independent observation when practical; record uncertainty and untested cases.
5. **Hand off safely.** Summarize the result, versions, evidence, limitations, remaining tests, and decision owner. Keep proposed changes distinct from changes actually applied.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

4. **Verify a bounded result.** Check copied secrets, default service accounts, cross-namespace assumptions, rotation ownership, and accidental credential exposure in manifests. Compare against a known baseline or independent observation when practical; record uncertainty and untested cases.

### Source conditional guidance from: Kubernetes Checks

- Preserve object UIDs and timestamps when correlating events; treat manifests, logs, snapshots, and traces as potentially sensitive.

### Source conditional guidance from: Guardrails

- Stop when resource ownership, data retention, failure impact, provider responsibility, or recovery authority is unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

This workflow is independently authored for this repository using public Kubernetes documentation for topic discovery and technical reference. No upstream skill prose, code, scripts, commands, examples, prompts, or assets were copied. Kubernetes behavior and feature support vary by version and distribution; verify the effective behavior of the target cluster. This document does not grant authority to operate a cluster.

Technical reference: [Kubernetes Secret security guidance](https://kubernetes.io/docs/concepts/configuration/secret/)

## Output Format

Not specified in source skill.

## Validation Checklist

### Preserved source section: Kubernetes Checks

- Verify the exact server/client versions, distribution, feature gates, API versions, and provider-managed boundaries relevant to the finding.
- Distinguish desired API objects, controller status, node/runtime behavior, and provider-side infrastructure evidence.
- Preserve object UIDs and timestamps when correlating events; treat manifests, logs, snapshots, and traces as potentially sensitive.
- Recheck current Kubernetes and provider documentation before using version-sensitive fields, defaults, or recovery procedures.

**Unchecked checklist derived from source criteria (not test evidence):**

- [ ] Verify the exact server/client versions, distribution, feature gates, API versions, and provider-managed boundaries relevant to the finding.
- [ ] Distinguish desired API objects, controller status, node/runtime behavior, and provider-side infrastructure evidence.
- [ ] Preserve object UIDs and timestamps when correlating events; treat manifests, logs, snapshots, and traces as potentially sensitive.
- [ ] Recheck current Kubernetes and provider documentation before using version-sensitive fields, defaults, or recovery procedures.

## Edge Cases and Recovery

### Source edge/failure guidance from: Kubernetes Checks

- Recheck current Kubernetes and provider documentation before using version-sensitive fields, defaults, or recovery procedures.

### Source edge/failure guidance from: Guardrails

- Stop when resource ownership, data retention, failure impact, provider responsibility, or recovery authority is unclear.

## Stop Conditions

### Source stop-related guidance from: Inputs and Boundaries

Record cluster identity, server and client versions, distribution/provider, API versions, namespace, resource owner, intended outcome, maintenance window, data sensitivity, and stop condition. Separate read-only investigation from an applied change. Prefer synthetic data and disposable namespaces for tests.

### Source stop-related guidance from: Guardrails

- Stop when resource ownership, data retention, failure impact, provider responsibility, or recovery authority is unclear.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance

The result answers the stated operational question, identifies cluster and component versions, includes reproducible evidence and limitations, and names required owner approvals. It makes no unsupported claim of availability, security, durability, or provider compatibility.
