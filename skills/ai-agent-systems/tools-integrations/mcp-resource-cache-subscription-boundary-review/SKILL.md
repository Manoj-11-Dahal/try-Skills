---
name: mcp-resource-cache-subscription-boundary-review
description: "Use when designing or auditing MCP resources, paginated discovery, response caching, or change subscriptions, especially when visibility depends on the caller’s authorization to review resource URIs, cache keys, TTL, public/private scope, pagination, invalidation, subscription filters, and reconnect behavior. Success means private data cannot cross authorization contexts, stale results are invalidated or refreshed appropriately, and cursors and subscription IDs are handled as opaque protocol values."
---

# MCP Resource Cache and Subscription Boundary Review

## Overview

This skill applies when designing or auditing MCP resources, paginated discovery, response caching, or change subscriptions, especially when visibility depends on the caller’s authorization. Its intended outcome is to review resource URIs, cache keys, TTL, public/private scope, pagination, invalidation, subscription filters, and reconnect behavior.

## When to Use

### Preserved source section: When to Use

Use this workflow for MCP resources and other cacheable list results when a client, server, or gateway must balance freshness, performance, authorization, pagination, and pushed updates. It complements resource exposure and authentication reviews but does not define the resource’s business semantics.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Workflow

3. **Set freshness deliberately.** Treat `ttlMs` as a freshness hint, not a guarantee that data cannot change before expiry. Define when to re-fetch, how errors are handled, and whether stale data may be served during a failed refresh. Do not cache an `input_required` result or a retry carrying `inputResponses`/`requestState` as though it were a stable response.
4. **Handle paginated lists.** Treat cursors as opaque tokens, continue until `nextCursor` is absent, and cache each page independently. Do not assume fixed page sizes or a consistent snapshot across pages; plan deduplication and gap detection if the underlying collection may change.

### Source boundary statements from: Safety and Stop Conditions

Never use a shared cache for `private` results. Do not parse or modify opaque cursors or subscription identifiers. Stop if the server cannot determine whether a result is user-specific or if a change notification cannot be tied to the relevant cached data.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record protocol revision, resource URI scheme, caller/authentication context, list filters and cursors, `ttlMs`, `cacheScope`, server capabilities, notification filters, cache layers, and data classification. Identify whether results vary by user, tenant, scope, or request parameters.

## Instructions

### Preserved source section: Workflow

1. **Define resource identity and visibility.** Give each resource a stable URI and determine which callers may list or read it. Verify that resource lists may vary by request authorization as intended and that no per-user result is exposed as a global catalog.
2. **Set cache keys and scope.** Key cached results by method and all result-affecting parameters, such as resource URI or page cursor. Use `public` only for results safe to share across users; use `private` for caller-specific content and isolate private cache entries by authorization context.
3. **Set freshness deliberately.** Treat `ttlMs` as a freshness hint, not a guarantee that data cannot change before expiry. Define when to re-fetch, how errors are handled, and whether stale data may be served during a failed refresh. Do not cache an `input_required` result or a retry carrying `inputResponses`/`requestState` as though it were a stable response.
4. **Handle paginated lists.** Treat cursors as opaque tokens, continue until `nextCursor` is absent, and cache each page independently. Do not assume fixed page sizes or a consistent snapshot across pages; plan deduplication and gap detection if the underlying collection may change.
5. **Use change subscriptions safely.** Request only the notification types and resource URIs needed through `subscriptions/listen`. Check the acknowledged filter, correlate every event with its subscription ID, invalidate relevant cache entries, and re-establish subscriptions after disconnect when required.
6. **Test authorization and staleness.** Exercise cross-user cache attempts, scope changes, URI changes, expired TTL, early invalidation, page cursors, invalid cursors, repeated notifications, and reconnect. Verify no result from one authorization context can be served to another.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

3. **Set freshness deliberately.** Treat `ttlMs` as a freshness hint, not a guarantee that data cannot change before expiry. Define when to re-fetch, how errors are handled, and whether stale data may be served during a failed refresh. Do not cache an `input_required` result or a retry carrying `inputResponses`/`requestState` as though it were a stable response.
4. **Handle paginated lists.** Treat cursors as opaque tokens, continue until `nextCursor` is absent, and cache each page independently. Do not assume fixed page sizes or a consistent snapshot across pages; plan deduplication and gap detection if the underlying collection may change.
5. **Use change subscriptions safely.** Request only the notification types and resource URIs needed through `subscriptions/listen`. Check the acknowledged filter, correlate every event with its subscription ID, invalidate relevant cache entries, and re-establish subscriptions after disconnect when required.

### Source conditional guidance from: Safety and Stop Conditions

Never use a shared cache for `private` results. Do not parse or modify opaque cursors or subscription identifiers. Stop if the server cannot determine whether a result is user-specific or if a change notification cannot be tied to the relevant cached data.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The official resources, caching, pagination, and subscription pages below informed topic discovery only; no upstream skill text or examples were copied. Confirm the protocol revision before implementation.

- [MCP Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [MCP Caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching)
- [MCP Pagination](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination)
- [MCP Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

3. **Set freshness deliberately.** Treat `ttlMs` as a freshness hint, not a guarantee that data cannot change before expiry. Define when to re-fetch, how errors are handled, and whether stale data may be served during a failed refresh. Do not cache an `input_required` result or a retry carrying `inputResponses`/`requestState` as though it were a stable response.
6. **Test authorization and staleness.** Exercise cross-user cache attempts, scope changes, URI changes, expired TTL, early invalidation, page cursors, invalid cursors, repeated notifications, and reconnect. Verify no result from one authorization context can be served to another.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Never use a shared cache for `private` results. Do not parse or modify opaque cursors or subscription identifiers. Stop if the server cannot determine whether a result is user-specific or if a change notification cannot be tied to the relevant cached data.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The record includes resource visibility, cache-key dimensions, `ttlMs`, `cacheScope`, pagination behavior, notification filters and acknowledgment, invalidation, and cross-context tests. Cache freshness and data authorization are evaluated separately.
