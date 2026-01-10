from enum import Enum
from base_classes.demon_assets import Position 
import math

RACE_ARRAY = ["None", "Unused", "Herald", "Megami", "Avian", "Divine", "Yoma", "Vile", "Raptor", "Unused9", "Deity", "Wargod", "Avatar", "Holy", "Genma", "Element", "Mitama", "Fairy", "Beast", "Jirae", "Fiend", "Jaki", "Wilder", "Fury", "Lady", "Dragon", "Kishin", "Kunitsu", "Femme", "Brute", "Fallen", "Night", "Snake", "Tyrant", "Drake", "Haunt", "Foul", "Chaos", "Devil", "Meta", "Nahobino", "Proto-fiend", "Matter", "Panagia", "Enigma", "UMA", "Qadistu", "Human", "Primal", "Void"]

PROTOFIEND_IDS = [1101,1102,1103,1104,1105,1106,1107,1108,1109,1110,1111,1112,1113,1114,1115,1116,1117,1118]

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
#Unused demon id used to temporarily store data
COPYOVER_DEMON = 1149

#List of demons with a name that cannot be accessed by the player
INACCESSIBLE_DEMONS = [71,364] #Old Lilith, Tao

NORMAL_ENEMY_COUNT = 396

BAD_IDS = [71, 365, 364, 366] #Old Lilith, Tao x2, Yoko

TOTAL_DEMON_COUNT = 1201

SPECIAL_FUSION_COUNT = 62
#Races that cannot be downfused with an element
NO_DOWNFUSE_RACES = ["Enigma","Fiend","UMA","Qadistu","Devil","Primal","","Chaos","Human","Panagia"]

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

#List of chests that are not used in the game
UNUSED_CHESTS = [
    #Credit to CTOBN: https://docs.google.com/spreadsheets/d/1MOWJL29_geEw5w7X2gTmNBx_bQiKnb4xVMxY2nI34PY/edit?gid=1095877054#gid=1095877054 
    3859, 3860, 3861, 3862, 3863, 3864, 3865, 3866, 3867, 3868,
    3869, 3870, 3871, 3872, 3873, 3874, 3875, 3876, 3877, 3878,
    3879, 3880, 3881, 3882, 3883, 3884, 3885, 3886, 3887, 3888,
    3889, 3890, 3891, 3892, 3893, 3894, 3895, 3896, 3897, 3898,
    3899, 3900, 3901, 3902, 3903, 3904, 3905, 3906, 3907, 3908,
    3909, 3910, 3911, 3912, 3913, 3914, 3915, 3916, 3917, 3918,
    3919, 3920, 3921, 3922, 3923, 3924,
    3927, 3928, 3929, 3930, 3931, 3932, 3933, 3934, 3935, 3936,
    3937, 3938, 3939, 3940, 3941, 3942, 3943, 3944, 3945, 3946,
    3947, 3948, 3949, 3950, 3951, 3952,
    0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19,
    38, 59, 68, 80, 106, 107, 131, 183, 208, 227, 230, 248, 264, 361, 407, 428,
    511, 512, 513, 514, 515, 516, 517, 518, 519, 520,
    530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540,
    547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580,
    612, 613, 614, 615, 616, 617, 618, 619, 620,
    635, 636, 637, 638, 639, 640,
    654, 655, 656, 657, 658, 659, 660,
    743, 744, 745, 746, 747, 748, 749, 750,
    766, 767, 768, 769, 770,
    784, 785, 786, 787, 788, 789, 790,
    793, 794, 795, 796, 797, 798, 799, 800,
    # These are technically not unused, but contain quest related key-items that we dont wanna mess with currently
    76,77, 78, 79, 142, 231, 232, 233, 254
]
#The very first chest is unfortunately missable
MISSABLE_CHESTS = [29]

CHEST_MACCA_MIN = 500
CHEST_MACCA_MAX = 60000
#Chance of a chest containing macca instead of an item/essence
CHEST_MACCA_ODDS = 0.035
CHEST_RELIC_ODDS = 0.00347
#Chance of a chest containing an essence instead of an item
CHEST_ESSENCE_ODDS = 0.42
#Map of Areas that need to duplicate their rewards to another area
AREA_MIRRORS = {
    63: 64, 64: 63, #Chiyoda / Shinjuku
    36: 38, 38: 36, #Demon Kings Castle / Shakan
}

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

#Based on Vending machines for now
RELIC_MAP_SCALING = {
    60: [634, 643, 617, 635, 636, 651, 637, 638, 639, 655, 652, 647, 623, 653], #['Hologram Trading Card', 'Vinyl Umbrella', 'Soda', 'Time Capsule', 'Balloon Value Pack', 'Sealed Magazine', 'Antique Shirt', 'Game Console with Handle', 'Mysterious Mummy', 'Golden Triangle', 'Cardboard Cap Bottle', 'Rubber Duck', 'Can of Jelly', 'Marble Bottle'], 
    61: [616, 640, 644, 617, 648, 652, 618, 619, 620, 621, 653, 642, 623, 635, 643, 629], #['Fortune', 'Black Tape Set', 'Powder Box', 'Soda', 'Old Newspaper', 'Cardboard Cap Bottle', 'Melted Doll', 'Cloth Mask', 'Cartridge Game Console', 'Shabby Building Material', 'Marble Bottle', 'High-Capacity Bottle', 'Can of Jelly', 'Time Capsule', 'Vinyl Umbrella', 'Can of Oden']
    62: [622, 653, 652, 623, 624, 625, 626, 627, 617, 645, 649, 648, 650, 641], #['Hexagram Trading Card', 'Marble Bottle', 'Cardboard Cap Bottle', 'Can of Jelly', 'Anime Paperweight', 'Simple Undershirt', 'Segata III Game Console', 'Mouse Mummy', 'Soda', 'Bottle Container', 'Old Magazine', 'Old Newspaper', 'Novel', 'Ripped Manga'],
    63: [628, 617, 629, 630, 631, 646, 632, 623, 633, 642, 654, 616], #['Telephone Card', 'Soda', 'Can of Oden', 'Electronic Music Box', 'School Swimsuit', 'Radio-yaki', 'Tablet Game Console', 'Can of Jelly', 'Crow Mummy', 'High-Capacity Bottle', 'Maid Costume', 'Fortune'], 
    64: [856, 617, 857, 861, 865, 862, 623, 858, 642, 859, 866, 860, 648, 864, 863, 649, 616, 644], # 64: ['Soup Can', 'Soda', 'Dry Cell Battery', 'Crowned Bottle', 'Western Game Console', 'Chipped Decoration', 'Can of Jelly', 'Disposable Camera', 'High-Capacity Bottle', 'Mini Cartridge', 'Monstrous Mummy', "Traveler's Check", 'Old Newspaper', 'Dazzling Dress', 'Floral Painting', 'Old Magazine', 'Fortune', 'Powder Box']
    16: [634, 643, 617, 635, 636, 651, 637, 638, 639, 655, 652, 647, 623, 653], #Copy of Taito 60
    35: [634, 643, 617, 635, 636, 651, 637, 638, 639, 655, 652, 647, 623, 653], #Copy of Taito 60
    36: [628, 617, 629, 630, 631, 646, 632, 623, 633, 642, 654, 616], #Copy of Chiyoda 63
    38: [856, 617, 857, 861, 865, 862, 623, 858, 642, 859, 866, 860, 648, 864, 863, 649, 616, 644], #Copy of Shinjuku 64
    107: [634, 643, 617, 635, 636, 651, 637, 638, 639, 655, 652, 647, 623, 653], #Copy of Taito 60
    960: [634, 643, 617, 635, 636, 651, 637, 638, 639, 655, 652, 647, 623, 653], #Copy of Taito 60
}

VENDING_MACHINE_RELIC_QUANTITY_WEIGHTS = {
    1: 284, 
    2: 29, 
    3: 11,
    4: 8,  
    5: 12, 
    6: 6,
    7: 5, 
    8: 5,
    12: 8, 
    24: 4,
}
#This Vending Machine is missable because it only activates later after you are well past it making it unlikely that players will pick it up
MISSABLE_VENDING_MACHINE = [50]

#The number of different consumable items (including some DUMMY items), from indices 0-113
CONSUMABLE_ITEM_COUNT = 114

#Any chest with an item index 657 or higher contains a key item and should not be randomized
KEY_ITEM_CUTOFF = 657

#Item indices that correspond to reusable items like the return pillar or gleam grenade and spyglass(spyscope is given by tutorial daemon)
BANNED_ITEMS = [70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 55]

BANNED_ESSENCES = [359,555,545,546,547,548,549,550,551,552,553,554,556,557,558,559,606,607,608] #Old Lilith's Essence, Demi-fiends Essence, Aogami & Tsukuyomi Essences
#TODO: We need a way to keep track of demi-fiend essence if demi-fiend is swapped but not resistance randomized


#Chance that a miman reward is an essence
MIMAN_ESSENCE_ODDS = 0.27272727
MIMAN_RELIC_ODDS = 0.005 #Completely made up
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

#Map of key item ids and in which areas they are only allowed in
KEY_ITEM_AREA_RESTRICTIONS = {
    658: [60,61,62,63,64,36,38], #Key of Austerity
    659: [60,61,62,63,64,36,38], #Key of Benevolence
    660: [60,61,62,63,64,36,38], #Key of Harmony

}

# Names belonging to areas
AREA_NAMES = {
  16: 'Empyrean',
  35: 'TempleOfEternity',
  36: 'DemonKingsCastle',
  38: 'Shakan',
  60: 'Taito',
  61: 'Minato',
  62: 'Shinagawa',
  63: 'Chiyoda',
  64: 'Shinjuku',
  107: 'DemiFiend Area',
  960: 'Taito Post KeyLock'
}

#Chance a mission rewards macca
MISSION_MACCA_ODDS= 0.1717
#Chance a mission rewards an essence instead of an consumable item
MISSION_ESSENCE_ODDS= 0.09090
#Chance a mission rewards rewards a relic
MISSION_RELIC_ODDS = 0.013
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
  218: [219], #Guardian of Light CoC And CoV
}

#Missions that cannot receive macca as a reward
MACCALESS_MISSIONS = [
    72, #Falcon's Head cannot get macca as reward due to being synced with Additional reward in CoV Rescue Miyazu Atsuta
    58,59,62,64,65,66,67 #Missions whose reward can be gained repeatedly and cannot be macca due to repeat being given via event
]

#List of exclusive key item rewards from both canons #TODO: what even is the purpose here?? for potential exclusive progression items
CREATION_EXCLUSIVE_KEY_REWARDS = [] #Currently not any
VENGEANCE_EXCLUSIVE_KEY_REWARDS = [] #Currently not any

#List of banned key rewards
BANNED_KEY_REWARDS = [79] #Spyscope (dropped by tutorial daemon)

#Exclusive mission from both canons to give potential exclusive rewards to (excluding missions whose rewards are not randomized or are not allowed to receive key item rewards)
CREATION_EXLUSIVE_MISSIONS = [72,40,42,26,25,30,22,24,27,204,206,187,93,-7,-8,-9-10,169,77,78] #The Falcon's Head, Egyptians Fate, Succesion of Ra, Path to Myojin Forest, One Mokois Trash,
        #He of a Hundred Hands, Hellfire Highway, Search for Oyamatsumi, Glitter in Ginza, Netherworld Relay Racing, Will of the Samurai, Trial of the Seven Stars, Defeat the Demon Kings Armies, The One I (Still) Love
        #Keeper of South/North/West/East Secondary Rewards, Black Frost Strikes Back/Sobering Standoff
VENGEANCE_EXLUSIVE_MISSIONS = [157,152,159,177,171,194,203,178,202,184,200,210,172,211,193,174,188,190,108,109,110,111,112,113,176,175] #Supply Run, Guide to the Lost, Heart of Garnet, As God Wills, A Self of my Own, Devotion To Order, Part-time Gasser, A Star is Born
        #Disgraced Bird God, Alice's Wonderland, Shinjuku Jewel Hunt, Heroes of Heaven and Earth, Rite of Resurrection, 'God of Old, Devourer of Kin', The Heartbroken, Special Training: Army of Chaos
        #The Serpent King, The Great Adversary, Investigate the Anomalies in Tokyo, Investigate the Salt Incidents, Rescue Miyazu Atsuta, Investigate Jozoji Temple, Qadištu Showdown
        #Vampire in Black/Hunter in White

#Mutually exclusive missions (or timed availability missions) that should never reward a key item 
MUTUALLY_EXCLUSIVE_MISSIONS = [
    176,175,#Vampire in Black/Hunter in White
    70,71, #The Water Nymph/Spirit of Love
    79,80, #Raid on Tokyo/In Defense of Tokyo
    77,78, #Black Frost Strikes Back/Sobering Standoff
    138,139, #Reclaim/Liberate the Golden Stool (Have duplicates but not needed here)
    75,76, #Those Seeking Sanctuary, Holding the Line
    51,50, #The Red Dragon's Invitation/The Seraphs Return
    -2, -3, #Additional Rewards from The Red Dragon's Invitation/The Seraphs Return
    156, #Prince of her Dream (Missable)
    157, #Supply Run (Missable)
    162, #In Pursuit of Knowledge (Missable according to the Wiki)
    192, #Infiltrate the Demon Feast (Missable)
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
LARGE_SYMBOL_NORMAL_DEMONS = [77,80,94,127,212,283] #Mara, Surt, Huang Long, Chimera, Oyamatsumi, Thunderbird
#List of demons with huge models with normal scaling, that should use smaller scaling instead
LARGE_MODEL_NORMAL_DEMONS = {
    87: 0.7, #King Frost
    115: 0.5, #Hydra (Currently has no symbol param data)
    565: 0.3, #Tiamat
    525: 0.4, #Abdiel Nahobino
    520: 0.4, #Nuwa Nahobino
    435: 0.5, #Hydra (boss)
}
#List of demons that should be added to the MapSymbolParamTable for the sake of collision calculation and which demons encount collision they should use
ADD_LARGE_MODEL_DEMONS = {
    #TODO: Check implications for punishing replacements/ normal enemies like Hydra
    565: 832, #Tiamat (Abaddon)
    525: 832, #Abdiel Nahobino  (Abaddon)
    520: 826, #Nuwa Nahobino  (Oyamatsumi)
    435: 812, #Hydra (boss) (Chimera)
    115: 812, #Hydra (Normal) (Chimera)
    441: 855 ,# Lahmu Mask (Zhuque Collision)

    -617: 20, #Koshimizu (Anahita Collision)
    561: 20, #Yuzuru (Anahita Collision)
    240: 8, #Abdiel (Zeus Collision)
    264: 8, #Abdiel Fallen(Zeus Collision)
    7: 20, #Khonsu (Anahita Collision)
    15: 8, #Khonsu Ra (Zeus Collision)
    31: 27, #Artemis (Parvati Collision)
    934: 20, #Demi-fiend (Anahita Collision)
    41: 20, #Anansi (Anahita Collision)
    386: 27, #Onyankopon (Parvati Collision)
    250: 20, #Mastema (Anahita Collision)
    118: 16, #Samael (Vishnu Collision)
    38: 27, #Amanozako (Parvati Collision)
    237: 8, #Saturnus (Zeus Collision)
    75: 20, #Nuwa (Anahita Collision)
    465: 20, #Yakumo (Anahita Collision)
    227: 16, #Masakado (Vishnu Collision)
    876: 27, #Amanozako Rage(Parvati Collision)
    40: 20, #Kresnik (Anahita Collision)
    394: 576, #Eisheth (Agrat Copy Collision)
    393: 576, #Naamah (Agrat Copy Collision)
    392: 576, #Agrat (Agrat Copy Collision)
    391: 576, #Lilith (Agrat Copy Collision)
    529: 855, #Lucifer (Phase 1) (Zhuque Collision)
    236: 855, #Lahmu (Zhuque Collision))
    197: 16, #Snake Nuwa (Vishnu Collision)
    32: 576, #Konohana Sakuya (Agrat Copy Collision)
    597: 812, #Tehom (Chimera)
    1: 8, #Satan (Demon) (Zeus Collision)
    2: 8, #Lucifer (Demon) (Zeus Collision)
    175: 27, #Turbo Granny (Parvati Collision)
    99: 16, #Vritra (Vishnu Collision)
    4: 8, #Dagda (Zeus Collision)
    142: 352, #Glasya-Labolas (Black Rider Collision)
    528 : 8, #Tsukuyomi (Zeus Collision)
    454 : 80, #Surt Boss (Surt)
    385: 576, #Kinmamon (Agrat Copy Collision)
    207:16, #Marici (Vishnu Collision)
    387: 59, #Amabie (pixie collision)
    381: 345, #Hare of Inaba (Preta Collision)
    60: 58, #Nahobeeho (Jack Frost)
    100: 59, #Nyami Nyami (pixie collision)
    122: 20, #Xiezhai (Anahita Collision)
    226: 27, #Nezha Taishi (Parvati Collision)
    251 :254, #Armaiti (Throne Collision)
    275 :16, #Azazel (Vishnu Collision)

}
#List of demons that should be removed to the MapSymbolParamTable after collision calculation is done
REMOVE_TEMP_MODEL_DEMONS = [-617,561,240,7,15,31,934,41,386,250,118,38,237,75,465,227,876,40,394,393,392,391,529,236,197,32,597,1,175,99,4,142,
                            528,454,385,207,387,381,60,100,122,226,2,251,275,264]

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
  960: CONSUMABLE_PROGRESSION[0] + CONSUMABLE_PROGRESSION[1] + CONSUMABLE_PROGRESSION[3] + CONSUMABLE_PROGRESSION[4] + [13], #Taito Post Keys: Ambrosia,
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
  960: [52,71], #Taito Post Keys
}

#Defines the missions that are scaled on the area
REWARD_AREA_MISSIONS = {
  16: [47,52,53,54,55,188,190,51,50,222,221],
  35: [81,95,116],
  36: [212,114,174],
  38: [212,114,174],
  60: [33,35,36,37,38,39,40,42,43,44,46,49,63,64,65,66,67,79,80,82,87,94,165,172,181,183,185,193,196,198,205,209,211,41,218,219,143],
  61: [6,7,8,9,13,56,57,58,61,68,69,70,71,86,150,151,166,167,170,201],
  62: [12,92,14,15,16,17,18,19,20,21,75,76,83,91,106,152,155,156,157,160,161,162,189,191,192,197],
  63: [73,34,139,59,22,24,25,26,27,28,138,30,48,32,72,62,77,78,93,31,159,164,186,187,204,206,208,29],
  64: [108,109,111,112,113,140,141,142,145,146,147,148,153,169,171,173,175,176,177,178,179,180,184,194,200,202,203,210],
  107: [84,144],
  960: [45,74], #The Holy Ring, Destined Leader (Post Taito KeyLock)
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
    107: [666666,666666], #Return of True Demon
    960: [25000, 85000],#Escort the Prime Minister ,To The Empyrean
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
    107: [50000, 60000], #same as taito
    960: [50000, 60000],

}
#Combined maps for macca reward ranges
COMBINED_MACCA_AREA_RANGES = {
    "mission": MISSION_REWARD_AREA_MACCA_RANGES,
    "chest": CHEST_AREA_MACCA_RANGES,
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
#TODO: Decide if we should try to keep track of Yuzuru/Dazai but since you can just give them normal phys skills via fusion seems unnecessary
GUEST_IDS_WORKING_ANIMS_ONLY = [1152, 1154, 1157, 1158, 1159, 1161]

#Guests and special demons and which ids they additionally occupy
GUEST_GROUPS = {
    1150: [1153,1162], #Yuzuru Atsuta
    1151: [], # Ichiro Dazai
    1152: [1154], #Tao Isonokami
    1157: [1158,1159], #Yoko Hiromine
    365: [], #Tao (Panagia)
    366: [], #Yoko (Panagia)
}

GUEST_DEMIFIEND = 1161

#Event encounter IDs of Ishtar except one
EXTRA_ISHTAR_ENCOUNTERS = [76, 77, 78, 79, 80, 81, 82]
#Event encounter ID of Ishtar that is kept in the pool
TRUE_ISHTAR_ENCOUNTER = 75
#Demon ID of the Ishtar that is kept in the pool
TRUE_ISHTAR_DEMON = 455

#Demon and EventEncounter IDs of the Maras both punishing and virtual trainer
PUNISHING_MARA_DEMON = 892
PUNISHING_MARA_ENCOUNTER = 240
VIRTUAL_MARA_DEMON = 893
VIRTUAL_MARA_ENCOUNTER = 45

#Event Encounter Ids of bosses that appear up until and including Hydra
EARLY_STORY_EVENT_ENCOUNTERS = [135, 134, 33] #Glasya-Labolas, 3 Pretas, Hydra

#Lilith, Tehom, and Mastema's music starts playing in a cutscene, so their track is set to 255 instead of their actual music
BOSS_TRACK_FIX_MAP = {
    155: 57,
    163: 66,
    164: 68
}
EARLY_BOSS_LEVEL_LIMIT = 16 #Hydra+1
PHYS_IMMUNE_BOSSES = [630,827,626,928,890,828,932,621] #Siegfried(Abcess),Giri,Rangda,Mother Harlot,Gogmagog,Arahabaki,Mephisto,Slime(Abcess)

#IDs of enemy only healing skills that heal more than the player versions
ENEMY_HEALING_SKILL_IDS = [103, 104, 105, 106, 352, 353, 354, 355, 381, 382, 383, 384, 385, 386, 850, 852, 856, 887, 888,
                            890 #Healing Part of Qadistu Entropy Boss Version
]

#Skill ID of Lunation Flux which should be restricted more than other unique skills
LUNATION_FLUX_ID = 927

#Mission ID of Brawny Ambitions II for skill condition
BRAWNY_AMBITIONS_ID = 197
BRAWNY_AMBITIONS2_SKILL = "Puncture Punch"

#List of which demon join is in which script
SCRIPT_JOIN_DEMONS = {
    'MM_M061_EM1630': 305, # Leanan Sidhe
    'MM_M061_EM1640': 43, # Apsaras
    'MM_M062_EM1660': 257, # Principality
    'MM_M062_EM1650': 67, # Lilim
    'MM_M060_EM1690': 265, # Adramelech
    'MM_M060_EM1700': 201, # Futsunushi
    'MM_M063_EM1670': 72, # Black Frost
    'MM_M063_EM1680': 183, # Dionysus
    'MM_M064_EM2310': 41, # Anansi
    'MM_M064_EM2320': 386, # Onyankopon
    'MM_M064_EM2270': 40, # Kresnik
    'MM_M064_EM2280': 346, # Kudlak
    'MM_M060_EM1420': 35, # Fionn
    'MM_M060_EM1602': 38, # Amanozako (Amanazako Could't Join Initially)
    'MM_M060_EM1601': 38, # Amanozako
    'MM_M016_E0885': 152, #Hayataro CoC Chaos 
    'MM_M016_E0885_Direct': 152, #Hayataro CoC Chaos 
    'MM_M016_EM1450': 19, # Demeter
    'MM_M035_EM1480': 242, # Michael
    'MM_M036_EM1490': 83, # Belial
    'MM_M061_EM1781': 295, # Cleopatra
    'MM_M061_EM1782': 295, # Cleopatra
    'MM_M061_EM2613_HitAction': 4, # Dagda
    'MM_M030_EM1769': 78, # Mephisto (Can only join this way)
    'MM_M061_EM1791': 31, # Artemis
    'MM_M061_EM2601': 32, # Konohana Sakuya
    'MM_M063_EM2170': 227, # Masakado
    'MM_M061_EM2705': 207, # Marici
}

#List of Magatsuhi Skills tied to race (and Critical)
MAGATSUHI_SKILLS = [60,76,78,87,109,110,111,112,113,114,#Omagatoki: Critical, Big Bang, Freikugel EX, Soul Drain, Twilight Wave, Eternal Prayer, Sea of Stars, Waters of Youth, Accursed Poison, Rasetsu Feast
                    120,121,130,131,138,145,146,147,177,#Fairy Banquet, Expand:Criical Aura, Expand: Piercing Aura, Shield of God, Impaler's Glory, Dekajaon, Omagatoki: Pierce, Omagatoki: Hit, Omgatoki: Adversity
                    187,193,201,215,249,274,309,345,928,#Omagatoki: Free, Omagatoki: Doubler, Omagatoki:Dance, Omagatoki: Sincerity, Omagatoki: Savage, Omagatoki: Luck, Omagatoki: Potential, Omagatoki: Charge, Omagtoki: Succession
                    801,802,803,804,805,806,807,808,809,#Feline Fury, Immolating Breath, Frost Storm, Calamitious Thunder, Raging Whirlwind, Holy Wrath, Diabolical Deluge, Harvest Festival, Omagatoki: Exploit
                    810,811,812,813,814,815,816,817,818,#Oni Formation, Four Heavenly Edicts, Fairies' Game, Bouncy Body, Guardian Angels, Omagatoki:Bounty, Dana's Wisdom, Waves of Order, Rains of Order
                    819,820,821,822,823,824,825,826,857 #Wellspring of Order, Tides of Chaos, Torrent of Chaos, Fountain of Chaos, Omagatoki:Momentum, Omagatoki: Conserve, Omagatoki: Strategize, Qadistu Entropy, Blossoming Sakura
                    ]

#Enemy Versions of Magatsuhi Skills
MAGATSUHI_ENEMY_VARIANTS = {131:842,138:843,76:934,78:935,87:936,109:937,110:938, #Shield of God, Impaler's Glory, Big Bang, Freikugel EX, Sould Drain, Twilight Wave, Eternal Prayer
                            112:939,113:940,114:941,120:942,121:943,138:944,145:945} #Waters of Youth, Accursed Poison, Rasetsu Feast, Fairy Banquet, Shield of God, Impaler's Glory, Dekajaon

#Lists level ranges for magatsuhi skills that are not the standard 1 to 99
MAGATSUHI_SKILLS_LEVEL_RESTRICTIONS = {
    76: [16,99], #Big Bang (Drake Talisman is gotten via The Ultimate Omelete which has Recommended Level 16)
    78: [6,99], #Freikugel EX (Wargod Talisman via No Stone Unturned with Recommended level 6)
    87: [32,99], #Soul Drain (Night Talisman via Kumbhanda's Bottle with Recommended Level 32)
    109: [3,99], #Twilight Wave (Haunt Talisman via A Preate Predicament with Recommended Level 3)
    110: [50,99], #Eternal Prayer (Megami Talisman via The Horn of Plenty with Recommended Level 50)
    111: [28,99], #Sea of Stars (Divine Talisman from Angel after Loup-garou/Eisheth which are level 28)
    112: [30,99], #Waters of Youth (Enigma Talisman via Song of Nostalgia with Recommended Level 30)
    113: [16,99], #Accursed Poison (Raptor Talisman via Movin' on Up with Recommended Level 16)
    114: [20,99], #Rasetsu Feast (Jaki Talisman from Rakshasa on Diet Building after Eligor who is level 20)
    120: [34,99], #Fairy Banquet (Fairy Talisman via The Root of the Problem with Recommended Level 34)
    121: [18,99], #Expand:Critical Aura (Brute Talisman via Talisman Hunt with Recommended Level 18)
    130: [73,99], #Expand: Piercing Aura (Fury Talisman via The Destined Leader with Recommended Level 73)
    131: [73,99], #Shield of God (Herald Talisman via The Holy Ring with Recommended Level 73)
    138: [25,99], #Impaler's Glory (Vile Talisman via Magic from the East with Recommended Level 25)
    145: [50,99], #Dekajaon (Kunitsu Talisman via Kunitsu Quest with Recommended Level 50)
    146: [32,99], #Omgatoki: Pierce (Kishin Talisman via 90 Miman which requires at least beating Fionn who is level 32)
    147: [20,99], #Omagtoki: Hit (Avatar Talisman via 45 Miman which requires at least beating Eligor who is level 20)
    177: [26,99], #Omagatoki: Adversity (Beast Talisman via A Wish for a Fish with Recommended Level 26)
    187: [17,99], #Omagatoki: Free (Femme Talisman via The Demon of the Spring with Recommended Level 17)
    193: [16,99], #Omagtoki: Doubler (Fallen Talisman via To Cure a Curse with Recommended Level 16)
    201: [46,99], #Omagatoki: Dance (Snake Talisman via Yurlungur who can only be accessed in Chiyoda after beating Yakumo who is level 46)
    215: [17,99], #Omagatoki: Sincerity (Jirae Talisman via Chakra Drop Chomp with Recommended Level 17)
    249: [71,99], #Omagatoki: Savage (Tyrant Talisman via The Winged Sun with Recommeded Level 71)
    274: [9,99], #Omagatoki: Luck (Level of lowest level Element demon)
    309: [11,99], #Omagatoki: Potential (Yoma Talisman via Pollution Panic with Recommended Level 11)
    345: [69,99], #Omagatoki: Charge (Deity Talisman via The Bull God's Lineage with Recommended Level 69)
    801: [34,99], #Feline Fury (Nekomata is highest level demon required, 34)
    802: [64,99], #Immolating Breath (Cerberus is highest level demon required, 64)
    803: [44,99], #Frost Storm (Black Frost is highest level demon required)
    804: [61,99], #Calamitious Thunder (Periapt via Rascal of the Norse with Recommended Level 61)
    805: [55,99], #Raging Whirlwind (Scathach is highest level demon required)
    806: [80,99], #Holy Wrath (Periapt via The Seraph's Return with Recommended level 80)
    807: [80,99], #Diaobolical Deluge (Periapt via The Red Dragon's Invitation with Recommended level 80)
    808: [82,99], #Harvest Festival (Periapt via A Plot Revealed with Recommended level 82)
    809: [38,99], #Omagatoki: Exploit (Periapt via The Golden Dragon's Arrival with Recommded level 48)
    810: [75,99], #Oni Formation (Ongyo-Ki is highest level demon required
    811: [64,99], #Four Heavenly Edicts (Additional Reward of Keeper of the North with Recommended level 64)
    812: [18,99], #Faerie's Game (High Pixie is highest level demon required)
    813: [33,99], #Bouncy Body (Black Ooze is highest level demon required)
    814: [29,99], #Guardian Angels (after Eligor who is level 20)
    815: [95,99], #Omagatoki: Bounty (Metatron is highest level demon required)
    816: [75,99], #Dana's Wisdom (Periapt via Holy Will and Profane Dissent with recommended level 75)
    817: [31,99], #Waves of Order (Periapt via Tough Love with recommended level 31)
    818: [16,99], #Rains of Order (Periapt via In Pursuit of Knowledge with recommended level 16)
    819: [9,99], #Wellspring of Order (Periapt via Brawny Ambitions with recommended level 9)
    820: [21,99], #Tides of Chaos (Periapt via Training:Minato with recommeded level 21)
    821: [11,99], #Torrent of Chaos (Periapt via Knocking on Death's Door with recommended level 11)
    822: [17,99], #Fountain of Chaos (Periapt via Home Sweet Home with recommeded level 17)
    823: [17,99], #Omagatoki: Momentum (Periapt via Beastly Battle of Wits with recommeded level 17)
    824: [21,99], #Omgatoki: Conserve (Periapt via Essential Research with recommended level 21)
    825: [17,99], #Omagatoki: Strategize (Periapt via Pixie on the Case with recommended level 17)
    826: [52,99], #Qadistu Entropy (52 is level of Lilith Boss in CoV, you get Periapt after)
    857: [47,99], #Blossoming Sakura (Periapt via Sakura Cinders of the East with recommended level 47
    928: [52,99] #Omnipotent Succession (52 is level of Lilith Boss in CoV, you get Talisman after)
}

SKILL_STAT_PENALTY_MULTIPLIER = 0.8 #Penalty applied to weight in skill rando if stat used to attack is lower than other attacking stat
POTENTIAL_WEIGHT_MULITPLIER = 10 #Multiplier applied to potential to update weight of skill rando
MAGATSUHI_SKILL_WEIGHT = 60 #Base weight of magatsuhi skills if included in skill rando
SKILL_WEIGHT = 100 #Base weight for all skills in skill rando
SKILL_APPEARANCE_PENALTY_MULTIPLIER = 0.5 #Weight penalty for skills if the skill has already been assigned in process in an attempt to diversify skill sets
#FORCE_SKILL_MULTIPLIER = 100 #Multiplier to ensure all skills are assigned to at least one enemy
LEVEL_SKILL_WEIGHT_MULTIPLIER = 175 #Multiplier for a skill that is in the level range

DIVERSE_RESIST_FACTOR = 2
ELEMENT_RESIST_NAMES = ["fire","ice","elec","force","light","dark"]
AILMENT_NAMES = ["poison","confusion","charm","sleep","seal","mirage"]
SIMPLE_RESIST_VALUES = [-1.5,-1,0,0.5,1,1.5] #1.5 is here despite weaknesses only having a 1.25 damage multiplier, but this way it exactly counteroffsets a resistance. Drain=-1.5, Repel=-1
#What the simple resist values correspond to as actual values in gamedata
SIMPLE_RESIST_RESULTS = {
    -1.5: 1000,
    -1: 999,
    0 : 0,
    0.5 : 50,
    1 : 100,
    1.5: 125 
}
# Boss ailments can have different resist values than just normal resist
SIMPLE_BOSS_AILMENT_RESIST_RESULTS = {
    0 : 0,
    0.1 : 10,
    0.2 : 20,
    0.4 : 40,
    0.5 : 50,
    1 : 100,
    1.5: 125 
}

#These distributions are calculated for ranges of level with CEIL(LEVEL / 10)
PHYS_RESIST_DISTRIBUTION = [
    [1,3,5,20,246,4], #TOTAL Distribution
    [0,0,0,0,16,0],
    [0,0,0,1,29,0],
    [0,0,0,2,29,0],
    [0,0,0,2,34,1],
    [0,0,0,3,35,1],
    [0,0,0,4,32,0],
    [1,3,2,1,27,1],
    [0,0,1,3,23,0],
    [0,0,2,1,15,1],
    [0,0,0,3,6,0], 
]
# Fire, Ice, Elec, Force
FIEF_RESIST_DISTRIBUTION = [
    [7,5,32,31,141,65], #TOTAL Distribution
    [0,0,1,3,7,6],
    [0,0,2,4,17,9],
    [1,0,4,3,19,7],
    [1,0,5,4,19,9],
    [1,1,7,4,21,8],
    [1,1,5,2,21,9],
    [2,1,3,5,16,10],
    [1,2,4,5,12,5], 
    [1,1,3,2,9,4],
    [1,1,1,3,3,1],
]
# Light, Dark
LD_RESIST_DISTRIBUTION = [
    [5,6,54,47,124,45], #TOTAL Distribution
    [0,0,1,2,10,4],
    [0,0,3,4,20,4],
    [0,0,5,5,15,7],
    [1,0,6,7,18,7],
    [0,1,7,6,20,7],
    [1,0,9,6,16,5],
    [1,1,7,9,12,6],
    [2,2,7,5,9,4],
    [0,2,8,4,4,2],
    [1,1,4,2,2,1], 
]
AILMENT_RESIST_DISTRIBUTION = [
    [0,0,12.33333333,21,229.8333333,15.83333333], #TOTAL Distributio
    [0,0,0.3333333333,0.6666666667,14.5,0.5],
    [0,0,0.3333333333,2.666666667,25.33333333,1.666666667],
    [0,0,0.8333333333,3.166666667,24.16666667,2.833333333],
    [0,0,1,2.166666667,32,1.833333333],
    [0,0,2.166666667,2.5,31,3.333333333],
    [0,0,1.166666667,5,28.33333333,1.5],
    [0,0,1.333333333,2.5,29.16666667,2],
    [0,0,2.5,1.166666667,21.5,1.833333333],
    [0,0,1.5,1,16.5,0],
    [0,0,1.166666667,0.1666666667,7.333333333,0.3333333333],
    ]

BOSS_PHYS_RESIST_DISTRIBUTION = [
    [1,4,5,32,273,8],
    [0,0,0,0,5,0],
    [0,0,0,3,34,1],
    [0,0,0,4,22,1],
    [0,0,0,2,28,0],
    [0,1,1,4,59,2],
    [0,0,0,4,25,0],
    [1,2,1,0,24,0],
    [0,0,1,5,32,1],
    [0,1,0,3,26,3],
    [0,0,2,7,18,0],

]

BOSS_FIEF_RESIST_DISTRIBUTION = [
    [0,0,1,1,3,2],
    [0.25,0,3.25,4.25,20,10.25],
    [0.75,0.25,2,3,15.75,5.25],
    [0.25,0,4.5,3.25,15.25,6.75],
    [1,1.25,8,8.25,34,14.5],
    [0.5,0.75,3.5,3,16,5.25],
    [0.5,0.25,3.75,3.25,12.75,7.5],
    [1.25,1,5.5,7.5,16.75,7],
    [2.5,1,2.75,4.25,16,4.75],
    [1,0,3.25,2.25,12,8.5],
    [8,4.5,37,39.25,160.75,71.75],
]

BOSS_LD_RESIST_DISTRIBUTION = [
    [3,4,30,26,69,29],
    [0,0,0,0,1.5,1],
    [0,0,0.5,3.5,10,5],
    [0,0,1,2.5,5,5],
    [0,0,1.5,2,7.5,4],
    [0,0.5,6,4,18.5,4.5],
    [0,1,4,3,3.5,3],
    [0.5,0,5,3.5,4,1],
    [2,2,7,3,4,1.5],
    [0,0.5,2.5,2,9.5,1.5],
    [0.5,0,2.5,2.5,5.5,2.5], 
]

BOSS_AILMENT_RESIST_DISTRIBUTION = [
#0         ,0.1         ,0.2        ,0.4         ,0.5       ,1           ,1.5
[35.33333333,0.6666666667,51.16666667,161.6666667,7.333333333,48.33333333,18.33333333],
[0.1666666667,0,0,0.8333333333,0.1666666667,3.666666667,0],
[1.5,0,1.166666667,4.166666667,3.666666667,24.5,3],
[3.666666667,0,4.666666667,7.333333333,1,8.5,1.833333333],
[3.5,0,4.833333333,16.83333333,1.166666667,3,0.6666666667],
[4.333333333,0.1666666667,10.33333333,41.83333333,0.5,5.166666667,4.666666667],
[1.333333333,0.3333333333,5.5,20,0,0,1.833333333],
[1,0,1.666666667,22.33333333,0,0,3],
[3.333333333,0,8.5,24.66666667,0.6666666667,0,1.833333333],
[12.66666667,0,10.83333333,9,0,0,0.5],
[3.833333333,0.1666666667,3.666666667,14.66666667,0.1666666667,3.5,1],

]

#Skills that grant element resistance and their value
RESIST_SKILLS = {
    401	: ["physical",50], #	Resist Phys
    402	: ["physical",0], #	Null Phys
    403	: ["physical",1000], #	Drain Phys
    404	: ["physical",999], #	Repel Phys
    405	: ["fire",50], #	Resist Fire
    406	: ["fire",0], #	Null Fire
    407	: ["fire",1000], #	Drain Fire
    408	: ["fire",999], #	Repel Fire
    409	: ["ice",50], #	Resist Ice
    410	: ["ice",0], #	Null Ice
    411	: ["ice",1000], #	Drain Ice
    412	: ["ice",999], #	Repel Ice
    413	: ["elec",50], #	Resist Elec
    414	: ["elec",0], #	Null Elec
    415	: ["elec",1000], #	Drain Elec
    416	: ["elec",999], #	Repel Elec
    417	: ["force",50], #	Resist Force
    418	: ["force",0], #	Null Force
    419	: ["force",1000], #	Drain Force
    420	: ["force",999], #	Repel Force
    421	: ["dark",50], #	Resist Dark
    422	: ["dark",0], #	Null Dark
    423	: ["dark",1000], #	Drain Dark
    424	: ["dark",999], #	Repel Dark
    425	: ["light",50], #	Resist Light
    426	: ["light",0], #	Null Light
    427	: ["light",1000], #	Drain Light
    428	: ["light",999], #	Repel Light
}

#Source Wiki, some values made up
OFFENSIVE_POTENTIAL_COST_MULTIPLIERS = {
    -9: 1.6,-8: 1.5,-7: 1.46,-6: 1.4,
    -5: 1.34,-4: 1.25,-3: 1.16,-2: 1.13,-1: 1.1,
    0: 1,1: 0.9,2: 0.87,3: 0.84, 4: 0.81,5: 0.75,
    6: 0.72,7: 0.69, 8: 0.66,9: 0.6,
}
NON_OFFENSIVE_POTENTIAL_COST_MULTIPLIERS = {
    -5: 1.6,-4: 1.5,-3: 1.4,-2: 1.3,-1: 1.15,
    0: 1,1: 0.85,2: 0.8,3: 0.75, 4: 0.7,5: 0.6,
}

#Maps boss versions of demons with few voice lines to their normal counterparts so missing lines can be filled in for the voice randomizer
VOICE_MAP_DEMON_ALTS = {
    39: 38, #Amanozako
    432: 431, #Hydra
    455: 98, #Tiamat -> Ananta
    460: 607, #Tehom -> Yoko
    502: 80, #Surt
    504: 84, #Abaddon
    505: 85, #Moloch
    506: 86, #Belphegor
    507: 94, #Huang Long
    508: 127, #Chimera
    509: 211, #Arahabaki
    510: 212, #Oyamatsumi
    511: 237, #Girimekhala
    512: 283, #Thunderbird
    513: 322, #Hecatoncheires
    514: 87, #King Frost
    515: 72, #Black Frost
    516: 77, #Mara
    517: 291, #Gurulu
    518: 337, #Gogmagog
    519: 142, #Glasya Labolas
}

#Key: Normal navigator demon ID, Value: Boss demon ID to find the replacement for when changing the navigator demons
NAVIGATOR_BOSS_MAP = {
    77: 892, #Mara
    356: 923, #Hell Biker
    295: 931 #Cleopatra
}

MIN_NAVI_SIZE = 60 #Sets the bounds on navigator hitboxes
MAX_NAVI_SIZE = 175

GIANT_DEMON_MODELS = [565] #List of demon models that need to be shrunk extra as navigators
GIANT_MODEL_SCALE_FACTOR = 2.5
BASE_NAVI_MODEL_SCALE_FACTOR = 1.2 #Model size to normalize to before calculating hitboxes

CONTEMPT_OF_GOD_ID = 342 

#Skills that have that are physical but not technically StrBased as a skill type
PHYSICAL_RATE_SKILLS = [170,69] #Power Punch, Beatdown

#Enemy only (and Nahobino) skills that don't have a skill rank and what they should use as their skill rank for the boss skill randomization
ENEMY_SKILL_RANKS = {
    255 : 32, #Moonlight Frost (Same As Gaea Rage 450 Power Pierce)
    283: 6, #Frenzy (Weaker than Heat Wave which is 7)
    284 : 16, #Galavanic Slash (More Accurate Storm Dracostrike which is 15)
    292: 21, #Sakanagi (Mortal Jihad has +20 BP, but isn't Almighty and is 20)
    293: 21, #Divine Arrowfall (Megidola is 20 and - 10 BP)
    294 : 30, #Murakumo (Akashic Arts is 29)
    295 : 9, #Enemy Red Capote (Player is 6, Cautious Cheer is 9)
    298: 5, #Aramasa (Heat Wave is 7, Multi-Hits are below weaker AOEs)
    299: 22, #Wrath Tempest (Hades Blast is 23)
    300: 16, #Ruinous Thunder (Ziodyne is +15BP and 18)
    301: 29, #Thalassic Calamity (Glacial Blast is 27, and -10BP -1MinHit)
    306: 13, #Kannabi Veil (Elemental Blocks are 12)
    307: 22, #Profaned Land (Mudobarion is +25BP and 24)
    310: 6, #Miracle Water (Media is 8 with +10BP but -7%MHP)
    315: 10, #Toxic Breath (Mamudo is 8, with -15 BP)
    320: 30, #Purgatorium (Trisagion is -10BP and 27, but not AOE)
    321: 26, #Impetus (Hades Blast is -30BP and 23)
    329: 29, #Inferno of God (Maragidyne is 26 and - 35 BP)
    330: 29, #Hailstorm of God (Maragidyne is 26 and - 35 BP)
    331: 29, #Lightning of God (Maragidyne is 26 and - 35 BP)
    332: 29, #Tornado of God (Maragidyne is 26 and - 35 BP)
    333: 9, #Cold Dark Matter (Harvest Dance is a Heal only 2 ranks and target choosing and tier 8)
    334: 14, #Hot Dark Matter (King of Tales has Taunt + only 2 ranks + target choosing => 17)
    335: 30, #Freikugel (Lucifer) (Player ones are 29)
    336: 26, #Gaea Rage(Lucifer) (Hades Blast is -30BP and 23)
    337: 30, #Magma Axis (Ragnarok is 27, and -10BP -1MinHit and -3MaxHit)
    338: 22, #Javelin Rain (Lucifer) (Hades Blast is +30BP and 23)
    339: 22, #Xeros Beat (Hades Blast is +30BP and 23)
    340: 30, #Deadly Fury (Akashich is same BP on crit and 29)
    341: 18, #Wild Dance (Tentarafoo is 15 with -35%, Capitulate is 20 with same% but ATK down)
    343: 29, #Holy Crucifixion (Untainted Wind is attack AOE at 30, Decidial is 28 but only Acc/Eva)
    372: 29, #Javelin Rain (Demi-fiend) (Tandava is -30BP almighty rank 30)
    373: 27, #Deadly Fury (Demi-fiend) (Catastrophe is 25, -200% Crit + 90BP)
    374: 31, #Chaotic Will (31 is highest)
    390: 17, #Evil Gleam(Sexy Dance is 15 with -20%)
    392: 17, #Sonic Boom (Mazandyne is +15BP rank 21)
    394: 30, #Gaea Rage (270BP, Pierce)
    395: 31, #Chaotic Will (31 is highest)
    397: 29, #Javelin Rain (Tandava is -30BP almighty rank 30)
    398: 27, #Deadly Fury (Catastrophe is 25, -200% Crit + 90BP)
    848: 8, #Freikugel (Masakado) (Gram Slice is +48BP and not almighty and is 5)
    849: 6, #Recalcitrant Execution (Masakado) (Bestial Bite is +38BP and not almighty and is 3)
    861: 28, #Abyssal Beckoning (Energy Drain is -40BP -150%HP no Sleep and Rank 24)
    865: 30, #Boundless Sea (Ice Age is 29 and not AOE)
    883: 6, #Ice Shard (Mabufu is 6)
    884: 8, #Light Shard (Mahama is 8)
    885: 14, #Sleep Gem (Lullaby is 14)
    902: 1, #Bufu (Yuzuru)
    903: 5, #Rakunda (Yuzuru)
    904: 5, #Gram Slice (Yuzuru)
    905: 6, #Charge (Yuzuru)
    906: 8, #Bufula (Yuzuru)
    908: 14, #Carnage Fang (Yuzuru)
    911: 4, #Hama (Yuzuru)
    912: 17, #Mahamaon (Dazai)
    913: 6, #Mirage Shot (Dazai)
    914: 8, #Zanma (Dazai)
    916: 9, #Cautious Cheer (Dazai)
    917: 14, #Toxic Cloud (Dazai)
    918: 31, #Parasalene Blur (31 cause they can always use it)
    919: 31, #Megido Ark (Player) (450 BP if my math is right)
    930: 32, #Megido Ark (Boss) (450 BP if my math is right + potential bonus?)
    922: 20, #Inflaming Divinity (Sakuya Sakura is 19, but has heal and aoe but only +1)
    923: 17, #Heavenly Ikuyumi (Babylon Curse is 17)
    924: 31, #Moonlight Frost (Player)
    925: 16, #Lunar Hurricane (Wind Dracostrike is 15)
    926: 19, #Luminescent Mirage (Tetrakarn is 16)
    342: 30, #Contempt of God 
    842: 26, #Shield of God(Enemy) (Kannabi Veil * 2)
    843: 27, #Impaler's Glory(Enemy) (Impaler's Animus +5)
    934: 31, #Big Bang (Enemy) 
    935: 32, #Freikugel EX (Enemy) 
    936: 31, #Soul Drain(Enemy)
    937: 31, #Twilight Wave (Enemy)
    940: 31, #Accursed Poison (Enemy)
    941: 28, #Rasetsu Feast (Enemy) (Debilitate +5)
    942: 28, #Fairy Banquet (Enemy) (Luster +5)
    943: 26, #Shield of God(Enemy) (Kannabi Veil * 2)
    944: 27, #Impaler's Glory(Enemy) (Impaler's Animus +5)
    945: 21, #Dekajaon (Dekaja/Dekunda +5)
    103: 1, #Dia (Enemy (Agathion,Kodama))
    104: 12, #Diarama (Enemy (Amanozako))) 
    277: 25, #Matriarchs Love (Enemy (Danu))
    353: 11, #Diarama (Enemy (Camael, Tsukuyomi, Okuninushi, Principality))
    354: 12, #Media (Enemy (Okuninushi)) (Media +4)
    355: 19, #Mediarama (Enemy (Kushinada, Tiamat)) 
    381: 15, #Dia (Enemy (Abcess Pixie)) (+3 Normal Diarama)
    382: 19, #Diarama (Enemy (Dominion, Power)) (same rank as Diarahan)
    384: 20, #Mediarama (Enemy (Ananta, Throne)) (High % Heal, same Rank as Light of Order/Golden Apple)
    385: 13, #Dia (Enemy (Demi-fiend Pixie)) (+1 Normal Diarama)
    386: 22, #Diarama (Enemy (Camael, Ishtar, Khonsu)) 
    850: 25, #Diarama (Enemy (Masakado, Mastema)) 
    852: 23, #Mediarama (Enemy (Samael))
    888: 15, #Diamrita (Enemy (Agrat))
}   
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

def calculateResistBase(x):
    #trendline for average resist/weak sum with phys counting 1.5 times
    return -0.0414*x + 9.21

def calculateTotalResistBase(x):
    #trendline for average resist/weak sum with phys counting 1.5 times and ailments counting half
    return -0.0449*x + 12.2

def getEnemyOnlySkills():
    return [["Impaler's Revenge",510,90,90],
            [ 'Moonlight Frost',255,83,83],
            [ 'Frenzy',283,15,15],
            [ 'Galvanic Slash',284,46,49],
            [ 'Red Capote',295,25,25], #+1 so it does not roll on the same demon as often when skills are scaled
            [ 'Dreadful Gleam',312,52,52],
            [ 'Purgatorium',320,83,83],
            [ 'Impetus',321,83,83],
            [ 'Inferno of God',329,95,99],
            [ 'Hailstorm of God',330,95,99],
            [ 'Lightning of God',331,95,99],
            [ 'Tornado of God',332,95,99],
            [ 'Cold Dark Matter',333,90,99],
            [ 'Hot Dark Matter',334,95,99],
            [ 'Freikugel',335,95,99],
            [ 'Gaea Rage',336,95,99],
            [ 'Magma Axis',337,95,99],
            [ 'Javelin Rain',338,90,99],
            [ 'Xeros Beat',339,95,99],
            [ 'Deadly Fury',340,90,99],
            [ 'Wild Dance',341,95,99],
            [ 'Contempt of God',342,95,99],
            [ 'Freikugel',370,95,99],
            [ 'Sonic Boom',392,35,35],
            [ 'Evil Gleam',390,95,99],
            [ 'Abyssal Beckoning',861,84,84],
            [ 'Seething Mansemat',863,84,84],
            [ 'Untainted Wind',864,84,84],
            [ 'Boundless Sea',865,83,83],
            [ 'Holy Crucifixion',343,95,99],
            ]

def getBonusSkills():
    return [
            [ 'Intercalation',452,69,69],
            [ 'Elusive Eclipse',451,52,52],
            [ 'Rooted Soul',450,12,12],
            [ 'Sakanagi',292,25,25],
            [ 'Divine Arrowfall',293,41,41],
            [ 'Murakumo',294,67,67],
            [ 'Aramasa',298,8,8],
            [ 'Wrath Tempest',299,44,44],
            [ 'Ruinous Thunder',300,31,31],
            [ 'Thalassic Calamity',301,54,54],
            [ 'Kannabi Veil',306,36,36],
            [ 'Profaned Land',307,48,48],
            [ 'Miracle Water',310,17,17],
            [ 'Javelin Rain',372,95,99],
            [ 'Deadly Fury',373,95,99],
            [ 'Gaea Rage',394,95,99],
            [ 'Chaotic Will',395,95,99],    
            [ 'Bufu',902,8,8],
            [ 'Rakunda',903,8,8],
            [ 'Gram Slice',904,8,8],
            [ 'Charge',905,44,47],
            [ 'Bufula',906,44,47],
            [ 'Carnage Fang',908,44,47],
            [ "Sun's Radiance",909,44,47],
            [ 'Witness Me',910,44,47],
            [ 'Hama',911,8,8],
            [ 'Mahamaon',912,44,44],
            [ 'Mirage Shot',913,44,44],
            [ 'Zanma',914,44,44],
            [ 'Trafuri',915,44,44],
            [ 'Cautious Cheer',916,44,44],
            [ 'Toxic Cloud',917,44,44],
            [ 'Paraselene Blur',918,80,80],
            [ 'Evergreen Dance',921,51,51],
            [ 'Inflaming Divinity',922,28,28],
            [ 'Heavenly Ikuyumi',923,72,72],
            [ 'Moonlight Frost',924,52,52],
            [ 'Lunar Hurricane',925,69,69],
            [ 'Luminescent Mirage',926,80,80],
            [ 'Lunation Flux',927,69,69],
            [ 'Gaea Rage',830,95,99]
        ]


def getAnimationFixOnlySkills():
    return [
        [ 'Revival Chant',311,61,61] #Revival Chant can only be used by non-nahobino with the animation fix (though then functions as a revive swap for demons/npcs)
    ]

'''
Compares two values of resistances.
    Parameters:
        a(Number): first value to compare
        b (Number): second value to compare
    Returns 0 if the values are the same, 1 if resistance a is weaker than b, else -1
'''
def compareResistValues(a, b):
    values = list(SIMPLE_RESIST_RESULTS.values())

    aIndex = values.index(a)
    bIndex = values.index(b)

    if aIndex == bIndex:
        return 0
    elif aIndex > bIndex:
        return 1
    else:
        return -1


class Canon(Enum):
    CREATION = 0
    VENGEANCE = 1
    