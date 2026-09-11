# Restore the original homework mathematics

The homework default is again Pazo/Palatino mathematics with Pagella prose.
Notes retain Pagella prose and Euler mathematics. The v2 API, heading-spacing
fix, and explicit integral sizes remain in place. No course source changes
are needed; the installed class symlink already selects this checkout.

## Correction to the original font assessment

The original homework class loaded `mathpazo`, then `mathspec`, and called
`\setmathfont{TeX Gyre Pagella Math}`. With `mathspec`, omitting the parenthesized
character-set argument selects its `Special` handler, whose default is a no-op.
Thus that line did not establish Pagella Math. The archived homework PDFs
actually embed URW Palladio, Pazo Math, and Computer Modern math symbols,
alongside Pagella prose. The Unicode font migration replaced those math faces.
Describing that migration as retaining the existing homework font was incorrect.

## Implementation and verification

The `pazo` profile restores `mathpazo` with its original options and uses
`fontspec`'s `no-math` option for prose. The ineffective `mathspec` setup is
unnecessary. The `mathbold` expression helper retains the `bm` backend and its
ability to work in prose; `mathpazo`'s identically named alphabet does not replace it.
Explicit `font-profile=pagella` and `font-profile=euler` options remain available.

Run `python3 tests/run_api.py` for behavior and profile-loading tests and
`python3 tests/check_homework_font.py` for the original-font comparison. The latter
compares identical positioned glyph rows against `archive/coursework-v2-api`,
including Greek, delimiters, integrals, derivatives, bold vectors, and script-r.
It resolves the same prose and mono font files by filename in a scratch copy of
the reference; frozen baselines and checkpoints are never modified.

The signed `v2.0.0` tag and `v2-final` checkpoints describe the earlier Unicode
homework release and remain historical references. Comparisons with them will
show the intentional homework font and pagination changes.
