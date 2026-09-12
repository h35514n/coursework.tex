# Remaining content and layout issues

The current defaults are Pagella prose, Pazo/Palatino homework mathematics,
and Pagella notes mathematics with AMS Euler chapter numerals. All six courses
use the shared classes. No API or font decision remains pending.

Warnings are evidence tied to particular revisions, not a single evergreen
checkpoint. The [homework restoration](HOMEWORK-FONT-RESTORATION.md),
[legacy course adoption](LEGACY-COURSES-ADOPTION.md), and
[notes restoration](NOTES-FONT-RESTORATION.md) record their respective inventories.
The [cleanup record](WORKSPACE-CLEANUP.md) links the current smoke-build logs.
Historical reports and frozen manifests retain their original results.

- **Long equations:** PHYS 331's second assignment recorded a 72.29-point
  overflow in solution 10 with restored Pazo math. PHYS 433's first assignment
  recorded a 14.16-point overflow. Reflow these in dedicated content changes.
- **Mechanics layout:** legacy-course validation recorded content overflows up
  to 60.17 points. These are preserved in that course's warning backlog.
- **Thermal notes:** the Pagella restoration recorded a 35.56-point overflow
  in a long probability-list item and smaller overflows in other chapters.
  Paragraph fitting and classicthesis page-height warnings remain visible.
- **Standalone references:** thermal's Useful mathematics chapter references
  `sec:velocity_distribution`; its Maxwell–Boltzmann chapter references
  `eq:guassian_integral`. They resolve in combined notes but point outside the
  standalone chapter. Keep these warnings visible.
- **Package and bookmark notices:** math-command ownership, mathtools bracket
  configuration, footmisc configuration, and PDF-string notices are recorded
  where emitted. Review bookmark wording separately from printed mathematics.

The latest font validation introduced no missing glyphs, duplicate active labels,
duplicate PDF destinations, or font-substitution warnings. Current smoke checks
report their own results; older warning counts are not claims about edited sources.
