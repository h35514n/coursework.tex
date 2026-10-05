# Coursework v2

Coursework supplies XeLaTeX classes for homework and reading notes, with shared mathematics and document environments.
Use the [authoring guide](https://h35514n.github.io/coursework.tex/) for document instructions, command reference, and complete examples.
Use the [documentation index](docs/README.md) for migration instructions, known issues, and historical evidence.

## Installation

Use TeX Live 2026 with the June 2026 LaTeX kernel or newer.
Compile documents with XeLaTeX.

From a stable checkout, run:

```sh
git clone https://github.com/h35514n/coursework.tex.git
cd coursework.tex
./install.sh
kpsewhich coursepsets.cls
kpsewhich coursenotes.cls
```

The installer links this checkout into `TEXMFHOME`.
Changes to the checkout take effect through that link.
The installer verifies both classes, six packages, and both script-r glyph PDFs.

Download a complete project from the [example gallery](https://h35514n.github.io/coursework.tex/examples/).
Extract the source ZIP.
From the extracted project directory, run the command in its README.
Most projects use:

```sh
latexmk -xelatex -halt-on-error main.tex
```

## Packages and defaults

| Module | Purpose |
| --- | --- |
| `coursepsets.cls` | Homework layout and assignment output |
| `coursenotes.cls` | Notes layout, chapters, and contents |
| `coursecommon.sty` | Course metadata and shared configuration |
| `courseassignments.sty` | Problem declarations, fragment files, and output modes |
| `courseenvironments.sty` | Theorems, formulas, mathematics tables, and subparts |
| `coursemath.sty` | Shared mathematics notation |
| `coursephys.sty` | Optional physics notation, constants, and SI units |
| `coursefonts.sty` | Prose and mathematics fonts |

Both classes use Pagella prose.
Homework defaults to Pazo/Palatino mathematics.
Notes default to Pagella mathematics with separate AMS Euler chapter numerals.
Select other [font profiles](https://h35514n.github.io/coursework.tex/reference/fonts/) through class options.
Load `coursephys` explicitly for physics notation.

## Development checks

For a review checkout, use scoped `TEXINPUTS` instead of the installer:

```sh
TEXINPUTS="$(pwd)/tex/latex/coursework//:" latexmk -xelatex document.tex
python3 -m unittest discover -s tests -v
python3 tests/run_api.py
python3 tests/check_homework_font.py
python3 tests/check_notes_font.py
python3 scripts/build_docs.py --check
```

See [guide maintenance](docs/guide/CONTRIBUTING.md) for the full documentation build and writing policy.
See the [test instructions](tests/README.md) for behavior and font checks.

All six course repositories use this checkout for regression builds.
For example, run `make -C ../phys432-thermal-physics candidate`.
Set `candidate_repository` in the course's `regression.json` to test another checkout.
Use `COURSEWORK_TOOLS` to select another scripts directory.

`make compare` compares against the selected immutable baseline or checkpoint.
Later font and source changes can produce previously accepted differences.
Read the revision-specific reports before you classify a difference as a new regression.
Save a named checkpoint only after you review deliberate changes.

## Migration and history

- [Shared v1 migration](docs/MIGRATION.md)
- [Self-contained legacy class migration](docs/LEGACY-COURSE-MIGRATION.md)
- [Known issues](docs/KNOWN-ISSUES.md)
- [Historical records](docs/history/README.md)
- [Evidence manifests](docs/README.md#evidence-manifests)
