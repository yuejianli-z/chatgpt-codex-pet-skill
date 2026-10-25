"""Check structured motion-cue applicability, not artwork or free-text prompts."""
import argparse
import json
from pathlib import Path

FACIAL_FEATURES = frozenset(('face', 'face_surface', 'eyes', 'pupils', 'nose', 'nose_tip', 'mouth', 'eyebrows'))

STRUCTURAL_FEATURES = frozenset(('body_axis', 'head_offset', 'connected_arm', 'torso_lean', 'support_point', 'tail', 'wing', 'wheel', 'pointer'))
FEATURE_KEYS = FACIAL_FEATURES | STRUCTURAL_FEATURES


def validate(data):
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get('actors'), list) or not data['actors']:
        return ['actors must be a nonempty array']
    actors = {}
    for i, actor in enumerate(data['actors']):
        label = f'actors[{i}]'
        if not isinstance(actor, dict):
            errors.append(f'{label} must be an object')
            continue
        aid = actor.get('id')
        if not isinstance(aid, str) or not aid.strip() or aid in actors:
            errors.append(f'{label}.id must be nonempty and unique')
            continue
        actors[aid] = actor
        if 'has_face' not in actor or not (actor['has_face'] is None or type(actor['has_face']) is bool):
            errors.append(f'{label}.has_face must be true, false, or null (unknown)')
        features = actor.get('features')
        if not isinstance(features, dict):
            errors.append(f'{label}.features must be an object')
            continue
        for name, value in features.items():
            if name not in FEATURE_KEYS:
                errors.append(f'{label}: unknown feature key {name}; map to documented canonical vocabulary')
            if not isinstance(name, str) or not name.strip() or not (value is None or type(value) is bool):
                errors.append(f'{label}.features values must be true, false, or null')
            if actor.get('has_face') is False and name in FACIAL_FEATURES and value is True:
                errors.append(f'{label}: faceless actor cannot declare facial feature {name}')
    cues = data.get('cues')
    if not isinstance(cues, list) or not cues:
        errors.append('cues must be a nonempty array')
        return errors
    for i, cue in enumerate(cues):
        label = f'cues[{i}]'
        if not isinstance(cue, dict):
            errors.append(f'{label} must be an object')
            continue
        aid = cue.get('actor_id')
        if not isinstance(aid, str) or aid not in actors:
            errors.append(f'{label}.actor_id must resolve to one actor')
            continue
        actor = actors[aid]
        if not isinstance(cue.get('signal'), str) or not cue['signal'].strip():
            errors.append(f'{label}.signal must describe a readable signal')
        req = cue.get('required_features')
        if not isinstance(req, list) or not req or any(not isinstance(x, str) or not x.strip() for x in req):
            errors.append(f'{label}.required_features must be a nonempty list of feature names')
            continue
        features = actor.get('features', {})
        if not isinstance(features, dict):
            continue
        for feature in req:
            if feature not in FEATURE_KEYS:
                errors.append(f'{label}: unknown required feature key {feature}')
                continue
            if actor.get('has_face') is False and feature in FACIAL_FEATURES:
                errors.append(f'{label}: {feature} is inapplicable to a faceless actor')
            elif features.get(feature) is not True:
                errors.append(f'{label}: {feature} is absent or unverified on actor {aid}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.plan.read_text()))
    except (ValueError, OSError) as exc:
        errors = [str(exc)]
    print(json.dumps({'ok': not errors, 'errors': errors, 'scope': 'structured applicability only; no free-text, identity, motion or runtime verdict', 'authorizes_upload': False}, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
