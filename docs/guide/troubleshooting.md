---
layout: default
title: Troubleshooting
nav_order: 8
---

# Troubleshooting

## The class or a glyph cannot be found

Run `kpsewhich coursepsets.cls`.
Run `kpsewhich coursephys.sty`.
Run `kpsewhich -format='graphic/figure' coursework-scriptr.pdf`.
Both glyph PDFs must be available with the packages.
For a stable checkout, use the installer.
For a temporary checkout, set scoped `TEXINPUTS` with a trailing colon.

## The LaTeX kernel is too old

Run `xelatex --version`.
Read the `LaTeX2e <...>` line in the compile log.
The classes require the June 2026 kernel or newer.
Make sure the executable on your PATH belongs to your updated TeX Live installation.

## A vector or unit command is undefined

Physics notation requires `coursephys`.
Add `\usepackage{coursephys}`.
The package supplies vectors, gradient and Laplacian operators, constants, and `siunitx` commands.
For a Unicode article, load `coursemath` with the `unicode` option before `unicode-math`.

## A required fragment is missing

Compile from the project root.
Match the `directory` value and problem IDs exactly.
ID `01` requires `problem01.tex`.
It does not select `problem1.tex`.

Worked mode requires `solution01.tex`, even for an unsolved problem.
The solution file can be empty.
Worksheet and compact modes never read solution or discussion files.

## IDs or selections are rejected

Start each ID with a letter or digit.
Use only letters, digits, hyphens, or underscores for the remaining characters.
Assignment IDs must be unique in the document.

Declare the assignment before its problems.
Declare each problem only once.
Select known problem IDs without duplicates.
Print the assignment only once.
Assignment numbers must be positive integers.

## A reference has the wrong number

Use canonical labels such as `prob:motion:01`.
Do not build labels from the printed problem number.
The renderer numbers selected problems from 1 in their selected order.
Explicit source labels must be unique across the combined document.
Run `latexmk` to complete the reference passes.
A formula's displayed tag is independent of its reference number.

## A table label causes an error

A `mathtable` label requires a caption.
Use `caption={...},label={...}` on the same table.
Each table's options apply only to that table.
To change subsequent defaults, use `\courseenvironmentsetup`.

Table bodies are mathematics arrays.
For text, use `\text{...}` or `\tableheading`.
Supply the row endings.
Supply a bottom rule if required.

## An example's first word disappears

V2 theorem environments accept an optional title and ordinary body text.
Use `\begin{example}[Title]\label{ex:one}Text...`.
Do not supply a legacy label argument.
See the [migration map]({{ '/migration/' | relative_url }}).

## The font profile does not change

Set the profile in `\documentclass[font-profile=...]`.
Fonts load with the class.
Later setup calls cannot replace the loaded font backend.
Notes chapter numerals are independent of the mathematics profile.

## An empty file creates a role section

The renderer uses file presence to select optional sections.
To omit an optional role, remove its guide or discussion file.
Keep an empty solution file for an unsolved problem in worked mode.

## Page breaks do not match the intended output

Read the mode setting first.
Worksheet mode starts each problem on a separate page.
Compact mode uses continuous output.
In worked mode, set `problem-breaks`.
Then inspect `assignment-breaks` and `section-breaks` separately.
Explicit breaks in content and front matter still apply.

See [repository known issues](https://github.com/h35514n/coursework.tex/blob/master/docs/KNOWN-ISSUES.md) for maintenance findings and their historical evidence.
