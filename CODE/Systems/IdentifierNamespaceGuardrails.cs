using System;
using System.Diagnostics;
using EntityHandle = global::Caelmor.Runtime.Tick.EntityHandle;
using PlayerId = global::Caelmor.Runtime.Onboarding.PlayerId;
using SaveId = global::Caelmor.Runtime.Persistence.SaveId;
using SessionId = global::Caelmor.Runtime.Onboarding.SessionId;

namespace Caelmor.Runtime.Diagnostics
{
    /// <summary>
    /// DEBUG-only guardrails that assert identifier namespaces remain canonical.
    /// Prevents silent drift where similarly named identifiers are introduced under different namespaces.
    /// </summary>
    internal static class IdentifierNamespaceGuardrails
    {
        private const string SessionNamespace = "Caelmor.Runtime.Onboarding";
        private const string PlayerNamespace = "Caelmor.Runtime.Onboarding";
        private const string SaveNamespace = "Caelmor.Runtime.Persistence";
        private const string EntityNamespace = "Caelmor.Runtime.Tick";

        [Conditional("DEBUG")]
        public static void AssertCanonicalIdentifierNamespaces()
        {
            EnsureNamespace(nameof(SessionId), SessionNamespace, typeof(SessionId).Namespace);
            EnsureNamespace(nameof(PlayerId), PlayerNamespace, typeof(PlayerId).Namespace);
            EnsureNamespace(nameof(SaveId), SaveNamespace, typeof(SaveId).Namespace);
            EnsureNamespace(nameof(EntityHandle), EntityNamespace, typeof(EntityHandle).Namespace);
        }

        private static void EnsureNamespace(string typeName, string expectedNamespace, string? actualNamespace)
        {
            if (!string.Equals(expectedNamespace, actualNamespace, StringComparison.Ordinal))
                throw new InvalidOperationException($"{typeName} must reside in namespace {expectedNamespace} (found {actualNamespace ?? "<null>"}).");
        }
    }
}
