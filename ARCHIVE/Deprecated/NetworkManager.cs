using System;
using System.Collections.Generic;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Minimal host-authoritative networking facade for the Vertical Slice.
    /// Wraps a pluggable transport (INetworkTransport) and:
    /// - Manages host/client role
    /// - Buffers client inputs for TickManager
    /// - Broadcasts snapshots & gameplay events
    /// - Handles join/leave flows
    ///
    /// NOTE: You must provide an INetworkTransport implementation that
    /// actually sends/receives bytes or messages (Mirror, NGO, custom, etc).
    /// </summary>
    public class NetworkManager : MonoBehaviour
    {
        public static NetworkManager Instance { get; private set; }

        public enum NetworkRole
        {
            None,
            Host,
            Client
        }

        // --------------------------------------------------------------------
        // Public API / State
        // --------------------------------------------------------------------

        public NetworkRole Role { get; private set; } = NetworkRole.None;

        /// <summary>Local logical clientId (0 on host; assigned by host on client).</summary>
        public int LocalClientId { get; private set; } = -1;

        /// <summary>True if we are running as host (server-authoritative).</summary>
        public bool IsHost => Role == NetworkRole.Host;

        /// <summary>True if we are running as a connected client.</summary>
        public bool IsClient => Role == NetworkRole.Client;

        /// <summary>Plug in your transport in the inspector or at runtime.</summary>
        public INetworkTransport Transport;

        // References (set by bootstrap / GameManager)
        public WorldManager WorldManager { get; set; }
        public SaveSystem   SaveSystem   { get; set; }

        // Host-side client registry
        private readonly Dictionary<int, RemoteClient> _clients =
            new Dictionary<int, RemoteClient>();

        // Host-side input buffering for TickManager
        private readonly InputBatch _bufferedInputs = new InputBatch();

        // Simple clientId counter for VS (not persisted)
        private int _nextClientId = 1; // 0 reserved for host

        // --------------------------------------------------------------------
        // Unity Lifecycle
        // --------------------------------------------------------------------

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;

            if (Transport != null)
                HookTransportEvents(Transport);
        }

        private void OnDestroy()
        {
            if (Transport != null)
                UnhookTransportEvents(Transport);
        }

        // --------------------------------------------------------------------
        // Public Role Setup
        // --------------------------------------------------------------------

        /// <summary>
        /// Initialize as host (server + local player).
        /// </summary>
        public void StartHost()
        {
            if (Transport == null)
            {
                Debug.LogError("NetworkManager.StartHost: No transport assigned.");
                return;
            }

            Role          = NetworkRole.Host;
            LocalClientId = 0;

            Transport.StartHost();
            Debug.Log("[NetworkManager] Host started.");
        }

        /// <summary>
        /// Initialize as client and connect to specified host address.
        /// </summary>
        public void StartClient(string address)
        {
            if (Transport == null)
            {
                Debug.LogError("NetworkManager.StartClient: No transport assigned.");
                return;
            }

            Role = NetworkRole.Client;
            Transport.StartClient(address);
            Debug.Log("[NetworkManager] Client connecting to " + address + "...");
        }

        /// <summary>
        /// Disconnect from current session (host or client).
        /// </summary>
        public void Disconnect()
        {
            if (Transport == null) return;

            if (IsClient)
            {
                // Best-effort leave notice to host.
                var msg = new Msg_LeaveNotice { ClientId = LocalClientId };
                Transport.SendToServer(msg, reliable: true);
            }

            if (IsHost)
            {
                // Graceful host shutdown for clients.
                var shutdown = new Msg_Shutdown();
                Broadcast(shutdown, reliable: true);
            }

            Transport.Stop();
            Role          = NetworkRole.None;
            LocalClientId = -1;
            _clients.Clear();

            Debug.Log("[NetworkManager] Disconnected.");
        }

        // --------------------------------------------------------------------
        // TickManager Integration (Host Side)
        // --------------------------------------------------------------------

        /// <summary>
        /// Drains buffered input messages accumulated since the last tick.
        /// Called only on host by TickManager.
        /// </summary>
        public InputBatch DrainBufferedInputs()
        {
            var batch = new InputBatch();
            batch.MovementCommands.AddRange(_bufferedInputs.MovementCommands);
            batch.AttackCommands.AddRange(_bufferedInputs.AttackCommands);
            // Future: add inventory, crafting, etc.

            _bufferedInputs.MovementCommands.Clear();
            _bufferedInputs.AttackCommands.Clear();

            return batch;
        }

        /// <summary>
        /// Broadcasts the authoritative transform snapshot to all connected clients.
        /// Called from TickManager each tick (or every N ticks).
        /// </summary>
        public void BroadcastTransformSnapshot(TransformSnapshot snapshot)
        {
            if (!IsHost || Transport == null) return;

            var msg = new Msg_Snapshot_Transforms
            {
                TickIndex = TickManager.Instance != null
                    ? TickManager.Instance.CurrentTickIndex
                    : 0,
                Snapshot = snapshot
            };

            Broadcast(msg, reliable: false);
        }

        /// <summary>
        /// Broadcasts HP snapshot (coarser-grained than transform snapshots).
        /// </summary>
        public void BroadcastHpSnapshot(HpSnapshot snapshot)
        {
            if (!IsHost || Transport == null) return;

            var msg = new Msg_HpSnapshot
            {
                Snapshot = snapshot
            };

            Broadcast(msg, reliable: true);
        }

        /// <summary>
        /// Broadcast a combat result event to all relevant clients.
        /// </summary>
        public void BroadcastCombatEvent(Event_CombatResult evt)
        {
            if (!IsHost || Transport == null) return;

            var msg = new Msg_Event_CombatResult { Event = evt };
            Broadcast(msg, reliable: true);
        }

        // Future: BroadcastInventoryChanged, BroadcastCraftingResult, etc.

        // --------------------------------------------------------------------
        // Client → Host send helpers
        // --------------------------------------------------------------------

        /// <summary>
        /// Called on client to send movement input to host (unreliable).
        /// </summary>
        public void SendPlayerMove(PlayerInput_Move move)
        {
            if (!IsClient || Transport == null) return;
            Transport.SendToServer(move, reliable: false);
        }

        /// <summary>
        /// Called on client to send attack input to host (reliable).
        /// </summary>
        public void SendPlayerAttack(PlayerInput_Attack attack)
        {
            if (!IsClient || Transport == null) return;
            Transport.SendToServer(attack, reliable: true);
        }

        /// <summary>
        /// Generic client → host send (for quest, inventory, crafting, etc.).
        /// </summary>
        public void SendToHost(object message, bool reliable = true)
        {
            if (!IsClient || Transport == null) return;
            Transport.SendToServer(message, reliable);
        }

        // --------------------------------------------------------------------
        // Host-side client registry & join/leave
        // --------------------------------------------------------------------

        private void HandleClientConnected(int transportClientId)
        {
            if (!IsHost) return;

            int assignedClientId = _nextClientId++;
            var rc = new RemoteClient
            {
                TransportConnectionId = transportClientId,
                ClientId              = assignedClientId,
                PlayerId              = null
            };
            _clients[assignedClientId] = rc;

            Debug.Log($"[NetworkManager] Client connected: transportId={transportClientId}, clientId={assignedClientId}");
        }

        private void HandleClientDisconnected(int transportClientId)
        {
            if (!IsHost) return;

            int clientId = FindClientIdByTransport(transportClientId);
            if (clientId == -1) return;

            if (_clients.TryGetValue(clientId, out var rc))
            {
                // Despawn player entity & persist PlayerSave
                if (!string.IsNullOrEmpty(rc.PlayerId))
                {
                    if (WorldManager != null)
                    {
                        WorldManager.DespawnPlayer(rc.PlayerId);
                    }
                    if (SaveSystem != null)
                    {
                        SaveSystem.SavePlayer(rc.PlayerId);
                    }

                    // Notify other clients
                    var despawn = new Msg_PlayerDespawn { PlayerId = rc.PlayerId };
                    Broadcast(despawn, reliable: true, exceptClientId: clientId);
                }

                _clients.Remove(clientId);
                Debug.Log($"[NetworkManager] Client disconnected: clientId={clientId}");
            }
        }

        private int FindClientIdByTransport(int transportClientId)
        {
            foreach (var kvp in _clients)
            {
                if (kvp.Value.TransportConnectionId == transportClientId)
                    return kvp.Key;
            }
            return -1;
        }

        // --------------------------------------------------------------------
        // Transport Hooks
        // --------------------------------------------------------------------

        private void HookTransportEvents(INetworkTransport t)
        {
            t.OnServerClientConnected    += HandleClientConnected;
            t.OnServerClientDisconnected += HandleClientDisconnected;
            t.OnServerDataReceived       += HandleServerDataReceived;
            t.OnClientDataReceived       += HandleClientDataReceived;
        }

        private void UnhookTransportEvents(INetworkTransport t)
        {
            t.OnServerClientConnected    -= HandleClientConnected;
            t.OnServerClientDisconnected -= HandleClientDisconnected;
            t.OnServerDataReceived       -= HandleServerDataReceived;
            t.OnClientDataReceived       -= HandleClientDataReceived;
        }

        /// <summary>
        /// Host: called by transport when a message arrives from a client.
        /// </summary>
        private void HandleServerDataReceived(int transportClientId, object message)
        {
            if (!IsHost) return;

            // Join / leave messages
            if (message is Msg_JoinRequest join)
            {
                ProcessJoinRequest(transportClientId, join);
                return;
            }

            if (message is Msg_LeaveNotice leave)
            {
                HandleClientDisconnected(transportClientId);
                return;
            }

            // Gameplay input messages → route into input buffer for TickManager
            if (message is PlayerInput_Move move)
            {
                _bufferedInputs.MovementCommands.Add(move);
            }
            else if (message is PlayerInput_Attack attack)
            {
                _bufferedInputs.AttackCommands.Add(attack);
            }
            else
            {
                // Other request types (inventory, crafting, etc.) should be
                // routed to the appropriate systems here.
                // e.g., CraftingSystem.HandleCraftRequest, InventorySystem.HandleAction, etc.
            }
        }

        /// <summary>
        /// Client: called by transport when a message arrives from the host.
        /// </summary>
        private void HandleClientDataReceived(object message)
        {
            if (!IsClient) return;

            // Join handshake
            if (message is Msg_JoinAccept joinAccept)
            {
                LocalClientId = joinAccept.AssignedClientId;
                // Initialize local player & world snapshots.
                // (GameManager / WorldManager should handle this in project-specific code.)
                return;
            }

            if (message is Msg_Shutdown)
            {
                Debug.LogWarning("[NetworkManager] Host shutdown received.");
                // Go back to main menu, show dialog, etc.
                return;
            }

            // Transform snapshots
            if (message is Msg_Snapshot_Transforms snapMsg)
            {
                // Forward to client world interpolator
                var clientWorld = FindObjectOfType<ClientWorld>();
                if (clientWorld != null)
                {
                    clientWorld.ApplyTransformSnapshot(snapMsg.Snapshot);
                }
                return;
            }

            // HP snapshots
            if (message is Msg_HpSnapshot hpMsg)
            {
                var clientWorld = FindObjectOfType<ClientWorld>();
                if (clientWorld != null)
                {
                    clientWorld.ApplyHpSnapshot(hpMsg.Snapshot);
                }
                return;
            }

            // Combat events
            if (message is Msg_Event_CombatResult combatMsg)
            {
                // Route to combat UI / hit reactions.
                // For VS, you can simply update HP bars from combatMsg.Event.NewHp.
                return;
            }

            // Player spawn / despawn, world object updates, etc. can be added here.
        }

        // --------------------------------------------------------------------
        // Join Handshake (Host)
        // --------------------------------------------------------------------

        private void ProcessJoinRequest(int transportClientId, Msg_JoinRequest join)
        {
            // Version check (simplified)
            if (join.ClientVersion != VSVersion.Current)
            {
                // Optionally send a reject message and close connection.
                Transport.KickClient(transportClientId, "Version mismatch");
                return;
            }

            int clientId = FindClientIdByTransport(transportClientId);
            if (clientId == -1)
            {
                Debug.LogWarning("[NetworkManager] JoinRequest from unknown transport client.");
                return;
            }

            string playerId = join.DesiredPlayerId;
            if (string.IsNullOrEmpty(playerId))
            {
                playerId = Guid.NewGuid().ToString("N");
            }

            _clients[clientId] = new RemoteClient
            {
                TransportConnectionId = transportClientId,
                ClientId              = clientId,
                PlayerId              = playerId
            };

            // Load or create PlayerSave and world snapshot.
            PlayerSave  playerSave  = SaveSystem != null ? SaveSystem.LoadPlayerOrCreateDefault(playerId) : new PlayerSave();
            WorldSnapshot worldSnap = WorldManager != null ? WorldManager.BuildInitialWorldSnapshotForPlayer(playerId) : new WorldSnapshot();

            // Spawn authoritative player entity on host.
            if (WorldManager != null)
            {
                WorldManager.SpawnPlayerFromSave(playerSave);
            }

            // Send JoinAccept with baseline state.
            var accept = new Msg_JoinAccept
            {
                AssignedClientId = clientId,
                PlayerSnapshot   = playerSave,
                WorldSnapshot    = worldSnap
            };

            Transport.SendToClient(transportClientId, accept, reliable: true);

            // Notify existing clients to spawn this player, and send them to the new client.
            var spawn = new Msg_PlayerSpawn { PlayerId = playerId };
            Broadcast(spawn, reliable: true, exceptClientId: clientId);

            Debug.Log($"[NetworkManager] Join accepted. clientId={clientId}, playerId={playerId}");
        }

        // --------------------------------------------------------------------
        // Host broadcast helpers
        // --------------------------------------------------------------------

        private void Broadcast(object message, bool reliable, int exceptClientId = -1)
        {
            if (!IsHost || Transport == null) return;

            foreach (var kvp in _clients)
            {
                int clientId = kvp.Key;
                if (clientId == exceptClientId) continue;

                var rc = kvp.Value;
                Transport.SendToClient(rc.TransportConnectionId, message, reliable);
            }
        }

        // --------------------------------------------------------------------
        // Helper types
        // --------------------------------------------------------------------

        /// <summary>
        /// Host-side representation of a connected remote client.
        /// </summary>
        private class RemoteClient
        {
            public int    TransportConnectionId;
            public int    ClientId;
            public string PlayerId;
        }
    }

    // ------------------------------------------------------------------------
    // Transport Abstraction Interface
    // ------------------------------------------------------------------------

    /// <summary>
    /// Simple transport abstraction for the VS. Implement this with Mirror,
    /// NGO, or a custom socket layer.
    /// </summary>
    public interface INetworkTransport
    {
        // Server side
        event Action<int>                 OnServerClientConnected;
        event Action<int>                 OnServerClientDisconnected;
        event Action<int, object>         OnServerDataReceived;

        // Client side
        event Action<object>              OnClientDataReceived;

        void StartHost();
        void StartClient(string address);
        void Stop();

        void SendToClient(int transportClientId, object message, bool reliable);
        void SendToServer(object message, bool reliable);

        void KickClient(int transportClientId, string reason);
    }

    // ------------------------------------------------------------------------
    // Message DTOs for handshake & events used here
    // (You likely have some of these already; keep them in sync with your
    // existing NetworkMessages.cs, or move them there.)
    // ------------------------------------------------------------------------

    public static class VSVersion
    {
        // Keep in sync with client build; update as needed.
        public const int Current = 1;
    }

    public struct Msg_JoinRequest
    {
        public string DesiredPlayerId;
        public int    ClientVersion;
    }

    public struct Msg_JoinAccept
    {
        public int          AssignedClientId;
        public PlayerSave   PlayerSnapshot;
        public WorldSnapshot WorldSnapshot;
    }

    public struct Msg_LeaveNotice
    {
        public int ClientId;
    }

    public struct Msg_Shutdown { }

    public struct Msg_PlayerSpawn
    {
        public string PlayerId;
    }

    public struct Msg_PlayerDespawn
    {
        public string PlayerId;
    }

    public struct Msg_Snapshot_Transforms
    {
        public long            TickIndex;
        public TransformSnapshot Snapshot;
    }

    public struct Msg_HpSnapshot
    {
        public HpSnapshot Snapshot;
    }

    public struct Msg_Event_CombatResult
    {
        public Event_CombatResult Event;
    }

    // These are placeholder types expected to exist elsewhere in your VS:
    // - PlayerSave
    // - WorldSnapshot
    // - TransformSnapshot
    // - HpSnapshot
    // - Event_CombatResult
    // - InputBatch
    // - PlayerInput_Move
    // - PlayerInput_Attack
    // - ClientWorld
    // - SaveSystem
    // - WorldManager
}
