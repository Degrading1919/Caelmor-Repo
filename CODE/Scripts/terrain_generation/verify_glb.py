"""Independently compare exported GLB vertices to every authoritative terrain sample."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import numpy as np


def verify(arrays, glb):
    with np.load(arrays,allow_pickle=False) as data:
        local="height_engineered" not in data.files
        z=data["height"] if local else data["height_engineered"]
        x=data["x"]; y=data["y"]
    raw=glb.read_bytes()
    if struct.unpack_from("<II",raw,0)!=(0x46546c67,2): raise AssertionError("GLB2 header")
    length,kind=struct.unpack_from("<II",raw,12)
    if kind!=0x4e4f534a: raise AssertionError("GLB JSON")
    doc=json.loads(raw[20:20+length]); start=20+length
    bin_size,kind=struct.unpack_from("<II",raw,start)
    if kind!=0x004e4942: raise AssertionError("GLB BIN")
    binary=memoryview(raw)[start+8:start+8+bin_size]
    if len(doc["meshes"])!=1 or len(doc["meshes"][0]["primitives"])!=1: raise AssertionError("One technical terrain mesh expected")
    primitive=doc["meshes"][0]["primitives"][0]
    accessor=doc["accessors"][primitive["attributes"]["POSITION"]]
    view=doc["bufferViews"][accessor["bufferView"]]
    if accessor["componentType"]!=5126 or accessor["type"]!="VEC3": raise AssertionError("Float3 positions required")
    offset=view.get("byteOffset",0)+accessor.get("byteOffset",0)
    positions=np.ndarray((accessor["count"],3),dtype="<f4",buffer=binary,offset=offset,strides=(view.get("byteStride",12),4))
    columns=np.rint((positions[:,0]-x[0])/(x[1]-x[0])).astype(int)
    rows=np.rint((-positions[:,2]-y[0])/(y[1]-y[0])).astype(int)
    if positions.shape[0]!=z.size or np.any(columns<0) or np.any(columns>=len(x)) or np.any(rows<0) or np.any(rows>=len(y)): raise AssertionError("Full-resolution world extent/vertex count changed")
    if len(np.unique(rows*len(x)+columns))!=z.size: raise AssertionError("Export omitted or duplicated a grid sample")
    error=float(np.max(np.abs(positions[:,1]-z[rows,columns])))
    if error>0.00002: raise AssertionError("Exported elevation precision changed")
    np.testing.assert_allclose(positions[:,0],x[columns],atol=0.00001,rtol=0)
    np.testing.assert_allclose(positions[:,2],-y[rows],atol=0.00001,rtol=0)
    triangles=doc["accessors"][primitive["indices"]]["count"]//3
    if triangles!=2*(len(x)-1)*(len(y)-1): raise AssertionError("Full-resolution face count changed")
    if local:
        indices_accessor=doc["accessors"][primitive["indices"]]
        indices_view=doc["bufferViews"][indices_accessor["bufferView"]]
        dtype={5123:"<u2",5125:"<u4"}[indices_accessor["componentType"]]
        offset=indices_view.get("byteOffset",0)+indices_accessor.get("byteOffset",0)
        indices=np.frombuffer(binary,dtype=dtype,count=indices_accessor["count"],offset=offset).reshape(-1,3)
        rr,cc=rows[indices],columns[indices]
        r0,c0=rr.min(axis=1),cc.min(axis=1)
        if not np.all((rr.max(axis=1)-r0==1)&(cc.max(axis=1)-c0==1)):
            raise AssertionError("A local triangle skips grid samples")
        sw=((rr==r0[:,None])&(cc==c0[:,None])).any(axis=1)
        ne=((rr==r0[:,None]+1)&(cc==c0[:,None]+1)).any(axis=1)
        if not np.all(sw&ne): raise AssertionError("Local mesh no longer uses the verified SWNE surface")
        nw=((rr==r0[:,None]+1)&(cc==c0[:,None])).any(axis=1)
        codes=(r0*(len(x)-1)+c0)*2+nw
        if len(np.unique(codes))!=triangles: raise AssertionError("Local faces duplicated or omitted")
        signed=(cc[:,1]-cc[:,0])*(rr[:,2]-rr[:,0])-(rr[:,1]-rr[:,0])*(cc[:,2]-cc[:,0])
        if not np.all(signed>0): raise AssertionError("Local terrain winding faces below ground")
    return {"vertices":int(z.size),"triangles":triangles,"maximum_elevation_error_m":error,
            "axes":"GLB east X / elevation Y / minus north Z; Blender east X / north Y / elevation Z",
            "glb_bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
            "scope":"Every vertex checked; local meshes also verify all SWNE faces and upward winding. No Unity import is implied."}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--arrays",type=Path,required=True); p.add_argument("--glb",type=Path,required=True); p.add_argument("--report",type=Path,required=True)
    a=p.parse_args(); report=verify(a.arrays,a.glb); a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print("CAELMOR_TERRAIN_GLB_VERIFIED "+json.dumps(report))
