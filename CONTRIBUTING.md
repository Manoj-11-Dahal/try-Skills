# Maintaining the skill library

## Requirements

Use **Python 3.10 or newer**. The maintenance tools and tests use only the Python standard library; there is no package installation or dependency upgrade step. CI checks Python 3.10 and 3.14. GitHub Actions are pinned to commit hashes and Dependabot checks them weekly.

## Add or update a skill

1. Choose an approved category and subject branch from [`skills/README.md`](skills/README.md).
2. Create `skills/<category>/<subcategory>/<unique-kebab-case-name>/SKILL.md`, or edit the existing package in place. Keep names globally unique.
3. Start the file with exactly these frontmatter keys, in order:

   ```yaml
   ---
   name: unique-kebab-case-name
   description: "Use when ..."
   ---
   ```

   The actual description must contain at least 40 content units (English-like words count as one; CJK characters as three) and at most 1,024 characters. Use a single-line JSON-compatible double-quoted string. Include the use condition in the description and a `## When to Use` section in the body.
4. Include exactly one level-one title, at least three distinct headings, and a bounded workflow with explicit inputs, outputs, verification, limits, and approval/stop conditions. Keep the file between 400 and 60,000 bytes. Code-fence examples do not count as headings.
5. Check relative links against the package location. Record sources and licensing limitations honestly; a reference is not proof of current upstream compatibility.
6. Refresh metadata and run every check below. Review the diff before submitting changes.

## Maintenance commands

Run from the repository root:

```bash
# Read-only drift check (also the default when no flags are given)
python scripts/sync_catalog.py --check

# Reconcile catalog links, current counts, category guide, README and SVG banner
python scripts/sync_catalog.py --write

# Validate every package, taxonomy placement, unique names and index coverage
python scripts/validate_skills.py

# Optional machine-readable output; failures still return exit status 1
python scripts/validate_skills.py --json

# Full repository and regression test suite
python -m unittest discover -s tests -v

git diff --check
```

`sync_catalog.py` uses the **current skill files** as the source of truth. It regenerates the root tree, all category and branch pages, and current counts. Every skill is listed once on a topic page, alphabetically within a context/workflow group, with a shortened frontmatter summary. Terminal lists contain at most 40 skills. Topics add navigation depth without moving package directories. Full instructions remain in `SKILL.md`. Do not manually edit generated navigation pages; change the skill frontmatter or taxonomy source instead. Review removals carefully: an accidentally deleted package should be restored, not hidden by a metadata refresh. The tool refuses an empty library or invalid/duplicate inventory metadata. It never changes skill bodies, reclassifies/moves packages, or fetches external content.

Historical reports and assignment CSVs under `references/` describe past snapshots and are deliberately not rewritten. They may mention totals or paths no longer present. [`INDEX.md`](INDEX.md) and [`skills/README.md`](skills/README.md) describe the current checkout.

## Multi-level topic navigation

The navigation hierarchy is **category → subject → topic → context/workflow group → skill**. Package storage stays at `skills/<category>/<subject>/<skill-name>/SKILL.md`.

Topic pages live under `skills/<category>/<subject>/_topics/*.md` and are generated indexes, not installable skills. The topic assignment rules are in [`scripts/topic_tree.py`](scripts/topic_tree.py):

1. Reuse subject/context labels from `references/internet-topic-seeds-2026-09-30.csv` when a current skill's base name matches a recorded seed. Historical paths and totals from that file are never used as current inventory.
2. Group older matrix workflows by the name preceding a recognized workflow suffix.
3. Group remaining standalone skills by shared name prefixes, with a clearly labeled **Named workflows** list where there is no shared family. This is browsing assistance, not semantic reclassification.
4. Split long terminal lists into groups of at most 40 skills. Keys include a short digest to avoid punctuation-normalization collisions and excessive filename lengths.

`sync_catalog.py --check` detects drift and obsolete generated topic pages. `--write` refreshes pages and prunes only obsolete topic files carrying the generator marker. Unmarked documents are never pruned; a generated-path collision with a user-authored file is an error. Root/category/subject pages are canonical generated outputs. When changing a topic hint, regenerate navigation and review the affected links.

Validation checks exact skill coverage, topic pages, local anchors, orphaned pages, and reachability from `INDEX.md`. See the [multi-level tree report](references/multi-level-tree-2026-10-14.md).

## Category tree and migrations

The current package layout has **12 categories and 65 subject branches**, with deeper navigation-only topic/context branches. The three dedicated categories are Cybersecurity & Privacy, Healthcare & Medicine, and Music & Audio. Cloud & Infrastructure and Science & Research have narrower scopes and renamed folder paths.

- [`scripts/skill_tree.py`](scripts/skill_tree.py): current category labels, scope descriptions, and explicit old-to-new branch mappings.
- [`scripts/skill_taxonomy.py`](scripts/skill_taxonomy.py): branch labels and topic-to-branch helpers.
- [`scripts/tree_navigation.py`](scripts/tree_navigation.py): generated tree, category pages, and complete branch lists.

The migration moves entire existing branches, not individual skills based on guessed keywords. Existing names are stable; only affected folder paths change. Current local links are checked automatically. Historical reports/CSVs remain historical and are not redirects.

```bash
# Safe to rerun on the current tree: reports no moves
python scripts/migrate_category_tree.py

# Only when intentionally migrating an old layout, after reviewing the plan
python scripts/migrate_category_tree.py --apply
```

The migration checks collisions before writing, refuses unreviewed resource-file moves, rebases local links when needed, and rolls back package moves and metadata if applying fails. It writes an old/new path and SHA-256 receipt and refuses to overwrite an existing receipt. See [the redesign report](references/category-tree-redesign-2026-10-14.md).

When adding a new category/branch, update the taxonomy, create packages, and regenerate navigation. When retiring a whole branch, also remove its obsolete generated `README.md` after reviewing the move. The root index is now navigation, **not a flat table of all skill descriptions**.

## Versioned releases

The root [`VERSION`](VERSION) file is the source of truth for the version being prepared. The current preparation is **v1.0.0**, the first versioned release; it is **not yet published**. See [`CHANGELOG.md`](CHANGELOG.md) and the [release checklist](releases/v1.0.0.md).

- Use a major version for incompatible package-path, catalog-format, or tooling-interface changes after v1.0.0.
- Use a minor version for backward-compatible additions, and a patch version for backward-compatible corrections.
- Update `VERSION`, the changelog, version-specific notes under `releases/`, and the README status together.
- Keep upcoming entries marked **Unreleased** until publication. Record the actual publication date rather than treating a preparation date as a release date.
- Run the complete validation and test suite against the intended release commit. Push and review the existing branch before creating a GitHub tag/release that references it.
- Never point a release at an older commit to work around a failed push. Resolve permission blockers first; do not advertise a release URL or installable tag that does not exist.

## Legacy generators and migrations

The dated batch builders and reformat/reorganization scripts are historical authoring tools, **not an update-all command**. Some write files, assume the old nine-category tree, or expect a flat `INDEX.md` table. They must be adapted before use with the current tree; do not run them directly as maintenance commands. Inspect them and use their read-only/preflight modes where available before applying a migration. Do not mass-regenerate the library merely to update counts. Run the current validation and synchronization commands after an intentional migration.

## Review expectations

- Explain the task, expected artifact, and evidence supporting any substantive skill update.
- Keep untrusted input separate from instructions and retain authorization boundaries.
- Do not claim upstream versions or links were verified unless you actually checked them.
- Keep generated caches and environments out of Git.
- All quality workflow checks should pass; external URL availability and domain-specific workflow correctness still require human review.
