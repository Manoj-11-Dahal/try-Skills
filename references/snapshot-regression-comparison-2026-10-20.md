# Snapshot Regression Comparison — 2026-10-20

**Scope:** the 5,500 packages captured in both archives under `backups/`, compared
against the same packages in the current checkout. Generated output is reproducible
with `scripts/compare_snapshots.py`; no skill file was modified for this report.

## Why this exists

The 2026-09-29 reformat reports record that 5,500 files were rewritten and that all
validation passed. Passing validation means the *structure* is valid; it does not
show whether the rewrite preserved content efficiently. These snapshots make that
question answerable, so a future regeneration can be checked against a baseline.

## Baselines

| Label | Source | Date |
|---|---|---|
| A | `backups/before-template-reformat-2026-09-29.tar.gz` | 2026-09-29, before template reformat |
| B | `backups/before-creator-template-2026-09-29.tar.gz` | 2026-09-29, before creator-template reformat |
| Current | `skills/` in this checkout | 2026-10-20 |

All 5,500 packages present in A and B are still present today; **zero packages were
removed**, and packages were matched by skill name across the category migration.

## Measured result

| Metric | A | B | Current |
|---|---:|---:|---:|
| Matched packages | 5,500 | 5,500 | 5,500 |
| Body bytes | 31,789,187 | 63,103,704 | 67,258,067 |
| Duplicate characters inside a package | **0** | 5,721,285 | 7,050,513 |
| Packages containing repeats | **0** | 5,500 | 5,259 |
| Packages with placeholder sections | **0** | 5,500 | 5,500 |

Two distinct changes are visible.

**A → B (the creator-template reformat) is the regression.** For the same 5,500
packages, body size grew **+98%** while unique content did not grow: every package
gained verbatim repeats of its own sections and a set of `Not specified in source
skill` placeholders. No package lost content.

**B → Current is a partial correction.** Six template sections were dropped —
`Related Skills`, `Test Cases`, `Trigger Examples`, `Common Pitfalls`, `Maintenance`,
and `Quality Standards`. All but `Quality Standards` were placeholder-only in 5,500
of 5,500 files, so removing them was correct. `Quality Standards` was a duplicate of
`Acceptance Evidence` in 5,451 packages and re-titled in the rest.

Repetition nevertheless grew a further **+1,329,228 characters** between B and now.

## Content preservation

No substantive text was lost. Every section that disappeared from a package was
either a placeholder or its prose survives under a re-titled heading:

- A → Current: 34,662 sections re-titled or re-nested, **0** content losses.
- B → Current: 5,497 re-titled, 27,901 placeholder sections dropped, **0** content losses.

This matters for interpreting the section lists in earlier reports: headings such as
`Loop Contract`, `Tool Map`, `Focused Procedure`, and `Safety and Stop Conditions`
were not deleted, they were demoted beneath composite sections as
`### Preserved source section: …`.

## Recoverable duplication

About **7,050,513 characters (4.6% of the library)** are verbatim copies of a
paragraph that already appears in the same file. Collapsing each repeat to its first
occurrence would remove that text without removing any unique statement. It would
touch 5,259 files, so it is recorded here rather than applied silently.

## Reproduce

```bash
python scripts/compare_snapshots.py backups/before-template-reformat-2026-09-29.tar.gz
python scripts/compare_snapshots.py backups/before-creator-template-2026-09-29.tar.gz
python scripts/audit_skill_quality.py
```

`compare_snapshots.py` exits 1 under `--fail-on-regression` when a package is
removed, repetition grows, placeholders grow, substantive section text is lost, or
body size grows by more than 25% without added packages. Use it before accepting any
future corpus-wide regeneration.
