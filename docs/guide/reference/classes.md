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

Assignment-oriented `article` layout: defaults to 11 pt, letter paper, no paragraph indentation, and course/assignment/problem information in the footer. Mathematics defaults to Pazo / Palatino. Loads `coursecommon`, `courseassignments`, `courseenvironments`, `coursemath`, and `coursefonts`.

It also loads tools used in recipes: `subfiles`, `cleveref`, `hyperref`, `graphicx`, `todonotes`, `caption`, and `subcaption`. The `final` option hides todos. Physics remains an explicit `\usepackage{coursephys}`.

[Runnable homework]({{ '/examples/homework-worked/' | relative_url }}) · [Source](https://github.com/h35514n/coursework.tex/blob/master/tex/latex/coursework/coursepsets.cls)

## `coursenotes`

```latex
\documentclass[font-profile=pagella]{coursenotes}
```

Chapter-oriented `report` / classicthesis layout: defaults to 12 pt, letter paper, Pagella Math, mixed-case contents entries, and AMS Euler chapter numerals. Loads `coursecommon`, `courseenvironments`, `coursemath`, and `coursefonts`. It also supplies `\localtableofcontents` through `etoc`, plus `subfiles`, `cleveref`, `hyperref`, and `graphicx`.

Notes set math-table defaults to `table-placement=H,table-top-skip=-2ex`. The class does not load the assignment renderer or homework todos.

[Runnable notes]({{ '/examples/notes/' | relative_url }}) · [Source](https://github.com/h35514n/coursework.tex/blob/master/tex/latex/coursework/coursenotes.cls)

## Class options

Both classes consume the [shared configuration keys]({{ '/reference/configuration/' | relative_url }}) before forwarding other options to their base class. Output mode and break settings affect assignments; they do not turn notes into a problem-set document.

Select `font-profile=pazo|pagella|euler` **in the class options** so mathematics packages load in the correct order. Later setup calls cannot reload the font backend.

Other base-class options, such as `a4paper` or `twoside`, are forwarded to `article` or `report`. The coursework classes still own geometry and visual styling; forwarding is not a promise to replace all layout decisions.
