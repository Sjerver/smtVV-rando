PROTOFIEND_IDS = [1101,1102,1103,1104,1105,1106,1107,1108,1109,110,1111,1112,1113,1114,1115,1116,1117,1118]

#Demons that overlap in Event Encounters and in which ones they do
DUPLICATE_SOURCES = {442 : [61 ,65], #School Aitvaras
                     443 : [56, 58, 59, 60], #School Andras
                     444 : [56, 57, 59, 60, 63], #School Rakshasa 
                     445 : [57, 58, 61, 64, 129], #School Incubus + Extra One(?)
                     446 : [62, 63], #School Oni 
                     447 : [64, 66, 129], #School Manangal + Extra One(?)
                     448 : [65, 66], #School Shiki-Ouji 
                     484 : [232, 233, 234, 235, 236, 237, 248], #Area 3 Powers
                     756 : [158, 159, 160], #Mad Gasser Quest Zhens
                     #870 : [108] #Seth appears as a punishing foe and an event encounter
}
#Selection of dummy demons to be overwritten with overlapping demons
DUMMY_DEMONS= [487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511]

NORMAL_ENEMY_COUNT = 395

BAD_IDS = [71, 365, 364, 366] #Old Lilith, Tao x2, Yoko

TOTAL_DEMON_COUNT = 1201

#Obtained by creating a linear trend function for the potential of compendium demons
POTENTIAL_SCALING_FACTOR = 0.167
BASE_POTENTIAL_VALUE = 6.67

#Lists of miracle IDs that are "progressive", with IDs in the order the player should obtain them
MIRACLE_DEPENDENCIES = [
    [24, 25, 26, 131], #Deathly Aura
    [32, 33, 34], #Art of Essences
    [35, 36], #Healer's Hospitality
    [37, 38], #Merchant's Hospitality
    [39, 40, 41], #Summoner's Hospitality
    [49, 50], #Empowering Cheer
    [51, 52, 53, 54], #Demon Proficiency
    [55, 56, 57, 58, 59, 60, 118, 119, 120], #Divine Garrison
    [61, 62, 63, 64], #Divine Proficiency
    [65, 66, 67, 68, 69], #Almighty Mastery
    [70, 71, 72, 73, 74], #Physical Mastery
    [75, 76, 77, 78, 79], #Fire Mastery
    [80, 81, 82, 83, 84], #Ice Mastery
    [85, 86, 87, 88, 89], #Elec Mastery
    [90, 91, 92, 93, 94], #Force Mastery
    [95, 96, 97, 98, 99], #Light Mastery
    [100, 101, 102, 103, 104], #Dark Mastery
    [105, 106, 107], #Recover Mastery
    [108, 109, 110], #Support Mastery
    [111, 112, 113, 114, 115], #Ailment Mastery
    [21, 130], #Inspiring Covenant
    [132, 133], #Frugal Soul
    [138, 139] #Estoma Field
]

#IDs of miracles obtained when you first unlock the cathedral of shadows
STARTING_MIRACLES = [13, 27, 49, 75, 80, 85, 90]

TUTORIAL_DAEMON_ID = 430

FIRST_GUEST_YUZURU_ID = 1150

CHEST_MACCA_MIN = 500
CHEST_MACCA_MAX = 60000
#Chance of a chest containing macca instead of an item/essence
CHEST_MACCA_ODDS = 0.035

#Chance of a chest containing an essence instead of an item
CHEST_ESSENCE_ODDS = 0.42

#Items that have a bag limit of less than 5, excluding essences
ITEM_QUANTITY_LIMITS = {
    60: 1, #Whittled Goat
    62: 3, #Dampeners
    63: 3,
    64: 3,
    65: 3,
    66: 3,
    67: 3,
    68: 3,
}

#Odds of a chest containing 1-5 items excluding essences which are always 1
CHEST_QUANTITY_WEIGHTS = {
    1: 134,
    2: 78,
    3: 42,
    4: 8,
    5: 4
}

#The number of different consumable items (including some DUMMY items), from indices 0-113
CONSUMABLE_ITEM_COUNT = 114

#Any chest with an item index 611 or higher contains a key item and should not be randomized
KEY_ITEM_CUTOFF = 611

#Item indices that correspond to reusable items like the return pillar or gleam grenade
BANNED_ITEMS = [70, 73, 74, 75, 76, 77, 78, 79, 80, 81]

#Event encounter ID of chimera who needs to drop the horn of plenty
CHIMERA_ENCOUNTER_ID = 92

#Demon ID of chimera who drops the horn of plenty
CHIMERA_DEMON_ID = 812

#Demon ID of Seth who has an event encounter and normal unique symbol encounter
SETH_DEMON_ID = 870
#Event Encounter ID of Seth
SETH_EVENT_ENCOUNTER_ID = 108
#List of demons with overly large symbol scaling (>2)
LARGE_SYMBOL_DEMONS = [77,80,94,127,212,283] #Mara, Surt, Huang Long, Chimera, Oyamatsumi, Thunderbird

def getMaccaValues ():
    return [0,10,13,15,16,17,18,20,21,23,24,26,28,29,31,33,34,36,38,40,41,44,46,49,51,55,58,61,65,68,71,74,78,82,87,90,94,98,103,107,111,116,121,126,131,137,142,147,153,159,164,170,177,184,190,198,204,212,218,225,233,241,249,257,264,273,281,290,298,307,315,356,374,415,456,542,629,758,887,1016,1145,1274,1403,1532,1661,1790,1919,2048,2177,2306,2435,2564,2693,2822,2951,3080,3209,3338,3467,3596]


def getExpValues():
    return [0,24,26,29,32,37,42,47,57,74,87,98,123,151,182,217,257,300,347,398,453,512,575,642,713,788,867,949,1035,1124,1216,1312,1427,1548,1675,1807,1946,2090,2241,2397,2559,2727,2901,3081,3267,3459,3657,3861,4071,4281,4500,4728,4856,4927,4997,5165,5334,5372,5410,5460,5509,5597,5672,5773,5821,5860,5933,6000,6058,6132,6172,6280,6326,6447,6568,6665,6762,6858,6954,7050,7146,7242,7338,7434,7530,7626,7722,7818,7914,8010,8106,8202,8298,8394,8490,8586,8682,8778,8874,8970]


def getBonusSkills():
    return [["Impaler's Revenge",510,90,90],['Intercalation',452,69,69],['Elusive Eclipse',451,52,52],['Rooted Soul',450,12,12],[ 'Moonlight Frost',255,83,83],[ 'Frenzy',283,15,15],[ 'Galvanic Slash',284,46,49],[ 'Sakanagi',292,25,25],[ 'Divine Arrowfall',293,41,41],[ 'Murakumo',294,67,67],[ 'Red Capote',295,24,24],[ 'Aramasa',298,8,8],[ 'Wrath Tempest',299,44,44],[ 'Ruinous Thunder',300,31,31],[ 'Thalassic Calamity',301,54,54],[ 'Kannabi Veil',306,36,36],[ 'Profaned Land',307,48,48],[ 'Miracle Water',310,17,17],[ 'Dreadful Gleam',312,52,52],[ 'Purgatorium',320,83,83],[ 'Impetus',321,83,83],[ 'Inferno of God',329,95,99],[ 'Hailstorm of God',330,95,99],[ 'Lightning of God',331,95,99],[ 'Tornado of God',332,95,99],[ 'Cold Dark Matter',333,90,99],[ 'Hot Dark Matter',334,95,99],[ 'Freikugel',335,95,99],[ 'Gaea Rage',336,95,99],[ 'Magma Axis',337,95,99],[ 'Javelin Rain',338,90,99],[ 'Xeros Beat',339,95,99],[ 'Deadly Fury',340,90,99],[ 'Wild Dance',341,95,99],[ 'Contempt of God',342,95,99],[ 'Freikugel',370,95,99],[ 'Javelin Rain',372,95,99],[ 'Deadly Fury',373,95,99],[ 'Evil Gleam',390,95,99],[ 'Sonic Boom',392,35,35],[ 'Gaea Rage',394,95,99],[ 'Chaotic Will',395,95,99],[ 'Javelin Rain',397,95,99],[ 'Deadly Fury',398,95,99],[ 'Abyssal Beckoning',861,84,84],[ 'Seething Mansemat',863,84,84],[ 'Untainted Wind',864,84,84],[ 'Boundless Sea',865,83,83],[ 'Bufu',902,8,8],[ 'Rakunda',903,8,8],[ 'Gram Slice',904,8,8],[ 'Charge',905,44,47],[ 'Bufula',906,44,47],[ 'Carnage Fang',908,44,47],[ "Sun's Radiance",909,44,47],[ 'Witness Me',910,44,47],[ 'Hama',911,8,8],[ 'Mahamaon',912,44,44],[ 'Mirage Shot',913,44,44],[ 'Zanma',914,44,44],[ 'Trafuri',915,44,44],[ 'Cautious Cheer',916,44,44],[ 'Toxic Cloud',917,44,44],[ 'Paraselene Blur',918,80,80],[ 'Evergreen Dance',921,51,51],[ 'Inflaming Divinity',922,28,28],[ 'Heavenly Ikuyumi',923,72,72],[ 'Moonlight Frost',924,52,52],[ 'Lunar Hurricane',925,69,69],[ 'Luminescent Mirage',926,80,80],[ 'Lunation Flux',927,69,69]]