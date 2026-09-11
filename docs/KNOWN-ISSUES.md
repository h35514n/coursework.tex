# Remaining content and layout issues

The final migration matrix introduces no warnings relative to the reviewed
font-adoption checkpoint. There are no missing glyphs, duplicate PDF destinations,
or duplicate active labels. These existing issues remain separate follow-up work:

- **Long equations:** PHYS 331 `homework/02-pset/solution10.tex`, line 64,
  still overflows by 61.61 points. Its testbed copy has the same warning.
  Reflow that derivation in a dedicated content-layout change.
- **Paragraph and page fitting:** PHYS 433 has a 14.16-point overflow in its
  first assignment; notes retain smaller overflows and underfull boxes.
  Notes also retain classicthesis page-height warnings. Review these locally
  without changing the global font or spacing defaults.
- **Standalone references:** the thermal testbed's Useful mathematics chapter
  references `sec:velocity_distribution`, and its Maxwell–Boltzmann chapter
  references `eq:guassian_integral`. Both resolve in combined notes; standalone
  builds omit their target chapters. Keep the warnings visible unless external
  chapter-reference support is added deliberately.
- **Package and bookmark notices:** unicode-math reports its math-command and
  mathtools bracket ownership; classicthesis reports its footmisc configuration.
  The thermal notes also retain hyperref PDF-string notices. These are recorded,
  not suppressed. Bookmark wording can be reviewed separately from printed math.

Every occurrence remains in each repository's `checkpoints/v2-final/warnings.json`.
The preserved comparison reports distinguish existing and resolved warnings;
there are no new warning entries. See [FINALIZATION.md](FINALIZATION.md).

The older mechanics and thermal repositories with local classes remain outside
this migration. No additional API or font decisions are pending.
