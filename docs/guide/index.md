---
layout: default
title: Home
nav_order: 1
permalink: /
---

<p class="eyebrow">Coursework · XeLaTeX · v2</p>

# Write the course. Keep the structure.

<p class="lead">A practical guide to homework, reading notes, and the mathematics they share. Start with a working document, then find the exact command you need.</p>

<div class="cards">
<a class="card" href="{{ '/getting-started/' | relative_url }}"><strong>Start a document →</strong>Install the classes and compile your first PDF.</a>
<a class="card" href="{{ '/homework/' | relative_url }}"><strong>Build a problem set →</strong>Declare problems once. Produce worked copies, worksheets, and compact handouts.</a>
<a class="card" href="{{ '/notes/' | relative_url }}"><strong>Organize your notes →</strong>Chapters, local contents, theorems, and formulas.</a>
<a class="card" href="{{ '/command-index/' | relative_url }}"><strong>Find a command →</strong>Signatures, defaults, examples, and loading requirements.</a>
</div>

## From source to page

Every preview in this guide is compiled with XeLaTeX and the repository's actual classes. Download the source alongside its PDF, or copy an example directly from the reference. The [example gallery]({{ '/examples/' | relative_url }}) shows the results in full.

## Two classes, shared notation

| Choose | For | Default mathematics |
| --- | --- | --- |
| `coursepsets` | Homework, exams, worksheets, and problem handouts | Pazo / Palatino |
| `coursenotes` | Chapter-based reading notes | TeX Gyre Pagella Math |

Both classes load mathematics and document environments. Add `\usepackage{coursephys}` for physics notation and SI units. They share Pagella prose and accept explicit [font profiles]({{ '/reference/fonts/' | relative_url }}).

This guide assumes basic LaTeX familiarity and documents the current **v2 API**. It requires **TeX Live 2026 with the June 2026 LaTeX kernel or newer** and **XeLaTeX**.
