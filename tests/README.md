# Validation

`python3 -m unittest discover -s tests -v` tests source migration behavior.
`python3 tests/run_api.py` compiles the semantic TeX matrix and records its
results in `build/api/report.json`. No inputs outside `build/api` are changed.
Page-boundary cases verify independent assignment, section, and problem break
settings, including a fully flowing worked build overriding worksheet defaults.
The cases include deliberately invalid documents; success means these fail
with the expected diagnostic. Successful cases must have correct labels,
expected visible content, no hidden file inputs, no duplicate PDF destinations,
and no undefined references or missing glyphs.

`tests/notation.tex` exercises all retained and newly named notation and can
be included in either class or in an article loading the shared packages.
The real-course regression driver is `scripts/regression.py`; set
`COURSEWORK_TEST_ROOT` to the course root when invoking it directly.

`python3 tests/check_notes_font.py` checks the notes default against an explicit
Pagella selection, verifies the font families found in the saved thermal PDF,
and checks mixed-case contents lettering with chapter and local contents.
`python3 tests/check_homework_font.py` verifies the restored Pazo homework glyphs
against the original API checkpoint at 300 dpi.

`tests/test_legacy_migration.py` covers the two self-contained course dialects,
embedded/imported solution extraction, label disambiguation, archival exclusions,
and relocated local-class snapshots. These snapshot tests run from this repository. The additional harness tests
reported during the original migration belonged to the former testbed, which
is no longer present; do not count them as part of the current local test suite.
