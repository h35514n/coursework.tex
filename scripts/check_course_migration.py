#!/usr/bin/env python3
"""Verify a completed legacy-course candidate beyond its rendered comparison."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

import migrate_legacy as m
import regression as r


def verify(root):
    candidate=root/'build/candidate';manifest=json.loads((candidate/'manifest.json').read_text())
    r.check_integrity(candidate,manifest)
    if manifest['testbed']!=r.source_info(root):raise RuntimeError('Candidate sources changed')
    mapping=json.loads((root/'migration-map.json').read_text())
    content=json.loads((root/'migration-content.json').read_text())
    expected=r.expected_pdfs(root)
    if sorted(manifest['pdfs'])!=expected:raise RuntimeError('Incomplete candidate inventory')
    baseline=root/'baseline';old=json.loads((baseline/'manifest.json').read_text());r.check_integrity(baseline,old)
    pairs={(p['assignment'],p['problem']):p for p in content['problems']}
    transformed={};checked=0
    for assignment in mapping['assignments']:
        src=baseline/'fixtures';wrapper=(src/assignment['path']).read_text()
        _,b,_=list(m.calls(wrapper,{'sect'}))[0];_,start=m.group(wrapper,b)
        end=wrapper.index(r'\end{document}',start)
        parts=m.split_problems(m.expand_inputs(wrapper[start:end],src,{}))
        for number,part in enumerate(parts,1):
            key=(assignment['id'],f'{number:02}');record=pairs[key]
            for role in ['statement','solution']:
                if m.digest(part[role])!=record[role+'_sha256']:raise RuntimeError('Extraction hash mismatch: '+str(key))
                path='homework/'+key[0]+('/problem' if role=='statement' else '/solution')+key[1]+'.tex'
                transformed[path]=m.migrate_notation(part[role])
            checked+=1
    m.qualify_labels(transformed)
    for path,text in transformed.items():
        if (root/path).read_text()!=text:raise RuntimeError('Unexplained source transformation: '+path)
    for path in mapping['notes']:
        wrapper=(baseline/'fixtures'/path).read_text()
        expanded=m.expand_inputs(wrapper,baseline/'fixtures',{})
        anchors=(r'\renewcommand{\theHchapter}{notes-'+Path(path).stem+'}\n'+
                 r'\renewcommand{\theHsection}{\theHchapter.\thesection}'+'\n')
        expanded=expanded.replace(r'\begin{document}',r'\begin{document}'+'\n'+anchors,1)
        expected_note=m.migrate_notation(expanded,notes=True)
        for repair in content.get('compatibility_repairs',[]):
            if repair['file']==path:expected_note=expected_note.replace(repair['before'],repair['after'])
        if (root/path).read_text()!=expected_note:raise RuntimeError('Unexplained notes transformation: '+path)
    # Existing graphics, handouts, guides and calculation documents are immutable.
    original=root/'migration-evidence/original/source';preserved=0
    for source in original.rglob('*'):
        if not source.is_file():continue
        rel=source.relative_to(original)
        archival=rel.parts[0]=='handouts'
        asset=source.suffix not in {'.tex','.cls'} and len(rel.parts)>1
        if archival or asset:
            actual=root/rel
            if not actual.is_file() or r.sha(actual)!=r.sha(source):raise RuntimeError('Original asset changed: '+str(rel))
            preserved+=1
    by_id={a['id']:a for a in mapping['assignments']};checks=[]
    for name in expected:
        pdf=candidate/'pdf'/name;fls=pdf.with_suffix('.fls').read_text();log=pdf.with_suffix('.log').read_text(errors='replace')
        inputs=[(root/line[6:]).resolve() for line in fls.splitlines() if line.startswith('INPUT ')]
        package_names={p.name for p in inputs};is_notes=name=='notes.pdf' or name.startswith('notes/')
        if 'mathspec.sty' in package_names or 'physics.sty' in package_names:raise RuntimeError('Legacy font/physics package loaded: '+name)
        needed={'unicode-math.sty','euler-math.sty'} if is_notes else {'mathpazo.sty','bm.sty'}
        if not needed<=package_names:raise RuntimeError('Wrong font backend: '+name)
        if not is_notes and 'unicode-math.sty' in package_names:raise RuntimeError('Unicode homework font: '+name)
        if re.search(r'Missing character:|Undefined control sequence|multiply defined|LaTeX Error:',log):raise RuntimeError('Critical TeX diagnostic: '+name)
        labels={};counts=Counter()
        aux=pdf.with_suffix('.aux').read_text()
        for a,b,_ in m.calls(aux,{'newlabel'}):
            values,_=m.args(aux,b,2);key,fields=values;counts[key]+=1
            value,_=m.group(fields,0);labels[key]=value
        if is_notes:
            old_aux=(baseline/'pdf'/name).with_suffix('.aux').read_text()
            old_labels={}
            for a,b,_ in m.calls(old_aux,{'newlabel'}):
                (key,fields),_=m.args(old_aux,b,2);old_labels[key]=m.group(fields,0)[0]
            for key,value in old_labels.items():
                if key.endswith('@cref') and value.startswith('[section]'):
                    ref=key.removesuffix('@cref')
                    if labels.get(ref)!=old_labels.get(ref):raise RuntimeError('Section reference changed: '+name+': '+ref)
        duplicates=[key for key,n in counts.items() if n>1]
        if duplicates:raise RuntimeError('Duplicate active labels: '+name+': '+str(duplicates))
        hidden=name=='problems.pdf' or name.startswith(('problems/','worksheets/'))
        solution_inputs=sorted({str(p.relative_to(root)) for p in inputs if p.is_relative_to(root) and re.fullmatch(r'solution\d+\.tex',p.name)})
        if hidden and solution_inputs:raise RuntimeError('Hidden solution file read: '+name)
        if not is_notes:
            if name in ['homework.pdf','problems.pdf']:assignments=mapping['assignments']
            else:
                stem=Path(name).stem.removesuffix('-problems').removesuffix('-worksheet');assignments=[by_id[stem]]
            canonical={}
            for a in assignments:
                for number in range(1,a['problems']+1):canonical[f"prob:{a['id']}:{number:02}"]=f"{a['number']}.{number}"
            actual={k:v for k,v in labels.items() if k.startswith('prob:') and not k.endswith('@cref')}
            if actual!=canonical:raise RuntimeError('Incorrect problem labels/numbering: '+name)
            if any(not labels.get(k+'@cref','').startswith('[problem]') for k in canonical):
                raise RuntimeError('Incorrect cleveref problem type: '+name)
            if not hidden:
                expected_solutions={f"homework/{a['id']}/solution{n:02}.tex" for a in assignments for n in range(1,a['problems']+1)}
                if set(solution_inputs)!=expected_solutions:raise RuntimeError('Incomplete worked solutions: '+name)
        checks.append({'pdf':name,'pages':manifest['pdfs'][name]['pages'],'font_profile':'euler' if is_notes else 'pazo',
                       'hidden_solutions':hidden,'loaded_solutions':len(solution_inputs),'labels':len(labels),
                       'recorder_font_paths':sorted({str(p) for p in inputs if p.suffix.lower() in {'.otf','.ttf','.pfb'}})})
    console=(candidate/'build.log').read_text(errors='replace')
    if re.search(r'Object @[^\n]*already defined',console):raise RuntimeError('Duplicate PDF destinations')
    font_files={}
    for name in ['texgyrepagella-regular.otf','texgyrepagella-italic.otf','texgyrepagella-bold.otf',
                 'texgyrepagella-bolditalic.otf','Euler-Math.otf','DejaVuSansMono.ttf',
                 'uplr8a.pfb','uplri8a.pfb','uplb8a.pfb','uplbi8a.pfb','fplmr.pfb','fplmri.pfb']:
        path=Path(subprocess.check_output(['kpsewhich',name],text=True).strip())
        if not path.is_file():raise RuntimeError('Selected font is missing: '+name)
        font_files[name]={'path':str(path),'sha256':r.sha(path)}
    return {'passed':True,'font_files':font_files,'source_revision':manifest['testbed']['revision'],'class_revision':manifest['class_revision'],
            'baseline_fixture_revision':old['testbed']['revision'],'outputs':len(checks),'problems':checked,
            'empty_solutions':content['empty_solutions'],'preserved_original_assets':preserved,
            'pdf_checks':checks,'remaining_warnings':manifest['warnings']}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('repository',type=Path);parser.add_argument('--output',type=Path)
    opts=parser.parse_args();root=opts.repository.resolve()
    report=verify(root)
    if opts.output:r.write_json(opts.output,report)
    print(f"PASS: {report['outputs']} outputs, {report['problems']} problems, {report['preserved_original_assets']} original assets")

if __name__=='__main__':main()
