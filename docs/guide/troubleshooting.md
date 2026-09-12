---
layout: default
title: Troubleshooting
nav_order: 8
---

# Troubleshooting

## The class or a glyph cannot be found

Check `kpsewhich coursepsets.cls`, `kpsewhich coursephys.sty`, and `kpsewhich -format='graphic/figure' coursework-scriptr.pdf`. Both glyph PDFs must be available alongside the packages. Use the installer from a stable checkout, or set scoped `TEXINPUTS` with a trailing colon.

## The LaTeX kernel is too old

Run `xelatex --version` and inspect the `LaTeX2e <...>` line in the log. The coursework classes require the June 2026 kernel or newer. Confirm that the executable on your PATH belongs to your updated TeX Live installation.

## A vector or unit command is undefined

Physics notation is optional. Load `\usepackage{coursephys}`. It supplies vector helpers, gradient and Laplacian operators, constants, and `siunitx`. Load math before `unicode-math` with the `unicode` option when configuring a Unicode article yourself.

## A required fragment is missing

Build from the project root. Match `directory` and problem IDs exactly: ID `01` looks for `problem01.tex`, not `problem1.tex`. Worked mode requires `solution01.tex`, even for an unsolved problem; an empty file is valid. Worksheet and compact modes never read solution or discussion files.

## IDs or selections are rejected

IDs begin with a letter or digit. Remaining characters may be letters, digits, hyphens, or underscores. Assignment IDs must be unique in the document. Declare an assignment before its problems; declare each problem once; select known IDs without duplicates; render once. Assignment numbers must be positive.

## A reference has the wrong number

Use canonical labels such as `prob:motion:01`, not labels built from the printed ordinal. A reordered selection renumbers from 1. Explicit source labels must be unique across the combined document. Run `latexmk` to complete reference passes. A formula's displayed tag is independent of its reference number.

## A table label errors, or the next table inherits settings

A `mathtable` label requires a caption. Use `caption={...},label={...}` on the same table. Options are local to each table; change subsequent defaults explicitly with `\courseenvironmentsetup`. Table bodies are math arrays: use `\text{...}` or `\tableheading` for text and supply row endings and any bottom rule.

## An example's first word disappears

V2 theorem-like environments take an optional title and ordinary body text. Write `\begin{example}[Title]\label{ex:one}Text...`; do not pass a legacy special label argument. See the [migration map]({{ '/migration/' | relative_url }}).

## Changing font-profile in the preamble has no effect

Set the profile in `\documentclass[font-profile=...]`. Fonts load with the class. Notes chapter numerals are independent of the mathematics profile.

## A role section appears despite an empty file

Optional sections are controlled by file presence. Remove the optional guide or discussion file if you want that role absent. An empty solution file remains useful for a worked problem you have not solved yet.

## Page breaks do not match the intended output

Check the mode first: worksheet forces problem pages and compact flows. In worked mode, set `problem-breaks`. Then check `assignment-breaks` and `section-breaks` independently. Explicit breaks inside content and front matter still apply.

[Repository known issues](https://github.com/h35514n/coursework.tex/blob/master/docs/KNOWN-ISSUES.md) records maintenance findings and historical context.
