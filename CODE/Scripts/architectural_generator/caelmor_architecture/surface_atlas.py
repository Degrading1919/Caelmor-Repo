"""Bake semantic surface fields into standard glTF PBR maps without mesh changes.

UV0 metric and UV1 lightmap coordinates remain editable. UV2 packs face charts
with gutters. A material bank is local to its geometry/settings fingerprint;
unchanged regeneration reuses datablocks (including user node edits).
"""
import hashlib
import json
import math
import numpy as np
from .materials import PALETTE, _palette_entry, _hash2
from .surface_detail import sample_detail,generate_normal_tile,DETAIL_PERIOD
from .surface_conditions import condition_fields, environment
from .benchmark_finish import (masonry_stock_tint, surface_base, uses_hewn_pigment,
                               uses_masonry_stock)
from .surface_pigments import masonry_pigment, timber_pigment
from .roof_pigments import TILE_BUFFERS, course_start, roof_pigment, course_pigment
from .surface_conditions import smooth

ATLAS_REVISION=2
UV_NAME='UV2_Surface'
DETAIL_UV='UV3_Detail'
FAMILY={'timber':'wood','timber_light':'wood','stone':'stone','stone_light':'stone',
        'mortar':'stone','stone_sooted':'stone','plaster':'plaster','plaster_patch':'plaster',
        'roof':'roof','roof_dark':'roof','roof_patch':'roof','roof_worn':'roof',
        'iron':'iron','bellows_leather':'leather','charcoal':'charcoal'}
PAD=2


def _components(mesh):
    """Connected pieces retain one stock grade across all their faces."""
    parent=list(range(len(mesh.vertices)))
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]];a=parent[a]
        return a
    for p in mesh.polygons:
        root=find(p.vertices[0])
        for v in p.vertices[1:]:parent[find(v)]=root
    groups={}
    for v in mesh.vertices:groups.setdefault(find(v.index),[]).append(tuple(v.co))
    centers={k:np.mean(v,axis=0) for k,v in groups.items()}
    return {p.index:centers[find(p.vertices[0])] for p in mesh.polygons}


def _charts(objects, density, course_edges=False):
    charts=[]
    course_cache={}
    for obj,host in objects:
        mesh=obj.data; uv=mesh.uv_layers['UV0_Metric']; pieces=_components(mesh)
        cover_tiles=course_edges and obj['caelm_buffer_id'].endswith(TILE_BUFFERS)
        for poly in mesh.polygons:
            ids=list(poly.loop_indices)
            coords=np.array([tuple(uv.data[i].uv) for i in ids],dtype=float)
            points=np.array([tuple(mesh.vertices[mesh.loops[i].vertex_index].co) for i in ids])
            low=coords.min(axis=0); span=coords.max(axis=0)-low
            if min(span)<1e-7: continue
            # Solve the existing metric projection in least squares, including
            # triangles/ngons; no guessed world height for sloped roof charts.
            transform=np.linalg.lstsq(np.column_stack((coords,np.ones(len(ids)))),points,rcond=None)[0]
            w,h=[max(1,min(256,int(math.ceil(float(s)*density)))) for s in span]
            charts.append(dict(obj=obj,poly=poly.index,loops=ids,coords=coords,low=low,span=span,
                transform=transform,normal=tuple(poly.normal),center=pieces[poly.index],
                w=w,h=h,host=host,
                course=course_start(host,points,poly.normal,course_cache) if cover_tiles else None))
    return sorted(charts,key=lambda c:(-c['h'],-c['w'],c['obj']['caelm_buffer_id'],c['poly']))


def _pack(charts):
    choices=[]
    for width in (256,512,1024,2048,4096):
        x=y=row=0;ok=True
        layout=[]
        for c in charts:
            w,h=c['w']+2*PAD,c['h']+2*PAD
            if w>width:ok=False;break
            if x+w>width:x=0;y+=row;row=0
            if y+h>4096:ok=False;break
            layout.append((x,y));x+=w;row=max(row,h)
        if ok:
            height=max(4,int(math.ceil((y+row)/4))*4)
            choices.append((width*height,width,height,layout))
    if choices:
        _,width,height,layout=min(choices,key=lambda c:(c[0],c[1]))
        for c,xy in zip(charts,layout):c['xy']=xy
        return width,height
    raise ValueError('Surface atlas exceeded 4096; reduce chart density')


def _image(name,pixels,colorspace):
    import bpy
    height,width,_=pixels.shape
    image=bpy.data.images.new(name,width=width,height=height,alpha=False,float_buffer=False)
    image.colorspace_settings.name=colorspace
    if colorspace=='sRGB':
        # Byte-backed Image.pixels are encoded values. Convert our linear
        # material albedo once; the shader/export importer decodes sRGB once.
        pixels=pixels.copy();rgb=pixels[:,:,:3]
        pixels[:,:,:3]=np.where(rgb<=.0031308,12.92*rgb,1.055*np.power(rgb,1./2.4)-.055)
    image.pixels.foreach_set(np.asarray(pixels,dtype=np.float32).ravel())
    image.file_format='PNG';image.pack()
    image['caelm_atlas_revision']=ATLAS_REVISION
    return image


def _make_material(key,fingerprint,base,images):
    import bpy
    mat=bpy.data.materials.new(f'Caelmor | {key} | Surface {fingerprint[:12]}')
    mat.use_nodes=True;nodes=mat.node_tree.nodes;links=mat.node_tree.links
    nodes.clear();output=nodes.new('ShaderNodeOutputMaterial');shader=nodes.new('ShaderNodeBsdfPrincipled')
    output.location=(650,0);shader.location=(360,0);links.new(shader.outputs['BSDF'],output.inputs['Surface'])
    shader.inputs['Base Color'].default_value=(1,1,1,1)
    uv=nodes.new('ShaderNodeUVMap');uv.uv_map=UV_NAME;uv.location=(-700,0)
    detail_uv=nodes.new('ShaderNodeUVMap');detail_uv.uv_map=DETAIL_UV;detail_uv.location=(-700,-200)
    textures=[]
    for i,(name,im) in enumerate(zip(('Base Color','Normal','ORM'),images)):
        tex=nodes.new('ShaderNodeTexImage');tex.image=im;tex.label=name
        tex.extension='REPEAT' if i==1 else 'EXTEND';tex.location=(-450,300-i*300)
        links.new((detail_uv if i==1 else uv).outputs['UV'],tex.inputs['Vector']);textures.append(tex)
    links.new(textures[0].outputs['Color'],shader.inputs['Base Color'])
    normal=nodes.new('ShaderNodeNormalMap');normal.space='TANGENT';normal.uv_map=DETAIL_UV
    normal.inputs['Strength'].default_value=1.;normal.location=(80,-100)
    links.new(textures[1].outputs['Color'],normal.inputs['Color']);links.new(normal.outputs['Normal'],shader.inputs['Normal'])
    separate=nodes.new('ShaderNodeSeparateColor');separate.mode='RGB';separate.location=(50,-370)
    links.new(textures[2].outputs['Color'],separate.inputs['Color'])
    links.new(separate.outputs['Green'],shader.inputs['Roughness'])
    links.new(separate.outputs['Blue'],shader.inputs['Metallic'])
    mat.diffuse_color=base
    mat['caelm_material']=key;mat['caelm_atlas_revision']=ATLAS_REVISION
    mat['caelm_surface_fingerprint']=fingerprint
    mat['caelm_surface_uv']=UV_NAME
    mat['caelm_detail_uv']=DETAIL_UV
    return mat


def _detail_image(family,settings):
    import bpy
    name=f'Caelmor Detail2 {family} {settings.region} {settings.craftsmanship}'
    found=bpy.data.images.get(name)
    if found is not None:return found
    pixels=generate_normal_tile(family,settings.region,settings.craftsmanship,resolution=256)
    image=_image(name,pixels,'Non-Color');image['caelm_shared_detail']=True
    return image


def apply_surfaces(objects,plan,settings,context_objects=None,*,roof_finish="BASELINE"):
    """Finish native objects; can recoat fixed geometry for controlled diagnostics.

    Production build calls this with its real settings. Diagnostic surface-only
    sweeps explicitly hold geometry fixed, rather than silently changing massing
    while attributing all differences to surface treatment.
    """
    import bpy
    if roof_finish not in ('BASELINE','PIGMENT','COURSES'):
        raise ValueError(f'Unsupported roof finish {roof_finish!r}')
    hosts={m.key:m.plan for m in getattr(plan,'world_zones',())}
    contexts={id(host):environment(host) for host in [plan,*hosts.values()]}
    for obj in (objects if context_objects is None else context_objects):
        if obj.type!='MESH' or obj.get('caelm_collider'):continue
        host=hosts.get(obj.get('caelm_world_zone'),plan)
        role=obj.get('caelm_functional_role','')
        if role not in ('forge_fire','chimney'):continue
        if role=='forge_fire' and obj.get('caelm_material')!='iron':continue
        points=np.asarray([tuple(obj.matrix_local @ v.co) for v in obj.data.vertices])
        low=points.min(axis=0);high=points.max(axis=0);center=(low+high)*.5
        if role=='forge_fire':
            contexts[id(host)].setdefault('heat',[]).append((float(center[0]),float(center[1]),float(high[2])))
        else:
            contexts[id(host)]['soot'].append((float(center[0]),float(center[1]),float(high[2])))
    groups={}
    for obj in objects:
        if obj.type!='MESH' or obj.get('caelm_collider'):continue
        key=obj.get('caelm_material','timber')
        if key not in FAMILY or obj.get('caelm_finish','').startswith('material:'):continue
        host=hosts.get(obj.get('caelm_world_zone'),plan)
        base=_palette_entry(key,getattr(host,'style',None),settings)[0]
        buffer_id=obj.get('caelm_buffer_id','')
        base=surface_base(key,buffer_id,settings,base)
        wall_stock=uses_masonry_stock(buffer_id,settings)
        groups.setdefault((key,base,wall_stock),[]).append((obj,host))
    reports=[]
    surface_settings={k:v for k,v in settings.__dict__.items() if k!='construction_overrides'}
    for (key,base,wall_stock),members in sorted(groups.items()):
        painted_roof=(FAMILY[key]=='roof' and roof_finish!='BASELINE'
                      and settings.world_aware
                      and (settings.region,settings.function) in (('LOWMARK','SMITHY'),('THORNFELL','GATEHOUSE')))
        course_edges=painted_roof and roof_finish=='COURSES'
        digest=hashlib.sha256()
        digest.update(json.dumps((ATLAS_REVISION,key,base,surface_settings),sort_keys=True).encode())
        if painted_roof:
            digest.update(f'roof pigment v1 {roof_finish}'.encode())
        hewn={obj.name for obj,_ in members if FAMILY[key]=='wood'
              and uses_hewn_pigment(obj.get('caelm_buffer_id',''),settings)}
        if wall_stock:
            digest.update(b'Thornfell masonry stock v1, pigment v1')
        if hewn:
            digest.update(b'Lowmark hewn pigment v1')
        for obj,host in members:
            digest.update(obj['caelm_buffer_id'].encode())
            digest.update(json.dumps(contexts[id(host)],sort_keys=True).encode())
            for v in obj.data.vertices:digest.update(np.asarray(v.co,dtype='<f4').tobytes())
            for p in obj.data.polygons:digest.update(np.asarray(p.vertices,dtype='<i4').tobytes())
            digest.update(np.asarray([tuple(v.uv) for v in obj.data.uv_layers['UV0_Metric'].data],dtype='<f4').tobytes())
        fingerprint=digest.hexdigest()
        material=next((m for m in bpy.data.materials if m.get('caelm_surface_fingerprint')==fingerprint),None)
        base_density={'wood':64,'stone':24,'roof':24,'plaster':32,'iron':32,'leather':48,'charcoal':16}[FAMILY[key]]
        density=base_density*{'LOW':.5,'MEDIUM':1.,'HIGH':1.5}[settings.detail]
        charts=_charts(members,density,course_edges);width,height_px=_pack(charts)
        for c in charts:
            mesh=c['obj'].data
            layer=mesh.uv_layers.get(UV_NAME) or mesh.uv_layers.new(name=UV_NAME)
            detail=mesh.uv_layers.get(DETAIL_UV) or mesh.uv_layers.new(name=DETAIL_UV)
            center=c['center']
            c['phase']=tuple(DETAIL_PERIOD*_hash2(int(round(center[0]*97))+offset,
                       int(round(center[1]*101))+int(round(center[2]*149)),settings.seed+offset)
                       for offset in (701,811))
            x,y=c['xy']
            for li,coord in zip(c['loops'],c['coords']):
                unit=(coord-c['low'])/c['span']
                layer.data[li].uv=((x+PAD+unit[0]*c['w'])/width,(y+PAD+unit[1]*c['h'])/height_px)
                detail.data[li].uv=((coord[0]+c['phase'][0])/DETAIL_PERIOD,(coord[1]+c['phase'][1])/DETAIL_PERIOD)
        if material is None:
            # Sample each material bank in one vector batch instead of invoking
            # procedural noise thousands of times for individual small stones.
            count=sum((c['w']+2*PAD)*(c['h']+2*PAD) for c in charts)
            positions=np.empty((count,3));normals=np.empty_like(positions)
            uu=np.empty(count);vv=np.empty(count);unit=np.empty(count);uz=np.empty(count)
            hewn_mask=np.zeros(count,dtype=np.uint8) if hewn else None
            start=0
            for c in charts:
                w,h=c['w'],c['h'];length=(w+2*PAD)*(h+2*PAD)
                fx=np.clip((np.arange(w+2*PAD)-PAD+.5)/w,0.,1.)
                fy=np.clip((np.arange(h+2*PAD)-PAD+.5)/h,0.,1.)
                u,v=np.meshgrid(c['low'][0]+fx*c['span'][0],c['low'][1]+fy*c['span'][1])
                end=start+length;uu[start:end]=u.ravel()+c['phase'][0];vv[start:end]=v.ravel()+c['phase'][1]
                positions[start:end]=np.column_stack((u.ravel(),v.ravel(),np.ones(length)))@c['transform']
                normals[start:end]=c['normal']
                center=c['center'];stock=_hash2(int(round(center[0]*107)),int(round(center[1]*107))+int(round(center[2]*149)),settings.seed)
                unit[start:end]=stock;uz[start:end]=center[2]
                if hewn and c['obj'].name in hewn:
                    long_span,cross_span=c['span']
                    # Real narrow longitudinal faces on the hewn frame and
                    # verge. Wide faces get pigment without the arris accent.
                    arris=cross_span<.055 and long_span>max(.16,4.*cross_span)
                    hewn_mask[start:end]=2 if arris else 1
                c['slice']=(start,end);start=end
            family=FAMILY[key]
            # Metric fields have unbounded coordinates. Stable world offsets
            # distinguish stock faces without resetting a knot every polygon.
            pattern=sample_detail(family,uu,vv,region=settings.region,craftsmanship=settings.craftsmanship)
            color=pattern['albedo']*np.asarray(base[:3])
            if wall_stock:
                tints=masonry_stock_tint([c['center'] for c in charts],settings.seed)
                for c,tint in zip(charts,tints):
                    start,end=c['slice']
                    color[start:end]*=tint
                color*=masonry_pigment(positions,normals,unit)
            if hewn:
                selected=hewn_mask>0
                color[selected]*=timber_pigment(uu[selected],vv[selected],unit[selected],
                                              hewn_mask[selected]==2,settings.craftsmanship)
            if painted_roof:
                color*=roof_pigment(positions,normals,settings.region,settings.seed)
            if course_edges:
                for c in charts:
                    if c['course'] is None:
                        continue
                    axis,direction,edge,row,has_butt=c['course']
                    start,end=c['slice']
                    distance=direction*(positions[start:end,axis]-edge)
                    lip=(1.-smooth(.006,.095,distance)) if has_butt else np.zeros(end-start)
                    lip*=.66+.34*unit[start:end]
                    row_stock=_hash2(row,axis*direction,settings.seed+911)
                    color[start:end]*=course_pigment(unit[start:end],row_stock,lip,settings.region)
            rough=pattern['roughness'].copy();metal=pattern['metallic'].copy()
            # Regions/material cohorts share textures but retain their actual
            # host volume's eaves, apertures and hearths.
            for host in {id(c['host']):c['host'] for c in charts}.values():
                idx=np.concatenate([np.arange(*c['slice']) for c in charts if c['host'] is host])
                fields=condition_fields(positions[idx],normals[idx],uu[idx],vv[idx],key,settings,contexts[id(host)],
                    unit=unit[idx],unit_z=uz[idx],family=family)
                silver=fields['silver'][:,None]
                color[idx]=(color[idx]*(1.-silver)+np.array([.16,.18,.165])*silver)*fields['tint']
                white=fields['white'][:,None]
                color[idx]=color[idx]*(1.-white)+np.array([.66,.63,.53])*white
                rust=fields['corrosion'][:,None]
                color[idx]=color[idx]*(1.-rust)+np.array([.23,.083,.026])*rust
                metal[idx]*=1.-fields['corrosion'];rough[idx]+=fields['roughness_delta']+.12*fields['corrosion']
            color=np.clip(color,0.,1.);rough=np.clip(rough,.24,.99)
            pixels=np.ones((height_px,width,4),dtype=np.float32)
            orm=np.ones_like(pixels);orm[:,:,1]=.9;orm[:,:,2]=0.
            for c in charts:
                x,y=c['xy'];w,h=c['w']+2*PAD,c['h']+2*PAD;s,e=c['slice']
                pixels[y:y+h,x:x+w,:3]=color[s:e].reshape(h,w,3)
                orm[y:y+h,x:x+w,1]=rough[s:e].reshape(h,w)
                orm[y:y+h,x:x+w,2]=metal[s:e].reshape(h,w)
            label=f'Caelmor Surface {fingerprint[:16]}'
            # Albedo is encoded once for byte-backed sRGB PNG; normal/ORM data
            # remain linear. The exported image payload is checked on reimport.
            # Roughness/metallic are broad condition signals; 2x area-filtered
            # maps share the exact normalized UV chart layout. Normal detail is
            # reusable at metric scale rather than copied into every face tile.
            compact_orm=orm.reshape(height_px//2,2,width//2,2,4).mean(axis=(1,3))
            images=(_image(label+' Color',pixels,'sRGB'),_detail_image(family,settings),
                    _image(label+' ORM',compact_orm,'Non-Color'))
            material=_make_material(key,fingerprint,base,images)
            material['caelm_atlas_size']=[width,height_px];material['caelm_texels_per_metre']=density
            material['caelm_orm_size']=[width//2,height_px//2]
        for obj,_ in members:
            obj.data.materials.clear();obj.data.materials.append(material)
            obj['caelm_surface_material']=material.name
            obj['caelm_surface_fingerprint']=fingerprint
            # Conditions are already in the PBR map. Neutral COLOR_0 prevents
            # exporters multiplying the old vertex weathering a second time.
            tint=obj.data.color_attributes.get('CaelmorTint')
            if tint:
                tint.data.foreach_set('color',np.ones(len(tint.data)*4,dtype=np.float32))
            obj.data.uv_layers.active_index=0;obj.data.uv_layers[0].active_render=True
        reports.append({'material':key,'fingerprint':fingerprint,'size':[width,height_px],'density':density,
                        'orm_size':[width//2,height_px//2],'normal_size':[256,256],'shared_normal':True,
                        'charts':len(charts),'objects':len(members)})
    return reports
