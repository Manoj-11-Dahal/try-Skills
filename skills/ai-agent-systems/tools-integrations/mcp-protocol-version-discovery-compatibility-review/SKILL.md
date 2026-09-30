---
name: mcp-protocol-version-discovery-compatibility-review
description: "Use when verifying MCP protocol-version negotiation, server discovery, capability reporting, or modern/legacy interoperability across named client, server, SDK, and transport versions to produce a compatibility matrix and bounded test record. Success means request metadata and supported versions are explicit, extension behavior has a defined fallback or rejection, version errors trigger only valid retries, and unsupported combinations fail clearly. Do not treat self-reported server identity as a security guarantee or assume older handshake examples remain current."
---

# MCP Protocol Version and Discovery Compatibility Review

## Overview

This skill applies when verifying MCP protocol-version negotiation, server discovery, capability reporting, or modern/legacy interoperability across named client, server, SDK, and transport versions. Its intended outcome is to produce a compatibility matrix and bounded test record.

## When to Use

### Preserved source section: When to Use

Use this workflow when upgrading MCP client/server code, debugging version mismatches, adding extension support, or deciding whether a client must interoperate with legacy servers. Pin the protocol revision, SDK versions, and transport under review; protocol details change across revisions.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

Do not add unsupported extensions or silently infer security permissions from capability metadata. A compatible version is not automatically a secure version. Stop if the required backward-compatibility behavior or owner-approved support window is unclear.

### Source boundary statements from: Workflow

1. **Establish the protocol era.** Identify whether each endpoint uses per-request metadata (modern revisions, including 2026-07-28) or a connection-scoped `initialize` handshake (2025-11-25 and earlier). Do not mix an example from one era with assumptions from another.
6. **Test bounded cases.** Cover missing or malformed metadata, unknown versions, stale discovery cache, extension mismatch, server restart, and legacy fallback. Use an isolated server or simulator; do not update production settings during the review.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the host/client/server roles, protocol revisions, SDK/runtime versions, transport, declared capabilities, extension identifiers, intended fallback behavior, and compatibility requirements. Use current official specification pages for normative behavior and separate those claims from observed test results.

## Instructions

### Preserved source section: Workflow

1. **Establish the protocol era.** Identify whether each endpoint uses per-request metadata (modern revisions, including 2026-07-28) or a connection-scoped `initialize` handshake (2025-11-25 and earlier). Do not mix an example from one era with assumptions from another.
2. **Check discovery and metadata.** Verify the server implements `server/discover`, returns supported versions and capabilities, and that each request carries the required protocol-version, client-identity, and client-capability metadata. For HTTP, verify mirrored headers agree with the body according to the selected transport revision.
3. **Define version-error handling.** Test an unsupported version response, select only a mutually supported revision, and retry with the required request metadata. If there is no compatible revision, surface a clear failure rather than guessing or silently downgrading.
4. **Review extension negotiation.** For every optional extension, record the client advertisement, server discovery result, extension settings, supported request methods, and the fallback or explicit rejection path when one side lacks support.
5. **Build a compatibility matrix.** Include every supported client/server era and transport pair. For dual-era support, test the transport-specific detection and fallback paths; avoid sending ambiguous legacy/modern messages without a defined probe.
6. **Test bounded cases.** Cover missing or malformed metadata, unknown versions, stale discovery cache, extension mismatch, server restart, and legacy fallback. Use an isolated server or simulator; do not update production settings during the review.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

3. **Define version-error handling.** Test an unsupported version response, select only a mutually supported revision, and retry with the required request metadata. If there is no compatible revision, surface a clear failure rather than guessing or silently downgrading.
4. **Review extension negotiation.** For every optional extension, record the client advertisement, server discovery result, extension settings, supported request methods, and the fallback or explicit rejection path when one side lacks support.

### Source conditional guidance from: Guardrails

Do not add unsupported extensions or silently infer security permissions from capability metadata. A compatible version is not automatically a secure version. Stop if the required backward-compatibility behavior or owner-approved support window is unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The official specification below was consulted for version and discovery behavior only; no upstream skill text or examples were copied. Check for newer revisions before applying version-specific guidance.

- [MCP Specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- [Versioning and Compatibility](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
- [Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs and Boundaries

Record the host/client/server roles, protocol revisions, SDK/runtime versions, transport, declared capabilities, extension identifiers, intended fallback behavior, and compatibility requirements. Use current official specification pages for normative behavior and separate those claims from observed test results.

### Source edge/failure guidance from: Workflow

3. **Define version-error handling.** Test an unsupported version response, select only a mutually supported revision, and retry with the required request metadata. If there is no compatible revision, surface a clear failure rather than guessing or silently downgrading.
4. **Review extension negotiation.** For every optional extension, record the client advertisement, server discovery result, extension settings, supported request methods, and the fallback or explicit rejection path when one side lacks support.
5. **Build a compatibility matrix.** Include every supported client/server era and transport pair. For dual-era support, test the transport-specific detection and fallback paths; avoid sending ambiguous legacy/modern messages without a defined probe.
6. **Test bounded cases.** Cover missing or malformed metadata, unknown versions, stale discovery cache, extension mismatch, server restart, and legacy fallback. Use an isolated server or simulator; do not update production settings during the review.

### Source edge/failure guidance from: Acceptance Evidence

The result includes protocol and SDK versions, transport, discovery response, capability/extension matrix, tested retry/fallback behavior, and unsupported combinations. `serverInfo` is treated as display/debug metadata, not proof of publisher identity or trust.

## Stop Conditions

### Source stop-related guidance from: Guardrails

Do not add unsupported extensions or silently infer security permissions from capability metadata. A compatible version is not automatically a secure version. Stop if the required backward-compatibility behavior or owner-approved support window is unclear.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The result includes protocol and SDK versions, transport, discovery response, capability/extension matrix, tested retry/fallback behavior, and unsupported combinations. `serverInfo` is treated as display/debug metadata, not proof of publisher identity or trust.
