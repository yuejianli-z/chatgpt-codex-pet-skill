"""Isolated packaging invariants; these are not browser rendering tests."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'tools' / 'state-tester'

class StateTesterBuild(unittest.TestCase):
    def test_public_build_is_reproducible_art_free(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ('build.py', 'index.html', 'tester.js'):
                shutil.copyfile(SOURCE / name, root / name)
            subprocess.run([sys.executable, str(root / 'build.py')], check=True, capture_output=True)
            output = (root / 'standalone.html').read_bytes()
            self.assertEqual(output, (SOURCE / 'standalone.html').read_bytes())
            self.assertNotIn(b'embeddedBytes', output)
            self.assertNotIn(b'<script src=', output)

    def test_private_atlas_cannot_implicitly_replace_public_default(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ('build.py', 'index.html', 'tester.js'):
                shutil.copyfile(SOURCE / name, root / name)
            public = root / 'standalone.html'
            public.write_text('preserve public')
            atlas = root / 'fixture.png'
            atlas.write_bytes(b'synthetic test bytes')
            result = subprocess.run([sys.executable, str(root / 'build.py'), '--atlas', str(atlas)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(public.read_text(), 'preserve public')
            result = subprocess.run([sys.executable, str(root / 'build.py'), '--atlas', str(atlas), '--output', str(public)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(public.read_text(), 'preserve public')

    def test_case_insensitive_script_ending_is_escaped(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shutil.copyfile(SOURCE / 'build.py', root / 'build.py')
            (root / 'index.html').write_text('<script src="tester.js"></script>')
            (root / 'tester.js').write_text('const sample = "</ScRiPt>";')
            subprocess.run([sys.executable, str(root / 'build.py')], check=True, capture_output=True)
            html = (root / 'standalone.html').read_text()
            self.assertEqual(html.lower().count('</script>'), 1)
            self.assertIn('<\\/script>', html.lower())
