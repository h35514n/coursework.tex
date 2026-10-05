---
layout: default
title: Document classes
parent: Reference
nav_order: 1
---

# Document classes

## `coursepsets`

```latex
\documentclass[mode=worked,problem-breaks=page,final]{coursepsets}
```

`coursepsets` uses an `article` layout for assignments, with 11 pt text, letter paper, and unindented paragraphs by default.
The footer shows course, assignment, and problem information, and mathematics defaults to Pazo / Palatino.

The class loads `coursecommon`, `courseassignments`, `courseenvironments`, `coursemath`, and `coursefonts`.
It also loads `subfiles`, `cleveref`, `hyperref`, `graphicx`, `todonotes`, `caption`, and `subcaption`.
The `final` option hides todos.
For physics notation, add `\usepackage{coursephys}`.

[Homework example]({{ '/examples/homework-worked/' | relative_url }}) · [Class source](https://github.com/h35514n/coursework.tex/blob/master/tex/latex/coursework/coursepsets.cls)

## `coursenotes`

```latex
\documentclass[font-profile=pagella]{coursenotes}
```

`coursenotes` uses a `report` layout with classicthesis, defaulting to 12 pt text, letter paper, and Pagella Math.
Contents entries retain mixed-case letters, and chapter numerals use AMS Euler.

The class loads `coursecommon`, `courseenvironments`, `coursemath`, and `coursefonts`.
It supplies `\localtableofcontents` through `etoc`.
It also loads `subfiles`, `cleveref`, `hyperref`, and `graphicx`.
Notes use `table-placement=H,table-top-skip=-2ex` as the defaults for mathematics tables.
The class does not load assignment output or homework todos.

[Notes example]({{ '/examples/notes/' | relative_url }}) · [Class source](https://github.com/h35514n/coursework.tex/blob/master/tex/latex/coursework/coursenotes.cls)

## Class options

Both classes process [shared configuration keys]({{ '/reference/configuration/' | relative_url }}) before they forward other options to the base class.
Output modes and page-break settings control assignments without adding assignment output to notes.

Select `font-profile=pazo|pagella|euler` in the class options so the mathematics packages are chosen before they load.
Later setup calls cannot reload the font backend.

The classes forward other base-class options, such as `a4paper` or `twoside`, to `article` or `report`.
The coursework classes still control geometry and visual style, so forwarded options do not replace all layout settings.
