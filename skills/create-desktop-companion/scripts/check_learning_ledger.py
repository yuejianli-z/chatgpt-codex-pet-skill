"""Validate learning traceability, not visual quality or truth of evidence."""
import argparse
import json
from pathlib import Path


def validate(data):
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get('entries'), list):
        return ['root.entries must be an array']
    seen = set()
    for index, item in enumerate(data['entries']):
        label = f'entries[{index}]'
        if not isinstance(item, dict):
            errors.append(f'{label} must be an object')
            continue
        for key in ('id', 'case', 'stage', 'failure', 'hypothesis', 'bounded_change', 'generalization'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f'{label}.{key} must be nonempty text')
        if isinstance(item.get('id'), str):
            if item['id'] in seen:
                errors.append(f'{label}.id must be unique')
            seen.add(item['id'])
        for key in ('input_evidence', 'verification', 'regression_tests'):
            if not isinstance(item.get(key), list) or not item[key]:
                errors.append(f'{label}.{key} must be a nonempty array')
        if item.get('status') not in ('observed', 'untested', 'inconclusive'):
            errors.append(f'{label}.status must be observed, untested, or inconclusive')
        verification = item.get('verification', [])
        if isinstance(verification, list):
            for v in verification:
                if not isinstance(v, dict) or v.get('kind') not in ('machine', 'visual', 'user_feedback') or v.get('result') not in ('pass', 'warning', 'fail', 'not_run', 'blocked') or not v.get('evidence'):
                    errors.append(f'{label}.verification needs kind, result, evidence')
            if item.get('status') == 'untested' and any(isinstance(v, dict) and v.get('result') not in ('not_run', 'blocked') for v in verification):
                errors.append(f'{label}: untested cannot claim executed verification')
            if item.get('status') == 'observed' and not any(isinstance(v, dict) and v.get('result') in ('pass', 'warning', 'fail') for v in verification):
                errors.append(f'{label}: observed needs executed evidence')
        for test in item.get('regression_tests', []) if isinstance(item.get('regression_tests'), list) else []:
            if not isinstance(test, dict) or test.get('kind') not in ('machine', 'manual') or not test.get('reference') or test.get('status') not in ('passed', 'failed', 'not_run'):
                errors.append(f'{label}.regression_tests needs kind, reference, status')
        if item.get('generalization_status') not in ('supported_within_case', 'proposed_transfer', 'cross_case_verified'):
            errors.append(f'{label}.generalization_status invalid')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.ledger.read_text(encoding="utf-8")))
    except (ValueError, OSError) as exc:
        errors = [str(exc)]
    print(json.dumps({'ok': not errors, 'errors': errors, 'scope': 'schema and traceability only; no visual verdict'}, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
