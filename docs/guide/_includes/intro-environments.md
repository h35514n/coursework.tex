Loaded by both classes, or explicitly with `\usepackage{courseenvironments}`. It loads `coursemath`, `amsthm`, `booktabs`, `float`, and `enumitem` without selecting fonts. With an ordinary article, load `hyperref` and then `cleveref` after the shared package when you want semantic references.

### Counter families

| Family | Counter behavior |
| --- | --- |
| theorem, lemma, corollary, proposition, conjecture, algorithm | One shared counter; reset by section |
| definition, example, remark | Separate counters; each reset by section |
| summary | Separate counter; reset by subsection |
| formula | Sequential across the document |
| proof, note, caveat, warning, question, speculation | Unnumbered |

Use optional titles and ordinary body labels. `proof` comes from [amsthm](https://ctan.org/pkg/amsthm); table rules come from [booktabs](https://ctan.org/pkg/booktabs).
