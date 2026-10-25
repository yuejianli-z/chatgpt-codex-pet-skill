import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_package.py'
spec = importlib.util.spec_from_file_location('check_package', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PackageIntegrity(unittest.TestCase):
    def fixture(self, root):
        (root / 'scripts').mkdir()
        for name in ['SKILL.md', 'VERSION', 'requirements.txt', 'scripts/preflight.py']:
            (root / name).write_text('fixture')
        (root / 'public-export-allowlist.json').write_text(json.dumps({
            'allowed_roots': ['SKILL.md', 'VERSION', 'requirements.txt', 'scripts', 'public-export-allowlist.json'],
            'allowed_binary_assets': []}))

    def run_case(self, change):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            change(root)
            return m.validate(root)

    def test_complete_self_contained_fixture_passes(self):
        self.assertTrue(self.run_case(lambda root: None)['ok'])

    def test_missing_relative_link_fails(self):
        self.assertFalse(self.run_case(lambda root: (root / 'SKILL.md').write_text('[Missing](absent.md)'))['ok'])

    def test_parent_dependency_fails(self):
        self.assertFalse(self.run_case(lambda root: (root / 'SKILL.md').write_text('[Outside](../README.md)'))['ok'])

    def test_character_binary_fails(self):
        self.assertFalse(self.run_case(lambda root: (root / 'scripts/character.png').write_bytes(b'\x89PNG\x00\xff'))['ok'])

    def test_cache_fails(self):
        self.assertFalse(self.run_case(lambda root: (root / 'scripts/__pycache__').mkdir())['ok'])

    def test_symlink_fails(self):
        self.assertFalse(self.run_case(lambda root: (root / 'scripts/alias').symlink_to(root / 'SKILL.md'))['ok'])
