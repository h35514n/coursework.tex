Load `coursephys` explicitly with `\usepackage{coursephys}` in homework, notes, or an article.
It loads `coursemath`, `graphicx`, and `siunitx`.
It does not select fonts or page layout.

### Units

Use the [siunitx](https://ctan.org/pkg/siunitx) commands that this package supplies:

```latex
\qty{3.5}{\metre\per\second}
\unit{\joule}
```

The package supplies physics vectors and operators, including `\grad` and `\laplacian`.
The standard text accent `\u` is not a unit command.
Both coursework classes configure comma digit groups when `siunitx` loads.
