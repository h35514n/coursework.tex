---
layout: default
title: Font profiles
parent: Reference
nav_order: 7
---

# Font profiles

Both classes load `coursefonts`, which selects Pagella prose, DejaVu Sans Mono at 0.85 scale, and a mathematics backend.
The package has no additional author commands; choose the profile through a class option.

```latex
\documentclass[font-profile=euler]{coursenotes}
```

| Profile | Mathematics | Backend | Default use |
| --- | --- | --- | --- |
| `pazo` | Original Pazo / Palatino | `mathpazo` and `bm` | Homework |
| `pagella` | TeX Gyre Pagella Math | `unicode-math` | Notes |
| `euler` | Euler Math with upright letters | `euler-math` / `unicode-math` | Explicit selection |

The class selects its default profile, processes options, and then loads fonts.
A later `\courseworksetup{font-profile=...}` updates the stored configuration but cannot replace the loaded backend.
Choose fonts in the class options.

Notes chapter numerals use a separate AMS Euler display font, independent of the mathematics profile.

## Font comparison
{: #compare-an-expression }

[Pazo PDF and source]({{ '/examples/font-pazo/' | relative_url }})

<img class="preview" loading="lazy" alt="Pazo mathematics with Pagella prose" src="{{ '/assets/examples/font-pazo/preview.png' | relative_url }}">

[Pagella PDF and source]({{ '/examples/font-pagella/' | relative_url }})

<img class="preview" loading="lazy" alt="Pagella mathematics with Pagella prose" src="{{ '/assets/examples/font-pagella/preview.png' | relative_url }}">

[Euler PDF and source]({{ '/examples/font-euler/' | relative_url }})

<img class="preview" loading="lazy" alt="Euler mathematics with Pagella prose" src="{{ '/assets/examples/font-euler/preview.png' | relative_url }}">

## Standalone packages

You can use `coursemath` and `coursephys` with `article` without loading `coursefonts`, leaving font selection to the host document.
See the [article example]({{ '/examples/reference-article/' | relative_url }}).

[Font source](https://github.com/h35514n/coursework.tex/blob/master/tex/latex/coursework/coursefonts.sty) · [Homework font history](https://github.com/h35514n/coursework.tex/blob/master/docs/history/HOMEWORK-FONT-RESTORATION.md) · [Notes font history](https://github.com/h35514n/coursework.tex/blob/master/docs/history/NOTES-FONT-RESTORATION.md)
