import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('migrate',Path(__file__).resolve().parents[1]/'scripts/migrate.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class MigrationTests(unittest.TestCase):
    def test_nested_arguments_and_idempotence(self):
        before=r'\Int[t]{0}{\infty}{\p{\frac{a}{b}}+\Int[x]{1}{2}{x}}'
        after=r'\integral{\paren*{\frac{a}{b}}+\integral{x}{x}{1}{2}}{t}{0}{\infty}'
        self.assertEqual(m.migrate_text(before),after)
        self.assertEqual(m.migrate_text(after),after)
    def test_comments_escaped_percent_and_verbatim(self):
        before='% \\L and \\p{a}\n'+r'\verb|\L| \% \L(x\R) \begin{verbatim}\Int{x}\end{verbatim}'
        after='% \\L and \\p{a}\n'+r'\verb|\L| \% \left(x\right) \begin{verbatim}\Int{x}\end{verbatim}'
        self.assertEqual(m.migrate_text(before),after)
    def test_second_derivative_and_vectors(self):
        self.assertEqual(m.migrate_text(r'\fdl{f}{x}+\twovector{a}{\p{b}}'),r'\deriv[2]{f}{x}+\colvector[r]{a\\\paren*{b}}')
    def test_theorem_label_is_explicit(self):
        text=r'\begin{example}[A]{ex:a}Body\end{example}'
        result=r'\begin{example}[A]\label{ex:a}Body\end{example}'
        self.assertEqual(m.migrate_text(text),result)
        self.assertEqual(m.migrate_text(result),result)
    def test_table_caption(self):
        text=r'\begin{mathtable}[caption=true,title={A {nested} title},label={t:a}]{cc}x&y\end{mathtable}'
        result=r'\begin{mathtable}[caption={A {nested} title},label={t:a}]{cc}x&y\end{mathtable}'
        self.assertEqual(m.migrate_text(text),result)
        self.assertEqual(m.migrate_text(result),result)
    def test_inconsistent_declarations_rejected(self):
        with self.assertRaisesRegex(m.MigrationError,'Inconsistent'):
            m.migrate_assignment(r'\chap[1]{Title}\includeguide[A]{dir}{01}\includeproblem[B]{dir}{01}\end{document}')
    def test_unbalanced_rejected(self):
        with self.assertRaises(m.MigrationError):m.migrate_text(r'\Int[x]{0}{1}{x')

if __name__=='__main__':unittest.main()
