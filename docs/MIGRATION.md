# Migrating coursework v1 to v2

Version 2 replaces the old API. Work in an isolated course worktree and keep its original-class baseline. No legacy API mode is provided.

## Source transformation

```sh
python3 ../coursework-refactor/scripts/migrate.py . > build/migration.diff
python3 ../coursework-refactor/scripts/migrate.py . --write --report build/migration.json
python3 ../coursework-refactor/scripts/migrate.py .
```

The last command should report zero changes. The scanner handles balanced groups, optional arguments, nested expressions, comments and verbatim. It rejects inconsistent repeated titles and unrecognized assignment structure instead of silently dropping content. Inspect the dry-run before applying it. It is a v1 migration tool, not a formatter for newly authored v2 documents.

## Complete command map

| Old command | Replacement |
| --- | --- |
| `\D` | `\deriv` |
| `\Deg` | `\ensuremath{^\circ}` |
| `\L` | `\left` |
| `\PD` | `\pderiv` |
| `\R` | `\right` |
| `\bc` | `\bracket*` |
| `\bm` | `\mathbold` |
| `\brcurs` | `\separationvect` |
| `\bs` | `\bracket*` |
| `\cheq` | `\checkeq` |
| `\cndprb` | `\conditionalprob` |
| `\comb` | `\combinations` |
| `\cov` | `\covariance` |
| `\creq` | `\crosseq` |
| `\double` | `\tableheading` |
| `\ex` | `\expectation` |
| `\full` | `\displaystyle` |
| `\hrcurs` | `\separationunit` |
| `\ith` | `i\text{th}` |
| `\ivda` | `\int \uprightvect{v}\cdot\dd\uprightvect{a}` |
| `\ivdl` | `\int \uprightvect{v}\cdot\dd\uprightvect{l}` |
| `\lap` | `\laplacian` |
| `\mc` | `\text{,}\hspace{1em}` |
| `\mean` | `\average` |
| `\mtxt` | `\mathtext` |
| `\nth` | `n\text{th}` |
| `\p` | `\paren*` |
| `\parv` | `\pathregion` |
| `\pd` | `\partial` |
| `\perm` | `\permutations` |
| `\prob` | `\probability` |
| `\qeq` | `\questioneq` |
| `\rcurs` | `\separation` |
| `\sarv` | `\surfaceregion` |
| `\sfrac` | `\slashfrac` |
| `\siNa` | `\constantvalue{avogadro}` |
| `\sikB` | `\constantvalue{boltzmann}` |
| `\var` | `\variance` |
| `\varv` | `\volumeregion` |
| `\vectrm` | `\uprightvect` |
| `\vhat` | `\unitvect` |
| `\vhatrm` | `\uprightunitvect` |
| `\x` | `\times` |
| `\abs{x}, \norm{x}` | \abs*{x}, \norm*{x} (preserve old automatic sizing) |
| `\fdd{f}{x}, \fdl{f}{x}` | \deriv{f}{x}, \deriv[2]{f}{x} |
| `\pdd{f}{x}, \pdl{f}{x}` | \pderiv{f}{x}, \pderiv[2]{f}{x} |
| `\Int[x]{a}{b}{f}` | \integral{f}{x}{a}{b} |
| `\eval{a}{b}{f}, \Eval{a}{b}{f}` | \evalat{f}{a}{b}, \evalbracket{f}{a}{b} |
| `\Sum[n]{a}{b}, \infsum[n]{a}` | \sum_{n=a}^{b}, \sum_{n=a}^{\infty} |
| `\Lim[b]{x}{f}` | \lim_{x\to b} f |
| `\twovector, \threevector, \fourvector` | \colvector[alignment]{a\\b\\...} |
| `\e{n}, \E{n}` | \times 10^{n}, 10^{n} |
| `\u{unit}` | \unit{unit}; standard text \u is restored |
| `\n` | Removed (unused narrow-minus shorthand); write - |
| `\heading` | Explicit todos/page numbering, \makecourseworktitle, contents and \makeassignmentheading |
| `\chap, \sect` | \assignment and renderer-generated sections |
| `\problem, \solution, \includeproblem, \includeguide, \includediscussion` | One \declareproblem per fragment pair, then \printassignment |
| `\qqed, \SHOW, \HIDE, \TRUE, \FALSE` | Renderer-owned closing marker and named output modes |
| `\subsect` | \paragraph* |
| `\insertgraphic` | Standard center/includegraphics construction |
| `\Author, \CourseNumber, \CourseName, \CourseTerm, \CourseText, \CourseTextAuthor` | \courseworksetup metadata and \courseworkvalue accessors |

Retained: `\NN`, `\ZZ`, `\QQ`, `\RR`, `\CC`, `\dd`, `\grad`, `\vect`, `\xhat`, `\yhat`, `\zhat`, `\rhat`, `\shat`, `\thetahat`, `\phihat`, `\priming`, and `\procedure`. `\grad` no longer consumes its following token. New shared symbols are `\kB`, `\NA`, and `\dbar`. Remove local duplicate definitions.

## Environment and structure changes

- `sublist` becomes `subparts`. The theorem environments use optional titles and ordinary body labels. Internal abbreviated theorem names are removed.
- `mathtable` replaces `caption=true,title={...}` with `caption={...}`. A label without a caption is an error. Defaults do not leak between tables.
- Formula labels reference an actual formula counter; their optional displayed tags remain independent.
- Assignment IDs default in migration to their existing directory basename. Selected problems renumber from 1 in print order. Canonical labels use IDs, not printed numbers.
- `expand` becomes `problem-breaks=page`; `summary` becomes `mode=compact`; worksheet builds use `mode=worksheet`. Build-time overrides run at begin-document after source configuration.
- The migrator accepts both repeated inclusion lists and older adjacent statement/solution imports. It moves fragment-level problem titles into declarations.
- Duplicate active labels across assignments receive explicit assignment qualifiers; ambiguous references are reported. Standard label commands are untouched.
- Run builds from the repository root. Standalone subfiles name `homework.tex` or `notes.tex`, not their parent-relative paths.

## Deliberate output changes

The mechanical environment extraction is pixel-identical to v1. Subsequent v2 changes deliberately repair problem/object references, remove duplicate destinations, omit empty sections, move page breaks to problem boundaries, remove formula trailing line breaks, and use the consolidated derivative/delimiter helpers. Rendered closing markers are consistent across worked modes. Titles now display their requested document label. Original content and rounded constant values are preserved.

Use named checkpoints only after inspecting these changes. A comparison against the immutable v1 baseline should continue to report differences; that is not permission to disregard unexpected differences. Font experiments are separate from API acceptance.

The adopted Unicode fonts also replace the two PHYS 331 uses of the legacy
`\bigintssss` glyph with the selected font's standard `\int`. The migration
tool records this transformation; it changes integral sizing, not the
integrand or bounds. `\mathbold` works in prose and mathematics, and nested
`\mathrm`/`\mathit` retain their upright/italic choice while becoming bold.
