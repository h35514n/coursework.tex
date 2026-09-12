Load explicitly with `\usepackage{coursephys}` in homework, notes, or an article. It loads `coursemath`, `graphicx`, and `siunitx`, but does not select fonts or page layout.

### Units

Use the [siunitx](https://ctan.org/pkg/siunitx) commands supplied by this package:

```latex
\qty{3.5}{\metre\per\second}
\unit{\joule}
```

Physics vectors and operators belong to this package, including `\grad` and `\laplacian`. The standard text accent `\u` is not a unit shortcut. Both coursework classes configure comma digit grouping when siunitx loads.
