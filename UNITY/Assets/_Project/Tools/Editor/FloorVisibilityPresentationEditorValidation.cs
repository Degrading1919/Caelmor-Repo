using System;
using Caelmor.Unity.Playable;
using UnityEditor;
using UnityEngine;

namespace Caelmor.Unity.Editor
{
    public static class FloorVisibilityPresentationEditorValidation
    {
        [MenuItem("Caelmor/Validate floor visibility presentation")]
        public static void Run()
        {
            try
            {
                FloorVisibilityPresentationValidation.Run();
                Debug.Log("CAELMOR_FLOOR_VISIBILITY_CHECKS_PASSED");
            }
            catch (Exception error)
            {
                Debug.LogError("CAELMOR_FLOOR_VISIBILITY_CHECKS_FAILED: " + error);
                if (Application.isBatchMode) EditorApplication.Exit(1);
                throw;
            }
            if (Application.isBatchMode) EditorApplication.Exit(0);
        }
    }
}
