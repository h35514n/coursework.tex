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
verify_file() {
	f=$1
	shift
	resolved=$(kpsewhich -progname=xelatex "$@" "$f") || {
		echo "error: $f cannot be resolved" >&2
		exit 1
	}
	[ "$resolved" -ef "$src/$f" ] || {
		echo "error: $f resolves to $resolved instead of $src/$f" >&2
		exit 1
	}
	printf '  %-24s %s\n' "$f" "$resolved"
}
for f in coursenotes.cls coursepsets.cls coursecommon.sty courseassignments.sty \
         courseenvironments.sty coursemath.sty coursephys.sty coursefonts.sty; do
	verify_file "$f"
done
for f in coursework-scriptr.pdf coursework-boldr.pdf; do
	verify_file "$f" -format='graphic/figure'
done
