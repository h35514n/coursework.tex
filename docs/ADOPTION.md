# Coursework v2 adoption

The user approved the v2 API and coordinated course adoption, then selected
Pagella prose throughout, Pagella mathematics in homework, and Euler mathematics
in notes. Font configuration is centralized in `coursefonts.sty`; the defaults
require no course-specific font setup.

## Recovery and activation

The local `master` branches of `coursework.tex`, PHYS 331, 433, 440, and 491
have adopted the validated API migration and selected fonts. Each repository has an
`archive/coursework-v1` recovery branch at its original revision. The class
repository also preserves the approved API with its original typography as
`archive/coursework-v2-api`.

The installed symlink stays at `~/Library/texmf/tex/latex/coursework` and points
to the original `coursework.tex/tex/latex/coursework` checkout. Activation is
performed by advancing that checkout, without redirecting the symlink to a
development worktree. Nothing is pushed to a remote. Older mechanics and
thermal repositories with local classes remain outside this adoption.

## Validation

All four original course checkouts built their first assignment using the
installed v2 classes without a `TEXINPUTS` override. Recorder files confirmed
the installed checkout supplied every coursework module.

After font activation, homework and notes were built again in all four original
course checkouts: **8 installed-path smoke outputs** pass. Recorder and fontspec
logs confirm the selected class modules and math fonts, with no competing
mathspec, mathpazo, or eulervm package. Empty chapter/assignment placeholders do
not embed unused math fonts; their font selection is verified in the logs.

The approved font integration passes the full 170-output matrix: **1,637
pages**, compared with 1,621 at the pre-font API checkpoint. All **25 behavioral
TeX cases** and **8 migration tests** pass. There are no missing glyphs, duplicate
PDF destinations, or duplicate active labels. The original v1 baselines and
reviewed `v2-api` checkpoints remain immutable.

| Repository | PDFs | API checkpoint pages | Adopted font pages |
| --- | ---: | ---: | ---: |
| coursework-testing | 46 | 488 | 496 |
| PHYS 331 | 35 | 416 | 424 |
| PHYS 433 | 34 | 331 | 331 |
| PHYS 440 | 34 | 208 | 208 |
| PHYS 491 | 21 | 178 | 178 |

Each testbed/migration worktree retains font text/render differences in
`build/comparison-v2-api/` and the reviewed snapshot in
`checkpoints/v2-pagella-euler/`. Comparisons to that snapshot pass. The original
v1 comparison remains strict. See [adoption-validation.json](adoption-validation.json)
for pinned build revisions, manifests, and artifact paths.

Font changes alter glyph metrics and extracted Unicode characters. Warnings
remain explicit in the comparison reports: a few new paragraph overflows
(roughly 11–14 points), inherited equation overflows, and unicode-math notices
about its math-symbol/mathtools definitions. These are recorded separately
from build failures; they have not been suppressed.

Full-course font validation identified two remaining legacy integration cases.
PHYS 331 and its testbed replace two `\bigintssss` uses with standard integrals.
The shared bold helper now enters math mode when used in prose and preserves
boldness inside explicit upright/italic alphabets. Three additional behavioral
cases verify those properties under both classes and standalone legacy math.

## Post-adoption heading-spacing correction

The user reported Guide, Problem Set, and Discussion titles colliding with
their first problem heading. The class's inherited `\vspace{-4ex}` title
after-code caused a measured 2.67-point overlap. It is replaced with explicit
`titlesec` spacing. The first PHYS 331 assignment now has a 17.2-point gap in
all three sections, verified from PDF text bounds and page renders.

The 25-case API suite passes with an added rendered-heading check; that check
fails against the pre-fix PDF. The full-matrix counts above describe the font
adoption checkpoint before this subsequent spacing correction.

## Explicit integral sizes

Following the user's review of the resized PHYS 331 integrals, `\integral`
accepts `size=normal|medium|large`. Its default rendering is unchanged.
Medium and large enlarge the selected font's display integral by one and two
relative-size steps; this is an explicit author choice, not automatic sizing.
The PHYS 331 statement and solution use `large`, including their standard
integral formula. That formula places the differential after the fraction
to follow the shared command's argument convention.

The expanded 29-case API suite verifies all three sizes with Pagella homework,
Euler notes, and standalone legacy math; nested and consecutive calls do not
leak settings. Default dimensions match the original expression in inline
and display styles. Invalid sizes fail explicitly. The eight migration tests
pass, including the requirement to review legacy sized-integral conversions.
