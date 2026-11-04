"""Install and execute the distributable in isolated Blender user directories.

Does not modify the user's Blender preferences or installed extensions.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import tempfile
from package_addon import package


def run(blender, export=None, region='LOWMARK', function='FARMHOUSE', geometry_mode='SOLID',world_aware=True):
    archive,archive_hash=package()
    with tempfile.TemporaryDirectory(prefix='caelmor_install_') as directory:
        target=Path(directory).resolve()
        assert target.parent==Path(tempfile.gettempdir()).resolve()
        env=os.environ.copy()
        for variable,name in [('BLENDER_USER_CONFIG','config'),('BLENDER_USER_SCRIPTS','scripts'),('BLENDER_USER_EXTENSIONS','extensions')]:
            path=target/name
            path.mkdir()
            env[variable]=str(path)
        def call(args):
            result=subprocess.run([str(blender),*args],env=env,text=True,capture_output=True)
            print(result.stdout)
            if result.returncode:
                raise RuntimeError(result.stderr or f'Blender failed with exit {result.returncode}')
        call(['--factory-startup','--command','extension','repo-add','caelmor_test',
              '--name','Isolated Caelmor Test','--directory',str(target/'repo'),'--clear-all'])
        call(['--command','extension','install-file','--repo','caelmor_test','--enable',str(archive)])
        expression="""import bpy
assert hasattr(bpy.ops.caelmor,'generate')
"""
        expression+=f"""props=bpy.context.scene.caelmor_settings
props.caelm_region={region!r}
props.caelm_function={function!r}
props.caelm_geometry_mode={geometry_mode!r}
props.caelm_world_aware={world_aware!r}
"""
        expression+="""
import json
assert bpy.ops.caelmor.generate()=={'FINISHED'}
collection=next(c for c in bpy.data.collections if c.get('caelm_build'))
saved_settings=json.loads(collection['caelm_settings'])
assert saved_settings['crafted_curves'] is True and saved_settings['seed_massing'] is True
meshes=[o for o in collection.objects if o.get('caelm_generated') and not o.get('caelm_collider')]
assert len(meshes)>=15,len(meshes)
assert all('UV0_Metric' in o.data.uv_layers and 'UV1_Lightmap' in o.data.uv_layers for o in meshes)
assert any('UV2_Surface' in o.data.uv_layers for o in meshes)
print('ISOLATED_EXTENSION_INSTALL_AND_GENERATE_PASS',len(meshes))
"""
        if world_aware and function in ('SMITHY','MARKET_HALL','STABLE','GATEHOUSE'):
            expression+=f"""import json
program=json.loads(collection['caelm_functional_program'])
assert program['function']=={function!r},program
assert program['routes'] and program['rooms']
print('ISOLATED_FUNCTIONAL_PROGRAM_PASS',program['function'])
"""
        if export is not None:
            export=Path(export).resolve()
            export.parent.mkdir(parents=True,exist_ok=True)
            expression+=f"\nassert bpy.ops.caelmor.export(filepath={str(export)!r})=={{'FINISHED'}}\n"
        call(['--background','--python-exit-code','1','--python-expr',expression])
    return {'installed_archive':str(archive),'archive_sha256':archive_hash,
            'native_install_and_generate':True,'isolated_preferences':True,
            'region':region,'building_type':function,'geometry_mode':geometry_mode,'world_aware':world_aware}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--blender',default=r'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe')
    parser.add_argument('--export',help='Optionally retain a generated GLB for inspection')
    from caelmor_architecture.profiles import REGIONS, TYPE_SPECS
    parser.add_argument('--region',choices=tuple(REGIONS),default='LOWMARK')
    parser.add_argument('--function',choices=tuple(TYPE_SPECS),default='FARMHOUSE')
    parser.add_argument('--geometry-mode',choices=('SOLID','EFFICIENT'),default='SOLID')
    parser.add_argument('--report',help='Optionally retain the tested archive hash and settings as JSON')
    parser.add_argument('--legacy',action='store_true',help='Verify the preserved legacy architecture mode')
    args=parser.parse_args()
    result=run(Path(args.blender),args.export,args.region,args.function,args.geometry_mode,not args.legacy)
    if args.report:
        Path(args.report).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
