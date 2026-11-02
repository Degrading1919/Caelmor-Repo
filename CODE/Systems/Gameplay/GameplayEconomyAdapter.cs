#nullable disable
using System;
using System.Collections.Generic;
using System.Linq;
using Caelmor.Economy.Crafting;
using Caelmor.Economy.Gathering;
using Caelmor.Economy.Inventory;

namespace Caelmor.Runtime.Gameplay
{
    /// <summary>
    /// Composes the existing Stage 8 gather resolver and craft executor against the
    /// private gameplay draft. Caller has already validated action conditions, reach,
    /// line of sight, lifecycle, channel completion and corpse/node availability.
    /// No events escape this adapter before GameplaySession finalizes the draft.
    /// </summary>
    internal static class GameplayEconomyAdapter
    {
        const int LocalPlayer = 1;

        public static bool TryCraft(ActionDefinition action, GameplayContent content,
            SimplePlayerInventoryStore inventory, IReadOnlyList<ItemAmount> outputs, bool stationUsable, out string failureReason,IReadOnlyList<ItemAmount> inputs=null)
        {
            failureReason=null;
            if(!IsDefined(action,content,"craft") || inventory==null || outputs==null)
            { failureReason="invalid_craft_projection";return false; }
            var context=new CraftContext(action,content,inputs??action.inputs,outputs,stationUsable);
            var executor=new CraftingExecutionSystem(inventory,context,context,context,context,context,context);
            var result=executor.ExecuteCraft(new CraftingRequest(LocalPlayer,action.id,action.target));
            failureReason=result.FailureReason;
            return result.Success;
        }

        // nodeInstanceId must be supplied by authored placement data. An action index
        // is deliberately not converted into a ResourceNodeRuntimeSystem identifier.
        public static bool TryGather(ActionDefinition action, GameplayContent content,
            SimplePlayerInventoryStore inventory, int nodeInstanceId, bool available, out string failureReason)
        {
            failureReason=null;
            if(!IsDefined(action,content,"gather") || inventory==null || nodeInstanceId<=0)
            { failureReason="invalid_gather_projection";return false; }
            var context=new GatherContext(action,content,nodeInstanceId,available);
            var resolver=new GatheringResolutionSystem(context,context,context);
            var tool=string.IsNullOrEmpty(action.tool)?null:inventory.DebugEnumerate(LocalPlayer).FirstOrDefault(v=>v.Key==action.tool).Value>0?action.tool:null;
            var result=resolver.ResolveAttempt(LocalPlayer,nodeInstanceId,action.skill,new ToolContext(true,tool));
            failureReason=result.FailureReason;
            return result.Outcome==GatheringOutcome.Success && result.ResourceGrantAllowed;
        }

        static bool IsDefined(ActionDefinition action,GameplayContent content,string kind)=>
            action!=null && content!=null && action.kind==kind && content.actions.Any(a=>ReferenceEquals(a,action)) && content.targets.Any(t=>t.id==action.target);

        sealed class CraftContext : IRecipeDefinition,IRecipeRepository,IPlayerRecipeKnowledge,
            ICraftingStationContext,IPlayerSkillFlags,ICraftingExecutionEventSink,Caelmor.Economy.Crafting.IServerDiagnosticsSink
        {
            readonly ActionDefinition action;
            readonly GameplayContent content;
            readonly bool stationUsable;
            public CraftContext(ActionDefinition action,GameplayContent content,IReadOnlyList<ItemAmount> inputs,IReadOnlyList<ItemAmount> outputs,bool stationUsable)
            {
                this.action=action;this.content=content;this.stationUsable=stationUsable;
                Inputs=inputs.Select(v=>new CraftItemDelta(v.id,v.count)).ToArray();
                Outputs=outputs.Select(v=>new CraftItemDelta(v.id,v.count)).ToArray();
            }
            public string RecipeKey=>action.id;
            public string RequiredCraftingStationKey=>action.target;
            public string RequiredSkillFlagKey=>action.skill;
            public IReadOnlyList<CraftItemDelta> Inputs{get;}
            public IReadOnlyList<CraftItemDelta> Outputs{get;}
            public bool TryGetRecipe(string key,out IRecipeDefinition recipe){recipe=key==action.id?this:null;return recipe!=null;}
            // The projection's action requirements are the recipe unlock contract.
            // The caller evaluated them against this draft immediately before entry.
            public bool PlayerKnowsRecipe(int player,string key)=>player==LocalPlayer && key==action.id;
            public bool PlayerHasSkillFlag(int player,string skill)=>player==LocalPlayer && content.skills.Any(s=>s.id==skill);
            public bool IsStationUsable(int player,string key,out string failure)
            {
                bool ok=stationUsable && player==LocalPlayer && key==action.target && content.targets.Any(t=>t.id==key);
                failure=ok?null:"station_not_defined";return ok;
            }
            // Execution results are returned synchronously to the private draft owner.
            // They are not forwarded into persistence/UI/network event sinks here.
            public void Emit(CraftingExecutionResult result){}
            public void Emit(string code,string message){}
        }

        sealed class GatherContext : IGatheringNodeQuery,IPlayerGatheringSkillProvider,IGatheringToolPolicyProvider
        {
            readonly ActionDefinition action;readonly GameplayContent content;readonly int placementId;readonly bool available;
            public GatherContext(ActionDefinition action,GameplayContent content,int placementId,bool available)
            {this.action=action;this.content=content;this.placementId=placementId;this.available=available;}
            public bool TryGetNodeContext(int id,out string type,out NodeAvailability state,out IReadOnlyList<string> skills,out IReadOnlyList<string> risk)
            {
                type=action.target;state=available?NodeAvailability.Available:NodeAvailability.Depleted;
                skills=new[]{action.skill};risk=Array.Empty<string>();return id==placementId;
            }
            public bool PlayerHasGatheringSkill(int player,string skill)=>player==LocalPlayer && skill==action.skill && content.skills.Any(s=>s.id==skill);
            public ToolPolicy GetToolPolicy(string type,string skill)=>string.IsNullOrEmpty(action.tool)?ToolPolicy.NotApplicable:new ToolPolicy(ToolPolicyKind.Required,action.tool);
        }
    }
}
