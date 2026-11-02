using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using Caelmor.Runtime.Gameplay;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    /// <summary>
    /// Between-tick durable progress. The caller only marks commits inside simulation;
    /// Pump/Flush and loading are called outside it. Paths are injected so batch tests
    /// never need Application.persistentDataPath or player preferences.
    /// </summary>
    public sealed class GameplayCheckpointService
    {
        const double PeriodicSeconds=2;
        readonly Func<GameplaySave> capture;
        readonly Func<GameplaySave,GameplaySave> prepareRestore;
        readonly Func<string,bool> compatibleIdentity;
        readonly string identity;
        readonly AtomicTextCheckpoint automatic,manual;
        bool dirty,critical,blocked,writeBlocked;
        long revision=-1;
        double lastWrite=double.NegativeInfinity;
        public string Status {get;private set;}="Progress is saved automatically. F5 saves now; F9 reconnects without resetting quests.";
        public bool IsBlocked=>blocked;
        public int AutomaticWrites {get;private set;}
        public string AutomaticPath=>automatic.PathName;
        public string ManualPath=>manual.PathName;

        public GameplayCheckpointService(string manualPath,string contentIdentity,Func<GameplaySave> capture,
            Func<GameplaySave,GameplaySave> prepareRestore,Func<string,bool> compatibleIdentity)
        {
            this.capture=capture??throw new ArgumentNullException(nameof(capture));
            this.prepareRestore=prepareRestore??throw new ArgumentNullException(nameof(prepareRestore));
            this.compatibleIdentity=compatibleIdentity??throw new ArgumentNullException(nameof(compatibleIdentity));
            identity=contentIdentity??throw new ArgumentNullException(nameof(contentIdentity));
            manual=new AtomicTextCheckpoint(manualPath);
            automatic=new AtomicTextCheckpoint(Path.Combine(Path.GetDirectoryName(manual.PathName),"lowmark-gameplay.autosave.json"));
        }

        public void MarkCommitted(long durableRevision)
        {
            if(blocked)return;
            dirty=true;
            if(revision!=durableRevision){critical=true;revision=durableRevision;}
        }

        public bool Pump(double now)
        {
            if(blocked || !dirty || !critical && now-lastWrite<PeriodicSeconds)return false;
            Flush(now);return true;
        }

        public void Flush(double now)
        {
            DemandUnblocked();
            try
            {
                var text=EncodeValidated(capture());
                PreserveIncompatibleBeforeWrite(automatic.PathName);
                automatic.Write(text,ValidateCurrentText);
                dirty=critical=false;lastWrite=now;AutomaticWrites++;
                Status="Progress saved automatically.";
            }
            catch(Exception error){BlockWrite(error);throw;}
        }

        public void SaveExplicit(double now)
        {
            DemandUnblocked();
            try
            {
                var text=EncodeValidated(capture());
                PreserveIncompatibleBeforeWrite(manual.PathName);
                manual.Write(text,ValidateCurrentText);
                // The canonical resume slot must be at least as recent as the manual copy.
                PreserveIncompatibleBeforeWrite(automatic.PathName);
                automatic.Write(text,ValidateCurrentText);
                dirty=critical=false;lastWrite=now;AutomaticWrites++;
                Status="Progress checkpoint saved. Active quests and choices are retained.";
            }
            catch(Exception error){BlockWrite(error);throw;}
        }

        public void RetryFlush(double now)
        {
            if(!writeBlocked)throw new InvalidOperationException("Only a failed write may be retried; unsupported or corrupt restore cannot be replaced by fresh progress.");
            blocked=writeBlocked=false;Flush(now);
        }

        /// <summary>Null means no profile exists. Existing invalid data never means a new game.</summary>
        public GameplaySave LoadLatest()
        {
            DemandUnblocked();
            var candidates=new[]{automatic.PathName,automatic.PathName+".previous",manual.PathName,manual.PathName+".previous"};
            var failures=new List<string>();bool found=false;
            foreach(var path in candidates)
            {
                if(!File.Exists(path))continue;
                found=true;
                try
                {
                    var raw=File.ReadAllText(path,Encoding.UTF8);
                    var saved=Decode(raw);
                    if(!compatibleIdentity(saved.contentId))
                    {
                        blocked=true;
                        throw new UnsupportedCheckpointException("A checkpoint belongs to unsupported content. It was retained and was not replaced.");
                    }
                    var restored=prepareRestore(saved);
                    if(saved.contentId!=identity)ArchiveExact(path,"before-upgrade");
                    bool recovery=failures.Count>0 || path.EndsWith(".previous",StringComparison.Ordinal);
                    if(recovery)
                    {
                        // Keep both the rejected primary and chosen good backup before the
                        // next File.Replace can rotate .previous.
                        foreach(var existing in candidates)if(File.Exists(existing))ArchiveExact(existing,"before-recovery");
                    }
                    Status=recovery?"Recovered a valid progress backup. Original checkpoint files were retained.":saved.contentId!=identity?
                        "Progress upgraded from a supported published build. Original bytes were retained.":"Progress resumed. Active quests and choices were retained.";
                    return restored;
                }
                catch(UnsupportedCheckpointException){throw;}
                catch(Exception error) when(error is IOException || error is UnauthorizedAccessException || error is ArgumentException || error is InvalidOperationException)
                {failures.Add(Path.GetFileName(path)+": "+error.Message);}
            }
            if(found)
            {
                blocked=true;Status="Progress could not be restored. Existing saves were retained; gameplay is blocked to prevent a reset.";
                throw new InvalidOperationException(Status+" "+string.Join(" | ",failures));
            }
            Status="New progress profile. Progress will save automatically.";
            return null;
        }

        public GameplaySave ValidateLatestForReconnect()=>LoadLatest();

        string EncodeValidated(GameplaySave save)
        {
            if(save==null || save.contentId!=identity)throw new InvalidOperationException("Only the current validated progress profile can be written.");
            prepareRestore(save);
            return JsonUtility.ToJson(save,true);
        }
        void ValidateCurrentText(string text)
        {
            var save=Decode(text);
            if(save.contentId!=identity)throw new InvalidOperationException("Checkpoint write identity mismatch.");
            prepareRestore(save);
        }
        public static GameplaySave Decode(string text)
        {
            CheckpointJsonShape.Validate(text);
            var save=JsonUtility.FromJson<GameplaySave>(text);
            if(save==null)throw new InvalidOperationException("Checkpoint JSON has no profile.");
            CheckpointJsonShape.ValidateLegacyShape(text,save.contentId);
            return save;
        }
        void PreserveIncompatibleBeforeWrite(string path)
        {
            if(!File.Exists(path))return;
            try {if(Decode(File.ReadAllText(path,Encoding.UTF8)).contentId==identity)return;}
            catch(Exception error) when(error is ArgumentException || error is InvalidOperationException){}
            ArchiveExact(path,"before-replacement");
        }
        static void ArchiveExact(string path,string reason)
        {
            byte[] bytes=File.ReadAllBytes(path);string hash;
            using(var sha=SHA256.Create())hash=BitConverter.ToString(sha.ComputeHash(bytes)).Replace("-","");
            string preserved=path+"."+reason+"."+hash+".json";
            if(File.Exists(preserved))
            {
                using(var sha=SHA256.Create())
                using(var stream=File.OpenRead(preserved))
                    if(BitConverter.ToString(sha.ComputeHash(stream)).Replace("-","")!=hash)throw new IOException("Immutable checkpoint archive does not match its original bytes.");
                return;
            }
            // Copy exact bytes including BOM/whitespace, never a reserialized substitute.
            File.Copy(path,preserved,false);
            using(var sha=SHA256.Create())
            using(var stream=File.OpenRead(preserved))
                if(BitConverter.ToString(sha.ComputeHash(stream)).Replace("-","")!=hash)throw new IOException("Checkpoint archive verification failed.");
        }
        void DemandUnblocked(){if(blocked)throw new InvalidOperationException("Checkpoint recovery is blocked; existing progress will not be overwritten.");}
        void BlockWrite(Exception error){blocked=writeBlocked=true;Status="Progress could not be saved. Gameplay is paused to retain unflushed progress: "+error.Message;}
        sealed class UnsupportedCheckpointException : InvalidOperationException {public UnsupportedCheckpointException(string message):base(message){}}
    }
}
