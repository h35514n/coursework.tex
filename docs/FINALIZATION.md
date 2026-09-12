> Workspace status: the former testbed and migration worktrees are no longer
> present. Paths and testbed results below are historical. Consult the
> [cleanup record](WORKSPACE-CLEANUP.md) for current commands and evidence.

# Coursework v2.0.0 finalization

The later [notes styling restoration](NOTES-FONT-RESTORATION.md) supersedes
the Euler notes choice recorded here; this report retains its historical results.

This records the signed v2.0.0 release. Homework mathematics was subsequently
restored to its original Pazo/Palatino appearance; see
[HOMEWORK-FONT-RESTORATION.md](HOMEWORK-FONT-RESTORATION.md). The release tags,
checkpoints, and validation manifests below remain unchanged historical evidence.

Coursework v2 is adopted on the original class and four course `master` branches.
The local testbed now uses `main`. Pagella prose, Pagella homework mathematics,
and Euler notes mathematics are the selected defaults. The installed symlink
still points to the original `coursework.tex/tex/latex/coursework` checkout.

## Release and validation

The class release marker is **`v2.0.0`**. Each migrated course and the local testbed
use **`coursework-v2-adopted`**. Signed release markers identify the final commits;
class and course masters and recovery refs are published to their existing remotes.
The testbed and bulky regression evidence remain local.

| Repository | Release | Tested source revision | PDFs | Final pages |
| --- | --- | --- | ---: | ---: |
| coursework.tex | [v2.0.0](https://github.com/h35514n/coursework.tex/tree/v2.0.0) | `9fae5de` | — | — |
| coursework-testing | coursework-v2-adopted (local) | `5bc6111` | 46 | 499 |
| PHYS 331 | [coursework-v2-adopted](https://github.com/h35514n/phys331-electricity-and-magnetism/tree/coursework-v2-adopted) | `0945a20` | 35 | 427 |
| PHYS 433 | [coursework-v2-adopted](https://github.com/h35514n/phys433-quantum-physics/tree/coursework-v2-adopted) | `1234d13` | 34 | 333 |
| PHYS 440 | [coursework-v2-adopted](https://github.com/h35514n/phys440-wave-optics/tree/coursework-v2-adopted) | `0f6ac88` | 34 | 208 |
| PHYS 491 | [coursework-v2-adopted](https://github.com/h35514n/phys491-capstone/tree/coursework-v2-adopted) | `246e9a0` | 21 | 178 |

All **170 PDFs / 1,645 pages**, **29 behavioral TeX cases**, **eight migration
tests**, and **nine regression-harness tests** pass. All **58 notes outputs**
match the font-adoption checkpoint in extracted text, page counts, and page
pixels. No new warnings, missing glyphs, duplicate PDF destinations, or duplicate
active labels were found. Eight additional installed-path homework/notes builds
pass after worktree removal, with recorder-verified modules and selected fonts.

Homework differences from `v2-pagella-euler` are the corrected role-heading gaps,
resulting pagination/contents/footer shifts, and explicit large integrals in
PHYS 331 problem 2.12 and its testbed copy. The standard integral's differential
moves outside its fraction with unchanged meaning. The source audit found no
other changed TeX fragments. A supplementary character-inventory check found
no unexplained glyph differences after excluding page-footer text, pagination
numerals, whitespace, and line-wrap hyphens; the stored strict comparisons are
unmodified. Representative rendered headings and integrals were inspected;
Guide, Problem Set, and Discussion have 17.2-point heading gaps in assignment 1.

`v2-final` checkpoints freeze the tested classes and fixtures in all five
repositories, and strict comparisons against them pass. The final class tag
also includes this release documentation; its class assets match the tested
revision exactly. [final-validation.json](final-validation.json) pins source
revisions, class hashes, checkpoints, and checks.

## Permanent workflow and preserved evidence

The class repository owns the single regression driver. Course and testbed
`make candidate` commands default to the sibling `coursework.tex` checkout;
change `candidate_repository` in `regression.json` to test another checkout.
`COURSEWORK_TOOLS` overrides the scripts directory. `make check-api` remains
available in the testbed. Installation verifies all eight modules and both
source glyph PDFs.

Each retained repository contains its original `baseline/` and reviewed
`checkpoints/`. Their manifests remain byte-for-byte intact; frozen classes
resolve relative to their bundle, so old absolute provenance paths do not
prevent integrity checks after relocation. `make compare` remains strict
against v1; use `make compare REFERENCE=v2-final` for the release checkpoint.

Historical builds, migration reports, text/render differences, font inventories,
and final checks are preserved under ignored `migration-evidence/` directories.
They survive `make distclean`. [evidence-index.json](evidence-index.json) lists
relocated paths and hashes, including mappings for absolute paths recorded in
historical manifests. The font comparison PDF remains tracked under `output/pdf/`.
Publication verification is saved locally under
`migration-evidence/publication/verification.json`.

The six temporary class/font/course worktrees and seven redundant development
branches are removed. All their commits are reachable from retained masters;
recovery refs remain. No source graphics or original course directories were
removed. The testbed remains a permanent local Git repository.

## Recovery and follow-up

Every published repository retains `archive/coursework-v1` at its original
revision. The class repository also retains `archive/coursework-v2-api` for the
API before font adoption. The testbed retains `archive/original-fixtures`.

For source recovery, use detached worktrees at matching class and course recovery
refs. V1 classes and V1 course sources must be used together. For a reproducible
historical build on the recorded toolchain, use each frozen baseline's bundled
classes and compatibility-adjusted fixtures with process-scoped `TEXINPUTS`.
Neither method requires resetting a working master or changing the installation.

[KNOWN-ISSUES.md](KNOWN-ISSUES.md) records the remaining equation/paragraph
layout warnings, standalone cross-chapter references, and package/bookmark
notices. These are separate follow-up work; no further API or font decisions
are pending. Older mechanics and thermal repositories remain outside this migration.
