# coursework-texmf

Shared LaTeX document classes and macro packages for course repos. Installed
once per machine into `TEXMFHOME`; after that any document anywhere can say
`\documentclass{coursepsets}`.

## Requirements

- **TeX Live** (the full scheme is simplest). Beyond the base, the classes pull
  in `classicthesis`, `mathspec`, `diffcoeff`, `tkz-euclide`, `todonotes`,
  `subfiles`, `bigints`, `bera`, `txfonts`, `etoc`, and `hypcap`.
- **XeLaTeX** — see [Engine](#engine).
- **Fonts installed at the OS level**: TeX Gyre Pagella, TeX Gyre Pagella Math,
  DejaVu Sans Mono. `fontspec` looks fonts up by name through the system font
  list, so the copies inside the TeX Live tree are not enough; install the
  `.otf`/`.ttf` files themselves (on macOS, `~/Library/Fonts` or Font Book).

## Install

```sh
./install.sh
```

Symlinks `tex/latex/coursework` into `$TEXMFHOME/tex/latex/coursework`
(`~/Library/texmf/...` on macOS), then prints what `kpsewhich` resolves for each
file. Because it is a symlink, edits here take effect on the next build with no
reinstall, and new files added to the tree are picked up automatically. Because
`TEXMFHOME` is searched live by kpathsea, no `mktexlsr` is needed.

The clone can live anywhere; the script records whatever path it is run from.
Re-run it only if the repo moves.

## Contents

| File | Purpose |
| --- | --- |
| `coursenotes.cls` | Reading notes. `classicthesis` over `report`, per-chapter local TOCs. |
| `coursepsets.cls` | Problem sets and exams. `\heading`, `\chap`, `\sect`, `\problem`, `\solution`. |
| `coursemath.sty` | Math macros, theorem environments, `mathtable`, `formula`, `sublist`. |
| `coursephys.sty` | Vector notation, unit vectors, Griffiths' script-r, physical constants. |
| `coursework-scriptr.pdf`, `coursework-boldr.pdf` | Glyphs for `\rcurs` / `\brcurs`. |

Both classes require `coursemath` and `coursephys`, so every document gets the
same macro set.

## Engine

**XeLaTeX.** `coursepsets.cls` uses `fontspec` (`\setmainfont{TeX Gyre Pagella}`)
and `mathspec`; `coursenotes.cls` pulls in `unicode-math` by way of
`classicthesis`. Neither works under pdfLaTeX.

## Using it from a course repo

A repo keeps its course-specific values in one file and its structure in two
root documents, so the same skeleton serves every course:

```latex
% course.tex -- the only course-specific file
\newcommand{\Author}{...}
\newcommand{\CourseNumber}{PHYS~331}
\newcommand{\CourseName}{Electricity \& Magnetism}
\newcommand{\CourseTerm}{Fall 2024}
\newcommand{\CourseText}{Introduction to Electrodynamics}
\newcommand{\CourseTextAuthor}{David J. Griffiths}
```

```latex
% homework.tex
\documentclass[expand,final]{coursepsets}
\input{course}
\begin{document}
\heading[Homework]{\Author}{\CourseNumber}{\CourseName}{\CourseTerm}
\subfile{homework/01-pset}
\end{document}
```

```latex
% notes.tex
\documentclass{coursenotes}
\input{course}
\begin{document}
\title{\CourseText\\\large Reading Notes}
\author{\Author}
\date{\CourseTerm}
\maketitle
\tableofcontents
\subfile{notes/01-topic}
\end{document}
```

Individual sets and chapters are `subfiles`, so each builds on its own or as
part of the combined document. `\ifSubfilesClassLoaded` is the hook for
emitting a title block only in the standalone build.

## `coursepsets` class options

| Option | Effect |
| --- | --- |
| `final` | Hides to-dos. |
| `worksheet` | Hides solutions, one problem per page. |
| `summary` | Hides solutions without page breaks. |
| `expand` | One problem per page. |

`worksheet` is meant to be selected at build time rather than in the source, so
one set of files yields both the worked and the blank copy:

```sh
latexmk -usepretex='\PassOptionsToClass{worksheet}{coursepsets}' homework/01-pset.tex
```

## Conventions

These are what keep the tree safe to extend and old documents buildable.

- **Everything is prefixed `course`.** Once installed into `TEXMFHOME` these
  names share a namespace with all of TeX Live, so generic names like
  `notes.cls` are a collision risk.
- **Assets are referenced by bare name.** `coursephys.sty` says
  `\includegraphics{coursework-scriptr}`, and kpathsea resolves it from the
  installed tree — so documents compile from any working directory. Never
  reference a path relative to a course repo.
- **`\providecommand`, not `\newcommand`,** for anything a document might want
  to redefine locally.
- **Bold math goes through the `\course@bold` / `\course@bhat` hooks.**
  `coursepsets` is traditional NFSS plus `mathspec`, where `\bm` is correct;
  `coursenotes` is `unicode-math`, where `\bm` errors and `\symbf` is correct.
  A raw `\bm` in shared code breaks the notes build. The same applies to 8-bit
  NFSS font tricks (see the `txfonts` guard).
- **Per-class layout differences go through hooks** rather than forked
  definitions — see `\coursemathtablestart` in `coursemath.sty`, overridden by
  `coursenotes.cls`.
- **Bump the date and version** in `\ProvidesClass` / `\ProvidesPackage` when
  changing a file.

## Changing the classes

Documents from past terms are expected to keep compiling and re-rendering the
same. Prefer additive changes; when something would alter existing output, add
a class option and leave the default alone. Before committing, rebuild at least
one real course repo (`make`) rather than trusting a minimal test file — the
interactions that break here are between packages, and they only surface in a
full document.

## Adding a subject package

Follow `coursephys.sty`: name it `courseX.sty`, `\RequirePackage{coursemath}`
for the shared base, and guard anything that depends on the math engine. Load
it from a document's preamble with `\usepackage{coursechem}`; only add it to
the `\RequirePackage` list at the foot of both classes if every document should
have it. `coursephys` is on that list today only because every repo so far is
physics; it costs a non-physics document nothing but a few unused macros.
