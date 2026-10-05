---
layout: default
title: Notes
nav_order: 4
---

# Create reading notes

`coursenotes` uses `report` and classicthesis for its layout.
It loads metadata, mathematics, environments, and fonts.
It uses Pagella prose and Pagella Math.
Chapter numerals use a separate AMS Euler display font.

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

The standard `\title`, `\author`, `\date`, and `\maketitle` commands also work.
The example limits the main contents to chapters.
It then enables section entries for local contents.

## Write a chapter

{% include snippets/chapter.md %}

Put this body in a subfile.
Add `\documentclass[main.tex]{subfiles}`, `\begin{document}`, and `\end{document}` around the body.
The main file includes the chapter with `\subfile{chapters/energy}`.
To compile the chapter separately, run this command from the project root:

```sh
latexmk -xelatex chapters/energy.tex
```

Compare the [combined notes]({{ '/examples/notes/' | relative_url }}) and [standalone chapter]({{ '/examples/notes-subfile/' | relative_url }}).
Use `latexmk` to complete the passes for main and local contents.

## Choose an environment

The theorem family shares one counter.
Definitions, examples, and remarks have separate counters.
These counters reset by section.
Summaries reset by subsection.
The `note`, `caveat`, `warning`, `question`, and `speculation` environments have no numbers.

A `formula` has a sequential reference number independent of its displayed tag.
Its body is already in math mode.
A `mathtable` contains a mathematics array.
In notes, its default placement is `H`.
See the [environment reference]({{ '/reference/environments/' | relative_url }}).

## Add physics notation

For mathematics-only notes, omit `\usepackage{coursephys}`.
For physics notation, add `\usepackage{coursephys}`.
The package supplies vectors, gradient and Laplacian operators, physical constants, and script-r notation.
It also supplies `siunitx` commands such as `\qty` and `\unit`.

These examples use [classicthesis](https://ctan.org/pkg/classicthesis), [etoc](https://ctan.org/pkg/etoc), [subfiles](https://ctan.org/pkg/subfiles), and [cleveref](https://ctan.org/pkg/cleveref).
