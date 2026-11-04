"""Original periodic value and relief baselines for the Caelmor painting library."""
from hashlib import blake2b

import numpy as np


def seed_for(value):
    return int.from_bytes(blake2b(value.encode(), digest_size=8).digest(), 'little')


def ease(low, high, value):
    t = np.clip((value-low)/(high-low), 0., 1.)
    return t*t*(3.-2.*t)


class Sample:
    def __init__(self, size, identity):
        axis = (np.arange(size, dtype=np.float32)+.5)/size
        self.x, self.y = np.meshgrid(axis, axis)
        self.seed = seed_for(identity)
        self.identity = identity

    def noise(self, nx, ny, salt=0, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        lattice = np.random.default_rng(self.seed+salt).uniform(-1, 1, (ny, nx)).astype(np.float32)
        fx, fy = x*nx, y*ny
        ix, iy = np.floor(fx).astype(int), np.floor(fy).astype(int)
        a, b = ease(0., 1., fx-ix), ease(0., 1., fy-iy)
        top = lattice[iy%ny, ix%nx]*(1.-a)+lattice[iy%ny, (ix+1)%nx]*a
        bottom = lattice[(iy+1)%ny, ix%nx]*(1.-a)+lattice[(iy+1)%ny, (ix+1)%nx]*a
        return top*(1.-b)+bottom*b

    def stock(self, ix, iy, nx, ny, salt):
        cells = np.random.default_rng(self.seed+salt).uniform(-1, 1, (ny, nx))
        return cells[iy%ny, ix%nx]

    def grain(self, n, knots=2, across=False):
        u, v = (self.y, self.x) if across else (self.x, self.y)
        path = u+.028*self.noise(4, 3, 12, u, v)+.010*self.noise(8, 6, 13, u, v)
        growth = np.zeros_like(u)
        for cx, cy in np.random.default_rng(self.seed+14).random((knots,2)):
            dx,dy=(u-cx+.5)%1-.5,(v-cy+.5)%1-.5
            growth+=np.exp(-((dx/.045)**2+(dy/.115)**2))
            path+=.033*np.tanh(dx/.014)*np.exp(-((dy/.15)**2+(dx/.09)**2))
        line=np.sin(2*np.pi*n*path)
        secondary=np.sin(2*np.pi*(n+13)*(path+.012*self.noise(5,6,16,u,v)))
        band=.61+.39*self.noise(7,3,17,u,v)
        return .33*line*band+.22*secondary+.38*self.noise(38,4,15,u,v)-.52*growth


def _courses(s, motif, nx, ny):
    wood=any(w in motif for w in ('shingle','shake'))
    slate='slate' in motif
    clay=any(w in motif for w in ('clay','pantile','interlocking_pan'))
    roofing=wood or slate or clay
    ashlar='ashlar' in motif or 'level' in motif or 'sett' in motif
    drift=.030 if ashlar or slate else .085
    if 'shake' in motif or 'dry_stack' in motif:
        drift*=1.7
    v=s.y*ny+drift*s.noise(5,ny,20)
    row=np.floor(v).astype(int)
    y=v-row
    u=s.x*nx+.5*(row%2)+drift*s.noise(5,ny,21)
    col=np.floor(u).astype(int)
    x=u-col
    density={'split_oak_shingle':34,'pine_shingle':26,'cedar_shingle':56,
             'split_oak_shake':29}.get(s.identity,max(nx*8,28))
    grain=s.grain(density,2 if 'pine' in s.identity else 1)
    stock=s.stock(col,row,nx,ny,22)
    chipped=(.06 if 'cedar' in s.identity else .22 if 'shake' in motif else .08 if slate else .16)
    broken=(stock>.47)*(1-ease(.00,.28,np.minimum(x,1-x)))*chipped
    horizontal=ease(.016,.079 if ashlar else .12,y-broken)
    side=ease(.013,.051 if slate or ashlar else .083,np.minimum(x,1-x))
    if roofing:
        shape=horizontal*side
        if 'interlocking_pan' in motif:
            profile=.20+.54*np.sin(np.pi*x)**2+.19*np.exp(-((x-.86)/.068)**2)
        elif clay:
            profile=(.28+.62*np.sin(np.pi*x)**1.8 if 'pan' in motif else .58*(1-.42*y))
        else:
            profile=(.76 if wood else .58)*(1.-.68*y)
        h=shape*(profile+.055*grain+.06*stock)
        tone=.36+shape*(.26+.085*stock+(.10*grain if wood else .056*s.noise(11,14,23)))
        tone+=.028*(1.-ease(.07,.20,y))*shape
    else:
        shape=horizontal*ease(.016,.09,1.-y)*side
        h=shape*(.58+.12*stock+.075*s.noise(20,21,23))
        tone=.32+shape*(.30+.12*stock+.11*s.noise(10,11,24))
        if s.identity in ('volcanic_basalt','volcanic_tuff','ashlar_granite','hewn_sandstone'):
            if s.identity=='hewn_sandstone':
                mineral=s.noise(6,58,27)
            elif s.identity=='volcanic_basalt':
                mineral=s.noise(43,12,27)
            else:
                mineral=s.noise(52,47,27)
            tone+=shape*.087*mineral
            h+=shape*.094*mineral
        if 'cobble' in motif and s.identity!='flagstone':
            roundness=ease(.49,.23, np.hypot(x-.5,y-.5))
            h*=roundness
            tone-=.10*(1-roundness)*shape
    return tone,h,1.-shape


def _timber(s, motif, nx, ny):
    cross='horizontal' in motif or 'weatherlap' in motif
    u=s.y if cross else s.x
    n=ny if cross else nx
    width={'hewn_oak':27,'spruce_pole':46,'ash_beam':34,'oak_boarding':33,
           'pine_boarding':21}.get(s.identity,max(24,n*7))
    knots=3 if 'pine' in s.identity or 'spruce' in s.identity else 1
    grain=s.grain(width,knots,cross)
    if 'end_grain' in motif or s.identity=='end_grain_block':
        u,v=s.x*nx,s.y*ny
        ix,iy=np.floor(u).astype(int),np.floor(v).astype(int)
        offset=s.stock(ix,iy,nx,ny,34)
        u,v=u-ix,v-iy
        distance=np.hypot(u-.51-.12*offset,(v-.48+.10*offset)*(.91+.16*offset))
        circles=np.sin(2*np.pi*(distance*(10.5+2.3*offset)+.20*s.noise(8,9,33)))
        face=ease(.022,.084,np.minimum.reduce([u,1-u,v,1-v]))
        return .36+face*(.24+.12*circles+.07*grain),face*(.52+.14*circles),1-face
    if s.identity in ('oak_wainscot','pegged_oak_frame'):
        u,v=s.x*nx%1,s.y*ny%1
        sides=np.minimum(u,1-u)
        rails=np.minimum(v,1-v)
        rail=1-ease(.088,.144,rails)
        stile=1-ease(.078,.128,sides)
        join=np.maximum(rail,stile)
        grain=np.where(rail>stile,s.grain(37,1,True),grain)
        panel=ease(.165,.225,np.minimum(sides,rails))
        pegs=np.zeros_like(u)
        if s.identity=='pegged_oak_frame':
            pegs=1-ease(.032,.059,np.hypot((sides-.073)*1.4,rails-.075))
        tone=.54+.10*grain+.11*join+.07*panel-.12*pegs
        return tone,.34+.34*join+.12*panel+.08*grain+.13*pegs,1-join
    if 'steam' in motif:
        bent=np.sin(2*np.pi*(s.x*26+.36*np.cos(2*np.pi*s.y)))+.35*grain
        return .58+.15*bent,.53+.18*bent,np.maximum(0,-bent)*.43
    if 'scarf' in motif:
        z=(s.y*ny+(s.x*nx)%1*.64)%1
        seam=ease(.009,.048,np.minimum(z,1-z))
        return .38+seam*(.25+.12*grain),.33+seam*(.29+.10*grain),1-seam
    if 'grain' in motif or 'bark' in motif:
        rind='bark' in motif
        cut=s.noise(18,5,28)
        grooves=np.maximum(0.,-.1-grain)**1.6
        return .58+.19*grain+.11*cut-(.12*grooves if rind else 0), .50+.24*grain+.13*cut, grooves
    phase=(u*n+.075*s.noise(n,4,31))%1
    joint=ease(.009,.066,np.minimum(phase,1-phase))
    ridge=(.7+.18*np.cos(2*np.pi*phase) if cross else .75)
    if 'batten' in motif:
        batten=1-ease(.11,.18,np.minimum(phase,1-phase))
        return .40+.23*joint+.10*grain+.065*batten,.51+.19*batten+.068*grain,1.-joint
    stock=s.noise(n,3,32)
    saw=.055*s.noise(6,96,36) if s.identity=='sawn_plank' else 0.
    return .33+joint*(.31+.11*stock+.18*grain+saw),joint*(ridge+.10*grain+saw),1.-joint


def _weave(s,motif,nx,ny):
    u=(s.x*nx+.065*s.noise(6,7,40))
    v=(s.y*ny+.065*s.noise(7,6,41))
    ix,iy=np.floor(u).astype(int),np.floor(v).astype(int)
    x,y=u-ix,v-iy
    a=np.sin(np.pi*x)**.72
    b=np.sin(np.pi*y)**.72
    twill=any(word in motif for word in ('twill','basket','herringbone','braided'))
    diagonal=ix+iy
    if 'herringbone' in motif:
        diagonal=np.where(ix%8<4,ix+iy,ix-iy)
    if 'basket' in motif:
        diagonal=ix//2+iy//2
    over=diagonal%(4 if twill else 2)<(2 if twill else 1)
    fiber=np.where(over,s.noise(81,12,42),s.noise(12,81,43))
    if 'felt' in motif:
        felt=s.noise(37,42,43)+.45*fiber
        return .60+.12*felt,.49+.16*felt,np.clip(-felt*.45,0,1)
    if any(w in motif for w in ('knit','braided','tablet')):
        center=.5+.22*np.sin(2*np.pi*y)
        strand=1-ease(.055,.21,abs(x-center))
        paired=np.maximum(strand,(1-ease(.05,.21,abs(x-(1-center))))*.8)
        return .38+.33*paired+.063*fiber,.32+.46*paired,1-paired
    broad=np.where(over,a,b)
    crossing=np.where(over,b,a)
    strand=.76*broad+.14*crossing
    if 'sack' in motif:
        strand=np.maximum(0,strand-.15)**1.28
    elif 'fulled' in motif:
        strand=.60*strand+.32*(.5+.5*s.noise(34,29,44))
    elif 'dense' in motif:
        strand=.79*strand+.17
    return .38+.31*strand+.048*fiber, .32+.48*strand+.044*fiber,1-strand


def _plate(s,motif,nx,ny):
    if s.identity=='chain_link':
        u=(s.x*nx)%1-.5
        v=(s.y*ny)%1-.5
        link=1-ease(.018,.084,abs(np.hypot(u,v*.80)-.275))
        join=1-ease(.019,.078,abs(np.hypot((u+.5)%1-.5,v*1.8)-.27))
        shape=np.maximum(link,join*.68)
        return .29+.45*shape,.26+.52*shape,1-shape
    if 'quench' in motif:
        streak=s.noise(14,5,59)
        scale=ease(.12,.62,s.noise(25,19,57)+.52*streak)
        return .57+.10*streak-.13*scale,.53+.066*streak-.12*scale,scale
    if 'scale' in motif:
        x=s.x*nx+.5*(np.floor(s.y*ny)%2)
        y=s.y*ny
        x,y=x%1,y%1
        lip=ease(.010,.090,y-(.16*(2*x-1)**2))
        seams=ease(.007,.059,np.minimum(x,1-x))*lip
        return .32+seams*(.39+.14*s.noise(12,12,50)),.18+seams*(.65-.28*y),1-seams
    fold=s.noise(8,13,51)
    hammer=s.noise(21,18,52)+.30*s.noise(42,39,53)
    if any(w in motif for w in ('seam','rivet','brazed')):
        u=(s.x*nx)%1
        v=(s.y*ny)%1
        joint=ease(.011,.046,np.minimum(u,1-u))
        radius=np.hypot((u-.105)*1.7,v-.5)
        rivet=(1-ease(.049,.128,radius)) if 'rivet' in motif else np.zeros_like(u)
        rolled=(1-ease(.018,.09,abs(u-.08))) if 'folded' in motif or 'brazed' in motif else np.zeros_like(u)
        height=.36+.31*joint+.23*rivet+.16*rolled+.062*hammer
        return .42+.18*joint+.11*rivet+.07*rolled+.085*hammer+.09*fold,height,1-joint
    impacts, _, _ = _pebbles(s,max(nx,11),max(ny,12))
    draw=s.noise(33,7,55)
    pits=.53*impacts+.47*ease(.15,.65,-hammer)
    if 'patina' in motif:
        pits=ease(-.12,.45,s.noise(6,7,54)+.26*hammer)
    if 'cast' in motif:
        seam=(1-ease(.009,.03,abs(s.x-.50)))*(.7+.3*s.noise(5,5,56))
        return .57+.12*fold+.08*seam,.50+.16*seam+.11*hammer,pits
    if 'bloom' in motif:
        flakes=ease(.13,.59,-s.noise(29,8,56))
        return .52+.10*draw-.17*flakes,.56-.18*flakes+.065*hammer,flakes
    return .57+.08*fold-.11*pits+.065*draw,.54-.19*pits+.08*hammer,pits


def _pebbles(s,nx,ny):
    """Periodic cellular stock with individually shaped grains and recessed beds."""
    gx,gy=s.x*nx,s.y*ny
    ix,iy=np.floor(gx).astype(int),np.floor(gy).astype(int)
    one=np.full_like(gx,9.)
    two=one.copy()
    material=np.zeros_like(gx)
    cells=np.random.default_rng(s.seed+60).uniform(.17,.83,(3,ny,nx)).astype(np.float32)
    for oy in (-1,0,1):
        for ox in (-1,0,1):
            ax,ay=ix+ox,iy+oy
            px,py,stock=cells[:,ay%ny,ax%nx]
            distance=(gx-ax-px)**2+(gy-ay-py)**2
            winner=distance<one
            two=np.where(winner,one,np.minimum(two,distance))
            one=np.minimum(one,distance)
            material=np.where(winner,stock,material)
    seam=ease(.005,.14,np.sqrt(two)-np.sqrt(one))
    stone=(1.-ease(.12,.65,np.sqrt(one)))*seam
    return stone,material,seam


def _tufts(s,nx,ny):
    """Short, curved blade strokes grouped in periodic clumps."""
    gx,gy=s.x*nx,s.y*ny
    ix,iy=np.floor(gx).astype(int),np.floor(gy).astype(int)
    cells=np.random.default_rng(s.seed+101).uniform(.15,.85,(4,ny,nx)).astype(np.float32)
    marsh=s.identity=='marsh_grass'
    heather=s.identity=='heather_tufts'
    cover=np.zeros_like(gx)
    tips=np.zeros_like(gx)
    for oy in (-1,0,1):
        for ox in (-1,0,1):
            ax,ay=ix+ox,iy+oy
            px,py,lean,size=cells[:,ay%ny,ax%nx]
            dx,dy=gx-ax-px,gy-ay-py
            if heather:
                flower=(1-ease(.09,.34,np.hypot(dx,dy)))*(.55+.45*size)
                tips=np.maximum(tips,flower)
            for blade in (-1,0,1):
                vector=(lean-.50)*1.3+blade*(.34 if marsh else .65)
                length=(.85 if marsh else .45)+.49*size
                progress=(dy+dx*vector)/(length*(1.+vector*vector))
                edge=abs(dx-vector*dy-.13*blade*progress**2)
                blade_width=(.051 if marsh else .084)*(1.-.62*np.clip(progress,0,1))
                stroke=(1-ease(.32,1.,edge/blade_width))*ease(-.07,.14,progress)*(1-ease(.68,1.,progress))
                cover=np.maximum(cover,stroke*(.60+.40*size))
    floor=s.noise(6,6,102)
    return .43+.25*cover+.11*tips+.10*floor,.38+.40*cover+.13*tips+.07*floor,1-cover


def _organic(s,motif,nx,ny):
    if 'grass' in motif:
        return _tufts(s,nx,ny)
    if 'leaf' in motif:
        shift=.36 if 'grass' in motif else .22
        phase=(s.x*nx+shift*s.noise(nx,ny,66))%1
        rows=(s.y*ny+.16*s.noise(nx,ny,67))%1
        spine=1.-ease(.026,.083,abs(phase-.5))
        blades=ease(.43,.15,abs(phase-.5))*(np.sin(np.pi*rows)**.50)
        veins=(1.-ease(.019,.11,abs((rows*5+abs(phase-.5)*2)%1-.5)))*blades
        return .35+.26*blades+.12*spine+.057*veins+.09*s.noise(9,13,68),.31+.39*blades+.12*spine,1.-blades
    path=s.x*nx+(.50 if 'root' in motif else .28)*s.noise(nx,5,69)
    if 'reed' in motif or 'thatch' in motif:
        reed='reed' in motif
        path=s.x*(nx*3)+(.20 if reed else .47)*s.noise(nx,5,69)
        path+=(.09 if reed else .31)*np.sin(2*np.pi*s.y*ny)
        lip=(s.y*ny+(.09 if reed else .21)*s.noise(9,ny,71))%1
        lap=ease(.014,.12,lip)
        shaft=(np.sin(np.pi*(path%1))**.8)*(1.-.32*lip)
        stalk=lap*shaft
        fiber=s.noise(nx*4,9,72)
        return .36+.33*stalk+.11*fiber,.21+.55*stalk+.08*fiber,1-lap
    line=1-ease(.09,.34,abs(path%1-.5))
    ties=.77+.23*np.sin(2*np.pi*s.y*ny)
    stalk=line*ties
    return .38+.34*stalk+.11*s.noise(nx*2,7,70),.25+.55*stalk,1.-stalk


def _surface(s,motif,nx,ny):
    broad=s.noise(5,6,80)
    mid=s.noise(12,15,81)
    fine=s.noise(43,39,82)
    if s.identity=='ash_soil':
        grain,stock,seam=_pebbles(s,38,33)
        fleck=grain*(stock>.63)
        patches=s.noise(8,10,88)
        return .55+.11*patches-.21*fleck+.04*fine,.39+.11*mid+.22*fleck,1-seam
    if 'strata' in motif or 'striation' in motif:
        if s.identity=='bone_striation':
            grain=s.noise(36,4,88)
            pores=ease(.33,.62,-s.noise(60,33,89))
            return .63+.15*grain-.095*pores,.49+.18*grain-.11*pores,pores
        if s.identity=='peat_cut_face':
            fiber=s.noise(6,56,88)
            layer=np.sin(2*np.pi*(s.y*(ny*3)+.11*broad))
            return .48+.14*layer+.11*fiber,.50+.17*layer+.12*fiber,np.clip(-layer*.5,0,1)
        crest=np.sin(2*np.pi*(s.y*ny+.16*broad+.11*s.noise(3,9,83)))
        return .53+.14*crest+.12*broad+.075*fine,.48+.20*crest+.095*mid,np.clip(-crest*.48,0,1)
    if 'leaded' in motif or 'cased_lead' in motif:
        u=(s.x*nx+s.y*ny)%1
        v=(s.x*nx-s.y*ny)%1
        line=np.minimum.reduce([u,1-u,v,1-v])
        panes=ease(.027,.095,line) if 'cased' in motif else ease(.016,.064,line)
        if 'cased' in motif:
            lip=1-ease(.012,.031,abs(line-.094))
            bubble=1-ease(.28,.62,-fine)
            return .28+.36*panes+.12*lip+.08*broad+.05*bubble,.62-.26*panes+.10*lip,1-panes
        return .24+.48*panes+.11*broad,.62-.24*panes,1.-panes
    if 'wheel_rib' in motif:
        rib=(.5+.5*np.cos(2*np.pi*(s.y*(ny*3)+.04*broad)))**.8
        return .53+.19*rib+.07*mid,.45+.21*rib+.055*fine,1-rib
    if 'vitrified' in motif:
        pores=ease(.30,.67,-fine)
        return .59+.15*broad-.12*pores,.53+.07*mid-.16*pores,pores
    if 'salt_glaze' in motif:
        grain,stock,seam=_pebbles(s,max(nx,26),max(ny,25))
        return .57+.11*broad+.12*grain+.044*stock,.46+.17*grain+.055*fine,1-seam
    if 'glazed' in motif:
        bands=np.cos(2*np.pi*(s.y*ny+.09*broad))
        return .57+.16*bands+.12*broad+.033*fine,.52+.08*bands+.06*fine,np.clip(-bands*.25,0,1)
    if 'corduroy' in motif:
        bars=(s.y*ny+.1*broad)%1
        crown=np.sin(np.pi*bars)**.7
        return .33+.33*crown+.095*fine,.33+.51*crown,1-crown
    if 'wattle_daub' in motif:
        rough=s.noise(19,13,86)
        return .53+.14*broad+.13*rough,.48+.16*rough+.08*mid,np.clip(-rough,0,1)
    if 'wattle' in motif:
        return _weave(s,'basket_interlace',max(4,nx),max(4,ny))
    if 'lath' in motif:
        strip=ease(.023,.096,np.minimum(s.y*ny%1,1-s.y*ny%1))
        return .39+.25*strip+.09*broad,.40+.25*strip+.07*mid,1-strip
    if 'fibre_render' in motif or 'reed_key' in motif:
        rake=s.noise(56,11,87)
        straw=ease(.22,.63,rake)
        return .52+.14*broad+.10*straw,.47+.17*straw+.11*mid,1-straw
    if 'fine_float' in motif:
        return .62+.12*broad+.065*mid,.55+.11*mid+.055*fine,np.clip(-mid*.3,0,1)
    if s.identity=='mud_track':
        lane=s.x*nx+.07*s.noise(4,7,88)
        rut=1-ease(.08,.19,abs(lane%1-.5))
        splash=ease(.14,.46,mid)*(1-rut)
        return .53+.09*broad-.17*rut+.10*splash,.48-.25*rut+.10*splash,rut
    if 'compacted' in motif or 'causeway' in motif:
        wheel=np.cos(2*np.pi*(s.x*nx+.065*broad))
        return .47+.16*broad+.08*fine+.07*wheel,.49+.13*wheel+.12*mid,np.clip(-wheel*.42,0,1)
    trowel=s.noise(4,19,84)+.32*s.noise(17,5,85)
    return .59+.13*broad+.11*trowel+.09*fine,.53+.15*trowel+.085*mid,np.clip(-trowel*.41,0,1)


def _design(s,motif,nx,ny):
    if s.identity=='bark_shingle':
        tone,height,recess=_courses(s,'wooden_shake_irregular_lap',nx,ny)
        crust=s.noise(35,9,75)
        return tone+.12*crust*(1-recess),height+.13*crust*(1-recess),recess
    if any(word in motif for word in ('course','ashlar','shingle','shake','slate','cobbl','sett','roof_tile','clay_lap','pantile','dry_stack','interlocking_pan')):
        return _courses(s,motif,nx,ny)
    if any(word in motif for word in ('timber','board','bark','wood')):
        return _timber(s,motif,nx,ny)
    if any(word in motif for word in ('fabric','weave','basket','felt','rope','cord','net','wicker')):
        return _weave(s,motif,nx,ny)
    if any(word in motif for word in ('iron','metal','scale','hammer','patina')):
        return _plate(s,motif,nx,ny)
    if any(word in motif for word in ('gravel','pebble','leather','rubble','cobb','crack','scattered','aggregate','flint','scree')):
        stone,stock,seam=_pebbles(s,nx,ny)
        base=s.noise(7,9,90)
        if s.identity=='scattered_gravel':
            stone*=ease(.37,.64,stock)
        tone=.38+.28*stone+.17*stock+.08*base
        height=.32+.52*stone+.08*base
        if s.identity=='rawhide_lacing':
            u,v=s.x*nx%1,s.y*ny%1
            strap=(1-ease(.055,.13,abs(u-.53-(v-.5)*.66)))*ease(.13,.22,v)*(1-ease(.82,.93,v))
            holes=1-ease(.029,.068,np.minimum(np.hypot(u-.33,v-.2),np.hypot(u-.73,v-.80)))
            return .44+.12*base+.26*strap-.17*holes,.43+.30*strap-.14*holes,holes
        if 'tooled' in motif:
            stamp=1-ease(.014,.092,abs(np.hypot(s.x*nx%1-.5,s.y*ny%1-.5)-.27))
            tone+=.15*stamp
            height+=.25*stamp
        if 'laminated' in motif:
            bands=(.5+.5*np.sin(2*np.pi*s.y*(ny*2)))**2
            tone+=.14*bands
            height+=.20*bands
        if 'turned_edge' in motif or 'grain_panel' in motif:
            edge=np.minimum(s.x*nx%1,1-s.x*nx%1)
            welt=(1-ease(.026,.075,abs(edge-.115)))
            tone+=.14*welt
            height+=.24*welt
        if 'stitched' in motif:
            thread=(1-ease(.018,.065,abs(s.x*nx%1-.5)))*(1-ease(.24,.42,abs(s.y*ny%1-.5)))
            tone+=.22*thread
            height+=.20*thread
        return tone,height,1.-seam
    if any(word in motif for word in ('organic','grass','reed','thatch','root','leaf','shrub')):
        return _organic(s,motif,nx,ny)
    return _surface(s,motif,nx,ny)


def default_repeat(motif):
    if 'shingle' in motif: return 7,6
    if 'slate' in motif or 'tile' in motif: return 6,6
    if 'stone' in motif: return 5,6
    if 'weave' in motif: return 30,28
    if 'felt' in motif: return 32,32
    if 'board' in motif: return 7,8
    if 'grain' in motif: return 5,6
    if 'reed' in motif or 'thatch' in motif: return 28,6
    if any(word in motif for word in ('gravel','leather','pebbl')): return 17,16
    return 6,8


def generate(record,size):
    motif=record['motif']
    nx,ny=record.get('repeat',default_repeat(motif))
    # An even course count closes staggered bonds across the repeat boundary.
    s=Sample(size,record['id'])
    value,height,recess=_design(s,motif,int(nx),int(ny)+(int(ny)%2))
    medium=s.noise(9,11,100)
    value=np.clip(value+.030*medium,.035,.96)
    height=np.clip(height+.025*medium,0,1)
    paint=np.round(value*255).astype(np.uint8)
    scale_x,scale_y=record['scale_m']
    family=record['family'].lower()
    metal=('metal' in family or 'iron' in motif or 'metal' in motif)
    gain=min(scale_x,scale_y)*(.017 if metal else .034)
    dx=(np.roll(height,-1,axis=1)-np.roll(height,1,axis=1))*size*gain/(2*scale_x)
    dy=(np.roll(height,-1,axis=0)-np.roll(height,1,axis=0))*size*gain/(2*scale_y)
    normals=np.stack((-dx,dy,np.ones_like(height)),axis=-1)
    normals/=np.linalg.norm(normals,axis=-1,keepdims=True)
    encode=lambda x: np.round(np.clip(x,0,1)*255).astype(np.uint8)
    smoothness=(.39 if metal else .81)
    if 'glass' in motif or 'glazed' in motif:
        smoothness=.34
    rough=encode(smoothness+.15*recess+.075*medium)
    metal_value=encode(.92-.57*recess+.04*medium) if metal else np.zeros_like(paint)
    return {'master':paint,'color':np.repeat(paint[...,None],3,axis=-1),
            'normal':encode(normals*.5+.5),'height':encode(height),
            'roughness':rough,'metallic':metal_value}
