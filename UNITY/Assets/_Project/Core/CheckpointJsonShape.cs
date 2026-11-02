using System;
using System.Collections.Generic;
using System.Globalization;
using System.Reflection;
using System.Text;
using Caelmor.Runtime.Gameplay;

namespace Caelmor.Unity.Playable
{
    // JsonUtility intentionally ignores unknown members. Checkpoint restore must not:
    // reject duplicate/unknown fields and malformed primitive values before decoding.
    internal static class CheckpointJsonShape
    {
        static readonly HashSet<string> OldRoot=new HashSet<string>(new[]{"version","contentId","tick","health","flags","items","xp","quests","enemies","actions","hazards"},StringComparer.Ordinal);
        static readonly HashSet<string> OldEnemy=new HashSet<string>(new[]{"id","health","windup","cooldown","respawn","loot","aimX","aimZ"},StringComparer.Ordinal);
        public static void Validate(string text)=>new Reader(text,null).Run();
        public static void ValidateLegacyShape(string text,string identity)
        {
            if(identity==GameplaySession.LegacyTwoQuestIdentity)new Reader(text,OldRoot).Run();
            else if(identity==GameplaySession.LegacyThreeQuestIdentity)
            {
                var fields=new HashSet<string>(OldRoot,StringComparer.Ordinal){"flocks","presentations","counters"};
                new Reader(text,fields).Run();
            }
        }
        sealed class Reader
        {
            readonly string text;readonly HashSet<string> legacyRoot;int offset,depth;
            public Reader(string text,HashSet<string> legacyRoot){this.text=text??throw new ArgumentNullException(nameof(text));this.legacyRoot=legacyRoot;}
            public void Run(){White();Value(typeof(GameplaySave));White();Need(offset==text.Length,"Trailing checkpoint JSON.");}
            void Value(Type type)
            {
                White();Need(offset<text.Length,"Truncated checkpoint JSON.");
                if(Take("null")){Need(!type.IsValueType,"Null primitive.");return;}
                if(type==typeof(string)){String();return;}
                if(type==typeof(bool)){Need(Take("true")||Take("false"),"Invalid boolean.");return;}
                if(type==typeof(int)||type==typeof(long)||type==typeof(float)||type==typeof(double))
                {
                    int start=offset;
                    if(Peek()=='-')offset++;
                    Need(offset<text.Length && char.IsDigit(Peek()),"Invalid number.");
                    if(Peek()=='0')offset++;else while(offset<text.Length && char.IsDigit(Peek()))offset++;
                    if(Peek()=='.'){offset++;int digits=offset;while(offset<text.Length&&char.IsDigit(Peek()))offset++;Need(offset>digits,"Invalid fraction.");}
                    if(Peek()=='e'||Peek()=='E'){offset++;if(Peek()=='+'||Peek()=='-')offset++;int digits=offset;while(offset<text.Length&&char.IsDigit(Peek()))offset++;Need(offset>digits,"Invalid exponent.");}
                    string number=text.Substring(start,offset-start);
                    if(type==typeof(int))Need(int.TryParse(number,NumberStyles.AllowLeadingSign,CultureInfo.InvariantCulture,out _),"Invalid integer.");
                    else if(type==typeof(long))Need(long.TryParse(number,NumberStyles.AllowLeadingSign,CultureInfo.InvariantCulture,out _),"Invalid long integer.");
                    else Need(double.TryParse(number,NumberStyles.Float,CultureInfo.InvariantCulture,out double n)&&!double.IsNaN(n)&&!double.IsInfinity(n),"Invalid finite number.");
                    return;
                }
                Need(++depth<=32,"Checkpoint JSON nesting limit.");
                if(type.IsArray)
                {
                    Character('[');White();if(Peek()!=']'){while(true){Value(type.GetElementType());White();if(Peek()!=',')break;offset++;}}Character(']');
                }
                else
                {
                    Character('{');White();var seen=new HashSet<string>(StringComparer.Ordinal);
                    if(Peek()!='}')while(true)
                    {
                        string name=String();Need(seen.Add(name),"Duplicate checkpoint field.");
                        if(legacyRoot!=null && type==typeof(GameplaySave))Need(legacyRoot.Contains(name),"Field did not exist in this published checkpoint layout.");
                        if(legacyRoot!=null && type==typeof(EnemyProgress))Need(OldEnemy.Contains(name),"Enemy field did not exist in this published checkpoint layout.");
                        var field=type.GetField(name,BindingFlags.Public|BindingFlags.Instance);Need(field!=null,"Unknown checkpoint field.");
                        Character(':');Value(field.FieldType);White();if(Peek()!=',')break;offset++;White();
                    }
                    Character('}');
                }
                depth--;
            }
            string String()
            {
                White();Character('"');var value=new StringBuilder();
                while(offset<text.Length)
                {
                    char c=text[offset++];if(c=='"')return value.ToString();Need(c>=' ',"Control character in JSON string.");
                    if(c!='\\'){value.Append(c);continue;}
                    Need(offset<text.Length,"Truncated escape.");c=text[offset++];
                    switch(c)
                    {
                        case '"':case '\\':case '/':value.Append(c);break;
                        case 'b':value.Append('\b');break;case 'f':value.Append('\f');break;case 'n':value.Append('\n');break;case 'r':value.Append('\r');break;case 't':value.Append('\t');break;
                        case 'u':Need(offset+4<=text.Length,"Truncated unicode escape.");Need(ushort.TryParse(text.Substring(offset,4),NumberStyles.HexNumber,CultureInfo.InvariantCulture,out ushort code),"Invalid unicode escape.");value.Append((char)code);offset+=4;break;
                        default:throw new InvalidOperationException("Invalid JSON escape.");
                    }
                }
                throw new InvalidOperationException("Unterminated JSON string.");
            }
            bool Take(string value){if(offset+value.Length>text.Length||string.CompareOrdinal(text,offset,value,0,value.Length)!=0)return false;offset+=value.Length;return true;}
            char Peek()=>offset<text.Length?text[offset]:'\0';
            void Character(char c){White();Need(Peek()==c,"Unexpected checkpoint JSON token.");offset++;}
            void White(){while(offset<text.Length&&(text[offset]==' '||text[offset]=='\r'||text[offset]=='\n'||text[offset]=='\t'))offset++;}
            static void Need(bool value,string error){if(!value)throw new InvalidOperationException(error);}
        }
    }
}
