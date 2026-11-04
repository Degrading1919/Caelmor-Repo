"""Reusable assembly, workfront sightline, and stable route checks."""
from dataclasses import replace
from math import dist
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest

sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
from caelmor_architecture.construction_library import ASSEMBLIES, authored_overrides, replace_choice
from caelmor_architecture.engine import generate, geometry_hash, validate
from test_construction_treatments import fixture
from test_world import _ray_hits

PRESETS = {
    'timber_shingle': dict(foundation='broken_course',supports='hewn',
                           enclosure='board',rafters='hewn',cover='wood'),
    'render_slate': dict(foundation='level_course',supports='squared',
                         enclosure='lime',rafters='squared',cover='slate'),
    'earth_clay': dict(foundation='dressed',supports='hewn',
                       enclosure='earth',rafters='squared',cover='clay'),
}


def overrides(preset):
    roles={}
    for name,choice in PRESETS[preset].items():
        role,_,options=ASSEMBLIES[name]
        replace_choice(roles,role,options,choice)
    return {'by_role':roles}


def front_hits(target, buffers):
    origin=(1.47,-2.4,1.97)
    length=dist(origin,target)
    direction=tuple((x-y)/length for x,y in zip(target,origin))
    return _ray_hits(origin,direction,length+.03,buffers)


class ConstructionLibraryTests(unittest.TestCase):
    def test_three_assemblies_reuse_the_same_work_program(self):
        roles_by_function = {}
        for function in ('SMITHY','STABLE'):
            route_reference = None
            hashes = set()
            roles_by_function[function]=set()
            for preset in PRESETS:
                s=fixture(function=function,construction_overrides=overrides(preset))
                plan, meshes=generate(s)
                report=validate(plan,meshes)
                self.assertTrue(report['valid'],report['errors'])
                self.assertEqual(geometry_hash(meshes),geometry_hash(generate(s)[1]))
                hashes.add(geometry_hash(meshes))
                roles_by_function[function].update(b.construction.component_role for b in meshes if b.construction)
                routes=plan.functional_program['routes']
                if route_reference is None:
                    route_reference=routes
                self.assertEqual(routes,route_reference)
                if function=='SMITHY':
                    top=plan.world_zones[0].base+.91
                    for target in ((.83,.72,top),(1.46,.71,top),(2.15,.70,top)):
                        hits=front_hits(target,meshes)
                        self.assertTrue(hits,target)
                        self.assertIn(hits[0][1].functional_role,('forge_fire',),[b.name for _,b in hits[:4]])
            self.assertEqual(len(hashes),len(PRESETS))
        self.assertTrue({'plinth','frame_member','roof_support','wall_infill','roof_cover'} <=
                        roles_by_function['SMITHY'] & roles_by_function['STABLE'])

    def test_role_and_component_errors(self):
        s=fixture(construction_overrides={'by_role':{'roof_support':{'variant':'broken_course'}}})
        with self.assertRaisesRegex(ValueError,'roof_support.*variant'):
            generate(s)
        # A reed roof has its own separate assembly and cannot silently become
        # a timber-shingle system through the classified cover role.
        s=fixture(region='MIRE',function='FARMHOUSE',
                  construction_overrides={'by_role':{'roof_cover':{'substrate':'split_wood'}}})
        with self.assertRaisesRegex(ValueError,'roof_cover'):
            generate(s)

    def test_ui_overlay_preserves_unrepresented_fields(self):
        original={'by_component':{'forge_hall/roof_cover':{'substrate':'slate'}},
                  'by_role':{'plinth':{'substrate':'fieldstone'},'wall_infill':{'finish':'procedural'}}}
        props=SimpleNamespace(caelm_edit_finish=False,caelm_finish_role='wall_infill',
                              **{'caelm_assembly_'+name:'AUTO' for name in ASSEMBLIES})
        self.assertEqual(authored_overrides(props,original),original)
        props.caelm_assembly_foundation='level_course'
        result=authored_overrides(props,original)
        self.assertEqual(result['by_role']['plinth'],
                         {'treatment':'stone_masonry','variant':'level_course','substrate':'fieldstone'})
        self.assertEqual(result['by_component'],original['by_component'])
        self.assertEqual(original['by_role']['plinth'],{'substrate':'fieldstone'})


if __name__=='__main__':
    unittest.main(verbosity=2)
