#!/usr/bin/env python3
"""Read-only geometry evidence; never an acceptance gate or report replacement."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
from PIL import Image


def exterior(alpha, threshold, diagonal):
    w, h = alpha.size
    p = alpha.load()
    seen = set()
    q = deque()
    for x, y in ([(x, y) for x in range(w) for y in (0, h-1)] +
                 [(x, y) for y in range(h) for x in (0, w-1)]):
        if p[x, y] <= threshold and (x, y) not in seen:
            seen.add((x, y)); q.append((x, y))
    steps = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)
             if (x or y) and (diagonal or abs(x)+abs(y) == 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in steps:
            xx, yy = x+dx, y+dy
            if 0 <= xx < w and 0 <= yy < h and p[xx, yy] <= threshold and (xx, yy) not in seen:
                seen.add((xx, yy)); q.append((xx, yy))
    transparent = sum(v <= threshold for v in alpha.tobytes())
    return {'exterior_connected_pixels': len(seen), 'enclosed_transparent_pixels': transparent-len(seen)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('atlas', type=Path)
    ap.add_argument('--official-report', required=True, type=Path)
    ap.add_argument('--subjects', type=Path, help='Optional reviewed subject crops; see geometry-diagnostics.md')
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    inputs = [args.atlas, args.official_report]
    if args.subjects:
        inputs.append(args.subjects)
    if any(args.out.resolve() == source.resolve() or
           (args.out.exists() and source.exists() and args.out.samefile(source))
           for source in inputs):
        ap.error('output must not overwrite inputs or their aliases')
    if args.out.exists():
        ap.error('output already exists; choose a fresh output path')
    data = args.atlas.read_bytes()
    report_bytes = args.official_report.read_bytes()
    official = json.loads(report_bytes)
    im = Image.open(args.atlas).convert('RGBA')
    if im.size not in ((1536, 1872), (1536, 2288)):
        ap.error('expected supported 192x208-cell atlas geometry')
    result = {'purpose': 'diagnostic_only', 'authorizes_upload': False,
              'atlas_sha256': hashlib.sha256(data).hexdigest(),
              'official_report_sha256': hashlib.sha256(report_bytes).hexdigest(),
              'official_result_unchanged': official,
              'caution': 'Exterior connectivity does not prove artistic intent. Enclosed transparency does not prove a defect. Review at native size is required. This report cannot waive any mandatory gate.',
              'look_topology': [], 'subject_jump_evidence': []}
    if im.height == 2288:
        for i in range(16):
            x, y = (i%8)*192, (9+i//8)*208
            alpha = im.crop((x,y,x+192,y+208)).getchannel('A')
            result['look_topology'].append({'direction_degrees': i*22.5,
                'alpha_thresholds': {str(t): {str(n): exterior(alpha,t,n==8) for n in (4,8)} for t in (0,16)}})
    if args.subjects:
        manifest = json.loads(args.subjects.read_text())
        result['subject_manifest_sha256'] = hashlib.sha256(args.subjects.read_bytes()).hexdigest()
        for subject in manifest['subjects']:
            if subject.get('role') not in ('jumping_actor', 'stationary_support', 'attached_prop', 'other'):
                raise ValueError('each subject needs an explicit motion role')
            baselines = []
            for f in subject['frames']:
                row, col = f['row'], f['column']
                l,t,r,b = f['crop']
                if not (0 <= col < 8 and 0 <= row < im.height//208 and 0 <= l < r <= 192 and 0 <= t < b <= 208):
                    raise ValueError('subject crop outside cell')
                alpha=im.crop((col*192+l,row*208+t,col*192+r,row*208+b)).getchannel('A')
                box=alpha.point(lambda v: 255 if v>16 else 0).getbbox()
                baselines.append({'row':row,'column':col,'bottom_y':None if box is None else t+box[3], 'crop':f['crop']})
            jump=[f['bottom_y'] for f in baselines if f['row']==4 and f['bottom_y'] is not None]
            result['subject_jump_evidence'].append({'subject':subject['name'], 'role':subject['role'],
                'manual_crop_evidence':subject.get('evidence','UNREVIEWED'),
                'frames':baselines,'jump_bottom_range_pixels':max(jump)-min(jump) if jump else None,
                'caution':'Crop leakage, occlusion, limb motion, and changing pose can affect the metric. This is not a jump semantic verdict.'})
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(f'Diagnostic saved: {args.out}. No installation acceptance issued.')

if __name__ == '__main__':
    main()
