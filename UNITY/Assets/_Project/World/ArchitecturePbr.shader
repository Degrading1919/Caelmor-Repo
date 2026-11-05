Shader "Caelmor/Architecture PBR"
{
    Properties
    {
        _Color("Base factor (sRGB Color property)", Color) = (1,1,1,1)
        _MainTex("sRGB base color", 2D) = "white" {}
        _OrmTex("Linear ORM (R occlusion, G roughness, B metallic)", 2D) = "white" {}
        [Normal] _NormalTex("Tangent normal", 2D) = "bump" {}
        _BaseUv("Base UV channel", Float) = 0
        _OrmUv("ORM UV channel", Float) = 0
        _NormalUv("Normal UV channel", Float) = 0
        _Roughness("Roughness factor", Range(0,1)) = 1
        _Metallic("Metallic factor", Range(0,1)) = 0
        _NormalScale("Normal scale", Float) = 1
        _HasOrm("Use ORM", Float) = 0
        _HasNormal("Use normal", Float) = 0
        _OcclusionStrength("Occlusion strength", Range(0,1)) = 0
        _VertexColor("Multiply source vertex color", Float) = 1
        _Cutoff("Alpha cutoff (-1 opaque)", Float) = -1
        [Enum(UnityEngine.Rendering.CullMode)] _Cull("Cull mode", Float) = 2
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Cull [_Cull]
        CGPROGRAM
        #pragma surface surf Standard fullforwardshadows addshadow vertex:vert
        #pragma target 3.0
        #include "UnityCG.cginc"
        #include "UnityStandardUtils.cginc"
        sampler2D _MainTex, _OrmTex, _NormalTex;
        float4 _MainTex_ST, _OrmTex_ST, _NormalTex_ST;
        fixed4 _Color;
        float _BaseUv, _OrmUv, _NormalUv, _Roughness, _Metallic, _NormalScale;
        float _HasOrm, _HasNormal, _OcclusionStrength, _Cutoff, _VertexColor;
        struct Input { float2 coords0; float2 coords1; float2 coords2; float2 coords3; fixed4 vertexColor; float facing : VFACE; };
        void vert(inout appdata_full v, out Input o)
        {
            UNITY_INITIALIZE_OUTPUT(Input,o);
            o.coords0=v.texcoord.xy; o.coords1=v.texcoord1.xy;
            o.coords2=v.texcoord2.xy; o.coords3=v.texcoord3.xy;
            o.vertexColor=v.color;
        }
        float2 uvAt(Input i, float channel)
        {
            if(channel<0.5) return i.coords0;
            if(channel<1.5) return i.coords1;
            if(channel<2.5) return i.coords2;
            return i.coords3;
        }
        void surf(Input i, inout SurfaceOutputStandard o)
        {
            fixed4 c=tex2D(_MainTex,uvAt(i,_BaseUv)*_MainTex_ST.xy+_MainTex_ST.zw)*_Color;
            c*=lerp(float4(1,1,1,1),i.vertexColor,_VertexColor);
            if(_Cutoff>=0) clip(c.a-_Cutoff);
            float3 orm=tex2D(_OrmTex,uvAt(i,_OrmUv)*_OrmTex_ST.xy+_OrmTex_ST.zw).rgb;
            o.Albedo=c.rgb; o.Alpha=c.a;
            o.Metallic=_Metallic*lerp(1,orm.b,_HasOrm);
            o.Smoothness=1-_Roughness*lerp(1,orm.g,_HasOrm);
            o.Occlusion=lerp(1,orm.r,_OcclusionStrength);
            o.Normal=float3(0,0,1);
            if(_HasNormal>0.5) o.Normal=UnpackScaleNormal(tex2D(_NormalTex,uvAt(i,_NormalUv)*_NormalTex_ST.xy+_NormalTex_ST.zw),_NormalScale);
            o.Normal*=i.facing>=0?1:-1;
        }
        ENDCG
    }
    FallBack "Standard"
}
