---
layout: default
title: Troubleshooting
nav_order: 8
---

# Troubleshooting

## The class or a glyph cannot be found

Check TeX's search paths with `kpsewhich coursepsets.cls`, `kpsewhich coursephys.sty`, and `kpsewhich -format='graphic/figure' coursework-scriptr.pdf`.
Both glyph PDFs must be available alongside the packages.
Use the installer for a stable checkout, or set `TEXINPUTS` for the compile command when using a temporary checkout.
Keep the trailing colon to retain the normal TeX search paths.

## The LaTeX kernel is too old

Run `xelatex --version` to check the executable, and read the `LaTeX2e <...>` line in the compile log for the kernel date.
The classes need the June 2026 kernel or newer.
If you have updated TeX Live, check that the executable on your PATH belongs to that installation.

## A vector or unit command is undefined

Add `\usepackage{coursephys}` for vectors, gradient and Laplacian operators, constants, and `siunitx` commands.
For a Unicode article, load `coursemath` with the `unicode` option before `unicode-math`.

## A required fragment is missing

Compile from the project root and check that the `directory` value and problem IDs match the files exactly.
For example, ID `01` selects `problem01.tex`, not `problem1.tex`.

Worked mode requires `solution01.tex` even for an unsolved problem, but the file can be empty.
Worksheet and compact modes never read solution or discussion files.

## IDs or selections are rejected

Each ID must start with a letter or digit, followed by letters, digits, hyphens, or underscores.
Assignment IDs must be unique in the document.

Declare the assignment before its problems, and declare each problem only once.
Selections must contain known problem IDs without duplicates, and each assignment can be printed only once.
Assignment numbers must be positive integers.

## A reference has the wrong number

Use canonical labels such as `prob:motion:01` rather than building labels from the printed problem number.
Selected problems are numbered from 1 in the selected order.
Explicit source labels must be unique across the combined document.
Run `latexmk` to complete the passes needed for references.
A formula's displayed tag is independent of its reference number.

## A table label causes an error

A `mathtable` label requires a caption, so set `caption={...},label={...}` on the same table.
Options affect only that table; use `\courseenvironmentsetup` to change defaults for subsequent tables.

Table bodies are mathematics arrays, so use `\text{...}` or `\tableheading` for text.
Supply row endings and add a bottom rule if needed.

## An example's first word disappears

V2 theorem environments accept an optional title followed by ordinary body text, without a legacy label argument.
For a labelled example, use `\begin{example}[Title]\label{ex:one}Text...`.
See the [migration map]({{ '/migration/' | relative_url }}).

## The font profile does not change

Set the profile in `\documentclass[font-profile=...]`, before fonts load with the class.
Later setup calls update the stored configuration but cannot replace the loaded font backend.
Notes chapter numerals are independent of the mathematics profile.

## An empty file creates a role section

The renderer includes optional sections when their files exist, even if those files are empty.
Remove the guide or discussion file to omit that role.
Keep an empty solution file for an unsolved problem in worked mode.

## Page breaks do not match the intended output

Check the mode first: worksheet mode starts each problem on a separate page, while compact mode uses continuous output.
In worked mode, `problem-breaks` controls problem boundaries.
Check `assignment-breaks` and `section-breaks` separately for breaks between assignments and roles.
Explicit breaks in content and front matter still apply.

See [repository known issues](https://github.com/h35514n/coursework.tex/blob/master/docs/KNOWN-ISSUES.md) for maintenance findings and their historical evidence.
