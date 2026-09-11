#!/usr/bin/env python3
"""Compare homework glyphs to the retained pre-font v2 API revision."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/homework-font-restoration'
REFERENCE = 'archive/coursework-v2-api'


def run(args, **kwargs):
    return subprocess.check_output(args, text=True, cwd=ROOT, **kwargs)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    revision = run(['git', 'rev-parse', REFERENCE]).strip()
    archive = subprocess.check_output(['git', 'archive', revision, 'tex/latex/coursework'], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        bundle.extractall(OUT / 'reference', filter='data')
    old_classes = OUT / 'reference/tex/latex/coursework'
    # The old display-name lookup depends on the host's font cache. Resolve
    # the same prose/mono faces by filename in this scratch copy only. Leave
    # mathpazo, mathspec, and their loading order exactly as recorded.
    cls = old_classes / 'coursepsets.cls'
    cls.write_text(cls.read_text().replace(
        r'\setmainfont[Ligatures=TeX,Numbers=OldStyle]{TeX Gyre Pagella}',
        r'\setmainfont{texgyrepagella}[Extension=.otf,UprightFont=*-regular,ItalicFont=*-italic,BoldFont=*-bold,BoldItalicFont=*-bolditalic,Ligatures=TeX,Numbers=OldStyle]'
    ).replace(
        r'\setmonofont[Scale=0.85]{DejaVu Sans Mono}',
        r'\setmonofont{DejaVuSansMono}[Extension=.ttf,BoldFont=*-Bold,ItalicFont=*-Oblique,BoldItalicFont=*-BoldOblique,Scale=0.85]'))
    source = OUT / 'specimen.tex'
    source.write_text(r'''\documentclass{coursepsets}
\usepackage{coursephys}
\begin{document}
\input{tests/font_glyphs.tex}
\end{document}
''')
    results = {}
    for name, classes in [('old', old_classes), ('restored', ROOT / 'tex/latex/coursework')]:
        folder = OUT / name
        folder.mkdir(exist_ok=True)
        env = {**os.environ, 'TEXINPUTS': str(classes) + '//:',
               'SOURCE_DATE_EPOCH': '1789087534', 'FORCE_SOURCE_DATE': '1'}
        args = ['latexmk', '-xelatex', '-halt-on-error', '-interaction=nonstopmode',
                '-recorder', '-outdir=' + str(folder), str(source)]
        proc = subprocess.run(args, text=True, capture_output=True, cwd=ROOT, env=env)
        (folder / 'console.log').write_text(proc.stdout + proc.stderr)
        assert proc.returncode == 0, f'{name}: see {folder}/console.log'
        log = (folder / 'specimen.log').read_text()
        assert 'Missing character:' not in log, f'{name}: missing glyph'
        pdf = folder / 'specimen.pdf'
        assert 'Pages:           1' in run(['pdfinfo', str(pdf)]), 'Expected one specimen page'
        run(['pdftoppm', '-r', '300', '-png', '-singlefile', str(pdf), str(folder / 'glyphs')])
        fonts = run(['pdffonts', str(pdf)])
        (folder / 'fonts.txt').write_text(fonts)
        assert 'PazoMath' in fonts and 'TeXGyrePagellaMath' not in fonts, 'Wrong homework math font'
        results[name] = {'pdf': str(pdf), 'pdf_sha256': sha(pdf),
                         'render_sha256': sha(folder / 'glyphs.png'), 'fonts': fonts,
                         'class_files': {p.name: sha(p) for p in classes.iterdir() if p.is_file()}}
    assert results['old']['render_sha256'] == results['restored']['render_sha256'], \
        'Homework glyphs differ from the original-font API checkpoint'
    manifest = {'reference_revision': revision,
                'candidate_revision': run(['git', 'rev-parse', 'HEAD']).strip(),
                'candidate_status': run(['git', 'status', '--short']).strip(),
                'compatibility_adjustment': 'Resolve identical prose and mono faces by filename in scratch reference only',
                'fixture_sha256': sha(ROOT / 'tests/font_glyphs.tex'),
                'dpi': 300, 'matching_pixels': True, 'results': results}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('PASS: restored homework glyphs match the pre-font API pixel-for-pixel at 300 dpi.')


if __name__ == '__main__':
    main()
