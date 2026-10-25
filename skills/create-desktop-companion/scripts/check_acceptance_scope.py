"""Check acceptance-record consistency only; never evaluate art or authorize installation."""
import argparse
import json
from pathlib import Path

GATES = ('geometry', 'identity', 'direction_semantics', 'full_coverage', 'actual_runtime')


def validate(data):
    if not isinstance(data, dict):
        return ['record must be an object']
    errors = []
    required = data.get('required_directions')
    tested = data.get('tested_directions')
    for name, values in [('required_directions', required), ('tested_directions', tested)]:
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values):
            errors.append(f'{name} must be a nonempty array of direction identifiers')
        elif len(set(values)) != len(values):
            errors.append(f'{name} must not contain duplicate directions')
    gates = data.get('gates')
    if not isinstance(gates, dict):
        return errors + ['gates must be an object']
    for name in GATES:
        gate = gates.get(name)
        if not isinstance(gate, dict) or gate.get('status') not in ('pass', 'fail', 'unknown', 'not_run') or not isinstance(gate.get('evidence'), str) or not gate['evidence'].strip():
            errors.append(f'{name} requires status and evidence')
    complete = (isinstance(required, list) and isinstance(tested, list)
                and all(isinstance(x, str) for x in required + tested)
                and bool(required) and len(set(required)) == len(required)
                and len(set(tested)) == len(tested) and set(required) == set(tested))
    if isinstance(gates.get('full_coverage'), dict) and gates['full_coverage'].get('status') == 'pass' and not complete:
        errors.append('full_coverage cannot pass with partial, duplicate or unexpected directions')
    if data.get('claim') not in ('partial_diagnostic', 'candidate', 'fully_accepted'):
        errors.append('claim must be partial_diagnostic, candidate, or fully_accepted')
    if data.get('claim') == 'fully_accepted':
        if not complete:
            errors.append('fully_accepted requires exact complete direction coverage')
        if any(not isinstance(gates.get(k), dict) or gates[k].get('status') != 'pass' for k in GATES):
            errors.append('fully_accepted requires all five independent gates to pass')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.record.read_text()))
    except (ValueError, OSError) as exc:
        errors = [str(exc)]
    print(json.dumps({'ok': not errors, 'errors': errors, 'scope': 'record consistency only; supplied evidence is not independently verified', 'authorizes_installation': False}))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
