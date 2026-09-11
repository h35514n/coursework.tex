# Coursework font review

This is the historical font-choice report. Pagella prose, Pagella homework math,
and Euler notes math were subsequently adopted. Statements below about pending
review describe the original experiment. See [FINALIZATION.md](FINALIZATION.md)
for current status and [evidence-index.json](evidence-index.json) for relocated evidence.

**Decision:** adopt Pagella prose in both classes, Pagella mathematics in
homework, and Euler mathematics in notes. Euler has no corresponding regular,
italic, and bold prose family; the user explicitly selected Pagella prose as
its companion. See [ADOPTION.md](ADOPTION.md) for activation and validation.
The following is the original specimen review record.

Both choices use the same v2 API and XeLaTeX. The font experiment is isolated on `codex/coursework-fonts`; the API migration branch retains the original typography.

- **Distinct styles:** Pagella homework and Euler notes.
- **Unified style:** Pagella homework and Pagella notes.

Both variants use TeX Gyre Pagella text and DejaVu Sans Mono, resolved by filename from TeX Live. Homework is common to both choices. The notes comparison isolates the math-font change.

## Builds

| Document | Profile | Pages | Missing glyphs |
| --- | --- | --- | --- |
| specimen-pagella-homework | pagella | 2 | 0 |
| specimen-euler-notes | euler | 2 | 0 |
| specimen-pagella-notes | pagella | 2 | 0 |
| euler-01-useful-maths | euler | 4 | 0 |
| euler-03-probability | euler | 6 | 0 |
| pagella-01-useful-maths | pagella | 4 | 0 |
| pagella-03-probability | pagella | 5 | 0 |
| pagella-assignment | pagella | 17 | 0 |

Specimens are assembled in `output/pdf/coursework-font-comparison.pdf`. Individual PDFs, text, renders, font inventories, paths, and logs are under `build/font-review/`. The API suite also passes with these fonts.

The committed `docs/font-review-manifest.json` records the build revisions, file hashes, font paths, embedded fonts, and package/font warnings for this review. Against the original-font API build, the representative assignment increases from 16 to 17 pages. The probability chapter is six pages with Euler and five with Pagella; Useful Mathematics is four pages in both profiles.

Expected differences include equation width, delimiter and integral shapes, Greek letter forms, and resulting line/page breaks. Euler uses upright mathematical letters; Pagella uses conventional italic variables. Font selection is pending user review. Neither profile has been installed.
