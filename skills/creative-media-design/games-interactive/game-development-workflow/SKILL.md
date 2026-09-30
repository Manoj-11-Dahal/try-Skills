---
name: game-development-workflow
description: "Use when creating or changing a game loop, gameplay system, level, input model, or simulation to define a small playable slice, separate deterministic game state from presentation, and test controls, collisions, and win or loss conditions before expanding content. Trigger for game prototypes, mechanics, or engine-level changes."
---

# Game Development Workflow

## Overview

This skill applies when creating or changing a game loop, gameplay system, level, input model, or simulation. Its intended outcome is to define a small playable slice, separate deterministic game state from presentation, and test controls, collisions, and win or loss conditions before expanding content.

## When to Use

### Preserved source section: When to Use

Use for games or gameplay systems with update, input, rendering, and state transitions. Keep the first deliverable playable and bounded rather than starting with broad asset or engine infrastructure.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Target platform, player experience, controls, performance budget, and accessibility needs.
- Core mechanic, game states, level or content scope, and success/failure rules.
- Asset, audio, networking, and save-data constraints.

## Instructions

### Preserved source section: Procedure

1. **Define a playable slice.** State the player goal, core action, feedback, and one success or failure condition. Choose placeholder assets where art is not the feature under test.
2. **Separate simulation and presentation.** Model game state and rules independently from drawing and device input. Prefer a fixed simulation step or document the timing strategy.
3. **Implement input and feedback.** Map controls explicitly, handle focus loss and pause, and provide clear visual/audio feedback without making essential information audio-only.
4. **Add movement and collision incrementally.** Specify coordinate units, collision shapes, overlap resolution, and edge behavior. Test high speed, corners, platform boundaries, and simultaneous inputs.
5. **Make progression observable.** Define state transitions for menus, play, pause, win, loss, and restart. Keep save changes deliberate and recoverable.
6. **Test representative sessions.** Verify frame-rate variation, control remapping, keyboard/controller/touch as applicable, audio settings, pause/resume, and restart determinism.
7. **Profile the target device.** Measure frame time, memory, loading, and asset cost on the actual target before optimizing.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Report the playable loop, controls, supported platform, performance measurements, tests, and known usability limits. Accept when a player can complete the stated core loop, failure and restart behavior are stable, and controls remain responsive within the agreed budget.

## Output Format

### Preserved source section: Output and Acceptance

Report the playable loop, controls, supported platform, performance measurements, tests, and known usability limits. Accept when a player can complete the stated core loop, failure and restart behavior are stable, and controls remain responsive within the agreed budget.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Core mechanic, game states, level or content scope, and success/failure rules.

### Source edge/failure guidance from: Procedure

1. **Define a playable slice.** State the player goal, core action, feedback, and one success or failure condition. Choose placeholder assets where art is not the feature under test.

### Source edge/failure guidance from: Output and Acceptance

Report the playable loop, controls, supported platform, performance measurements, tests, and known usability limits. Accept when a player can complete the stated core loop, failure and restart behavior are stable, and controls remain responsive within the agreed budget.

## Stop Conditions

### Source stop-related guidance from: Procedure

3. **Implement input and feedback.** Map controls explicitly, handle focus loss and pause, and provide clear visual/audio feedback without making essential information audio-only.
5. **Make progression observable.** Define state transitions for menus, play, pause, win, loss, and restart. Keep save changes deliberate and recoverable.
6. **Test representative sessions.** Verify frame-rate variation, control remapping, keyboard/controller/touch as applicable, audio settings, pause/resume, and restart determinism.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report the playable loop, controls, supported platform, performance measurements, tests, and known usability limits. Accept when a player can complete the stated core loop, failure and restart behavior are stable, and controls remain responsive within the agreed budget.
