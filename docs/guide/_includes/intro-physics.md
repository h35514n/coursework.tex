Load `coursephys` with `\usepackage{coursephys}` in homework, notes, or an article to use physics notation.
It loads `coursemath`, `graphicx`, and `siunitx`, leaving fonts and page layout to the document.

### Units

Use the [siunitx](https://ctan.org/pkg/siunitx) commands that this package supplies:

```latex
\qty{3.5}{\metre\per\second}
\unit{\joule}
```

The package provides physics vectors and operators, including `\grad` and `\laplacian`.
Use `\unit` for units; `\u` retains its standard text-accent meaning.
Both coursework classes configure comma digit groups when `siunitx` loads.
