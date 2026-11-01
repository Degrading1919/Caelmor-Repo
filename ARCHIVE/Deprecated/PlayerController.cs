using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// LOCAL CLIENT-ONLY controller.
    /// - Reads player input
    /// - Applies local prediction movement
    /// - Sends move input to host
    ///
    /// All authoritative simulation occurs on host in WorldManager.ApplyPlayerMovementInputs().
    /// Client uses this only for visual responsiveness.
    /// </summary>
    public class PlayerController : MonoBehaviour
    {
        [Header("References")]
        public NetworkManager Network;
        public ClientWorld ClientWorld;

        [Header("Acceleration Settings")]
        public float walkSpeed = 3.4f;         // per VS design
        public float sprintSpeed = 4.8f;       // per VS design
        public float accelTimeWalk = 0.18f;
        public float accelTimeSprint = 0.28f;
        public float decelTime = 0.14f;

        [Header("Turning")]
        public float baseTurnRate = 420f;      // degrees/sec
        public float sprintTurnDampen = 0.85f; // 15% slower

        private Vector3 _velocity;
        private Vector3 _inputDir;
        private float _currentSpeed;
        private float _targetSpeed;

        private ClientEntity _local;

        private void Start()
        {
            _local = ClientWorld.GetOrCreateClientEntity(Network.LocalClientId.ToString());
        }

        private void Update()
        {
            if (_local == null)
                return;

            HandleInput();
            ApplyPrediction(Time.deltaTime);

            // Send input to host (unreliable)
            SendNetworkInput();
        }

        private void HandleInput()
        {
            float x = Input.GetAxisRaw("Horizontal");
            float y = Input.GetAxisRaw("Vertical");

            _inputDir = new Vector3(x, 0f, y);
            float mag = _inputDir.magnitude;

            if (mag > 1f)
                _inputDir.Normalize();

            // Walk if <60% input magnitude
            bool isSprint = mag >= 0.6f;

            _targetSpeed = isSprint ? sprintSpeed : walkSpeed;
        }

        private void ApplyPrediction(float dt)
        {
            // ACCELERATION
            float accel = (_targetSpeed == sprintSpeed)
                ? 1f / accelTimeSprint
                : 1f / accelTimeWalk;

            float decel = 1f / decelTime;

            if (_inputDir.sqrMagnitude > 0.001f)
            {
                _currentSpeed = Mathf.MoveTowards(
                    _currentSpeed,
                    _targetSpeed,
                    accel * dt * _targetSpeed
                );
            }
            else
            {
                _currentSpeed = Mathf.MoveTowards(
                    _currentSpeed,
                    0f,
                    decel * dt * _targetSpeed
                );
            }

            // MOVEMENT
            Vector3 displacement = _inputDir * (_currentSpeed * dt);
            _local.Position += displacement;

            // TURNING
            if (_inputDir.sqrMagnitude > 0.01f)
            {
                float turnRate = baseTurnRate;
                if (_targetSpeed == sprintSpeed)
                    turnRate *= sprintTurnDampen;

                Quaternion targetRot = Quaternion.LookRotation(_inputDir, Vector3.up);
                transform.rotation = Quaternion.RotateTowards(
                    transform.rotation,
                    targetRot,
                    turnRate * dt
                );
            }

            // Update client-world state for interpolation
            _local.RotationY = transform.rotation.eulerAngles.y;
            _local.TargetPosition = _local.Position;
        }

        private void SendNetworkInput()
        {
            Vector2 move = new Vector2(_inputDir.x, _inputDir.z);
            var msg = new PlayerInput_Move
            {
                PlayerId   = _local.EntityId,
                Direction  = move,
                ClientTime = Time.time
            };

            Network.SendPlayerMove(msg);
        }
    }
}
