import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image, ImageDraw

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/diagnose_visual_geometry.py'
spec=importlib.util.spec_from_file_location('geometry',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class GeometryEvidenceTests(unittest.TestCase):
    def test_true_enclosed_hole_retained(self):
        a=Image.new('L',(8,8),0);d=ImageDraw.Draw(a);d.rectangle((1,1,6,6),fill=255);d.rectangle((3,3,4,4),fill=0)
        self.assertEqual(m.exterior(a,16,False)['enclosed_transparent_pixels'],4)
        self.assertEqual(m.exterior(a,16,True)['enclosed_transparent_pixels'],4)

    def test_open_anatomical_gap_is_exterior(self):
        a=Image.new('L',(8,8),0);d=ImageDraw.Draw(a);d.rectangle((1,1,6,6),fill=255);d.rectangle((3,3,4,7),fill=0)
        self.assertEqual(m.exterior(a,16,False)['enclosed_transparent_pixels'],0)

    def test_diagonal_ambiguity_is_exposed(self):
        a=Image.new('L',(5,5),255)
        for i in range(3):a.putpixel((i,i),0)
        self.assertEqual(m.exterior(a,16,False)['enclosed_transparent_pixels'],2)
        self.assertEqual(m.exterior(a,16,True)['enclosed_transparent_pixels'],0)

    def test_compound_subject_and_original_failure(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);im=Image.new('RGBA',(1536,2288));d=ImageDraw.Draw(im)
            frames=[]
            for c, bottom in enumerate((150,130,118,130,150)):
                x=c*192;y=4*208
                d.rectangle((x+20,y+bottom-20,x+40,y+bottom-1), fill='red')
                d.rectangle((x+100,y+150,x+130,y+179), fill='blue')
                frames.append({'row':4,'column':c,'crop':[10,80,60,160]})
            im.save(p/'atlas.png')
            original={'ok':False,'errors':['compound total bbox has zero lift']}
            (p/'official.json').write_text(json.dumps(original))
            before=(p/'official.json').read_bytes()
            (p/'subjects.json').write_text(json.dumps({'subjects':[{'name':'actor','role':'jumping_actor','evidence':'synthetic disjoint rectangles','frames':frames}]}))
            subprocess.run([sys.executable,str(SCRIPT),str(p/'atlas.png'),'--official-report',str(p/'official.json'),'--subjects',str(p/'subjects.json'),'--out',str(p/'out.json')],check=True,capture_output=True)
            result=json.loads((p/'out.json').read_text())
            self.assertFalse(result['authorizes_upload'])
            self.assertEqual(result['official_result_unchanged'],original)
            self.assertEqual((p/'official.json').read_bytes(),before)
            self.assertEqual(result['subject_jump_evidence'][0]['jump_bottom_range_pixels'],32)
            self.assertNotIn('ok',result)


    def test_output_preserves_all_inputs_and_aliases(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            Image.new('RGBA', (1536, 1872)).save(p/'atlas.png')
            (p/'official.json').write_text('{}')
            (p/'subjects.json').write_text('{"subjects": []}')
            inputs = [p/'atlas.png', p/'official.json', p/'subjects.json']
            before = {f: f.read_bytes() for f in inputs}
            for source in inputs:
                aliases = [source, p/(source.name+'.symlink'), p/(source.name+'.hardlink')]
                aliases[1].symlink_to(source)
                aliases[2].hardlink_to(source)
                for out in aliases:
                    with self.subTest(source=source.name, output=out.name):
                        result = subprocess.run([sys.executable, str(SCRIPT), str(inputs[0]),
                            '--official-report', str(inputs[1]), '--subjects', str(inputs[2]),
                            '--out', str(out)], capture_output=True, text=True)
                        self.assertEqual(result.returncode, 2)
                        self.assertIn('must not overwrite', result.stderr)
                        for f in inputs:
                            self.assertEqual(f.read_bytes(), before[f])

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p/'out.json').write_text('existing evidence')
            result = subprocess.run([sys.executable, str(SCRIPT), str(p/'atlas.png'),
                '--official-report', str(p/'official.json'), '--out', str(p/'out.json')],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('output already exists', result.stderr)
            self.assertEqual((p/'out.json').read_text(), 'existing evidence')

if __name__=='__main__':unittest.main()
