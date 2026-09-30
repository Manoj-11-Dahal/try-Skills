---
name: web-search-engine-development
description: "Use when building a search engine that discovers and indexes web pages, combines crawl and query workflows, or serves web-scale search results to define the authorized crawl scope, access policy, indexing lifecycle, and ranking evaluation before enabling network collection. Trigger for crawlers, link discovery, web indexes, or public-web query services."
---

# Web Search Engine Development

## Overview

This skill applies when building a search engine that discovers and indexes web pages, combines crawl and query workflows, or serves web-scale search results. Its intended outcome is to define the authorized crawl scope, access policy, indexing lifecycle, and ranking evaluation before enabling network collection.

## When to Use

### Preserved source section: When to Use

Use for a system that crawls or searches web pages. For search over a bounded local or application corpus without crawling, use `search-engine-development` instead.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

1. **Constrain collection.** Define allowed hosts and paths. Respect robots directives, site terms, access controls, and rate limits; do not bypass logins, paywalls, CAPTCHAs, or blocks.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Crawl scope, seed URLs, supported content types, and legal/organizational restrictions.
- Robots and rate-limit policy, user-agent identity, refresh schedule, and retention rules.
- Indexing, ranking, freshness, abuse controls, and query latency requirements.

## Instructions

### Preserved source section: Procedure

1. **Constrain collection.** Define allowed hosts and paths. Respect robots directives, site terms, access controls, and rate limits; do not bypass logins, paywalls, CAPTCHAs, or blocks.
2. **Build a polite crawler.** Normalize URLs, prevent loops, deduplicate canonical content, limit depth and bytes, identify the crawler, and back off on errors or server pressure.
3. **Parse defensively.** Treat HTML and metadata as untrusted. Bound decompression and parsing, reject unsafe redirects and schemes, and keep script execution disabled.
4. **Store provenance.** Record source URL, fetch time, status, content hash, and policy decision. Support deletion, recrawl, and stale-document removal.
5. **Index and rank transparently.** Start with lexical retrieval, document ranking features, and snippets. Evaluate freshness and relevance separately; keep ranking signals inspectable.
6. **Protect query users and sources.** Rate-limit abusive queries, avoid leaking sensitive query strings in logs, and apply removal or opt-out policies where required.
7. **Test with a controlled corpus.** Use owned pages and fixtures to verify crawl boundaries, duplicate handling, parser failures, ranking, refresh, and deletion.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Acceptance

No broad public crawling or production indexing is authorized by implementing the skill. Require explicit approval for network collection at scale. Accept when the crawler stays within scope, honors rate controls, preserves provenance, and reliably removes stale or disallowed documents.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Build a polite crawler.** Normalize URLs, prevent loops, deduplicate canonical content, limit depth and bytes, identify the crawler, and back off on errors or server pressure.
7. **Test with a controlled corpus.** Use owned pages and fixtures to verify crawl boundaries, duplicate handling, parser failures, ranking, refresh, and deletion.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

No broad public crawling or production indexing is authorized by implementing the skill. Require explicit approval for network collection at scale. Accept when the crawler stays within scope, honors rate controls, preserves provenance, and reliably removes stale or disallowed documents.
