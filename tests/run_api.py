#!/usr/bin/env python3
"""Behavioral TeX fixtures. All generated files stay under build/api."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from heading_spacing import check_heading_spacing

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/api'
CLASSES=ROOT/'tex/latex/coursework'
EPOCH='1789087534'


def run(args, **kw):return subprocess.run(args,text=True,capture_output=True,**kw)


def compile_case(name, body, *, cls='coursepsets', options='', preamble='', early_preamble='', error=None, checks=()):
    source=OUT/(name+'.tex');folder=OUT/name;folder.mkdir(parents=True,exist_ok=True)
    source.write_text('\\documentclass'+('['+options+']' if options else '')+'{'+cls+'}\n'+
      early_preamble+'\n'+(r'\usepackage{courseenvironments}\usepackage{hyperref}\usepackage{cleveref}' if cls=='article' else '')+
      '\n\\usepackage{coursephys}\n'+preamble+'\n\\begin{document}\n'+body+'\n\\end{document}\n')
    env={**os.environ,'TEXINPUTS':str(CLASSES)+'//:','SOURCE_DATE_EPOCH':EPOCH,'FORCE_SOURCE_DATE':'1'}
    proc=run(['latexmk','-xelatex','-halt-on-error','-interaction=nonstopmode','-recorder','-outdir='+str(folder),str(source)],cwd=ROOT,env=env)
    (folder/'console.log').write_text(proc.stdout+proc.stderr)
    log=(folder/(name+'.log')).read_text(errors='replace') if (folder/(name+'.log')).exists() else ''
    if error:
        assert proc.returncode and error in log, f'{name}: expected {error!r}; see {folder}/console.log'
        print('PASS expected error:',name,flush=True);return {'name':name,'expected_error':error}
    assert proc.returncode==0,f'{name}: build failed; see {folder}/console.log'
    pdf=folder/(name+'.pdf');text=run(['pdftotext','-layout',str(pdf),'-']).stdout
    aux=(folder/(name+'.aux')).read_text();fls=(folder/(name+'.fls')).read_text()
    bad=[s for s in ['Missing character:','already defined.','multiply defined','undefined references','cref reference format','Invalid end-point'] if s in log]
    if 'already defined.' in proc.stdout+proc.stderr:bad.append('duplicate PDF destination')
    assert not bad,f'{name}: unexpected diagnostics: {bad}'
    for line in fls.splitlines():
        if line.startswith('INPUT ') and Path(line[6:]).name.startswith('course') and Path(line[6:]).suffix in {'.cls','.sty'}:
            assert Path(line[6:]).resolve().parent==CLASSES, f'{name}: installed package fallback: {line}'
    for check in checks:check(text,aux,fls,log)
    print('PASS:',name,flush=True)
    return {'name':name,'pdf':str(pdf),'warnings':[x for x in log.splitlines() if 'Warning:' in x]}


def require_text(*values):
    def check(text,*_):
        for value in values:assert value in text,f'Missing text: {value!r}'
    return check


def absent(*values):
    def check(text,aux,fls,log):
        for value in values:assert value not in text and value not in fls, f'Hidden input executed: {value}'
    return check


def label(name,number):
    def check(text,aux,*_):assert '\\newlabel{'+name+'}{{'+number+'}' in aux, f'Wrong label {name}: expected {number}\n{aux}'
    return check


def page_groups(*groups):
    """Markers in each group share a page; successive groups start later."""
    def check(text,*_):
        pages=text.split('\f');previous=-1
        for group in groups:
            positions=[]
            for marker in group:
                matches=[i for i,page in enumerate(pages) if marker in page]
                assert len(matches)==1, f'Expected one occurrence of {marker}: {matches}'
                positions.extend(matches)
            assert len(set(positions))==1, f'Expected same page for {group}: {positions}'
            assert positions[0]>previous, f'Expected a page boundary before {group}'
            previous=positions[0]
    return check


def font_backend(profile):
    def check(text,aux,fls,log):
        inputs={Path(line[6:]).name for line in fls.splitlines() if line.startswith('INPUT ')}
        if profile=='pazo':
            assert {'mathpazo.sty','bm.sty'} <= inputs, 'Original Pazo backend not loaded'
            assert not {'unicode-math.sty','mathspec.sty'} & inputs, 'Competing math backend'
        else:
            assert 'unicode-math.sty' in inputs, 'Unicode backend not loaded'
            assert not {'mathpazo.sty','bm.sty','mathspec.sty'} & inputs, 'Competing math backend'
            assert ('euler-math.sty' in inputs)==(profile=='euler'), 'Wrong Unicode profile'
    return check


def main():
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    fragments=OUT/'fragments';fragments.mkdir()
    for i in ['01','02']:
        for role,word in [('guide','GuideBody'),('problem','Statement'),('solution','SolutionBody'),('discussion','DiscussionBody')]:
            (fragments/(role+i+'.tex')).write_text(word+i+'.\n'+
              '\\begin{equation}x='+str(int(i))+'\\label{eq:'+role+i+'}\\end{equation}\n'+
              ('\\begin{figure}[H]\\centering\\rule{1cm}{1cm}\\caption{Figure '+role+i+'}\\label{fig:'+role+i+'}\\end{figure}\n' if i=='02' else ''))
    (fragments/'problem03.tex').write_text('Statement03.\n')
    (fragments/'solution03.tex').write_text(r'\UndefinedSolutionMustNotExecute')
    (fragments/'discussion03.tex').write_text(r'\UndefinedDiscussionMustNotExecute')
    (fragments/'problem04.tex').write_text('Unsolved04.\n')
    (fragments/'problem05.tex').write_text('EmptySolution05.\n')
    (fragments/'solution05.tex').write_text('')
    (fragments/'problem06.tex').write_text('LongFirstPage.\\newpage LongSecondPage.\n')
    (fragments/'solution06.tex').write_text('LongSolution.\n')
    for name,body in {
      'guide07':'FlowGuide', 'problem07':'FlowStatementA', 'solution07':'FlowSolutionA',
      'discussion07':'FlowDiscussion', 'problem08':'FlowStatementB', 'solution08':'FlowSolutionB',
      'problem09':'FlowOtherAssignment', 'solution09':'FlowOtherSolution',
    }.items():
        (fragments/(name+'.tex')).write_text(body+'.\n')
    start=r'\assignment[id=alpha,number=3,directory=build/api/fragments]{Assignment}\label{assignment:alpha}'
    decl=r'\declareproblem[title={First}]{01}\declareproblem[title={Second}]{02}'
    render=r'\printassignment[problems={02,01}]'
    cases=[]
    cases.append(compile_case('ordered',start+decl+render+r'\cref{prob:alpha:02,prob:alpha:01}; \cref{assignment:alpha}; \nameref{prob:alpha:02}',checks=[label('prob:alpha:02','3.1'),label('prob:alpha:01','3.2'),label('eq:guide02','3.1.1'),label('eq:problem02','3.1.2'),label('eq:solution02','3.1.3'),label('eq:discussion02','3.1.4'),label('fig:discussion02','3.1.4'),require_text('Problem 1. Second','Problem 2. First','problems 3.1 and 3.2','assignment 3'),label('assignment:alpha','3')]))
    cases.append(compile_case('subset',start+decl+r'\printassignment[problems={02}]',checks=[label('prob:alpha:02','3.1'),absent('Statement01')]))
    for mode in ['worksheet','compact']:
        cases.append(compile_case(mode,start+r'\declareproblem{03}\declareproblem{04}\printassignment',options='mode=worked,problem-breaks=page',preamble=r'\AtBeginDocument{\courseworksetup{mode='+mode+'}}',checks=[require_text('Statement03','Unsolved04'),absent('solution03.tex','discussion03.tex','solution04.tex','Discussion')]))
    cases.append(compile_case('no-optional',start+r'\declareproblem{05}\printassignment',checks=[require_text('EmptySolution05'),absent('Guide','Discussion')]))
    cases.append(compile_case('long-problem',start+r'\declareproblem{06}\declareproblem{05}\printassignment',options='mode=worked,problem-breaks=page',checks=[require_text('LongFirstPage','LongSecondPage','LongSolution','EmptySolution05')]))
    cases.append(compile_case('independent',start+r'\declareproblem{05}\printassignment\assignment[id=beta,number=7,directory=build/api/fragments]{Another}\declareproblem{05}\printassignment',checks=[label('prob:alpha:05','3.1'),label('prob:beta:05','7.1')]))
    flow_body=(r'FrontMarker\par'+start+r'\declareproblem{07}\declareproblem{08}\printassignment'
      r'\assignment[id=beta,number=7,directory=build/api/fragments]{Another}\declareproblem{09}\printassignment')
    flow_checks=[require_text('FlowSolutionA','FlowSolutionB','FlowOtherSolution'),
      label('prob:alpha:07','3.1'),label('prob:alpha:08','3.2'),label('prob:beta:09','7.1')]
    cases.append(compile_case('worked-flow',flow_body,
      options='mode=worksheet,problem-breaks=page,assignment-breaks=page,section-breaks=page',
      preamble=r'\AtBeginDocument{\courseworksetup{mode=worked,problem-breaks=flow,assignment-breaks=flow,section-breaks=flow}}',
      checks=flow_checks+[page_groups(('FrontMarker','FlowGuide','FlowStatementA','FlowStatementB','FlowDiscussion','FlowOtherAssignment'))]))
    cases.append(compile_case('worked-page-boundaries',flow_body,
      options='mode=worked,problem-breaks=page,assignment-breaks=page,section-breaks=page',
      checks=flow_checks+[page_groups(('FrontMarker','FlowGuide'),('FlowStatementA',),('FlowStatementB',),('FlowDiscussion',),('FlowOtherAssignment',))]))
    cases.append(compile_case('worked-section-flow',flow_body,
      options='mode=worked,problem-breaks=flow,assignment-breaks=page,section-breaks=flow',
      checks=flow_checks+[page_groups(('FrontMarker','FlowGuide','FlowStatementA','FlowStatementB','FlowDiscussion'),('FlowOtherAssignment',))]))
    cases.append(compile_case('worked-assignment-flow',flow_body,
      options='mode=worked,problem-breaks=flow,assignment-breaks=flow,section-breaks=page',
      checks=flow_checks+[page_groups(('FrontMarker','FlowGuide'),('FlowStatementA','FlowStatementB'),('FlowDiscussion','FlowOtherAssignment'))]))
    for name,body,message in [
      ('duplicate',start+r'\declareproblem{01}\declareproblem{01}','Duplicate problem ID'),
      ('unknown',start+decl+r'\printassignment[problems={99}]','Unknown problem ID'),
      ('duplicate-selection',start+decl+r'\printassignment[problems={01,01}]','Duplicate selected problem ID'),
      ('missing-statement',start+r'\declareproblem{99}\printassignment','Required file missing'),
      ('missing-solution',start+r'\declareproblem{04}\printassignment','Required file missing'),
      ('repeat-render',start+r'\declareproblem{05}\printassignment\printassignment','Assignment already rendered'),
      ('duplicate-assignment',start+start,'Duplicate assignment ID'),
      ('bad-id',r'\assignment[id=bad.id,directory=x]{A}','IDs must contain'),
      ('table-label',r'\begin{mathtable}[label=t:bad]{c}x\\\end{mathtable}','requires a caption')]:
        cases.append(compile_case(name,body,error=message))
    env=r'''
\section{Environments}
\begin{theorem}[Named]\label{th:a}A theorem.\end{theorem}
\begin{lemma}\label{th:b}A lemma.\end{lemma}
\begin{corollary}A corollary.\end{corollary}
\begin{proposition}A proposition.\end{proposition}
\begin{conjecture}A conjecture.\end{conjecture}
\begin{algorithm}An algorithm.\end{algorithm}
\begin{definition}\label{def:a}DefinitionBody.\end{definition}
\begin{example}FirstWordExample.\end{example}
\begin{example}[Title]\label{ex:a}ExampleBody.\end{example}
\begin{remark}FirstWordRemark.\end{remark}
\begin{proof}ProofBody.\end{proof}
\begin{summary}SummaryBody.\end{summary}
\begin{note}NoteBody.\end{note}\begin{caveat}CaveatBody.\end{caveat}
\begin{warning}WarningBody.\end{warning}\begin{question}QuestionBody.\end{question}
\begin{speculation}SpeculationBody.\end{speculation}
\begin{formula}\label{formula:auto}a=b\end{formula}
\begin{formula}[Named formula]\label{formula:named}c=d\end{formula}
\begin{mathtable}[caption={FirstCaption},label=t:first,placement=H]{cc}
\tableheading{One}{Two}& B\\ \bottomrule\end{mathtable}
\begin{mathtable}[placement=H]{c}\text{SecondTable}\\\end{mathtable}
\cref{th:a,th:b,def:a,ex:a,formula:auto,formula:named,t:first}
\begin{subparts}\item First part.\item Second part.\end{subparts}
'''
    for cls in ['coursepsets','coursenotes','article']:
        cases.append(compile_case('environments-'+cls,env,cls=cls,checks=[require_text('FirstWordExample','FirstWordRemark','FirstCaption','SecondTable'),label('formula:auto','1'),label('formula:named','2')]))
        cases.append(compile_case('notation-'+cls,r'\input{tests/notation.tex}',cls=cls,
          checks=[font_backend('pazo' if cls=='coursepsets' else 'euler')] if cls!='article' else []))
        cases.append(compile_case('integral-sizes-'+cls,r'\input{tests/integral_sizes.tex}',cls=cls))
        cases.append(compile_case('bold-text-'+cls,r'''
The position is \mathbold{\mathrm{r}}; an expression is \mathbold{\alpha+r}.
\IfPackageLoadedTF{unicode-math}{
  \setbox0=\hbox{$\mathbold{\mathrm{r}}$}
  \setbox1=\hbox{$\symbfup{r}$}
  \ifdim\wd0=\wd1\else\errmessage{Upright bold alphabet lost}\fi
  \setbox0=\hbox{$\mathbold{\mathit{r}}$}
  \setbox1=\hbox{$\symbfit{r}$}
  \ifdim\wd0=\wd1\else\errmessage{Italic bold alphabet lost}\fi
}{}
''',cls=cls))
    for cls,profile in [('coursepsets','pagella'),('coursepsets','euler'),('coursenotes','pazo')]:
        cases.append(compile_case('font-'+cls+'-'+profile,r'\input{tests/notation.tex}',
          cls=cls,options='font-profile='+profile,checks=[font_backend(profile)]))
    for order in ['before','after']:
        cases.append(compile_case('pazo-'+order+'-notation',r'''
Outside mathematics: \mathbold{\alpha+\mathrm{r}}.
\setbox0=\hbox{$\mathbold{\alpha+\mathrm{r}}$}
\setbox1=\hbox{$\bm{\alpha+\mathrm{r}}$}
\ifdim\wd0=\wd1\else\errmessage{Pazo replaced the mathbold expression helper}\fi
''',cls='article',early_preamble=r'\usepackage{mathpazo}' if order=='before' else '',
          preamble=r'\usepackage{mathpazo}' if order=='after' else '',checks=[font_backend('pazo')]))
    cases.append(compile_case('integral-bad-size',r'$\integral[size=giant]{x}{x}{0}{1}$',error='Unknown integral size'))
    check_heading_spacing(OUT/'ordered/ordered.pdf')
    (OUT/'report.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(f'All {len(cases)} API cases passed.',flush=True)

if __name__=='__main__':main()
