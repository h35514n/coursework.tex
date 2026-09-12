#!/usr/bin/env python3
"""Check the saved-notes font families, contents lettering, and default profile."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/notes-font-check'
CLASSES = ROOT / 'tex/latex/coursework'


def run(args):
    return subprocess.check_output(args, text=True, cwd=ROOT)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    results = {}
    for name, options in [('default', ''), ('explicit', '[font-profile=pagella]')]:
        folder = OUT / name
        folder.mkdir(parents=True, exist_ok=True)
        source = folder / 'specimen.tex'
        source.write_text('\\documentclass' + options + '{coursenotes}\n'
                          '\\usepackage{coursephys}\n\\begin{document}\n'
                          '\\input{tests/notes_appearance.tex}\n\\end{document}\n')
        env = {**os.environ, 'TEXINPUTS': str(CLASSES) + '//:',
               'SOURCE_DATE_EPOCH': '1789087534', 'FORCE_SOURCE_DATE': '1'}
        proc = subprocess.run(['latexmk', '-xelatex', '-halt-on-error',
                               '-interaction=nonstopmode', '-recorder',
                               '-outdir=' + str(folder), str(source)],
                              cwd=ROOT, env=env, text=True, capture_output=True)
        (folder / 'console.log').write_text(proc.stdout + proc.stderr)
        assert proc.returncode == 0, f'See {folder}/console.log'
        log = (folder / 'specimen.log').read_text()
        for bad in ['Missing character:', 'multiply defined', 'already defined.',
                    'undefined references', 'LaTeX Font Warning:']:
            assert bad not in log, (name, bad)
        assert 'already defined.' not in proc.stdout + proc.stderr, 'Duplicate PDF destination'
        fls = (folder / 'specimen.fls').read_text()
        for line in fls.splitlines():
            if line.startswith('INPUT ') and Path(line[6:]).name.startswith('course'):
                assert Path(line[6:]).resolve().parent == CLASSES, line
        pdf = folder / 'specimen.pdf'
        fonts = run(['pdffonts', str(pdf)])
        (folder / 'fonts.txt').write_text(fonts)
        for font in ['TeXGyrePagella-Regular', 'TeXGyrePagellaMath-Regular', 'EURB10']:
            assert font in fonts, f'Missing historical font: {font}'
        assert 'Euler-Math' not in fonts and 'PazoMath' not in fonts, fonts
        toc = run(['pdftotext', '-f', '1', '-l', '1', '-layout', str(pdf), '-'])
        assert 'Mixed Case Chapter' in toc, f'Contents lettering changed: {toc}'
        run(['pdftoppm', '-r', '160', '-png', str(pdf), str(folder / 'page')])
        results[name] = {'pdf_sha256': sha(pdf), 'fonts': fonts,
                         'renders': {p.name: sha(p) for p in sorted(folder.glob('page-*.png'))}}
    assert results['default']['renders'] == results['explicit']['renders'], \
        'Default notes differ from explicit Pagella profile'
    (OUT / 'manifest.json').write_text(json.dumps(results, indent=2) + '\n')
    print('PASS: notes use saved-PDF font families and mixed-case contents; '
          'default and explicit Pagella renders match.')


if __name__ == '__main__':
    main()
