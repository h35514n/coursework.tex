# Validation

`python3 -m unittest discover -s tests -v` tests source migration behavior.
`python3 tests/run_api.py` compiles the semantic TeX matrix and records its
results in `build/api/report.json`. No inputs outside `build/api` are changed.
The cases include deliberately invalid documents; success means these fail
with the expected diagnostic. Successful cases must have correct labels,
expected visible content, no hidden file inputs, no duplicate PDF destinations,
and no undefined references or missing glyphs.

`tests/notation.tex` exercises all retained and newly named notation and can
be included in either class or in an article loading the shared packages.
The real-course regression driver is `scripts/regression.py`; set
`COURSEWORK_TEST_ROOT` to the course root when invoking it directly.
