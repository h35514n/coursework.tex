"""Regression cases for the self-contained mechanics and thermal dialects."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import migrate_legacy as m
import regression as r

class LegacyMigrationTests(unittest.TestCase):
    def test_balanced_solution_and_comments(self):
        s=r'\problem[A {nested} title]Statement \solution{\frac{x}{\paren{y}} % } ignored'+'\n'+r'}'
        p=m.split_problems(s)[0]
        self.assertEqual(p['title'],'A {nested} title')
        self.assertIn(r'\frac{x}{\paren{y}}',p['solution'])
        self.assertIn('% } ignored',p['solution'])
    def test_mixed_imports_and_empty_solution(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'p.tex').write_text(r'\problem[B]Second\solution{\input{s}}')
            (root/'s.tex').write_text('Nested {solution}')
            used={};s=m.expand_inputs(r'\problem First\solution{}\input{p}',root,used)
            problems=m.split_problems(s)
            self.assertEqual(len(problems),2);self.assertTrue(problems[0]['empty_solution'])
            self.assertEqual(problems[1]['solution'],'Nested {solution}')
            self.assertEqual(set(used),{'p.tex','s.tex'})
    def test_missing_and_cyclic_imports_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with self.assertRaisesRegex(m.MigrationError,'Missing'):m.expand_inputs(r'\input{absent}',root,{})
            (root/'a.tex').write_text(r'\input{a}')
            with self.assertRaisesRegex(m.MigrationError,'Cyclic'):m.expand_inputs(r'\input{a}',root,{})
    def test_sum_dialects_preserve_bounds(self):
        self.assertEqual(m.migrate_notation(r'\Sum{i=0}{\infty}',notes=True),r'\sum_{i=0}^{\infty}')
        self.assertEqual(m.migrate_notation(r'\Sum[i]{0}{\infty}'),r'\sum_{i=0}^{\infty}')
    def test_held_variables_and_simple_derivatives(self):
        text=r'\diffp{V}{T}[p]+\diff[2]{x}{t}+\diffp{F}{x}+\diffp{f}{x,y}'
        result=r'\diffp{V}{T}[p]+\deriv[2]{x}{t}+\pderiv{F}{x}+\diffp{f}{x,y}'
        self.assertEqual(m.migrate_notation(text),result)
        self.assertEqual(m.migrate_notation(result),result)
    def test_native_notes_environment_keeps_braced_body(self):
        text=r'\begin{example}[Title]{First words} remain.\end{example}'
        self.assertEqual(m.migrate_notation(text,notes=True),text)
        self.assertEqual(m.migrate_notation(r'\begin{definition}[T]{def:a}Text',notes=True),r'\begin{definition}[T]\label{def:a}Text')
    def test_distinct_problem_labels_with_local_references(self):
        files={'homework/01-pset/solution01.tex':r'\label{eq:a}\eqref{eq:a}',
               'homework/01-pset/solution02.tex':r'\label{eq:a}\eqref{eq:a}',
               'homework/01-pset/problem02.tex':r'\eqref{eq:a}'}
        report=m.qualify_labels(files)
        self.assertIn(r'\label{eq:01-pset:01:a}',files['homework/01-pset/solution01.tex'])
        self.assertEqual(files['homework/01-pset/problem02.tex'],r'\eqref{eq:01-pset:02:a}')
        self.assertEqual(len(report),5)
    def test_ambiguous_reference_rejected(self):
        with self.assertRaisesRegex(m.MigrationError,'Ambiguous'):
            m.qualify_labels({'homework/a/solution01.tex':r'\label{eq:a}',
                              'homework/a/solution02.tex':r'\label{eq:a}',
                              'homework/b/problem01.tex':r'\ref{eq:a}'})
    def test_notes_labels_independent_of_homework(self):
        files={'homework/a/solution01.tex':r'\label{eq:a}', 'notes/x.tex':r'\label{eq:a}'}
        self.assertEqual(m.qualify_labels(files),[])
    def test_archived_guides_excluded(self):
        import subprocess
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);subprocess.run(['git','init','-q',str(root)],check=True)
            (root/'handouts').mkdir();(root/'handouts/guide.tex').write_text(r'\problem Legacy guide')
            (root/'main.tex').write_text('active')
            subprocess.run(['git','-C',str(root),'add','.'],check=True)
            self.assertEqual(m.read_active(root),{'main.tex':'active'})
    def test_unknown_trailing_content_rejected(self):
        with self.assertRaisesRegex(m.MigrationError,'outside solution'):
            m.split_problems(r'\problem A\solution{B}Unknown narrative')
    def test_physics_cross_preserves_bold_symbol(self):
        self.assertEqual(m.migrate_notation(r'\omega \cross r'),r'\omega \mathbold{\times} r')

    def test_known_legacy_todo_is_retained(self):
        p=m.split_problems(r'\problem A\solution{B}TODO')[0]
        self.assertIn('TODO',p['statement']);self.assertEqual(p['trailing_annotation'],'TODO')

class LegacySnapshotTests(unittest.TestCase):
    def test_relocation_and_corruption_do_not_use_original_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);old=root/'old';classes=old/'classes';classes.mkdir(parents=True)
            (classes/'problemsets.cls').write_text('original');(classes/'notes.cls').write_text('notes')
            manifest={'mode':'baseline','legacy_classes':True,'frozen_fixtures':True,
                      'class_directory':str(classes),'class_files':r.class_files(classes),
                      'testbed':{'files':{}},'pdfs':{}}
            encoded=json.dumps(manifest).encode();(old/'manifest.json').write_bytes(encoded)
            moved=root/'moved';old.rename(moved);r.check_integrity(moved,manifest)
            self.assertEqual((moved/'manifest.json').read_bytes(),encoded)
            classes.mkdir(parents=True);(classes/'problemsets.cls').write_text('original')
            (moved/'classes/problemsets.cls').write_text('corrupt')
            with self.assertRaisesRegex(RuntimeError,'snapshot changed'):r.check_integrity(moved,manifest)
            shutil.rmtree(moved/'classes')
            with self.assertRaisesRegex(RuntimeError,'snapshot missing'):r.check_integrity(moved,manifest)
    def test_legacy_recorder_rejects_fixture_shadow(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);recorder=root/'x.fls';selected=root/'classes'
            recorder.write_text('INPUT '+str(selected/'problemsets.cls')+'\n')
            self.assertEqual(r.verify_recorder(recorder,selected,root,legacy=True),['problemsets.cls'])
            recorder.write_text('INPUT problemsets.cls\n')
            with self.assertRaisesRegex(RuntimeError,'loaded'):
                r.verify_recorder(recorder,selected,root,legacy=True)

if __name__=='__main__':unittest.main()
