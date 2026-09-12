# Notes font and contents restoration

The shared notes default now matches the font families and contents lettering
in PHYS 432's saved `migration-evidence/supplied-pdfs/notes.pdf` from August 2024:

- Pagella prose and **TeX Gyre Pagella Math**, with conventional italic variables.
- Mixed-case Pagella entries in the main contents, with a compact number column.
- The original **AMS Euler bold chapter numerals**, at 70 pt. This is a display
  face for chapter numbers; it does not select Euler mathematics.

The saved PDF embeds Pagella Math and `EURB10`. The previously installed v2
notes instead embedded Euler Math and used Pagella chapter numerals. The legacy
class's `eulermath` option does not reliably reproduce the saved PDF on today's
TeX Live: classicthesis has changed since that PDF was made. The restoration
therefore selects the actual saved-PDF fonts explicitly, while retaining the
single mathematics backend and the v2 document API.

Homework retains its restored Pazo/Palatino mathematics. Explicit class options
`font-profile=euler` and `font-profile=pazo` remain available for notes; the
default is now `font-profile=pagella`. Chapter numerals are independent of that
math selection. No course source or installation-link change is needed.

## Validation

All **67 combined and individual notes outputs** in the six current course
repositories build successfully. Their total is 188 pages, versus 190 with
Euler mathematics. All were rebuilt and recorder-verified through the installed
classes in the original checkouts. The retained testbed was no longer present
at the start of this change.

| Combined notes | Before | Restored |
| --- | ---: | ---: |
| PHYS 321 | 11 | 11 |
| PHYS 331 | 10 | 10 |
| PHYS 432 | 46 | 45 |
| PHYS 433 | 15 | 15 |
| PHYS 440 | 17 | 17 |
| PHYS 491 | 2 | 2 |

The standalone thermal probability chapter also loses one page. The saved 2024
thermal PDF has 44 pages; current notes retain the v2 paragraph, environment,
table, and reference behavior. This restores the requested fonts and contents
styling rather than treating the old PDF as a whole-document pixel baseline.
Visual review covered contents, chapter numerals, factorial integrals, proofs,
tables, probability, and entropy/barred differentials.

All **39 behavioral TeX cases**, **24 migration/snapshot Python tests**, and the
focused notes-font check pass. The notes check verifies the saved font families,
mixed-case contents, and identical renders for default and explicit Pagella
profiles. The homework glyph specimen still matches the original Pazo API
checkpoint at **300 dpi**. The current combined thermal homework also has
unchanged extracted text and identical renders on all **123 pages**, at 100 dpi.

No missing glyphs, duplicate active labels, duplicate PDF destinations, or font
substitution warnings were introduced. Label values and course notes sources
are unchanged. Existing overflows, package notices, and standalone references
to omitted chapters remain recorded, with before/after warning differences.
The longest existing probability-list line overflows by 35.56 pt with Pagella
Math, versus 33.40 pt with Euler; it remains visible within the page margin.

## Reproduction and evidence

From the class checkout:

```sh
python3 tests/run_api.py
python3 tests/check_notes_font.py
python3 tests/check_homework_font.py
python3 -m unittest discover -s tests -v
```

From any course checkout, `make notes` rebuilds the combined document and each
chapter. Normal output is under `build/notes.pdf` and `build/notes/`. The legacy
course audit now expects Pagella notes; use `--notes-profile=euler` when auditing
a historical Euler candidate. Historical baselines and checkpoints are intact;
comparisons against them continue to expose this deliberate typography change.

[notes-font-validation.json](notes-font-validation.json) records source revisions,
tested runtime hashes, the exact saved-PDF hash, tools, and the evidence inventory.
Detailed before/after PDFs, text, renders, logs, font paths, class snapshots,
comparison results, installed-build checks, and test outputs are preserved under
the ignored `migration-evidence/notes-font-restoration/` directory. Its
`sha256.json` inventory was verified after copying. Existing user edits in other
course files were not included in these commits.
