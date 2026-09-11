# Migrating the self-contained PHYS 321 and PHYS 432 classes

The legacy courses use their own `notes.cls` and `problemsets.cls`, with
embedded solutions and different command definitions. Do not run the generic
v1 migrator over these repositories or their archived study guides.

Use an isolated course worktree. The dedicated scanner is dry-run by default:

```sh
python3 ../coursework.tex/scripts/migrate_legacy.py prepare . --dialect mechanics
python3 ../coursework.tex/scripts/migrate_legacy.py prepare . --dialect mechanics --write
# Use --dialect thermal for PHYS 432.
```

Preparation introduces the standard Makefile targets and subfiles but retains
the original class commands and problem imports. Subfiles introduce a TeX group:
chapter metadata and inherited section-number formats must be initialized in
each wrapper. Compare the prepared combined PDFs with fresh original builds
before conversion; supplied historical PDFs remain separate references.

The course's `regression.json` uses `baseline_layout: "local-classes"`.
`baseline_revision` pins the course commit containing its compatibility-repaired
classes; `baseline_fixture_revision` pins the prepared course sources. Both
must be full immutable commit hashes before building a reference. The baseline
bundles the two classes under `classes/`, removes shadowing class copies from
its build fixtures, and verifies class resolution and recorder inputs against
the bundle. The original files remain in the source revision and original
archive. Existing shared-class baseline configurations retain their behavior.

```sh
make baseline
python3 ../coursework.tex/scripts/migrate_legacy.py convert . > build/migration.diff
python3 ../coursework.tex/scripts/migrate_legacy.py convert . --write --report build/migration.json
python3 ../coursework.tex/scripts/migrate_legacy.py convert . # zero operations
make candidate
make compare
```

`COURSEWORK_TOOLS` overrides the scripts directory during tooling development;
`candidate_repository` selects experimental classes. Permanent defaults use the
original `coursework.tex` checkout and never alter the installed symlink.

Conversion preserves problem ordering, separates every statement and solution,
and records original text hashes in `migration-content.json`. Imports must be
local, present, and acyclic. Missing or ambiguous structure fails visibly.
The initial inventory is 72 mechanics problems and 193 thermal problems,
including 13 whitespace-empty thermal solutions and one additional solution
containing only a comment. No answers are generated.

Dialect-specific handling includes the notes' two-argument `Sum`, native notes
example/remark syntax, and the homework's optional-index `Sum`. Simple grouped
derivatives use the v2 helpers. Rich `diffcoeff` syntax, including held-variable
arguments, remains explicit. Mechanics dot accents stay in a course-local
package with their original glyphs. Duplicate labels are qualified by assignment
and problem, with local references resolved together; ambiguous references are
rejected. Homework and notes have independent label namespaces.

One known source annotation, the literal `TODO` after mechanics final problem 3's
solution, moves to the end of that problem's statement so it remains present in
all output modes. Other unrecognized trailing narrative requires inspection.

The three mechanics study guides, supplied handouts, and office documents are
archival exclusions. Their bytes and original dependencies are retained in the
original-source archive and recovery ref; they are not active build targets.

After reviewing deliberate v2 differences, freeze an explicit checkpoint:

```sh
COURSEWORK_TEST_ROOT="$PWD" python3 ../coursework.tex/scripts/regression.py checkpoint \
  --name v2-adopted --reason 'Reviewed migration; see the course migration report.'
make compare REFERENCE=v2-adopted
```

The local adoption record and remaining warnings are linked from the final
migration report. No shared TeX runtime modules or installed font defaults change
as part of these two course migrations.
