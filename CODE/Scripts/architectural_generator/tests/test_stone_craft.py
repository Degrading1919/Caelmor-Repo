"""Regional load-bearing masonry must retain the requested workmanship."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from caelmor_architecture.engine import generate,validate,geometry_hash
from caelmor_architecture.model import Settings


class StoneCraftTests(unittest.TestCase):
    def test_workmanship_changes_built_masonry_without_changing_room_program(self):
        for region in ('THORNFELL','EMBERHOLT'):
            s=Settings(region=region,function='COTTAGE',wealth='ESTABLISHED',
                       world_aware=True,use_grammar=True,detail='MEDIUM',seed=91)
            rough,rb=generate(replace(s,craftsmanship='ROUGH'))
            fine,fb=generate(replace(s,craftsmanship='FINE'))
            self.assertEqual(rough.world_zones[0].plan.style.construction,'RUBBLE')
            self.assertEqual(fine.world_zones[0].plan.style.construction,'ASHLAR')
            self.assertEqual([m.key for m in rough.world_zones],[m.key for m in fine.world_zones])
            self.assertNotEqual(geometry_hash([b for b in rb if b.layer=='walls']),
                                geometry_hash([b for b in fb if b.layer=='walls']))
            self.assertTrue(validate(rough,rb)['valid'])
            self.assertTrue(validate(fine,fb)['valid'])


if __name__=='__main__':unittest.main(verbosity=2)
