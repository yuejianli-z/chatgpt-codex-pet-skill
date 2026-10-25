import importlib.util,tempfile,unittest
from pathlib import Path

def load(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).parents[1]/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class PortabilityTests(unittest.TestCase):
    def test_preflight_does_not_invent_provider_or_host(self):
        c=load('preflight').capabilities();self.assertEqual(c['image_generation']['status'],'unknown');self.assertEqual(c['host_import']['status'],'unknown')
    def test_real_geometry_gif_roundtrip_and_no_overwrite(self):
        m=load('make_test_fixture')
        with tempfile.TemporaryDirectory()as d:
            r=m.create_fixture(d);self.assertEqual(r['decoded_holds_ms'],[100,200,300]);self.assertEqual(r['duration_ms'],600)
            with self.assertRaises(FileExistsError):m.create_fixture(d)
