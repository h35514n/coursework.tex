---
layout: default
title: Homework
nav_order: 3
---

# Create homework

`coursepsets` loads assignment output, metadata, mathematics, environments, and fonts.
For physics notation, load `coursephys` explicitly.

## Set course metadata

Put the configuration in the main preamble.
Alternatively, put it in a shared `course.tex` file that homework and notes load.

{% include snippets/metadata.md %}

The six metadata fields accept LaTeX.
Each setup call replaces the supplied values and retains the other values.

## Add front matter

{% include snippets/title.md %}

Title generation, contents, page numbers, todos, and assignment headings are separate operations.
For visible todos, omit the `final` class option.
Use `\listoftodos` to print the list.
Use `\clearpage` where you require a page break.
The `final` option suppresses todos in homework.

## Declare and print an assignment

{% include snippets/assignment.md %}

The example selects problem `02` first.
Its displayed reference is **1.1**.
Problem `01` becomes **1.2**.
The IDs and reference labels retain their identities when the selection order changes.

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

Each selected problem requires a `problem<ID>.tex` file.
Worked mode also requires a `solution<ID>.tex` file.
For an unsolved problem, the solution file can be empty.
Guide and discussion files are optional.
Fragments contain content only.
The assignment renderer supplies headings and the solution closing marker.

The renderer creates a Guide or Discussion section if at least one selected file for that role exists.
An existing empty file can create a heading.
To omit an optional role, omit its file.
Discussion sections appear only in worked mode.

{% include snippets/assignment-notes.md %}

## Choose a mode

| Class option | Result | Problem boundaries |
| --- | --- | --- |
| `mode=worked` | Guides, statements, solutions, and discussions | Continuous output by default. `problem-breaks=page` is available. |
| `mode=worksheet` | Guides and statements. The renderer never reads solution or discussion files. | Separate pages |
| `mode=compact` | Guides and statements. The renderer never reads solution or discussion files. | Continuous output |

Compare the [worked]({{ '/examples/homework-worked/' | relative_url }}), [worksheet]({{ '/examples/homework-worksheet/' | relative_url }}), and [compact]({{ '/examples/homework-compact/' | relative_url }}) outputs.
These outputs use the same project.

## Set page breaks

| Setting | Default | Effect |
| --- | --- | --- |
| `problem-breaks=page\|flow` | `flow` | Problem boundaries in worked mode. Worksheet and compact modes have their own behavior. |
| `assignment-breaks=page\|flow` | `flow` | Breaks before subsequent assignments |
| `section-breaks=page\|flow` | `page` | Breaks between Guide, Problem Set, and Discussion sections |

The first assignment and first role do not add automatic leading breaks.
Long problems can span multiple pages.
Explicit breaks in content and front matter still apply.

For continuous worked output, override source defaults when the document starts:

```sh
latexmk -xelatex -jobname=homework-flow \
  -usepretex='\AtBeginDocument{\courseworksetup{mode=worked,problem-breaks=flow,assignment-breaks=flow,section-breaks=flow}}' \
  main.tex
```

Course Makefiles provide `make homework-flow` for this configuration.
The target uses a separate job name and PDF.
It retains guides, solutions, discussions, and explicit source breaks.
This target belongs to the course repositories.

## Compile a subfile separately

```latex
\documentclass[main.tex]{subfiles}
\begin{document}
\ifSubfilesClassLoaded{\makeassignmentheading[title={Selected problems}]}{}
\input{assignment.tex}
\end{document}
```

From the project root, run `latexmk -xelatex standalone.tex`.
See the [compiled standalone assignment]({{ '/examples/homework-subfile/' | relative_url }}).
The parent can include it with `\subfile{standalone}`.
Include each assignment only once.

## Refer to problems and objects

Use `\cref{prob:motion:01}` for a problem reference.
Use standard `\label` and `\eqref` commands for equations.
Equation, figure, and table numbers use the format `assignment.problem.item`.
Each problem's object counters continue across its guide, statement, solution, and discussion.
Explicit labels must be unique across the combined document.

See the [assignment reference]({{ '/reference/assignments/' | relative_url }}), [subfiles documentation](https://ctan.org/pkg/subfiles), and [cleveref documentation](https://ctan.org/pkg/cleveref).
