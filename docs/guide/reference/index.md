---
layout: default
title: Reference
nav_order: 5
has_children: true
permalink: /reference/
---

# Public interfaces

Each entry gives its loading requirements, complete signature, arguments, behavior, and runnable example. Square brackets denote optional arguments; braces denote required arguments. Placeholder signatures explain syntax; the separate examples contain compilable code.

| Module | Responsibility | Loaded by the classes? |
| --- | --- | --- |
| `coursepsets.cls` | Homework layout, headers, footers, and assignment support | Select with `\documentclass` |
| `coursenotes.cls` | Notes layout, chapters, and contents | Select with `\documentclass` |
| `coursecommon.sty` | Metadata and shared configuration | Both |
| `courseassignments.sty` | Assignment declarations and rendering | Homework only |
| `courseenvironments.sty` | Theorems, formulas, math tables, and subparts | Both |
| `coursemath.sty` | Mathematics and bold-symbol backend | Both |
| `coursephys.sty` | Physics, constants, units, and script-r assets | Explicit load |
| `coursefonts.sty` | Prose and mathematics font selection | Both |

See the [alphabetical index]({{ '/command-index/' | relative_url }}) to find a specific command. Implementation helpers and commands inherited wholesale from third-party packages are not part of the custom API catalog. Useful inherited commands appear in recipes with upstream links.
