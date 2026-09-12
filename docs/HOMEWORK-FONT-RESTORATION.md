# Restore the original homework mathematics

The later [notes styling restoration](NOTES-FONT-RESTORATION.md) supersedes
the Euler notes choice recorded here; this report retains its historical results.

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

## Validated restoration

Class revision `750d53d` passes all **170 PDFs / 1,644 pages** and **34 behavioral
TeX cases**. The positioned glyph specimen matches the pre-font API rendering
pixel-for-pixel at 300 dpi. All **58 notes outputs** retain identical extracted
text, page counts, and page renders. Every output resolves the intended modules;
there are no missing glyphs, duplicate destinations, or duplicate active labels.
All 170 usual build-folder PDFs were also refreshed through the installed symlink.

| Repository | PDFs | v2.0.0 pages | Restored pages | Unchanged notes |
| --- | ---: | ---: | ---: | ---: |
| Testbed | 46 | 499 | 497 | 20 |
| PHYS 331 | 35 | 427 | 425 | 9 |
| PHYS 433 | 34 | 333 | 336 | 14 |
| PHYS 440 | 34 | 208 | 208 | 14 |
| PHYS 491 | 21 | 178 | 178 | 1 |

The deliberate homework font change alters math glyphs, extracted character
encodings, equation widths, line breaks, and pagination. The representative
PHYS 331 heading and enlarged-integral pages were visually inspected. Course
sources are unchanged. The original-font glyph comparison and unchanged notes
provide independent checks on the intended scope.

The five local `v2-pazo-homework` checkpoints freeze the restored build. Strict
comparisons against them pass; use `make compare REFERENCE=v2-pazo-homework` for
the current font selection. Older references remain intact. Revisions, hashes,
and evidence locations are recorded in
[homework-font-validation.json](homework-font-validation.json). Detailed comparisons,
logs, and API/font specimens survive under each repository's ignored
`migration-evidence/homework-font-restoration/` directory.

Legacy Computer Modern bold families emit font-size substitution notices when
the explicit enlarged integrals request intermediate sizes. No glyphs are
missing. PHYS 331's already overlong equation in `homework/02-pset/solution10.tex`
returns to its pre-font Pazo overflow of **72.29 pt** (61.61 pt in Unicode Pagella);
the midterm paragraph overflow returns to **11.39 pt**. These notices and the
existing content/layout warnings remain visible in the saved logs.
