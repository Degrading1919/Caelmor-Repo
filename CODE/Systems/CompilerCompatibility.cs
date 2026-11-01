// C# 9 init-only properties are supported by Unity's compiler but the marker is
// absent from the .NET Standard reference assembly used by the standalone build.
#if !NET5_0_OR_GREATER
namespace System.Runtime.CompilerServices
{
    internal static class IsExternalInit { }
}
#endif
