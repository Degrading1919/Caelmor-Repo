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


def run(blender, export=None):
    archive,_=package()
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
assert bpy.ops.caelmor.generate()=={'FINISHED'}
collection=next(c for c in bpy.data.collections if c.get('caelm_build'))
meshes=[o for o in collection.objects if o.get('caelm_generated') and not o.get('caelm_collider')]
assert len(meshes)>=15,len(meshes)
assert all(len(o.data.uv_layers)==2 for o in meshes)
print('ISOLATED_EXTENSION_INSTALL_AND_GENERATE_PASS',len(meshes))
"""
        if export is not None:
            export=Path(export).resolve()
            export.parent.mkdir(parents=True,exist_ok=True)
            expression+=f"\nassert bpy.ops.caelmor.export(filepath={str(export)!r})=={{'FINISHED'}}\n"
        call(['--background','--python-exit-code','1','--python-expr',expression])
    return {'installed_archive':str(archive),'native_install_and_generate':True,'isolated_preferences':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--blender',default=r'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe')
    parser.add_argument('--export',help='Optionally retain a generated GLB for inspection')
    args=parser.parse_args()
    print(json.dumps(run(Path(args.blender),args.export),indent=2))
