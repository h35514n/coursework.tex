# Maintaining the guide

The public site is https://h35514n.github.io/coursework.tex/. It documents the
current v2 API. Website sources live here; historical reports in the parent
`docs` directory remain ordinary repository documents.

## Local build

Requirements: TeX Live 2026 with the June kernel or newer, `latexmk`, XeLaTeX,
Poppler (`pdftoppm` and `pdftotext`), Ghostscript and `pdfcrop`, Python 3.10+, Ruby 4.0.5, and Bundler 4.0.12.
The Ruby gem versions and transitive dependencies are locked in `Gemfile.lock`.

From the repository root, install dependencies into the ignored build directory:

```sh
BUNDLE_GEMFILE=docs/guide/Gemfile BUNDLE_PATH="$PWD/build/docs/gems" bundle install
```

Then build everything with one command:

```sh
python3 scripts/build_docs.py
```

This checks API coverage, compiles the actual examples with scoped `TEXINPUTS`,
renders all pages, creates downloads and reference pages, builds Jekyll, and
checks local links, anchors, assets, and the generated search index. All derived
files stay in `build/docs`; it never runs `install.sh` or changes TeX sources.
It checks the final LaTeX log after `latexmk` completes its reference passes.
The build rejects missing glyphs, undefined references, duplicate destinations,
and package/glyph lookups outside the checkout. Empty PDFs and unexpected hidden
solution inputs also fail the build.

For prose/style-only edits, `python3 scripts/build_docs.py --site-only` reuses
compiled examples after checking their source fingerprint. To inspect coverage
without TeX or Ruby, run `python3 scripts/build_docs.py --check`.

Serve at the actual project base path:

```sh
mkdir -p build/docs/preview
ln -sfn ../site build/docs/preview/coursework.tex
python3 -m http.server 8000 --directory build/docs/preview
```

Open http://localhost:8000/coursework.tex/. Check desktop and mobile navigation,
searches such as `integral` and `\integral`, copy buttons, and readable previews.

## Reference entries and snippets

`api.json` is the author-maintained public reference catalog. Each entry names
its owning package, command/environment kind, complete signature, arguments,
behavior, and a runnable snippet ID. The build generates grouped reference pages
and the alphabetical index; do not edit generated Markdown.

`examples` contains the real TeX projects. Mark reusable bodies with
`% example:unique-id` and `% endexample`. The build extracts those exact lines for
code blocks. Each entry's linked snippet must actually invoke that entry.
Reference chapters use the same sources in both coursework classes and article.
`examples.json` selects roots and mode variants for compilation and downloads.

When adding a public definition, update the catalog and add its source example.
The coverage checker recognizes the definition forms currently used by the
packages (xparse commands/environments, newcommand, paired delimiters, and theorem
families). Update the checker if a new declaration form is introduced. Keep
implementation-helper exclusions explicit with a reason. Imported `proof` is
listed as a dependency environment; the guide does not inventory all third-party
package commands. Configuration key tables live in `_includes/intro-*.md`.

Class and font pages are authored separately. The migration table is extracted
from the existing migration document. Both templates and signatures preserve
literal TeX when Liquid would otherwise interpret adjacent braces.

## Publication

The Documentation workflow validates relevant pull requests and retains a site
artifact for review. On `master`, it builds and publishes only the generated site
through GitHub Pages, which must have its build source set to GitHub Actions.
The workflow also supports manual dispatch. The example job uses a digest-pinned
TeX Live 2026 Debian container built July 1, 2026. Update that pin deliberately
and review the resulting PDFs when updating TeX.

CI stores example PDFs, source projects, console logs, and the validation report
as a seven-day artifact. A failed example/site job prevents deployment and leaves
the previous published version available. The footer identifies the source commit.
To roll back documentation, revert the relevant commit and let `master` redeploy.

The first publication should be checked live: home page, one reference anchor,
search with and without a backslash, a source ZIP, a PDF, and mobile navigation.
