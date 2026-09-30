---
name: blockchain-cryptocurrency-development
description: "Use when designing or implementing a blockchain, cryptocurrency ledger, wallet prototype, transaction format, or consensus experiment to separate educational simulation from production financial systems, define state-transition invariants, and use vetted cryptographic libraries rather than inventing primitives. Trigger for ledger, token, block, transaction, wallet, or chain-reorganization work."
---

# Blockchain and Cryptocurrency Development

## Overview

This skill applies when designing or implementing a blockchain, cryptocurrency ledger, wallet prototype, transaction format, or consensus experiment. Its intended outcome is to separate educational simulation from production financial systems, define state-transition invariants, and use vetted cryptographic libraries rather than inventing primitives.

## When to Use

### Preserved source section: When to Use

Use for a bounded ledger or protocol implementation. First identify whether the goal is an educational simulation, a private test network, or a production system; do not let prototype code handle real funds by default.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Safety Boundaries

Never deploy contracts, broadcast transactions, move funds, or store production credentials without specific authorization. A correct hash or passing unit suite does not establish consensus safety or financial suitability.

### Source boundary statements from: When to Use

Use for a bounded ledger or protocol implementation. First identify whether the goal is an educational simulation, a private test network, or a production system; do not let prototype code handle real funds by default.

### Source boundary statements from: Procedure

2. **Use established cryptography.** Select maintained libraries and standard algorithms. Never invent a signature scheme, hash function, key derivation method, or randomness source.
5. **Protect keys and funds.** Do not log private keys or seed phrases. Use test keys and test networks; require explicit confirmation for signing or broadcast actions. Treat remote RPC responses as untrusted input.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The threat model, participants, trust assumptions, and desired consistency model.
- Transaction, block, state, fee, identity, and consensus requirements.
- Cryptographic libraries, test vectors, test-network boundaries, and key-handling rules.

## Instructions

### Preserved source section: Procedure

1. **Specify invariants.** Define canonical transaction encoding, authorization, replay protection, ordering, state-transition rules, and what constitutes a valid chain. Write invariants before networking or token economics.
2. **Use established cryptography.** Select maintained libraries and standard algorithms. Never invent a signature scheme, hash function, key derivation method, or randomness source.
3. **Implement deterministic state transitions.** Validate signatures and nonces, reject invalid or duplicate transactions, compute state changes predictably, and make serialization unambiguous.
4. **Add blocks and consensus as separate layers.** For a teaching prototype, use a clearly labeled toy consensus model. Document forks, finality, reorganization behavior, and limits before exposing a network interface.
5. **Protect keys and funds.** Do not log private keys or seed phrases. Use test keys and test networks; require explicit confirmation for signing or broadcast actions. Treat remote RPC responses as untrusted input.
6. **Test adversarial cases.** Include malformed encodings, invalid signatures, replayed transactions, conflicting spends, reordered messages, chain forks, and restart/recovery scenarios.
7. **Review economic and operational assumptions.** Separate protocol correctness from token valuation, compliance, and security claims. Request specialized human review before any real-money use.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

State the prototype boundary, threat assumptions, invariants, crypto dependencies, test network, and unimplemented attack surfaces. Accept only the declared simulation or test scope; label production readiness as unassessed unless it has undergone independent security and operational review.

## Output Format

### Preserved source section: Output and Acceptance

State the prototype boundary, threat assumptions, invariants, crypto dependencies, test network, and unimplemented attack surfaces. Accept only the declared simulation or test scope; label production readiness as unassessed unless it has undergone independent security and operational review.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

3. **Implement deterministic state transitions.** Validate signatures and nonces, reject invalid or duplicate transactions, compute state changes predictably, and make serialization unambiguous.
6. **Test adversarial cases.** Include malformed encodings, invalid signatures, replayed transactions, conflicting spends, reordered messages, chain forks, and restart/recovery scenarios.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

State the prototype boundary, threat assumptions, invariants, crypto dependencies, test network, and unimplemented attack surfaces. Accept only the declared simulation or test scope; label production readiness as unassessed unless it has undergone independent security and operational review.
