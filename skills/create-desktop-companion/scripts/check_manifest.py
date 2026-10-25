"""Bridge completeness-manifest lists to dynamic coverage/schedule diagnostics."""
import argparse,json
from pathlib import Path
from check_repair_contract import validate_coverage,validate_schedule

def check(data):
    try:
        expected=data['capability_matrix'];coverage=data['coverage']
        if not expected or len({x['requirement_key'] for x in expected})!=len(expected):return ['empty or duplicate requirements']
        if len({x['requirement_key']for x in coverage})!=len(coverage):return ['duplicate coverage entries']
        requirements={x['requirement_key']:{'kind':x['kind'],'frames':x['required_frames']}for x in expected}
        if any(type(x['frames'])is not int or x['frames']<1 for x in requirements.values()):return ['positive required_frames needed']
        delivered={x['requirement_key']:{'kind':x['kind'],'source_indices':x['source_indices'],'durations_ms':x.get('durations_ms',[])}for x in coverage}
        errors=validate_coverage(requirements,delivered,data.get('required_body_roles',[]),data.get('body_views',[]))
        schedule=data['preview_schedule'];errors+=validate_schedule(schedule['row_schedules'],schedule['master_period_ms'])
        required_animation_keys={k for k,v in requirements.items() if v['kind']=='animation'}
        if set(schedule['row_schedules'])!=required_animation_keys:errors.append('schedule keys must equal animation requirement keys')
        return errors
    except (KeyError,TypeError,ValueError)as exc:return ['incomplete or invalid manifest: '+str(exc)]
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);a=p.parse_args()
    try:errors=check(json.loads(a.manifest.read_text()))
    except (OSError,ValueError)as e:errors=[str(e)]
    print(json.dumps({'ok':not errors,'errors':errors,'scope':'coverage records and schedule arithmetic only; no image/identity/comfort verification'},indent=2));raise SystemExit(bool(errors))
