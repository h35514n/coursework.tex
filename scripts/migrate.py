#!/usr/bin/env python3
"""Migrate coursework v1 source. Dry-run by default; --write applies reviewed edits.

The scanner preserves comments/verbatim and reads balanced arguments. Ambiguous
assignment layouts and inconsistent repeated metadata are errors, not guesses.
"""
import argparse
import difflib
import json
from pathlib import Path
import re
import subprocess

SIMPLE = {
    'L': r'\left', 'R': r'\right', 'x': r'\times', 'pd': r'\partial',
    'p': r'\paren*', 'bs': r'\bracket*', 'bc': r'\bracket*',
    'mean': r'\average', 'ex': r'\expectation', 'var': r'\variance', 'cov': r'\covariance',
    'prob': r'\probability', 'cndprb': r'\conditionalprob', 'sfrac': r'\slashfrac',
    'mtxt': r'\mathtext', 'comb': r'\combinations', 'perm': r'\permutations',
    'vectrm': r'\uprightvect', 'vhat': r'\unitvect', 'vhatrm': r'\uprightunitvect',
    'lap': r'\laplacian', 'rcurs': r'\separation', 'brcurs': r'\separationvect',
    'hrcurs': r'\separationunit', 'varv': r'\volumeregion', 'sarv': r'\surfaceregion',
    'parv': r'\pathregion', 'qeq': r'\questioneq', 'cheq': r'\checkeq', 'creq': r'\crosseq',
    'full': r'\displaystyle', 'Deg': r'\ensuremath{^\circ}',
    'mc': r'\text{,}\hspace{1em}', 'nth': r'n\text{th}', 'ith': r'i\text{th}',
    'double': r'\tableheading', 'D': r'\deriv', 'PD': r'\pderiv',
    'sikB': r'\constantvalue{boltzmann}', 'siNa': r'\constantvalue{avogadro}',
    'ivda': r'\int \uprightvect{v}\cdot\dd\uprightvect{a}',
    'ivdl': r'\int \uprightvect{v}\cdot\dd\uprightvect{l}', 'bm': r'\mathbold',
}
META = {'Author':'author', 'CourseNumber':'course-code', 'CourseName':'course-title',
        'CourseTerm':'term', 'CourseText':'textbook', 'CourseTextAuthor':'textbook-author'}
THEOREMS = {'theorem','lemma','corollary','proposition','conjecture','algorithm',
            'remark','definition','example','summary'}

class MigrationError(ValueError): pass


def whitespace(s, i):
    while i < len(s):
        if s[i].isspace(): i += 1
        elif s[i] == '%':
            j = s.find('\n', i); i = len(s) if j < 0 else j + 1
        else: break
    return i


def group(s, i, left='{', right='}'):
    i = whitespace(s, i)
    if i >= len(s) or s[i] != left:
        raise MigrationError(f'Expected {left} near {s[max(0,i-25):i+50]!r}')
    start = i + 1; stack = [right]; i += 1
    while i < len(s):
        c = s[i]
        if c == '\\':
            m = re.match(r'\\(?:[A-Za-z@]+|.)', s[i:], re.S)
            i += len(m[0]) if m else 1; continue
        if c == '%':
            j = s.find('\n', i); i = len(s) if j < 0 else j + 1; continue
        if c == '{': stack.append('}')
        elif c == '[' and left == '[' and stack[-1] != '}': stack.append(']')
        elif c == stack[-1]:
            stack.pop()
            if not stack: return s[start:i], i + 1
        i += 1
    raise MigrationError('Unbalanced argument')


def optional(s, i, default=None):
    j = whitespace(s, i)
    return group(s, j, '[', ']') if j < len(s) and s[j] == '[' else (default, i)


def args(s, i, n):
    out=[]
    for _ in range(n):
        a,i=group(s,i);out.append(a)
    return out,i


def commands(s):
    """Yield active control words; skip comments and verbatim bodies."""
    i=0
    while i<len(s):
        if s[i]=='%':
            j=s.find('\n',i); i=len(s) if j<0 else j+1;continue
        if s[i]!='\\': i+=1;continue
        m=re.match(r'\\([A-Za-z@]+|.)',s[i:],re.S)
        if not m: break
        name=m[1];end=i+len(m[0])
        if name=='verb':
            if end<len(s) and s[end]=='*':end+=1
            if end<len(s):
                j=s.find(s[end],end+1);i=len(s) if j<0 else j+1;continue
        if name=='begin':
            env,j=group(s,end)
            if env in {'verbatim','verbatim*','lstlisting','minted'}:
                k=s.find('\\end{'+env+'}',j)
                if k<0:raise MigrationError('Unclosed verbatim environment')
                i=k+len(env)+6;continue
        yield i,end,name
        i=end


def migrate_text(s):
    out=[];cursor=0
    for start,end,name in commands(s):
        if start<cursor:continue
        replacement=None;j=end
        if re.fullmatch(r'bigint[s]*',name):
            raise MigrationError('Sized integral requires manual conversion to \\integral[size=medium|large]{expression}{variable}{lower}{upper}; preserve its sizing intent.')
        elif name in SIMPLE: replacement=SIMPLE[name]
        elif name in META: replacement='\\courseworkvalue{'+META[name]+'}'
        elif name in {'abs','norm'}:
            if end>=len(s) or s[end]!='*': replacement='\\'+name+'*'
        elif name in {'fdd','fdl','pdd','pdl'}:
            a,j=args(s,end,2); a=[migrate_text(x) for x in a]
            replacement=('\\deriv' if name.startswith('f') else '\\pderiv')
            if name.endswith('l'):replacement+='[2]'
            replacement+=''.join('{'+x+'}' for x in a)
        elif name=='Int':
            v,j=optional(s,end,'x');a,j=args(s,j,3)
            replacement='\\integral'+''.join('{'+migrate_text(x)+'}' for x in [a[2],v,a[0],a[1]])
        elif name in {'eval','Eval'}:
            a,j=args(s,end,3)
            replacement=('\\evalat' if name=='eval' else '\\evalbracket')+''.join('{'+migrate_text(x)+'}' for x in [a[2],a[0],a[1]])
        elif name in {'Sum','infsum'}:
            v,j=optional(s,end,'n');a,j=args(s,j,2 if name=='Sum' else 1)
            replacement='\\sum_{'+migrate_text(v)+'='+migrate_text(a[0])+'}^{'+(migrate_text(a[1]) if name=='Sum' else '\\infty')+'}'
        elif name=='Lim':
            limit,j=optional(s,end,r'\infty');a,j=args(s,j,2)
            replacement='\\lim_{'+migrate_text(a[0])+r'\to '+migrate_text(limit)+'}'+migrate_text(a[1])
        elif name in {'twovector','threevector','fourvector'}:
            align,j=optional(s,end,'r');a,j=args(s,j,{'twovector':2,'threevector':3,'fourvector':4}[name])
            replacement='\\colvector['+align+']{'+('\\' * 2).join(migrate_text(x) for x in a)+'}'
        elif name in {'e','E','u'}:
            a,j=args(s,end,1)
            replacement=({'e':r'\times 10^{%s}','E':'10^{%s}','u':r'\unit{%s}'}[name])%migrate_text(a[0])
        elif name=='heading':
            title,j=optional(s,end,'');a,j=args(s,j,4)
            replacement=('\\listoftodos\\clearpage\n\\pagenumbering{arabic}\n'
                         '\\makecourseworktitle[title={'+title+'}]\n'
                         '\\tableofcontents\\newpage\n\\makeassignmentheading[title={'+title+'}]')
        elif name in {'begin','end'}:
            env,j=group(s,end)
            if env=='sublist': replacement='\\'+name+'{subparts}'
            elif name=='begin' and env in THEOREMS:
                title,k=optional(s,j)
                q=whitespace(s,k)
                if q<len(s) and s[q]=='{':
                    label,k=group(s,k)
                    if not re.fullmatch(r'[\w:.-]+',label):raise MigrationError('Ambiguous theorem label: '+label)
                    replacement='\\begin{'+env+'}'+('['+migrate_text(title)+']' if title is not None else '')+'\\label{'+label+'}'
                    j=k
            elif name=='begin' and env=='mathtable':
                keys,k=optional(s,j)
                if keys is not None and re.search(r'\bcaption\s*=\s*(true|false)',keys):
                    # Existing tables use braced values. Split only top-level commas.
                    parts=[];at=0;depth=0
                    for pos,c in enumerate(keys+','):
                        if c=='{':depth+=1
                        if c=='}':depth-=1
                        if c==',' and depth==0:parts.append(keys[at:pos].strip());at=pos+1
                    pairs=dict(p.split('=',1) for p in parts if '=' in p)
                    pairs={k.strip():v.strip() for k,v in pairs.items()}
                    title=pairs.pop('title','{}');shown=pairs.pop('caption')=='true'
                    if shown:pairs={'caption':title,**pairs}
                    elif 'label' in pairs:pairs.pop('label')
                    replacement='\\begin{mathtable}['+','.join(k+'='+migrate_text(v) for k,v in pairs.items())+']';j=k
        if replacement is not None:
            out.extend([s[cursor:start],replacement]);cursor=j
    out.append(s[cursor:]);return ''.join(out)


def calls(s, wanted):
    for start,end,name in commands(s):
        if name in wanted:yield start,end,name


def migrate_assignment(s, root=None):
    matches=list(calls(s,{'chap'}))
    if not matches:return s
    if len(matches)!=1:raise MigrationError('Expected one assignment per subfile')
    start,end,_=matches[0];number,j=optional(s,end,'0');title,j=group(s,j)
    declarations=[];seen={}
    for _,end,name in calls(s,{'includeproblem','includeguide','includediscussion'}):
        heading,k=optional(s,end,'');a,k=args(s,k,2);key=(a[0],a[1])
        if key in seen and seen[key]!=heading:raise MigrationError('Inconsistent titles for '+str(key))
        seen[key]=heading
        if name=='includeproblem':declarations.append((a[0],a[1],heading))
    if not declarations:
        # Earlier courses use adjacent statement / wrapped-solution imports.
        for _,end,name in calls(s,{'input'}):
            fragment,_=group(s,end)
            match=re.fullmatch(r'(homework/[^/]+)/problem([^/]+?)(?:\.tex)?',fragment)
            if not match:continue
            if root is None:raise MigrationError('Fragment lookup requires repository root')
            text=(root/(fragment if fragment.endswith('.tex') else fragment+'.tex')).read_text()
            headings=list(calls(text,{'problem'}))
            if len(headings)!=1:raise MigrationError('Expected one problem heading in '+fragment)
            problem_title,_=optional(text,headings[0][1],'')
            declarations.append((match[1],match[2],problem_title))
    if not declarations:raise MigrationError('Assignment has no problem declarations')
    directories={x[0] for x in declarations}
    if len(directories)!=1:raise MigrationError('Multiple directories in one assignment')
    directory=next(iter(directories));ids=[x[1] for x in declarations]
    if len(ids)!=len(set(ids)):raise MigrationError('Duplicate problem inclusion')
    assignment_id=Path(directory).name
    tail=s.find(r'\end{document}',j)
    if tail<0:raise MigrationError('Assignment missing end document')
    # Only known structure is safe to replace. Comments/whitespace are allowed.
    body=s[j:tail]
    scrub=re.sub(r'%[^\n]*','',body)
    # Strip solution wrappers first so their nested inputs aren't processed twice.
    for a,b,n in reversed(list(calls(scrub,{'solution'}))):
        value,k=group(scrub,b)
        if not re.fullmatch(r'\s*\\input\{homework/[^}]+/solution[^}]+\}\s*',value):
            raise MigrationError('Non-fragment solution needs manual migration')
        scrub=scrub[:a]+scrub[k:]
    for a,b,n in reversed(list(calls(scrub,{'sect','pagebreak','newpage','clearpage','input','includeproblem','includeguide','includediscussion'}))):
        k=b
        if n=='sect':_,k=optional(scrub,k);_,k=group(scrub,k)
        elif n.startswith('include'):_,k=optional(scrub,k);_,k=args(scrub,k,2)
        elif n=='input':_,k=group(scrub,k)
        scrub=scrub[:a]+scrub[k:]
    if scrub.strip():raise MigrationError('Unrecognized assignment content: '+scrub[:100])
    new='\\assignment[id='+assignment_id+',number='+number+',directory='+directory+']{'+title+'}\n\n'
    new+='\n'.join('\\declareproblem[title={'+h+'}]{'+i+'}' for _,i,h in declarations)
    return s[:start]+new+'\n\n\\printassignment\n\n'+s[tail:]


def migrate_course(s):
    values={}
    for _,end,name in calls(s,{'newcommand'}):
        key,j=group(s,end)
        if key.lstrip('\\') in META:
            value,j=group(s,j);values[META[key.lstrip('\\')]]=value
    if not values:return s
    if len(values)!=len(META):raise MigrationError('Incomplete course metadata')
    return '% Shared course identity and subject notation.\n\\usepackage{coursephys}\n\\courseworksetup{\n'+',\n'.join('  '+k+'={'+v+'}' for k,v in values.items())+'\n}\n'


def migrate_file(path, s, root=None):
    if path.name=='course.tex':return migrate_course(s)
    if path.parent.name=='homework':s=migrate_assignment(s,root)
    if path.name.startswith('problem') and path.parent.parent.name=='homework':
        for start,end,_ in reversed(list(calls(s,{'problem'}))):
            _,j=optional(s,end,'');s=s[:start]+s[j:]
    s=s.replace(r'\documentclass[../homework.tex]{subfiles}',r'\documentclass[homework.tex]{subfiles}')
    s=s.replace(r'\documentclass[../notes.tex]{subfiles}',r'\documentclass[notes.tex]{subfiles}')
    s=s.replace(r'\documentclass[expand,final]{coursepsets}',r'\documentclass[mode=worked,problem-breaks=page,final]{coursepsets}')
    if path.name=='notes.tex':
        lines=s.splitlines(True)
        s=''.join(line for line in lines if not re.match(r'\\newcommand\{\\(?:kB|NA|dbar)\}',line))
    return migrate_text(s)


def scoped_labels(contents):
    definitions={}
    for path,s in contents.items():
        for _,end,name in calls(s,{'label'}):
            label,_=group(s,end);definitions.setdefault(label,[]).append(path)
    duplicate={label:paths for label,paths in definitions.items() if len(paths)>1}
    for label,paths in duplicate.items():
        if any(p.parent.parent.name!='homework' for p in paths):
            raise MigrationError('Ambiguous duplicate label: '+label)
        if len({p.parent for p in paths})!=len(paths):raise MigrationError('Duplicate label within assignment: '+label)
    for path,s in list(contents.items()):
        edits=[]
        for start,end,name in calls(s,{'label','ref','eqref','cref','Cref','nameref','pageref','autoref'}):
            label,j=group(s,end)
            if label in duplicate:
                owners=[p for p in duplicate[label] if p.parent==path.parent]
                if len(owners)!=1:raise MigrationError(f'Ambiguous cross-assignment reference {label} in {path}')
                prefix,sep,suffix=label.partition(':')
                target=(prefix+':'+path.parent.name+':'+suffix) if sep else path.parent.name+':'+label
                edits.append((start,j,'\\'+name+'{'+target+'}'))
        for a,b,t in reversed(edits):s=s[:a]+t+s[b:]
        contents[path]=s
    return duplicate


def migrate_repository(root):
    names=subprocess.check_output(['git','-C',str(root),'ls-files','-z'],text=True).split('\0')
    contents={Path(n):(root/n).read_text() for n in names if n.endswith('.tex') and (root/n).is_file()}
    updated={p:migrate_file(p,s,root) for p,s in contents.items()}
    duplicates=scoped_labels(updated)
    changes={str(p):(contents[p],s) for p,s in updated.items() if s!=contents[p]}
    make=root/'Makefile'
    if make.is_file():
        old=make.read_text();new=old.replace(r"\PassOptionsToClass{summary}{coursepsets}",r"\AtBeginDocument{\courseworksetup{mode=compact}}")
        new=new.replace(r"\PassOptionsToClass{worksheet}{coursepsets}",r"\AtBeginDocument{\courseworksetup{mode=worksheet}}")
        if new!=old:changes['Makefile']=(old,new)
    return changes,duplicates


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('repository',type=Path)
    parser.add_argument('--write',action='store_true');parser.add_argument('--report',type=Path)
    args=parser.parse_args();root=args.repository.resolve()
    try:changes,duplicates=migrate_repository(root)
    except MigrationError as e:parser.exit(2,f'Migration needs inspection: {e}\n')
    for name,(before,after) in changes.items():
        if args.write:(root/name).write_text(after)
        else:print(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=name,tofile=name)),end='')
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps({'repository':str(root),'changed_files':list(changes),
                                          'duplicate_labels':{k:[str(p) for p in v] for k,v in duplicates.items()}},indent=2)+'\n')
    print(f'{"Migrated" if args.write else "Would migrate"} {len(changes)} files.')

if __name__=='__main__':main()
