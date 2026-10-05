# Maintain the guide

The [public guide](https://h35514n.github.io/coursework.tex/) describes the current v2 API.
Its source files are in this directory.
The [documentation index](../README.md) links current workflows, historical reports, and evidence manifests.

## Local build

Use these tools for a complete build:

| Tool | Requirement |
| --- | --- |
| TeX Live | 2026 with the June 2026 LaTeX kernel or newer |
| TeX tools | `latexmk` and XeLaTeX |
| PDF tools | Poppler (`pdftoppm`, `pdftotext`), Ghostscript, and `pdfcrop` |
| Python | 3.10 or newer |
| Ruby | 4.0.5 |
| Bundler | 4.0.12 |

`Gemfile.lock` fixes the Ruby gem versions and their dependencies.
From the repository root, install gems into the ignored build directory:

```sh
BUNDLE_GEMFILE=docs/guide/Gemfile BUNDLE_PATH="$PWD/build/docs/gems" bundle install
```

Build the complete guide:

```sh
python3 scripts/build_docs.py
```

The build verifies API coverage.
It compiles examples with scoped `TEXINPUTS` and renders their pages.
It creates source downloads and reference pages.
It builds Jekyll and verifies local links, anchors, assets, and search entries.
All generated files remain in `build/docs`.
The build does not run the installer or change TeX sources.

The build inspects the final LaTeX log after `latexmk` completes reference passes.
Missing glyphs, undefined references, duplicate destinations, and package or glyph paths outside the checkout cause failures.
Empty PDFs and unexpected hidden solution inputs also cause failures.

For page text or style changes, run `python3 scripts/build_docs.py --site-only`.
This option reuses compiled examples only if their source fingerprint matches.
Changes to the build script, example sources, example catalog, or class assets require a full build.
To inspect coverage without TeX or Ruby, run `python3 scripts/build_docs.py --check`.

Serve the site at its project base path:

```sh
mkdir -p build/docs/preview
ln -sfn ../site build/docs/preview/coursework.tex
python3 -m http.server 8000 --directory build/docs/preview
```

Open [the local guide](http://localhost:8000/coursework.tex/).
Inspect desktop navigation.
Inspect mobile navigation.
Search for `integral` and `\integral`.
Use a copy button.
Inspect page previews.
Download a PDF and a source ZIP.

## Reference entries and snippets

`api.json` is the public reference catalog.
Each entry records its package, kind, signature, arguments, behavior, and example ID.
The build generates reference groups and the command index.
Edit the catalog instead of generated Markdown.

The `examples` directory contains the TeX projects.
Mark reusable code with `% example:unique-id` and `% endexample`.
The build copies those exact lines into code blocks.
Each linked example must use its entry's command or environment.
Reference chapters use the same sources in both coursework classes and `article`.
`examples.json` selects root files and output variants.

When you add a public definition, update the catalog.
Add a source example for the definition.
The coverage checker recognizes xparse commands and environments, newcommand, paired delimiters, and theorem families.
For a new declaration form, update the coverage checker.
Keep internal exclusions explicit with a reason.
The imported `proof` is a dependency environment.
The catalog does not inventory all third-party commands.
Configuration tables are in `_includes/intro-*.md`.

Class and font pages have separate authored sources.
The build extracts the migration table from `../MIGRATION.md`.
Preserve its `Complete command map` and `Environment and structure changes` headings.
The build uses raw Liquid blocks to preserve literal TeX.

## Writing policy

Apply the writing rules in [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) to public explanatory prose and instructions.
This project applies writing rules only.
It does not claim a complete dictionary audit or full ASD-STE100 conformance.

The policy covers authored pages, includes, catalog descriptions, and argument explanations.
It also covers example titles, navigation labels, alternative text, footers, generated pages, and source-download instructions.
Apply the same rules to new maintenance instructions.

Preserve executable TeX, shell commands, signatures, identifiers, file paths, mathematical notation, and specimen content.
Historical report bodies retain their original language and checkpoint facts.
Update their links and historical notices when necessary.

Use consistent technical terms:

| Term | Meaning |
| --- | --- |
| Project root | Directory from which the example's compile command runs |
| Fragment | Content file for a problem, solution, guide, or discussion |
| Role | Statement, solution, guide, or discussion within an assignment |
| Math mode | LaTeX mathematics context |
| Font profile | Class option that selects the mathematics backend |
| Checkpoint | Immutable source and output record used for comparison |

### Review checklist

- Limit procedural sentences to 20 words and descriptive sentences to 25 words.
- Count words with the standard's rules for technical names, identifiers, parentheses, and vertical lists.
- Give one instruction in each procedural sentence.
- Use the imperative for instructions.
- Use active voice. In descriptions, use passive voice only if the actor is unknown.
- Put a condition first if the reader must know it before the action.
- Use permitted simple verb forms. Avoid perfect tenses and verb forms that end in `-ing`.
- Limit noun groups to three words unless a defined technical name requires more words.
- Use one technical term for each meaning.
- Use complete sentences in prose. Retain articles and other necessary words.
- Start each descriptive paragraph with its topic. Keep each paragraph to one topic and six sentences or fewer.
- Use separate sentences instead of semicolons.
- Remove idioms, metaphors, ambiguous pronouns, and unnecessary words.
- Preserve each command's requirements, defaults, errors, and effects.
- Review generated HTML and source-download instructions as well as authored Markdown.

Code and signature punctuation do not follow prose punctuation rules.
Table headings, labels, and argument names can be fragments.
Use complete sentences for explanations in table cells.
Sentence counts and word scans assist the review.
They do not establish meaning, grammar, or full STE conformance.

## Publication

The Documentation workflow validates relevant pull requests and retains a site artifact for review.
On `master`, it builds and publishes the generated site through GitHub Pages.
Set the Pages build source to GitHub Actions.
The workflow also permits manual dispatch.

The example job uses a digest-pinned TeX Live 2026 Debian container built July 1, 2026.
Update that pin deliberately.
After a TeX update, review the resulting PDFs.

CI retains example PDFs, source projects, console logs, and validation reports for seven days.
A failed example or site job prevents deployment.
The previous published version remains available.
The footer identifies the source commit.
To roll back the documentation, revert the relevant commit.
The next `master` workflow deploys the reverted version.

After publication, inspect the home page and a reference anchor.
Search with and without a backslash.
Download a source ZIP.
Download a PDF.
Inspect mobile navigation.
