---
layout: default
title: Reference
nav_order: 5
has_children: true
permalink: /reference/
---

# Reference
{: #public-interfaces }

Each entry describes the required packages, syntax, arguments, and behavior, followed by example code and a link to a complete project.
In signatures, square brackets mark optional arguments and braces mark required arguments.
Signatures use placeholders to explain the syntax; the examples contain code you can compile.

| Module | Purpose | Class support |
| --- | --- | --- |
| `coursepsets.cls` | Homework layout, headers, footers, and assignments | Select with `\documentclass` |
| `coursenotes.cls` | Notes layout, chapters, and contents | Select with `\documentclass` |
| `coursecommon.sty` | Metadata and shared configuration | Both classes |
| `courseassignments.sty` | Assignment declarations and output | Homework only |
| `courseenvironments.sty` | Theorems, formulas, mathematics tables, and subparts | Both classes |
| `coursemath.sty` | Mathematics notation and bold symbols | Both classes |
| `coursephys.sty` | Physics, constants, units, and script-r assets | Load explicitly |
| `coursefonts.sty` | Prose and mathematics fonts | Both classes |

Use the [command index]({{ '/command-index/' | relative_url }}) to find a command.
The reference covers Coursework commands and environments, with selected third-party commands used in the examples.
Internal helpers and most third-party commands are excluded.
Links to third-party documentation provide details about inherited commands.
