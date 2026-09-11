# Coursework v2

XeLaTeX classes and notation for course notes, assignments, exams, worksheets,
and compact problem handouts. Version 2 is a breaking API change. The four
migrated courses use this API; recovery branches preserve their v1 sources.

Requires **TeX Live 2026**, including the June 2026 LaTeX kernel, and XeLaTeX.
Font selection is centralized in `coursefonts.sty`. Both classes use Pagella
prose; homework uses Pagella mathematics and notes use Euler mathematics.
These are the adopted defaults, so course preambles need no font options.
An explicit `font-profile=pagella` or `font-profile=euler` class option changes
the mathematics only. See [the adoption record](docs/ADOPTION.md) and
[the original font comparison](docs/FONT-REVIEW.md).

## Package responsibilities

| Module | Owns |
| --- | --- |
| `coursepsets.cls` | Assignment page layout, headings, footers and typography |
| `coursenotes.cls` | classicthesis notes layout, chapter contents and typography |
| `coursecommon.sty` | Metadata, output settings, title/heading commands |
| `courseassignments.sty` | Declarations, selection, numbering, fragment rendering |
| `courseenvironments.sty` | Theorems, formulas, math tables and subparts |
| `coursemath.sty` | Mathematical notation and the bold-symbol backend |
| `coursephys.sty` | Physics notation, constants, units and script-r assets |
| `coursefonts.sty` | Pagella prose and the class-specific Unicode math font |

Both classes load math and document environments. Load physics explicitly.
The math and physics packages also work with `article`; they do not select
fonts, configure a page layout, or overwrite standard text accents.

## Course identity

```latex
% course.tex: shared preamble for homework and notes
\usepackage{coursephys}
\courseworksetup{
  author={Your Name},
  course-code={PHYS 331},
  course-title={Electricity \& Magnetism},
  term={Fall 2026},
  textbook={Introduction to Electrodynamics},
  textbook-author={David J. Griffiths}
}
```

Read individual values with `\courseworkvalue{author}` (and the other keys).
Values may contain LaTeX. Repeated setup calls replace earlier values.

```latex
\documentclass[mode=worked,problem-breaks=page,final]{coursepsets}
\input{course}
\begin{document}
\listoftodos\clearpage
\pagenumbering{arabic}
\makecourseworktitle[title={Homework}]
\tableofcontents\newpage
\makeassignmentheading[title={Homework}]
\subfile{homework/01-pset}
\end{document}
```

Title generation, assignment headings, contents, todos and page numbering are
separate operations. A title/heading `date` defaults to the configured term.
Ordinary `\title`, `\author`, `\date`, and `\maketitle` remain usable for notes.

## Declare once, render consistently

```latex
% homework/01-pset.tex; compile from the course repository root
\documentclass[homework.tex]{subfiles}
\begin{document}
\ifSubfilesClassLoaded{%
  \makecourseworktitle[title={Problem Set 1}]
  \tableofcontents\newpage
  \makeassignmentheading[title={Problem Set 1}]
}{}
\assignment[id=pset01,number=1,directory=homework/01-pset]{Vector Analysis}
\declareproblem[title={Griffiths 1.7}]{01}
\declareproblem[title={Griffiths 1.11 a,b,c}]{02}
\printassignment
\end{document}
```

Each problem has a required `problemNN.tex` and, in worked mode, a required
`solutionNN.tex`. Optional `guideNN.tex` and `discussionNN.tex` are included
when present. Fragments contain content only; their parent supplies headings.
An empty solution file denotes an unsolved problem. Physics graphics stay in
the course tree, with paths relative to its root.

`\printassignment[problems={02,01}]` selects and orders declarations. Selected
problems are numbered from 1 in that order in every section. IDs never depend
on printed numbers. Canonical labels are `prob:<assignment-id>:<problem-id>`;
`\cref{prob:pset01:02}` refers to the selected problem's displayed number.
Each assignment may render once in a document. Duplicate assignment IDs,
duplicate problem declarations, unknown selections, duplicate selected IDs,
and missing required files are errors. IDs accept letters, digits, hyphens,
and underscores. Assignment numbers are positive integers, defaulting to the
next assignment; `id` and `directory` are required. The optional
`problems-title` key defaults to `Problem Set`.

Equations, figures and tables use `assignment.problem.item` numbers. Their
counters continue for the same problem across its guide, statement, solution
and discussion. PDF destinations use stable assignment/problem identity.
Explicit source labels remain ordinary LaTeX labels and must be unique across
the combined document. Problem headings do not borrow a section counter.

## Output profiles

| Mode | Solution/discussion files | Problems |
| --- | --- | --- |
| `worked` (default) | Read and shown | `problem-breaks=flow` by default; `page` is available |
| `worksheet` | Never read | Start on separate pages |
| `compact` | Never read | Flow without forced breaks |

Guides remain available. Empty guide/discussion sections are omitted.
Page breaks belong to problem boundaries, independent of solutions. Long
problems may span pages; the next problem starts on a fresh page in page mode.

Course Makefiles apply build overrides after source defaults:

```sh
latexmk -usepretex='\AtBeginDocument{\courseworksetup{mode=compact}}' homework.tex
```

Class-only mode options are consumed before packages process global options;
they must not leak into siunitx's unrelated `mode` setting. `final` continues
to hide todos. Other base-class options are forwarded to article/report.

## Environments and notation

```latex
\begin{example}[A title]\label{ex:demo}
The first word is always content; no label argument is required.
\end{example}
\begin{formula}[Reference equation]\label{formula:demo}
  \integral{x^2}{x}{0}{1} = \evalat{x^3/3}{0}{1}
\end{formula}
\begin{mathtable}[caption={Values},label={tab:values},placement=H]{cc}
  x & x^2 \\ \bottomrule
\end{mathtable}
```

The theorem family shares a section-reset counter. Definitions, examples and
remarks each have their own section-reset counters; summaries reset by
subsection. `proof`, `note`, `caveat`, `warning`, `question`, and `speculation`
are also available. Formula references return their sequential formula number,
independently of the optional displayed tag. No forced line break follows a
formula.

Math-table options are local to each table. A label requires a caption.
The array receives a top rule; the author supplies row endings and any bottom
rule. Standalone defaults are `[ht!]` and a `-1em` lead-in; notes select `[H]`
and `-2ex`. `\courseenvironmentsetup{table-placement=...,table-top-skip=...}`
changes those defaults explicitly.

Use `\paren`, `\bracket`, `\abs`, and `\norm` unstarred for fixed delimiters,
starred for automatic sizing, or with an optional explicit size such as
`\bracket[\Big]{x}`. Statistical helpers retain automatically sized notation.
Use `\deriv[2]{f}{x}`, `\pderiv{F}{T}`, `\uprightvect{v}`, `\unitvect{r}`,
and `\mathbold{\alpha}`. `\grad` and `\laplacian` are operators. Physics
constants separate symbols (`\kB`, `\NA`) from rounded quantities
(`\constantvalue{boltzmann}`, `\constantvalue{avogadro}`).

The complete migration map is in [docs/MIGRATION.md](docs/MIGRATION.md).
[tests/notation.tex](tests/notation.tex) is a runnable notation specimen.

## Development and installation

Do not run `install.sh` from a review worktree. Use scoped `TEXINPUTS`:

```sh
TEXINPUTS="$(pwd)/tex/latex/coursework//:" latexmk -xelatex document.tex
python3 -m unittest discover -s tests -v
python3 tests/run_api.py
make -C ../coursework-testing candidate
```

The regression driver builds every combined/individual document, compact
handout and worksheet. It records revisions, source hashes, resolved package
paths, recorder inputs, tool versions, warnings, PDFs, text and page renders.
`make compare` remains strict against the original baseline. Intentional
changes are reviewed before saving an explicitly named immutable checkpoint.

All assets are resolved by kpathsea. The adopted class and course checkouts
use the existing installation path; recovery branches and frozen checkpoints
preserve the earlier versions. See `docs/ADOPTION.md` for the activation record.
