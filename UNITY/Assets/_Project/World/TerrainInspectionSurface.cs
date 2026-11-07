using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;
using UnityEngine.Rendering;

namespace Caelmor.Unity.Inspection
{
    /// <summary>Loads immutable offline samples for an isolated inspection scene.</summary>
    [DefaultExecutionOrder(-200)]
    public sealed class TerrainInspectionSurface : MonoBehaviour
    {
        public TextAsset payload;
        public Material groundMaterial,roadMaterial,waterMaterial,proxyMaterial;
        public const int TerrainLayer = 9;
        public const int ProxyLayer = 10;
        public string sourceHash;
        public int meshCount, terrainTriangles;
        public float bridgeApproachGap;
        public readonly List<Grid> grids = new List<Grid>();
        public readonly List<Spawn> spawns = new List<Spawn>();
        public readonly List<Bridge> bridges = new List<Bridge>();
        readonly List<Mesh> meshes = new List<Mesh>();
        readonly List<Material> materials = new List<Material>();
        readonly List<GameObject> generated = new List<GameObject>();
        readonly List<Strip> strips = new List<Strip>();
        readonly List<Spawn> labels = new List<Spawn>();
        bool built;

        public sealed class Grid
        {
            public string name; public int nx, ny; public float east, north, step;
            public float[] height; public byte[] roads; public Vector4[] exclusions;
            public bool Contains(float x,float z) => x>=east && z>=north && x<=east+(nx-1)*step && z<=north+(ny-1)*step;
            public float Sample(float x,float z)
            {
                float fx=Mathf.Clamp((x-east)/step,0,nx-1), fy=Mathf.Clamp((z-north)/step,0,ny-1);
                int c=Mathf.Min((int)fx,nx-2),r=Mathf.Min((int)fy,ny-2); float u=fx-c,v=fy-r;
                float a=height[r*nx+c],b=height[r*nx+c+1],d=height[(r+1)*nx+c+1],q=height[(r+1)*nx+c];
                return v<=u ? a+(b-a)*u+(d-b)*v : a+(d-q)*u+(q-a)*v;
            }
        }
        public sealed class Spawn { public string name; public Vector2 point,target; }
        public sealed class Bridge { public string name; public Vector2 a,b; public float width,top,thickness; }
        sealed class Strip { public string name; public Vector3[] points; public float width; }

        void Awake() { if(Application.isPlaying) BuildGeometry(); }
        public void ReadPayload()
        {
            if(grids.Count>0) return;
            if(payload==null) throw new InvalidOperationException("Terrain inspection payload is missing.");
            using(var reader=new BinaryReader(new MemoryStream(payload.bytes)))
            {
                if(Encoding.ASCII.GetString(reader.ReadBytes(8))!="CLTRN001") throw new InvalidDataException("Unknown terrain inspection payload.");
                sourceHash=reader.ReadString(); int count=reader.ReadInt32();
                if(count<1 || count>16) throw new InvalidDataException("Invalid terrain grid count.");
                for(int i=0;i<count;i++)
                {
                    var g=new Grid{name=reader.ReadString(),nx=reader.ReadInt32(),ny=reader.ReadInt32(),east=reader.ReadSingle(),north=reader.ReadSingle(),step=reader.ReadSingle()};
                    if(g.nx<2 || g.ny<2 || (long)g.nx*g.ny>4000000 || g.step<=0) throw new InvalidDataException("Invalid terrain dimensions.");
                    g.height=new float[g.nx*g.ny];
                    for(int n=0;n<g.height.Length;n++) {g.height[n]=reader.ReadSingle();if(float.IsNaN(g.height[n])||float.IsInfinity(g.height[n]))throw new InvalidDataException("Nonfinite terrain elevation.");}
                    g.roads=reader.ReadBytes(g.height.Length); if(g.roads.Length!=g.height.Length)throw new EndOfStreamException();
                    g.exclusions=new Vector4[reader.ReadInt32()];
                    for(int n=0;n<g.exclusions.Length;n++)g.exclusions[n]=new Vector4(reader.ReadSingle(),reader.ReadSingle(),reader.ReadSingle(),reader.ReadSingle());
                    grids.Add(g);
                }
                count=reader.ReadInt32();
                for(int i=0;i<count;i++)
                {
                    string name=reader.ReadString();int length=reader.ReadInt32();float width=reader.ReadSingle();
                    var strip=new Strip{name=name,width=width,points=new Vector3[length]};
                    for(int n=0;n<length;n++){float x=reader.ReadSingle(),z=reader.ReadSingle(),y=reader.ReadSingle();strip.points[n]=new Vector3(x,y+.02f,z);}
                    strips.Add(strip);
                }
                count=reader.ReadInt32();for(int i=0;i<count;i++)spawns.Add(new Spawn{name=reader.ReadString(),point=new Vector2(reader.ReadSingle(),reader.ReadSingle()),target=new Vector2(reader.ReadSingle(),reader.ReadSingle())});
                count=reader.ReadInt32();for(int i=0;i<count;i++)labels.Add(new Spawn{name=reader.ReadString(),point=new Vector2(reader.ReadSingle(),reader.ReadSingle())});
                count=reader.ReadInt32();for(int i=0;i<count;i++)bridges.Add(new Bridge{name=reader.ReadString(),a=new Vector2(reader.ReadSingle(),reader.ReadSingle()),b=new Vector2(reader.ReadSingle(),reader.ReadSingle()),width=reader.ReadSingle(),top=reader.ReadSingle(),thickness=reader.ReadSingle()});
                if(reader.BaseStream.Position!=reader.BaseStream.Length)throw new InvalidDataException("Unexpected terrain payload suffix.");
            }
        }
        public float HeightAt(float east,float north)
        {
            ReadPayload();for(int i=grids.Count-1;i>=0;i--)if(grids[i].Contains(east,north))return grids[i].Sample(east,north);
            throw new ArgumentOutOfRangeException("Point outside the inspection terrain.");
        }
        public void BuildGeometry()
        {
            if(built)return;ReadPayload();built=true;
            Material ground=groundMaterial!=null?groundMaterial:MakeMaterial("Inspection ground",new Color(.38f,.44f,.34f));
            Material road=roadMaterial!=null?roadMaterial:MakeMaterial("Technical graded corridor",new Color(.48f,.43f,.34f));
            Material water=waterMaterial!=null?waterMaterial:MakeMaterial("Source water level cue",new Color(.15f,.37f,.46f));
            Material proxy=proxyMaterial!=null?proxyMaterial:MakeMaterial("Unapproved bridge scale proxy",new Color(.56f,.48f,.34f));
            foreach(var grid in grids)
                for(int row=0;row<grid.ny-1;row+=128)
                    for(int col=0;col<grid.nx-1;col+=128)CreateChunk(grid,row,col,Mathf.Min(128,grid.ny-1-row),Mathf.Min(128,grid.nx-1-col),ground,road);
            foreach(var strip in strips) CreateWater(strip,water);
            foreach(var bridge in bridges)
            {
                var box=GameObject.CreatePrimitive(PrimitiveType.Cube);box.name=bridge.name+" / TECHNICAL PROXY";
                box.transform.SetParent(transform,false);box.layer=ProxyLayer;box.hideFlags=HideFlags.DontSave;
                Vector2 direction=bridge.b-bridge.a,center=(bridge.a+bridge.b)*.5f;
                box.transform.position=new Vector3(center.x,bridge.top-bridge.thickness*.5f,center.y);
                box.transform.rotation=Quaternion.Euler(0,Mathf.Atan2(direction.x,direction.y)*Mathf.Rad2Deg,0);
                box.transform.localScale=new Vector3(bridge.width,bridge.thickness,direction.magnitude);
                box.GetComponent<Renderer>().sharedMaterial=proxy;generated.Add(box);
                bridgeApproachGap=Mathf.Max(bridgeApproachGap,Mathf.Abs(bridge.top-HeightAt(bridge.a.x,bridge.a.y)),Mathf.Abs(bridge.top-HeightAt(bridge.b.x,bridge.b.y)));
            }
            foreach(var label in labels)
            {
                var go=new GameObject(label.name);go.transform.SetParent(transform,false);go.hideFlags=HideFlags.DontSave;
                go.transform.position=new Vector3(label.point.x,HeightAt(label.point.x,label.point.y)+5,label.point.y);
                var text=go.AddComponent<TextMesh>();text.text=label.name;text.characterSize=.6f;text.fontSize=64;text.anchor=TextAnchor.MiddleCenter;text.color=new Color(.95f,.92f,.76f);
                generated.Add(go);
            }
            Physics.SyncTransforms();
            Debug.Log("CAELMOR_TERRAIN_INSPECTION_GEOMETRY: grids="+grids.Count+" chunks="+meshCount+" terrainTriangles="+terrainTriangles+" source="+sourceHash);
        }
        Material MakeMaterial(string name,Color color)
        {
            var material=new Material(Shader.Find("Standard")){name=name,color=color,hideFlags=HideFlags.DontSave};material.SetFloat("_Glossiness",.08f);materials.Add(material);return material;
        }
        void CreateChunk(Grid grid,int r0,int c0,int rows,int cols,Material ground,Material road)
        {
            var positions=new Vector3[(rows+1)*(cols+1)];var normals=new Vector3[positions.Length];var uv=new Vector2[positions.Length];
            var earth=new List<int>();var route=new List<int>();
            float east=grid.east+c0*grid.step,north=grid.north+r0*grid.step;
            for(int row=0;row<=rows;row++)for(int col=0;col<=cols;col++)
            {
                int index=row*(cols+1)+col;float x=east+col*grid.step,z=north+row*grid.step,y=grid.height[(r0+row)*grid.nx+c0+col];
                positions[index]=new Vector3(col*grid.step,y,row*grid.step);uv[index]=new Vector2(x/32,z/32);
                float dx=SafeHeight(x+2,z,y)-SafeHeight(x-2,z,y),dz=SafeHeight(x,z+2,y)-SafeHeight(x,z-2,y);
                normals[index]=new Vector3(-dx,4,-dz).normalized;
            }
            for(int row=0;row<rows;row++)for(int col=0;col<cols;col++)
            {
                float x=east+(col+.5f)*grid.step,z=north+(row+.5f)*grid.step;bool omitted=false;
                foreach(var rectangle in grid.exclusions)if(x>rectangle.x&&x<rectangle.z&&z>rectangle.y&&z<rectangle.w){omitted=true;break;}
                if(omitted)continue;
                int a=row*(cols+1)+col,b=a+1,c=a+cols+1,d=c+1;
                var indices=grid.roads[(r0+row)*grid.nx+c0+col]!=0?route:earth;
                indices.Add(a);indices.Add(d);indices.Add(b);indices.Add(a);indices.Add(c);indices.Add(d);
            }
            if(earth.Count+route.Count==0)return;
            var mesh=new Mesh{name=grid.name+" inspection chunk",indexFormat=IndexFormat.UInt32,hideFlags=HideFlags.DontSave};
            mesh.vertices=positions;mesh.normals=normals;mesh.uv=uv;mesh.subMeshCount=2;mesh.SetTriangles(earth,0);mesh.SetTriangles(route,1);mesh.RecalculateBounds();meshes.Add(mesh);
            var go=new GameObject(mesh.name);go.hideFlags=HideFlags.DontSave;go.layer=TerrainLayer;go.transform.SetParent(transform,false);go.transform.position=new Vector3(east,0,north);
            go.AddComponent<MeshFilter>().sharedMesh=mesh;go.AddComponent<MeshRenderer>().sharedMaterials=new[]{ground,road};go.AddComponent<MeshCollider>().sharedMesh=mesh;generated.Add(go);
            meshCount++;terrainTriangles+=(earth.Count+route.Count)/3;
        }
        float SafeHeight(float x,float z,float fallback)
        {
            if(grids[0].Contains(x,z))return HeightAt(x,z);return fallback;
        }
        void CreateWater(Strip strip,Material material)
        {
            var vertices=new Vector3[strip.points.Length*2];var indices=new int[(strip.points.Length-1)*6];
            for(int i=0;i<strip.points.Length;i++)
            {
                Vector3 direction=(strip.points[Mathf.Min(i+1,strip.points.Length-1)]-strip.points[Mathf.Max(0,i-1)]).normalized;
                Vector3 offset=new Vector3(-direction.z,0,direction.x).normalized*strip.width;
                vertices[i*2]=strip.points[i]+offset;vertices[i*2+1]=strip.points[i]-offset;
                if(i==strip.points.Length-1)continue;int a=i*2,j=i*6;
                indices[j]=a;indices[j+1]=a+2;indices[j+2]=a+1;indices[j+3]=a+1;indices[j+4]=a+2;indices[j+5]=a+3;
            }
            var mesh=new Mesh{name=strip.name+" source stage",indexFormat=IndexFormat.UInt32,vertices=vertices,triangles=indices,hideFlags=HideFlags.DontSave};mesh.RecalculateNormals();mesh.RecalculateBounds();meshes.Add(mesh);
            var go=new GameObject(mesh.name);go.hideFlags=HideFlags.DontSave;go.transform.SetParent(transform,false);go.AddComponent<MeshFilter>().sharedMesh=mesh;go.AddComponent<MeshRenderer>().sharedMaterial=material;generated.Add(go);
        }
        void LateUpdate()
        {
            if(!Application.isPlaying||Camera.main==null)return;
            foreach(var go in generated)if(go!=null&&go.GetComponent<TextMesh>()!=null)go.transform.rotation=Quaternion.LookRotation(go.transform.position-Camera.main.transform.position);
        }
        void OnDestroy()
        {
            foreach(var mesh in meshes)if(mesh!=null){if(Application.isPlaying)Destroy(mesh);else DestroyImmediate(mesh);}
            foreach(var material in materials)if(material!=null){if(Application.isPlaying)Destroy(material);else DestroyImmediate(material);}
        }
    }
}
