#!/usr/bin/env python3
"""Original educational stroke rig. No source artwork or native pet generation."""
import json, math
from pathlib import Path
from xml.sax.saxutils import quoteattr
ROOT = Path(__file__).resolve().parent
STROKE = 4.0
LENGTHS = {'torso': 35., 'upper_arm': 25., 'forearm': 23., 'thigh': 30., 'shin': 29.}
SHOULDER, HIP = (80., 66.), (80., 101.)
def endpoint(p, length, degrees):
    a = math.radians(degrees)
    return (p[0] + length * math.cos(a), p[1] + length * math.sin(a))
def chain(start, l1, a1, l2, a2):
    mid = endpoint(start, l1, a1)
    return [start, mid, endpoint(mid, l2, a2)]
def frame(t):
    # Raised arm gives a tiny greeting; all lengths are solved from angles.
    wave = math.sin(2 * math.pi * t)
    return {'head': {'center': [80., 43.], 'radius': 17.},
            'neck': [[80., 60.], SHOULDER], 'torso': [SHOULDER, HIP],
            'left_arm': chain(SHOULDER, 25., 145., 23., 75.),
            'right_arm': chain(SHOULDER, 25., -10., 23., -78. + 7. * wave),
            'left_leg': chain(HIP, 30., 109., 29., 92.),
            'right_leg': chain(HIP, 30., 71., 29., 88.)}
def path(points):
    return 'M ' + ' L '.join(f'{x:.6f},{y:.6f}' for x, y in points)
def render(frames, animated):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="160" height="176" viewBox="0 0 160 176" role="img" aria-label="Original educational line figure making a small greeting">',
             '<title>Educational line-art rig, not a native pet</title>',
             '<g fill="none" stroke="#247A85" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" shape-rendering="geometricPrecision">',
             '<circle cx="80" cy="43" r="17"/>']
    for name in ['neck', 'torso', 'left_arm', 'right_arm', 'left_leg', 'right_leg']:
        parts.append(f'<path id="{name}" d={quoteattr(path(frames[0][name]))}>')
        if animated and name == 'right_arm':
            # Discrete poses preserve the sampled length invariants. Interpolating
            # SVG endpoints linearly would shorten segments between keyframes.
            vals = ';'.join(path(f[name]) for f in frames)
            parts.append(f'<animate attributeName="d" values={quoteattr(vals)} dur="2s" repeatCount="indefinite" calcMode="discrete"/>')
        parts.append('</path>')
    return '\n'.join(parts + ['</g>', '</svg>'])
def main():
    frames = [frame(i / 24) for i in range(25)]
    (ROOT/'poses.json').write_text(json.dumps({'stroke_width': STROKE, 'lengths': LENGTHS, 'frames': frames}, indent=2)+'\n')
    (ROOT/'rest.svg').write_text(render(frames, False)+'\n')
    (ROOT/'microgesture.svg').write_text(render(frames, True)+'\n')
if __name__ == '__main__': main()
