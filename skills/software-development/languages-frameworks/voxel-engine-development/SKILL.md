---
name: voxel-engine-development
description: "Use when building a voxel renderer, terrain system, chunk store, or voxel-world interaction to define world coordinates, chunk dimensions, block representation, generation rules, and resource budgets before optimizing mesh or streaming behavior. Trigger for block-based worlds, voxel meshing, terrain, or chunk persistence."
---

# Voxel Engine Development

## Overview

This skill applies when building a voxel renderer, terrain system, chunk store, or voxel-world interaction. Its intended outcome is to define world coordinates, chunk dimensions, block representation, generation rules, and resource budgets before optimizing mesh or streaming behavior.

## When to Use

### Preserved source section: When to Use

Use for a world represented as a regular grid of discrete cells, often partitioned into chunks. Distinguish voxel storage and simulation from polygon rendering and general 3D rendering.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- World coordinate system, voxel size, chunk dimensions, and block/material schema.
- Terrain generation, editing, persistence, lighting, collision, and multiplayer requirements.
- Memory, draw-call, streaming, and target-device budgets.

## Instructions

### Preserved source section: Procedure

1. **Define coordinates and ownership.** Specify world-to-chunk mapping for negative and positive coordinates, local cell indexing, boundary conventions, and overflow behavior.
2. **Choose a compact representation.** Define block IDs, metadata, empty space, and versioning. Validate unknown or corrupt values when loading chunks.
3. **Build a visible chunk.** Generate a tiny deterministic world, emit only exposed faces, and verify normals, winding, texture/material assignment, and seam alignment.
4. **Separate generation and meshing.** Make terrain generation seeded and reproducible. Rebuild only affected chunks when blocks change; document neighbor dependencies at boundaries.
5. **Add streaming under budgets.** Prioritize nearby chunks, cap queued work and memory, cancel obsolete tasks, and avoid blocking the main/render thread on disk or generation.
6. **Test boundaries and edits.** Cover negative coordinates, chunk seams, empty/full chunks, edits at shared edges, persistence/reload, and deterministic generation.
7. **Measure before advanced meshing.** Record visible face count, generation time, memory, and frame time before adopting greedy meshing or level-of-detail complexity.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

2. **Choose a compact representation.** Define block IDs, metadata, empty space, and versioning. Validate unknown or corrupt values when loading chunks.
4. **Separate generation and meshing.** Make terrain generation seeded and reproducible. Rebuild only affected chunks when blocks change; document neighbor dependencies at boundaries.

### Source conditional guidance from: Output and Acceptance

Report grid conventions, chunk format, generation seed, meshing strategy, streaming budget, and supported world size. Accept when adjacent chunks align, edits persist as specified, and resource use remains within the declared budget.

## Output Format

### Preserved source section: Output and Acceptance

Report grid conventions, chunk format, generation seed, meshing strategy, streaming budget, and supported world size. Accept when adjacent chunks align, edits persist as specified, and resource use remains within the declared budget.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report grid conventions, chunk format, generation seed, meshing strategy, streaming budget, and supported world size. Accept when adjacent chunks align, edits persist as specified, and resource use remains within the declared budget.
