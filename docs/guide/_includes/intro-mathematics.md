Loaded by both classes, or explicitly with `\usepackage{coursemath}`. This package supplies notation without setting page layout or fonts. Standard text accents such as `\L` and `\u` remain intact.

The `unicode` package option avoids legacy symbol/bold packages when the document will supply `unicode-math`. The coursework classes select this automatically for Pagella and Euler profiles. In a plain article using Unicode math, load `coursemath` with `[unicode]` before `unicode-math`; otherwise the default legacy backend is suitable.

Individual entries specify whether math mode is required. The wrappers do not all insert `\ensuremath`.

Notation uses [mathtools](https://ctan.org/pkg/mathtools), [diffcoeff](https://ctan.org/pkg/diffcoeff), and either [bm](https://ctan.org/pkg/bm) or [unicode-math](https://ctan.org/pkg/unicode-math).
