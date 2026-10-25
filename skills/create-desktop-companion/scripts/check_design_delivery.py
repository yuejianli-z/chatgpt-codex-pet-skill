"""Validate explicit design/installation decisions; never grant permission or install."""
import argparse
import json
from pathlib import Path
import re

PRIORITY = ['idle','running','review','waiting','failed']

def validate(record):
    errors=[]
    if not isinstance(record,dict): return ['record must be an object']
    if record.get('design_priority') != PRIORITY: errors.append('declare default design priority idle > running > review > waiting > failed')
    if not record.get('core_identity'): errors.append('core_identity is required')
    states=record.get('states',{})
    if not isinstance(states,dict): return errors+['states must be an object']
    for state in PRIORITY:
        entry=states.get(state)
        if not isinstance(entry,dict): errors.append(f'{state}: design record required'); continue
        for key in ('motion_intent','fatigue_risk','identity_role','return_to_idle_review'):
            if not isinstance(entry.get(key),str) or not entry[key].strip(): errors.append(f'{state}: {key} required')
        occupancy=entry.get('observed_screen_share')
        if occupancy is not None:
            if isinstance(occupancy,bool) or not isinstance(occupancy,(int,float)) or not 0<=occupancy<=1:
                errors.append(f'{state}: observed_screen_share must be 0..1 or null')
            if not entry.get('runtime_evidence'): errors.append(f'{state}: occupancy requires actual-client evidence')
    if record.get('gaze_identity') != record.get('core_identity') and not record.get('alternate_gaze_approval'):
        errors.append('gaze must preserve approved core identity unless alternate explicitly approved')
    bindings=record.get('host_bindings',[])
    if not isinstance(bindings,list): return errors+['host_bindings must be an array']
    for item in bindings:
        if not isinstance(item,dict): errors.append('binding must be an object'); continue
        if item.get('evidence_kind') not in ('unknown','user_observed','source_verified','actual_client_test'):
            errors.append('binding needs explicit evidence_kind')
        if item.get('evidence_kind')!='unknown' and not all(item.get(k) for k in ('surface','client_version','source','event','animation')):
            errors.append('known binding needs surface/version/source/event/animation')
    return errors

def final_preflight_declared(record):
    """Check evidence declarations, not their authenticity or actual host acceptance.

    Both required production checks and supported eligibility preflight must cite
    the exact final encoded artifact. These records never run or waive a gate.
    """
    digest = record.get('final_artifact_sha256')
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest):
        return False
    for key in ('production_evidence', 'eligibility_evidence'):
        evidence = record.get(key)
        if not isinstance(evidence, dict) or evidence.get('passed') is not True:
            return False
        artifact = evidence.get('artifact_sha256')
        source = evidence.get('source')
        if not isinstance(artifact, str) or artifact.lower() != digest.lower():
            return False
        if not isinstance(source, str) or not source.strip():
            return False
    return True

def install_decision(record):
    """An advisory state machine; actual tool permissions remain authoritative."""
    if not isinstance(record,dict): return 'invalid_record'
    if record.get('operation') not in ('create','update','metadata_only','activate_existing'): return 'invalid_operation'
    if record.get('operation') in ('update','metadata_only','activate_existing') and not record.get('stable_pet_id'): return 'resolve_target'
    if record.get('operation') in ('create','update'):
        if record.get('structural_pass') is not True or record.get('visual_approved') is not True: return 'finish_validation_and_review'
    if record.get('install_authorized') is not True: return 'ask_installation'
    if record.get('supported_write_route') is not True: return 'deliver_import_package'
    if record.get('activate') is True or record.get('operation') == 'activate_existing':
        if record.get('activation_authorized') is not True: return 'ask_activation'
        surfaces=record.get('target_surfaces')
        if not isinstance(surfaces,list) or not surfaces or not all(isinstance(v,str) and v.strip() for v in surfaces): return 'resolve_activation_surface'
    if record.get('operation') in ('create','update') and not final_preflight_declared(record):
        return 'complete_final_preflight_before_authorized_operation'
    return 'execute_authorized_operation_then_verify'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record');p.add_argument('--installation',action='store_true');a=p.parse_args()
    try:
        value=json.loads(Path(a.record).read_text(encoding='utf-8'))
        result={'decision':install_decision(value),'scope':'advisory only; no external writes'} if a.installation else {'errors':validate(value)}
        result['ok']=result.get('decision') not in ('invalid_record','invalid_operation') if a.installation else not result['errors']
    except (OSError,ValueError,TypeError) as e: result={'ok':False,'errors':[str(e)]}
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['ok'] else 1)
