import importlib.util
from pathlib import Path
import tempfile
import unittest
import json
from PIL import Image,ImageDraw
S=Path(__file__).resolve().parents[1]/'scripts'
def load(name):
 spec=importlib.util.spec_from_file_location(name,S/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load('openai_pet_atlas'); d=load('check_design_delivery')
class Atlas(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def fixture(self):
  im=Image.new('RGBA',m.CELL);ImageDraw.Draw(im).rectangle((50,60,100,120),fill=(40,60,80,128));im.save(self.root/'f.png')
  data={'actions':{n:['f.png']*c for n,c in m.ROWS},'gaze':['f.png']*16};(self.root/'m.json').write_text(json.dumps(data));return data
 def test_display_order_does_not_change_protocol(self):
  self.assertEqual([n for n,c in m.ROWS],['idle','running-right','running-left','waving','jumping','failed','waiting','running','review'])
  self.assertEqual(m.DISPLAY_ORDER,['idle','running','review','waiting','failed','waving','jumping','running-left','running-right'])
  self.assertEqual(set(m.DISPLAY_ORDER),{n for n,c in m.ROWS})
 def test_build_counts_and_alpha(self):
  self.fixture();r=m.build(self.root/'m.json',self.root/'a.png');self.assertTrue(r['ok']);self.assertEqual(r['occupied_required_cells'],73);self.assertEqual(r['transparent_unused_cells'],15)
  with Image.open(self.root/'a.png') as im:self.assertEqual(im.getpixel((50,60)),(40,60,80,128))
 def test_fixed_counts(self):
  data=self.fixture();data['actions']['waving']*=2;(self.root/'m.json').write_text(json.dumps(data))
  with self.assertRaises(ValueError):m.build(self.root/'m.json',self.root/'a.png')
 def test_wrong_size(self):
  Image.new('RGBA',(768,1144)).save(self.root/'a.png');self.assertFalse(m.validate(self.root/'a.png')['ok'])
 def test_unused_cell_rejected(self):
  self.fixture();m.build(self.root/'m.json',self.root/'a.png')
  with Image.open(self.root/'a.png') as im: im.putpixel((7*192,0),(1,1,1,1));im.save(self.root/'b.png')
  self.assertFalse(m.validate(self.root/'b.png')['ok'])
 def test_missing_required_cell(self):
  Image.new('RGBA',m.SIZE).save(self.root/'a.png');self.assertFalse(m.validate(self.root/'a.png')['ok'])
 def test_size_limit(self):
  self.fixture();m.build(self.root/'m.json',self.root/'a.png')
  with (self.root/'a.png').open('ab') as f:f.write(b'\0'*(m.MAX_BYTES+1))
  self.assertIn('file exceeds 20 MiB',m.validate(self.root/'a.png')['errors'])
 def test_preserve_existing(self):
  self.fixture();m.build(self.root/'m.json',self.root/'a.png')
  with self.assertRaises(ValueError):m.build(self.root/'m.json',self.root/'a.png')
 def test_preview_is_not_installation(self):
  self.fixture();m.build(self.root/'m.json',self.root/'a.png');r=m.preview(self.root/'a.png',self.root/'p');self.assertEqual(r['installation'],'not performed');self.assertEqual(len(list((self.root/'p').glob('*.gif'))),9);self.assertEqual(len(list((self.root/'p').glob('gaze*.png'))),16)
class Decisions(unittest.TestCase):
 def good(self):return {'operation':'create','structural_pass':True,'visual_approved':True,'install_authorized':True,'supported_write_route':True}
 def test_visual_approval_not_install_permission(self):
  r=self.good();r['install_authorized']=False;self.assertEqual(d.install_decision(r),'ask_installation')
 def ready(self):
  r=self.good();r['final_artifact_sha256']='a'*64
  for key in ('production_evidence','eligibility_evidence'):
   r[key]={'passed':True,'artifact_sha256':'a'*64,'source':'reviewed-report.json'}
  return r
 def test_authorized_install_not_reasked(self):self.assertEqual(d.install_decision(self.ready()),'execute_authorized_operation_then_verify')
 def test_structural_visual_pass_still_requires_final_preflight(self):
  for operation in ('create','update'):
   r=self.good();r.update(operation=operation,stable_pet_id='example')
   self.assertEqual(d.install_decision(r),'complete_final_preflight_before_authorized_operation')
 def test_final_preflight_requires_both_reports_and_exact_artifact(self):
  for key in ('production_evidence','eligibility_evidence'):
   for bad in (None,[],True,{}, {'passed':False,'artifact_sha256':'a'*64,'source':'report'},
               {'passed':1,'artifact_sha256':'a'*64,'source':'report'},
               {'passed':True,'artifact_sha256':'b'*64,'source':'report'},
               {'passed':True,'artifact_sha256':True,'source':'report'},
               {'passed':True,'artifact_sha256':'a'*64,'source':' '},
               {'passed':True,'artifact_sha256':'a'*64,'source':True}):
    with self.subTest(key=key,bad=bad):
     r=self.ready();r[key]=bad
     self.assertEqual(d.install_decision(r),'complete_final_preflight_before_authorized_operation')
 def test_final_artifact_hash_required(self):
  for digest in (None,True,'','a'*63,'z'*64):
   r=self.ready();r['final_artifact_sha256']=digest
   self.assertEqual(d.install_decision(r),'complete_final_preflight_before_authorized_operation')
 def test_verified_update_retains_target_requirement(self):
  r=self.ready();r['operation']='update';self.assertEqual(d.install_decision(r),'resolve_target')
  r['stable_pet_id']='example';self.assertEqual(d.install_decision(r),'execute_authorized_operation_then_verify')
 def test_missing_route_delivers_package(self):
  r=self.good();r['supported_write_route']=False;self.assertEqual(d.install_decision(r),'deliver_import_package')
 def test_activation_separate(self):
  r=self.good();r['activate']=True;self.assertEqual(d.install_decision(r),'ask_activation')
 def test_activate_existing_cannot_bypass_activation_checks(self):
  for flag in (None,False):
   r={'operation':'activate_existing','stable_pet_id':'example','install_authorized':True,'supported_write_route':True,'activate':flag}
   self.assertEqual(d.install_decision(r),'ask_activation')
   r['activation_authorized']=True;self.assertEqual(d.install_decision(r),'resolve_activation_surface')
 def test_update_needs_identity(self):
  r=self.good();r['operation']='update';self.assertEqual(d.install_decision(r),'resolve_target')
 def test_metadata_no_visual_upload(self):
  r={'operation':'metadata_only','stable_pet_id':'example','install_authorized':True,'supported_write_route':True};self.assertEqual(d.install_decision(r),'execute_authorized_operation_then_verify')
 def test_design_occupancy_requires_evidence(self):
  r={'design_priority':d.PRIORITY,'core_identity':'approved form','gaze_identity':'approved form','states':{n:{'motion_intent':'clear','fatigue_risk':'low','identity_role':'core','return_to_idle_review':'pending visual review','observed_screen_share':None} for n in d.PRIORITY}}
  self.assertEqual(d.validate(r),[]);r['states']['running']['observed_screen_share']=.8;self.assertTrue(d.validate(r))
 def test_gaze_identity_change_needs_approval(self):
  r={'design_priority':d.PRIORITY,'core_identity':'A','gaze_identity':'B','states':{}};self.assertIn('gaze must preserve approved core identity unless alternate explicitly approved',d.validate(r))
