"""Frozen architectural working grammar for Caelmor's four regions.

Region-specific construction tendencies here are art-direction inferences, not
additional locked canon. The cited dossiers establish the broad cues only.
"""
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class RegionSpec:
    code: str
    label: str
    contexts: object  # immutable mapping: stable ID -> display label
    sources: tuple
    default_context: str
    foundation_mode: str
    wall_material: str
    construction: str
    roof_cover: str
    weather_exposure: float
    base_palette: object


@dataclass(frozen=True)
class TypeSpec:
    category: str
    label: str
    family: str
    width: float
    depth: float
    wing_width: float
    wing_depth: float
    floors: int
    footprint: str
    roof_style: str
    features: tuple

    @property
    def default_dimensions(self):
        return (self.width,self.depth,self.wing_width,self.wing_depth)

    @property
    def building_category(self):
        """Broad functional grouping; `category` remains the stable type ID."""
        return {
            'FARMHOUSE':'RESIDENTIAL','COTTAGE':'RESIDENTIAL','TOWNHOUSE':'RESIDENTIAL',
            'LONGHOUSE':'RESIDENTIAL','BARN':'AGRICULTURAL','GRAIN_STORE':'AGRICULTURAL',
            'STABLE':'AGRICULTURAL','MILLER':'COMMERCIAL','INN':'COMMERCIAL',
            'MERCHANT_HOUSE':'COMMERCIAL','SHOP':'COMMERCIAL','WAREHOUSE':'COMMERCIAL',
            'MARKET_HALL':'COMMERCIAL','SMITHY':'INDUSTRIAL','WORKSHOP':'INDUSTRIAL',
            'ASSEMBLY_HALL':'CIVIC','WATCHTOWER':'DEFENSIVE','GATEHOUSE':'DEFENSIVE',
            'BARRACKS':'DEFENSIVE','BOATHOUSE':'WATERFRONT',
        }[self.category]


def _region(code,label,contexts,source,default,mode,wall,construction,cover,exposure,palette):
    return RegionSpec(code,label,MappingProxyType(contexts), (source,), default, mode,
                      wall,construction,cover,exposure,MappingProxyType(palette))


REGIONS = MappingProxyType({r.code:r for r in (
    _region('LOWMARK','Lowmark Vale', {
        'BROOKHOLLOW':'Brookhollow riverside market town','CRESTBRIDGE':'Crestbridge trade crossing',
        'ASHENSTEAD':'Ashenstead rebuilt village','GREYHARROW':'Greyharrow side-river town',
        'RURAL':'Lowmark rural holdings'}, 'LORE/Regions/Caelmor_Region1_LowmarkVale.md', 'RURAL',
        'PLINTH','plaster','TIMBER_INFILL','SHINGLE',.38,
        {'roof':(.30,.22,.16,1),'roof_dark':(.19,.17,.15,1),'plaster':(.70,.63,.49,1),
         'timber':(.27,.19,.12,1),'stone':(.39,.38,.33,1),'glass':(.48,.64,.63,1),'metal':(.24,.25,.23,1)}),
    _region('THORNFELL','Thornfell Marches', {
        'STONEWAKE':'Stonewake cliff terraces','HIGHSTEADS':'Highsteads ridge longhouses',
        'PASSWATCH':'Passwatch fortified outpost','RIDGE':'Open ridge settlements'},
        'LORE/Regions/Caelmor_Region2_ThornfellMarches.md','RIDGE','PLINTH','stone','RUBBLE','SLATE',.92,
        {'roof':(.24,.27,.29,1),'roof_dark':(.15,.18,.20,1),'plaster':(.56,.52,.43,1),
         'timber':(.25,.20,.15,1),'stone':(.43,.43,.41,1),'glass':(.42,.51,.52,1),'metal':(.24,.27,.29,1)}),
    _region('MIRE','Mire of Fallen Banners', {
        'SORROWMERE':'Sorrowmere raised settlement','MARSHFALL':'Marshfall forest edge',
        'GRIEFWATCH':'Griefwatch ridge post','ROOTREST':'Rootrest tree-root settlement'},
        'LORE/Regions/Caelmor_Region3_MireOfFallenBanners.md','SORROWMERE','PIERS','timber_light','BOARD','REED',.74,
        {'roof':(.29,.27,.21,1),'roof_dark':(.18,.19,.17,1),'plaster':(.50,.47,.37,1),
         'timber':(.28,.24,.17,1),'stone':(.35,.34,.30,1),'glass':(.39,.48,.43,1),'metal':(.25,.25,.21,1)}),
    _region('EMBERHOLT','Emberholt Heights', {
        'EMBERHOLD':'Emberhold civic terraces','EMBERFORGES':'Forge district',
        'CINDERWEAVE':'Cinderweave artisan quarter','ASHSPIRE':'Ashspire wealthy ward'},
        'LORE/Regions/Caelmor_Region4_EmberholtHeights.md','EMBERHOLD','PLINTH','stone','ASHLAR','CLAY',.66,
        {'roof':(.31,.20,.15,1),'roof_dark':(.20,.15,.13,1),'plaster':(.57,.43,.34,1),
         'timber':(.25,.16,.12,1),'stone':(.34,.31,.29,1),'glass':(.45,.50,.50,1),'metal':(.27,.25,.24,1)}),
)} )


def _t(category,label,family,w,d,ww,wd,floors,footprint,roof,features):
    return TypeSpec(category,label,family,w,d,ww,wd,floors,footprint,roof,tuple(features))


TYPE_SPECS = MappingProxyType({s.category:s for s in (
    _t('FARMHOUSE','Farmhouse','dwelling',10.5,7,4,4,2,'L','GABLE',('chimney','porch','domestic_windows')),
    _t('BARN','Barn','agricultural',15,9,5,6,1,'T','GABLE',('wide_bay','loft_vents','lean_to')),
    _t('GRAIN_STORE','Grain Store','storage',9,7,3.2,4,2,'RECT','HIP',('raised_sill','vent_slots','loading_door')),
    _t('MILLER','Miller House','mixed_use',11,7,4.2,4.5,2,'L','GABLE',('mill_workshop','chimney','domestic_windows')),
    _t('INN','Inn','hospitality',13,9,4.5,5,2,'L','GABLE',('public_porch','sign_beam','larger_windows')),
    _t('COTTAGE','Cottage','dwelling',8,6,3,3.5,1,'RECT','GABLE',('low_eaves','chimney','small_windows')),
    _t('TOWNHOUSE','Townhouse','dwelling',7.5,8,3,4,3,'RECT','GABLE',('tall_facade','stacked_windows','street_entry')),
    _t('MERCHANT_HOUSE','Merchant House','mixed_use',11,8,4,4.5,2,'L','GABLE',('shopfront','upper_hall','store_entry')),
    _t('LONGHOUSE','Longhouse','communal',16,7,5,6,1,'RECT','GABLE',('long_bench_windows','central_hearth','deep_eaves')),
    _t('SHOP','Shop','commercial',8,7,3,4,2,'RECT','GABLE',('display_front','broad_entry','upper_store')),
    _t('WAREHOUSE','Warehouse','storage',17,10,5,6,1,'T','GABLE',('loading_bay','hoist_beam','clerestory_vents')),
    _t('MARKET_HALL','Market Hall','civic_commercial',18,12,5,7,1,'U','HIP',('open_arcade','market_porch','high_vents')),
    _t('STABLE','Stable','agricultural',13,8,4.5,5,1,'L','GABLE',('paired_stall_doors','hayloft','side_ramp')),
    _t('SMITHY','Smithy','industrial',10,8,3.5,4,1,'RECT','GABLE',('forge_stack','wide_workdoor','vented_ridge')),
    _t('WORKSHOP','Workshop','craft',10,7,3.5,4,1,'L','GABLE',('workbench_windows','wide_workdoor','tool_ledge')),
    _t('ASSEMBLY_HALL','Assembly Hall','civic',16,11,5,6,2,'T','HIP',('civic_porch','raised_entry','long_windows')),
    _t('WATCHTOWER','Watchtower','defensive',7,7,2.8,3,3,'RECT','HIP',('guard_gallery','corner_posts','narrow_windows')),
    _t('GATEHOUSE','Gatehouse','defensive',12,8,4,4.5,2,'U','HIP',('passage_arch','flanking_rooms','guard_gallery')),
    _t('BARRACKS','Barracks','defensive',15,8,4.5,5,2,'L','GABLE',('bunk_windows','covered_entry','equipment_bay')),
    _t('BOATHOUSE','Boathouse','waterfront',12,8,4,5,1,'RECT','GABLE',('waterside_door','slipway','raised_deck')),
)} )

CONTEXTS = MappingProxyType({code:region.contexts for code,region in REGIONS.items()})
WEALTH_LEVELS = ('MODEST','ESTABLISHED','AFFLUENT')
CRAFTSMANSHIP_LEVELS = ('ROUGH','STANDARD','FINE')
