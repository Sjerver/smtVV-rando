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

#IDs of divine garrison miracles in order
DIVINE_GARRISON_IDS = [55, 56, 57, 58, 59, 60, 118, 119, 120]

#ID of miracle rank violation
RANK_VIOLATION_ID = 31

TUTORIAL_DAEMON_ID = 430

FIRST_GUEST_YUZURU_ID = 1150

CHEST_MACCA_MIN = 500
CHEST_MACCA_MAX = 60000
#Chance of a chest containing macca instead of an item/essence
CHEST_MACCA_ODDS = 0.035

#Chance of a chest containing an essence instead of an item
CHEST_ESSENCE_ODDS = 0.42

#Chance that a boss demon will drop their essence
BOSS_ESSENCE_ODDS = 0.30

#Odds that a boss will drop 1, 2, or 3 items
BOSS_DROP_QUANTITY_WEIGHTS = {
    1: 133,
    2: 54,
    3: 12
}

#Items that have a bag limit of less than 10, excluding essences
ITEM_QUANTITY_LIMITS = {
    60: 1, #Whittled Goat
    62: 3, #Dampeners
    63: 3,
    64: 3,
    65: 3,
    66: 3,
    67: 3,
    68: 3,
    5: 5, #Bead Chain
    6: 5, #Soma
    59: 5, #Gold Card
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

#Item indices that correspond to reusable items like the return pillar or gleam grenade and spyglass(spyscope is given by tutorial daemon)
BANNED_ITEMS = [70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 55]

BANNED_ESSENCES = [359,555,545,546,547,548,549,550,551,552,553,554,556,557,558,559,606,607,608] #Old Lilith's Essence, Demi-fiends Essence, Aogami & Tsukuyomi Essences

#Chance that a miman reward is an essence
MIMAN_ESSENCE_ODDS = 0.27272727
#Odds of how many different items a miman reward has
MIMAN_ITEM_NUMBER_WEIGHTS = {
    1: 8,
    2: 1,
    3: 1,
    6: 4,
    7: 7,
    11: 3
}
#Odds if how many of a single item are in miman reward
MIMAN_ITEM_AMOUNT_WEIGHTS = {
    1: 4,
    2: 7,
    3: 5,
    4: 4,
    6: 3,
    8: 1
}

#Item IDs of Key items in Miman Rewards in the normal game
MIMAN_BASE_KEY_ITEMS = [819,816,810,829,818,823,817]#Talismans: Element, Avatar, Avian, Kishin, Genma, Fiend, Holy

#List of key item ids obtained via events
GIFT_BASE_KEY_ITEMS = []

#Chance a mission rewards macca
MISSION_MACCA_ODDS= 0.1717
#Chance a mission rewards an essence instead of an consumable item
MISSION_ESSENCE_ODDS= 0.09090
MISSION_MACCA_MAX= 150000
MISSION_MACCA_MIN= 4000

#The possible amounts for consumable rewards and their weights
MISSION_QUANTITY_WEIGHTS = {
    1:52,
    2:15,
    3:12,
    4:5,
    5:4,
    10:1,
    7:1,
    6:2
}

#Missions with duplicate missions that should have the same rewards
MISSION_DUPLICATES = {
  12: [106], #A Golden Opportunity
  73: [147], #A Power Beyond Control
  34: [148], #An Unusual Forecast
  139: [180], #Liberate the Golden Stool
  59: [145], #Lighting the Way
  138: [179], #Reclaim the Golden Stool
  84: [144], #Return of the True Demon
  32: [141], #Roar of Hatred
  62: [146], #Stones of Malice
  31: [142], #Angel of Destruction
  29: [140], #The Horn of Plenty
  51: [222], #The Red Dragon's Invitation
  50: [221], #The Seraph's Return
  41: [143], #The Winged Sun
  95: [116], #To the Empyrean
  52: [53,54], #The Compassionate Queen, The Noble Queen, The Wrathful Queen (Same reward but not true duplicate)
  28: [173], #Clash with the Kunitsukami, Special Training: Kunitsukami (Both normally give Kunitsu Talisman)
  -18: [-19], #Duplicates for the fake missions handling the Heavenly Kings Periapt
  72: [-20], #Falcon's Head and Isis Story Even in CoV both reward Lady Talisman
}

#List of exclusive key item rewards from both canons
CREATION_EXCLUSIVE_KEY_REWARDS = [] #Currently not any
VENGEANCE_EXCLUSIVE_KEY_REWARDS = [] #Currently not any

#List of banned key rewards
BANNED_KEY_REWARDS = [79] #Spyscope (dropped by tutorial daemon)

#Exclusive mission from both canons to give potential exclusive rewards to (excluding missions whose rewards are not randomized or are not allowed to receive key item rewards)
CREATION_EXLUSIVE_MISSIONS = [72,40,42,26,25,30,22,24,27,204,206,187,93,-7,-8,-9-10] #The Falcon's Head, Egyptians Fate, Succesion of Ra, Path to Myojin Forest, One Mokois Trash,
        #He of a Hundred Hands, Hellfire Highway, Search for Oyamatsumi, Glitter in Ginza, Netherworld Relay Racing, Will of the Samurai, Trial of the Seven Stars, Defeat the Demon Kings Armies
        #Keeper of South/North/West/East Secondary Rewards
VENGEANCE_EXLUSIVE_MISSIONS = [157,152,159,177,171,194,203,178,202,184,200,210,172,211,193,174,188,190,108,109,110,111,112,113] #Supply Run, Guide to the Lost, Heart of Garnet, As God Wills, A Self of my Own, Devotion To Order, Part-time Gasser, A Star is Born
        #Disgraced Bird God, Alice's Wonderland, Shinjuku Jewel Hunt, Heroes of Heaven and Earth, Rite of Resurrection, 'God of Old, Devourer of Kin', The Heartbroken, Special Training: Army of Chaos
        #The Serpent King, The Great Adversary, Investigate the Anomalies in Tokyo, Investigate the Salt Incidents, Rescue Miyazu Atsuta, Investigate Jozoji Temple, Qadištu Showdown

#Mutually exclusive missions that should never reward a key item
MUTUALLY_EXCLUSIVE_MISSIONS = [
    176,175,#Vampire in Black/Hunter in White
    70,71, #The Water Nymph/Spirit of Love
    79,80, #Raid on Tokyo/In Defense of Tokyo
    77,78, #Black Frost Strikes Back/Sobering Standoff
    138,139, #Reclaim/Liberate the Golden Stool (Have duplicates but not needed here)
    75,76, #Those Seeking Sanctuary, Holding the Line
    51,50 #The Red Dragon's Invitation/The Seraphs Return
    -2, -3, #Additional Rewards from The Red Dragon's Invitation/The Seraphs Return
]

#Reward cannot be randomized, due to Quest Progression Issues or too strong reward(True Demon) or mission is unused
BANNED_MISSIONS = [84,144,35, 1,2,3,60,89,90,154] #True Demon x2, Ancient Guardian, and Unused Missions

#Repeatable Missions that always have the same reward and therefore should not have unique reward or macca
REPEAT_MISSIONS = [66,59,145,62,146,65,64,67,58]# Incentive for Incense, Lighting the Way x2, Stones Of Malice x2,Princess in a Pickle, Sleeping Sands, Need for Nectar, Iced Out 

#Event encounter ID of chimera who needs to drop the horn of plenty
CHIMERA_ENCOUNTER_ID = 92
#Demon ID of chimera who drops the horn of plenty
CHIMERA_DEMON_ID = 812
#Event encounter ID of giri who needs to drop his head
GIRI_ENCOUNTER_ID = 93
#Demon ID of giri who drops his head
GIRI_DEMON_ID = 827
#Encounter ID of horus who needs to drop his head
HORUS_ENCOUNTER_ID = 1923
#Demon ID of horus who drops his head
HORUS_DEMON_ID = 864

#Boss demon ids who have quest related drops
QUEST_DROPS_BOSSES = [812, 827, 864, 808]#Chimera, Girimekhala, Horus, Thunderbird
#Encounter Ids of bosses who have quest related drops
QUEST_DROPS_BOSS_ENCOUNTERS = [92, 93, 1923, 91]#Chimera, Girimekhala, Horus, Thunderbird

#Demon ID of Seth who has an event encounter and normal unique symbol encounter
SETH_DEMON_ID = 870
#Event Encounter ID of Seth
SETH_EVENT_ENCOUNTER_ID = 108
#List of demons with overly large symbol scaling (>2)
LARGE_SYMBOL_DEMONS = [77,80,94,127,212,283] #Mara, Surt, Huang Long, Chimera, Oyamatsumi, Thunderbird
#Map of punishing foe ID - walkspeed for birds that have large flight cycles
PUNISHING_FOE_BIRD_SPEEDS = {802: 1400, #Jatayu
                             808: 1200, #Thunderbird
                             864: 1500, #Horus
                             865: 800,  #Garuda
                             870: 3000, #Seth
                             891: 1400} #Gurulu

#List of bosses able to fully heal themselves with diarahan infinitely
DIARAHAN_BOSSES = [842, 770, 617] #Onyankopon, Maria, Yurlungur

#Innate Skills that have no effect on player demons
BAD_INNATES = [697,698, 561, 562, 563, 695, 576, 660, 700, 706, 642, 696, 707, 699]
# Bit Conversion, Cleansing Jolt, Fire Star, Ice Star, Elemental Star, God's Aid, Ironclad Defense, King's Ascendancy, Mitama Soul, Musmahhuu, Synergistic Replication, Unwavering Faith, World Ingurgitation, Star Fragment

#Innate Skills that have no effect on the nahobino and are not listed in BAD_INNATES
BAD_INNATES_NAHO = [573, 574, 575, 629, 637, 628, 549, 550, 551, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 542, 543, 544, 545, 546, 547, 548]
#Moirae Cutter, Moirae Spinner, Moirae Measurer, Figment of Darkness, Pine Tree's Rebirth, Heart of Devotion, Wanton Rebel, Power Menace,
# Myopic Pressure, Demonic Mediation, Allure, Mother of Ploys, Monstrous Offering, Skyward Withdrawal, Four Horsemen, Curious Dance, Runes of Wisdom, Eye of Ra, Brewing Storm,
# Eye of Horus, Planck of Norn, Rallying Aid, Fairy King's Melody, Trumpets of Judgment, Heavenly Reversal

#Fionn, Idun, and Yoshitsune need to have their vanilla tones for quests to work. Moirae Sisters give a quest too but are regular encounters so their tones are unchanged
DEMON_HAUNT_QUESTGIVER_IDS = [23, 35, 224]

#Range for the modifiers of demons HP in comparison to nahobino at the same level. Multiplied by 1000
DEMON_HP_MOD_RANGE = [650,1200]
#Range for the modifiers of demons MP in comparison to nahobino at the same level. Multiplied by 1000
DEMON_MP_MOD_RANGE = [666,1400]
#Range for the modifiers of demons stats in comparison to nahobino at the same level. Multiplied by 1000
DEMON_STAT_MOD_RANGE = [500,2000]

#Predefines progression points from which items can show up
CONSUMABLE_PROGRESSION = {
  0: [1,2,4,7,59,61,63,64,65,66,67,68,72,82,83,109,111,113,91,92,93,94,95,96,97], 
    #Universal: Life Stone, Chakra Drop, Bead, Revival Bead, Gold Card, Smoke Ball, Dampeners, Attract Pipe, Gospel, Grimoire, Small Glory Crystals, Simple Demon Box, New Testament Tablet, Incenses,
  1: [3,5,6,8,23,24,25,26,27,28,37,38,39,40,41,42,43,44,45,46,47,50,51,52,53,98,99,100,101,102,103,104,105,106,107,108], #After Minato: Chakra Pot, Bead Chain, Soma, Balm of Life, Elemental Gems, Status Gems, 
    #Support Gems, Drain Gems, Purge/Dispel Charms, Attack Mirror, Magic Mirror, Sutras
  2: [15,16,17,18,19,20,21,22], #Pre Taito: Life Stone Chain, Soma Drop, Elemental Shards
  3: [60,62], #From Area 3 Dungeons onward: Whittled Goat, Phys Dampener
  4: [10,112,84,85,86,87,88,89,90,110,14], #Post Shinagawa: Amrita Shower, Lavish Demon Box, Stat Balms, Large Glory Crystal, Muscle Drink,
}

#Defines which items should be available in each area based on progression points
CONSUMABLE_MAP_SCALING = {
  60: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] + CONSUMABLE_PROGRESSION[3] + CONSUMABLE_PROGRESSION[4] + [13], #Taito: Ambrosia,
  61: CONSUMABLE_PROGRESSION[0] +CONSUMABLE_PROGRESSION[2] + [9,11], #Minato: Amrita Soda, Medicine, 
  62: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[2] +[9,12], #Shinagawa: Amrita Soda, Ox Bezoar,
  63: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[4]+CONSUMABLE_PROGRESSION[2] +[13], #Chiyoda: Ambrosia,
  64: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[4]+CONSUMABLE_PROGRESSION[2] +[13], #Shinjuku: same as above
  16: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[4]+ CONSUMABLE_PROGRESSION[3] +[], #Empyrean: 
  35: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[4]+ CONSUMABLE_PROGRESSION[3] +[], #Temple of Eternity: 
  36: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[4]+CONSUMABLE_PROGRESSION[2]+ CONSUMABLE_PROGRESSION[3] +[13], #Demon Kings Castle / Shakan: Ambrosia,
  38: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[4]+CONSUMABLE_PROGRESSION[2]+ CONSUMABLE_PROGRESSION[3] +[13], #Demon Kings Castle / Shakan: same as above
  107: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] +CONSUMABLE_PROGRESSION[4]+ CONSUMABLE_PROGRESSION[3] +[], #Demi-Fiend Area: same as Empyrean
}

# Describes what level essences rewards can be in areas
# [Min,Max] level based on base game (Excluding Outliers: Alice in Taito and Odaiba Essences in Minato)
ESSENCE_MAP_SCALING = {
  60: [52,71], #Taito
  61: [1,24], #Minato
  62: [15,37], #Shinagawa
  63: [36,50], #Chiyoda
  64: [36,50], #Shinjuku
  16: [76,95], #Empyrean
  35: [71,77], #Temple of Eternity
  36: [50,54], #Demon Kings Castle / Shakan
  38: [50,54], #Demon Kings Castle / Shakan,
  107: [86,95], #Demi-Fiend Area: same as Empyrean
}

#Defines the missions that are scaled on the area
REWARD_AREA_MISSIONS = {
  16: [47,52,53,54,55,188,190,51,50],
  35: [81,95],
  36: [212,114,174],
  38: [212,114,174],
  60: [33,35,36,37,38,39,40,42,43,44,45,46,49,63,64,65,66,67,74,79,80,82,87,94,165,172,181,183,185,193,196,198,205,209,211,41],
  61: [6,7,8,9,13,56,57,58,61,68,69,70,71,86,150,151,166,167,170,201],
  62: [12,92,14,15,16,17,18,19,20,21,75,76,83,91,152,155,156,157,160,161,162,189,191,192,197],
  63: [73,34,139,59,22,24,25,26,27,28,138,30,48,32,72,62,77,78,93,31,159,164,186,187,204,206,208,29],
  64: [108,109,111,112,113,153,169,171,173,175,176,177,178,184,194,200,202,203,210],
  107: [84]
}

#Defines the amount of macca missions can reward in an area
MISSION_REWARD_AREA_MACCA_RANGES = {
    16: [120000, 180000],# 30k around The Compassionate Queen and duplicates
    35: [25000, 85000], #Same as Taito
    36: [22000, 25000], #Defeat the Demon King's Armies ,Chase Through Shakan
    38: [22000, 25000], #Same as above
    60: [25000, 85000],#Escort the Prime Minister ,To The Empyrean
    61: [2000, 7500], #Half of Shinagawa
    62: [4000, 15000], #Jojozi Temple, Eliminate Lahmu
    63: [6000, 22000], #Investigate Anomalies in Tokyo, Defeat the Demon King's Armies
    64: [6000, 22000], #Same as Chiyoda
    107: [666666,666666] #Return of True Demon
}

#Defines the amount of macca chest can contain in an area
CHEST_AREA_MACCA_RANGES = {
    16: [50000, 60000], #same as taito
    35: [50000, 60000], #same as taito
    36: [20000, 40000],
    38: [30000, 40000],
    60: [50000, 60000],
    61: [500, 2000],
    62: [5000, 10000], 
    63: [6000, 22000], 
    64: [10000, 20000], 
    107: [50000, 60000] #same as taito

}

#Odds that the first drop of an enemy is a lifestone
DROP1_LIFESTONE_ODDS = 0.97

#The area each basic enemy is balanced around
ENCOUNTER_LEVEL_AREAS = [61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61, #Minato 0 + 1-17
                            62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62, #Shinagawa 18 -37
                            63,63,63,63,63,63,63,63,63,63,63, #Chiyoda/Shinjuku #38 - 48
                            36,36,36,36, #Demon Kings Castle/Shakan 49 -52
                            60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60, #Taito 53 - 71
                            35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35] # Temple of Eternity 72 - 99

#Defines which shop slots unlock in which area
AREA_SHOP_UNLOCKS= {
    61: [0,2,5,12,13,14,15,16,17,20,21,22,23,24,25,26],
    62: [1,28],
    63: [6,7,8,9,10,11,18,29],
    60: [3,4,19],
    35: [27],
    16: [30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51], #Also includes godborn unlocks
}

#IDs of guest party members like Yoko
GUEST_IDS = [1150, 1151, 1152, 1153, 1154, 1157, 1158, 1159, 1161, 1162]

#IDs of guest party members excluding Yuzuru and Dazai who have glitchy animations for physical skills
GUEST_IDS_WORKING_ANIMS_ONLY = [1152, 1154, 1157, 1158, 1159, 1161]

#Event encounter IDs of Ishtar except one
EXTRA_ISHTAR_ENCOUNTERS = [76, 77, 78, 79, 80, 81, 82]
#Event encounter ID of Ishtar that is kept in the pool
TRUE_ISHTAR_ENCOUNTER = 75
#Demon ID of the Ishtar that is kept in the pool
TRUE_ISHTAR_DEMON = 455

#Event Encounter Ids of bosses that appear up until and including Hydra
EARLY_STORY_EVENT_ENCOUNTERS = [87, 134, 33] #Glasya-Labolas, 3 Pretas, Hydra

#Lilith, Tehom, and Mastema's music starts playing in a cutscene, so their track is set to 255 instead of their actual music
BOSS_TRACK_FIX_MAP = {
    155: 57,
    163: 66,
    164: 68
}

#IDs of enemy only healing skills that heal more than the player versions
ENEMY_HEALING_SKILL_IDS = [103, 104, 105, 106, 352, 353, 354, 355, 381, 382, 383, 384, 385, 386, 850, 852, 856, 887, 888]

#Skill ID of Lunation Flux which should be restricted more than other unique skills
LUNATION_FLUX_ID = 927

'''
Returns dictionary lining out to which reward are each shop slot belongs
'''
def getShopUnlockAreas():
    shopUnlockArea = {}
    for key in AREA_SHOP_UNLOCKS.keys():
        for value in AREA_SHOP_UNLOCKS[key]:
            shopUnlockArea[value] = key
    return shopUnlockArea

'''
Returns dictionary lining out to which reward are each mission belongs
'''
def getMissionRewardAreas():
    missionRewardArea = {}
    for key in REWARD_AREA_MISSIONS.keys():
        for value in REWARD_AREA_MISSIONS[key]:
            missionRewardArea[value] = key
    return missionRewardArea

def getMaccaValues ():
    return [0,10,13,15,16,17,18,20,21,23,24,26,28,29,31,33,34,36,38,40,41,44,46,49,51,55,58,61,65,68,71,74,78,82,87,90,94,98,103,107,111,116,121,126,131,137,142,147,153,159,164,170,177,184,190,198,204,212,218,225,233,241,249,257,264,273,281,290,298,307,315,356,374,415,456,542,629,758,887,1016,1145,1274,1403,1532,1661,1790,1919,2048,2177,2306,2435,2564,2693,2822,2951,3080,3209,3338,3467,3596]


def getExpValues():
    return [0,24,26,29,32,37,42,47,57,74,87,98,123,151,182,217,257,300,347,398,453,512,575,642,713,788,867,949,1035,1124,1216,1312,1427,1548,1675,1807,1946,2090,2241,2397,2559,2727,2901,3081,3267,3459,3657,3861,4071,4281,4500,4728,4856,4927,4997,5165,5334,5372,5410,5460,5509,5597,5672,5773,5821,5860,5933,6000,6058,6132,6172,6280,6326,6447,6568,6665,6762,6858,6954,7050,7146,7242,7338,7434,7530,7626,7722,7818,7914,8010,8106,8202,8298,8394,8490,8586,8682,8778,8874,8970]


def getBonusSkills():
    return [["Impaler's Revenge",510,90,90],['Intercalation',452,69,69],['Elusive Eclipse',451,52,52],['Rooted Soul',450,12,12],[ 'Moonlight Frost',255,83,83],[ 'Frenzy',283,15,15],[ 'Galvanic Slash',284,46,49],[ 'Sakanagi',292,25,25],[ 'Divine Arrowfall',293,41,41],[ 'Murakumo',294,67,67],[ 'Red Capote',295,24,24],[ 'Aramasa',298,8,8],[ 'Wrath Tempest',299,44,44],[ 'Ruinous Thunder',300,31,31],[ 'Thalassic Calamity',301,54,54],[ 'Kannabi Veil',306,36,36],[ 'Profaned Land',307,48,48],[ 'Miracle Water',310,17,17],[ 'Dreadful Gleam',312,52,52],[ 'Purgatorium',320,83,83],[ 'Impetus',321,83,83],[ 'Inferno of God',329,95,99],[ 'Hailstorm of God',330,95,99],[ 'Lightning of God',331,95,99],[ 'Tornado of God',332,95,99],[ 'Cold Dark Matter',333,90,99],[ 'Hot Dark Matter',334,95,99],[ 'Freikugel',335,95,99],[ 'Gaea Rage',336,95,99],[ 'Magma Axis',337,95,99],[ 'Javelin Rain',338,90,99],[ 'Xeros Beat',339,95,99],[ 'Deadly Fury',340,90,99],[ 'Wild Dance',341,95,99],[ 'Contempt of God',342,95,99],[ 'Freikugel',370,95,99],[ 'Javelin Rain',372,95,99],[ 'Deadly Fury',373,95,99],[ 'Evil Gleam',390,95,99],[ 'Sonic Boom',392,35,35],[ 'Gaea Rage',394,95,99],[ 'Chaotic Will',395,95,99],[ 'Javelin Rain',397,95,99],[ 'Deadly Fury',398,95,99],[ 'Abyssal Beckoning',861,84,84],[ 'Seething Mansemat',863,84,84],[ 'Untainted Wind',864,84,84],[ 'Boundless Sea',865,83,83],[ 'Bufu',902,8,8],[ 'Rakunda',903,8,8],[ 'Gram Slice',904,8,8],[ 'Charge',905,44,47],[ 'Bufula',906,44,47],[ 'Carnage Fang',908,44,47],[ "Sun's Radiance",909,44,47],[ 'Witness Me',910,44,47],[ 'Hama',911,8,8],[ 'Mahamaon',912,44,44],[ 'Mirage Shot',913,44,44],[ 'Zanma',914,44,44],[ 'Trafuri',915,44,44],[ 'Cautious Cheer',916,44,44],[ 'Toxic Cloud',917,44,44],[ 'Paraselene Blur',918,80,80],[ 'Evergreen Dance',921,51,51],[ 'Inflaming Divinity',922,28,28],[ 'Heavenly Ikuyumi',923,72,72],[ 'Moonlight Frost',924,52,52],[ 'Lunar Hurricane',925,69,69],[ 'Luminescent Mirage',926,80,80],[ 'Lunation Flux',927,69,69]]
