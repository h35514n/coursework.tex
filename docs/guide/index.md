---
layout: default
title: Home
nav_order: 1
permalink: /
---

<p class="eyebrow">Coursework · XeLaTeX · v2</p>

# Coursework documentation
{: #create-course-documents }

<p class="lead">Coursework provides XeLaTeX classes for homework and reading notes, with shared notation and environments. This guide covers installation, document setup, and the available commands.</p>

<div class="cards">
<a class="card" href="{{ '/getting-started/' | relative_url }}"><strong>Getting started</strong>Install the classes and compile an example.</a>
<a class="card" href="{{ '/homework/' | relative_url }}"><strong>Homework</strong>Declare problems and produce worked copies, worksheets, or compact handouts.</a>
<a class="card" href="{{ '/notes/' | relative_url }}"><strong>Reading notes</strong>Set up chapters, local contents, theorems, and formulas.</a>
<a class="card" href="{{ '/command-index/' | relative_url }}"><strong>Command index</strong>Look up syntax, defaults, examples, and required packages.</a>
</div>

## Compiled examples

Each [example]({{ '/examples/' | relative_url }}) includes a PDF and the source used to compile it.
Download a complete project to use as a starting point, or copy a code snippet from the reference.
All previews are compiled with XeLaTeX and the classes in this repository.

## Classes and notation

| Class | Document types | Default mathematics |
| --- | --- | --- |
| `coursepsets` | Homework, exams, worksheets, and problem handouts | Pazo / Palatino |
| `coursenotes` | Reading notes with chapters | TeX Gyre Pagella Math |

Both classes use Pagella prose and load shared mathematics notation and document environments.
Add `\usepackage{coursephys}` for physics notation and SI units.
You can select other [font profiles]({{ '/reference/fonts/' | relative_url }}) through class options.

This guide covers Coursework v2 and assumes basic LaTeX knowledge.
Use XeLaTeX and TeX Live 2026 with the June 2026 LaTeX kernel or newer.
