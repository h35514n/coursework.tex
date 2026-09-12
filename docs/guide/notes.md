---
layout: default
title: Notes recipes
nav_order: 4
---

# Reading notes with room to grow

`coursenotes` builds on `report` and classicthesis. It loads shared metadata, mathematics, environments, and fonts. It uses Pagella prose and Pagella Math, with separate AMS Euler display numerals for chapters.

## Set up the main document

```latex
\documentclass{coursenotes}
\usepackage{coursephys}
\courseworksetup{author={Alex Student},course-code={PHYS 101},
  course-title={Motion and Energy},term={Fall 2026}}
\begin{document}
\makecourseworktitle[title={Reading notes}]
\setcounter{tocdepth}{0}
\tableofcontents
\setcounter{tocdepth}{1}
\subfile{chapters/energy}
\end{document}
```

Ordinary `\title`, `\author`, `\date`, and `\maketitle` also work. The example keeps the main contents at chapter depth, then enables section entries for local contents.

## Write a chapter

{% include snippets/chapter.md %}

Place this body in a subfile wrapped with `\documentclass[main.tex]{subfiles}`, `\begin{document}`, and `\end{document}`. The main file includes it through `\subfile{chapters/energy}`. Compile it independently from the project root:

```sh
latexmk -xelatex chapters/energy.tex
```

Compare the [combined notes]({{ '/examples/notes/' | relative_url }}) and [standalone chapter]({{ '/examples/notes-subfile/' | relative_url }}). Run through `latexmk` so both global and local contents settle.

## Choose the right environment

The theorem family shares a counter. Definitions, examples, and remarks have separate counters; all reset by section. Summaries reset by subsection. Unnumbered observations include `note`, `caveat`, `warning`, `question`, and `speculation`.

A `formula` has a sequential reference number independent of its displayed tag. Its body is already mathematics. A `mathtable` contains a math array and defaults to placement `H` in notes. See the [complete environment reference]({{ '/reference/environments/' | relative_url }}).

## Keep physics optional

For math-only notes, omit `\usepackage{coursephys}`. Add it for vectors, gradient and Laplacian operators, physical constants, script-r notation, and `siunitx` commands such as `\qty` and `\unit`.

Dependencies used by these recipes: [classicthesis](https://ctan.org/pkg/classicthesis), [etoc](https://ctan.org/pkg/etoc), [subfiles](https://ctan.org/pkg/subfiles), and [cleveref](https://ctan.org/pkg/cleveref).
