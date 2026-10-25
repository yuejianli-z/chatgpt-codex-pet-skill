import unittest,json,sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))
from check_manifest import check
class ManifestBridgeTests(unittest.TestCase):
    def setUp(self):self.d=json.loads((Path(__file__).parents[1]/'examples/geometry-coverage.json').read_text())
    def test_real_example_bridge(self):self.assertEqual(check(self.d),[])
    def test_placeholder_template_fails(self):
        self.assertTrue(check(json.loads((Path(__file__).parents[1]/'templates/completeness-manifest.example.json').read_text())))
    def test_missing_schedule_is_not_complete(self):
        self.d['preview_schedule']['row_schedules']={};self.assertTrue(check(self.d))
