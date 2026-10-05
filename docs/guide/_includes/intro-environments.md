Both classes load `courseenvironments`.
You can also load it explicitly with `\usepackage{courseenvironments}`.
It loads `coursemath`, `amsthm`, `booktabs`, `float`, and `enumitem`.
It does not select fonts.

For semantic references in an article, load `hyperref` after the shared package.
Then load `cleveref`.

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
