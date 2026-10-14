# Multi-level skill tree — 2026-10-14

## Entire-library coverage

All **15,860 existing skills** are now organized for browsing through:

```text
12 categories
└── 65 subjects
    └── 724 topics
        └── 1,629 context / workflow groups
            └── 15,860 skill links
```

Every current skill appears exactly once across the terminal topic-page lists. There are no omitted categories or selected-only subsets. Each terminal list contains at most **40 skills**.

There are **803 navigation pages**: the root index and library overview, 12 category pages, 65 subject pages, and 724 topic pages. The largest generated navigation page is the 129,304-byte root index, rather than a single multi-megabyte list.

## Example

```text
Software & Development
└── Implementation & Code Architecture
    └── Python services
        ├── API evolution
        │   ├── Build configuration runbook
        │   ├── Design blueprint
        │   └── … remaining workflows
        ├── Asynchronous work
        ├── Database changes
        └── … remaining contexts
```

Open [the full tree](../INDEX.md), expand a category and a subject, then open a topic. Topic pages include context/workflow sub-branches, direct skill links, shortened summaries, and breadcrumbs back through the tree.

## Navigation, not another package migration

This update adds browsing depth without moving or rewriting any skill package. Physical package storage remains:

```text
skills/<category>/<subject>/<skill-name>/SKILL.md
```

Generated topic indexes are separate Markdown documents under:

```text
skills/<category>/<subject>/_topics/<topic-key>.md
```

These indexes are not installable skills. All current skill names and Git blob hashes were compared with `HEAD` by stable skill name, including packages moved in the earlier category migration: **all 15,860 matched**. No external skills were imported during this update.

## Grouping rules

- Current files on disk define the inventory and category/subject placement.
- Known authoring seeds supply subject and context labels where available. Only labels are read from the historical seed CSV; historical paths and counts do not define the current inventory.
- Older matrix workflows are grouped by the stable name before a recognized workflow suffix.
- Remaining standalone skills use shared name prefixes or an explicitly labeled Named workflows list. This is a browsing rule, not a claim of semantic reclassification.
- Long terminal lists are split into numbered groups. Topic filenames include a short stable digest to avoid normalization collisions and overlong paths.

## Maintenance and validation

```bash
python scripts/sync_catalog.py --check
python scripts/sync_catalog.py --write
python scripts/validate_skills.py --json
python -m unittest discover -s tests -v
```

The synchronizer regenerates all navigation levels and removes only obsolete topic files carrying its generator marker. It preserves unmarked user-authored documents and refuses to overwrite one at a generated topic path.

Validation checks exact skill coverage, duplicate/stale links, topic-page existence, local section anchors, orphaned indexes, and reachability from `INDEX.md`. Regression tests also cover deterministic grouping, bounded lists, metadata errors, safe pruning, and user-authored file collisions.

The README count updater was narrowed to explicit total-count locations so it does not accidentally replace unrelated limits such as “40 skills per list.”

## Final local checks

- Full test suite: **67 tests passed**.
- Skill and navigation validation: **15,860 skills scanned, zero issues**.
- Generated metadata: no drift.
- Skill-name and Git-blob comparison against `HEAD`: all 15,860 match.
- `git diff --check`: passed.

The configured remote CI matrix was not executed during this local update.
