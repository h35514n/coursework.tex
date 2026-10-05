---
layout: default
title: Reference
nav_order: 5
has_children: true
permalink: /reference/
---

# Public interfaces

Each entry gives the required packages, signature, arguments, behavior, and a complete example.
Square brackets identify optional arguments.
Braces identify required arguments.
Signatures contain placeholders to explain syntax.
The separate examples contain code that you can compile.

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
The catalog excludes internal helpers and most commands from third-party packages.
The guide links to third-party documentation where examples use inherited commands.
