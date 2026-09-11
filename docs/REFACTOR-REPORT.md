# Coursework v2 review report

This records the completed review milestone before adoption. For the user's
subsequent approval, selected fonts, and activation status, see [ADOPTION.md](ADOPTION.md).

The breaking API, balanced-argument source migration, four course migration worktrees, and isolated Unicode font comparison are implemented. At that historical milestone, nothing had been merged or installed.

## Review branches

- Class API: `coursework-refactor`, branch `codex/coursework-refactor`.
- Testbed: `coursework-testing`, branch `codex/coursework-migration`.
- Four sibling `<course>-migration` worktrees, each on `codex/coursework-migration`.
- Font experiments: `coursework-fonts`, branch `codex/coursework-fonts`.

All worktrees are under `/Users/jmromer/Courses`. The installed `coursework` symlink still targets the original `coursework.tex` checkout.

## Build matrix

| Repository | PDFs | v1 pages | v2 pages |
| --- | ---: | ---: | ---: |
| coursework-testing | 46 | 517 | 488 |
| phys331-electricity-and-magnetism-migration | 35 | 445 | 416 |
| phys433-quantum-physics-migration | 34 | 374 | 331 |
| phys440-wave-optics-migration | 34 | 272 | 208 |
| phys491-capstone-migration | 21 | 242 | 178 |

Total: **170 candidate PDFs**, **1621 pages**, with corresponding original-class baselines.

The mechanical environment extraction was pixel-identical across all 46 testbed PDFs and 517 pages. Later changes intentionally fix reference identity, remove empty sections, move pagination to problem boundaries, make document labels visible in titles, remove formula trailing line breaks, and consolidate notation spacing. The reduced page counts do not indicate omitted problem content.

## Acceptance evidence

- 22 behavioral TeX cases cover ordered/subset selections, semantic assignment/problem labels, named references, object counters across sections, missing files, hidden invalid inputs, empty solutions, long problems, theorem/table/formula behavior, and every notation command.
- Seven migration tests cover balanced nested arguments, comments/verbatim, optional arguments, idempotence, tables/theorems, and ambiguity rejection.
- Eight testbed harness tests cover selected package paths, new-module fallbacks, frozen fixture/artifact integrity, warning normalization, and visual-difference detection.
- Every candidate PDF has recorder-verified class/package inputs. No migrated output has missing glyphs, duplicate destinations or duplicate active labels.
- The original testbed baseline manifest SHA-256 is `8c858e9130836771b945ca17310bf083ac163130c25ea896b5a963d9056053d5`.
- `checkpoints/environment-extraction` and `checkpoints/v2-api` preserve reviewed stages. Original comparisons and named-checkpoint comparisons retain separate report/diff directories.

## Known differences and limitations

Existing overfull/underfull boxes and references to omitted standalone chapters remain visible in warning manifests. Two compact testbed outputs now record the standard conversion of float placement `h` to `ht`; these are documented layout warnings, not missing content. The notes font stack still has inherited package/font warnings on the API branch. Font cleanup lives on the separate experimental branch.

A real-document diff review caught and fixed diffcoeff consuming a following `[expression]` as an evaluation-point argument. Wrappers now delimit their own arguments. The notes title page no longer creates a duplicate page-1 destination. PHYS 331's dropped Unicode minus is repaired in its own compatibility commit.

## Inspecting the results

Read `docs/MIGRATION.md` for the complete command map and `README.md` for authoring examples. Each course has a `MIGRATION.md` with its pinned baseline and migration milestones. Use `make candidate` for the experimental classes and `make compare` for strict v1 differences. Use `make compare REFERENCE=v2-api` after a reviewed checkpoint has been saved.

The preserved font comparison is [the specimen PDF](../output/pdf/coursework-font-comparison.pdf); its build/font inventory is summarized in [FONT-REVIEW.md](FONT-REVIEW.md). Both styles use explicit Unicode math: Pagella homework with either Euler or Pagella notes. The six-page specimen PDF and representative real documents are provided for the user's font choice.

Merging, activation, and font selection were subsequent steps and are now complete. The older local-class mechanics/thermal repositories remain outside the migration. See [FINALIZATION.md](FINALIZATION.md) for current locations and release status.
