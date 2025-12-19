# NPC Asset Brief (Prompt-Ready Template)
> Output this **exact structure**. Every field maps 1:1 into the image-generation prompt.

## CORE
- **NPC_NameOrTitle:** {e.g., The Flameward Speaker}
- **Region:** {Lowmark | Thornfell | Mire | Emberholt}
- **FactionOrAlignment:** {optional; short tag string}
- **Role_OneLine:** {what they are in one sentence, diegetic}
- **PlayerFunction:** {merchant | quest-giver | trainer | witness | antagonist | ambient}
- **Tone_Constraints:** grounded mythic-medieval, lived-in, minimal spectacle; magic rare/dangerous unless explicitly required

## SILHOUETTE + READABILITY
- **Silhouette_Keywords_3to5:** {comma-separated}
- **ReadAtDistance_Top2Identifiers:** {1) shape/garment/prop 2) color/material contrast}

## BODY + POSE (NO AGE REQUIRED)
- **Proportions_Read:** {short, average, tall; lean/average/heavy; any asymmetry like limp}
- **Posture_Read:** {erect/guarded/hunched/proud/burdened}
- **NeutralPose_ForTurnaround:** {relaxed stance | light A-pose | hands clasped | etc}

## FACE + HAIR (CONCRETE CUES)
- **Face_Cues_2to4:** {comma-separated specifics: scar location, soot lines, broken nose, etc}
- **Eyes_Cue:** {color + how they catch light; avoid “glowing” unless canon}
- **Hair_Cues_2to4:** {style, length, grooming, ties/clasps, ash/grease presence}

## MATERIALS + PALETTE
- **Palette_3to5Colors:** {comma-separated; dominant, secondary, accent}
- **Primary_Materials_3to6:** {comma-separated: ash-wool, leather, iron, ember-silk, etc}
- **Metal_Finish:** {dull iron | heat-blued | brass | tarnished | none}
- **Cloth_Finish:** {matte coarse | lightly reflective | stiffened hem | etc}

## OUTFIT LAYERS (MODEL-FRIENDLY)
- **BaseLayer_Garments:** {comma-separated}
- **MidLayer_Garments:** {comma-separated}
- **OuterLayer_Garments:** {comma-separated}
- **Fasteners_AndHardware:** {laces/toggles/pins/belts; what metal/finish}
- **Footwear:** {boots/shoes type + condition}
- **Gloves:** {none | work gloves | thin formal gloves + material}

## MOTIFS + ICONOGRAPHY (SUBTLE)
- **Motif_SourceAndMeaning_OneLine:** {e.g., civic seal stitch signifying office}
- **Motif_Placement:** {cuff/collar/buckle/pendant/etc}

## PROPS (STORY OBJECTS)
- **Primary_Prop:** {what it is + construction}
- **Primary_Prop_CarryMethod:** {in hand | slung | belt loop | back strap | etc}
- **Secondary_Props_Optional:** {comma-separated}

## WEAR + GRIME (REGION-TRUE)
- **WearAndGrime_Notes_2to4:** {where dirt/ash/mud collects; repairs; singe; fray}

## VARIANTS (OPTIONAL BUT USEFUL)
- **VariantA_OneLine:** {formal/work/travel differences}
- **VariantB_OneLine:** {weather/damage/late-state differences}

## BLENDER NOTES (SOLO-SAFE)
- **Modular_Pieces_ShortList:** {outer, belt, hood, prop head, etc}
- **Complexity_Target:** {low | medium}
- **DontOverbuild_Warning_OneLine:** {what to simplify}
