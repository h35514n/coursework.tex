Both classes load `courseenvironments`; you can also load it separately with `\usepackage{courseenvironments}`.
The package loads `coursemath`, `amsthm`, `booktabs`, `float`, and `enumitem`, leaving font selection to the document.

For semantic references in an article, load `hyperref` after the shared package, followed by `cleveref`.

### Counter families

| Family | Counter behavior |
| --- | --- |
| theorem, lemma, corollary, proposition, conjecture, algorithm | One shared counter that resets by section |
| definition, example, remark | Separate counters that reset by section |
| summary | Separate counter that resets by subsection |
| formula | Sequential across the document |
| proof, note, caveat, warning, question, speculation | No numbers |

Use optional titles and standard body labels.
The `proof` environment comes from [amsthm](https://ctan.org/pkg/amsthm).
Table rules come from [booktabs](https://ctan.org/pkg/booktabs).
