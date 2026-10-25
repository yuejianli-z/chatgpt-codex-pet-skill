#!/usr/bin/env python3
"""Check delivery-claim evidence records, not asset quality or evidence truth."""
import argparse
import json


def validate(record):
    if not isinstance(record, dict):
        return ['record must be an object']
    errors = []
    def require(key):
        value = record.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append('missing evidence: ' + key)
    claims = record.get('claims', {})
    if not isinstance(claims, dict):
        return ['claims must be an object']
    allowed = {'displayable', 'production_ready', 'installed', 'active', 'runtime_accepted'}
    if set(claims) - allowed:
        errors.append('unknown delivery claim')
    if any(type(v) is not bool for v in claims.values()):
        errors.append('claims must be explicit booleans')
    if any(v is True for v in claims.values()):
        require('artifact_hash')
    if claims.get('displayable') is True:
        require('preview_evidence')
    if claims.get('production_ready') is True:
        for key in ('host_version', 'contract_evidence', 'eligibility_evidence'):
            require(key)
        gates = record.get('mandatory_gates')
        if not isinstance(gates, dict) or not gates:
            errors.append('mandatory gates must be enumerated')
        elif any(v != 'pass' for v in gates.values()):
            errors.append('production_ready requires every mandatory gate to pass')
    if claims.get('installed') is True or claims.get('active') is True:
        require('host_version')
        require('authorization_evidence')
        require('installation_receipt')
    if claims.get('active') is True:
        require('activation_readback')
    if claims.get('runtime_accepted') is True:
        for key in ('host_version', 'runtime_observation', 'runtime_scope', 'runtime_limitations'):
            require(key)
        if record.get('observation_mode') != 'actual_client':
            errors.append('runtime acceptance requires actual-client observation')
    caps = record.get('capabilities', {})
    if not isinstance(caps, dict):
        errors.append('capabilities must be an object')
        caps = {}
    for name, cap in caps.items():
        if not isinstance(cap, dict) or cap.get('status') not in ('supported', 'unsupported', 'unknown'):
            errors.append('invalid capability: ' + name)
        elif cap['status'] != 'unknown' and (not isinstance(cap.get('evidence'), str) or not cap['evidence'].strip()):
            errors.append('missing capability evidence: ' + name)
    asserted = record.get('asserted_supported', [])
    if not isinstance(asserted, list) or any(not isinstance(name, str) or not name.strip() for name in asserted):
        errors.append('asserted_supported must be an array of nonempty capability names')
        asserted = []
    for name in asserted:
        if not isinstance(caps.get(name), dict) or caps[name].get('status') != 'supported':
            errors.append('unverified support claim: ' + name)
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record')
    args = parser.parse_args()
    try:
        with open(args.record, encoding='utf-8') as f:
            result = validate(json.load(f))
    except (OSError, ValueError) as exc:
        result = [str(exc)]
    print(json.dumps({'ok': not result, 'errors': result}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result))
