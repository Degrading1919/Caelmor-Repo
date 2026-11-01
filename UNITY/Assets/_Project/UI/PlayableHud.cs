using UnityEngine;

namespace Caelmor.Unity.Playable
{
    public sealed class PlayableHud : MonoBehaviour
    {
        public PlayableBootstrap game;
        GUIStyle title, label, small, value;
        Texture2D dark, accent;
        internal static bool BlocksPointer(PlayableBootstrap game, Vector2 screen)
        {
            if (game.HelpOpen) return true;
            float scale = Mathf.Min(Screen.width / 1280f, Screen.height / 720f);
            var point = new Vector2((screen.x - (Screen.width - 1280 * scale) / 2) / scale,
                (Screen.height - screen.y - (Screen.height - 720 * scale) / 2) / scale);
            if (new Rect(24, 24, 418, 110).Contains(point) || new Rect(946, 24, 310, 172).Contains(point) ||
                new Rect(24, 584, 1232, 112).Contains(point)) return true;
            var target = game.playerCamera.WorldToScreenPoint(game.interactionAnchor.transform.position + Vector3.up * 2.1f);
            if (target.z <= 0) return false;
            var labelPoint = new Vector2((target.x - (Screen.width - 1280 * scale) / 2) / scale,
                (Screen.height - target.y - (Screen.height - 720 * scale) / 2) / scale);
            return new Rect(labelPoint.x - 135, labelPoint.y - 18, 270, 54).Contains(point);
        }
        void OnGUI()
        {
            EnsureStyles();
            float scale = Mathf.Min(Screen.width / 1280f, Screen.height / 720f);
            GUI.matrix = Matrix4x4.TRS(new Vector3((Screen.width - 1280 * scale) / 2, (Screen.height - 720 * scale) / 2), Quaternion.identity, Vector3.one * scale);
            GUI.DrawTexture(new Rect(24, 24, 418, 110), dark);
            GUI.DrawTexture(new Rect(24, 24, 4, 110), accent);
            GUI.Label(new Rect(44, 36, 380, 32), "CAELMOR", title);
            GUI.Label(new Rect(44, 75, 380, 24), "PLAYABLE RUNTIME  /  TECHNICAL GREYBOX", small);
            GUI.Label(new Rect(44, 102, 380, 24), "A foundation for the first Lowmark narrative.", small);
            if (game == null || game.Host == null)
            {
                GUI.Label(new Rect(40, 180, 1160, 450), "Runtime could not start.\n" + game?.StartupFailure, label);
                return;
            }
            var state = game.Host.Snapshot;
            GUI.DrawTexture(new Rect(946, 24, 310, 172), dark);
            GUI.Label(new Rect(968, 38, 270, 25), "HOST AUTHORITY", label);
            GUI.Label(new Rect(968, 72, 270, 25), "10 Hz  ·  tick " + state.Tick.ToString("D6"), value);
            GUI.Label(new Rect(968, 106, 270, 24), "Position  " + state.Position.x.ToString("F1") + " / " + state.Position.z.ToString("F1"), small);
            GUI.Label(new Rect(968, 130, 270, 24), (state.Sprinting ? "SPRINTING" : "WALK / IDLE") + "  ·  session active", small);
            GUI.Label(new Rect(968, 154, 270, 24), "Committed interactions  " + state.InteractionCount, small);
            var anchor = game.interactionAnchor;
            float distance = Vector3.Distance(state.Position, anchor.transform.position);
            Vector3 target = game.playerCamera.WorldToScreenPoint(anchor.transform.position + Vector3.up * 2.1f);
            if (target.z > 0)
            {
                float x = (target.x - (Screen.width - 1280 * scale) / 2) / scale;
                float y = (Screen.height - target.y - (Screen.height - 720 * scale) / 2) / scale;
                GUI.DrawTexture(new Rect(x - 135, y - 18, 270, 54), dark);
                GUI.Label(new Rect(x - 124, y - 13, 250, 25), anchor.displayName, label);
                GUI.Label(new Rect(x - 124, y + 11, 250, 24), distance <= anchor.interactionRange ? "[ E ]  Interact" : distance.ToString("F1") + " m  ·  approach to interact", small);
            }
            GUI.DrawTexture(new Rect(24, 584, 1232, 112), dark);
            GUI.Label(new Rect(44, 599, 1180, 25), state.Feedback, label);
            GUI.Label(new Rect(44, 635, 1180, 25), "LEFT CLICK   Move       SHIFT   Sprint       E   Interact       RMB   Orbit       Wheel   Zoom       ESC   Help       F3   Debug WASD", small);
            GUI.Label(new Rect(44, 666, 1180, 22), "Scene fixtures only. No narrative, rewards, or production world content is loaded. Session resets on exit.", small);
            if (game.HelpOpen)
            {
                GUI.DrawTexture(new Rect(290, 184, 700, 330), dark);
                GUI.Label(new Rect(320, 210, 640, 36), "Explore the runtime", title);
                GUI.Label(new Rect(320, 266, 640, 130), "Left-click terrain to walk; click again to change destination.\nThe host finds a route around obstacles. Hold Shift to sprint.\nApproach the amber marker, then press E to interact.\nMovement and interactions commit on the 10 Hz host tick.", label);
                GUI.Label(new Rect(320, 402, 640, 44), "RMB: orbit. Wheel: zoom. F3: optional WASD debug controls.\nEscape stops your route and opens or closes this panel.", small);
                if (GUI.Button(new Rect(320, 460, 145, 32), "Quit application")) Application.Quit();
            }
        }
        void EnsureStyles()
        {
            if (title != null) return;
            title = new GUIStyle(GUI.skin.label) { fontSize = 25, fontStyle = FontStyle.Bold, normal = { textColor = new Color(.91f, .86f, .70f) } };
            label = new GUIStyle(GUI.skin.label) { fontSize = 17, normal = { textColor = new Color(.94f, .94f, .90f) } };
            small = new GUIStyle(GUI.skin.label) { fontSize = 13, normal = { textColor = new Color(.70f, .76f, .75f) } };
            value = new GUIStyle(label) { fontSize = 21, normal = { textColor = new Color(.37f, .85f, .70f) } };
            dark = Texture(new Color(.035f, .065f, .075f, .94f)); accent = Texture(new Color(.67f, .51f, .26f));
        }
        static Texture2D Texture(Color color)
        { var texture = new Texture2D(1, 1); texture.SetPixel(0, 0, color); texture.Apply(); return texture; }
        void OnDestroy() { if (dark != null) Destroy(dark); if (accent != null) Destroy(accent); }
    }
}
