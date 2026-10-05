---
layout: default
title: Homework
nav_order: 3
---

# Homework
{: #create-homework }

`coursepsets` provides the homework layout, assignment output, course metadata, shared mathematics notation, environments, and fonts.
Load `coursephys` explicitly if you need physics notation.

## Set course metadata

Put the configuration in the main preamble, or in a shared `course.tex` file loaded by both homework and notes.

{% include snippets/metadata.md %}

All six metadata fields accept LaTeX.
Each setup call updates the supplied values and leaves the others unchanged.

## Add front matter

{% include snippets/title.md %}

Titles, contents, page numbers, todos, and assignment headings are configured separately.
Use `\clearpage` wherever you need a page break.
To show todos, omit the `final` class option and use `\listoftodos` to print their list.
With `final`, homework todos are hidden.

## Declare and print an assignment

{% include snippets/assignment.md %}

This example selects problem `02` first, giving it the displayed reference **1.1**.
Problem `01` becomes **1.2**.
Changing the selection order changes the displayed numbers while keeping the IDs and reference labels stable.

```text
main.tex
assignment.tex
fragments/
  problem01.tex
  solution01.tex
  guide02.tex
  problem02.tex
  solution02.tex
  discussion02.tex
```

Each selected problem needs a `problem<ID>.tex` file.
Worked mode also needs `solution<ID>.tex`, which can be empty for an unsolved problem.
Guide and discussion files are optional.
Fragments contain only the content: the assignment renderer adds headings and the solution closing marker.

The renderer creates a Guide or Discussion section when at least one selected file for that role exists, even if the file is empty.
To omit an optional role, leave out its file.
Discussion sections appear only in worked mode.

{% include snippets/assignment-notes.md %}

## Choose a mode

| Class option | Result | Problem boundaries |
| --- | --- | --- |
| `mode=worked` | Guides, statements, solutions, and discussions | Continuous by default; use `problem-breaks=page` for separate pages. |
| `mode=worksheet` | Guides and statements; solution and discussion files are never read. | Separate pages |
| `mode=compact` | Guides and statements; solution and discussion files are never read. | Continuous output |

Compare the [worked]({{ '/examples/homework-worked/' | relative_url }}), [worksheet]({{ '/examples/homework-worksheet/' | relative_url }}), and [compact]({{ '/examples/homework-compact/' | relative_url }}) outputs.
All three outputs come from the same project.

## Set page breaks

| Setting | Default | Effect |
| --- | --- | --- |
| `problem-breaks=page\|flow` | `flow` | Controls problem boundaries in worked mode. Worksheet and compact modes set their own boundaries. |
| `assignment-breaks=page\|flow` | `flow` | Breaks before subsequent assignments |
| `section-breaks=page\|flow` | `page` | Breaks between Guide, Problem Set, and Discussion sections |

No automatic break is added before the first assignment or before the first role within an assignment.
Long problems can span multiple pages, and explicit breaks in content and front matter still apply.

For continuous worked output, override the source settings at the start of the document:

```sh
latexmk -xelatex -jobname=homework-flow \
  -usepretex='\AtBeginDocument{\courseworksetup{mode=worked,problem-breaks=flow,assignment-breaks=flow,section-breaks=flow}}' \
  main.tex
```

The course repositories provide `make homework-flow` for this configuration.
The target produces a separate PDF and job name while retaining guides, solutions, discussions, and explicit source breaks.

## Compile a subfile separately

```latex
\documentclass[main.tex]{subfiles}
\begin{document}
\ifSubfilesClassLoaded{\makeassignmentheading[title={Selected problems}]}{}
\input{assignment.tex}
\end{document}
```

Run `latexmk -xelatex standalone.tex` from the project root to produce the [standalone assignment]({{ '/examples/homework-subfile/' | relative_url }}).
The parent document can include the same file with `\subfile{standalone}`.
Include each assignment only once.

## Refer to problems and objects

Refer to a problem with `\cref{prob:motion:01}`, and use standard `\label` and `\eqref` commands for equations.
Equation, figure, and table numbers use the format `assignment.problem.item`.
Each problem's object counters continue across its guide, statement, solution, and discussion.
Explicit labels must be unique across the combined document.

See the [assignment reference]({{ '/reference/assignments/' | relative_url }}), [subfiles documentation](https://ctan.org/pkg/subfiles), and [cleveref documentation](https://ctan.org/pkg/cleveref).
