# PHYS 321 and PHYS 432: local Coursework v2 adoption

Completed September 11, 2026. Both original local `master` branches now contain
the validated migration and have signed `coursework-v2-adopted` tags. No remote
was created and nothing was pushed. The two course migration worktrees and the
tooling worktree were removed after retaining their commits and evidence.

The adopted fonts are Pagella prose, Pazo/Palatino homework mathematics, and
Euler notes mathematics. This migration changes no shared TeX runtime module,
glyph asset, installation link, document API, or font default.

## Revisions and preservation

| Repository | Original / `archive/coursework-v1` | Font-compatible legacy classes | Prepared legacy fixtures | Adopted `master` / signed tag |
| --- | --- | --- | --- | --- |
| [PHYS 321](../../phys321-classical-mechanics/README.md) | `14c974480faf7fb97878b094cee548cd06d6a3da` | `97a2e9cd2fb5f538958274b401da697634226255` | `24e511dc05ca791ee42e0c18ebea53ecaccbd184` | `bbd2529aaa78abb8ff560b107c6b507ab13fa244` |
| [PHYS 432](../../phys432-thermal-physics/README.md) | `fdcdf4ebc92d6c19121ffc0e3e4557ba692c19b1` | `0451fb7b5f345e5c30c4b2463b7352f89b50c5ea` | `0b4e24b296c087f7af4e3a8b4ba3c86dcfdcfaff` | `cdf957dc184d8418e9660ffce3e8fc1503711b54` |

The runtime is byte-identical to class revision
`41d0e4bf1c3c9f3988fb22fe6abbbb8a180c626b`. The final 102-output rebuild used
tooling revision `9086706fac321a232061e5cc2a431ccddd5441ee` from the original
`coursework.tex` checkout, after removing the course migration worktrees.
Later changes in this delivery only record the results and evidence index.

Signed commits separate legacy font lookup repairs, structural preparation,
API migration, and subsequent reference/build-compatibility repairs. The font
lookup repairs use filenames for the same legacy fonts. Preparation retains
legacy rendering; explicit subfile state and a final paragraph boundary preserve
the combined output. PHYS 321's later reference repair converts manually tagged
equations to unnumbered equation environments with the original explicit tags.
Both courses preserve chapter-qualified section references despite their short
printed section headings. Commit and tag signature receipts are retained in
the class evidence archive.

Original Git source archives, local classes, and supplied PDFs have SHA-256
inventories. All 44 mechanics and 9 thermal source graphics, handouts, and other
non-TeX assets were checked unchanged. The three mechanics study guides remain
unchanged under `handouts/study_guides/`, outside the build matrix. Their original
dependencies are recoverable together through the complete original archive or
recovery ref. Obsolete root PDFs are archived; new output belongs under `build/`.

## Document and numbering mappings

Mechanics `problems.tex` and thermal `assignments.tex` become `homework.tex`.
Metadata and explicit physics notation loading live in `course.tex`. Each
assignment is a subfile at `homework/<stable-id>.tex`, declaring each problem
once. In original problem order, problem N becomes
`homework/<stable-id>/problemNN.tex` and its solution becomes
`homework/<stable-id>/solutionNN.tex`. Statement and solution content may have
originated inline, in an imported problem, or in an imported solution body.
The balanced scanner expands those imports without discarding comments.

The source inventories and assignment mappings are in each course's
`migration-map.json`; original extracted statement/solution hashes, problem
titles, empty bodies, imported-source hashes, and explicit label/reference
renames are in `migration-content.json`. The final audit re-extracts the frozen
legacy sources and checks the migrated content against the prescribed
transformations, including the documented repairs below.

### Mechanics

| Original identity | Displayed assignment | Stable ID / assignment subfile stem | Problems |
| --- | ---: | --- | ---: |
| Problem Set 1 | 1 | `01-pset` | 10 |
| Problem Set 2 | 2 | `02-pset` | 10 |
| Problem Set 3 | 3 | `03-pset` | 8 |
| Problem Set 4 | 4 | `04-pset` | 6 |
| Midterm Exam | 5 | `midterm` | 7 |
| Problem Set 5 | 6 | `05-pset` | 5 |
| Problem Set 6 | 7 | `06-pset` | 8 |
| Problem Set 7 | 8 | `07-pset` | 11 |
| Final Exam | 9 | `final` | 7 |

All 72 problems are retained. The eight notes files keep their original names:
`chapter01`, `chapter01-appendix`, `chapter02`, `chapter03`, `chapter04`,
`chapter06`, `chapter07`, and `chapter09`, under `notes/`. Their chapter numbers,
gaps, appendix position, and local contents are preserved. Appendix and reset
section destinations use source identity without altering printed numbers.

### Thermal

| Original identity | Displayed assignment | Stable ID / assignment subfile stem | Problems |
| --- | ---: | --- | ---: |
| Problem Set 1 | 1 | `01-pset` | 12 |
| Quiz 1 | 2 | `01-quiz` | 10 |
| Problem Set 2 | 3 | `02-pset` | 10 |
| Quiz 2 | 4 | `02-quiz` | 10 |
| Problem Set 3 | 5 | `03-pset` | 9 |
| Quiz 3 | 6 | `03-quiz` | 10 |
| Midterm | 7 | `04-midterm` | 27 |
| Problem Set 5 | 8 | `05-pset` | 10 |
| Quiz 5 | 9 | `05-quiz` | 10 |
| Problem Set 6 | 10 | `06-pset` | 10 |
| Quiz 6 | 11 | `06-quiz` | 10 |
| Problem Set 7 | 12 | `07-pset` | 10 |
| Quiz 7 | 13 | `07-quiz` | 10 |
| Final | 14 | `08-final` | 45 |

All 193 problems and 13 whitespace-empty solutions are retained. A further
solution contains only its original comment. No answers were supplied.
All nineteen notes fragments keep their original filenames and chapter-number
prefixes. “Useful mathematics” remains section A attached to the introduction;
the gaps through chapter 33 are retained. The full ordered list is recorded in
[the thermal mapping](../../phys432-thermal-physics/migration-map.json).

## Validation and accepted differences

| Course | Worked assignments | Compact assignments | Worksheets | Individual notes | Combined homework, compact, notes | Total PDFs | Total pages |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PHYS 321 | 9 | 9 | 9 | 8 | 3 | 38 | 366 |
| PHYS 432 | 14 | 14 | 14 | 19 | 3 | 64 | 752 |
| Total | 23 | 23 | 23 | 27 | 6 | 102 | 1,118 |

Before API conversion, both prepared combined homework and notes matched their
freshly rebuilt legacy references exactly in page count, extracted text, and
120-dpi page renders. The complete prepared legacy matrix contains 102 PDFs
and 1,180 pages. Supplied historical PDFs remain separate evidence because the
TeX environment and fonts in those saved PDFs can differ from a fresh build.

After migration, all 102 outputs were compared with the legacy baseline. The
reviewed results are frozen as `checkpoints/v2-adopted/`. A second complete
rebuild from the original checkouts passes strict comparison with those
checkpoints: identical text, page counts, and page renders, with no new warnings.
PDF byte hashes are retained as provenance; binary PDF equality is not the
rendering criterion. The normal installed-class combined homework and notes
builds also passed from both original checkouts.

| Combined document | Fresh legacy pages | Adopted pages |
| --- | ---: | ---: |
| Mechanics homework | 90 | 115 |
| Mechanics compact problems | 17 | 19 |
| Mechanics notes | 11 | 11 |
| Thermal homework | 200 | 187 |
| Thermal compact problems | 59 | 41 |
| Thermal notes | 46 | 46 |

Accepted differences are the existing v2 assignment/title layout, sequential
assignment and object numbering, reference destinations, renderer-owned problem
page boundaries, standard shared environments, and the selected notes font
profile. Mechanics adopts the shared 11-point homework layout and standard
margins in place of its local 10-point layout with smaller vertical margins.
This explains the substantial mechanics homework pagination increase. Worked
problems start on separate pages; compact output flows, and worksheets omit
solutions while retaining workspace.

The notation conversion preserves the distinct legacy sum signatures and
bounds. Simple derivatives use `\deriv`/`\pderiv`; richer `diffcoeff` syntax,
including held-variable derivatives, remains intact. Mechanics `\bvect` becomes
`\uprightvect`, and `\mechanicsdot`/`\mechanicsddot` preserve the original
scaled bullet accents. The physics package's bold cross-product sign remains
bold through `\mathbold{\times}`. Native theorem titles and body text are
preserved according to each local class's actual environment definitions.

Two content-adjacent cases are explicit:

- The existing literal `TODO` after mechanics final-exam problem 3's solution
  moves to the end of its statement, keeping it visible in every output mode.
- Thermal notes used the text dot-below accent `\d{V}` inside mathematics in
  the fundamental thermodynamic relation. Separate compatibility commit
  `5501adb` replaces it with `\dd V`, the intended volume differential. Its
  historical missing-glyph warning remains in the baseline and is absent from
  migrated output.

Thermal's supplied saved notes PDF used Pagella Math and had 44 pages. The
fresh legacy build uses Euler and has 46 pages. Adopted notes use the explicitly
selected Euler profile; the supplied PDF is not treated as an Euler reference.

All final outputs have correct class/package resolution, no missing glyphs,
no duplicate active labels, and no duplicate PDF destinations. Canonical problem
labels and cleveref types match sequential assignment/problem values. Compact
and worksheet recorder files contain no solution inputs. Existing references
were resolved from their source context; no ambiguous references remain for
manual decision. Notes' chapter-qualified section reference values match the
legacy values.

Visual inspection covered mechanics accents and diagrams, heading separation,
appendix numbering, thermal tables and sum bounds, barred differentials,
held-variable derivatives, and worksheets. All output text and render
differences are retained, along with reviewed-page hashes. Source and recorder
audits cover every problem, including empty solutions and multi-page problems.

The 34 behavioral TeX cases, 24 migration/snapshot Python tests, and 9 existing
regression-harness tests pass. New coverage includes embedded and mixed imported
solutions, empty solutions, dialect-specific sums, rich derivatives, duplicate
labels within an assignment, archived-file exclusions, relocated local-class
snapshots, and corruption rejection. The migrator is dry-run by default and a
repeat conversion of either migrated course reports zero operations.

Builds used TeX Live 2026/XeTeX 0.999998, latexmk 4.88, Poppler 26.09.0, and
ImageMagick 7.1.2-31. Manifests record full versions, commands, fixed build epochs,
class and fixture revisions, resolved modules, recorder inputs, and PDF/text/page
hashes. Audit reports include twelve resolved primary font files and their
hashes; each inspected PDF has a `pdffonts` report.

## Warning backlog

Layout and package warnings remain visible. Counts below include repeated
content in combined, individual, compact, and worksheet outputs; they are not
counts of unique source defects.

| Course | Overfull occurrences | Distinct output/warning entries | Representative follow-up |
| --- | ---: | ---: | --- |
| Mechanics | 124 | 108 | `05-pset` equation/figure layout up to 60.17 pt; `04-pset` paragraph about 48.80 pt; `03-pset`/midterm figure layouts about 48.78 pt |
| Thermal | 188 | 118 | `06-quiz` displays up to 56.12 pt and 54.06 pt; probability notes paragraph about 33.40 pt |

Thermal standalone `01-useful-maths` references `sec:velocity_distribution`,
and standalone `05-mb-distribution` references `eq:guassian_integral` outside
their chapters. Both resolve in combined notes. Mechanics has no unresolved
references. Underfull boxes, classicthesis's 7.5-point overfull vertical boxes,
PDF-string/bookmark notices, and package configuration notices are also retained.

The legacy comparisons record 132 mechanics and 81 thermal warning occurrences
as new relative to legacy, including changed source locations and layouts.
These are not suppressed or represented as a warning-free migration. There
are zero new warnings relative to the reviewed adopted checkpoint. Each
`migration-evidence/warning-backlog.json` contains the complete current warning
inventory and the legacy comparison's new/resolved split. Mathematical assertions
and unrelated source typos remain outside this migration.

## Evidence locations and integrity

[The tracked validation index](legacy-courses-validation.json) records full
revisions and SHA-256 hashes for the retained manifests, reports, and complete
file inventories. Paths inside inventories are relative to their repository;
they remain useful if the repository is relocated. Historical manifests and
logs retain their original absolute paths as provenance and were not rewritten.
The driver resolves bundled classes relative to the frozen artifact directory
and rejects modified classes, fixtures, PDFs, text, or page renders.

In each original course checkout:

- `baseline/`: immutable prepared legacy classes, fixtures, 38 or 64 PDFs,
  logs, extracted text, page renders, package paths, and manifests.
- `checkpoints/v2-adopted/`: immutable reviewed v2 reference with bundled
  classes, fixtures, full output inventory, and acceptance reason.
- `migration-evidence/original/` and `supplied-pdfs/`: original source tar,
  extracted source tree, local classes, supplied PDFs, and original inventories.
- `migration-evidence/legacy-rebuild/` and `preparation-comparison/`: fresh
  legacy references and strict structural-preparation comparison. Earlier
  preparation attempts remain separately labeled historical artifacts.
- `migration-evidence/comparison-legacy/`, `comparison-v2-adopted/`, and
  `post-adoption-comparison/`: reviewed differences and strict comparison
  results before and after local adoption.
- `migration-evidence/post-adoption-validation.json`,
  `post-adoption-candidate-manifest.json`, `installed-build/`,
  `installed-build.json`, `visual-review.json`, and `warning-backlog.json`:
  source audits, final build provenance, normal combined-build evidence,
  visual review, and remaining warnings.
- `migration-evidence/retained-files.json`: complete SHA-256 inventory of
  `baseline/`, `checkpoints/`, and `migration-evidence/`, excluding itself.

The class checkout retains behavioral tests, Python test logs, the manual
equation-tag test, runtime and installation hashes, signature receipts, and
relocation receipts under `migration-evidence/legacy-courses/`. Its complete
inventory is `migration-evidence/legacy-courses/inventory.json`. Relocation
verified every copied file before and after moving the archives; subsequent
rebuilds verified that no removed worktree was required.

These large artifacts are local, ignored evidence. Back them up with the
repositories if preserving the compiled history matters; Git recovery refs
preserve source but do not contain the ignored build archive.

## Permanent commands and rollback

Run from either original course repository:

```sh
make
make problems
make worksheets
make baseline
make compare REFERENCE=v2-adopted
python3 ../coursework.tex/scripts/check_course_migration.py . --output build/validation.json
```

`make compare` without `REFERENCE` intentionally stays strict against the
legacy baseline and reports the reviewed migration differences. The canonical
driver is in the original `coursework.tex/scripts/` directory; `COURSEWORK_TOOLS`
can override that directory, and `candidate_repository` in `regression.json`
can select experimental classes for scoped test builds. The installation link
still points to the original class checkout. All eight modules and both glyph
assets were verified through `kpsewhich` and actual recorder inputs.

To review the exact original source without altering adopted `master`:

```sh
# From the mechanics checkout:
git worktree add ../phys321-legacy-review archive/coursework-v1
# From the thermal checkout:
git worktree add ../phys432-legacy-review archive/coursework-v1
```

Those exact originals retain the historical font-lookup issue. For a buildable
legacy comparison with the repaired local classes and standalone targets, use
prepared revision `24e511d` for mechanics or `0b4e24b` for thermal in a separate
worktree instead. The signed adoption tag preserves the complete v2 source.
No branch reset, shared class downgrade, remote update, or force push is needed
to inspect either state. The local-class archive retains the study guides and
their historical dependencies together.
