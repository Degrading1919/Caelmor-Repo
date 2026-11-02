using System;
using System.IO;
using System.Text;

namespace Caelmor.Runtime.Gameplay
{
    /// <summary>
    /// Explicit, synchronous checkpoint publication. Call only at a stopped/between-tick
    /// save boundary or on a persistence worker; never from simulation execution.
    /// Validation completes before disk publication. Corrupt loads are reported, not repaired.
    /// </summary>
    public sealed class AtomicTextCheckpoint
    {
        private readonly string _path;
        private readonly object _gate = new object();
        public AtomicTextCheckpoint(string path)
        {
            if (string.IsNullOrWhiteSpace(path)) throw new ArgumentException("Checkpoint path is required.", nameof(path));
            _path = Path.GetFullPath(path);
        }
        public string PathName => _path;
        public bool Exists => File.Exists(_path);
        public string Read(Action<string> validate)
        {
            if (validate == null) throw new ArgumentNullException(nameof(validate));
            lock (_gate)
            {
                var text = File.ReadAllText(_path, Encoding.UTF8);
                validate(text);
                return text;
            }
        }
        public void Write(string text, Action<string> validate)
        {
            if (text == null) throw new ArgumentNullException(nameof(text));
            if (validate == null) throw new ArgumentNullException(nameof(validate));
            validate(text);
            lock (_gate)
            {
                Directory.CreateDirectory(Path.GetDirectoryName(_path)!);
                var temporary = _path + ".pending";
                try
                {
                    var bytes = new UTF8Encoding(false).GetBytes(text);
                    using (var stream = new FileStream(temporary, FileMode.Create, FileAccess.Write, FileShare.None))
                    {
                        stream.Write(bytes, 0, bytes.Length);
                        stream.Flush(true);
                    }
                    if (File.Exists(_path)) File.Replace(temporary, _path, _path + ".previous");
                    else File.Move(temporary, _path);
                }
                finally
                {
                    if (File.Exists(temporary)) File.Delete(temporary);
                }
            }
        }
    }
}
