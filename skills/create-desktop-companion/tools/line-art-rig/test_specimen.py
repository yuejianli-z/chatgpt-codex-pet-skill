#!/usr/bin/env python3
"""Geometric invariants only: not a visual, semantic or platform gate."""
import json, math, unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from build_specimen import ROOT, frame, main

def distance(a,b): return math.dist(a,b)
def point_segment(p,a,b):
    v=(b[0]-a[0], b[1]-a[1]); den=v[0]**2+v[1]**2
    t=max(0., min(1., ((p[0]-a[0])*v[0]+(p[1]-a[1])*v[1])/den))
    return distance(p,(a[0]+t*v[0],a[1]+t*v[1]))
class RigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main(); cls.frames=json.loads((ROOT/'poses.json').read_text())['frames']
    def test_fixed_segment_lengths(self):
        for f in self.frames:
            self.assertAlmostEqual(distance(*f['torso']),35.,places=9)
            for side in ('left','right'):
                for kind, lengths in [('arm',(25.,23.)),('leg',(30.,29.))]:
                    pts=f[f'{side}_{kind}']
                    for i,l in enumerate(lengths): self.assertAlmostEqual(distance(pts[i],pts[i+1]),l,places=9)
    def test_connected_anatomy_and_stable_feet(self):
        base=self.frames[0]
        for f in self.frames:
            for side in ('left','right'):
                self.assertEqual(f[f'{side}_arm'][0], f['torso'][0])
                self.assertEqual(f[f'{side}_leg'][0], f['torso'][1])
                self.assertEqual(f[f'{side}_leg'][-1], base[f'{side}_leg'][-1])
            self.assertEqual(f['head'],base['head'])
            self.assertEqual(f['neck'][-1], f['torso'][0])
            self.assertAlmostEqual(distance(f['neck'][0],f['head']['center']),f['head']['radius'])
    def test_loop_closure_and_bounded_steps(self):
        for a,b in zip(self.frames[0]['right_arm'],self.frames[-1]['right_arm']): self.assertLess(distance(a,b),1e-9)
        steps=[distance(a['right_arm'][-1],b['right_arm'][-1]) for a,b in zip(self.frames,self.frames[1:])]
        self.assertGreater(max(steps),0.)
        self.assertLess(max(steps),1.)
    def test_selected_negative_space_clearances(self):
        # Explicit landmark diagnostics, NOT a complete silhouette evaluator.
        report=[]
        for f in self.frames:
            c=f['head']['center']; radius=f['head']['radius']
            forearm=f['right_arm'][1:]
            head_gap=point_segment(c,*forearm)-radius-4. # two half strokes
            hand_torso_gap=point_segment(f['right_arm'][-1],*f['torso'])-4.
            foot_gap=distance(f['left_leg'][-1],f['right_leg'][-1])-4.
            self.assertGreater(head_gap,5.)
            self.assertGreater(hand_torso_gap,10.)
            self.assertGreater(foot_gap,10.)
            report.append({'head_to_raised_forearm_edge_gap':head_gap,'hand_to_torso_edge_gap':hand_torso_gap,'foot_endpoint_edge_gap':foot_gap})
        (ROOT/'diagnostics.json').write_text(json.dumps({'scope':'Selected geometric clearances; not visual acceptance or native pet validation','minimums':{k:min(r[k] for r in report) for k in report[0]}},indent=2)+'\n')
    def test_svg_stroke_and_no_fill(self):
        for file in ('rest.svg','microgesture.svg'):
            root=ET.parse(ROOT/file).getroot(); ns='{http://www.w3.org/2000/svg}'
            group=root.find(ns+'g')
            self.assertEqual(group.attrib['fill'],'none')
            self.assertEqual(group.attrib['stroke-width'],'4')
            self.assertEqual(group.attrib['stroke-linecap'],'round')
            self.assertEqual(group.attrib['stroke-linejoin'],'round')
            self.assertEqual(len(group.findall(ns+'path')),6)
            self.assertEqual(len(group.findall(ns+'circle')),1)
if __name__=='__main__': unittest.main(verbosity=2)
