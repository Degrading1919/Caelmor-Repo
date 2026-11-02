#nullable disable
using System;
using Caelmor.Combat;
using Caelmor.Runtime.Tick;

namespace Caelmor.Runtime.Gameplay
{
    /// <summary>Uses existing combat state legality and resolution. The existing core produces
    /// proposals and explicitly owns no HP; GameplaySession supplies the bounded melee HP sink.
    /// Derived engagement is local to the private tick draft and cannot survive an aborted tick.</summary>
    internal static class GameplayCombatAdapter
    {
        public static bool ResolveAttack(long tick,int actor,int target)
        {
            var context=new Context(checked((int)tick));
            var state=new CombatStateAuthoritySystem(context,context,context);
            var entity=new EntityHandle(actor);
            state.EstablishCombatContext(entity,"lowmark-melee");
            var intent=new FrozenIntentRecord("melee-"+tick+"-"+actor+"-"+target,CombatIntentType.CombatAttackIntent,entity,context.CurrentTick,1,
                CombatIntentPayload.ForAttack(new AttackIntentPayload(new OptionalEntityHandle(new EntityHandle(target)),default)));
            var batch=state.GateFrozenQueue(new FrozenIntentBatch(context.CurrentTick,new[]{intent},1));
            CombatResolutionResult result=null;
            try
            {
                result=new CombatResolutionEngine().Resolve(batch);
                return result.OutcomesInOrder.Count==1 && result.OutcomesInOrder[0].OutcomeKind==CombatOutcomeKind.AttackProposed;
            }
            finally {result?.Release();batch.Release();}
        }
        sealed class Context : ITickSource,IEntityIdValidator,IIntentGateRejectionSink
        {
            public int CurrentTick{get;}
            public Context(int tick){CurrentTick=tick;}
            public event Action<int> OnTickAdvanced {add{} remove{}}
            public bool IsValidEntityId(string id)=>!string.IsNullOrWhiteSpace(id);
            public bool IsValidInteractableId(string id)=>!string.IsNullOrWhiteSpace(id);
            public void OnRejected(IntentGateRejection rejection){}
        }
    }
}
