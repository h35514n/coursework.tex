Both classes load `coursemath`.
You can also load it explicitly with `\usepackage{coursemath}`.
It supplies notation.
It does not select page layout or fonts.
Standard text accents such as `\L` and `\u` retain their meanings.

With the `unicode` option, the package does not load legacy symbol or bold packages.
The coursework classes select it automatically for Pagella and Euler profiles.
For a Unicode article, load `coursemath` with `[unicode]` before `unicode-math`.
For other articles, use the default legacy backend.

Individual entries identify commands that require math mode.
Some commands do not insert `\ensuremath`.

The package uses [mathtools](https://ctan.org/pkg/mathtools), [diffcoeff](https://ctan.org/pkg/diffcoeff), and either [bm](https://ctan.org/pkg/bm) or [unicode-math](https://ctan.org/pkg/unicode-math).
