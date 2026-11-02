#nullable disable
using System;
using System.Collections.Generic;
using System.Linq;

namespace Caelmor.Runtime.Gameplay
{
    public sealed partial class GameplaySession
    {
        public const string LegacyTwoQuestIdentity="lowmark_playable:68FAD7F482236FDFC06D924139719BA26F79C965F0B98FDE5767F94DF8FD135E";
        public const string LegacyThreeQuestIdentity="lowmark_playable:ACA90A4C0BF8961028EA5AACC7C812BCB7B7FABC8D7243BB5EF163E3DBF273AD";
        static readonly string[] TwoItems = "weathered_marker_post|dispatch_order|marker_stem|crew_hatchet|common_timber|game_meat|dried_game_strips|payment|tannin_rich_bark".Split('|');
        static readonly string[] TwoSkills = "woodcutting|hunting|cooking|melee".Split('|');
        static readonly string[] TwoActions = "arrive|hear_order|hear_river|settle|nan_lead|nan_alibi|dace_lead|order_lead|tovin_start|tovin_odd|tovin_lead|notch|earth|drag|post_found|shallows|clear|hatchet|stem|notch_cut|seat|discovery_end|maelin_after|proof_notches|proof_walk|proof_nan|proof_order|proof_tovin|proof_pier|close_crossing|order_transfer|lift1|deliver1|lift2|deliver2|lift3|deliver3|trunk_lift|trunk_set|uphill_done|TL_EVIDENCE_KEEPERS|TL_EVIDENCE_RIVERFOLK|TL_EVIDENCE_PLAYER|TL_STONE_PUBLIC|TL_STONE_KEPT|quest_finish|ansel_hook|tovin_trust|marker_read|timber_cut|cook_meat|feed_camp|boar_harvest|wild_boar_harvest|eat_food|wreck_enter|wreck_inspect|stone_dry|stone_sketch|true_marker_read|epilogue_keepers|epilogue_riverfolk|epilogue_player|maelin_who|maelin_across|hollis_keepers|hollis_riverfolk|hollis_player|nan_tune|dace_fed|dace_unfed|wynn_camp_line|BW_start|BW_axe|BW_measure1|BW_grip|BW_measure2|BW_measure3|BW_wrack|BW_repair|BW_wade|BW_cut_jam|BW_cord|BW_leaner_read|BW_holder_read|BW_old_read|BW_leaner_notch|BW_leaner_back|BW_keep|BW_cut|BW_build|BW_holder_notch|BW_holder_back|BW_spare_limbs|BW_give_wood|BW_stage1|BW_stage2|BW_finish|BW_kept_bark|BW_built_bark|BW_tamsin_bark".Split('|');
        static readonly string[] TwoQuests = "lowmark.main.01_true_line|lowmark.side.bank_walk".Split('|');
        static readonly string[] TwoEnemies = "silt1|silt2|silt3|leech|goose1|goose2|boar|wild_boar|wreck1|wreck2|wreck3|BW_skitter1|BW_skitter2|BW_skitter3|BW_skitter4|BW_skitter5".Split('|');
        static readonly string[] TwoHazards = "BW_jam_swing|BW_leaner_fall".Split('|');
        static readonly string[] TwoFlags = "ansel_hook|arrive|arrived|boar_dead|BW_axe|BW_BANK_CUT|BW_BANK_KEPT|BW_build|BW_build_chosen|BW_choice_done|BW_choice_locked|BW_cord|BW_cut|BW_cut_chosen|BW_cut_jam|BW_finish|BW_give_wood|BW_grip|BW_holder_back|BW_holder_notch|BW_holder_notched|BW_holder_read|BW_jam_cut|BW_JAM_SWUNG|BW_keep|BW_LANDING_BUILT|BW_leaner_back|BW_leaner_backcut|BW_LEANER_FALLEN|BW_leaner_notch|BW_leaner_notched|BW_leaner_read|BW_measure1|BW_measure1_done|BW_measure2|BW_measure2_done|BW_measure3|BW_measure3_done|BW_OLD_CORD_SEEN|BW_old_read|BW_repair|BW_REPAIR_SEEN|BW_skitter1_dead|BW_skitter2_dead|BW_skitter3_dead|BW_skitter4_dead|BW_skitter5_dead|BW_spare_limbs|BW_stage1|BW_stage1_done|BW_stage2|BW_start|BW_started|BW_TAMSIN_HEARD|BW_wade|BW_waded|BW_wood_given|BW_wrack|BW_wrack_seen|choices_done|clear|close_crossing|crossing_closed|dace_lead|deliver1|deliver2|deliver3|discovery|discovery_end|discovery_finished|drag|earth|evidence_chosen|feed_camp|goose1_dead|goose2_dead|hatchet|hear_order|hear_river|heard_both|heard_order|heard_river|leech_dead|maelin_after|nan_alibi|nan_lead|notch|notch_cut|order_lead|order_transfer|people_uphill|post_found|proof_nan|proof_notches|proof_order|proof_pier|proof_tovin|proof_walk|quest_done|quest_finish|river_read|sack1_done|sack1_lifted|sack2_done|sack2_lifted|sack3_done|sack3_lifted|seat|settle|shallows|shallows_entered|silt_clear|silt1_dead|silt2_dead|silt3_dead|stem|stem_cut|TL_EVIDENCE_KEEPERS|TL_EVIDENCE_PILINGS|TL_EVIDENCE_PLAYER|TL_EVIDENCE_RIVERFOLK|TL_FED_CAMP|TL_HOLLIS_SAW_ORDER|TL_LEAD_DACE|TL_LEAD_NAN|TL_LEAD_ORDER|TL_LEAD_TOVIN|TL_NAN_ALIBI|TL_STONE_KEPT|TL_STONE_PUBLIC|TL_TOVIN_TRUSTED|tool_loaned|tovin_asked|tovin_hesitated|tovin_lead|tovin_odd|tovin_start|tovin_trust|trunk_done|trunk_lifted|trunk_set|uphill_done|wild_boar_dead|wreck_enter|wreck_entered|wreck_inspect|wreck1_dead|wreck2_dead|wreck3_dead".Split('|');
        static readonly string[] TwoCounters = Array.Empty<string>();
        static readonly string[] ThreeItems = "weathered_marker_post|dispatch_order|marker_stem|crew_hatchet|common_timber|game_meat|dried_game_strips|payment|tannin_rich_bark|raw_fowl|fowl_stew".Split('|');
        static readonly string[] ThreeSkills = "woodcutting|hunting|cooking|melee".Split('|');
        static readonly string[] ThreeActions = "arrive|hear_order|hear_river|settle|nan_lead|nan_alibi|dace_lead|order_lead|tovin_start|tovin_odd|tovin_lead|notch|earth|drag|post_found|shallows|clear|hatchet|stem|notch_cut|seat|discovery_end|maelin_after|proof_notches|proof_walk|proof_nan|proof_order|proof_tovin|proof_pier|close_crossing|order_transfer|lift1|deliver1|lift2|deliver2|lift3|deliver3|trunk_lift|trunk_set|uphill_done|TL_EVIDENCE_KEEPERS|TL_EVIDENCE_RIVERFOLK|TL_EVIDENCE_PLAYER|TL_STONE_PUBLIC|TL_STONE_KEPT|quest_finish|ansel_hook|tovin_trust|marker_read|timber_cut|cook_meat|feed_camp|boar_harvest|wild_boar_harvest|eat_food|wreck_enter|wreck_inspect|stone_dry|stone_sketch|true_marker_read|epilogue_keepers|epilogue_riverfolk|epilogue_player|maelin_who|maelin_across|hollis_keepers|hollis_riverfolk|hollis_player|nan_tune|dace_fed|dace_unfed|wynn_camp_line|BW_start|BW_axe|BW_measure1|BW_grip|BW_measure2|BW_measure3|BW_wrack|BW_repair|BW_wade|BW_cut_jam|BW_cord|BW_leaner_read|BW_holder_read|BW_old_read|BW_leaner_notch|BW_leaner_back|BW_keep|BW_cut|BW_build|BW_holder_notch|BW_holder_back|BW_spare_limbs|BW_give_wood|BW_stage1|BW_stage2|BW_finish|BW_kept_bark|BW_built_bark|BW_tamsin_bark|FK_enter|FK_start|FK_lanes|FK_whisperflow|FK_flood_lines|FK_wet_wood|FK_wood|FK_lift1|FK_deposit1|FK_lift2|FK_deposit2|FK_light_fire|FK_tracks|FK_sentinel|FK_nesting|FK_closed|FK_prepare|FK_resolve|FK_recover1|FK_recover2|FK_recover_repeat|FK_cook_batch|FK_cook_repeat|FK_hush|FK_feed1|FK_feed2|FK_feed3|FK_feed4|FK_crew|FK_family|FK_own|FK_tune|FK_finish_crew|FK_finish_family|FK_finish_own|FK_crew_after|FK_family_after|FK_nan_after|FK_bottom_step".Split('|');
        static readonly string[] ThreeQuests = "lowmark.main.01_true_line|lowmark.side.bank_walk|lowmark.side.flood_kitchen".Split('|');
        static readonly string[] ThreeEnemies = "silt1|silt2|silt3|leech|goose1|goose2|boar|wild_boar|wreck1|wreck2|wreck3|BW_skitter1|BW_skitter2|BW_skitter3|BW_skitter4|BW_skitter5|FK_goose1|FK_goose2|FK_leech".Split('|');
        static readonly string[] ThreeHazards = "BW_jam_swing|BW_leaner_fall".Split('|');
        static readonly string[] ThreeFlags = "ansel_hook|arrive|arrived|boar_dead|BW_axe|BW_BANK_CUT|BW_BANK_KEPT|BW_build|BW_build_chosen|BW_choice_done|BW_choice_locked|BW_cord|BW_cut|BW_cut_chosen|BW_cut_jam|BW_finish|BW_give_wood|BW_grip|BW_holder_back|BW_holder_notch|BW_holder_notched|BW_holder_read|BW_jam_cut|BW_JAM_SWUNG|BW_keep|BW_LANDING_BUILT|BW_leaner_back|BW_leaner_backcut|BW_LEANER_FALLEN|BW_leaner_notch|BW_leaner_notched|BW_leaner_read|BW_measure1|BW_measure1_done|BW_measure2|BW_measure2_done|BW_measure3|BW_measure3_done|BW_OLD_CORD_SEEN|BW_old_read|BW_repair|BW_REPAIR_SEEN|BW_skitter1_dead|BW_skitter2_dead|BW_skitter3_dead|BW_skitter4_dead|BW_skitter5_dead|BW_spare_limbs|BW_stage1|BW_stage1_done|BW_stage2|BW_start|BW_started|BW_TAMSIN_HEARD|BW_wade|BW_waded|BW_wood_given|BW_wrack|BW_wrack_seen|choices_done|clear|close_crossing|crossing_closed|dace_lead|deliver1|deliver2|deliver3|discovery|discovery_end|discovery_finished|drag|earth|evidence_chosen|feed_camp|FK_choice_done|FK_closed|FK_closed_entered|FK_cook_batch|FK_crate1_done|FK_crate2_done|FK_crew|FK_deposit1|FK_deposit2|FK_done|FK_enter|FK_entered|FK_family|FK_feed1|FK_feed2|FK_feed3|FK_feed4|FK_finish|FK_fire_lit|FK_fowl1_recovered|FK_fowl2_recovered|FK_fuel_ready|FK_goose1_dead|FK_goose2_dead|FK_household1_fed|FK_household2_fed|FK_household3_fed|FK_household4_fed|FK_hush|FK_HUSH_SEEN|FK_lanes|FK_leech_dead|FK_light_fire|FK_meal_cooked|FK_NAN_TUNE|FK_own|FK_POT_CREW|FK_POT_FAMILY|FK_POT_OWN|FK_recover1|FK_recover2|FK_sentinel_read|FK_start|FK_started|FK_traces_read|FK_tune|FK_whisperflow|FK_wood|goose1_dead|goose2_dead|hatchet|hear_order|hear_river|heard_both|heard_order|heard_river|leech_dead|maelin_after|nan_alibi|nan_lead|notch|notch_cut|order_lead|order_transfer|people_uphill|post_found|proof_nan|proof_notches|proof_order|proof_pier|proof_tovin|proof_walk|quest_done|quest_finish|river_read|sack1_done|sack1_lifted|sack2_done|sack2_lifted|sack3_done|sack3_lifted|seat|settle|shallows|shallows_entered|silt_clear|silt1_dead|silt2_dead|silt3_dead|stem|stem_cut|TL_EVIDENCE_KEEPERS|TL_EVIDENCE_PILINGS|TL_EVIDENCE_PLAYER|TL_EVIDENCE_RIVERFOLK|TL_FED_CAMP|TL_HOLLIS_SAW_ORDER|TL_LEAD_DACE|TL_LEAD_NAN|TL_LEAD_ORDER|TL_LEAD_TOVIN|TL_NAN_ALIBI|TL_STONE_KEPT|TL_STONE_PUBLIC|TL_TOVIN_TRUSTED|tool_loaned|tovin_asked|tovin_hesitated|tovin_lead|tovin_odd|tovin_start|tovin_trust|trunk_done|trunk_lifted|trunk_set|uphill_done|wild_boar_dead|wreck_enter|wreck_entered|wreck_inspect|wreck1_dead|wreck2_dead|wreck3_dead".Split('|');
        static readonly string[] ThreeFlocks = "reed_margin_flock".Split('|');
        static readonly string[] ThreePresentationEvents = "marking_stone_water|shelter_water_hush".Split('|');
        static readonly string[] ThreeCounters = "fk_portions_cooked".Split('|');

        public bool IsCompatibleSaveIdentity(string value)=>value==identity || value==LegacyTwoQuestIdentity || value==LegacyThreeQuestIdentity;

        /// <summary>Only the two explicitly approved published layouts may be upgraded.
        /// All progress is retained; newly appended content receives fresh defaults.
        /// The file owner must preserve original bytes before publishing upgraded data.</summary>
        public GameplaySave PrepareRestore(GameplaySave saved)
        {
            if(saved!=null && saved.contentId==identity){ValidateSave(saved);return Clone(saved);}
            GameplayContent.Need(saved!=null && saved.version==1 && (saved.contentId==LegacyTwoQuestIdentity || saved.contentId==LegacyThreeQuestIdentity),"unsupported_checkpoint_content");
            bool two=saved.contentId==LegacyTwoQuestIdentity;
            var itemIds=two?TwoItems:ThreeItems;var skillIds=two?TwoSkills:ThreeSkills;
            var actionIds=two?TwoActions:ThreeActions;var questDefinitions=two?TwoQuests:ThreeQuests;
            var enemyIds=two?TwoEnemies:ThreeEnemies;var hazardIds=two?TwoHazards:ThreeHazards;
            var flagIds=two?TwoFlags:ThreeFlags;
            RequirePrefix(content.items.Select(v=>v.id),itemIds);
            RequirePrefix(content.skills.Select(v=>v.id),skillIds);
            RequirePrefix(content.actions.Select(v=>v.id),actionIds);
            RequirePrefix(content.quests.Select(v=>v.id),questDefinitions);
            RequirePrefix(content.enemies.Select(v=>v.id),enemyIds);
            RequirePrefix(content.hazards.Select(v=>v.id),hazardIds);
            GameplayContent.Need(saved.items!=null && saved.flags!=null && saved.items.All(v=>v!=null && itemIds.Contains(v.id)) && saved.flags.All(flagIds.Contains),"legacy_unknown_items_or_flags");
            ExactIds(saved.xp,skillIds,v=>v.id);ExactIds(saved.actions,actionIds,v=>v.id);
            ExactIds(saved.quests,questDefinitions,v=>v.id);ExactIds(saved.enemies,enemyIds,v=>v.id);
            ExactIds(saved.hazards,hazardIds,v=>v.id);
            GameplayContent.Need(saved.traps==null && saved.arenas==null,"legacy_unexpected_dungeon_state");
            if(two)GameplayContent.Need(saved.flocks==null && saved.presentations==null && saved.counters==null,"legacy_unexpected_extended_state");
            else
            {
                ExactIds(saved.flocks,ThreeFlocks,v=>v.id);ExactIds(saved.presentations,ThreePresentationEvents,v=>v.id);
                ExactIds(saved.counters,ThreeCounters,v=>v.id);
            }
            var upgraded=Copy(NewState());
            upgraded.tick=saved.tick;upgraded.health=saved.health;
            upgraded.flags=(string[])saved.flags.Clone();
            upgraded.items=saved.items.Select(v=>new ItemAmount(v.id,v.count)).ToArray();
            for(int i=0;i<saved.xp.Length;i++)upgraded.xp[i]=new ItemAmount(saved.xp[i].id,saved.xp[i].count);
            for(int i=0;i<saved.quests.Length;i++)upgraded.quests[i]=new QuestProgress{id=saved.quests[i].id,stage=saved.quests[i].stage};
            for(int i=0;i<saved.actions.Length;i++)upgraded.actions[i]=new ActionProgress{id=saved.actions[i].id,cooldown=saved.actions[i].cooldown};
            for(int i=0;i<saved.enemies.Length;i++)
            {
                var old=saved.enemies[i];var next=upgraded.enemies[i];
                GameplayContent.Need(old.spawnWarning==0 && !old.activated && old.x==0 && old.y==0 && old.z==0 && old.aimY==0,"legacy_unexpected_enemy_fields");
                GameplayContent.Need(string.IsNullOrEmpty(content.enemies[i].spawnFrom),"legacy_enemy_changed_to_summon");
                next.health=old.health;next.windup=old.windup;next.cooldown=old.cooldown;next.respawn=old.respawn;next.loot=old.loot;
                next.aimX=old.aimX;next.aimY=content.targets.First(t=>t.id==content.enemies[i].target).y;next.aimZ=old.aimZ;next.activated=true;
            }
            for(int i=0;i<saved.hazards.Length;i++)upgraded.hazards[i]=new HazardProgress{id=saved.hazards[i].id,remaining=saved.hazards[i].remaining};
            if(!two)
            {
                for(int i=0;i<saved.flocks.Length;i++)upgraded.flocks[i]=CloneFlock(saved.flocks[i]);
                for(int i=0;i<saved.counters.Length;i++)
                {
                    int destination=Array.FindIndex(upgraded.counters,v=>v.id==saved.counters[i].id);
                    GameplayContent.Need(destination>=0,"legacy_counter_removed");
                    upgraded.counters[destination]=new ItemAmount(saved.counters[i].id,saved.counters[i].count);
                }
                for(int i=0;i<saved.presentations.Length;i++)
                {
                    var old=saved.presentations[i];var definition=content.presentationEvents.First(p=>p.id==old.id);
                    GameplayContent.Need(old.remaining>=0 && old.remaining<=definition.ticks && old.seen==saved.flags.Contains(definition.triggerFlag) && (old.seen || old.remaining==0),"legacy_presentation");
                }
            }
            // A historical seen event is not replayed, even if its old DTO had no presentation array.
            foreach(var presentation in upgraded.presentations)
            {
                var definition=content.presentationEvents.First(p=>p.id==presentation.id);
                presentation.seen=upgraded.flags.Contains(definition.triggerFlag);presentation.remaining=0;
            }
            ValidateSave(upgraded);
            return upgraded;
        }
        static void RequirePrefix(IEnumerable<string> current,string[] expected)
        {
            GameplayContent.Need(current.Take(expected.Length).SequenceEqual(expected,StringComparer.Ordinal),"legacy_content_identity_removed_or_reordered");
        }
        static void ExactIds<T>(T[] records,string[] expected,Func<T,string> id) where T:class
        {
            GameplayContent.Need(records!=null && records.Length==expected.Length && records.All(v=>v!=null) && records.Select(id).SequenceEqual(expected,StringComparer.Ordinal),"legacy_checkpoint_layout");
        }
    }
}
