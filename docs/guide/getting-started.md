---
layout: default
title: Getting started
nav_order: 2
---

# Your first document

Use XeLaTeX and a full TeX Live 2026 installation with current updates.
The classes require fontspec, classicthesis, TikZ, and other TeX Live packages.
An older installation can lack the required LaTeX kernel.

## Install the checkout

```sh
git clone https://github.com/h35514n/coursework.tex.git
cd coursework.tex
./install.sh
kpsewhich coursepsets.cls
kpsewhich coursenotes.cls
```

The installer links this checkout into `TEXMFHOME`.
Changes to the checkout take effect through the link.
It verifies both classes, six packages, and both script-r glyph PDFs.
It refuses to overwrite a real directory.
It can replace an existing symbolic link.
Use a stable checkout for installation.

For a temporary checkout or review worktree, use scoped lookup:

```sh
TEXINPUTS="/absolute/path/to/coursework.tex/tex/latex/coursework//:" \
  latexmk -xelatex -halt-on-error main.tex
```

The trailing colon retains the normal TeX search paths.
This command does not require installation.

## Start from a complete example

| Example | Contents |
| --- | --- |
| [Homework project]({{ '/examples/homework-worked/' | relative_url }}) | Metadata, front matter, an assignment declaration, and all fragment roles |
| [Reading notes project]({{ '/examples/notes/' | relative_url }}) | Chapters, local contents, examples, and formulas |
| [Ordinary article]({{ '/examples/reference-article/' | relative_url }}) | Shared notation and environments without a coursework layout |

Download a source ZIP.
Extract the ZIP.
From the extracted project directory, run `latexmk -xelatex -halt-on-error main.tex`.
For the article example, replace `main.tex` with `reference-article.tex`.
The included README identifies the root file.

## A minimal notes document

```latex
\documentclass{coursenotes}
\usepackage{coursephys}
\begin{document}
\chapter{Motion}
\section{Velocity}
\begin{definition}[Velocity]
  The velocity is $v=\deriv{x}{t}$.
\end{definition}
\end{document}
```

For homework, use `coursepsets` and the [assignment instructions]({{ '/homework/' | relative_url }}).
Both classes also accept plain text and standard LaTeX displays.

## Compile from the project root

Assignment directories, image paths, and example instructions use paths relative to the project root.
Compile combined documents and standalone subfiles from that directory.
Use `latexmk` to complete the additional passes for contents and references.

The classes use XeLaTeX.
Layouts can differ with pdfLaTeX or LuaLaTeX.
