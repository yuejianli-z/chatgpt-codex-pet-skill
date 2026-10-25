#!/usr/bin/env python3
"""Independent OpenAI v2 atlas build/structural validation/preview adapter.

Requires approved, registered 192x208 RGBA frames, not the official Work Pets skills.
Never generates, rescales, redraws, installs or activates artwork. A structural pass
is NOT visual approval, server acceptance, or proof of host event bindings.
"""
import argparse
import json
from pathlib import Path
import sys
from PIL import Image

CELL = (192, 208)
SIZE = (1536, 2288)
MAX_BYTES = 20 * 1024 * 1024
ROWS = [('idle', 6), ('running-right', 8), ('running-left', 8), ('waving', 4),
        ('jumping', 5), ('failed', 8), ('waiting', 6), ('running', 6), ('review', 6)]
DISPLAY_ORDER = ['idle', 'running', 'review', 'waiting', 'failed', 'waving', 'jumping', 'running-left', 'running-right']
DURATIONS = [[280,110,110,140,140,320], [120]*7+[220], [120]*7+[220],
             [140]*3+[280], [140]*4+[280], [140]*7+[240], [150]*5+[260],
             [120]*5+[220], [150]*5+[280]]

def box(row, col):
    return (col*CELL[0], row*CELL[1], (col+1)*CELL[0], (row+1)*CELL[1])

def validate(path):
    errors = []
    path = Path(path)
    result = {'ok': False, 'errors': errors, 'scope': 'v2 structural checks only',
              'visual_review': 'required', 'server_preflight': 'not_performed'}
    try:
        result['bytes'] = path.stat().st_size
        if result['bytes'] > MAX_BYTES: errors.append('file exceeds 20 MiB')
        with Image.open(path) as source:
            result['format'] = source.format
            if source.format not in {'PNG', 'WEBP'}: errors.append('format must be PNG or WebP')
            if getattr(source, 'n_frames', 1) != 1: errors.append('atlas must be a single image, not animated')
            if source.size != SIZE: errors.append('v2 size must be exactly 1536 x 2288')
            if 'A' not in source.getbands() and 'transparency' not in source.info:
                errors.append('image needs an alpha channel or transparency')
            image = source.convert('RGBA')
        if image.size == SIZE:
            alpha = image.getchannel('A')
            if alpha.getextrema()[0] == 255: errors.append('atlas has no transparent pixels')
            occupied = empty = 0
            for row in range(11):
                used = ROWS[row][1] if row < 9 else 8
                for col in range(8):
                    has_art = alpha.crop(box(row, col)).getbbox() is not None
                    if col < used:
                        occupied += has_art
                        if not has_art: errors.append(f'required cell {row},{col} is empty')
                    else:
                        empty += not has_art
                        if has_art: errors.append(f'unused cell {row},{col} must be fully transparent')
            result.update(occupied_required_cells=occupied, transparent_unused_cells=empty)
    except (OSError, ValueError) as e:
        errors.append(str(e))
    result['ok'] = not errors
    return result

def build(manifest_path, output):
    manifest_path = Path(manifest_path)
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    if not isinstance(data, dict): raise ValueError('manifest must be an object')
    actions = data.get('actions')
    if not isinstance(actions, dict) or set(actions) != {name for name, _ in ROWS}:
        raise ValueError('actions must contain exactly the nine row names')
    gaze = data.get('gaze')
    if not isinstance(gaze, list) or len(gaze) != 16: raise ValueError('gaze must contain 16 ordered frame paths')
    atlas = Image.new('RGBA', SIZE)
    for row, (name, count) in enumerate(ROWS + [('gaze-first',8), ('gaze-second',8)]):
        frames = actions[name] if row < 9 else gaze[(row-9)*8:(row-8)*8]
        if not isinstance(frames, list) or len(frames) != count:
            raise ValueError(f'{name} requires exactly {count} frames')
        for col, relative in enumerate(frames):
            if not isinstance(relative, str) or not relative: raise ValueError('frame paths must be nonempty strings')
            p = (manifest_path.parent / relative).resolve()
            with Image.open(p) as source:
                if source.size != CELL: raise ValueError(f'{relative}: frame must be registered at 192 x 208')
                if getattr(source, 'n_frames', 1) != 1: raise ValueError(f'{relative}: source frame is animated')
                if 'A' not in source.getbands() and 'transparency' not in source.info:
                    raise ValueError(f'{relative}: alpha/transparency required')
                frame = source.convert('RGBA')
            if frame.getchannel('A').getbbox() is None: raise ValueError(f'{relative}: empty frame')
            atlas.paste(frame, (col*CELL[0], row*CELL[1]))  # copy alpha; no alpha squaring
    output = Path(output)
    if output.exists(): raise ValueError('output exists; choose a new revision path')
    if output.suffix.lower() not in {'.png', '.webp'}: raise ValueError('output must end in .png or .webp')
    output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output, **({'lossless':True} if output.suffix.lower()=='.webp' else {}))
    return validate(output)

def preview(path, directory):
    report = validate(path)
    if not report['ok']: return report
    directory = Path(directory)
    if directory.exists() and any(directory.iterdir()): raise ValueError('preview directory must be empty')
    directory.mkdir(parents=True, exist_ok=True)
    with Image.open(path) as src: atlas = src.convert('RGBA')
    for row, (name, count) in enumerate(ROWS):
        frames = []
        for col in range(count):
            # White backing belongs only to the preview, never to the import atlas.
            base = Image.new('RGBA', CELL, 'white'); base.alpha_composite(atlas.crop(box(row,col)))
            frames.append(base.convert('RGB'))
        frames[0].save(directory/f'{name}.gif', save_all=True, append_images=frames[1:],
                       duration=DURATIONS[row], loop=0, disposal=2)
    gaze = [atlas.crop(box(9+i//8, i%8)) for i in range(16)]
    for i, frame in enumerate(gaze): frame.save(directory/f'gaze-{i:02d}.png')
    metadata = {'scope':'offline source-loop preview, not actual host timing or triggering',
                'display_order':DISPLAY_ORDER,
                'row_order':[name for name, _ in ROWS],
                'row_durations_ms':dict(zip((r[0] for r in ROWS), DURATIONS)),
                'gaze':'16 still samples clockwise from up; no intrinsic duration',
                'installation':'not performed'}
    (directory/'preview.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return {'ok':True, **metadata}

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    v=sub.add_parser('validate'); v.add_argument('atlas')
    b=sub.add_parser('build'); b.add_argument('manifest'); b.add_argument('output')
    r=sub.add_parser('preview'); r.add_argument('atlas'); r.add_argument('directory')
    args=p.parse_args()
    try:
        result = validate(args.atlas) if args.command=='validate' else build(args.manifest,args.output) if args.command=='build' else preview(args.atlas,args.directory)
    except (OSError,ValueError,TypeError) as e: result={'ok':False,'errors':[str(e)]}
    print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(0 if result['ok'] else 1)
