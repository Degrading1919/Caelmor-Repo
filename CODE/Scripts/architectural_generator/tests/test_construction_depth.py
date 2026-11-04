"""Compatibility and geometry gates for optional mapped construction depth."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parent)]
from caelmor_architecture.engine import generate, geometry_hash, validate
from test_construction_treatments import fixture
from test_construction_library import overrides
from test_world import _ray_hits


def case(function, mode=None, stock=None):
    roof=function=='SMITHY'
    opts=overrides('timber_shingle') if roof else {'by_role':{}}
    role='roof_cover' if roof else 'wall_body'
    if mode:
        opts['by_role'].setdefault(role,{})['representation']=mode
    if stock:
        opts['by_role'][role].update(treatment='slate_tile_roofing',substrate=stock)
    return fixture('LOWMARK' if roof else 'THORNFELL',function,construction_overrides=opts)


class DepthTests(unittest.TestCase):
    def test_geometry_and_semantics(self):
        for function,layer in (('SMITHY','roof'),('GATEHOUSE','walls')):
            counts=[]
            old=None
            for mode in (None,'HYBRID','TEXTURE'):
                settings=case(function,mode)
                plan,meshes=generate(settings)
                report=validate(plan,meshes)
                self.assertTrue(report['valid'],report['errors'])
                self.assertEqual(geometry_hash(meshes),geometry_hash(generate(settings)[1]))
                counts.append(report['triangles'])
                fields=[b for b in meshes if b.field_family]
                self.assertEqual(bool(fields),bool(mode))
                if mode:
                    self.assertEqual(plan.functional_program,old[0].functional_program)
                    unchanged={b.name:b for b in old[1] if b.layer!=layer or
                               b.name.endswith(('curtain_return.east','curtain_return.west'))}
                    for b in meshes:
                        if b.name in unchanged:
                            self.assertEqual(geometry_hash([b]),geometry_hash([unchanged[b.name]]))
                    for b in fields:
                        self.assertEqual(b.construction.representation,mode)
                        self.assertEqual(len(b.field_uv),sum(map(len,b.faces)))
                    if function=='GATEHOUSE':
                        portal=plan.world_zones[0]
                        x0,y0,x1,y1=portal.bounds
                        for height in (1.6,2.86,3.22):
                            self.assertFalse(_ray_hits(((x0+x1)/2,y0-.5,portal.base+height),
                                                       (0,1,0),y1-y0+1,meshes))
                else:
                    old=plan,meshes
            self.assertGreater(counts[0],counts[1])
            self.assertGreater(counts[1],counts[2])

    def test_cover_stock_and_finish_keep_their_roles(self):
        for stock,family in (('slate','slate'),('fired_clay','clay')):
            s=case('SMITHY','HYBRID',stock)
            p,b=generate(s)
            self.assertTrue(validate(p,b)['valid'])
            self.assertEqual({mesh.field_family for mesh in b if mesh.field_family},{family})
            opts=s.construction_overrides
            opts['by_role']['roof_cover']['finish']='material:Reviewed artist'
            _,finished=generate(s,finish_names=('Reviewed artist',))
            self.assertEqual(geometry_hash(b),geometry_hash(finished))

    def test_incompatible_representation_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'requires Efficient'):
            generate(replace(case('SMITHY','HYBRID'),geometry_mode='SOLID'))
        opts={'by_component':{'gatehouse_west_watchtower/curtain_return':{'representation':'TEXTURE'}}}
        with self.assertRaisesRegex(ValueError,'requires modeled'):
            generate(replace(case('GATEHOUSE'),construction_overrides=opts))


if __name__=='__main__':
    unittest.main(verbosity=2)
