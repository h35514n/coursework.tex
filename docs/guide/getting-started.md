---
layout: default
title: Getting started
nav_order: 2
---

# Your first document

Use XeLaTeX and a full, updated TeX Live 2026 installation. The classes use fontspec, classicthesis, TikZ, and other TeX Live packages; an older system TeX installation may be missing the required LaTeX kernel.

## Install the checkout

```sh
git clone https://github.com/h35514n/coursework.tex.git
cd coursework.tex
./install.sh
kpsewhich coursepsets.cls
kpsewhich coursenotes.cls
```

The installer symlinks this checkout into `TEXMFHOME`, so changes to the checkout take effect immediately. It verifies the six packages and both script-r glyph PDFs as well as the classes. It refuses to overwrite a real directory, but may replace an existing symlink. Use a stable checkout for installation.

For a temporary checkout or review worktree, use scoped lookup instead:

```sh
TEXINPUTS="/absolute/path/to/coursework.tex/tex/latex/coursework//:" \
  latexmk -xelatex -halt-on-error main.tex
```

The trailing colon keeps the normal TeX search paths. No installation is needed for this command.

## Start from a complete example

- [Homework project]({{ '/examples/homework-worked/' | relative_url }}): metadata, front matter, a declared assignment, and all fragment roles.
- [Reading notes project]({{ '/examples/notes/' | relative_url }}): chapters, local contents, examples, and formulas.
- [Ordinary article]({{ '/examples/reference-article/' | relative_url }}): shared notation and environments without a coursework layout.

Download a source ZIP, extract it, and run `latexmk -xelatex -halt-on-error main.tex` **from the extracted project root**. For the article specimen, use `reference-article.tex` instead. The included README names the exact root file.

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

A homework document uses `coursepsets` and the [declaration workflow]({{ '/homework/' | relative_url }}). Plain text and ordinary LaTeX displays are also valid in either class.

## Keep the working directory consistent

Paths in `\assignment[directory=...]`, image paths, and example instructions are relative to the project root. Compile combined documents and standalone subfiles from that same directory. Use `latexmk` so contents and references receive the additional passes they need.

The classes target XeLaTeX. This guide does not promise identical layouts with pdfLaTeX or LuaLaTeX.
