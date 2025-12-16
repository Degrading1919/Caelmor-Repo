namespace Caelmor.Systems
{
    /// <summary>
    /// Server authority boundary for runtime infrastructure. Centralized to avoid
    /// duplicate interface declarations across subsystems.
    /// </summary>
    public interface IServerAuthority
    {
        bool IsServerAuthoritative { get; }
    }
}
