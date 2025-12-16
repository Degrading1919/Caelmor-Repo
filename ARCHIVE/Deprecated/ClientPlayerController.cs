using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Local-only movement prediction and input sending.
    /// </summary>
    public class ClientPlayerController : MonoBehaviour
    {
        public NetworkManager NetworkManager;
        public ClientEntity   LocalEntity;

        private void Update()
        {
            Vector2 input = ReadMovementInput();
            float   dt    = Time.deltaTime;

            if (input.sqrMagnitude > float.Epsilon)
            {
                Vector3 dir = new Vector3(input.x, 0f, input.y).normalized;
                LocalEntity.Position += dir * GameConstants.MOVE_SPEED * dt;
            }

            var msg = new PlayerInput_Move
            {
                PlayerId   = LocalEntity.EntityId,
                Direction  = input,
                ClientTime = Time.time
            };

            NetworkManager.SendToHost(msg);
        }

        private Vector2 ReadMovementInput()
        {
            float x = Input.GetAxisRaw("Horizontal");
            float y = Input.GetAxisRaw("Vertical");
            return new Vector2(x, y);
        }
    }
}
