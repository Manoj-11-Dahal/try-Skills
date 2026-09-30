---
name: mcp-skills-extension-interoperability-review
description: "Use when exposing, discovering, or loading Agent Skills through the MCP Skills extension `io.modelcontextprotocol/skills` to review capability declaration, skills/list and skills/get, resource manifests, URI identity, digest verification, cache origin, directoryRead support, user approval, and activation behavior. Success means skill content is loaded only from its approved server and verified manifest, and reading a SKILL.md is not mistaken for permission to activate or execute it."
---

# MCP Skills Extension Interoperability Review

## Overview

This skill applies when exposing, discovering, or loading Agent Skills through the MCP Skills extension `io.modelcontextprotocol/skills`. Its intended outcome is to review capability declaration, skills/list and skills/get, resource manifests, URI identity, digest verification, cache origin, directoryRead support, user approval, and activation behavior.

## When to Use

### Preserved source section: When to Use

Use this workflow when a host, client, or server implements the official Skills-over-MCP extension. The extension reuses MCP Resources to discover and retrieve Agent Skills; it does not make arbitrary remote skill content trustworthy.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Workflow

6. **Handle updates and dynamic content.** If any file URI, digest, size, or frontmatter changes, refresh the entry and renew approval. Treat `resources: "dynamic"` as content without stable manifest hashes; do not extend a prior approval to arbitrary future content.

### Source boundary statements from: Safety and Stop Conditions

Treat skill content and its declared tool permissions as untrusted input. Do not allow skill files to silently replace a same-name local skill, escape the approved server origin, or grant tools without user approval. Stop if the host cannot verify content or maintain its origin through caching and restart.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the MCP server identity, protocol revision, extension identifier/settings, SDK/client support, skill URI namespace, frontmatter, resource manifest, digest algorithm, cache behavior, approval policy, and whether supporting files or directory reads are used. Verify current extension support because client implementations may differ.

## Instructions

### Preserved source section: Workflow

1. **Check extension declaration.** Confirm the server declares both Resources support and `io.modelcontextprotocol/skills` through `server/discover`. Clients should issue `skills/list` and `skills/get` only after observing the declaration; `directoryRead` is optional and defaults off.
2. **Validate listing and lookup.** Check that `skills/list` returns complete entries with frontmatter and a complete file manifest, while `skills/get` can retrieve a specific skill by URI even if it was not listed. Treat skill identity as the pair of originating server and URI; names alone may collide.
3. **Verify the manifest.** For every served file, compare raw byte size and SHA-256 digest with the manifest, parse `SKILL.md` frontmatter, and compare it with the listed metadata. Restrict supporting-file reads to manifest URIs and resolve relative paths within the skill root.
4. **Separate integrity from trust.** A matching digest proves consistency with the server’s manifest, not that the skill is safe or authoritative. Review the server’s publisher, permissions, data flows, scripts, and references under the host’s normal supply-chain policy.
5. **Enforce user approval and activation.** Preserve the server origin in the approval record and cache. Loading a skill requires the host’s skill-loading path and any required user approval; reading a file as a resource does not by itself activate the skill. A nested skill needs fresh consent before activation.
6. **Handle updates and dynamic content.** If any file URI, digest, size, or frontmatter changes, refresh the entry and renew approval. Treat `resources: "dynamic"` as content without stable manifest hashes; do not extend a prior approval to arbitrary future content.
7. **Test failures.** Exercise unknown URI, incomplete listing, missing file, digest/size mismatch, same-name skills from two servers, unauthorized cross-server reads, directoryRead disabled, and approval denial. On failure, refuse to load the content.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

2. **Validate listing and lookup.** Check that `skills/list` returns complete entries with frontmatter and a complete file manifest, while `skills/get` can retrieve a specific skill by URI even if it was not listed. Treat skill identity as the pair of originating server and URI; names alone may collide.
6. **Handle updates and dynamic content.** If any file URI, digest, size, or frontmatter changes, refresh the entry and renew approval. Treat `resources: "dynamic"` as content without stable manifest hashes; do not extend a prior approval to arbitrary future content.

### Source conditional guidance from: Safety and Stop Conditions

Treat skill content and its declared tool permissions as untrusted input. Do not allow skill files to silently replace a same-name local skill, escape the approved server origin, or grant tools without user approval. Stop if the host cannot verify content or maintain its origin through caching and restart.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The official MCP Skills extension and its final design record informed topic discovery only; no upstream skill text or examples were copied. Verify the extension revision and host support matrix.

- [MCP Skills extension overview](https://modelcontextprotocol.io/extensions/skills/overview)
- [SEP-2640: Skills Extension](https://modelcontextprotocol.io/seps/2640-skills-extension)
- [Skills Over MCP Working Group](https://modelcontextprotocol.io/community/working-groups/skills-over-mcp)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

7. **Test failures.** Exercise unknown URI, incomplete listing, missing file, digest/size mismatch, same-name skills from two servers, unauthorized cross-server reads, directoryRead disabled, and approval denial. On failure, refuse to load the content.

### Source edge/failure guidance from: Acceptance Evidence

The evidence records server+URI identity, extension support, listing/get behavior, byte/hash/frontmatter verification, approval and activation path, cache isolation, and failure handling. No remote skill is auto-activated solely because it appeared in a listing.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Treat skill content and its declared tool permissions as untrusted input. Do not allow skill files to silently replace a same-name local skill, escape the approved server origin, or grant tools without user approval. Stop if the host cannot verify content or maintain its origin through caching and restart.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The evidence records server+URI identity, extension support, listing/get behavior, byte/hash/frontmatter verification, approval and activation path, cache isolation, and failure handling. No remote skill is auto-activated solely because it appeared in a listing.
