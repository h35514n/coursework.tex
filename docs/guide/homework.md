---
layout: default
title: Homework recipes
nav_order: 3
---

# Declare once, choose the output

`coursepsets` loads the assignment renderer, shared metadata, mathematics, environments, and fonts. Add physics explicitly when you need it.

## Share the course identity

Put this configuration in the main preamble, or in a shared `course.tex` file loaded by homework and notes:

{% include snippets/metadata.md %}

The six metadata fields accept LaTeX. Repeated setup calls replace only the values supplied.

## Assemble front matter explicitly

{% include snippets/title.md %}

Title generation, contents, page numbering, todos, and assignment headings are separate operations. For visible todos, omit `final`; use `\listoftodos` and `\clearpage` where desired. The `final` class option suppresses todos in homework.

## Declare and render an assignment

{% include snippets/assignment.md %}

The example selects problem `02` first, so its displayed reference is **1.1**; problem `01` becomes **1.2**. The IDs and reference labels retain their identities even when selection order changes.

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

Each selected problem requires a `problem<ID>.tex` file. Worked mode also requires a `solution<ID>.tex` file, which may be empty for an unsolved problem. Guides and discussions are optional. Fragments contain content only: the renderer supplies their headings and the solution closing marker.

A Guide or Discussion section is created when at least one corresponding selected file exists. An existing empty file can still create a heading; omit the file when you want that role omitted. Discussions are rendered only in worked mode.

{% include snippets/assignment-notes.md %}

## Choose a mode

| Class option | Result | Problem boundaries |
| --- | --- | --- |
| `mode=worked` | Guides, statements, solutions, and discussions | Flow by default; `problem-breaks=page` is available |
| `mode=worksheet` | Guides and statements; solution/discussion files are never read | Separate pages |
| `mode=compact` | Guides and statements; solution/discussion files are never read | Flow |

Compare [worked]({{ '/examples/homework-worked/' | relative_url }}), [worksheet]({{ '/examples/homework-worksheet/' | relative_url }}), and [compact]({{ '/examples/homework-compact/' | relative_url }}) outputs of the same project.

## Control the three kinds of breaks

| Setting | Default | Controls |
| --- | --- | --- |
| `problem-breaks=page\|flow` | `flow` | Problem boundaries in worked mode; worksheet and compact choose their own behavior |
| `assignment-breaks=page\|flow` | `flow` | Before subsequent assignments |
| `section-breaks=page\|flow` | `page` | Between Guide, Problem Set, and Discussion |

The first assignment and first role do not introduce automatic leading breaks. Long problems can span multiple pages. Explicit breaks inside content or front matter remain in force.

For a fully flowing worked document, override source defaults at begin-document time:

```sh
latexmk -xelatex -jobname=homework-flow \
  -usepretex='\AtBeginDocument{\courseworksetup{mode=worked,problem-breaks=flow,assignment-breaks=flow,section-breaks=flow}}' \
  main.tex
```

The course Makefiles provide `make homework-flow` for this combination, but that target belongs to the course repositories rather than the class package.

## Compile a subfile on its own

```latex
\documentclass[main.tex]{subfiles}
\begin{document}
\ifSubfilesClassLoaded{\makeassignmentheading[title={Selected problems}]}{}
\input{assignment.tex}
\end{document}
```

From the project root: `latexmk -xelatex standalone.tex`. See the [compiled standalone assignment]({{ '/examples/homework-subfile/' | relative_url }}). The parent can use `\subfile{standalone}` to include it; avoid including the same assignment a second time.

## References that survive reordering

Use `\cref{prob:motion:01}` for a problem and ordinary `\label` / `\eqref` for equations. Equation, figure, and table numbers are `assignment.problem.item`; each problem's object counters continue across its guide, statement, solution, and discussion. Explicit labels must remain unique across the combined document.

Read more in the [assignment reference]({{ '/reference/assignments/' | relative_url }}), [subfiles documentation](https://ctan.org/pkg/subfiles), and [cleveref documentation](https://ctan.org/pkg/cleveref).
