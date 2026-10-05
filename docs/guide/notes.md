---
layout: default
title: Reading notes
nav_order: 4
---

# Reading notes
{: #create-reading-notes }

`coursenotes` uses a `report` layout with classicthesis and loads course metadata, shared mathematics notation, environments, and fonts.
The defaults are Pagella prose and Pagella Math, with a separate AMS Euler display font for chapter numerals.

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
The example limits the main contents to chapters, then enables section entries for local contents.

## Write a chapter

{% include snippets/chapter.md %}

Put this body in a subfile, with `\documentclass[main.tex]{subfiles}` in the preamble and the body between `\begin{document}` and `\end{document}`.
Include the chapter in the main file with `\subfile{chapters/energy}`.
To compile the chapter separately, run this command from the project root:

```sh
latexmk -xelatex chapters/energy.tex
```

Compare the [combined notes]({{ '/examples/notes/' | relative_url }}) and [standalone chapter]({{ '/examples/notes-subfile/' | relative_url }}).
Use `latexmk` to run the passes needed for both main and local contents.

## Choose an environment

The theorem family shares one counter, while definitions, examples, and remarks each have their own.
These counters reset by section; summaries have a separate counter that resets by subsection.
The `note`, `caveat`, `warning`, `question`, and `speculation` environments have no numbers.

A `formula` has a sequential reference number independent of its displayed tag, and its body is already in math mode.
A `mathtable` contains a mathematics array and defaults to placement `H` in notes.
See the [environment reference]({{ '/reference/environments/' | relative_url }}).

## Add physics notation

Add `\usepackage{coursephys}` for vectors, gradient and Laplacian operators, physical constants, and script-r notation.
It also provides `siunitx` commands such as `\qty` and `\unit`.
You can omit it for mathematics-only notes.

These examples use [classicthesis](https://ctan.org/pkg/classicthesis), [etoc](https://ctan.org/pkg/etoc), [subfiles](https://ctan.org/pkg/subfiles), and [cleveref](https://ctan.org/pkg/cleveref).
