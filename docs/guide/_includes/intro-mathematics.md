Both classes load `coursemath` for shared notation.
You can also load it separately with `\usepackage{coursemath}` without changing the document's layout or fonts.
Standard text accents such as `\L` and `\u` retain their meanings.

The `unicode` option skips legacy symbol and bold packages.
The coursework classes select it automatically for Pagella and Euler profiles.
In a Unicode article, load `coursemath` with `[unicode]` before `unicode-math`; otherwise, use the default legacy backend.

Some commands do not insert `\ensuremath` and therefore require math mode, as noted in their reference entries.

The package uses [mathtools](https://ctan.org/pkg/mathtools), [diffcoeff](https://ctan.org/pkg/diffcoeff), and either [bm](https://ctan.org/pkg/bm) or [unicode-math](https://ctan.org/pkg/unicode-math).
