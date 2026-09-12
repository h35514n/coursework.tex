---
layout: default
title: Fonts
parent: Reference
nav_order: 7
---

# Font profiles

`coursefonts` is loaded by both classes. It selects Pagella prose, DejaVu Sans Mono at 0.85 scale, and a mathematics backend. It exposes no additional author commands: select its profile through the class option.

```latex
\documentclass[font-profile=euler]{coursenotes}
```

| Profile | Mathematics | Backend | Default for |
| --- | --- | --- | --- |
| `pazo` | Original Pazo / Palatino | `mathpazo` and `bm` | Homework |
| `pagella` | TeX Gyre Pagella Math | `unicode-math` | Notes |
| `euler` | Euler Math, upright style | `euler-math` / `unicode-math` | Explicit choice |

The class selects its default before processing options and loading fonts. A later `\courseworksetup{font-profile=...}` changes stored configuration but cannot switch an already loaded font backend. Use the class option.

The notes chapter numerals use a separate AMS Euler display face and remain independent of the mathematics profile.

## Compare the same expression

[Pazo PDF and source]({{ '/examples/font-pazo/' | relative_url }})

<img class="preview" loading="lazy" alt="Pazo mathematics with Pagella prose" src="{{ '/assets/examples/font-pazo/preview.png' | relative_url }}">

[Pagella PDF and source]({{ '/examples/font-pagella/' | relative_url }})

<img class="preview" loading="lazy" alt="Pagella mathematics with Pagella prose" src="{{ '/assets/examples/font-pagella/preview.png' | relative_url }}">

[Euler PDF and source]({{ '/examples/font-euler/' | relative_url }})

<img class="preview" loading="lazy" alt="Euler mathematics with Pagella prose" src="{{ '/assets/examples/font-euler/preview.png' | relative_url }}">

## Standalone libraries

`coursemath` and `coursephys` can be used with `article` without `coursefonts`. In that case the host document controls fonts. The [article specimen]({{ '/examples/reference-article/' | relative_url }}) exercises this separation.

[Font implementation](https://github.com/h35514n/coursework.tex/blob/master/tex/latex/coursework/coursefonts.sty) · [Homework font restoration](https://github.com/h35514n/coursework.tex/blob/master/docs/HOMEWORK-FONT-RESTORATION.md) · [Notes styling restoration](https://github.com/h35514n/coursework.tex/blob/master/docs/NOTES-FONT-RESTORATION.md)
