---
layout: default
title: Getting started
nav_order: 2
---

# Getting started
{: #your-first-document }

Use XeLaTeX with a full, updated TeX Live 2026 installation.
The classes need the June 2026 LaTeX kernel or newer, along with fontspec, classicthesis, TikZ, and other TeX Live packages.

## Installation
{: #install-the-checkout }

```sh
git clone https://github.com/h35514n/coursework.tex.git
cd coursework.tex
./install.sh
kpsewhich coursepsets.cls
kpsewhich coursenotes.cls
```

The installer links the checkout into `TEXMFHOME`, so changes to its files take effect immediately.
It verifies that TeX can find both classes, all six packages, and both script-r glyph PDFs.
It can replace an existing symbolic link but refuses to overwrite a real directory.
Keep the checkout in a stable location after installation.

To compile against a temporary checkout or review worktree, set `TEXINPUTS` for the compile command:

```sh
TEXINPUTS="/absolute/path/to/coursework.tex/tex/latex/coursework//:" \
  latexmk -xelatex -halt-on-error main.tex
```

The trailing colon retains the normal TeX search paths, so this command works without installation.

## Example projects
{: #start-from-a-complete-example }

| Example | Contents |
| --- | --- |
| [Homework project]({{ '/examples/homework-worked/' | relative_url }}) | Metadata, front matter, an assignment declaration, and all fragment roles |
| [Reading notes project]({{ '/examples/notes/' | relative_url }}) | Chapters, local contents, examples, and formulas |
| [Ordinary article]({{ '/examples/reference-article/' | relative_url }}) | Shared notation and environments without a coursework layout |

Download and extract a source ZIP, then run `latexmk -xelatex -halt-on-error main.tex` from the extracted project directory.
For the article example, replace `main.tex` with `reference-article.tex`.
Each project includes a README with its root file and compile command.

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

Assignment directories and image paths are relative to the project root.
Compile both combined documents and standalone subfiles from that directory, as shown in the example instructions.
Use `latexmk` to run the additional passes needed for contents and references.

The classes use XeLaTeX; pdfLaTeX and LuaLaTeX can produce different layouts.
