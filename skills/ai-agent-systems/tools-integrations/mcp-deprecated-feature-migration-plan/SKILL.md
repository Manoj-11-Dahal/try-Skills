---
name: mcp-deprecated-feature-migration-plan
description: "Use when upgrading an MCP client, server, SDK, or deployment and identifying protocol features that are deprecated in the target revision to produce a versioned inventory, migration plan, compatibility window, owners, and regression tests. Success means each deprecated use is mapped to the current migration path, new code does not adopt deprecated behavior by default, and existing clients remain supported only through an explicit, tested transition plan. Recheck the live deprecation registry before scheduling work."
---

# MCP Deprecated Feature Migration Plan

## Overview

This skill applies when upgrading an MCP client, server, SDK, or deployment and identifying protocol features that are deprecated in the target revision. Its intended outcome is to produce a versioned inventory, migration plan, compatibility window, owners, and regression tests.

## When to Use

### Preserved source section: When to Use

Use this workflow during an MCP protocol or SDK upgrade, dependency review, or interoperability audit. It is a migration-planning skill: it identifies deprecated features and their replacements without authorizing code changes or removing legacy support on its own.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Inputs and Boundaries

Record source and target protocol revisions, client/server roles, SDK versions, transports, extension use, supported host versions, deployment dates, owners, and rollback criteria. Use the official deprecation registry for the target revision; do not rely on old blog summaries or assume a deprecation has already become removal.

### Source boundary statements from: Workflow

4. **Choose a phased plan.** Define a non-deprecated default, a compatibility adapter where needed, client/server owners, support window, telemetry, rollback, and removal criteria. Do not silently change authentication, tool behavior, or data boundaries as a side effect of a protocol migration.

### Source boundary statements from: Safety and Stop Conditions

Do not remove a legacy path that active clients still require without an approved transition. Do not claim interoperability from a single successful test. Stop if the target revision, support window, or replacement path is unresolved.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record source and target protocol revisions, client/server roles, SDK versions, transports, extension use, supported host versions, deployment dates, owners, and rollback criteria. Use the official deprecation registry for the target revision; do not rely on old blog summaries or assume a deprecation has already become removal.

## Instructions

### Preserved source section: Workflow

1. **Pin the target revision.** Capture the protocol version and current deprecation page date. Separate normative requirements from planned migration and locally supported compatibility policy.
2. **Inventory feature usage.** Search code, configuration, tests, deployment settings, documentation, and telemetry for deprecated methods or modes. Record which client/server, transport, version, and user flow depends on each.
3. **Map the migration.** For the 2026-07-28 registry, review at least: Roots (pass paths via tool parameters, resource URIs, or server configuration); Sampling (new implementations should call provider APIs directly); Logging (use stderr for STDIO diagnostics or OpenTelemetry for observability); Dynamic Client Registration (prefer Client ID Metadata Documents, retaining DCR only as compatibility requires); and HTTP+SSE (move to Streamable HTTP). Check deprecated sampling context options and other entries in the target registry.
4. **Choose a phased plan.** Define a non-deprecated default, a compatibility adapter where needed, client/server owners, support window, telemetry, rollback, and removal criteria. Do not silently change authentication, tool behavior, or data boundaries as a side effect of a protocol migration.
5. **Test both sides of the transition.** Verify the new path, expected rejection/fallback for old peers, user-visible diagnostics, and failure recovery. Test a representative client/server matrix rather than assuming all SDKs adopt the same revision at once.
6. **Close the migration.** Record evidence that deprecated behavior is no longer used by supported configurations or is isolated behind a named compatibility path. Recheck the registry before declaring the migration complete.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Acceptance Evidence

The plan includes a source-to-replacement map, target revision, client/server compatibility matrix, owners, deadlines, regression tests, rollback path, and unresolved dependencies. A feature marked Deprecated is treated as still present but not appropriate for new adoption; removal is asserted only when the specification says it is removed.

### Source conditional guidance from: Safety and Stop Conditions

Do not remove a legacy path that active clients still require without an approved transition. Do not claim interoperability from a single successful test. Stop if the target revision, support window, or replacement path is unresolved.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The current official registry and versioning documentation below informed topic discovery only; no upstream skill text or examples were copied. Recheck current status because deprecation and removal dates may change.

- [MCP Deprecated Features registry](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)
- [MCP Versioning and Compatibility](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
- [MCP Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

5. **Test both sides of the transition.** Verify the new path, expected rejection/fallback for old peers, user-visible diagnostics, and failure recovery. Test a representative client/server matrix rather than assuming all SDKs adopt the same revision at once.

### Source edge/failure guidance from: Acceptance Evidence

The plan includes a source-to-replacement map, target revision, client/server compatibility matrix, owners, deadlines, regression tests, rollback path, and unresolved dependencies. A feature marked Deprecated is treated as still present but not appropriate for new adoption; removal is asserted only when the specification says it is removed.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not remove a legacy path that active clients still require without an approved transition. Do not claim interoperability from a single successful test. Stop if the target revision, support window, or replacement path is unresolved.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The plan includes a source-to-replacement map, target revision, client/server compatibility matrix, owners, deadlines, regression tests, rollback path, and unresolved dependencies. A feature marked Deprecated is treated as still present but not appropriate for new adoption; removal is asserted only when the specification says it is removed.
