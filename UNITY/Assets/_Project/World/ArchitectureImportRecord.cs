using System;
using UnityEngine;

namespace Caelmor.Unity
{
    /// <summary>Editor import provenance and ownership ledger, not gameplay content.</summary>
    public sealed class ArchitectureImportRecord : ScriptableObject
    {
        public string sourcePath;
        public string importerVersion;
        public string sourceHash;
        public string collisionHash;
        public string sidecarHash;
        public string compatibilitySignature;
        public string bindingsSignature;
        public string buildingId;
        public string generatedPrefab;
        public string placementPrefab;
        public string placementGuid;
        public string unresolvedLibraryMappings;
        public long sourceBytes;
        public long generatedBytes;
        public double importSeconds;
        public int rendererCount;
        public int meshCount;
        public int colliderCount;
        public int materialCount;
        public int textureCount;
        public long vertices;
        public long triangles;
        public OwnedFile[] ownedFiles;

        [Serializable] public sealed class OwnedFile { public string path; public string sha256; }
    }
}
