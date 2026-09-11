# Coursework v2 adoption

The user approved the v2 API and coordinated course adoption, then selected
Pagella prose throughout, Pagella mathematics in homework, and Euler mathematics
in notes. Font configuration is centralized in `coursefonts.sty`; the defaults
require no course-specific font setup.

## Recovery and activation

The local `master` branches of `coursework.tex`, PHYS 331, 433, 440, and 491
have adopted the validated API migration. Each repository has an
`archive/coursework-v1` recovery branch at its original revision. The class
repository also preserves the approved API with its original typography as
`archive/coursework-v2-api`.

The installed symlink stays at `~/Library/texmf/tex/latex/coursework` and points
to the original `coursework.tex/tex/latex/coursework` checkout. Activation is
performed by advancing that checkout, without redirecting the symlink to a
development worktree. Nothing is pushed to a remote. Older mechanics and
thermal repositories with local classes remain outside this adoption.

## Validation

All four original course checkouts built their first assignment using the
installed v2 classes without a `TEXINPUTS` override. Recorder files confirmed
the installed checkout supplied every coursework module.

The approved font integration is undergoing the full 170-output matrix and
the behavioral API suite before activation. The original v1 baselines and
reviewed `v2-api` checkpoints remain immutable; font differences are compared
against `v2-api` separately.

Full-course font validation identified two remaining legacy integration cases.
PHYS 331 and its testbed replace two `\bigintssss` uses with standard integrals.
The shared bold helper now enters math mode when used in prose and preserves
boldness inside explicit upright/italic alphabets. Three additional behavioral
cases verify those properties under both classes and standalone legacy math.
