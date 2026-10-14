---
name: network-stack-development
description: "Use when implementing packet parsing, transport behavior, protocol layering, or a network-stack component to select a bounded protocol subset, define byte-level invariants and state transitions, and validate malformed traffic in an isolated test harness before opening sockets. Trigger for link, network, or transport protocol work."
---

# Network Stack Development

## Overview

This skill applies when implementing packet parsing, transport behavior, protocol layering, or a network-stack component. Its intended outcome is to select a bounded protocol subset, define byte-level invariants and state transitions, and validate malformed traffic in an isolated test harness before opening sockets.

## When to Use

### Preserved source section: When to Use

Use for packet or protocol implementation below the application layer. Name the exact protocols and features in scope; do not imply full standards compliance from a small parser or loopback demo.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use for packet or protocol implementation below the application layer. Name the exact protocols and features in scope; do not imply full standards compliance from a small parser or loopback demo.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Protocol specifications and target layer boundaries.
- Supported address families, MTU, packet sizes, timeouts, and concurrency limits.
- Synthetic packet fixtures, loopback harness, and permission for any live network activity.

## Instructions

### Preserved source section: Procedure

1. **Define the subset.** Specify header fields, byte order, checksum rules, optional extensions, fragmentation or retransmission behavior, and explicit unsupported cases.
2. **Implement bounded parsers.** Validate lengths before reading fields, reject truncated or inconsistent packets, and cap allocation and nesting. Keep parsing separate from state mutation.
3. **Model state machines.** Define legal transitions, timeout behavior, duplicate handling, and cleanup for each connection or protocol exchange.
4. **Use synthetic tests first.** Test valid vectors, malformed lengths, invalid checksums, reordered and duplicated packets, timeout, and resource exhaustion without transmitting on a live interface.
5. **Add loopback integration.** Keep addresses and ports isolated, and test interoperability against a known implementation only within authorized boundaries.
6. **Review operational risk.** Avoid raw sockets, packet injection, scanning, spoofing, or firewall changes unless specifically authorized and necessary.
7. **Measure and document.** Record throughput, latency, loss behavior, and memory under declared conditions; profile only after correctness.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

6. **Review operational risk.** Avoid raw sockets, packet injection, scanning, spoofing, or firewall changes unless specifically authorized and necessary.

### Source conditional guidance from: Output and Acceptance

Report implemented layers, protocol version/features, parser limits, state behavior, test vectors, and network permissions used. Accept when boundary cases are rejected safely, valid vectors are handled correctly, and no unapproved network side effect occurs.

## Output Format

### Preserved source section: Output and Acceptance

Report implemented layers, protocol version/features, parser limits, state behavior, test vectors, and network permissions used. Accept when boundary cases are rejected safely, valid vectors are handled correctly, and no unapproved network side effect occurs.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Supported address families, MTU, packet sizes, timeouts, and concurrency limits.

### Source edge/failure guidance from: Procedure

3. **Model state machines.** Define legal transitions, timeout behavior, duplicate handling, and cleanup for each connection or protocol exchange.
4. **Use synthetic tests first.** Test valid vectors, malformed lengths, invalid checksums, reordered and duplicated packets, timeout, and resource exhaustion without transmitting on a live interface.

### Source edge/failure guidance from: Output and Acceptance

Report implemented layers, protocol version/features, parser limits, state behavior, test vectors, and network permissions used. Accept when boundary cases are rejected safely, valid vectors are handled correctly, and no unapproved network side effect occurs.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report implemented layers, protocol version/features, parser limits, state behavior, test vectors, and network permissions used. Accept when boundary cases are rejected safely, valid vectors are handled correctly, and no unapproved network side effect occurs.
