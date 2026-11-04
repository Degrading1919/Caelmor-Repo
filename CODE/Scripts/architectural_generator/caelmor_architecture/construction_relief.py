"""Repeatable construction relief for broad roof and masonry fields."""
import numpy as np

from .surface_detail import DETAIL_PERIOD, sample_detail

SIZE = 512
ROOFS = ('shingle', 'slate', 'clay')


def _edge(value, low, high):
    x=np.clip((value-low)/(high-low),0.,1.)
    return x*x*(3.-2.*x)


def _unit(ix, iy, salt):
    # Integer coordinates are explicitly periodic across this four-course tile.
    value=np.sin((ix%4)*127.1+(iy%4)*311.7+salt*74.7)*43758.5453
    return value-np.floor(value)


def field_maps(kind, craftsmanship, weather, base):
    """Build repeatable original albedo, height-derived normals and packed ORM."""
    coord=(np.arange(SIZE)+.5)*4/SIZE
    u,v=np.meshgrid(coord,coord)
    roof=kind in ROOFS
    craft={'FINE':.62,'STANDARD':1.,'ROUGH':1.27}[craftsmanship]
    pi=np.pi
    # Related courses remain recognizable at distance. Offset beds vary
    # modestly within their row and repeat continuously through the texture.
    shift={'rubble':.095,'level':.022,'dressed':.012,
           'shingle':.048,'slate':.023,'clay':.019}[kind]*craft
    vv=v+shift*(np.sin(2*pi*u/4)+.25*np.sin(2*pi*(u/2+v/4)))
    row=np.floor(vv).astype(int)
    fv=vv-row
    uu=u+(row%2)*(.25 if kind=='clay' else .5)
    uu+=shift*.46*np.sin(2*pi*(v/4+row/4))
    col=np.floor(uu).astype(int)
    fu=uu-col
    unit=_unit(col,row,1)
    gauge=(.80+.30*unit)
    # Sloping fractures and chips sit against a course or vertical joint.
    # They remain narrower on slate and dressed masonry.
    chip_depth={'rubble':.14,'level':.075,'dressed':.049,'shingle':.14,'slate':.08,'clay':.054}[kind]
    chip=(chip_depth*craft*(.7+.3*weather)
          *np.maximum(0.,1.-np.minimum(fu,1.-fu)*6.)
          *(_unit(col,row,3)<.38))
    top=fv-chip
    side=np.minimum(fu,1.-fu)
    if roof:
        # Wood wedges thin upslope; flat slate has shallow seating and clay
        # lifts through the middle section. All three keep a physical lap.
        side_mask=_edge(side,.006,.033 if kind!='clay' else .056)
        face=_edge(top,.009,.072)*side_mask
        if kind=='clay':
            profile=(.010+.020*np.sin(pi*fu)**1.6)*(.94-.30*fv)
        elif kind=='slate':
            profile=.012*(1.-.66*fv)
        else:
            profile=.023*(1.-.70*fv)
        height=face*profile*gauge
        relief=1.-face
        roughness={'clay':.72,'slate':.84,'shingle':.90}[kind]
        micro=sample_detail('wood' if kind=='shingle' else 'roof',
                            u*DETAIL_PERIOD/4,v*DETAIL_PERIOD/4,
                            craftsmanship=craftsmanship)['albedo']
        scale=(1.28,1.5)
    else:
        side_mask=_edge(side,.014,.049 if kind=='rubble' else .034)
        beds=_edge(top,.023,.111 if kind=='rubble' else .071)*_edge(1.-fv,.022,.085)
        face=beds*side_mask
        crown=.90+.10*np.sin(pi*fu)*np.sin(pi*fv)
        height=face*crown*gauge*(.025 if kind=='rubble' else .017)
        relief=1.-face
        roughness=.91
        micro=sample_detail('stone',u*DETAIL_PERIOD/4,v*DETAIL_PERIOD/4,
                            craftsmanship=craftsmanship)['albedo']
        scale=(3.92,1.52)
    # Albedo carries restrained unit stock and contact occlusion. Lighting
    # direction and relief are left to the tangent-space normals.
    stock=(unit-.5)*(.23 if kind in ('shingle','rubble') else .17)
    tide=.055*weather*np.sin(2*pi*(u/4+v/2))
    rgb=np.asarray(base[:3])[None,None,:]*micro.reshape(SIZE,SIZE,3)*(1.+stock+tide)[...,None]
    if not roof:
        mineral=(_unit(col,row,7)*2.-1.)*.75
        rgb*=1.+mineral[...,None]*np.array([.14,.028,-.115])
    mortar=np.asarray(base[:3])*(.48 if roof else .62)
    rgb=rgb*(1.-relief[...,None]*.76)+mortar*relief[...,None]*.76
    gx=(np.roll(height,-1,axis=1)-np.roll(height,1,axis=1))*SIZE/(2*scale[0])
    gy=(np.roll(height,-1,axis=0)-np.roll(height,1,axis=0))*SIZE/(2*scale[1])
    normal=np.stack((-gx,-gy,np.ones_like(height)),axis=2)
    normal/=np.linalg.norm(normal,axis=2,keepdims=True)
    albedo=np.ones((SIZE,SIZE,4),dtype=np.float32)
    normals=np.ones_like(albedo)
    orm=np.ones_like(albedo)
    albedo[:,:,:3]=np.clip(rgb,0.,1.)
    normals[:,:,:3]=normal*.5+.5
    orm[:,:,0]=1.-.36*relief
    orm[:,:,1]=np.clip(roughness+.10*relief+.04*weather+stock*.11,0.,1.)
    orm[:,:,2]=0.
    return albedo,normals,orm.reshape(SIZE//2,2,SIZE//2,2,4).mean(axis=(1,3))
