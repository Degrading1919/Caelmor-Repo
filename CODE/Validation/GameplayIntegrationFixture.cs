using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Caelmor.Runtime.Gameplay;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.Quests;

internal sealed class GameplayIntegrationFixture
{
    static readonly JsonSerializerOptions Json = new() { IncludeFields=true };
    readonly GameplayContent content;
    readonly string identity;
    GameplaySession session;
    long tick;
    float x,z;
    bool active=true;
    public GameplayIntegrationFixture()
    {
        var directory=new DirectoryInfo(AppContext.BaseDirectory);
        while(directory!=null && !File.Exists(Path.Combine(directory.FullName,"04_CONTENT_PRODUCTION","Quests","LowmarkGameplay.json"))) directory=directory.Parent;
        Check(directory!=null,"Locate production gameplay pack.");
        var raw=File.ReadAllText(Path.Combine(directory!.FullName,"04_CONTENT_PRODUCTION","Quests","LowmarkGameplay.json"));
        content=JsonSerializer.Deserialize<GameplayContent>(raw,Json)!;content.Validate();
        identity="lowmark_playable:"+Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(raw)));
        session=New();
    }
    GameplaySession New()=>new(content,identity,new PlayerHandle(1),()=>active);
    public void Boundaries()
    {
        var initial=session.Capture();var arrival=Index("arrive");x=0;z=-4;
        session.PrepareTick(++tick,x,z,new[]{new GameplayRequest(GameplayRequestKind.Action,arrival)},_=>true);
        Check(!session.Has("arrived") && session.Stage(0)==0,"Prepare is private.");
        Throws(()=>session.Capture(),"No checkpoint of a half-prepared frame.");
        session.AbortTick();Check(!session.Has("arrived"),"Abort discards quest flags.");
        Step();Check(session.Stage(0)==1,"Area entry starts quest.");
        Check(session.CoarseState(0)==QuestState.Active,"Existing quest runtime activated on commit.");
        Throws(()=>session.CommitTick(tick),"Duplicate commit rejected.");
        x=12;z=-12;Act("hear_order",false);Check(!session.Has("heard_order"),"Host rejects range spoofing.");
        Move("hollis");Step(new(GameplayRequestKind.Action,Index("hear_order")),false);Check(!session.Has("heard_order"),"Host rejects blocked LOS.");
        active=false;Throws(()=>Step(),"Suspended lifecycle cannot simulate activities.");active=true;session.AbortTick();
        Act("hear_order");Act("hear_river");Act("settle");
        Check(session.Stage(0)==2,"Dialogue requirements advance quest.");
        var copy=session.Capture();copy.flags=Array.Empty<string>();Check(session.Has("heard_both"),"Save DTO cannot mutate authoritative state.");
        Check(initial.items.Length==0,"Fresh inventory.");
    }
    public void FullQuest(bool optional,bool riverfolk=false)
    {
        x=0;z=-4;Step();Act("hear_order");Act("hear_river");Act("settle");
        if(optional){Act("nan_lead");Act("nan_alibi");Act("order_lead");Act("dace_lead");Act("tovin_start");Act("tovin_odd");Act("tovin_lead");}
        Act("notch");Act("earth");Act("drag");Act("post_found");
        Move("footing");Step();
        foreach(var id in new[]{"silt1","silt2","silt3","leech"})Fight(id);
        Act("clear");Act("hatchet");Act("stem");
        Check(session.Quantity("marker_stem")==1 && session.Capture().xp.Single(v=>v.id=="woodcutting").count==22,"Gather uses real inventory and action XP.");
        Act("notch_cut");Act("seat");
        Move("footing");for(int i=0;i<105;i++)Step();Act("maelin_after");
        Check(session.Stage(0)==7,"Discovery and repair advance, stem consumed.");
        Check(session.Quantity("marker_stem")==0,"Seat consumes exactly one stem.");
        Act("proof_notches");Act(optional?"proof_order":"proof_walk");Act("close_crossing");
        if(optional){Check(session.Quantity("dispatch_order")==1,"D7 conditionally transfers optional order in the same atomic action.");Act("order_transfer");}
        for(int i=1;i<=3;i++){Act("lift"+i);Check(session.Carry=="sack"+i,"Transient carry set.");Act("deliver"+i);}
        Act("trunk_lift");Act("trunk_set");Fight("boar");Act("uphill_done");
        Act(riverfolk?"TL_EVIDENCE_RIVERFOLK":optional?"TL_EVIDENCE_KEEPERS":"TL_EVIDENCE_PLAYER");
        Check(!session.Available(Index("TL_EVIDENCE_RIVERFOLK")),"Alternate evidence choice cannot execute twice.");
        Act(optional?"TL_STONE_PUBLIC":"TL_STONE_KEPT");Act("quest_finish");
        Check(session.CoarseState(0)==QuestState.Completed && session.Stage(0)==11,"Full quest mirrors existing coarse completed lifecycle.");
        Check(session.Quantity("payment")==8,"One payment, no lump quest XP.");
        Check(session.Quantity("weathered_marker_post")== (optional?0:1),"Evidence transfer respects player choice.");
        Check(session.Quantity("dispatch_order")==0,"Optional order transferred with evidence.");
        Check(!session.Available(Index("quest_finish")),"Completed dialogue/reward cannot repeat.");
        if(optional)Act("tovin_trust");Act("ansel_hook");Act("marker_read");
        RepeatableLoop();
    }
    void RepeatableLoop()
    {
        Act("timber_cut");Fight("wild_boar");Act("wild_boar_harvest");
        Check(session.Quantity("game_meat")==1,"One harvest per corpse.");
        Check(!session.Available(Index("wild_boar_harvest")),"Corpse cannot produce infinite meat.");
        Act("cook_meat");Check(session.Quantity("dried_game_strips")==1 && session.Quantity("game_meat")==0 && session.Quantity("common_timber")==0,"Craft atomically spends meat and fuel.");
        int original=session.Quantity("dried_game_strips");
        // Stand in a live boar tell, then eat from anywhere through a numeric command.
        Move("wild_boar");for(int i=0;i<335;i++)Step();
        for(int i=0;i<17;i++)Step();
        Check(session.Health<content.tuning.health,"Authoritative enemy windup damages player.");
        int before=session.Health;
        Step(new(GameplayRequestKind.Consume,Array.FindIndex(content.items,i=>i.id=="dried_game_strips")));
        Check(session.Health>before && session.Quantity("dried_game_strips")==original-1,"Food heals and consumes once.");
        Check(session.Capture().xp.Single(v=>v.id=="cooking").count==28,"Fixed base cooking XP.");
        var save=session.Capture();var clone=JsonSerializer.Deserialize<GameplaySave>(JsonSerializer.Serialize(save,Json),Json)!;
        var restored=New();restored.Restore(clone);Check(restored.Stage(0)==11 && restored.Quantity("payment")==8 && restored.CoarseState(0)==QuestState.Completed,"Complete durable DTO rehydrates quest and inventory.");
        Throws(()=>restored.Restore(New().Capture()),"Second hydration cannot desynchronize coarse and objective state.");
        var corrupt=JsonSerializer.Deserialize<GameplaySave>(JsonSerializer.Serialize(save,Json),Json)!;corrupt.flags=corrupt.flags.Concat(new[]{session.Has("TL_STONE_PUBLIC")?"TL_STONE_KEPT":"TL_STONE_PUBLIC"}).ToArray();
        var untouched=New();Throws(()=>untouched.Restore(corrupt),"Conflicting choices rejected.");Check(untouched.Stage(0)==0,"Bad restore leaves live state unchanged.");
        corrupt=JsonSerializer.Deserialize<GameplaySave>(JsonSerializer.Serialize(save,Json),Json)!;corrupt.items=new[]{new ItemAmount("payment",-1)};
        Throws(()=>New().Restore(corrupt),"Negative inventory rejected.");
        corrupt.contentId="wrong";Throws(()=>New().Restore(corrupt),"Content mismatch rejected.");
        var path=Path.Combine(Path.GetTempPath(),"Caelmor-gameplay-check-"+Guid.NewGuid().ToString("N"),"checkpoint.json");
        var disk=new AtomicTextCheckpoint(path);var text=JsonSerializer.Serialize(save,Json);
        void Validate(string raw)=>restored.ValidateSave(JsonSerializer.Deserialize<GameplaySave>(raw,Json)!);
        disk.Write(text,Validate);disk.Write(text,Validate);Check(disk.Read(Validate)==text && File.Exists(path+".previous"),"Actual atomic disk checkpoint and previous backup.");
        Throws(()=>disk.Write("{}",Validate),"Invalid write rejected before publication.");Check(disk.Read(Validate)==text,"Failed checkpoint preserves previous file.");
    }
    public void Interruptions()
    {
        FullQuest(false);
        // Reusable gather channels validate origin and do not spend/award on interruption.
        Move("timber");while(!session.Available(Index("timber_cut")))Step();
        int before=session.Quantity("common_timber");Step(new(GameplayRequestKind.Action,Index("timber_cut")));Check(session.ChannelAction>=0,"Gather channel started.");
        x+=1;Step();Check(session.ChannelAction<0 && session.Quantity("common_timber")==before,"Moving interrupts gathering without free reward.");
        var initial=New();var invalid=initial.Capture();invalid.enemies[0].health=int.MaxValue;Throws(()=>initial.Restore(invalid),"Enemy restore bounds enforced.");
    }
    public void CarryRecovery()
    {
        x=0;z=-4;Step();Act("hear_order");Act("hear_river");Act("settle");Act("notch");Act("earth");Act("drag");Act("post_found");Move("footing");Step();
        foreach(var id in new[]{"silt1","silt2","silt3","leech"})Fight(id);
        Act("clear");Act("hatchet");Act("stem");Act("notch_cut");Act("seat");Move("footing");for(int i=0;i<105;i++)Step();Act("maelin_after");Act("proof_notches");Act("proof_walk");Act("close_crossing");Act("lift1");
        var save=session.Capture();session=New();session.Restore(save);tick=0;
        Check(session.Carry=="" && session.Available(Index("lift1")),"Interrupted carry can be collected after reload.");Act("lift1");Act("deliver1");Check(session.Has("sack1_done"),"Recovered carry still advances.");
        Act("lift2");session.ClearTransient();Check(session.Carry=="sack2","Input cancellation preserves a carried load.");Act("deliver2");
    }
    public void BankWalk(string choice)
    {
        Check(!session.Available(Index("BW_start")) && session.CoarseState(1)==QuestState.Inactive,"Follow-on activity is gated by prerequisite, no quest-specific runtime code.");
        FullQuest(false);
        Check(session.QuestAvailable(1),"Completed crossing exposes next authored activity.");
        Act("BW_start");Act("BW_measure1");Act("BW_measure2");Act("BW_measure3");Act("BW_wrack");
        Move("bw_jam");Step();for(int i=1;i<=5;i++)Fight("BW_skitter"+i);
        Act("BW_cut_jam");int before=session.Health;float push=0;
        for(int i=0;i<18;i++){Step();push+=Math.Abs(session.PendingPushX)+Math.Abs(session.PendingPushZ);}
        Check(session.Has("BW_JAM_SWUNG") && session.Health<before && push>0,"Generic timed jam hazard damages and requests bounded host push.");
        Act("BW_cord");Act("BW_repair");Act("BW_leaner_read");Act("BW_holder_read");Act("BW_old_read");Act("BW_leaner_notch");Act("BW_leaner_back");
        x+=2.5f;for(int i=0;i<23;i++)Step();
        Check(session.Has("BW_LEANER_FALLEN") && session.Stage(1)==4,"Felling changes the bank state and advances the independent quest.");
        Act("BW_"+choice);
        if(choice=="cut"){Act("BW_holder_notch");Act("BW_holder_back");}
        if(choice=="build"){Act("BW_give_wood");Act("BW_stage1");Act("BW_stage2");}
        Act("BW_finish");Check(session.Stage(1)==6 && session.CoarseState(1)==QuestState.Completed && session.Quantity("payment")==12,"Second quest completes with independent reward.");
        Check(!session.Available(Index("BW_finish")),"Second reward cannot replay.");
        var save=session.Capture();var restored=New();restored.Restore(save);Check(restored.Stage(1)==6,"Second quest choices and hazards survive hydration.");
        save.hazards[0].remaining=1;Throws(()=>New().Restore(save),"A resolved hazard cannot restore a permanent active tell.");
    }
    public void FloodKitchen(string choice,bool crates)
    {
        FullQuest(false);StartKitchen(crates);
        // Reading is a prompt rather than a mandatory hunt unlock.
        Check(!session.Has("FK_traces_read") && !session.Has("FK_sentinel_read"),"Reading remains optional.");
        RecoverFowl("FK_recover1");RecoverFowl("FK_recover2");
        Check(session.Quantity("raw_fowl")==2 && session.Stage(2)==3,"Two recoveries, not kills, advance the Hunting objective.");
        Act("FK_cook_batch");Check(session.Quantity("fowl_stew")==4 && session.Quantity("raw_fowl")==0,"Nan's once-only batch yields four shelter portions.");
        int hush=Array.FindIndex(content.presentationEvents,p=>p.triggerFlag=="FK_HUSH_SEEN");
        Check(session.Presentation(hush).seen && session.Presentation(hush).remaining>0,"First Cooking completion starts one committed hush.");
        var save=session.Capture();var restored=New();restored.Restore(save);
        Check(restored.Presentation(hush).seen && restored.Presentation(hush).remaining==0,"Hydration retains the raised waterline without replaying the hush.");
        for(int i=1;i<=4;i++)Act("FK_feed"+i);
        Check(session.Quantity("fowl_stew")==0 && session.Stage(2)==5,"Four unique household receipts consume exactly four tagged portions.");
        Check(!session.Available(Index("FK_own")),"Own-food choice is unavailable without cooked food.");
        if(choice=="own")
        {
            Act("timber_cut");Fight("wild_boar");Act("wild_boar_harvest");Act("cook_meat");
            Check(session.Quantity("dried_game_strips")==1,"Alternative cooked item prepared by pre-existing economy loop.");
        }
        Act("FK_"+choice);
        Check(!session.Available(Index("FK_crew")) && !session.Available(Index("FK_family")) && !session.Available(Index("FK_own")),"Last-pot choice is exclusive.");
        if(choice=="own")Check(session.Quantity("dried_game_strips")==0,"Any-cooked-food input accepts and consumes an unrelated cooked item.");
        Act("FK_tune");Act("FK_finish_"+choice);
        Check(session.Stage(2)==7 && session.CoarseState(2)==QuestState.Completed && session.Quantity("payment")==12 && session.Quantity("fowl_stew")==1,"Kitchen completes, pays once and gives Nan's bowl.");
        Check(!session.Available(Index("FK_finish_"+choice)),"Completion reward cannot repeat.");
        RecoverFowl("FK_recover_repeat");Act("timber_cut");Act("FK_cook_repeat");
        Check(session.Quantity("fowl_stew")==3 && session.Presentation(hush).seen,"Public station remains useful after the quest without replaying first-cook wonder.");
        save=session.Capture();restored=New();restored.Restore(save);Check(restored.Stage(2)==7 && restored.Quantity("fowl_stew")==3,"Completed kitchen and repeatable inventory survive restore.");
    }
    void StartKitchen(bool crates)
    {
        Move("fk_shelter");Step();Act("FK_start");
        if(crates)
        {
            Act("FK_lift1");var save=session.Capture();session=New();session.Restore(save);tick=0;
            Check(session.Carry=="" && session.Available(Index("FK_lift1")),"Dry-slat carry can be recollected after disconnect.");
            Act("FK_lift1");Act("FK_deposit1");Act("FK_lift2");Act("FK_deposit2");
        }
        else {Act("timber_cut");while(!session.Available(Index("timber_cut")))Step();Act("timber_cut");Act("FK_wood");}
        Act("FK_light_fire");Check(session.Stage(2)==2 && session.Has("FK_fire_lit"),"Either fuel route activates shelter Cooking.");
    }
    void RecoverFowl(string action)
    {
        Act("FK_prepare");int ti=Array.FindIndex(content.targets,t=>t.id==content.flocks[0].target);var point=session.CurrentTargetPosition(ti);
        x=point.X;z=point.Z;Step(new(GameplayRequestKind.Action,Index("FK_resolve")));
        Check(session.Flock(0).recoveryPending,"Non-combat resolution creates a recoverable bird.");
        Act(action);Check(!session.Flock(0).recoveryPending && !session.Flock(0).prepared,"Recovery consumes one corpse and preparation.");
    }
    public void FlockAuthorityAndRecovery()
    {
        FullQuest(false);StartKitchen(true);
        var definition=content.flocks[0];int sentinel=Array.FindIndex(content.targets,t=>t.id==definition.target);var point=session.CurrentTargetPosition(sentinel);
        x=point.X;z=point.Z;Step();Check(session.Flock(0).warning==15,"Unprepared approach warns before scatter.");
        int firstPosition=session.Flock(0).positionIndex;for(int i=0;i<15;i++)Step();
        Check(session.Flock(0).positionIndex!=firstPosition && session.Flock(0).warning==0,"Warning expires and relocates without a wait timer.");
        Act("FK_prepare");point=session.CurrentTargetPosition(sentinel);x=point.X;z=point.Z;
        Step(new(GameplayRequestKind.Action,Index("FK_resolve")),true,true);
        Check(!session.Flock(0).prepared && !session.Flock(0).recoveryPending && session.Flock(0).warning>0,"Rushing invalidates preparation before a take can resolve.");
        int warning=session.Flock(0).warning;Step();Check(session.Flock(0).warning==warning-1,"Stopping does not reset the running warning.");
        Move(definition.coverTarget);Step();Check(session.Flock(0).warning==0,"Withdrawal into cover cancels warning.");
        Act("FK_prepare");point=session.CurrentTargetPosition(sentinel);x=point.X;z=point.Z;
        int items=session.Quantity("raw_fowl"),xp=session.Capture().xp.Single(v=>v.id=="hunting").count;
        Step(new(GameplayRequestKind.Action,Index("FK_resolve")));
        Check(session.Flock(0).recoveryPending && session.Quantity("raw_fowl")==items && session.Capture().xp.Single(v=>v.id=="hunting").count==xp,"Take grants neither item nor XP.");
        Check(!session.TargetVisible(sentinel),"Live sentinel is hidden while a recovery is pending.");
        Step(new(GameplayRequestKind.Action,Index("FK_sentinel")));Check(!session.Has("FK_sentinel_read"),"Stale numeric interaction cannot inspect a hidden sentinel.");
        for(int i=0;i<20;i++)Step(null,true,true);
        Check(session.Flock(0).warning==0,"Pending recovery cannot create a hidden warning/scatter cycle.");
        var save=session.Capture();session=New();session.Restore(save);tick=0;
        Check(session.Flock(0).recoveryPending && !session.Available(Index("FK_resolve")),"Pending corpse survives reload and blocks a second take.");
        Act("FK_recover1");Check(session.Quantity("raw_fowl")==items+1 && session.Capture().xp.Single(v=>v.id=="hunting").count==xp+28,"Recovery grants one fowl and fixed action XP.");
        Check(!session.Available(Index("FK_recover2")),"A different recovery action cannot reuse the same consumed corpse.");
        Move(definition.closedTarget);Step();int goose=Array.FindIndex(content.enemies,e=>!string.IsNullOrEmpty(e.boundaryTarget));var enemy=content.enemies[goose];var t=content.targets.Single(v=>v.id==enemy.target);var center=content.targets.Single(v=>v.id==enemy.boundaryTarget);
        float dx=t.x-center.x,dz=t.z-center.z;float length=MathF.Sqrt(dx*dx+dz*dz);if(length<.001f){dx=1;dz=0;length=1;}
        x=center.x+dx/length*(enemy.boundaryRadius+.05f);z=center.z+dz/length*(enemy.boundaryRadius+.05f);
        int hp=session.Enemy(goose).health;Step(new(GameplayRequestKind.Attack,goose));for(int i=0;i<30;i++)Step();
        Check(session.Enemy(goose).health==hp && session.Enemy(goose).windup==0,"Outside closure boundary neither side can exploit one-way melee.");
        // Select the authored far endpoint, whose take range overlaps the nesting boundary.
        if(session.Flock(0).positionIndex==0)
        {
            point=session.CurrentTargetPosition(sentinel);x=point.X;z=point.Z;Step();for(int n=0;n<15;n++)Step();
        }
        Act("FK_prepare");point=session.CurrentTargetPosition(sentinel);var closed=content.targets.Single(t=>t.id==definition.closedTarget);
        x=(point.X+closed.x)/2;z=(point.Z+closed.z)/2;
        Check(MathF.Sqrt((x-point.X)*(x-point.X)+(z-point.Z)*(z-point.Z))<2.3f && MathF.Sqrt((x-closed.x)*(x-closed.x)+(z-closed.z)*(z-closed.z))<definition.closedRadius,"Closed-ground regression is within otherwise valid take reach.");
        Step(new(GameplayRequestKind.Action,Index("FK_resolve")));
        Check(!session.Flock(0).recoveryPending,"Closed nesting ground cannot produce fowl.");
        save=session.Capture();save.flocks[0].warning=1;save.flocks[0].prepared=true;Throws(()=>New().Restore(save),"Impossible prepared-warning saves are rejected.");
    }
    public void KitchenFailureRecovery()
    {
        FullQuest(false);StartKitchen(true);RecoverFowl("FK_recover1");RecoverFowl("FK_recover2");
        int before=session.Quantity("raw_fowl"),xp=session.Capture().xp.Single(v=>v.id=="cooking").count;
        Act("FK_cook_repeat");Check(session.Quantity("raw_fowl")==before && session.Capture().xp.Single(v=>v.id=="cooking").count==xp && !session.Has("FK_HUSH_SEEN"),"Missing fuel craft consumes nothing and emits no XP/hush.");
        Act("FK_cook_batch");
        // Model an already-consumed ordinary inventory snapshot without changing quest progress.
        var save=session.Capture();save.items=save.items.Where(v=>v.id!="fowl_stew").ToArray();session=New();session.Restore(save);tick=0;
        Check(!session.Available(Index("FK_feed1")),"No tagged food cannot feed a household.");
        for(int n=0;n<2;n++){RecoverFowl("FK_recover_repeat");Act("timber_cut");Act("FK_cook_repeat");}
        for(int i=1;i<=4;i++)Act("FK_feed"+i);
        Check(session.Stage(2)==5,"Repeatable hunt/cook replenishes an active quest after its batch was spent.");
    }
    public void KitchenProductionCounters()
    {
        FullQuest(false);StartKitchen(true);RecoverFowl("FK_recover1");RecoverFowl("FK_recover2");
        const string counter="fk_portions_cooked";
        Check(session.Counter(counter)==0 && session.Counter("unknown")==0,"Production totals begin at zero.");
        int xp=session.Capture().xp.Single(v=>v.id=="cooking").count;Act("FK_cook_repeat");
        Check(session.Counter(counter)==0 && session.Quantity("raw_fowl")==2 && session.Capture().xp.Single(v=>v.id=="cooking").count==xp,"Rejected craft cannot advance production or spend ingredients.");
        Act("timber_cut");while(!session.Available(Index("timber_cut")))Step();Act("timber_cut");
        Act("FK_cook_repeat");
        Check(session.Counter(counter)==2 && session.Stage(2)==3 && !session.Has("FK_meal_cooked"),"First public recipe records two portions without the batch receipt.");
        var save=session.Capture();session=New();session.Restore(save);tick=0;
        Check(session.Counter(counter)==2 && session.Stage(2)==3,"Partial production total survives checkpoint hydration.");
        Act("FK_cook_repeat");
        Check(session.Counter(counter)==4 && session.Stage(2)==4 && session.Quantity("fowl_stew")==4 && !session.Has("FK_meal_cooked"),"Two public cooks satisfy generic stage production requirements.");
        RecoverFowl("FK_recover_repeat");Act("timber_cut");save=session.Capture();
        save.counters.Single(c=>c.id==counter).count=int.MaxValue;session=New();session.Restore(save);tick=0;
        int raw=session.Quantity("raw_fowl"),wood=session.Quantity("common_timber");xp=session.Capture().xp.Single(v=>v.id=="cooking").count;
        Act("FK_cook_repeat");
        Check(session.Counter(counter)==int.MaxValue && session.Quantity("raw_fowl")==raw && session.Quantity("common_timber")==wood && session.Capture().xp.Single(v=>v.id=="cooking").count==xp,"Counter overflow rejects the entire action before inventory mutation.");
        save=session.Capture();save.counters[0].id="unknown_counter";Throws(()=>New().Restore(save),"Unknown saved production keys are rejected.");
        var stage=content.quests[2].stages[3];var requirements=stage.counterRequirements;
        try {stage.counterRequirements=new[]{new CounterRequirement{id="no_producer",min=1}};Throws(()=>content.Validate(),"Unproducible requirements fail content validation.");}
        finally {stage.counterRequirements=requirements;}
    }
    public void TaggedInputAtomicity()
    {
        FullQuest(false);
        void CookExistingFood()
        {
            Move("timber");while(!session.Available(Index("timber_cut")))Step();Act("timber_cut");
            int wild=Array.FindIndex(content.enemies,e=>e.id=="wild_boar");while(session.Enemy(wild).health==0)Step();
            Fight("wild_boar");Act("wild_boar_harvest");Act("cook_meat");
        }
        CookExistingFood();
        var recipe=content.actions[Index("cook_meat")];var originalInputs=recipe.inputs;var originalOutputs=recipe.outputs;int originalTicks=recipe.ticks;
        try
        {
            // Valid temporary policy uses the confirmed generic contract, not new production data.
            recipe.inputs=new[]{new ItemAmount("dried_game_strips",1)};recipe.tagInputs=new[]{new TagAmount{tag="cooked_food",count=1}};
            recipe.outputs=new[]{new ItemAmount("fowl_stew",1)};recipe.ticks=0;content.Validate();
            int xp=session.Capture().xp.Single(v=>v.id=="cooking").count;Act("cook_meat");
            Check(session.Quantity("dried_game_strips")==1 && session.Quantity("fowl_stew")==0 && session.Capture().xp.Single(v=>v.id=="cooking").count==xp,"Explicit and tagged inputs cannot reserve the same single item.");
            recipe.inputs=originalInputs;recipe.outputs=originalOutputs;recipe.tagInputs=Array.Empty<TagAmount>();recipe.ticks=originalTicks;CookExistingFood();
            recipe.inputs=new[]{new ItemAmount("dried_game_strips",1)};recipe.outputs=new[]{new ItemAmount("fowl_stew",1)};recipe.ticks=0;
            recipe.tagInputs=new[]{new TagAmount{tag="cooked_food",count=1},new TagAmount{tag="cooked_food",count=1}};content.Validate();
            Act("cook_meat");Check(session.Quantity("dried_game_strips")==2 && session.Quantity("fowl_stew")==0,"Overlapping tag requirements preserve all inputs on failure.");
            recipe.tagInputs=new[]{new TagAmount{tag="cooked_food",count=1}};content.Validate();Act("cook_meat");
            Check(session.Quantity("dried_game_strips")==0 && session.Quantity("fowl_stew")==1,"Existing craft executor consumes concrete fixed/tag inputs in one transaction.");
        }
        finally{recipe.inputs=originalInputs;recipe.outputs=originalOutputs;recipe.tagInputs=Array.Empty<TagAmount>();recipe.ticks=originalTicks;}
    }
    void Fight(string id)
    {
        int index=Array.FindIndex(content.enemies,e=>e.id==id);var target=content.targets.Single(t=>t.id==content.enemies[index].target);
        float side=target.x>10?-1:1;float origin=target.x+side*1.55f;
        x=origin;z=target.z;
        // The former 1.8–2.3 m safe annulus must not deal player damage.
        if(id=="boar")
        {
            x=target.x+side*2.15f;int hp=session.Enemy(index).health;
            Step(new(GameplayRequestKind.Attack,index));for(int i=0;i<25;i++)Step();
            Check(session.Enemy(index).health==hp,"Out-of-reach attacks cannot exploit anchored enemies.");x=origin;
        }
        int before=session.Health;bool damaged=false,dodged=false;
        Step(new(GameplayRequestKind.Attack,index));
        for(int i=0;i<1500 && session.Enemy(index).health>0;i++)
        {
            if(session.Health<before)damaged=true;
            var enemy=session.Enemy(index);
            if(enemy.windup>0 && (id!="boar" || damaged))
            {
                int health=session.Health;x=origin+side*1.05f;
                while(session.Enemy(index).windup>0)Step();
                if(id=="boar" && !dodged)
                {
                    Check(session.Health==health,"Moving off the boar's committed tell dodges damage.");
                    Check(session.Enemy(index).cooldown>=20,"Missed boar strike exposes a recovery window.");dodged=true;
                }
                x=origin;
            }
            Step();
        }
        if(id=="boar")Check(damaged && dodged,"Required boar fight executes a real hit and an intentional dodge.");
        Check(session.Enemy(index).health==0,"Enemy defeated: "+id);
    }
    void Move(string id){var t=content.targets.Single(t=>t.id==id);x=t.x;z=t.z;}
    void Act(string id,bool move=true)
    {
        int i=Index(id);if(move)Move(content.actions[i].target);
        Step(new(GameplayRequestKind.Action,i));
        for(int n=0;n<1000 && session.ChannelAction>=0;n++)Step();
    }
    int Index(string id)=>Array.FindIndex(content.actions,a=>a.id==id);
    void Step(GameplayRequest? request=null,bool sight=true,bool rushing=false)
    {
        session.PrepareTick(++tick,x,z,request.HasValue?new[]{request.Value}:Array.Empty<GameplayRequest>(),_=>sight,rushing);
        session.CommitTick(tick);
    }
    static void Check(bool ok,string message){if(!ok)throw new Exception(message);}
    static void Throws(Action action,string message){try{action();}catch(InvalidOperationException){return;}throw new Exception(message);}
}
