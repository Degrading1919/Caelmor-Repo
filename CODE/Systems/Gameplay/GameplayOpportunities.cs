#nullable disable
using System;
using System.Collections.Generic;
using System.Linq;

namespace Caelmor.Runtime.Gameplay
{
    public sealed partial class GameplaySession
    {
        public GameplayPoint CurrentTargetPosition(int target)
        {
            if(target<0 || target>=content.targets.Length)throw new ArgumentOutOfRangeException(nameof(target));
            return TargetPoint(current,target);
        }
        public FlockProgress Flock(int index)=>CloneFlock(current.data.flocks[index]);
        public PresentationProgress Presentation(int index)=>ClonePresentation(current.data.presentations[index]);
        static FlockProgress CloneFlock(FlockProgress f)=>new FlockProgress{id=f.id,positionIndex=f.positionIndex,warning=f.warning,prepared=f.prepared,recoveryPending=f.recoveryPending};
        static PresentationProgress ClonePresentation(PresentationProgress p)=>new PresentationProgress{id=p.id,seen=p.seen,remaining=p.remaining};
        GameplayPoint TargetPoint(State state,int target)
        {
            var t=content.targets[target];
            for(int i=0;i<content.flocks.Length;i++)
                if(content.flocks[i].target==t.id && state.data.flocks[i].positionIndex==1)
                {t=content.targets.First(v=>v.id==content.flocks[i].alternateTarget);break;}
            return new GameplayPoint(t.x,t.z);
        }
        bool OpportunityTargetVisible(State state,int target)
        {
            var id=content.targets[target].id;
            for(int i=0;i<content.flocks.Length;i++)
            {
                var f=content.flocks[i];var progress=state.data.flocks[i];
                if(id==f.target || id==f.recoveryTarget)
                {
                    if(!Meets(state.flags,f.all,f.none,Array.Empty<string>(),0))return false;
                    return id==f.target?!progress.recoveryPending:progress.recoveryPending;
                }
            }
            return true;
        }
        bool OpportunityEnabled(State state,ActionDefinition action)
        {
            if(string.IsNullOrEmpty(action.flock))return true;
            int i=Array.FindIndex(content.flocks,f=>f.id==action.flock);var definition=content.flocks[i];var progress=state.data.flocks[i];
            if(!Meets(state.flags,definition.all,definition.none,Array.Empty<string>(),0))return false;
            switch(action.flockOperation)
            {
                case "prepare":return !progress.recoveryPending && progress.warning==0;
                case "resolve":return !progress.recoveryPending && progress.prepared && progress.warning==0;
                case "recover":return progress.recoveryPending;
                default:return false;
            }
        }
        bool OpportunityCanUse(State state,ActionDefinition action,float x,float z)
        {
            if(string.IsNullOrEmpty(action.flock))return true;
            var f=content.flocks.First(d=>d.id==action.flock);
            if(action.flockOperation=="prepare")
            {var t=content.targets.First(v=>v.id==f.coverTarget);return Distance(x,z,t.x,t.z)<=f.coverRadius;}
            if(action.flockOperation=="resolve")
            {var t=content.targets.First(v=>v.id==f.closedTarget);return Distance(x,z,t.x,t.z)>f.closedRadius;}
            return true;
        }
        void ApplyOpportunity(ActionDefinition action)
        {
            if(string.IsNullOrEmpty(action.flock))return;
            var p=draft.data.flocks[Array.FindIndex(content.flocks,f=>f.id==action.flock)];
            switch(action.flockOperation)
            {
                case "prepare":p.prepared=true;break;
                case "resolve":p.recoveryPending=true;break;
                case "recover":p.recoveryPending=false;p.prepared=false;break;
            }
        }
        void TickFlocks(float x,float z,bool rushing)
        {
            for(int i=0;i<content.flocks.Length;i++)
            {
                var f=content.flocks[i];var p=draft.data.flocks[i];
                if(!Meets(draft.flags,f.all,f.none,Array.Empty<string>(),0)){p.warning=0;p.prepared=false;continue;}
                if(p.recoveryPending){p.warning=0;continue;}
                var point=TargetPoint(draft,Array.FindIndex(content.targets,t=>t.id==f.target));
                if(Distance(x,z,point.X,point.Z)>f.alertRadius){p.warning=0;continue;}
                if(p.warning>0)
                {
                    if(--p.warning==0)
                    {
                        p.positionIndex=1-p.positionIndex;p.prepared=false;
                        Say("The flock lifts and resettles at the other end of the open margin.");
                    }
                }
                else if(rushing || !p.prepared)
                {p.warning=f.warningTicks;p.prepared=false;Say("The sentinel's head rises. One warning honk. Withdraw into cover.");}
            }
        }
        void TickPresentations()
        {
            for(int i=0;i<content.presentationEvents.Length;i++)
            {
                var definition=content.presentationEvents[i];var p=draft.data.presentations[i];
                if(!p.seen && draft.flags.Contains(definition.triggerFlag)){p.seen=true;p.remaining=definition.ticks;}
                else if(p.remaining>0)p.remaining--;
            }
        }
        void ValidateOpportunitySave(GameplaySave save,HashSet<string> flags)
        {
            for(int i=0;i<save.flocks.Length;i++)
            {
                var p=save.flocks[i];var definition=content.flocks[i];
                GameplayContent.Need(p!=null && p.id==definition.id && (p.positionIndex==0 || p.positionIndex==1) && p.warning>=0 && p.warning<=definition.warningTicks && !(p.prepared && p.warning>0) && !(p.recoveryPending && p.warning>0),"save_flock");
                GameplayContent.Need((!p.prepared && !p.recoveryPending && p.warning==0 && p.positionIndex==0) || Meets(flags,definition.all,definition.none,Array.Empty<string>(),0),"save_flock_prerequisites");
            }
            for(int i=0;i<save.presentations.Length;i++)
            {
                var p=save.presentations[i];var definition=content.presentationEvents[i];
                GameplayContent.Need(p!=null && p.id==definition.id && p.remaining>=0 && p.remaining<=definition.ticks && p.seen==flags.Contains(definition.triggerFlag) && (p.seen || p.remaining==0),"save_presentation");
            }
        }
        bool EnemyWithinBoundary(EnemyDefinition enemy,float x,float z)
        {
            if(string.IsNullOrEmpty(enemy.boundaryTarget))return true;
            var target=content.targets.First(t=>t.id==enemy.boundaryTarget);
            return Distance(x,z,target.x,target.z)<=enemy.boundaryRadius;
        }
        bool TryInputs(State state,ActionDefinition action,out ItemAmount[] inputs)
        {
            var required=new Dictionary<string,long>(StringComparer.Ordinal);
            foreach(var amount in action.inputs)
            {
                required.TryGetValue(amount.id,out var count);count+=amount.count;
                if(count>int.MaxValue || count>Count(state,amount.id)){inputs=null;return false;}
                required[amount.id]=count;
            }
            foreach(var tag in action.tagInputs)
            {
                long remaining=tag.count;
                foreach(var item in content.items.Where(i=>i.tags.Contains(tag.tag)).OrderBy(i=>i.id,StringComparer.Ordinal))
                {
                    required.TryGetValue(item.id,out var reserved);long available=Count(state,item.id)-reserved;
                    long take=Math.Min(remaining,Math.Max(0,available));
                    if(take>0){required[item.id]=reserved+take;remaining-=take;}
                    if(remaining==0)break;
                }
                if(remaining>0){inputs=null;return false;}
            }
            inputs=required.Where(v=>v.Value>0).OrderBy(v=>v.Key,StringComparer.Ordinal).Select(v=>new ItemAmount(v.Key,(int)v.Value)).ToArray();return true;
        }
    }
}
