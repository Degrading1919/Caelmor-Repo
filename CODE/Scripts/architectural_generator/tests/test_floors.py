"""Cheap gates for additive floor metadata and visual-selection semantics."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from caelmor_architecture import _settings_from_json
from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate, geometry_hash
from caelmor_architecture import floors
from dataclasses import replace


class Floors(unittest.TestCase):
    def test_schedule_and_legacy_hashes(self):
        for count in (1,2,3):
            s = Settings(floors=count,detail='LOW')
            plan, buffers = generate(s)
            host = floors.schedule(plan)[0]
            self.assertEqual(host['count'],count)
            self.assertEqual(floors.ceiling([host],'main',count-1),plan.eave)
            self.assertEqual(geometry_hash(buffers),geometry_hash(generate(replace(s,floor_separation=False))[1]))

    def test_old_settings_are_explicitly_unsplit(self):
        self.assertTrue(Settings().floor_separation)
        self.assertFalse(_settings_from_json({'seed':17}).floor_separation)
        self.assertTrue(_settings_from_json({'floor_separation':True}).floor_separation)
        with self.assertRaises(ValueError): Settings(floor_separation=1).check()

    def test_selection_and_invalid_occupancy_are_not_inferred(self):
        volumes=[dict(volume='low',base=.3,height=2.7,count=2),
                 dict(volume='raised',base=1.8,height=3.,count=1)]
        self.assertEqual(floors.ceiling(volumes,'raised',0),4.8)
        with self.assertRaises(ValueError): floors.ceiling(volumes,'raised',1)
        with self.assertRaises(ValueError): floors.ceiling(volumes,'missing',0)
        for role in ('FLOOR','COVERING','ALWAYS'):
            self.assertTrue(floors.visible(role,3,8,None))
        self.assertFalse(floors.visible('FLOOR',3,6,3))
        self.assertTrue(floors.visible('FLOOR',.3,3,3))
        self.assertFalse(floors.visible('COVERING',2,5,3))
        self.assertTrue(floors.visible('COVERING',1,2,3))
        self.assertTrue(floors.visible('ALWAYS',0,12,3))

    def test_semantic_continuity_and_covering(self):
        self.assertEqual(floors.behavior('details','supported_hollow_masonry_flue'),'ALWAYS')
        self.assertEqual(floors.behavior('details',functional_role='chimney'),'ALWAYS')
        self.assertEqual(floors.behavior('roof'),'COVERING')
        self.assertEqual(floors.behavior('details',envelope={'plane':[0,0,2.4],'clearance':0}),'COVERING')
        self.assertEqual(floors.behavior('structure',component_role='roof_deck'),'COVERING')
        self.assertEqual(floors.behavior('structure'),'FLOOR')


if __name__=='__main__': unittest.main()
