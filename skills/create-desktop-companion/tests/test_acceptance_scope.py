import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('scope', Path(__file__).resolve().parents[1] / 'scripts/check_acceptance_scope.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def complete():
    return {'claim': 'fully_accepted', 'required_directions': [str(i) for i in range(16)], 'tested_directions': [str(i) for i in range(16)], 'gates': {k: {'status': 'pass', 'evidence': 'Synthetic test record, not production evidence'} for k in m.GATES}}


class AcceptanceScope(unittest.TestCase):
    def test_complete_synthetic_record(self):
        self.assertEqual(m.validate(complete()), [])

    def test_four_cardinals_cannot_pass_full_coverage(self):
        p = complete(); p['tested_directions'] = ['0', '4', '8', '12']
        self.assertTrue(m.validate(p))

    def test_repeating_four_cardinals_does_not_make_sixteen(self):
        p = complete(); p['tested_directions'] = ['0', '4', '8', '12'] * 4
        self.assertTrue(m.validate(p))

    def test_partial_diagnostic_can_be_honestly_recorded(self):
        p = complete(); p['claim'] = 'partial_diagnostic'; p['tested_directions'] = ['0', '4', '8', '12']
        p['gates']['full_coverage']['status'] = 'not_run'
        p['gates']['actual_runtime']['status'] = 'unknown'
        self.assertEqual(m.validate(p), [])

    def test_geometry_pass_cannot_override_identity_failure(self):
        p = complete(); p['gates']['identity']['status'] = 'fail'
        self.assertTrue(m.validate(p))

    def test_direction_semantics_are_independent(self):
        p = complete(); p['gates']['direction_semantics']['status'] = 'fail'
        self.assertTrue(m.validate(p))

    def test_unknown_runtime_cannot_be_fully_accepted(self):
        p = complete(); p['gates']['actual_runtime']['status'] = 'unknown'
        self.assertTrue(m.validate(p))

    def test_missing_evidence_fails(self):
        p = complete(); p['gates']['geometry']['evidence'] = ''
        self.assertTrue(m.validate(p))

    def test_wrong_direction_set_fails(self):
        p = complete(); p['tested_directions'][-1] = 'unexpected'
        self.assertTrue(m.validate(p))

    def test_malformed_input_is_reported(self):
        for p in [None, {}, {'gates': None}, {'required_directions': [{}], 'tested_directions': [0], 'gates': {}}]:
            with self.subTest(p=p): self.assertTrue(m.validate(p))
