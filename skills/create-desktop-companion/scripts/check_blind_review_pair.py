"""Check immutable blind-review pairing; does not judge visual directions."""
import hashlib


def verify_pair(board_bytes, key_bytes, review):
    """review must bind the exact board and answer key actually reviewed."""
    errors = []
    for field, payload in [('board_sha256', board_bytes), ('key_sha256', key_bytes)]:
        actual = hashlib.sha256(payload).hexdigest()
        if review.get(field) != actual:
            errors.append(field + ': missing or mismatched; do not reuse verdict')
    return errors
