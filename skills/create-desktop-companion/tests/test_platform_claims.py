import importlib.util
from pathlib import Path
import unittest
import json
import subprocess
import sys
import tempfile
p = Path(__file__).resolve().parents[1] / 'scripts/check_platform_claims.py'
spec = importlib.util.spec_from_file_location('platform_claims', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PlatformClaims(unittest.TestCase):
    def test_unknown_capability_is_permitted(self):
        self.assertEqual(m.validate({'capabilities': {'blend': {'status': 'unknown'}}}), [])
    def test_unknown_cannot_be_advertised(self):
        self.assertTrue(m.validate({'capabilities': {'blend': {'status': 'unknown'}}, 'asserted_supported': ['blend']}))
    def test_support_requires_evidence(self):
        self.assertTrue(m.validate({'capabilities': {'blend': {'status': 'supported'}}}))
    def test_preview_does_not_need_installation(self):
        self.assertEqual(m.validate({'claims': {'displayable': True}, 'artifact_hash': 'fixture-sha', 'preview_evidence': 'decoded fixture'}), [])
    def test_failed_gate_cannot_be_exempted_by_diagnostic(self):
        r = dict(claims={'production_ready': True}, artifact_hash='fixture-sha', host_version='test-host', contract_evidence='test-schema', eligibility_evidence='test-preflight', mandatory_gates={'quality': 'fail'}, import_acceptance_gates={'content': 'pass'}, supplemental_diagnostic='suspected false-positive')
        self.assertTrue(m.validate(r))
        r['mandatory_gates']['quality'] = 'pass'
        self.assertEqual(m.validate(r), [])
    def test_installation_does_not_imply_active(self):
        r = dict(claims={'installed': True}, artifact_hash='fixture-sha', host_version='test-host', authorization_evidence='test-approval', installation_receipt='test-receipt')
        self.assertEqual(m.validate(r), [])
        r['claims']['active'] = True
        self.assertTrue(m.validate(r))
    def test_offline_observation_cannot_accept_runtime(self):
        r = dict(claims={'runtime_accepted': True}, artifact_hash='fixture-sha', host_version='test-host', runtime_observation='test-record', runtime_scope='idle only', runtime_limitations='other states untested', observation_mode='offline')
        self.assertTrue(m.validate(r))
        r['observation_mode'] = 'actual_client'
        self.assertEqual(m.validate(r), [])
    def test_missing_gates_not_vacuously_pass(self):
        self.assertTrue(m.validate({'claims': {'production_ready': True}, 'mandatory_gates': {}}))
    def test_truthy_strings_not_claims(self):
        self.assertTrue(m.validate({'claims': {'installed': 'false'}}))
    def test_unknown_claim_rejected(self):
        self.assertTrue(m.validate({'claims': {'perfect': True}}))

    def test_production_ready_does_not_certify_installed(self):
        r = dict(claims={'production_ready': True}, artifact_hash='fixture-sha', host_version='test-host', contract_evidence='test-schema', eligibility_evidence='structural-preflight', mandatory_gates={'quality': 'pass'})
        self.assertEqual(m.validate(r), [])
        r['claims']['installed'] = True
        self.assertTrue(m.validate(r))


    def test_nonobject_record_rejected(self):
        for value in (None, [], 'text', 12, True):
            with self.subTest(value=value):
                self.assertEqual(m.validate(value), ['record must be an object'])

    def test_capability_evidence_requires_nonempty_string(self):
        for status in ('supported', 'unsupported'):
            for evidence in (None, False, 0, [], {}, '', '   '):
                with self.subTest(status=status, evidence=evidence):
                    self.assertTrue(m.validate({'capabilities': {'blend': {'status': status, 'evidence': evidence}}}))
            self.assertEqual(m.validate({'capabilities': {'blend': {'status': status, 'evidence': 'actual source'}}}), [])

    def test_asserted_supported_requires_name_array(self):
        for value in (None, 'blend', {}, [None], [[]], ['']):
            with self.subTest(value=value):
                self.assertTrue(m.validate({'asserted_supported': value}))

    def test_cli_bad_json_and_root_are_structured_failures(self):
        with tempfile.TemporaryDirectory() as td:
            record = Path(td)/'record.json'
            for text in ('[]', 'null', '{invalid'):
                record.write_text(text)
                result = subprocess.run([sys.executable, str(p), str(record)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertFalse(json.loads(result.stdout)['ok'])
                self.assertNotIn('Traceback', result.stderr)
            result = subprocess.run([sys.executable, str(p), str(record.with_name('missing.json'))], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)['ok'])

    def test_capability_status_rejects_nonstring_values(self):
        for value in (None, [], {}, False, 1):
            with self.subTest(value=value):
                self.assertTrue(m.validate({'capabilities': {'blend': {'status': value, 'evidence': 'source'}}}))
