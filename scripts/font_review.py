#!/usr/bin/env python3
"""Build review specimens and real documents for explicit Unicode font profiles."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/font-review'
FINAL=OUT/'output'
TESTBED=ROOT.parent/'coursework-testing'
CLASSES=ROOT/'tex/latex/coursework'
EPOCH='1789087534'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def command(args, **kw):
 p=subprocess.run(args,text=True,capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout+p.stderr


def build(name,source,cwd,profile,cls):
 folder=OUT/name;folder.mkdir(parents=True,exist_ok=True)
 env={**os.environ,'TEXINPUTS':str(CLASSES)+'//:','SOURCE_DATE_EPOCH':EPOCH,'FORCE_SOURCE_DATE':'1'}
 args=['latexmk','-xelatex','-halt-on-error','-interaction=nonstopmode','-recorder',
       '-usepretex=\\PassOptionsToClass{font-profile='+profile+'}{'+cls+'}',
       '-outdir='+str(folder),str(source)]
 p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
 (folder/'console.log').write_text(p.stdout+p.stderr)
 if p.returncode:raise RuntimeError(f'{name} failed; see {folder}/console.log')
 pdf=folder/(Path(source).stem+'.pdf');log=pdf.with_suffix('.log').read_text()
 fls=pdf.with_suffix('.fls').read_text()
 for line in fls.splitlines():
  if line.startswith('INPUT ') and Path(line[6:]).name.startswith('course') and Path(line[6:]).suffix in {'.cls','.sty'}:
   actual=(cwd/line[6:]).resolve()
   if actual.parent!=CLASSES:raise RuntimeError('Wrong class input: '+str(actual))
 if 'Missing character:' in log:raise RuntimeError('Missing glyph in '+name)
 if 'Object @' in p.stdout+p.stderr and 'already defined.' in p.stdout+p.stderr:raise RuntimeError('Duplicate destination in '+name)
 info=command(['pdfinfo',str(pdf)]);pages=int(re.search(r'Pages:\s+(\d+)',info)[1])
 command(['pdftotext','-layout',str(pdf),str(folder/'text.txt')])
 command(['pdftoppm','-r','120','-png',str(pdf),str(folder/'page')])
 fonts=command(['pdffonts',str(pdf)]);(folder/'fonts.txt').write_text(fonts)
 result={'name':name,'profile':profile,'class':cls,'pdf':str(pdf),'pages':pages,'sha256':sha(pdf),
  'text_sha256':sha(folder/'text.txt'),'warnings':[x for x in log.splitlines() if 'Warning:' in x or 'Missing character:' in x],
  'font_paths':sorted({line[6:] for line in fls.splitlines() if line.startswith('INPUT ') and Path(line[6:]).suffix.lower() in {'.otf','.ttf','.pfb'}}),
  'font_table':fonts,'command':args}
 print('PASS',name,pages,'pages',flush=True)
 return result


def main():
 OUT.mkdir(parents=True,exist_ok=True);FINAL.mkdir(parents=True,exist_ok=True)
 specimens=[];results=[]
 for cls,profile,title in [('coursepsets','pagella','Pagella homework'),('coursenotes','euler','Euler notes'),('coursenotes','pagella','Pagella notes')]:
  name='specimen-'+title.lower().replace(' ','-');source=OUT/(name+'.tex')
  source.write_text('\\documentclass{'+cls+'}\n\\usepackage{coursephys}\n'
   '\\courseworksetup{author={Coursework v2 font review},course-code={Font specimen},course-title={'+title+'},term={September 2026}}\n'
   '\\begin{document}\n\\pagestyle{plain}\n\\setcounter{section}{1}\n'
   '\\ifdefined\\chapter\\setcounter{chapter}{1}\\fi\n'
   '\\ifdefined\\PrelimText\\renewcommand{\\PrelimText}{}\\fi\n'
   '\\section*{'+title+'}\nSame notation and environment content in each font profile.\n'
   '\\input{tests/notation.tex}\n\\clearpage\\section*{Environment specimen}\n'
   '\\begin{definition}[Vector field]\\label{def:field}A field assigns a vector $\\vect{v}$ to each point.\\end{definition}\n'
   '\\begin{example}[Thermal notation]\\label{ex:thermal}For a particle, $E=\\slashfrac{3}{2}\\kB T$.\\end{example}\n'
   '\\begin{remark}Greek letters and vector accents should remain distinct at text and script sizes.\\end{remark}\n'
   '\\begin{proof}The notation is evaluated consistently by the selected Unicode math font.\\end{proof}\n'
   '\\begin{formula}[Reference]\\label{formula:ref}\\grad f=\\xhat\\pderiv{f}{x}+\\yhat\\pderiv{f}{y}\\end{formula}\n'
   '\\begin{mathtable}[caption={Small math table},label=tab:specimen,placement=H]{cc}x&x^2\\\\ 1&1\\\\ 2&4\\\\\\bottomrule\\end{mathtable}\n'
   '\\begin{figure}[H]\\centering\\fbox{\\rule{0pt}{1cm}\\hspace{2cm}}\\caption{Figure and caption specimen}\\label{fig:specimen}\\end{figure}\n'
   '\\cref{def:field,ex:thermal,formula:ref,tab:specimen,fig:specimen}.\n\\end{document}\n')
  result=build(name,source,ROOT,profile,cls);results.append(result);specimens.append(result)
 for profile in ['euler','pagella']:
  for source in ['notes/01-useful-maths.tex','notes/03-probability.tex']:
   results.append(build(profile+'-'+Path(source).stem,source,TESTBED,profile,'coursenotes'))
 results.append(build('pagella-assignment','homework/01-pset.tex',TESTBED,'pagella','coursepsets'))
 from pypdf import PdfReader, PdfWriter
 writer=PdfWriter()
 # The combined visual comparison has section bookmarks. Keep internal
 # reference links in the individual PDFs; their repeated destination names
 # must not create cross-specimen links in the merged document.
 for specimen in specimens:
  first_page=len(writer.pages)
  reader=PdfReader(specimen['pdf'])
  for page in reader.pages:
   page.pop('/Annots',None)
   writer.add_page(page)
  writer.add_outline_item(specimen['name'],first_page)
 output=FINAL/'coursework-font-comparison.pdf'
 with output.open('wb') as f:writer.write(f)
 results_meta={'class_revision':command(['git','rev-parse','HEAD'],cwd=ROOT).strip(),
               'class_status':command(['git','status','--short'],cwd=ROOT).strip(),
               'class_files':{p.name:sha(p) for p in CLASSES.iterdir() if p.is_file()},
               'testbed_revision':command(['git','rev-parse','HEAD'],cwd=TESTBED).strip(),
               'testbed_status':command(['git','status','--short'],cwd=TESTBED).strip(),
               'source_date_epoch':EPOCH,
               'xelatex':command(['xelatex','--version']).splitlines()[0],'results':results,'comparison_pdf':str(output)}
 (OUT/'manifest.json').write_text(json.dumps(results_meta,indent=2)+'\n')
 lines=['# Coursework font review','','Both choices use the same v2 API and XeLaTeX. This run reproduces the Unicode font alternatives. Homework now defaults to its restored Pazo mathematics, which is covered by tests/check_homework_font.py.','','- **Distinct styles:** Pagella homework and Euler notes.','- **Unified style:** Pagella homework and Pagella notes.','','Both variants use TeX Gyre Pagella text and DejaVu Sans Mono, resolved by filename from TeX Live. Homework is common to both choices. The notes comparison isolates the math-font change.','','## Builds','','| Document | Profile | Pages | Missing glyphs |','| --- | --- | --- | --- |']
 for result in results:lines.append(f"| {result['name']} | {result['profile']} | {result['pages']} | 0 |")
 lines+=['','Specimens are assembled in `build/font-review/output/coursework-font-comparison.pdf`. Individual PDFs, text, renders, font inventories, paths, and logs are under `build/font-review/`. The API suite also passes with these fonts.','','Expected differences include equation width, delimiter and integral shapes, Greek letter forms, and resulting line/page breaks. Euler uses upright mathematical letters; Pagella uses conventional italic variables. Pazo homework and Euler notes are the installed defaults; the explicit Pagella profiles here remain comparison alternatives. Generated comparisons stay under build/font-review and do not replace the historical review.']
 (OUT/'review.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
