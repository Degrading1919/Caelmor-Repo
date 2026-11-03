"""Open working ranges need a clear two-metre approach, despite having no door."""
from pathlib import Path
import sys
import unittest
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parent)]
from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate,validate
from test_world import _ray_hits


class WorkAccessTests(unittest.TestCase):
    def test_stair_route_is_not_a_post_or_diagonal_bay(self):
        for function in ('COTTAGE','FARMHOUSE','BARN','WAREHOUSE'):
            for wealth in ('MODEST','ESTABLISHED'):
                with self.subTest(function=function,wealth=wealth):
                    plan,buffers=generate(Settings(function=function,region='LOWMARK',wealth=wealth,
                        seed=91,detail='MEDIUM',geometry_mode='EFFICIENT',world_aware=True,use_grammar=True))
                    wing=next(m for m in plan.world_zones if m.key=='lowmark_service_wing')
                    members=[b for b in buffers if getattr(b,'world_zone',None)==wing.key
                             and b.layer in ('structure','details')]
                    x0,y0,x1,y1=wing.bounds
                    for offset in (-.6,0.,.6):
                        for height in (1.,1.9,2.):
                            hits=_ray_hits(((x0+x1)*.5+offset,y0-.45,wing.base+height),
                                           (0,1,0),.9,members)
                            self.assertFalse(hits,(function,wealth,offset,height,[h[1].name for h in hits[:3]]))
                    self.assertTrue(validate(plan,buffers)['valid'])


if __name__=='__main__':unittest.main(verbosity=2)
