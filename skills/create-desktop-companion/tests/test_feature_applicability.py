import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('applicability', Path(__file__).resolve().parents[1] / 'scripts/check_feature_applicability.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def plan():
    return {'actors': [{'id': 'object', 'has_face': False, 'features': {'body_axis': True, 'pupils': False, 'nose_tip': False}}], 'cues': [{'actor_id': 'object', 'signal': 'tilt body axis toward target', 'required_features': ['body_axis']}]}


class FeatureApplicability(unittest.TestCase):
    def test_faceless_body_cue_passes(self):
        self.assertEqual(m.validate(plan()), [])
    def test_pupil_template_leakage_rejected(self):
        p = plan(); p['cues'][0]['required_features'] = ['pupils']
        self.assertTrue(m.validate(p))
    def test_nose_template_leakage_rejected(self):
        p = plan(); p['cues'][0]['required_features'] = ['nose_tip']
        self.assertTrue(m.validate(p))
    def test_unknown_is_not_present(self):
        p = plan(); p['actors'][0]['features']['body_axis'] = None
        self.assertTrue(m.validate(p))
    def test_other_actors_feature_cannot_leak(self):
        p = plan(); p['actors'].append({'id': 'face', 'has_face': True, 'features': {'pupils': True}})
        p['cues'][0]['required_features'] = ['pupils']
        self.assertTrue(m.validate(p))
        p['cues'][0]['actor_id'] = 'face'
        self.assertEqual(m.validate(p), [])
    def test_false_string_is_not_boolean(self):
        p = plan(); p['actors'][0]['has_face'] = 'false'
        self.assertTrue(m.validate(p))
    def test_faceless_contradiction_rejected(self):
        p = plan(); p['actors'][0]['features']['pupils'] = True
        self.assertTrue(m.validate(p))
    def test_empty_and_malformed_fail(self):
        for p in ({}, {'actors': []}, {'actors': [None]}, {'actors': [{}]}, {'actors': [{'id':'a','has_face':False,'features':[]}], 'cues':[{}]}):
            self.assertTrue(m.validate(p))
    def test_unknown_actor_rejected(self):
        p = plan(); p['cues'][0]['actor_id'] = 'missing'
        self.assertTrue(m.validate(p))
    def test_missing_feature_declaration_fails(self):
        p = plan(); p['actors'][0]['features'] = {}
        self.assertTrue(m.validate(p))

    def test_face_surface_alias_rejected(self):
        p = plan(); p['actors'][0]['features']['face_surface'] = True
        p['cues'][0]['required_features'] = ['face_surface']
        self.assertTrue(m.validate(p))
    def test_face_alias_rejected(self):
        p = plan(); p['actors'][0]['features']['face'] = True
        p['cues'][0]['required_features'] = ['face']
        self.assertTrue(m.validate(p))
    def test_nose_alias_rejected(self):
        p = plan(); p['actors'][0]['features']['nose'] = True
        p['cues'][0]['required_features'] = ['nose']
        self.assertTrue(m.validate(p))

    def test_unknown_synonym_true_does_not_bypass(self):
        p = plan(); p['actors'][0]['features']['snout_surface'] = True
        p['cues'][0]['required_features'] = ['snout_surface']
        self.assertTrue(m.validate(p))
