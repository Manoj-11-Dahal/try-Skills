---
name: mcp-streamable-http-stateless-deployment-review
description: "Use when deploying, upgrading, or auditing an MCP server over Streamable HTTP, especially when moving from session-based or HTTP+SSE behavior to the 2026-07-28 stateless request model to review the endpoint, POST/SSE flow, request metadata, Origin validation, authentication, subscriptions, cancellation, and legacy compatibility. Success means each request is correctly scoped, network exposure is intentional, and no deprecated stream/session assumption creates a security or interoperability gap."
---

# MCP Streamable HTTP Stateless Deployment Review

## Overview

This skill applies when deploying, upgrading, or auditing an MCP server over Streamable HTTP, especially when moving from session-based or HTTP+SSE behavior to the 2026-07-28 stateless request model. Its intended outcome is to review the endpoint, POST/SSE flow, request metadata, Origin validation, authentication, subscriptions, cancellation, and legacy compatibility.

## When to Use

### Preserved source section: When to Use

Use this workflow for a remote MCP endpoint or a local HTTP server that can be reached by a browser or another network client. It focuses on transport and deployment boundaries, not general tool quality or OAuth implementation details.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Workflow

2. **Trace request and response framing.** Verify each request body is one permitted JSON-RPC request or notification, request metadata is present, and response handling supports a JSON object or a request-scoped SSE stream. Keep long-lived change delivery on an explicitly opened `subscriptions/listen` request; do not send unrelated server-initiated requests on a tool response stream.
4. **Review network safeguards.** Validate `Origin` on incoming requests; reject a present but invalid origin with 403 and test DNS-rebinding defenses. Do not assume missing `Origin` is equivalent to a valid one. Bind a local-only server to loopback, not all interfaces, and require suitable authentication for remote exposure.
5. **Verify cancellation and lifecycle.** Check that a client closing a request-scoped SSE response cancels the associated work, while a subscription stream has its own lifecycle and reconnect behavior. Ensure a partial disconnect cannot duplicate an external side effect.

### Source boundary statements from: Safety and Stop Conditions

Do not bind an unapproved server to a public interface or expose credentials to browser-origin traffic. Do not disable origin checks to make an integration pass. Stop if proxy behavior, authentication ownership, or the allowed network boundary is unclear.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the protocol revision, endpoint and hostnames, server/SDK version, reverse proxies, allowed origins, authentication mode, response types, subscriptions, client versions, network exposure, and rollout/rollback owner. Perform tests only in a controlled environment with explicit authorization.

## Instructions

### Preserved source section: Workflow

1. **Confirm transport revision.** For the 2026-07-28 Streamable HTTP model, expect one MCP endpoint, client messages sent as HTTP POSTs, no protocol-level session, and no GET stream endpoint. Treat older session/HTTP+SSE behavior as a separate compatibility path.
2. **Trace request and response framing.** Verify each request body is one permitted JSON-RPC request or notification, request metadata is present, and response handling supports a JSON object or a request-scoped SSE stream. Keep long-lived change delivery on an explicitly opened `subscriptions/listen` request; do not send unrelated server-initiated requests on a tool response stream.
3. **Check metadata consistency.** Confirm the protocol version and client metadata in the message body are the source of truth. If the transport mirrors fields into HTTP headers, test mismatch handling, routing, proxy behavior, and logging redaction.
4. **Review network safeguards.** Validate `Origin` on incoming requests; reject a present but invalid origin with 403 and test DNS-rebinding defenses. Do not assume missing `Origin` is equivalent to a valid one. Bind a local-only server to loopback, not all interfaces, and require suitable authentication for remote exposure.
5. **Verify cancellation and lifecycle.** Check that a client closing a request-scoped SSE response cancels the associated work, while a subscription stream has its own lifecycle and reconnect behavior. Ensure a partial disconnect cannot duplicate an external side effect.
6. **Plan backward compatibility.** Inventory clients using earlier HTTP+SSE/session semantics. Isolate any compatibility adapter, set a retirement owner/date, and test both the supported legacy path and the modern stateless path.
7. **Test the deployment boundary.** Exercise allowed/denied origins, unauthenticated access, unexpected methods, malformed metadata, oversized requests, SSE buffering, proxy timeouts, server shutdown, and loopback exposure. Use synthetic data and non-production credentials.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

3. **Check metadata consistency.** Confirm the protocol version and client metadata in the message body are the source of truth. If the transport mirrors fields into HTTP headers, test mismatch handling, routing, proxy behavior, and logging redaction.

### Source conditional guidance from: Safety and Stop Conditions

Do not bind an unapproved server to a public interface or expose credentials to browser-origin traffic. Do not disable origin checks to make an integration pass. Stop if proxy behavior, authentication ownership, or the allowed network boundary is unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The official transport and security references below informed topic discovery; no upstream skill text or sample configuration was copied. Verify the exact spec and SDK version in use.

- [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [Transport Overview](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

4. **Review network safeguards.** Validate `Origin` on incoming requests; reject a present but invalid origin with 403 and test DNS-rebinding defenses. Do not assume missing `Origin` is equivalent to a valid one. Bind a local-only server to loopback, not all interfaces, and require suitable authentication for remote exposure.
7. **Test the deployment boundary.** Exercise allowed/denied origins, unauthenticated access, unexpected methods, malformed metadata, oversized requests, SSE buffering, proxy timeouts, server shutdown, and loopback exposure. Use synthetic data and non-production credentials.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not bind an unapproved server to a public interface or expose credentials to browser-origin traffic. Do not disable origin checks to make an integration pass. Stop if proxy behavior, authentication ownership, or the allowed network boundary is unclear.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The record shows endpoint topology, protocol era, request/response behavior, Origin/auth checks, cancellation, subscription lifecycle, proxy settings, legacy support, and rollback. A local successful call alone does not prove safe public deployment.
