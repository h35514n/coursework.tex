# Migrating coursework v1 to v2

Version 2 replaces the old API.
Use an isolated course worktree.
Retain its original-class baseline.
The classes do not provide a legacy API mode.

For the self-contained PHYS 321 and PHYS 432 classes, use the [legacy workflow](LEGACY-COURSE-MIGRATION.md).
Its dialect rules and solution extraction differ from the generic v1 scanner.

## Source transformation

```sh
python3 ../coursework.tex/scripts/migrate.py . > build/migration.diff
python3 ../coursework.tex/scripts/migrate.py . --write --report build/migration.json
python3 ../coursework.tex/scripts/migrate.py .
```

The last command must report zero changes.
The scanner processes balanced groups, optional arguments, nested expressions, comments, and verbatim content.
It rejects inconsistent repeated titles and unrecognized assignment structures.
It does not silently discard content.
Inspect the proposed changes before you run the command with `--write`.
Use this tool for v1 migration only.

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
| `\abs{x}, \norm{x}` | `\abs*{x}`, `\norm*{x}` (preserve old automatic sizing) |
| `\fdd{f}{x}, \fdl{f}{x}` | `\deriv{f}{x}`, `\deriv[2]{f}{x}` |
| `\pdd{f}{x}, \pdl{f}{x}` | `\pderiv{f}{x}`, `\pderiv[2]{f}{x}` |
| `\Int[x]{a}{b}{f}` | `\integral{f}{x}{a}{b}` |
| `\eval{a}{b}{f}, \Eval{a}{b}{f}` | `\evalat{f}{a}{b}`, `\evalbracket{f}{a}{b}` |
| `\Sum[n]{a}{b}, \infsum[n]{a}` | `\sum_{n=a}^{b}`, `\sum_{n=a}^{\infty}` |
| `\Lim[b]{x}{f}` | `\lim_{x\to b} f` |
| `\twovector, \threevector, \fourvector` | `\colvector[alignment]{a\\b\\...}` |
| `\e{n}, \E{n}` | `\times 10^{n}`, `10^{n}` |
| `\u{unit}` | `\unit{unit}`. The standard text accent `\u` retains its meaning. |
| `\n` | Removed unused narrow-minus shorthand. Write `-` instead. |
| `\heading` | Explicit todos/page numbering, `\makecourseworktitle`, contents and `\makeassignmentheading` |
| `\chap, \sect` | `\assignment` and renderer-generated sections |
| `\problem, \solution, \includeproblem, \includeguide, \includediscussion` | One `\declareproblem` per fragment pair, then `\printassignment` |
| `\qqed, \SHOW, \HIDE, \TRUE, \FALSE` | Renderer-owned closing marker and named output modes |
| `\subsect` | `\paragraph*` |
| `\insertgraphic` | Standard `center`/`\includegraphics` construction |
| `\Author, \CourseNumber, \CourseName, \CourseTerm, \CourseText, \CourseTextAuthor` | `\courseworksetup` metadata and `\courseworkvalue` accessors |

These commands retain their names: `\NN`, `\ZZ`, `\QQ`, `\RR`, `\CC`, `\dd`, `\grad`, `\vect`, `\xhat`, `\yhat`, `\zhat`, `\rhat`, `\shat`, `\thetahat`, `\phihat`, `\priming`, and `\procedure`.
`\grad` no longer consumes its subsequent token.
New shared symbols are `\kB`, `\NA`, and `\dbar`.
Remove duplicate local definitions.

## Environment and structure changes

- `sublist` becomes `subparts`. Theorem environments use optional titles and standard body labels. Internal abbreviated theorem names are removed.
- `mathtable` replaces `caption=true,title={...}` with `caption={...}`. A label requires a caption. Options apply only to the current table.
- Formula references use a formula counter. Their optional displayed tags remain independent of that counter.
- Assignment IDs default to their existing directory names during migration. The renderer numbers selected problems from 1 in print order. Canonical labels use IDs independently of printed numbers.
- `expand` becomes `problem-breaks=page`. `summary` becomes `mode=compact`. Worksheet builds use `mode=worksheet`. Build overrides run when the document starts, after source configuration.
- The migrator accepts repeated inclusion lists and adjacent statement/solution imports. It moves problem titles from fragments into declarations.
- The migrator qualifies duplicate active labels with assignment IDs. It reports ambiguous references. Standard label commands retain their meanings.
- Compile from the repository root. Standalone subfiles name `homework.tex` or `notes.tex`. Do not use parent-relative paths for these names.

## Deliberate output changes

The initial environment extraction produced output identical to v1.
Later v2 changes correct problem and object references and remove duplicate destinations.
The renderer omits optional sections when no selected file for that role exists.
It places page breaks at problem boundaries.
It removes forced line breaks after formulas.
It uses shared derivative and delimiter commands.

Worked modes use consistent closing markers.
Titles show their requested document label.
The migration preserves original content and rounded constant values.

Review these changes before you save a named checkpoint.
Comparisons against the immutable v1 baseline must continue to report deliberate differences.
Inspect unexpected differences separately.
Font experiments have separate acceptance records in the [historical index](history/README.md).

The initial Unicode adoption replaced PHYS 331's `\bigintssss` commands with standard integrals.
This removed their explicit size selection.
The current API supports `\integral[size=normal|medium|large]{expression}{variable}{lower}{upper}`.
The affected statement and solution explicitly select `large`.

The migration tool flags legacy sized integrals for manual conversion.
It cannot reliably identify their unbraced integrands and differentials.
The `\mathbold` command works in text and math mode.
Nested `\mathrm` and `\mathit` retain their upright or italic shape with bold output.
