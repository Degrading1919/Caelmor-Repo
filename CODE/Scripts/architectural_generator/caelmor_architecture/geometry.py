"""Small dependency-free solid/convex geometry kernel. All dimensions are metres."""
import hashlib
import math
from dataclasses import dataclass, field

EPS = 1e-8


def stable_seed(seed, label):
    return int.from_bytes(hashlib.sha256(f'{seed}:{label}'.encode()).digest()[:8], 'big')


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def mul(a, s):
    return tuple(x*s for x in a)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def unit(a):
    length = math.sqrt(dot(a, a))
    if length < EPS:
        raise ValueError('Zero length direction')
    return mul(a, 1/length)


def area(poly):
    return sum(p[0]*q[1]-q[0]*p[1] for p, q in zip(poly, poly[1:]+poly[:1]))*.5


def clean(poly):
    result = []
    for p in poly:
        if not result or sum((a-b)**2 for a,b in zip(p,result[-1])) > EPS**2:
            result.append(tuple(p))
    if len(result)>1 and sum((a-b)**2 for a,b in zip(result[0],result[-1])) <= EPS**2:
        result.pop()
    return result


def clip(poly, a, b, c):
    """Sutherland-Hodgman half-plane clip, retaining a*x+b*y+c >= 0."""
    if not poly:
        return []
    result = []
    for p,q in zip(poly, poly[1:]+poly[:1]):
        dp, dq = a*p[0]+b*p[1]+c, a*q[0]+b*q[1]+c
        pin, qin = dp >= -EPS, dq >= -EPS
        if pin:
            result.append(p)
        if pin != qin:
            result.append(lerp(p,q,dp/(dp-dq)))
    result = clean(result)
    return result if len(result)>=3 and abs(area(result)) > EPS else []


def inequalities(poly):
    """Interior half planes of a CCW convex polygon."""
    return [(p[1]-q[1], q[0]-p[0], p[0]*q[1]-q[0]*p[1])
            for p,q in zip(poly,poly[1:]+poly[:1])]


def subtract_convex(poly, planes):
    """Partition poly minus convex cutter into nonoverlapping convex fragments."""
    result, remaining = [], poly
    for a,b,c in planes:
        outside = clip(remaining,-a,-b,-c)
        if outside:
            result.append(outside)
        remaining = clip(remaining,a,b,c)
        if not remaining:
            break
    return result


@dataclass
class MeshBuffer:
    name: str
    material: str = 'timber'
    layer: str = 'structure'
    vertices: list = field(default_factory=list)
    faces: list = field(default_factory=list)

    def indexed(self, vertices, faces):
        offset = len(self.vertices)
        self.vertices.extend(tuple(float(v) for v in p) for p in vertices)
        self.faces.extend(tuple(offset+i for i in face) for face in faces)

    def face(self, points):
        self.indexed(points, [tuple(range(len(points)))])

    def box(self, center, size):
        if min(size) <= 0:
            raise ValueError('Box dimensions must be positive')
        x,y,z = center
        a,b,c = (s*.5 for s in size)
        self.indexed([(x-a,y-b,z-c),(x+a,y-b,z-c),(x+a,y+b,z-c),(x-a,y+b,z-c),
                      (x-a,y-b,z+c),(x+a,y-b,z+c),(x+a,y+b,z+c),(x-a,y+b,z+c)],
                     [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])

    def extrude(self, poly_xyz, vector):
        poly = clean(poly_xyz)
        if len(poly)<3:
            return
        normal = (0.,0.,0.)
        for i in range(1,len(poly)-1):
            normal = add(normal,cross(sub(poly[i],poly[0]),sub(poly[i+1],poly[0])))
        if dot(normal,vector) < 0:
            poly.reverse()
        if abs(dot(normal,vector)) < EPS:
            return
        n = len(poly)
        verts = poly + [add(p,vector) for p in poly]
        faces = [tuple(reversed(range(n))),tuple(range(n,2*n))]
        faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        self.indexed(verts,faces)

    def prism(self, poly_xy, z0, z1):
        self.extrude([(x,y,z0) for x,y in poly_xy], (0,0,z1-z0))

    def beam(self, a, b, width, depth=None):
        depth = width if depth is None else depth
        axis = unit(sub(b,a))
        ref = (0,0,1) if abs(axis[2])<.95 else (0,1,0)
        u = mul(unit(cross(axis,ref)),width*.5)
        v = mul(unit(cross(axis,unit(u))),depth*.5)
        poly = [add(add(a,mul(u,s)),mul(v,t)) for s,t in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        self.extrude(poly,sub(b,a))

    def cylinder(self, a, b, radius, segments=8):
        axis = unit(sub(b,a))
        ref = (0,0,1) if abs(axis[2])<.95 else (0,1,0)
        u = unit(cross(axis,ref))
        v = cross(axis,u)
        poly = [add(a,add(mul(u,radius*math.cos(2*math.pi*i/segments)),
                         mul(v,radius*math.sin(2*math.pi*i/segments)))) for i in range(segments)]
        self.extrude(poly,sub(b,a))

    def chamfered_beam(self,a,b,width,depth=None,chamfer=.008):
        """Closed hewn member with restrained, physical edge arrises."""
        depth=width if depth is None else depth
        axis=unit(sub(b,a))
        ref=(0,0,1) if abs(axis[2])<.95 else (0,1,0)
        u=unit(cross(axis,ref))
        v=cross(axis,u)
        hw,hd=width*.5,depth*.5
        cut=max(0.,min(chamfer,min(width,depth)*.2))
        if cut<1e-6:
            return self.beam(a,b,width,depth)
        section=[(-hw+cut,-hd),(hw-cut,-hd),(hw,-hd+cut),(hw,hd-cut),
                 (hw-cut,hd),(-hw+cut,hd),(-hw,hd-cut),(-hw,-hd+cut)]
        self.extrude([add(a,add(mul(u,x),mul(v,y))) for x,y in section],sub(b,a))
