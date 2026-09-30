---
name: bittorrent-client-development
description: "Use when implementing or reviewing a BitTorrent client, parser, peer protocol, or piece-transfer workflow to start with a bounded, lawful test torrent and validate metainfo, peer messages, piece hashes, file paths, and resource limits before enabling broader networking. Trigger for BitTorrent-compatible download or seeding behavior."
---

# BitTorrent Client Development

## Overview

This skill applies when implementing or reviewing a BitTorrent client, parser, peer protocol, or piece-transfer workflow. Its intended outcome is to start with a bounded, lawful test torrent and validate metainfo, peer messages, piece hashes, file paths, and resource limits before enabling broader networking.

## When to Use

### Preserved source section: When to Use

Use for a protocol-learning implementation or a client that exchanges torrent pieces with peers. Keep interoperability claims tied to the exact protocol version and features implemented.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

1. **Choose a small lawful scope.** Begin with a self-generated or explicitly licensed fixture, loopback peers, and one file. Do not use the implementation to obtain or distribute content without rights.

### Source boundary statements from: Safety and Acceptance

Do not bind privileged ports, scan peer networks, evade access controls, or silently seed. Enforce connection, memory, disk, and rate limits. A valid acceptance run downloads only the authorized fixture, verifies its pieces, writes only inside the selected directory, and stops or seeds according to the user's explicit setting.

### Source boundary statements from: Output

Report protocol features supported, fixture provenance, integrity checks, filesystem safeguards, networking behavior, and known interoperability gaps. Never describe a narrow teaching client as a complete production client.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Authorized test content and a controlled tracker or peer test setup.
- Required protocol subset, supported transports, file sizes, and concurrency budget.
- Storage policy, destination directory, seeding policy, and user-visible controls.

## Instructions

### Preserved source section: Procedure

1. **Choose a small lawful scope.** Begin with a self-generated or explicitly licensed fixture, loopback peers, and one file. Do not use the implementation to obtain or distribute content without rights.
2. **Parse metainfo defensively.** Implement the selected bencoding rules, preserve exact byte sequences where hashes depend on them, validate lengths and piece metadata, and reject malformed or oversized inputs.
3. **Verify peer exchange.** Add peer identity and handshake handling, message framing, state transitions, and timeouts. Reject invalid lengths, unexpected messages, and excessive connections.
4. **Transfer bounded pieces.** Request blocks within protocol limits, assemble pieces in a controlled buffer, verify each piece hash before writing, and handle duplicate, missing, or corrupt blocks safely.
5. **Protect filesystem state.** Resolve output paths beneath the chosen destination, reject traversal and symlink escapes, avoid overwriting unrelated files, and use temporary files until integrity checks pass.
6. **Add discovery carefully.** Introduce tracker or peer discovery only after local transfer works. Make public-IP exposure, outbound connections, seeding, and stop controls explicit.
7. **Exercise failures.** Test corrupt metadata, truncated messages, peer disconnects, timeouts, disk errors, duplicate blocks, restart/resume, and resource exhaustion.

## Decision Rules

Not specified in source skill.

## Output Format

### Preserved source section: Output

Report protocol features supported, fixture provenance, integrity checks, filesystem safeguards, networking behavior, and known interoperability gaps. Never describe a narrow teaching client as a complete production client.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

2. **Parse metainfo defensively.** Implement the selected bencoding rules, preserve exact byte sequences where hashes depend on them, validate lengths and piece metadata, and reject malformed or oversized inputs.
3. **Verify peer exchange.** Add peer identity and handshake handling, message framing, state transitions, and timeouts. Reject invalid lengths, unexpected messages, and excessive connections.
7. **Exercise failures.** Test corrupt metadata, truncated messages, peer disconnects, timeouts, disk errors, duplicate blocks, restart/resume, and resource exhaustion.

## Stop Conditions

### Source stop-related guidance from: Procedure

6. **Add discovery carefully.** Introduce tracker or peer discovery only after local transfer works. Make public-IP exposure, outbound connections, seeding, and stop controls explicit.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Do not bind privileged ports, scan peer networks, evade access controls, or silently seed. Enforce connection, memory, disk, and rate limits. A valid acceptance run downloads only the authorized fixture, verifies its pieces, writes only inside the selected directory, and stops or seeds according to the user's explicit setting.
