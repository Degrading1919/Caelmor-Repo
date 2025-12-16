using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Client-only camera controller matching the VS Movement & Camera Design.
    /// - Top-down / OTS hybrid
    /// - Smooth follow + rotation smoothing
    /// - Collision correction
    /// - Pitch + height clamping
    ///
    /// No network authority; camera is purely local.
    /// </summary>
    public class CameraController : MonoBehaviour
    {
        [Header("Follow Target")]
        public Transform target;

        [Header("Camera Settings")]
        public float defaultHeight = 9.5f; // spec
        public float minHeight = 8f;
        public float maxHeight = 12.5f;
        public float pitch = 52f;         // Degrees, fixed tilt
        public float fov = 38f;           // Top-down readability

        [Header("Smoothing")]
        public float positionLag = 0.12f;
        public float rotationLag = 0.06f;

        [Header("Collision")]
        public LayerMask collisionMask;
        public float collisionRadius = 0.45f;

        private Vector3 _camOffset;
        private Camera _cam;

        private void Awake()
        {
            _cam = GetComponentInChildren<Camera>();

            if (_cam != null)
                _cam.fieldOfView = fov;

            // Precompute the camera offset from design
            _camOffset = Quaternion.Euler(pitch, 0f, 0f) * new Vector3(0f, 0f, -defaultHeight);
        }

        private void LateUpdate()
        {
            if (target == null)
                return;

            Vector3 desiredPos = target.position + _camOffset;

            // Smooth follow
            transform.position = Vector3.Lerp(
                transform.position,
                desiredPos,
                1f - Mathf.Exp(-Time.deltaTime / positionLag)
            );

            // Smooth rotation (camera yaw is fixed in VS)
            Quaternion desiredRot = Quaternion.Euler(pitch, 0f, 0f);
            transform.rotation = Quaternion.Lerp(
                transform.rotation,
                desiredRot,
                1f - Mathf.Exp(-Time.deltaTime / rotationLag)
            );

            // Collision correction
            ApplyCameraCollision();
        }

        private void ApplyCameraCollision()
        {
            if (_cam == null)
                return;

            Vector3 camDir = (_cam.transform.position - target.position).normalized;
            float camDist = Vector3.Distance(target.position, _cam.transform.position);

            if (Physics.SphereCast(
                target.position,
                collisionRadius,
                camDir,
                out RaycastHit hit,
                camDist,
                collisionMask
            ))
            {
                float correctedDist = Mathf.Clamp(hit.distance, minHeight, maxHeight);
                Vector3 correctedPos = target.position + camDir * correctedDist;
                _cam.transform.position = correctedPos;
            }
        }
    }
}
