"""Machine-checkable repair scope/timing, never visual identity or comfort."""
from fractions import Fraction
import hashlib


def phase(durations, time_ms):
    if not durations or any(type(d) is not int or d <= 0 for d in durations):
        raise ValueError('positive integer durations required')
    t = time_ms % sum(durations)
    for i, d in enumerate(durations):
        if t < d:
            return i
        t -= d


def validate_schedule(rows, master_ms):
    errors = []
    if not isinstance(rows, dict) or not rows:
        return ['nonempty row schedules required']
    if type(master_ms) is not int or master_ms <= 0:
        return ['positive integer master period required']
    for name, ds in rows.items():
        try:
            phase(ds, 0)
        except ValueError:
            errors.append(name + ': invalid durations'); continue
        if master_ms % sum(ds):
            errors.append(name + ': period does not divide master')
        elif phase(ds, master_ms - 1) != len(ds) - 1 or phase(ds, master_ms) != 0:
            errors.append(name + ': terminal successor mismatch')
    return errors


def validate_encoded_end(duration_ms, pts_ms, holds_ms):
    """Use decoded timestamps/durations, not requested encoder parameters."""
    if not pts_ms or len(pts_ms) != len(holds_ms):
        return ['decoded timeline is missing or mismatched']
    pts = [Fraction(str(x)) for x in pts_ms]
    holds = [Fraction(str(x)) for x in holds_ms]
    errors = []
    if pts[0] != 0 or any(h <= 0 for h in holds):
        errors.append('nonzero start or nonpositive hold')
    if any(pts[i] + holds[i] != pts[i+1] for i in range(len(pts)-1)):
        errors.append('timestamp gap or overlap')
    if pts[-1] + holds[-1] != duration_ms:
        errors.append('terminal duration mismatch')
    return errors


def changed_cells(approved_bytes, current_bytes, approved_sha256):
    """Validate baseline provenance and return every changed cell; no likeness verdict."""
    if len(approved_bytes) != len(current_bytes) or len(approved_bytes) != len(approved_sha256):
        raise ValueError('cell counts differ')
    if [hashlib.sha256(b).hexdigest() for b in approved_bytes] != approved_sha256:
        raise ValueError('approved reference hashes do not match')
    return [i for i, (a, b) in enumerate(zip(approved_bytes, current_bytes)) if a != b]


def validate_identity_review(changes, review):
    """Require scoped human-review evidence, never verify its visual truth."""
    errors = []
    if not changes:
        return errors
    if set(review.get('changed_cells', [])) != set(changes):
        errors.append('review must cover every changed cell, not unchanged cells')
    for field in ['approved_reference', 'same_view_comparison', 'native_size_evidence',
                  'enlarged_evidence', 'ratio_landmarks', 'eye_mouth_silhouette', 'reviewer']:
        if not review.get(field): errors.append('missing ' + field)
    if review.get('verdict') != 'pass': errors.append('identity review not passed')
    return errors


def translation_only(source_rgba, result_rgba, dx, dy):
    """Exact integer translation proof; transparent padding may differ in hidden RGB.
    This establishes preserved visible RGBA pixels without clipping, not whole-cell equality.
    """
    if source_rgba.size != result_rgba.size: return False
    w, h = source_rgba.size
    expected = {}
    for y in range(h):
        for x in range(w):
            px = source_rgba.getpixel((x, y))
            if px[3]:
                nx, ny = x+dx, y+dy
                if not (0 <= nx < w and 0 <= ny < h): return False
                expected[(nx, ny)] = px
    actual = {(x, y): result_rgba.getpixel((x, y)) for y in range(h) for x in range(w)
              if result_rgba.getpixel((x, y))[3]}
    return actual == expected


def validate_coverage(requirements, delivered, required_body_roles=(), body_views=()):
    """Dynamic host coverage. A direction pose is not an animation."""
    errors = []
    for key, required in requirements.items():
        item = delivered.get(key, {})
        if item.get('kind') != required['kind']: errors.append(key + ': kind mismatch')
        if item.get('source_indices') != list(range(required['frames'])):
            errors.append(key + ': missing, reordered or extra source indices')
        durations = item.get('durations_ms', [])
        if required['kind'] == 'animation' and (len(durations) != required['frames'] or any(type(x) is not int or x <= 0 for x in durations)):
            errors.append(key + ': missing source-index timing')
    if set(delivered) != set(requirements): errors.append('unexpected/missing requirement key')
    if set(required_body_roles) != {v.get('role') for v in body_views} or len(body_views) != len(required_body_roles):
        errors.append('missing or duplicate body roles')
    for v in body_views:
        if v.get('evidence_kind') not in ('observed', 'inferred', 'proposed') or not v.get('source'):
            errors.append('body evidence missing')
    return errors


def can_start_batch(case_id, style_version, approval):
    """Scope-record check only. Caller must authenticate actual user evidence."""
    if not approval.get('evidence'):
        return False
    if approval.get('case_id') != case_id or approval.get('style_version') != style_version:
        return False
    return approval.get('basis') in ('user_style_choice', 'explicit_case_style_waiver', 'unchanged_approved_baseline')
