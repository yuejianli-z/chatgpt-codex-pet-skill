import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('ledger', Path(__file__).parents[1] / 'scripts/check_learning_ledger.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sample():
    return {'entries': [{'id': 'x', 'case': 'example', 'stage': 'extract', 'input_evidence': ['source frame'], 'failure': 'hole', 'hypothesis': 'fringe', 'bounded_change': 'one local cleanup', 'verification': [{'kind': 'machine', 'result': 'pass', 'evidence': 'pixel comparison'}], 'generalization': 'trace source first', 'generalization_status': 'supported_within_case', 'status': 'observed', 'regression_tests': [{'kind': 'manual', 'reference': 'inspect original alpha', 'status': 'not_run'}]}]}


class LedgerTests(unittest.TestCase):
    def test_valid_observation(self):
        self.assertEqual(module.validate(sample()), [])

    def test_missing_evidence(self):
        d = sample(); d['entries'][0]['input_evidence'] = []
        self.assertTrue(module.validate(d))

    def test_no_false_tested_claim(self):
        d = sample(); d['entries'][0]['status'] = 'untested'
        self.assertTrue(module.validate(d))

    def test_observed_requires_execution(self):
        d = sample(); d['entries'][0]['verification'][0]['result'] = 'not_run'
        self.assertTrue(module.validate(d))

    def test_unexecuted_manual_is_not_machine_pass(self):
        d = sample(); d['entries'][0]['status'] = 'untested'; d['entries'][0]['verification'][0]['result'] = 'not_run'
        self.assertEqual(module.validate(d), [])

    def test_duplicate_ids(self):
        d = sample(); d['entries'].append(copy.deepcopy(d['entries'][0]))
        self.assertTrue(module.validate(d))

    def test_missing_regression_reference(self):
        d = sample(); d['entries'][0]['regression_tests'][0]['reference'] = ''
        self.assertTrue(module.validate(d))

    def test_failure_is_valid_evidence(self):
        d = sample(); d['entries'][0]['verification'][0]['result'] = 'fail'
        self.assertEqual(module.validate(d), [])

    def test_bad_root(self):
        self.assertTrue(module.validate([]))
