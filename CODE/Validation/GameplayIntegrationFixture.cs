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
    void Step(GameplayRequest? request=null,bool sight=true)
    {
        session.PrepareTick(++tick,x,z,request.HasValue?new[]{request.Value}:Array.Empty<GameplayRequest>(),_=>sight);
        session.CommitTick(tick);
    }
    static void Check(bool ok,string message){if(!ok)throw new Exception(message);}
    static void Throws(Action action,string message){try{action();}catch(InvalidOperationException){return;}throw new Exception(message);}
}
