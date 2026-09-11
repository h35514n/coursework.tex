#!/usr/bin/env python3
"""Prepare and migrate the two self-contained coursework dialects.

Dry-run by default. Preparation preserves the legacy renderer and input order;
conversion extracts problem/solution pairs and uses the public v2 renderer.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

from migrate import MigrationError, args, calls, commands, group, optional, whitespace

COURSES = {
 'mechanics': dict(code='321', title='Modern Classical Mechanics', term='Fall 2024',
                   textbook='Modern Classical Mechanics', authors=r'Helliwell \& Sahakian',
                   entry='problems.tex', counts=[10,10,8,6,7,5,8,11,7],
                   ids=['01-pset','02-pset','03-pset','04-pset','midterm','05-pset','06-pset','07-pset','final'],
                   chapters=[1,1,2,3,4,6,7,9]),
 'thermal': dict(code='432', title=r'Thermodynamics \& Statistical Mechanics', term='Summer 2024',
                 textbook='Concepts in Thermal Physics', authors=r'Blundell \& Blundell',
                 entry='assignments.tex', counts=[12,10,10,10,9,10,27,10,10,10,10,10,10,45],
                 ids=['01-pset','01-quiz','02-pset','02-quiz','03-pset','03-quiz','04-midterm','05-pset','05-quiz','06-pset','06-quiz','07-pset','07-quiz','08-final'],
                 chapters=[1,1,2,3,4,5,6,11,12,14,15,16,18,19,20,21,23,24,33]),
}


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def read_active(root):
    names=subprocess.check_output(['git','-C',str(root),'ls-files','-z'],text=True).split('\0')
    return {n:(root/n).read_text() for n in names if n.endswith('.tex') and not n.startswith(('handouts/','archive/'))}


def prepare(root, dialect):
    meta=COURSES[dialect];contents=read_active(root);changes={};mapping=[]
    source=contents[meta['entry']]
    structs=list(calls(source,{'chap','sect'}));starts=[];chapter=None;number=None
    for i,(a,b,n) in enumerate(structs):
        if n=='chap':
            number,k=optional(source,b,'0');chapter,k=group(source,k)
        else:
            role,k=group(source,b)
            start=structs[i-1][0] if i and structs[i-1][2]=='chap' else a
            starts.append((start,chapter,number,role))
    if len(starts)!=len(meta['ids']):raise MigrationError('Unexpected assignment inventory')
    end=source.index(r'\end{document}')
    combined=source[:starts[0][0]].replace(r'\begin{document}',r'\usepackage{subfiles}'+'\n'+r'\input{course}'+'\n\n'+r'\begin{document}')
    for index,(start,title,number,role) in enumerate(starts):
        ident=meta['ids'][index];stop=starts[index+1][0] if index+1<len(starts) else end
        body=source[start:stop]
        original_number=re.match(r'\d+',ident)
        label=(role+' '+str(int(original_number[0]))) if original_number and role in ['Problem Set','Quiz'] else role
        if dialect=='mechanics' and ident=='midterm':label='Midterm Exam'
        if dialect=='mechanics' and ident=='final':label='Final Exam'
        standalone=(r'\ifSubfilesClassLoaded{'+ '\n'+
                    r'\heading['+label+r']{Jacob Romer}{PHYS~'+meta['code']+'}{'+meta['title']+'}{'+meta['term']+'}\n')
        # A quiz/midterm shares its topic chapter in the combined legacy book.
        if not list(calls(body,{'chap'})):
            standalone+=r'\chap['+number+']{'+title+'}\n'
        standalone+='}{}\n'
        if not list(calls(body,{'chap'})):
            standalone+=r'\renewcommand*{\currentchapter}{'+number+'}\n'+r'\renewcommand*{\currentchaptername}{'+title+'}\n'
        path='homework/'+ident+'.tex'
        changes[path]=r'\documentclass[homework.tex]{subfiles}'+'\n'+r'\begin{document}'+'\n'+standalone+body+r'\end{document}'+'\n'
        combined+=r'\subfile{homework/'+ident+'}\n'
        mapping.append(dict(id=ident, number=index+1, original_number=number, title=title,
                            role=role, label=label, problems=meta['counts'][index], path=path))
    combined+=source[end:]
    changes['homework.tex']=combined;changes[meta['entry']]=None
    changes['course.tex']='% Course metadata remains in legacy headings until v2 conversion.\n'
    notes=contents['notes.tex'];includes=list(calls(notes,{'input'}));pairs=[]
    for a,b,n in includes:
        path,k=group(notes,b)
        if path.startswith('notes/'):pairs.append((a,k,path+'.tex' if not path.endswith('.tex') else path))
    if len(pairs)!=len(meta['chapters']):raise MigrationError('Unexpected notes inventory')
    start=notes.index(r'\chapter');end=notes.index(r'\end{document}')
    result=notes[:start].replace(r'\begin{document}',r'\usepackage{subfiles}'+'\n'+r'\input{course}'+'\n\n'+r'\begin{document}')
    cursor=start
    for index,(a,b,path) in enumerate(pairs):
        prefix=notes[cursor:a];body=contents[path];cursor=b
        if (dialect=='thermal' and index>=2) or (dialect=='mechanics' and path.endswith('chapter01-appendix.tex')):
            prefix=r'\renewcommand{\thesection}{\arabic{section}}'+'\n'+prefix
        seed=meta['chapters'][index] if path.endswith('01-useful-maths.tex') else meta['chapters'][index]-1
        changes[path]=(r'\documentclass[notes.tex]{subfiles}'+'\n'+r'\begin{document}'+'\n'+
                       r'\ifSubfilesClassLoaded{\setcounter{chapter}{'+str(seed)+'}}{}\n'+prefix+
                       r'\input{'+path.replace('notes/','notes/fragments/')[:-4]+'}\n'+
                       (r'\par'+'\n' if path.endswith('05-mb-distribution.tex') else '')+r'\end{document}'+'\n')
        changes[path.replace('notes/','notes/fragments/')]=body
        result+=r'\subfile{'+path[:-4]+'}\n'
    result+=notes[cursor:];changes['notes.tex']=result
    # Reuse the established course interface; omit unrelated textbook-index tooling.
    template=(Path(__file__).resolve().parents[2]/'phys331-electricity-and-magnetism/Makefile').read_text()
    a=template.index('# Rebuilds tools/textbook-index.json');b=template.index('clean:',a)
    template=template[:a]+template[b:]
    template='\n'.join(line for line in template.splitlines() if 'textbook-index' not in line)+'\n'
    template=template.replace('COMMON  := course.tex','COMMON  := course.tex\nLEGACY := $(wildcard problems/*.tex assignments/*.tex assignments/*/*.tex notes/fragments/*.tex)')
    template=template.replace('$(CLSDEPS)','$(CLSDEPS) $(LEGACY)')
    template=template.replace('kpsewhich coursepsets.cls','kpsewhich problemsets.cls')
    template=template.replace(r'\AtBeginDocument{\courseworksetup{mode=compact}}',r'\PassOptionsToClass{summary}{problemsets}')
    template=template.replace(r'\AtBeginDocument{\courseworksetup{mode=worksheet}}',r'\PassOptionsToClass{worksheet}{problemsets}')
    template=template.replace('$(wildcard notes/*.tex)', '$(wildcard notes/*.tex) $(wildcard notes/fragments/*.tex)')
    # CHAPS must list entrypoints only, never the fragments.
    template=template.replace('$(patsubst notes/%.tex,%,$(wildcard notes/*.tex) $(wildcard notes/fragments/*.tex))','$(patsubst notes/%.tex,%,$(wildcard notes/*.tex))')
    changes['Makefile']=template
    changes['latexmkrc']="""# XeLaTeX with isolated output directories; invoke from the repository root.
$out_dir = 'build';
$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
$max_repeat = 8;
$clean_ext .= ' fdb_latexmk fls run.xml synctex.gz xdv';
"""
    report={'dialect':dialect,'source_revision':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),
            'assignments':mapping,'notes':[p for _,_,p in pairs],
            'original_content_hashes':{n:digest(s) for n,s in contents.items()}}
    changes['migration-map.json']=json.dumps(report,indent=2)+'\n'
    return changes,report


def expand_inputs(text, root, used, stack=()):
    """Expand only explicit local TeX imports, retaining their complete bytes."""
    edits=[]
    for a,b,_ in calls(text,{'input'}):
        value,end=group(text,b);path=Path(value)
        if not path.suffix:path=path.with_suffix('.tex')
        resolved=(root/path).resolve()
        if not resolved.is_relative_to(root.resolve()):raise MigrationError('Input escapes repository: '+value)
        if path in stack:raise MigrationError('Cyclic input: '+value)
        if not resolved.is_file():raise MigrationError('Missing input: '+value)
        contents=resolved.read_text();used[str(path)]=digest(contents)
        edits.append((a,end,expand_inputs(contents,root,used,(*stack,path))))
    for a,b,s in reversed(edits):text=text[:a]+s+text[b:]
    return text


def split_problems(text):
    starts=list(calls(text,{'problem'}))
    if not starts:raise MigrationError('No problems found')
    problems=[]
    for index,(a,b,_) in enumerate(starts):
        title,k=optional(text,b,'');stop=starts[index+1][0] if index+1<len(starts) else len(text)
        chunk=text[k:stop];solutions=list(calls(chunk,{'solution'}))
        if len(solutions)!=1:raise MigrationError('Expected exactly one solution wrapper per problem')
        c,d,_=solutions[0];visibility,q=optional(chunk,d)
        if visibility is not None:raise MigrationError('Explicit solution visibility needs review')
        solution,q=group(chunk,q)
        suffix=chunk[q:]
        # Parent-level breaks become renderer-owned problem boundaries.
        for x,y,n in reversed(list(calls(suffix,{'pagebreak','newpage','clearpage'}))):suffix=suffix[:x]+suffix[y:]
        trailing = re.sub(r'%[^\n]*','',suffix).strip()
        if trailing and trailing != 'TODO':raise MigrationError('Content outside solution needs review: '+suffix[:80])
        prefix=text[:a] if index==0 else ''
        if index==0 and re.sub(r'%[^\n]*','',prefix).strip():raise MigrationError('Content before first problem needs review')
        problems.append(dict(title=title,statement=prefix+chunk[:c]+(suffix if trailing else ''),
                             solution=solution+('' if trailing else suffix), trailing_annotation=trailing,
                             empty_solution=not solution.strip()))
    return problems


def migrate_notation(text, *, notes=False):
    from migrate import migrate_text
    edits=[]
    for a,b,name in commands(text):
        if name=='Sum' and notes:
            values,end=args(text,b,2)
            edits.append((a,end,r'\sum_{'+migrate_notation(values[0],notes=True)+'}^{'+migrate_notation(values[1],notes=True)+'}'))
        elif name in {'diff','diffp'}:
            try:
                order,k=optional(text,b,'1');values,k=args(text,k,2)
                held,end=optional(text,k)
                if held is None and re.fullmatch(r'\d+',order) and ',' not in values[1]:
                    result=('\\deriv' if name=='diff' else '\\pderiv')+('['+order+']' if order!='1' else '')
                    result+=''.join('{'+migrate_notation(v,notes=notes)+'}' for v in values)
                    edits.append((a,k,result))
            except MigrationError:
                # diffcoeff also accepts unbraced/mixed/operator forms. Keep its
                # public syntax; the shared math package deliberately loads it.
                pass
        elif name == 'cross':
            edits.append((a,b,r'\mathbold{\times}'))
        elif name in {'bvect','bdot','bddot'}:
            edits.append((a,b,{'bvect':r'\uprightvect','bdot':r'\mechanicsdot','bddot':r'\mechanicsddot'}[name]))
    # Outer replacements already transform their balanced nested arguments.
    cursor=0;parts=[]
    for a,b,value in sorted(edits):
        if a<cursor:continue
        parts.extend([text[cursor:a],value]);cursor=b
    parts.append(text[cursor:]);text=''.join(parts)
    # The notes classes use native theorem syntax for these environments;
    # only definition has the old mandatory label argument.
    if notes:
        for env in ['example','remark','summary']:
            text=text.replace('{'+env+'}', '{legacyNative'+env+'}')
    text=migrate_text(text)
    if notes:
        for env in ['example','remark','summary']:
            text=text.replace('{legacyNative'+env+'}', '{'+env+'}')
    return text


def qualify_labels(contents):
    definitions={};report=[]
    def scope(path):
        p=Path(path)
        if p.parts[0]=='homework':
            problem=re.search(r'(?:problem|solution)([^/]+)\.tex$',p.name)
            return ('homework',p.parent.name,problem[1] if problem else '')
        return ('notes',p.stem,'')
    for path,text in contents.items():
        doc,assignment,problem=scope(path)
        for a,b,n in calls(text,{'label'}):
            label,_=group(text,b);definitions.setdefault((doc,label),[]).append(path)
    duplicates={key:paths for key,paths in definitions.items() if len(paths)>1}
    for (doc,label),owners in duplicates.items():
        if len(owners)!=len(set(owners)):raise MigrationError('Duplicate label in one fragment: '+label)
        targets={}
        for owner in owners:
            _,assignment,problem=scope(owner);prefix,sep,tail=label.partition(':')
            target=':'.join(filter(None,[prefix if sep else 'label',assignment,problem,tail if sep else label]))
            if target in targets.values():raise MigrationError('Duplicate label across roles in one problem: '+label)
            targets[owner]=target
        for path,text in list(contents.items()):
            if scope(path)[0]!=doc:continue
            edits=[]
            for a,b,name in calls(text,{'label','ref','eqref','cref','Cref','nameref','pageref','autoref'}):
                start=b+1 if text[b:b+1]=='*' else b
                value,end=group(text,start);labels=value.split(',')
                if label not in labels:continue
                if path in owners:owner=path
                else:
                    local=[p for p in owners if scope(p)[1:]==scope(path)[1:]]
                    if len(local)!=1:local=[p for p in owners if scope(p)[1]==scope(path)[1]]
                    if len(local)!=1:raise MigrationError(f'Ambiguous reference {label} in {path}')
                    owner=local[0]
                target=targets[owner];labels=[target if x==label else x for x in labels]
                edits.append((a,end,'\\'+name+('*' if start>b else '')+'{'+','.join(labels)+'}'))
                report.append(dict(file=path,command=name,old=label,new=target))
            for a,b,value in reversed(edits):text=text[:a]+value+text[b:]
            contents[path]=text
    return report


def convert(root):
    mapping=json.loads((root/'migration-map.json').read_text());dialect=mapping['dialect'];meta=COURSES[dialect]
    # Completed repositories are a no-op, including archived legacy sources.
    if r'\documentclass[mode=worked' in (root/'homework.tex').read_text():
        return {},{'dialect':dialect,'idempotent':True,'changed_files':[]}
    original=read_active(root);changes={};pairs=[];consumed={};fragments={};empty=0
    for assignment in mapping['assignments']:
        wrapper=original[assignment['path']]
        sects=list(calls(wrapper,{'sect'}))
        if len(sects)!=1:raise MigrationError('Expected one legacy role in '+assignment['path'])
        _,b,_=sects[0];_,begin=group(wrapper,b);end=wrapper.index(r'\end{document}',begin)
        text=expand_inputs(wrapper[begin:end],root,consumed)
        problems=split_problems(text)
        if len(problems)!=assignment['problems']:raise MigrationError('Problem count changed in '+assignment['id'])
        declarations=[]
        for index,problem in enumerate(problems,1):
            ident=f'{index:02}';directory='homework/'+assignment['id']
            for role in ['statement','solution']:
                dest=directory+('/problem' if role=='statement' else '/solution')+ident+'.tex'
                fragments[dest]=migrate_notation(problem[role])
            declarations.append(r'\declareproblem[title={'+migrate_notation(problem['title'])+'}]{'+ident+'}')
            pairs.append(dict(assignment=assignment['id'],problem=ident,title=problem['title'],
                              statement_sha256=digest(problem['statement']),solution_sha256=digest(problem['solution']),
                              empty_solution=problem['empty_solution'],trailing_annotation=problem['trailing_annotation']))
            empty+=problem['empty_solution']
        label=assignment['label'];title=assignment['title']
        # Identify quizzes/exams explicitly even when their topic matches a set.
        heading=label+': '+title
        changes[assignment['path']]=(r'\documentclass[homework.tex]{subfiles}'+'\n'+r'\begin{document}'+'\n'+
            r'\ifSubfilesClassLoaded{'+ '\n'+r'\makeassignmentheading[title={'+label+'}]\n}{}\n\n'+
            r'\assignment[id='+assignment['id']+',number='+str(assignment['number'])+',directory=homework/'+assignment['id']+
            ',problems-title={'+assignment['role']+'}]{'+heading+'}\n\n'+'\n'.join(declarations)+'\n\n'+r'\printassignment'+'\n'+r'\end{document}'+'\n')
    if len(pairs)!=sum(meta['counts']) or empty!=(13 if dialect=='thermal' else 0):raise MigrationError('Content inventory mismatch')
    label_changes=qualify_labels(fragments);changes.update(fragments)
    for path in consumed:changes[path]=None
    for path in mapping['notes']:
        wrapper=original[path];used={};expanded=expand_inputs(wrapper,root,used)
        # Group prefixes and printed counters remain unchanged. H-destinations
        # use source identity and printed section names (A versus 1).
        ident=Path(path).stem
        anchors=(r'\renewcommand{\theHchapter}{notes-'+ident+'}\n'+
                 r'\renewcommand{\theHsection}{\theHchapter.\thesection}'+'\n')
        expanded=expanded.replace(r'\begin{document}',r'\begin{document}'+'\n'+anchors,1)
        changes[path]=migrate_notation(expanded,notes=True)
        for source in used:changes[source]=None
    changes['course.tex']=(r'\usepackage{coursephys}'+'\n'+r'\courseworksetup{'+'\n'+
        '  author={Jacob Romer},\n  course-code={PHYS~'+meta['code']+'},\n  course-title={'+meta['title']+'},\n  term={'+meta['term']+'},\n'+
        '  textbook={'+meta['textbook']+'},\n  textbook-author={'+meta['authors']+'}\n}\n')
    changes['homework.tex']=(r'\documentclass[mode=worked,problem-breaks=page,final]{coursepsets}'+'\n'+r'\input{course}'+'\n'+
        (r'\usepackage{mechanicsnotation}'+'\n' if dialect=='mechanics' else '')+'\n'+r'\begin{document}'+'\n'+
        r'\listoftodos\clearpage'+'\n'+r'\pagenumbering{arabic}'+'\n'+r'\makecourseworktitle[title={Assignments}]'+'\n'+
        r'\tableofcontents\newpage'+'\n'+r'\makeassignmentheading[title={Assignments}]'+'\n\n'+
        '\n'.join(r'\subfile{'+a['path'][:-4]+'}' for a in mapping['assignments'])+'\n\n'+r'\end{document}'+'\n')
    changes['notes.tex']=original['notes.tex'].replace(r'\documentclass{notes}',r'\documentclass{coursenotes}').replace(r'\usepackage{subfiles}'+'\n','')
    for name in ['notes.cls','problemsets.cls']:changes[name]=None
    if dialect=='mechanics':
        changes['mechanicsnotation.sty']=r'''% Course-specific Newton notation: preserve the original accent glyphs.
\ProvidesPackage{mechanicsnotation}[2026/09/11 Mechanics time accents]
\RequirePackage{accents}
\NewDocumentCommand\mechanicsdot{m}{%
  \accentset{\scalebox{0.4}[0.4]{\ensuremath{\bullet}}}{#1}}
\NewDocumentCommand\mechanicsddot{m}{%
  \accentset{\scalebox{0.4}[0.4]{\ensuremath{\bullet\bullet}}}{#1}}
\endinput
'''
    make=(root/'Makefile').read_text()
    make=make.replace('LEGACY := $(wildcard problems/*.tex assignments/*.tex assignments/*/*.tex notes/fragments/*.tex)','')
    make=make.replace(' $(LEGACY)','').replace(' $(wildcard notes/fragments/*.tex)','')
    make=make.replace('kpsewhich problemsets.cls','kpsewhich coursepsets.cls')
    make=make.replace(r'\PassOptionsToClass{summary}{problemsets}',r'\AtBeginDocument{\courseworksetup{mode=compact}}')
    make=make.replace(r'\PassOptionsToClass{worksheet}{problemsets}',r'\AtBeginDocument{\courseworksetup{mode=worksheet}}')
    make=make.replace('COMMON  := course.tex','COMMON  := course.tex $(wildcard *.sty)')
    changes['Makefile']=make
    report=dict(dialect=dialect,assignments=mapping['assignments'],problems=pairs,
                source_fragments=consumed,label_changes=label_changes,empty_solutions=empty,
                retained_rich_derivatives=True,archived_exclusions=['handouts/','archive/'])
    changes['migration-content.json']=json.dumps(report,indent=2)+'\n'
    return changes,report


def apply_changes(root,changes,write):
    for name,after in changes.items():
        path=root/name;before=path.read_text() if path.exists() else ''
        if after==before:continue
        if write:
            if after is None:path.unlink(missing_ok=True)
            else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(after)
        else:
            print(''.join(difflib.unified_diff(before.splitlines(True),(after or '').splitlines(True),fromfile=name,tofile=name)),end='')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['prepare','convert']);parser.add_argument('repository',type=Path)
    parser.add_argument('--dialect',choices=COURSES);parser.add_argument('--write',action='store_true');parser.add_argument('--report',type=Path)
    opt=parser.parse_args();root=opt.repository.resolve()
    try:
        if opt.operation=='prepare':
            if not opt.dialect:raise MigrationError('--dialect is required for preparation')
            changes,report=prepare(root,opt.dialect)
        else:changes,report=convert(root)
        apply_changes(root,changes,opt.write)
        if opt.report:opt.report.parent.mkdir(parents=True,exist_ok=True);opt.report.write_text(json.dumps(report,indent=2)+'\n')
        print(f'{"Applied" if opt.write else "Proposed"} {len(changes)} file operations.')
    except MigrationError as error:parser.exit(2,'Migration needs inspection: '+str(error)+'\n')

if __name__=='__main__':main()
