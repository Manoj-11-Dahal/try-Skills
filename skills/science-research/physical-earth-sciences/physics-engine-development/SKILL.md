---
name: physics-engine-development
description: "Use when implementing a physics simulation, collision system, rigid-body solver, or particle model for games or interactive scenes to define units, coordinate conventions, timestep, and approximation limits before adding complexity, then test conservation and collision behavior within stated tolerances. Trigger for simulated motion, forces, contacts, or constraints."
---

# Physics Engine Development

## Overview

This skill applies when implementing a physics simulation, collision system, rigid-body solver, or particle model for games or interactive scenes. Its intended outcome is to define units, coordinate conventions, timestep, and approximation limits before adding complexity, then test conservation and collision behavior within stated tolerances.

## When to Use

### Preserved source section: When to Use

Use for numerical simulation of motion, collision, or physical constraints. Distinguish visual plausibility from scientific accuracy and state the intended fidelity.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Units, coordinate system, time scale, bodies, forces, and interaction requirements.
- Target frame rate, stability tolerance, collision geometry, and determinism needs.
- Reference cases, expected tolerances, and whether results affect safety-critical decisions.

## Instructions

### Preserved source section: Procedure

1. **Specify the model.** Define state variables, mass/inertia, force units, gravity, and constraint semantics. Make invalid masses and non-finite values explicit errors.
2. **Choose a timestep strategy.** Prefer a fixed simulation step with bounded catch-up; document integrator choice and stability limitations.
3. **Implement in layers.** Start with free motion, then broad-phase candidate generation, narrow-phase contacts, response, and constraints. Keep rendering interpolation separate from authoritative simulation state.
4. **Handle collisions deliberately.** Test tunneling, resting contacts, corners, zero-area shapes, high speed, and multiple simultaneous contacts.
5. **Preserve reproducibility.** Control update ordering and seeds. Define acceptable floating-point drift and whether the engine promises deterministic results across platforms.
6. **Use invariant-based tests.** Check momentum or energy where the model should conserve it, bounded penetration, no NaNs, and stable behavior across timestep variation.
7. **Profile representative scenes.** Measure candidate counts, solver iterations, and frame time before optimizing.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

State the physical assumptions, units, integrator, collision features, determinism level, and tolerances. Accept only when reference cases remain stable within the declared error bounds and failures are visible rather than silently producing invalid state.

## Output Format

### Preserved source section: Output and Acceptance

State the physical assumptions, units, integrator, collision features, determinism level, and tolerances. Accept only when reference cases remain stable within the declared error bounds and failures are visible rather than silently producing invalid state.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

1. **Specify the model.** Define state variables, mass/inertia, force units, gravity, and constraint semantics. Make invalid masses and non-finite values explicit errors.

### Source edge/failure guidance from: Output and Acceptance

State the physical assumptions, units, integrator, collision features, determinism level, and tolerances. Accept only when reference cases remain stable within the declared error bounds and failures are visible rather than silently producing invalid state.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

State the physical assumptions, units, integrator, collision features, determinism level, and tolerances. Accept only when reference cases remain stable within the declared error bounds and failures are visible rather than silently producing invalid state.
