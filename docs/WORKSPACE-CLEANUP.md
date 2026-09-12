# Workspace documentation and build cleanup

Completed locally on September 11, 2026, across `coursework.tex` and all six
course repositories. This pass changes documentation and Makefiles. Course
content, shared TeX runtime modules, fonts, graphics, archived handouts, and
recovery refs remain unchanged. The existing PHYS 331 `homework.tex` working
edit is preserved and excluded from the cleanup commits. No pushes are made.

## Current documentation and commands

Course READMEs now share setup, build, editor, v2 authoring, and regression
instructions, retaining their course-specific textbook and migration material.
They describe `homework-flow`, `open-problems` and individual opening targets,
compact output, worksheets, and the current Pazo homework/Pagella notes defaults.
Historical migration documents identify earlier fonts and checkpoints explicitly.
The class README uses an existing course for regression examples; it no longer
advertises a retained testbed. That former repository has not been recreated.

Makefiles remain self-contained. Their common rules and help are synchronized;
the mechanics media dependency and three textbook-index targets remain local
extensions. Configuration, local notation, and shared glyph dependencies now
trigger Make. Exact names take precedence over prefix matching, fixing mechanics
`notes/chapter01` when `chapter01-appendix` also exists. Ambiguous short prefixes,
including thermal `homework/01` and `open-problems/01`, still fail.

The target names, output modes, LaTeX invocations, and viewer commands are
otherwise unchanged. `make compare` remains strict against its selected
historical reference; later approved font and source changes may differ from it.

## Validation

- 476 valid aliases and 20 ambiguity rejections checked across the six Makefiles.
- Matching common rules and unchanged existing LaTeX/viewer command lines.
- Up-to-date and dependency-trigger checks for eight PDF targets per course,
  including local notation, configuration, both glyph assets, and mechanics media.
- 24 Python migration/snapshot tests and 32 existing editor-routing tests passed.
- All 24 README TeX examples compiled: combined and standalone homework/notes
  in temporary fixtures using each course README's literal snippets.
- 15 smoke PDFs, totaling 712 pages, built through the installed classes.
  Recorder paths and active labels were checked; compact/worksheet recorder
  files contain no solution or discussion inputs. No missing glyphs or duplicate
  active labels or PDF destinations were found.

| Course | Combined homework pages | Combined notes pages | Additional smoke output/pages |
| --- | ---: | ---: | --- |
| PHYS321 | 116 | 11 | problems/01-pset-problems.pdf: 4 |
| PHYS331 | 110 | 10 | homework-flow.pdf: 71 |
| PHYS432 | 123 | 45 | worksheets/01-quiz-worksheet.pdf: 10 |
| PHYS433 | 80 | 15 | — |
| PHYS440 | 49 | 17 | — |
| PHYS491 | 49 | 2 | — |

Existing layout/reference/package warnings remain in the smoke logs. PHYS 331's
enlarged-integral font-size substitutions match the previously archived warnings;
the checker initially rejected all font warnings, then verified these exact
messages against the historical evidence. No font change was made. This is a
build/tooling check, not a new full rendering checkpoint. Prior rendering and
font-validation reports retain their revision-specific results.

## Cleanup and preservation

Removed **12,453 scratch files** totaling
**794.7 MiB** from working locations. Their contents remain recoverable:
existing archived copies were reused by SHA-256, and **170.5 MiB** of
unique evidence was copied into new archives before deletion. These are logical
file sizes; filesystem compression/cloning may affect actual disk space.

Removed locations include old migration candidates and comparisons, flow/font
experiment working copies, old activation/smoke folders and logs, and obsolete
mechanics/thermal root auxiliary files. Normal course PDFs and their build files
remain. Current API/font test caches remain under the class `build/` directory.
Source graphics, original supplied PDFs, Calca files, study guides, handouts,
editor configuration, and other course material remain untouched.

Every repository has a new ignored `migration-evidence/workspace-cleanup/`
directory. Its `inventory.json` maps each removed path to a retained file and
its hash. New copies live under `retained/`; duplicate files point to an existing
baseline, checkpoint, or evidence archive. Retained paths are relative to the
parent Courses directory. To recover a working file, copy its `retained_at` path
to the original course-relative path after verifying its hash.

All **39,325 existing evidence files** still match their original hashes.
The canonical driver verified all **24 baselines/checkpoints**, including their
bundled classes, fixtures, PDF/text/render hashes. Existing manifests were not
rewritten. No temporary worktrees remained to remove; archive refs and tags
were retained.

The class archive additionally contains `validation/`: build and test logs,
compiled examples, installed module paths, before-state hashes, and the exact
maintenance drivers. `validation-sha256.json` indexes these new files.

[workspace-cleanup-index.json](workspace-cleanup-index.json) records starting
revisions, tested file hashes, archive locations and hashes, and check counts.
The signed cleanup commits provide the resulting revisions; earlier release
tags and checkpoint revisions remain unchanged.
