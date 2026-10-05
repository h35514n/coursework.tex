---
layout: default
title: Home
nav_order: 1
permalink: /
---

<p class="eyebrow">Coursework · XeLaTeX · v2</p>

# Create course documents

<p class="lead">Use this guide to create homework and reading notes. Start with a complete example. Use the reference to find commands.</p>

<div class="cards">
<a class="card" href="{{ '/getting-started/' | relative_url }}"><strong>Start a document →</strong>Install the classes. Compile your first PDF.</a>
<a class="card" href="{{ '/homework/' | relative_url }}"><strong>Create homework →</strong>Declare problems. Select worked copies, worksheets, or compact handouts.</a>
<a class="card" href="{{ '/notes/' | relative_url }}"><strong>Create notes →</strong>Add chapters, local contents, theorems, and formulas.</a>
<a class="card" href="{{ '/command-index/' | relative_url }}"><strong>Find a command →</strong>Read signatures, defaults, examples, and package requirements.</a>
</div>

## Compiled examples

The guide build compiles each preview with XeLaTeX and this repository's classes.
Each example includes its source and PDF.
Download an example from the [example gallery]({{ '/examples/' | relative_url }}).
You can also copy code from the reference.

## Classes and notation

| Class | Document types | Default mathematics |
| --- | --- | --- |
| `coursepsets` | Homework, exams, worksheets, and problem handouts | Pazo / Palatino |
| `coursenotes` | Reading notes with chapters | TeX Gyre Pagella Math |

Both classes load mathematics notation and document environments.
For physics notation and SI units, add `\usepackage{coursephys}`.
Both classes use Pagella prose.
You can select other [font profiles]({{ '/reference/fonts/' | relative_url }}) through class options.

This guide describes the current v2 API for readers with basic LaTeX knowledge.
Use XeLaTeX and TeX Live 2026 with the June 2026 LaTeX kernel or newer.
