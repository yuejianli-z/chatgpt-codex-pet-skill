import importlib.util,hashlib,unittest
from pathlib import Path
from PIL import Image
spec=importlib.util.spec_from_file_location('repair',Path(__file__).parents[1]/'scripts/check_repair_contract.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RepairContractTests(unittest.TestCase):
    def test_12s_commensurate(self):
        self.assertEqual(m.validate_schedule({'gait':[160,140]*4,'work':[500]*6,'event':[1000,2000,9000]},12000),[])
    def test_old_8s_midcycle_reset_rejected(self):
        self.assertTrue(m.validate_schedule({'gait':[160,140]*4},8000))
    def test_all_ms_phase_repeat(self):
        ds=[160,140]*4
        self.assertTrue(all(m.phase(ds,t)==m.phase(ds,t+12000) for t in range(12000)))
        self.assertEqual((m.phase(ds,11999),m.phase(ds,12000)),(7,0))
    def test_empty_schedule_rejected(self):self.assertTrue(m.validate_schedule({},12000))
    def test_zero_hold_rejected(self):self.assertTrue(m.validate_schedule({'x':[20,0]},12000))
    def test_exact_encoded_end(self):self.assertEqual(m.validate_encoded_end(12000,list(range(0,12000,20)),[20]*600),[])
    def test_missing_final_hold_rejected(self):self.assertTrue(m.validate_encoded_end(12000,list(range(0,11980,20)),[20]*599))
    def test_timestamp_gap_rejected(self):self.assertTrue(m.validate_encoded_end(60,[0,40],[20,20]))
    def test_wrong_approved_baseline_rejected(self):
        with self.assertRaises(ValueError):m.changed_cells([b'a'],[b'a'],['wrong'])
    def test_unchanged_majority_does_not_approve_changed(self):
        a=[b'a']*73;b=a.copy();b[42]=b'changed';hs=[hashlib.sha256(x).hexdigest()for x in a]
        changed=m.changed_cells(a,b,hs);self.assertEqual(changed,[42]);self.assertTrue(m.validate_identity_review(changed,{'changed_cells':list(range(42)),'verdict':'pass'}))
    def test_complete_review_record_is_schema_only(self):
        r={k:'evidence'for k in ['approved_reference','same_view_comparison','native_size_evidence','enlarged_evidence','ratio_landmarks','eye_mouth_silhouette','reviewer']};r.update(changed_cells=[42],verdict='pass');self.assertEqual(m.validate_identity_review([42],r),[])
    def test_translation_is_not_cell_identity(self):
        a=Image.new('RGBA',(4,4));a.putpixel((1,1),(20,30,40,255));b=Image.new('RGBA',(4,4));b.putpixel((1,2),(20,30,40,255));self.assertNotEqual(a.tobytes(),b.tobytes());self.assertTrue(m.translation_only(a,b,0,1))
    def test_translation_rejects_clipping_or_recolor(self):
        a=Image.new('RGBA',(4,4));a.putpixel((1,3),(20,30,40,255));b=Image.new('RGBA',(4,4));self.assertFalse(m.translation_only(a,b,0,1));b.putpixel((1,3),(20,30,41,255));self.assertFalse(m.translation_only(a,b,0,0))

class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.req={'idle':{'kind':'animation','frames':2},'up':{'kind':'direction_pose','frames':1}}
        self.data={'idle':{'kind':'animation','source_indices':[0,1],'durations_ms':[100,200]},'up':{'kind':'direction_pose','source_indices':[0]}}
        self.roles=('front','side','rear','three-quarter')
        self.bodies=[{'role':r,'evidence_kind':'inferred','source':'fixture'}for r in self.roles]
    def test_complete_dynamic_contract(self):self.assertEqual(m.validate_coverage(self.req,self.data,self.roles,self.bodies),[])
    def test_missing_body_card(self):self.assertTrue(m.validate_coverage(self.req,self.data,self.roles,self.bodies[:-1]))
    def test_dropped_or_wrong_source_index(self):
        self.data['idle']['source_indices']=[0,2];self.assertTrue(m.validate_coverage(self.req,self.data))
    def test_direction_not_animation(self):
        self.data['up']['kind']='animation';self.assertTrue(m.validate_coverage(self.req,self.data))
    def test_missing_index_duration(self):
        self.data['idle']['durations_ms']=[100];self.assertTrue(m.validate_coverage(self.req,self.data))

class StyleScopeTests(unittest.TestCase):
    def test_explicit_choice_for_exact_case_style(self):
        self.assertTrue(m.can_start_batch('a','ink1',{'case_id':'a','style_version':'ink1','basis':'user_style_choice','evidence':'verified selection'}))
    def test_generic_autonomy_or_another_style_not_waiver(self):
        self.assertFalse(m.can_start_batch('a','ink1',{'case_id':'a','style_version':'ink1','basis':'do_everything','evidence':'generic delegation'}))
        self.assertFalse(m.can_start_batch('a','ink2',{'case_id':'a','style_version':'ink1','basis':'explicit_case_style_waiver','evidence':'verified waiver'}))
    def test_missing_evidence_cannot_approve(self):
        self.assertFalse(m.can_start_batch('a','ink1',{'case_id':'a','style_version':'ink1','basis':'unchanged_approved_baseline'}))
