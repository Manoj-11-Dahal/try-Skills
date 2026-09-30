---
name: mcp-conformance-and-interoperability-test-plan
description: "Use when preparing a test plan for an MCP client, server, SDK, or integration across protocol versions, transports, capabilities, or optional extensions to produce a reproducible matrix of discovery, request/response, authorization, errors, cancellation, and extension scenarios. Success means tests cover both expected behavior and meaningful failure paths for each supported peer combination, findings identify exact versions, and no single visual inspection is presented as full protocol conformance."
---

# MCP Conformance and Interoperability Test Plan

## Overview

This skill applies when preparing a test plan for an MCP client, server, SDK, or integration across protocol versions, transports, capabilities, or optional extensions. Its intended outcome is to produce a reproducible matrix of discovery, request/response, authorization, errors, cancellation, and extension scenarios.

## When to Use

### Preserved source section: When to Use

Use this workflow before releasing an MCP implementation, upgrading an SDK, or claiming support for a protocol revision or extension. It creates a bounded verification plan; it does not itself certify formal conformance or replace the protocol’s normative requirements.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Workflow

6. **Exercise failure and recovery.** Cover timeout, disconnect, server restart, duplicate request, stale cursor, cancellation race, wrong protocol metadata, auth failure, and partial external effect. Confirm retries are safe and do not repeat non-idempotent work.
7. **Use test tools proportionately.** Use a version-pinned MCP Inspector or SDK test harness only when authorized and in an isolated environment. Record manual probes separately from automated conformance tests and never install or run an unreviewed tool merely because a guide recommends it.

### Source boundary statements from: Safety and Stop Conditions

Do not use production credentials or real user data for protocol smoke tests without explicit approval. Do not invoke write-capable tools against live targets simply to prove connectivity. Stop if the test harness, server identity, or expected side effects are unclear.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record client/server roles, protocol revisions, SDK versions, STDIO or Streamable HTTP transport, declared capabilities, optional extensions, authentication mode, test environment, expected side effects, and release owner. Use an isolated server or staging environment and synthetic data unless separate approval authorizes otherwise.

## Instructions

### Preserved source section: Workflow

1. **Define supported combinations.** List the client/server versions, transport bindings, legacy compatibility paths, capabilities, and extensions the product claims to support. Mark unsupported combinations and expected diagnostics.
2. **Verify discovery and version behavior.** Test `server/discover`, protocol metadata on requests, supported-version reporting, an unsupported-version error, retry with a mutually supported version, and legacy fallback only where claimed.
3. **Test each declared primitive.** Exercise the advertised tools, resources, prompts, pagination, cache hints, and list-change behavior. Include valid, invalid, unauthorized, oversized, and malformed inputs; verify protocol errors versus tool-level failures are distinguished.
4. **Test transport and security boundaries.** For STDIO, verify framing, stdout/stderr separation, process shutdown, and environment isolation. For Streamable HTTP, verify POST behavior, request-scoped responses, Origin/auth handling, cancellation, proxy/SSE behavior, and subscription lifecycle.
5. **Test optional extensions independently.** For each claimed extension (for example Tasks or Skills), verify both sides opt in, unsupported peers follow the documented fallback/rejection, and extension-specific state, integrity, approval, and retention requirements hold.
6. **Exercise failure and recovery.** Cover timeout, disconnect, server restart, duplicate request, stale cursor, cancellation race, wrong protocol metadata, auth failure, and partial external effect. Confirm retries are safe and do not repeat non-idempotent work.
7. **Use test tools proportionately.** Use a version-pinned MCP Inspector or SDK test harness only when authorized and in an isolated environment. Record manual probes separately from automated conformance tests and never install or run an unreviewed tool merely because a guide recommends it.
8. **Report release evidence.** Provide a matrix with case ID, exact versions, expected/observed outcome, logs with secrets redacted, known limitations, owner, and go/no-go decision.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs and Boundaries

Record client/server roles, protocol revisions, SDK versions, STDIO or Streamable HTTP transport, declared capabilities, optional extensions, authentication mode, test environment, expected side effects, and release owner. Use an isolated server or staging environment and synthetic data unless separate approval authorizes otherwise.

### Source conditional guidance from: Workflow

7. **Use test tools proportionately.** Use a version-pinned MCP Inspector or SDK test harness only when authorized and in an isolated environment. Record manual probes separately from automated conformance tests and never install or run an unreviewed tool merely because a guide recommends it.

### Source conditional guidance from: Safety and Stop Conditions

Do not use production credentials or real user data for protocol smoke tests without explicit approval. Do not invoke write-capable tools against live targets simply to prove connectivity. Stop if the test harness, server identity, or expected side effects are unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The official MCP specification and Inspector project below informed topic discovery only; no upstream skill text, code, or examples were reused. Verify current test-tool behavior and version compatibility.

- [MCP Specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

2. **Verify discovery and version behavior.** Test `server/discover`, protocol metadata on requests, supported-version reporting, an unsupported-version error, retry with a mutually supported version, and legacy fallback only where claimed.
3. **Test each declared primitive.** Exercise the advertised tools, resources, prompts, pagination, cache hints, and list-change behavior. Include valid, invalid, unauthorized, oversized, and malformed inputs; verify protocol errors versus tool-level failures are distinguished.
5. **Test optional extensions independently.** For each claimed extension (for example Tasks or Skills), verify both sides opt in, unsupported peers follow the documented fallback/rejection, and extension-specific state, integrity, approval, and retention requirements hold.
6. **Exercise failure and recovery.** Cover timeout, disconnect, server restart, duplicate request, stale cursor, cancellation race, wrong protocol metadata, auth failure, and partial external effect. Confirm retries are safe and do not repeat non-idempotent work.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not use production credentials or real user data for protocol smoke tests without explicit approval. Do not invoke write-capable tools against live targets simply to prove connectivity. Stop if the test harness, server identity, or expected side effects are unclear.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

A reviewer can reproduce the supported matrix, see at least one negative case per major boundary, and distinguish tested facts from documentation and assumptions. The release claim is limited to the tested clients, servers, transports, protocol revisions, and extensions.
