#!/bin/sh
# Install the coursework LaTeX classes into TEXMFHOME.
#
# Symlinks (does not copy) tex/latex/coursework into
# $TEXMFHOME/tex/latex/coursework, so edits in this repo take effect
# immediately with no reinstall.
#
# TEXMFHOME is searched live by kpathsea -- no mktexlsr needed.
set -eu

repo=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
src="$repo/tex/latex/coursework"
texmfhome=$(kpsewhich -var-value=TEXMFHOME)
dest="$texmfhome/tex/latex/coursework"

[ -d "$src" ] || { echo "error: $src not found" >&2; exit 1; }

mkdir -p "$texmfhome/tex/latex"

if [ -L "$dest" ]; then
	current=$(readlink "$dest")
	if [ "$current" = "$src" ]; then
		echo "already installed: $dest -> $src"
	else
		ln -sfn "$src" "$dest"
		echo "relinked: $dest -> $src (was $current)"
	fi
elif [ -e "$dest" ]; then
	echo "error: $dest exists and is not a symlink; move it aside first" >&2
	exit 1
else
	ln -s "$src" "$dest"
	echo "installed: $dest -> $src"
fi

echo
echo "Verifying kpathsea can resolve the package:"
for f in coursenotes.cls coursepsets.cls coursemath.sty coursephys.sty; do
	printf '  %-18s %s\n' "$f" "$(kpsewhich "$f" || echo 'NOT FOUND')"
done
for f in coursework-scriptr.pdf coursework-boldr.pdf; do
	printf '  %-18s %s\n' "$f" \
		"$(kpsewhich -progname=xelatex -format='graphic/figure' "$f" || echo 'NOT FOUND')"
done
