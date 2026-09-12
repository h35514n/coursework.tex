#!/usr/bin/env python3
"""Compile the guide's real TeX sources, build Jekyll, and validate the output.

Run from any directory: python3 scripts/build_docs.py
All derived files (including staged Markdown) are confined to build/docs.
"""
from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'docs/guide'
CLASSES = ROOT / 'tex/latex/coursework'
BUILD = ROOT / 'build/docs'
STAGE = BUILD / 'source'
SITE = BUILD / 'site'
BASE = '/coursework.tex'
REPO = 'https://github.com/h35514n/coursework.tex'
GROUPS = {'configuration': 'Configuration', 'assignments': 'Assignments',
          'environments': 'Environments', 'mathematics': 'Mathematics', 'physics': 'Physics'}


def run(args, *, cwd=ROOT, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(map(str, args))}\n{result.stdout[-4000:]}\n{result.stderr[-4000:]}")
    return result.stdout


def read_json(path):
    return json.loads(path.read_text())


def snippets():
    found = {}
    for file in sorted((GUIDE / 'examples').rglob('*.tex')):
        for match in re.finditer(r'^% example:([\w-]+)\n(.*?)^% endexample\s*$', file.read_text(), re.M | re.S):
            key, body = match.groups()
            if key in found:
                raise ValueError(f'Duplicate snippet: {key}')
            found[key] = body.rstrip()
    return found


def inventory():
    """Recognize this repository's public definition forms, not arbitrary TeX."""
    found = {}
    patterns = [
        (r'\\(?:New|Renew)(?:Expandable)?DocumentCommand\s*\{?\\([A-Za-z]+)(?![A-Za-z@_:])', 'command'),
        (r'\\(?:newcommand|DeclarePairedDelimiter)\s*\{?\\([A-Za-z]+)(?![A-Za-z@_:])', 'command'),
        (r'\\(?:newenvironment|NewDocumentEnvironment|newtheorem\*?)\s*\{([A-Za-z]+)\}', 'environment'),
    ]
    for file in sorted(CLASSES.glob('*.sty')):
        source = re.sub(r'(?<!\\)%[^\n]*', '', file.read_text())
        for pattern, kind in patterns:
            for match in re.finditer(pattern, source):
                found[match.group(1)] = (file.stem, kind)
    # These non-xparse definitions are intentionally internal but must remain accounted for.
    for name in ['courseassignmentfooter', 'courseproblemfooter']:
        if re.search(r'\\cs_new:Npn\s*\\' + name + r'\b', (CLASSES/'courseassignments.sty').read_text()):
            found[name] = ('courseassignments', 'command')
    return found


def check_catalog():
    catalog = read_json(GUIDE/'api.json')
    examples = snippets()
    declared = inventory()
    documented = {entry['name']: entry for entry in catalog['entries']}
    if len(documented) != len(catalog['entries']):
        raise ValueError('Duplicate public API entry')
    expected = set(declared) - set(catalog['internal'])
    actual = {name for name, entry in documented.items() if not entry['kind'].startswith('dependency-')}
    if actual != expected:
        raise ValueError(f'API coverage mismatch. Undocumented: {expected-actual}; stale: {actual-expected}')
    if set(catalog['internal']) - set(declared):
        raise ValueError('Stale internal API exclusions')
    for name, entry in documented.items():
        for field in ['signature', 'description', 'arguments', 'module', 'example', 'group']:
            if not entry.get(field):
                raise ValueError(f'{name}: missing {field}')
        if name in declared and declared[name] != (entry['module'], entry['kind']):
            raise ValueError(f'{name}: wrong module or kind')
        if entry['example'] not in examples:
            raise ValueError(f'{name}: no runnable snippet')
        # Every public entry's example must actually exercise that entry.
        if not re.search(r'\\' + re.escape(name) + r'\b|\\begin\{' + re.escape(name) + r'\}', examples[entry['example']]):
            raise ValueError(f'{name}: linked example does not use this API')
    print(f'API coverage: {len(expected)} public definitions plus dependency proof environment', flush=True)
    return catalog, examples


def fingerprint():
    digest = hashlib.sha256()
    for file in sorted([*CLASSES.iterdir(), *(GUIDE/'examples').rglob('*'), GUIDE/'examples.json', Path(__file__)]):
        if file.is_file():
            digest.update(str(file.relative_to(ROOT)).encode())
            digest.update(file.read_bytes())
    return digest.hexdigest()


def compile_examples():
    items = read_json(GUIDE/'examples.json')
    out = BUILD/'examples'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    env = {**os.environ, 'TEXINPUTS': str(CLASSES)+'//:',
           'SOURCE_DATE_EPOCH': '1789087534', 'FORCE_SOURCE_DATE': '1'}
    results = []
    for item in items:
        folder = out/item['id']
        if item.get('files'):
            folder.mkdir()
            for name in item['files']:
                shutil.copy2(GUIDE/'examples'/item['project']/name, folder/name)
        else:
            shutil.copytree(GUIDE/'examples'/item['project'], folder)
        source = folder/item['root']
        if item.get('mode'):
            source.write_text(source.read_text().replace('mode=worked', 'mode='+item['mode'], 1))
        # Downloadable files are exactly those used for this variant.
        text = ('# '+item['title']+'\n\nRequires TeX Live 2026 (LaTeX kernel 2026-06-01 or newer), XeLaTeX,\n'
                'and coursework v2. Install coursework from '+REPO+' following its guide.\n\n'
                'Compile from this directory, even for chapter/assignment subfiles:\n\n'
                '```sh\nlatexmk -xelatex -halt-on-error '+item['root']+'\n```\n\n'
                'For an uninstalled checkout, prefix that command with\n'
                '`TEXINPUTS="/absolute/path/to/coursework.tex/tex/latex/coursework//:"`.\n')
        (folder/'README.md').write_text(text)
        pdfdir = folder/'output'
        pdfdir.mkdir()
        args = ['latexmk', '-xelatex', '-halt-on-error', '-interaction=nonstopmode', '-file-line-error',
                '-recorder', '-outdir=output', item['root']]
        proc = subprocess.run(args, cwd=folder, env=env, text=True, capture_output=True)
        (pdfdir/'console.log').write_text(proc.stdout+proc.stderr)
        stem = source.stem
        if proc.returncode:
            raise RuntimeError(f"{item['id']} failed: {pdfdir/'console.log'}\n{proc.stdout[-2500:]}")
        log = (pdfdir/(stem+'.log')).read_text(errors='replace')
        if not re.search(r'LaTeX2e <2026-(?:0[6-9]|1[0-2])-\d\d>|LaTeX2e <202[7-9]-', log):
            raise RuntimeError('Examples require the June 2026 LaTeX kernel or newer')
        for bad in ['Missing character:', 'undefined references', 'multiply defined', 'destination with the same identifier',
                    'already defined.', 'cref reference format', 'Invalid end-point', 'Overfull \\hbox']:
            if bad in log:
                raise RuntimeError(f"{item['id']}: {bad}")
        if re.search(r'pdf:warning.*already defined|destination.*same identifier', proc.stderr, re.I):
            raise RuntimeError(f"{item['id']}: duplicate PDF destination")
        aux = (pdfdir/(stem+'.aux')).read_text()
        if item['project'] == 'homework':
            for name, number in [('prob:motion:02', '1.1'), ('prob:motion:01', '1.2')]:
                if '\\newlabel{'+name+'}{{'+number+'}' not in aux:
                    raise RuntimeError('Incorrect selected-problem reference: '+name)
        fls = (pdfdir/(stem+'.fls')).read_text()
        for line in fls.splitlines():
            if not line.startswith('INPUT '):
                continue
            path = Path(line[6:])
            if path.name.startswith('course') and path.suffix in {'.cls', '.sty', '.pdf'}:
                resolved = path if path.is_absolute() else folder/path
                if resolved.resolve().parent != CLASSES:
                    raise RuntimeError(f'Installed package or glyph fallback: {line}')
        if item.get('mode') in {'compact', 'worksheet'} and re.search(r'INPUT .*fragments/(solution|discussion)', fls):
            raise RuntimeError('Hidden solution/discussion input was read')
        pdf = pdfdir/(stem+'.pdf')
        pdftext = run(['pdftotext', str(pdf), '-'])
        if not pdftext.strip():
            raise RuntimeError('Empty example PDF')
        run(['pdftoppm', '-scale-to', '1400', '-png', str(pdf), str(pdfdir/'page')])
        if item['id'].startswith('font-'):
            run(['pdfcrop', '--margins', '12', str(pdf), str(pdfdir/'preview.pdf')])
            run(['pdftoppm', '-scale-to', '1400', '-singlefile', '-png', str(pdfdir/'preview.pdf'), str(pdfdir/'preview')])
        pages = sorted(pdfdir.glob('page-*.png'), key=lambda p: int(p.stem.split('-')[-1]))
        if not pages:
            raise RuntimeError('No rendered preview pages')
        results.append({**item, 'pages': len(pages), 'warnings': [s for s in log.splitlines() if 'Warning:' in s]})
        print(f"Compiled {item['id']}: {len(pages)} pages", flush=True)
    report = {'fingerprint': fingerprint(), 'xelatex': run(['xelatex','--version']).splitlines()[0], 'examples': results}
    (BUILD/'examples-report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def fence(code, language='latex'):
    return '{% raw %}\n```'+language+'\n'+code+'\n```\n{% endraw %}\n'


def page(title, body, order=0, parent=None, permalink=None):
    fields = {'title': title, 'layout': 'default', 'nav_order': order}
    if parent:
        fields['parent'] = parent
    if permalink:
        fields['permalink'] = permalink
    return '---\n'+'\n'.join(k+': '+json.dumps(v) for k,v in fields.items())+'\n---\n\n'+body+'\n'


def link(path):
    return "{{ '"+path+"' | relative_url }}"


def build_source(catalog, snippets_by_id, report):
    if report['fingerprint'] != fingerprint():
        raise RuntimeError('Compiled examples are stale. Run the full build first.')
    if STAGE.exists():
        shutil.rmtree(STAGE)
    shutil.copytree(GUIDE, STAGE, ignore=shutil.ignore_patterns('examples', 'Gemfile*', 'api.json', 'examples.json', 'CONTRIBUTING.md'))
    revision = run(['git','rev-parse','HEAD']).strip()
    (STAGE/'_includes/footer_custom.html').write_text('<p class="text-small text-grey-dk-000">Built from <a href="'+REPO+'/tree/'+revision+'">'+revision[:7]+'</a>. Examples use '+html.escape(report['xelatex'])+'.</p>\n')
    inc = STAGE/'_includes/snippets'
    inc.mkdir(parents=True)
    for key, code in snippets_by_id.items():
        (inc/(key+'.md')).write_text(fence(code))
    reference = STAGE/'reference'
    reference.mkdir(exist_ok=True)
    index = ['# Command and environment index\n', 'Search accepts command names with or without a leading backslash.\n', '| Name | Kind | Provided by |', '| --- | --- | --- |']
    for entry in sorted(catalog['entries'], key=lambda e: e['name'].lower()):
        name=entry['name']
        target=link('/reference/'+entry['group']+'/#'+name.lower())
        index.append(f"| [`{name}`]({target}) | {entry['kind'].replace('dependency-', '')} | `{entry['module']}` |")
    (STAGE/'command-index.md').write_text(page('Command index', '\n'.join(index), 7))
    for group, title in GROUPS.items():
        intro = (GUIDE/'_includes'/('intro-'+group+'.md')).read_text()
        body = '# '+title+'\n\n'+intro+'\n\n'
        for entry in [e for e in catalog['entries'] if e['group']==group]:
            name=entry['name']
            source=REPO+'/blob/'+revision+'/tex/latex/coursework/'+entry['module']+'.sty'
            body += '## `'+name+'`\n{: #'+name.lower()+' }\n\n'
            body += '<p class="api-meta">'+entry['kind']+' · <a href="'+source+'">'+entry['module']+'</a></p>\n\n'
            body += fence(entry['signature'])+'\n'+entry['description']+'\n\n**Arguments.** '+entry['arguments']+'\n\n'
            body += fence(snippets_by_id[entry['example']])+'\n'
            sample='homework-worked' if group in {'configuration','assignments'} else 'reference-coursepsets'
            body += '[View compiled example]('+link('/examples/'+sample+'/')+').\n\n'
            if group in {'mathematics', 'physics', 'environments'}:
                preview_page = {'mathematics': 1, 'physics': 2, 'environments': 3}[group]
                if entry['example'] in {'env-formula', 'env-mathtable', 'env-subparts'}:
                    preview_page = 4
                body += '<details><summary>Compiled specimen page · homework</summary><img class="preview" loading="lazy" alt="Compiled '+html.escape(title.lower())+' specimen including '+name+'" src="'+link('/assets/examples/'+sample+f'/page-{preview_page}.png')+'"></details>\n\n'
                body += '[Compare in notes]('+link('/examples/reference-coursenotes/')+').\n\n'
        (reference/(group+'.md')).write_text(page(title,body,list(GROUPS).index(group)+2,'Reference'))
    examplesdir=STAGE/'examples'
    examplesdir.mkdir()
    for item in report['examples']:
        folder=BUILD/'examples'/item['id']
        assets=STAGE/'assets/examples'/item['id']
        assets.mkdir(parents=True)
        pdf=folder/'output'/(Path(item['root']).stem+'.pdf')
        shutil.copy2(pdf,assets/'example.pdf')
        if (folder/'output/preview.png').exists():
            shutil.copy2(folder/'output/preview.png',assets/'preview.png')
        with zipfile.ZipFile(assets/'source.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(folder.rglob('*')):
                if file.is_file() and 'output' not in file.relative_to(folder).parts:
                    archive.write(file,arcname=item['id']+'/'+str(file.relative_to(folder)))
        body='# '+item['title']+'\n\n'
        body+='[Download PDF]('+link('/assets/examples/'+item['id']+'/example.pdf')+') · [Download runnable sources]('+link('/assets/examples/'+item['id']+'/source.zip')+')\n\n'
        body+='Compile `'+item['root']+'` from the extracted project directory. The source bundle includes instructions and all fragments.\n\n'
        if item['id'] == 'reference-coursepsets':
            body += 'This notation specimen uses an empty page style and does not declare an assignment. Its table therefore starts at 0.0.1; the complete homework projects show assignment-based numbering.\n\n'
        body+='## Source\n\n'+fence((folder/item['root']).read_text())+'\n'
        for file in sorted(folder.rglob('*.tex')):
            if file==folder/item['root'] or 'output' in file.relative_to(folder).parts:
                continue
            body+='<details markdown="1"><summary>'+html.escape(str(file.relative_to(folder)))+'</summary>\n\n'+fence(file.read_text())+'\n</details>\n\n'
        body+='## Compiled output\n\n'
        for i,file in enumerate(sorted((folder/'output').glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1])),1):
            shutil.copy2(file,assets/f'page-{i}.png')
            body+='### Page '+str(i)+'\n\n'
            body+='<a href="'+link('/assets/examples/'+item['id']+'/example.pdf')+'"><img class="preview" loading="lazy" alt="'+html.escape(item['title'])+', compiled page '+str(i)+'" src="'+link('/assets/examples/'+item['id']+f'/page-{i}.png')+'"></a>\n\n'
        (examplesdir/(item['id']+'.md')).write_text(page(item['title'],body,report['examples'].index(item)+1,'Examples','/examples/'+item['id']+'/'))
    migration=(ROOT/'docs/MIGRATION.md').read_text()
    table=migration.split('## Complete command map',1)[1].split('## Environment and structure changes',1)[0]
    # Protect literal TeX from Liquid, preserving the table as Markdown.
    body='# Migrating from v1\n\nThe guide documents v2. Old aliases are not a compatibility layer. Use the source migration workflow for existing courses.\n\n{% raw %}\n'+table+'\n{% endraw %}\n\n'
    body+='[Full migration workflow]('+REPO+'/blob/master/docs/MIGRATION.md) · [Legacy course migration]('+REPO+'/blob/master/docs/LEGACY-COURSE-MIGRATION.md).\n'
    (STAGE/'migration.md').write_text(page('Migration from v1',body,9))


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.links=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate HTML anchor: '+attrs['id'])
            self.ids.add(attrs['id'])
        for attr in ['href','src']:
            if attrs.get(attr):
                self.links.append(attrs[attr])


def check_site():
    documents={}
    for file in SITE.rglob('*.html'):
        parser=Links()
        parser.feed(file.read_text())
        documents[file.resolve()]=parser
    for file, parser in documents.items():
        for url in parser.links:
            parsed=urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            path=unquote(parsed.path)
            if path.startswith('/'):
                if path != BASE and not path.startswith(BASE+'/'):
                    raise ValueError(f'URL escapes project base path: {file}: {url}')
                target=SITE/path[len(BASE):].lstrip('/')
            else:
                target=file.parent/path if path else file
            if target.is_dir():
                target=target/'index.html'
            if not target.exists():
                raise ValueError(f'Broken local link: {file}: {url}')
            if parsed.fragment and target.resolve() in documents and unquote(parsed.fragment) not in documents[target.resolve()].ids:
                raise ValueError(f'Broken anchor: {file}: {url}')
    search=read_json(SITE/'assets/js/search-data.json')
    searchable=json.dumps(search)
    for entry in read_json(GUIDE/'api.json')['entries']:
        if entry['name'] not in searchable:
            raise ValueError('Missing search entry: '+entry['name'])
    print(f'Validated {len(documents)} HTML pages, local assets, anchors, and search index',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--check',action='store_true',help='Check API coverage and runnable snippet links only')
    mode.add_argument('--examples-only',action='store_true',help='Compile/render examples; used by the TeX CI job')
    mode.add_argument('--site-only',action='store_true',help='Build site from verified, current compiled examples')
    args=parser.parse_args()
    BUILD.mkdir(parents=True,exist_ok=True)
    catalog, example_snippets=check_catalog()
    if args.check:
        return
    report=read_json(BUILD/'examples-report.json') if args.site_only else compile_examples()
    if args.examples_only:
        return
    build_source(catalog,example_snippets,report)
    env={**os.environ,'BUNDLE_GEMFILE':str(GUIDE/'Gemfile'),'BUNDLE_PATH':str(BUILD/'gems')}
    print(run(['bundle','exec','jekyll','build','--source',str(STAGE),'--destination',str(SITE),
               '--config',str(STAGE/'_config.yml'),'--strict_front_matter','--trace'],env=env),flush=True)
    check_site()
    print('Guide ready: '+str(SITE/'index.html'),flush=True)


if __name__=='__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        print(str(error),file=sys.stderr)
        sys.exit(1)
