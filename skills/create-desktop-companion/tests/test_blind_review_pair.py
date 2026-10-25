import hashlib
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / 'scripts/check_blind_review_pair.py'
spec = importlib.util.spec_from_file_location('blind_pair', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class BlindPairTests(unittest.TestCase):
    def setUp(self):
        self.board, self.key = b'original board', b'original key'
        self.review = {'board_sha256': hashlib.sha256(self.board).hexdigest(),
                       'key_sha256': hashlib.sha256(self.key).hexdigest()}

    def test_original_pair_matches(self):
        self.assertEqual(module.verify_pair(self.board, self.key, self.review), [])

    def test_new_randomized_board_rejects_old_review(self):
        self.assertTrue(module.verify_pair(b'new board', self.key, self.review))

    def test_new_key_or_missing_binding_rejected(self):
        self.assertTrue(module.verify_pair(self.board, b'new key', self.review))
        self.assertTrue(module.verify_pair(self.board, self.key, {}))
