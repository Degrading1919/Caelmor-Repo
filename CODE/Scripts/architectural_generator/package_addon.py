"""Build reproducible Blender extension ZIP, without external dependencies."""
from pathlib import Path
import hashlib
import zipfile

ROOT=Path(__file__).resolve().parent


def package(destination=None):
    destination=Path(destination) if destination else ROOT/'dist'/'caelmor_architecture.zip'
    destination.parent.mkdir(parents=True,exist_ok=True)
    source=ROOT/'caelmor_architecture'
    members={p.name:p for p in source.iterdir() if p.is_file() and p.suffix in ('.py','.toml')}
    members['LICENSE']=source/'LICENSE'
    for name in ('README.md','THIRD_PARTY.md','Caelmor_Architectural_Generator_Research.md'):
        members[name]=ROOT/name
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,path in sorted(members.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,11,2,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            archive.writestr(info,path.read_bytes())
    return destination,hashlib.sha256(destination.read_bytes()).hexdigest()


if __name__=='__main__':
    print(*package(),sep='\n')
