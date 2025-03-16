from base_classes.encounters import Encounter, Event_Encounter, Mixed_Boss_Encounter
from util import numbers, translation, paths
from base_classes.settings import Settings
from base_classes.base import Translated_Value
import math
import copy
import random
import pandas as pd

#Stores the distribution of resist in the boss resistance process
TOTAL_BOSS_RESIST_MAP = {}
#Stores resist profiles of all bosses
resistProfiles = []
#Filled with ids of bosses and which comp demon they represent
BOSS_PLAYER_MAP = {}
#Encounter IDs that should not be randomized
BANNED_BOSSES = [0, 7, 32, #Dummy Abbadon, Tutorial Pixie, Tutorial Daemon
                 #33, #Hydra (game hangs when supposed to lose limbs)
                 #57, 58, 59, 60, 63, 64, 65, #School dungeon fights with overlapping demons(Temp)
                 #129, 159, 160, #Mananangal/Incubus overlap with school(Temp), Zhens in gasser sidequest that overlap with each other(Temp)
                 139,#Unused Lahmu II (presumably planned as Vengeance phase 2)
                 141, #Dummy Eisheth
                 #232, 233, 234, 235, 236, 237 #Area 3 Powers that overlap with each other(Temp)
                 ] 

#Boss IDs that summon other enemies
BOSS_SUMMONS = {
    519: [517, 518],    #Khonsu Ra - Anubis and Thoth
    845: [871, 872, 873, 874, 875], #Shiva - Ganesha, Kali, Dakini, Ananta and Parvati
    934: [940, 941, 942, 943, 944, 945, 946], #Demi-Fiend - Cerberus, Jack Frost, Pixie, Thor, Girimekhala, Parvati, Cu Chulainn
    529: [531, 532, 533], #Lucifer True Ending - Brimstone Star, Cocytus Star, Morning Star
    537: [538, 539], #Lucifer Normal Endings - Brimstone Star, Cocytus Star
    839: [846, 847, 848, 849], #Huang Long - Qing Long, Zhuque, Baihu, Xuanwu
    828: [850, 851, 852, 853], #Arahabaki - Sui-Ki, Kin-Ki, Fuu-Ki, Ongyo-Ki
    760: [761, 762, 764, 766], #Samael - Lilith's Shadow, Agrat's Shadow, Eisheth's Shadow, Naamah's Shadow
    569: [570, 572, 574], #Lilith - Agrat, Eisheth, Naamah
    473: [474, 475], #Alilat - Flauros, Ose
    681: [682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693], #Satan - Arahabaki, Titania, Sarasvati, Yatagarasu, Ganesha, Kumphanda, Fafnir, Mada, Sraosha, Hariti, Kaiwan, Macabre
    463: [464], #Arioch - Decarabia
    924: [935], #White Rider - Dominion
    925: [936], #Red Rider - Power
    926: [937,939], #Black Rider - Legion (Seems to use 2 different legions with the same stats/skills but different AIs)
    927: [938], #Pale Rider - Loa
    843: [885,886,887], #Danu - Mandrake, Jack Frost, Jack O'Lantern
    783: [784,785,786], #Marici - Conquering Mirage, Stitching Mirage, Warding Mirage
}

#Boss IDs (first in the encounter) with multiple enemies of equal strength
PARTNER_BOSSES = [433, #Eligor(Andras)
    442, 443, 444, 445, 446, 447, 448, 449, #All enemies during the school dungeon
    463, 471, 481, 485, 554, 561, 567,  #Arioch(Decarabias), Melchizedeks, Zeus(Odin), Dominion(Power), Naamah(GL), Yuzuru(Hayataro), Yakumo(Nuwa)
    577, 579, 602, 752, 772, #Fallen Abdiel(Dazai), Isis(Lamias), Makamis(Feng Huangs), Nozuchi(Kodamas), Kudlak(Black Oozes) 
    779, 814, 822, 829, 836, 866, 868, #Norn(Dis), Camael(Powers), Okuninushi(Kunitsu), Asura(Mithras), Gabriel(Uriel/Raphael), Leannan(Ippon), Apsaras(Agathions)
    605, 608, 612, 614, 618, 627, 621, 623, 721, 724, 726, 730 #Abscess bosses
]

#Boss IDs (first in the encounter) with a single strong enemy and multiple weaker enemies
MINION_BOSSES = [452, 473, 519, 520, 525, #Lahmu(Tentacles), Alilat(Flauros/Ose), Khonsu Ra(Anubis/Thoth), Nuwa Nahobino(Thunder Bits), Abdiel Nahobino(Depraved arm/wing),
                 529, 537, 556, 565, 569, 681, #True Lucifer(Stars), Lucifer(Stars), Lahmu again(Tentacles), Tiamat(Heads), Lilith(Qadistu), Satan(Arahabaki/Friends),
                 760, 776, 816, 839, 843, 845, #Samael(Shadows), Atavaka(Rakshasa), Moloch(Orobos/Flauros), Huang Long(Holy Beasts), Danu(Mandrake), Shiva(Ananta/Friends),
                 877, 924, 925, 926, 927, 934] #Zaou-Gongen(Kurama), All Four Riders(Call X), Demi-Fiend(Pixie/Friends)

#For bosses that can die and be resummoned (Hayataro etc), there's a second copy of the demon that needs to match stats with the original
REVIVED_DEMON_DUPLICATE_MAP = {
    528: [530, 540], #Tsukuyomi
    562: [563], #Hayataro
    570: [571], #Agrat
    572: [573], #Eisheth
    574: [575], #Naamah
    762: [763], #Agrat's Shadow
    764: [765], #Eisheth's Shadow
    766: [767]  #Naamah's Shadow
}

#Phase 1, 2, and 3 of Lucifer need to have their HP and stats synced (Phase 3 has triple the HP of the others)
LUCIFER_PHASES = [529, 534, 535]

#HP Penalty for single target bosses/bonus for multi-target bosses to account for AOE skills
GROUP_HP_MODIFIER = 0.85

#Event Encounter IDs that contain Lucifer (normal and true version), excluding VR battle duplicates
LUCIFER_ENCOUNTERS = [6, 12]

#Event Encounter IDs that contain superbosses (Shiva x2, Demi-Fiend x2, Satan x2, Masakado x3)
SUPERBOSS_ENCOUNTERS = [46, 88, 89,121, 48, 157, 168, 169, 53]

#Event Encounter IDs that contain minibosses, including some weaker quest bosses
MINIBOSS_ENCOUNTERS = [13, 14, 15, #Empyrean angels
                       29, 30, 36, 54, 55,    #Belial, Michael, Pazuzu, Initial Lahmu and demons before him
                       56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,129, #School fights
                       84, 97, 98, 102, 103, 104, 105, #Shiki-Ouji, Leanan, Apsaras, Principality, Lilim, Dionysus, BFrost
                       106, 107, 132, 133, 134, 144, 145, #Futsunushi, Adramelech, 6 Pretas, Oni, 3 Pretas, Dormarth, Nozuchi
                       147, 158, 159, 160, 170, 172, 173, 174, 175, #Pisaca, Zhen*3, Yakshini, Onyakopon, Anansi, Kudlak, Kresnik
                       232, 233, 234, 235, 242, 248] #Power*4, Isis, Dominion

BOSS_HP_MODIFIERS = {
    435: 0.5, #Snake Nuwa's replacement should have half HP
    529: 3 #True Lucifer's replacement will have triple HP (not completely accurate but fine for now)
}

#Event Encounter IDs that break when moving to a normal array because of too many demons (Lahmu) or event flags
EVENT_ONLY_BOSSES = [6, 39, 69, 138]

#Event Encounter IDs that have DUMMY fights and can be replaced with probelematic demons like True Lucifer
DUMMY_EVENT_ENCOUNTERS = [0,139,141]

# Map of bosses who summon a set number of minions at a time, used to calculate total press turns
PRESS_TURN_MAX_SUMMONS = {
    934: 3, # Demi-Fiend
    681: 3, # Satan
    760: 2, # Samael
    845: 3, # Shiva
    828: 1, # Arahabaki
    839: 2, # Huang Long
    843: 2, # Danu
}

# Map of boss summons that are summoned in groups of more than one, like Arioch's 2 decarabias
SUMMONED_DEMON_COUNTS = {
    464: 2, # Decarabia
    935: 2, # Rider summons (Except Legions from Black Rider)
    936: 2,
    938: 2,
    885: 2, # Mandrake
}

#Bosses whose resistances are not randomized and who need non special sum for checkSum calc
STANDARD_RESIST_BOSSES = [758,757,597] #Masakado (Both), Tehom
#Bosses who have stronger weaknesses than normal
STRONG_WEAKNESS_BOSSES = [940,941,942,943,944,945]#Demifiend Summons (Cerberus946,Jack Frost, Pixie,Girimekhala,Thor,Parvati)
#Resistances for Lucifer phase 2 since lucifer phase handling does not calculate this, so do it once by hand
LUCIFER_PHASE_2_RESIST_TOTALS = [5.5, 0]

#Symbol Id in the Encounter Table for Illusion Agrat
ILLUSION_AGRAT_SYMBOL = 1862
#Encounter ID for Illusion Agrat
ILLUSION_AGRAT_ENCOUNTER = 2629

#Map of bosses with healing skills and which one instead shows up in their AI scripts
HEALING_BOSS_MAP = {
    822: { #Okuninushi
       354 : 383, #Media
    },
    814: { #Camael
       353 : 386, #Diarama
    },
    876: { #Amanozako
       104 : 386, #Diarama
    },
}

#Map of bosses and which skills are missing in their skill list but they can still use
MISSING_SKILLS_IN_LIST = {
    861: [ #Koumokuten (4 Turn)
        75, #Megidoloan
        127, #Dekaja
    ],
    862: [ #Jikokuten (4 Turn)
        127, #Dekaja
    ],
    863: [ #Bishamonten (4 Turn)
        137, #Dekunda
    ],
    519: [ #Khonsu Ra 
        323, #Wait for Mesekteths Path??
    ],
    520: [ #Nuwa (Nahobino)
        359,360,361,362, #Rising Storm Dragon (Variants)
        285 #Electrify (Variant)
    ],
    528: [ #Tsukuyomi
        324, #Wait for Tsukuyomi?
        136, #Debilitate
        386, #Diarama Variant
    ],
    452: [ #Lahmu (Tentacles CoC?)
        287, #Attack (AOE?)
    ],
    455: [#Ishtar
        137, #Dekunda
        313, #Dreadful Gleam (Does Nothing)
    ],
    561: [#Yuzuru Atsuta
        136, #Debilitate (Is an Initial Value (unlikely to be used))
    ],
    565: [ #Tiamat
        866, #Annihilation Ray
        867, #Annihilation Ray (Not working)
        933, #Magatsuhi Harvest (Special)
    ],
    567: [#Shohei Yakumo (CoV)
        151, #Do Nothing
    ],
    550: [#Nuwa (CoV)
        151, #Do Nothing
    ],
    569: [#Lilith
        151, #Do Nothing
        889, #Qadistu Entropy
        907, #Failed Qadistu Entropy
        933, #Magatsuhi Harvest (Special)
    ],
    570: [#Agrat (lilith)
        151, #Do Nothing
        889, #Qadistu Entropy
        907, #Failed Qadistu Entropy
    ],
    572: [#Eisheth
        151, #Do Nothing
        889, #Qadistu Entropy
        907, #Failed Qadistu Entropy
    ],
    574: [#Naamah
        151, #Do Nothing
        889, #Qadistu Entropy
        907, #Failed Qadistu Entropy
    ],
    577: [#Abdiel (Dazai)
        151, #Do Nothing
    ],
    578: [#Dazai
        151, #Do Nothing
    ],
    597: [#Tehom
        75, #Megidoloan
        127, #Dekaja
        137, #Dekunda
        859, #Tehom Wait
        862, #Inception of Chaos
        933, #Magatsuhi Harvest
    ],
    947: [#Dagda
        77, #Freikugel
    ],
    681: [#Satan #TODO: Sync with Minions
        7, # Agibarion
        12, # Maragibarion
        22, # Bufubarion
        27, # Mabufubarion
        37, # Ziobarion
        42, # Maziobarion
        52, # Zanbarion
        57, # Mazanbarion
        63, # Mudobarion
        66, # Mamudobarion
        69, # Hamabarion
        72, # Mahamabarion
        75, # Megidolaon
        77, # Freikugel
        81, # Energy Drain
        82, # Slumber Vortex
        89, # Pulinpa
        91, # Marin Karin
        93, # Makajama
        194, # Figment Slash
        211, # Yabusame Shot
        250, # Toxic Spray
        933, # Magatsuhi Harvest (Special)
    ],
    826: [#Oyamatsumi (Punishing)
        153, #Wait and see
    ],
    576: [#Agrat (Illusion)
        143, #Concentrate
        888, #Diamrita
    ],
    596: [#Mastema
        126, #Luster Candy
        850, #Diarama
    ],
    529: [#Lucifer (True P1)
        127, #Dekaja
        137, #Dekunda
        69, #Hamabarion
        63, #Mudobarion 
    ],
    529: [#Lucifer (False)
        127, #Dekaja
        137, #Dekunda
        69, #Hamabarion
        63, #Mudobarion 
    ],
    932: [#Mephisto
        127, #Dekaja
    ],
    758: [#Masakado
        244, #Black Dracostrike
        245, #White Dracostrike
        179, #Ice Dracostrike
        180, #Storm Dracostrike
        181, #Wind Dracostrike
    ],
    757: [#Masakado
        244, #Black Dracostrike
        245, #White Dracostrike
        179, #Ice Dracostrike
        180, #Storm Dracostrike
        181, #Wind Dracostrike
    ],
}

class Boss_Metadata(object):
    def __init__(self, demons, id):
        self.ind = id
        self.summons = [] #List(number)
        self.totalHP = 0
        self.totalEXP = 0
        self.totalMacca = 0
        self.resistTotals = {} #Holds the resistance sums of demons in the encounter
        self.hpShares = {} #Holds the relative amount of the total HP each demon has 
        self.demons = demons #List(number)
        if demons[0] in BOSS_SUMMONS.keys():
            self.summons = BOSS_SUMMONS[demons[0]]
        self.partnerType = demons[0] in PARTNER_BOSSES
        self.minionType = demons[0] in MINION_BOSSES
        self.countPerDemon = {} #Holds the number of times each demon appears in the encounter
        for demon in self.getAllDemonsInEncounter():
            if demon in self.countPerDemon.keys():
                self.countPerDemon[demon] = self.countPerDemon[demon] + 1
            elif demon in SUMMONED_DEMON_COUNTS.keys():
                self.countPerDemon[demon] = SUMMONED_DEMON_COUNTS[demon]
            else:
                self.countPerDemon[demon] = 1
                
    '''
    Calculates the HP value, EXP total, and Macca total that will be used to balance a new encounter.
    If the boss is a single strong demon with minions, it returns the strong demon's HP, otherwise it sums the HP of all demons in the encounter
    The EXP and Macca totals are the sum of all the demons in the encounter's exp and macca
    '''
    def calculateTotals(self, demonReferenceArr):
        self.totalHP = 0
        self.totalEXP = 0
        self.totalMacca = 0
        self.resistTotals = {}
        for demon, count in self.countPerDemon.items():
            if demon == 0:
                continue
            self.totalHP += demonReferenceArr[demon].stats.HP * count
            self.totalEXP += demonReferenceArr[demon].experience * count
            self.totalMacca += demonReferenceArr[demon].money * count

            resistTotalSubDict = calculateResistTotals(demon,demonReferenceArr[demon])
            self.resistTotals.update(resistTotalSubDict)
        if self.minionType:
            self.totalHP = demonReferenceArr[self.demons[0]].stats.HP * self.countPerDemon[self.demons[0]]
        self.hpPercents = {}
        for demon, count in self.countPerDemon.items():
            if demon == 0:
                continue
            self.hpPercents[demon] = demonReferenceArr[demon].stats.HP * count / self.totalHP

    '''
    Returns a List of demon IDs that are present in the encounter in order whether at the start or through a summon
    '''
    def getAllDemonsInEncounter(self):
        allDemons = []
        for demon in self.demons:
            if demon > 0:
                allDemons.append(demon)
        allDemons = allDemons + self.summons
        return allDemons
    
    '''
    Returns a List of demon IDs that are present in the encounter in order whether at the start or through a summon
    '''
    def getAllUniqueDemonsInEncounter(self):
        uniqueDemons = []
        for demon in self.getAllDemonsInEncounter():
            if demon not in uniqueDemons:
                uniqueDemons.append(demon)
        return uniqueDemons
    
    '''
    Returns the total number of notable demons in the encounter for the purpose of calculating a HP bonus/penalty  
    '''
    def getCountOfDemonsExcludingMinions(self):
        if self.minionType:
            return self.countPerDemon[self.demons[0]]
        totalCount = 0
        for demon, count in self.countPerDemon.items():
            if demon == 0:
                continue
            totalCount += count
        return totalCount

'''
Balances the stats of boss demons, including summoned adds to their new location
    Parameters:
        oldEncounter (List(number)): The original demons at the check
        newEncounter (List(number)): The demons replacing the old encounter
        demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
        bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
        oldEncounterID(Number): id of the old encounter
        newEncounterID(Number): id of the new encounter
        configSettings (Settings): settings of the current rando run
        compendium (List(Compendium_Demon)): list of compendium demons
        playerBossArr (List(Compendium_Demon)): list of compendium version of bosses and other demons
        skillReplacementMap (Dict): map of bosses and their skills and replacement skills
'''
def balanceBossEncounter(oldEncounter, newEncounter, demonReferenceArr, bossArr, oldEncounterID, newEncounterID, configSettings, compendium, playerBossArr, skillReplacementMap):
    balanceInstakillRates = configSettings.scaleBossInstakillRates
    
    oldEncounterData = Boss_Metadata(oldEncounter,oldEncounterID)
    newEncounterData = Boss_Metadata(newEncounter,newEncounterID)
    oldEncounterData.calculateTotals(demonReferenceArr)
    newEncounterData.calculateTotals(demonReferenceArr)

    #Halve HP of Snake Nuwa and Tehom Check
    if oldEncounterID in [35, 163]:
        oldEncounterData.totalHP = oldEncounterData.totalHP // 2
    #Double HP if  Tehom is Replacement
    if newEncounterID in [163]:
        oldEncounterData.totalHP = oldEncounterData.totalHP * 2
        
    #Times 7 HP of Tentacle Lahmu checks due to tentacles being the majority of his health
    if oldEncounterID in [69, 138]:
        oldEncounterData.totalHP = oldEncounterData.totalHP * 7
    #If Tentacle Lahmu is replacement, only give him a seventh of the normal HP due to tentacle jank
    if newEncounterID in [69, 138]:
        oldEncounterData.totalHP = oldEncounterData.totalHP // 7

    #Divide Maria's hp by 3 because she spams diarahan
    if newEncounterID == 31:
        oldEncounterData.totalHP = oldEncounterData.totalHP // 3
        
    adjustBossPressTurns(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, configSettings.scaleBossPressTurnsToCheck, configSettings.bossPressTurnChance)    
        
    if balanceInstakillRates:
        adjustInstakillRatesToCheck(oldEncounterData, newEncounterData, demonReferenceArr, bossArr)
    
    if oldEncounterData.minionType and newEncounterData.minionType:
        balanceMinionToMinion(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, configSettings, compendium, playerBossArr, skillReplacementMap)
    elif oldEncounterData.partnerType and newEncounterData.partnerType:
        balancePartnerToPartner(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, configSettings, compendium, playerBossArr, skillReplacementMap)
    else:
        balanceMismatchedBossEncounter(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, configSettings, compendium, playerBossArr, skillReplacementMap)

'''
Balances two boss encoutners that don't meet any special cases like both having minions
The first demon will give the entirity of the old encounter's exp and macca
If the new encounter is a strong demon with minions, the main demon will get the full HP tool while minions retain their original HP ratio.
Otherwise the HP pool will be split with demons that appear multiple times in the new encounter receiving a smaller share.
If the old encounter has multiple 'strong' demons, stats for new demons will be taken from a random demon, otherwise they will be taken from the main demon in the old encounter
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
            configSettings (Settings): settings of the current rando run
            compendium (List(Compendium_Demon)): list of compendium demons
            playerBossArr (List(Compendium_Demon)): list of compendium version of bosses and other demons
            skillReplacementMap (Dict): map of bosses and their skills and replacement skills
'''
def balanceMismatchedBossEncounter(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, configSettings , compendium, playerBossArr, skillReplacementMap):
    oldHPPool = calculateHPPool(oldEncounterData, newEncounterData)
    newDemons = newEncounterData.getAllUniqueDemonsInEncounter()
    oldDemons = oldEncounterData.getAllUniqueDemonsInEncounter()
    for index, ind in enumerate(newDemons):
        replacementDemon = bossArr[ind]
        referenceIndex = oldDemons[0]
        referenceDemon = demonReferenceArr[referenceIndex]
        if oldEncounterData.partnerType:
            referenceDemon = demonReferenceArr[random.choice(oldDemons)]
        replacementDemon.stats = copy.deepcopy(referenceDemon.stats)
        replacementDemon.stats.HP = round(oldHPPool * newEncounterData.hpPercents[ind] / newEncounterData.countPerDemon[ind])
        if index == 0:
            replacementDemon.experience = oldEncounterData.totalEXP // newEncounterData.countPerDemon[ind]
            replacementDemon.money = oldEncounterData.totalMacca // newEncounterData.countPerDemon[ind]
        else:
            replacementDemon.experience = 0
            replacementDemon.money = 0
        replacementDemon.level = referenceDemon.level
        replacementDemon.damageMultiplier = referenceDemon.damageMultiplier
        #TODO: Consider Resist Sum penalty if more demons in new encounter (or bonus if less?)
        if configSettings.randomizeBossResistances and configSettings.scaleResistToCheck:
            replacementDemon.resist = randomizeBossResistances(replacementDemon, copy.deepcopy(referenceDemon),oldEncounterData.resistTotals[referenceIndex],configSettings, compendium, playerBossArr)
        elif configSettings.randomizeBossResistances and not configSettings.scaleResistToCheck:
            replacementDemon.resist = randomizeBossResistances(replacementDemon,copy.deepcopy(referenceDemon),newEncounterData.resistTotals[ind],configSettings, compendium, playerBossArr) 
        if replacementDemon in HEALING_BOSS_MAP.keys():
            adjustHealingSkills(replacementDemon, referenceDemon, skillReplacementMap)
        if configSettings.randomizeBossSkills:
            randomizeSkills(replacementDemon, skillReplacementMap)
        adjustForResistSkills(replacementDemon)


'''
Balances two boss encounters that feature minions. The main new demon will get its stats from the old main demon
The old minion pool is shuffled, and if there are more new minions than old minions, the old pool will be stacked and shuffled until there's enough
Minion HP and stats will be taken from random old minions
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
            configSettings (Settings): settings of the current rando run
            compendium (List(Compendium_Demon)): list of compendium demons
            playerBossArr (List(Compendium_Demon)): list of compendium version of bosses and other demons
            skillReplacementMap (Dict): map of bosses and their skills and replacement skills
'''
def balanceMinionToMinion(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, configSettings: Settings, compendium, playerBossArr, skillReplacementMap):
    newDemons = newEncounterData.getAllUniqueDemonsInEncounter()
    oldDemons = oldEncounterData.getAllUniqueDemonsInEncounter()
    if oldEncounterData.ind != newEncounterData.ind:
        shuffledMinions = [0] + sorted(oldDemons[1:], key=lambda x: random.random())
        while len(shuffledMinions) < len(newDemons):
            shuffledMinions = shuffledMinions + sorted(oldDemons[1:], key=lambda x: random.random())
    else:
        shuffledMinions = [0] + copy.deepcopy(oldDemons[1:])
    for index, ind in enumerate(newDemons):
        replacementDemon = bossArr[ind]
        if index == 0:
            referenceIndex = oldDemons[0]
            referenceDemon = demonReferenceArr[referenceIndex]
            replacementDemon.experience = oldEncounterData.totalEXP // newEncounterData.countPerDemon[ind]
            replacementDemon.money = oldEncounterData.totalMacca // newEncounterData.countPerDemon[ind]
        else:
            referenceIndex = shuffledMinions[index]
            referenceDemon = demonReferenceArr[referenceIndex]
            replacementDemon.experience = 0
            replacementDemon.money = 0
        replacementDemon.stats = copy.deepcopy(referenceDemon.stats)
        replacementDemon.level = referenceDemon.level
        replacementDemon.damageMultiplier = referenceDemon.damageMultiplier
        if configSettings.randomizeBossResistances and configSettings.scaleResistToCheck:
            replacementDemon.resist = randomizeBossResistances(replacementDemon, copy.deepcopy(referenceDemon),oldEncounterData.resistTotals[referenceIndex],configSettings, compendium, playerBossArr)
        elif configSettings.randomizeBossResistances and not configSettings.scaleResistToCheck:
            replacementDemon.resist = randomizeBossResistances(replacementDemon,copy.deepcopy(referenceDemon),newEncounterData.resistTotals[ind],configSettings, compendium, playerBossArr) 
        if replacementDemon in HEALING_BOSS_MAP.keys():
            adjustHealingSkills(replacementDemon, skillReplacementMap)
        if configSettings.randomizeBossSkills:
            randomizeSkills(replacementDemon, skillReplacementMap)
        adjustForResistSkills(replacementDemon)

'''
Balances two boss encounters that feature multiple demons. Each new demon will get its stats from one of the old ones randomly
The old demon pool is shuffled, and if there are more new demons than old demons, the old pool will be stacked and shuffled until there's enough
If the number of demons is equal between the two encounters, HP will be transfered directly between demons, otherwise the HP pool formula from the default function is used
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
            configSettings (Settings): settings of the current rando run
            compendium (List(Compendium_Demon)): list of compendium demons
            playerBossArr (List(Compendium_Demon)): list of compendium version of bosses and other demons
            skillReplacementMap (Dict): map of bosses and their skills and replacement skills
'''
def balancePartnerToPartner(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, configSettings, compendium, playerBossArr, skillReplacementMap):
    oldHPPool = calculateHPPool(oldEncounterData, newEncounterData)
    newDemons = newEncounterData.getAllUniqueDemonsInEncounter()
    oldDemons = oldEncounterData.getAllUniqueDemonsInEncounter()
    if len(newDemons) != len(oldDemons):
        oldHPPool = oldHPPool // len(newDemons)
    if oldEncounterData.ind != newEncounterData.ind:
        shuffledOldDemons = sorted(oldDemons[0:], key=lambda x: random.random())
        while len(shuffledOldDemons) < len(newDemons):
            shuffledOldDemons = shuffledOldDemons + sorted(oldDemons[1:], key=lambda x: random.random())
    else:
        shuffledOldDemons = copy.deepcopy(oldDemons)
    for index, ind in enumerate(newDemons):
        replacementDemon = bossArr[ind]
        referenceIndex = shuffledOldDemons[index]
        referenceDemon = demonReferenceArr[referenceIndex]
        if index == 0:
            replacementDemon.experience = oldEncounterData.totalEXP // newEncounterData.countPerDemon[ind]
            replacementDemon.money = oldEncounterData.totalMacca // newEncounterData.countPerDemon[ind]
        else:
            replacementDemon.experience = 0
            replacementDemon.money = 0
        replacementDemon.stats = copy.deepcopy(referenceDemon.stats)
        if len(newDemons) == len(oldDemons):
            replacementDemon.stats.HP = referenceDemon.stats.HP * oldEncounterData.countPerDemon[shuffledOldDemons[index]] // newEncounterData.countPerDemon[ind]
        else:
            replacementDemon.stats.HP = round(oldHPPool * newEncounterData.hpPercents[ind] / newEncounterData.countPerDemon[ind])
        replacementDemon.level = referenceDemon.level
        replacementDemon.damageMultiplier = referenceDemon.damageMultiplier
        if configSettings.randomizeBossResistances and configSettings.scaleResistToCheck:
            replacementDemon.resist = randomizeBossResistances(replacementDemon, copy.deepcopy(referenceDemon),oldEncounterData.resistTotals[referenceIndex],configSettings, compendium, playerBossArr)
        elif configSettings.randomizeBossResistances and not configSettings.scaleResistToCheck:
            replacementDemon.resist = randomizeBossResistances(replacementDemon,copy.deepcopy(referenceDemon),newEncounterData.resistTotals[ind],configSettings, compendium, playerBossArr) 
        if replacementDemon in HEALING_BOSS_MAP.keys():
            adjustHealingSkills(replacementDemon, skillReplacementMap)
        if configSettings.randomizeBossSkills:
            randomizeSkills(replacementDemon, skillReplacementMap)
       
        adjustForResistSkills(replacementDemon)
'''
Calculates a modified HP Pool for a replacement boss encounter to use based on the total HP of the old encounter's demons and the number of demons in each encounter
    Parameters:
        oldEncounter (List(Boss_Metadata)): The original demons at the check
        newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
    Returns:
        The calculated HP total to split among the new encounter demons
'''
def calculateHPPool(oldEncounterData, newEncounterData):
    pool = oldEncounterData.totalHP
    oldDemonCount = oldEncounterData.getCountOfDemonsExcludingMinions()
    newDemonCount = newEncounterData.getCountOfDemonsExcludingMinions()
    multiplier = 1.0
    modifier = GROUP_HP_MODIFIER
    while oldDemonCount > newDemonCount: #More demons in the old encounter, apply a HP penalty
        multiplier = multiplier * modifier
        modifier = modifier + (1 - modifier) ** 2
        oldDemonCount -= 1
    while newDemonCount > oldDemonCount: #More demons in the new encounter, apply a HP bonus
        multiplier = multiplier * 1 + (1 - modifier) * 3 / 4
        modifier = modifier + (1 - modifier) ** 2
        newDemonCount -= 1
    modifiedPool = round(pool * multiplier)
    if oldEncounterData.demons[0] in BOSS_HP_MODIFIERS.keys():
        modifiedPool = round(modifiedPool * BOSS_HP_MODIFIERS[oldEncounterData.demons[0]])
    if newEncounterData.demons[0] in BOSS_HP_MODIFIERS.keys():
        modifiedPool = round(modifiedPool / BOSS_HP_MODIFIERS[newEncounterData.demons[0]])
    return modifiedPool
    

'''
Fixes some special cases after boss randomization has been done
Demons that can be revived have a second version in the data that needs to sync with the original's stats
True Lucifer's phase 2 and phase 3 versions need to be synced as well, and their HP is reduced to account for the multiple phases
    Parameters:
        bossArr (List(Enemy_Demon)): The list of boss demons to patch
        configSettings (Settings): Settings determining what types of bosses were randomized
        compendium (List(Compendium_Demon)): list of compendium demons
        playerBossArr (List(Compendium_Demon)): list of compendium version of bosses and other demons
'''
def patchSpecialBossDemons(bossArr, configSettings, compendium, playerBossArr):
    for base, duplicates in REVIVED_DEMON_DUPLICATE_MAP.items():
        referenceDemon = bossArr[base]
        for duplicate in duplicates:
            demonToPatch = bossArr[duplicate]
            demonToPatch.level = referenceDemon.level
            demonToPatch.stats = copy.deepcopy(referenceDemon.stats)
            demonToPatch.pressTurns = referenceDemon.pressTurns
            demonToPatch.damageMultiplier = referenceDemon.damageMultiplier
            demonToPatch.instakillRate = referenceDemon.instakillRate
            demonToPatch.resist = referenceDemon.resist
    if configSettings.randomizeLucifer:
        luciferPhase1 = bossArr[LUCIFER_PHASES[0]]
        luciferPhase2 = bossArr[LUCIFER_PHASES[1]]
        luciferPhase3 = bossArr[LUCIFER_PHASES[2]]
        luciferPhase2.stats = copy.deepcopy(luciferPhase1.stats) #Lucifer has some stat variance between phases but eh
        luciferPhase3.stats = copy.deepcopy(luciferPhase1.stats)
        luciferPhase2.pressTurns = luciferPhase1.pressTurns
        luciferPhase3.pressTurns = luciferPhase1.pressTurns
        luciferPhase2.instakillRate = luciferPhase1.instakillRate
        luciferPhase3.instakillRate = luciferPhase1.instakillRate
        luciferPhase3.stats.HP = luciferPhase2.stats.HP * 3
        luciferPhase3.experience = luciferPhase1.experience
        luciferPhase3.money = luciferPhase1.money
        luciferPhase1.experience = 0
        luciferPhase1.money = 0
        luciferPhase2.damageMultiplier = luciferPhase1.damageMultiplier
        luciferPhase3.damageMultiplier = luciferPhase1.damageMultiplier
        luciferPhase2.level = luciferPhase1.level
        luciferPhase3.level = luciferPhase1.level
        luciferPhase3.resist = luciferPhase1.resist
        
        if configSettings.randomizeBossResistances and configSettings.scaleResistToCheck:
            luciferPhase2.resist = randomizeBossResistances(luciferPhase2, copy.deepcopy(luciferPhase1),LUCIFER_PHASE_2_RESIST_TOTALS,configSettings, compendium, playerBossArr)
        elif configSettings.randomizeBossResistances and not configSettings.scaleResistToCheck:
            resistTotalSubDict = calculateResistTotals(LUCIFER_PHASES[2],luciferPhase2)
            luciferPhase2.resist = randomizeBossResistances(luciferPhase2,copy.deepcopy(luciferPhase1),resistTotalSubDict[LUCIFER_PHASES[2]],configSettings, compendium, playerBossArr)       
    

'''
Creates the pools of boss encounters that should be randomized within themselves
TODO: Handle duplicate Abscesses
    Parameters:
        eventEncountArr (List(Event_Encounter)): The list of event encounters containing most bosses
        encountArr (List(Encounter)): The list of normal encounters containing bosses from Abscesses and Punishing Foes
        bossDuplicateMap (Dict(int, int)): A dict that maps duplicate encounters to their original version
        configSettings (Settings): Settings determining what types of bosses should be randomized
        validBossDemons (Set): Set of boss demon IDs that will be used for things like item drop randomization
    Returns:
        A List of lists containing deep copied Mixed Boss Encounters to randomize
'''
def createBossEncounterPools(eventEncountArr, encountArr, uniqueSymbolArr, abscessArr, bossDuplicateMap, configSettings):
    bossPools = {}
    mixedPool = []
    abscessPool = []
    punishingPool = []
    minibossPool = []
    foundEventEncounters = []
    for abscess in abscessArr:
        if abscess.miracles[0] == 0:
            continue
        if abscess.eventEncounter > 0:
            abscessPool.append(copy.deepcopy(eventEncountArr[abscess.eventEncounter]))
            foundEventEncounters.append(abscess.eventEncounter)
        elif abscess.encounter > 0:
            abscessPool.append(copy.deepcopy(encountArr[abscess.encounter]))
    for symbol in uniqueSymbolArr:
        if symbol.symbol.value < numbers.NORMAL_ENEMY_COUNT:
            continue
        if symbol.eventEncounterID > 0:
            punishingPool.append(copy.deepcopy(eventEncountArr[symbol.eventEncounterID]))
            foundEventEncounters.append(symbol.eventEncounterID)
        elif symbol.encounterID > 0:
            punishingPool.append(copy.deepcopy(encountArr[symbol.encounterID]))
    normalPool = [copy.deepcopy(e) for index, e in enumerate(eventEncountArr) if index not in BANNED_BOSSES and index not in bossDuplicateMap.keys()
                    and index not in LUCIFER_ENCOUNTERS and index not in SUPERBOSS_ENCOUNTERS and index not in MINIBOSS_ENCOUNTERS and index not in foundEventEncounters]
    if configSettings.randomizeLucifer:
        normalPool = normalPool + [copy.deepcopy(e) for index, e in enumerate(eventEncountArr) if index in LUCIFER_ENCOUNTERS]
    superbossPool = [copy.deepcopy(e) for index, e in enumerate(eventEncountArr) if index in SUPERBOSS_ENCOUNTERS and index not in bossDuplicateMap.keys()]
    minibossPool = [copy.deepcopy(e) for index, e in enumerate(eventEncountArr) if index in MINIBOSS_ENCOUNTERS]
    minibossPool = minibossPool + [copy.deepcopy(encountArr[ILLUSION_AGRAT_ENCOUNTER])] #Add shadow agrat encounter to miniboss pool
    if configSettings.mixedRandomizeNormalBosses:
        mixedPool = mixedPool + normalPool
    elif configSettings.selfRandomizeNormalBosses:
        bossPools.update({"Random Normal":normalPool})
    else:
        bossPools.update({"Vanilla Normal":normalPool})
    if configSettings.mixedRandomizeSuperbosses:
        mixedPool = mixedPool + superbossPool
    elif configSettings.selfRandomizeSuperbosses:
        bossPools.update({"Random Superboss":superbossPool})
    else:
        bossPools.update({"Vanilla Superboss":superbossPool})
    if configSettings.mixedRandomizeAbscessBosses:
        mixedPool = mixedPool + abscessPool
    elif configSettings.selfRandomizeAbscessBosses:
        bossPools.update({"Random Abcess":abscessPool})
    else:
        bossPools.update({"Vanilla Abcess":abscessPool})   
    if configSettings.mixedRandomizeOverworldBosses:
        mixedPool = mixedPool + punishingPool
    elif configSettings.selfRandomizeOverworldBosses:
        bossPools.update({"Random Punishing":punishingPool})
    else:
        bossPools.update({"Vanilla Punishing":punishingPool})
    if configSettings.mixedRandomizeMinibosses:
        mixedPool = mixedPool + minibossPool
    elif configSettings.selfRandomizeMinibosses:
        bossPools.update({"Random Mini":minibossPool})
    else:
        bossPools.update({"Vanilla Mini":minibossPool})
    if mixedPool:
        bossPools.update({"Mixed": mixedPool})
    return formatBossPools(bossPools)


'''
Converts the mixed normal and event encounter boss pools to a single format of Mixed_Boss_Encounter
    Parameters:
        bossPools (List of lists)
    Returns:
       The formatted List of List of Mixed_Boss_Encounter
'''
def formatBossPools(bossPools):
    formattedBossPools = {}
    for name,pool in bossPools.items():
        formattedPool = []
        for boss in pool:
            formattedPool.append(formatBossEncounter(boss))
        formattedBossPools.update({name:formattedPool})
    return formattedBossPools

'''
Converts an Encounter or Event_Encounter to a single Mixed_Boss_Encounter format to use while randomizing bosses
    Paramters:
        encounter (Encounter or Event_Encounter)
    Returns:
        The formatted Mixed_Boss_Encounter
'''
def formatBossEncounter(encounter):
    formattedEncounter = Mixed_Boss_Encounter()
    formattedEncounter.ind = encounter.ind
    if isinstance(encounter, Event_Encounter):
        formattedEncounter.demons = [demon.value for demon in encounter.demons]
        formattedEncounter.isEvent = True
        formattedEncounter.eventEncounter = encounter
        formattedEncounter.track = encounter.track
    else:
        formattedEncounter.demons = encounter.demons
        formattedEncounter.normalEncounter = encounter
        formattedEncounter.track = encounter.track
    return formattedEncounter

'''
Fills a DUMMY event encounter with demons that would otherwise go into a normal encounter but require an event or 8 demon slots.
The corresponding abscess or unique symbol is updated to use the new event encounter id instead of their original normal encounter id
    Parameters:
        encounterToUpdate (Mixed_Boss_Encounter): The normal encounter to convert to an event encounter
        newEncounter (Mixed_Boss_Encounter): The event encounter containing problematic demons
        dummyIndex (Number): The index of the dummy event encounters to use - different from the actual index in the eventEncountArr
        eventEncountArr (List(Event_Encounter))
        abscessArr (List(Abscess))
        uniqueSymbolArr (List(Unique_Symbol_Encounter))
'''
def assignDummyEventEncounter(encounterToUpdate, newEncounter, dummyIndex, eventEncountArr, abscessArr, uniqueSymbolArr):
    normalEncounterIndex = encounterToUpdate.ind
    newEventIndex = DUMMY_EVENT_ENCOUNTERS[dummyIndex]
    newEventEncounter = eventEncountArr[newEventIndex]
    newEventEncounter.demons = newEncounter.eventEncounter.demons
    newEventEncounter.track = newEncounter.track
    encounterToUpdate.isEvent = True
    encounterToUpdate.demons = newEncounter.demons
    encounterToUpdate.track = newEventEncounter.track
    encounterToUpdate.eventEncounter = newEventEncounter
    encounterToUpdate.normalEncounter = None
    encounterToUpdate.ind = newEventIndex
    
    for abscess in abscessArr:
        if abscess.encounter == normalEncounterIndex:
            abscess.encounter = 0
            abscess.eventEncounter = newEventIndex
            
    for symbol in uniqueSymbolArr:
        if symbol.encounterID == normalEncounterIndex:
            symbol.encounterID = 0
            symbol.eventEncounterID = newEventIndex
            

'''
    Returns the amount of press turns a boss encounter with no demons dead will have
        Parameters:
            encounter (Boss_Metadata): The encounter data containing the number and ids of demons
            staticBossArr (List(Enemy_Demon)): The list containing press turn data for all demons
'''
def calculateEncounterPressTurns(encounter, staticBossArr):
    totalPressTurns = 0
    maxSummons = 999
    numSummons = -1
    if encounter.demons[0] in PRESS_TURN_MAX_SUMMONS.keys():
        maxSummons = PRESS_TURN_MAX_SUMMONS[encounter.demons[0]]
    for demonID, count in encounter.countPerDemon.items():
        demonPressTurns = staticBossArr[demonID].pressTurns
        totalPressTurns += demonPressTurns * count
        numSummons += 1
        if numSummons >= maxSummons:
            break
    return totalPressTurns

'''
Balances the press turns of a boss encounter
All demons will receive at least one press turn
If it's impossible to exactly match the check's press turns, the new encounter will get the closest amount of turns that's lower than the old check's turns
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
            balanceTurnsToCheck (Bool): If true, press turns should match check instead of boss
            extraTurnChance (Number): Chance of adding one or more press turns to the boss
'''
def adjustBossPressTurns(oldEncounterData, newEncounterData, demonReferenceArr, bossArr, balanceTurnsToCheck, extraTurnChance):
    currentPressTurns = calculateEncounterPressTurns(newEncounterData, demonReferenceArr)
    if balanceTurnsToCheck:
        targetTurns = calculateEncounterPressTurns(oldEncounterData, demonReferenceArr)
    else:
        targetTurns = currentPressTurns
    targetTurns = targetTurns + math.trunc(extraTurnChance)
    if random.random() < math.modf(extraTurnChance)[0]:
        targetTurns += 1
    targetTurns = min(targetTurns, 8)
    #print("Boss " + bossArr[newEncounterData.demons[0]].name + " with " + str(currentPressTurns) + " should have " + str(targetTurns) + " to match " + bossArr[oldEncounterData.demons[0]].name)
    demonsWithPressTurns = [] # Some 'demons' like Lahmu's tentacles have 0 press turns and should stay that way
    demonsWithMultipleTurns = []
    demonsWithLowestTurns = []
    for demonID in newEncounterData.getAllUniqueDemonsInEncounter():
        if bossArr[demonID].pressTurns > 0:
            demonsWithPressTurns.append(demonID)
        if bossArr[demonID].pressTurns > 1:
            demonsWithMultipleTurns.append(demonID)
        if bossArr[demonID].pressTurns == 1:
            demonsWithLowestTurns.append(demonID)
    if currentPressTurns > targetTurns: # Remove press turns to match the check
        while demonsWithMultipleTurns and currentPressTurns > targetTurns:
            random.shuffle(demonsWithMultipleTurns)
            targetReduction = currentPressTurns - targetTurns
            chosenDemon = demonsWithMultipleTurns[0]
            reduction = newEncounterData.countPerDemon[chosenDemon]
            for demonID in demonsWithMultipleTurns: # Search for a demon that will reduce the number of press turns to the target if it loses a single press turn
                if newEncounterData.countPerDemon[demonID] == targetReduction:
                    chosenDemon = demonID
                    reduction = targetReduction
                    break
            currentPressTurns -= reduction
            bossArr[chosenDemon].pressTurns -= 1
            if bossArr[chosenDemon].pressTurns <= 1:
                demonsWithMultipleTurns.remove(chosenDemon)
    elif currentPressTurns < targetTurns: # Add press turns to match the check
        if newEncounterData.minionType: # For minion bosses give all bonus turns to the main demon
            mainDemon = bossArr[newEncounterData.demons[0]]
            mainDemon.pressTurns += (targetTurns - currentPressTurns)
        else:
            lowestTurns = 1
            while currentPressTurns < targetTurns:
                while not demonsWithLowestTurns:
                    lowestTurns += 1
                    for demonID in demonsWithPressTurns:
                        if bossArr[demonID].pressTurns == lowestTurns:
                            demonsWithLowestTurns.append(demonID)
                random.shuffle(demonsWithLowestTurns)
                targetIncrease = targetTurns - currentPressTurns
                chosenDemon = demonsWithLowestTurns[0]
                increase = newEncounterData.countPerDemon[chosenDemon]
                for demonID in demonsWithLowestTurns: # Search for a demon that will not go over the target if its press turns are increased by one
                    if newEncounterData.countPerDemon[demonID] <= targetIncrease:
                        chosenDemon = demonID
                        increase = newEncounterData.countPerDemon[demonID]
                        break
                if increase <= targetIncrease:
                    currentPressTurns += increase
                    bossArr[chosenDemon].pressTurns += 1
                    demonsWithLowestTurns.remove(chosenDemon)
                else:
                    break
    #print("The boss now has " + str(calculateEncounterPressTurns(newEncounterData, bossArr)))

'''
Balances the instakill rates of a boss encounter to match the check it replaces
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
'''
def adjustInstakillRatesToCheck(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    oldEncounterDemons = oldEncounterData.getAllUniqueDemonsInEncounter()
    for index, demonID in enumerate(newEncounterData.getAllUniqueDemonsInEncounter()):
        if index < len(oldEncounterDemons):
            bossArr[demonID].instakillRate = demonReferenceArr[oldEncounterDemons[index]].instakillRate
        else:
            diff = demonReferenceArr[demonID].instakillRate - demonReferenceArr[newEncounterData.demons[0]].instakillRate
            newRate = max(min(bossArr[newEncounterData.demons[0]].instakillRate + diff, 100), 0)
            bossArr[demonID].instakillRate = newRate
        #print("Instakill rate went from " + str(demonReferenceArr[demonID].instakillRate) + " to " + str(bossArr[demonID].instakillRate))
'''
Randomizes the resistance profiles of a boss. The process attempts to follow base game distribution of resistances and elemnents.
A resistance profile of a boss either tries to match the actual boss or the check it replaces in their sum of resistances.
The outcome is changed depending on what resistance settings are chosen. 
    Parameters: 
        replacementDemon(Enemy_Demon): the demon the resistances are chosen for
        referenceDemon(Enemy_Demon): The demon that is being replaced
        checkSums(List(Number)): list of two numbers, first being the sum for elemental resists, second for ailment resists
        configSettings(Settings): settings to use to modify how resistances are randomized
        compendium (List(Compendium_Demon)): list of compendium demons, used to reference player version of boss
        playerBossArr (List(Compendium_Demon)): list of compendium version of bosses and other demons, used to reference player version of boss
    Returns: a resistance profile for the replacement demon to use
'''
def randomizeBossResistances(replacementDemon, referenceDemon, checkSums, configSettings: Settings, compendium, playerBossArr):
    if configSettings.playerResistSync:
        if len(BOSS_PLAYER_MAP) == 0:
            #initialize boss player map if needed
            df = pd.read_csv(paths.BOSS_PLAYER_MAP)
        
            for _ , row in df.iterrows():
                boss_id = row['BossID']
                comp_id = row['CompID']
                BOSS_PLAYER_MAP[boss_id] = comp_id
    
    endResist = None
    if replacementDemon.ind in STANDARD_RESIST_BOSSES:
        endResist = replacementDemon.resist
    elif configSettings.playerResistSync and replacementDemon.ind in BOSS_PLAYER_MAP.keys():
        if BOSS_PLAYER_MAP[replacementDemon.ind] > len(compendium):
            endResist = playerBossArr[BOSS_PLAYER_MAP[replacementDemon.ind]].resist
        else:
            endResist = compendium[BOSS_PLAYER_MAP[replacementDemon.ind]].resist
    else:
    
        if len(TOTAL_BOSS_RESIST_MAP) == 0:
            #initialize TOTAL_BOSS_RESIST_MAP if needed
            TOTAL_BOSS_RESIST_MAP["count"] = 0
            for element in ["physical"] + numbers.ELEMENT_RESIST_NAMES:
                valueDict = {}
                for simpleValue in numbers.SIMPLE_RESIST_VALUES:
                    valueDict.update({simpleValue: 0})
                TOTAL_BOSS_RESIST_MAP.update({element: valueDict})
            for ailment in numbers.AILMENT_NAMES:
                valueDict = {}
                for simpleValue in numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS.keys():
                    valueDict.update({simpleValue: 0})
                TOTAL_BOSS_RESIST_MAP.update({ailment: valueDict})
                    


        

        if not configSettings.scaleResistToCheck:
            physWeights = copy.deepcopy(numbers.BOSS_PHYS_RESIST_DISTRIBUTION[0])
        else:
            physWeights = copy.deepcopy(numbers.BOSS_PHYS_RESIST_DISTRIBUTION[math.ceil(replacementDemon.level / 10)])

        
        validPhysResist = False
        while not validPhysResist: #reroll phys resist to be valid with diverseResists if enabled
            physResist = random.choices(numbers.SIMPLE_RESIST_VALUES,physWeights)[0]
            if configSettings.diverseBossResists and physResist != 1 and TOTAL_BOSS_RESIST_MAP["physical"].get(physResist) > TOTAL_BOSS_RESIST_MAP["count"] / numbers.DIVERSE_RESIST_FACTOR:
                validPhysResist =False
            else:
                validPhysResist = True
        chosenResists = [1,1,1,1,1,1] #the element resist results will be saved here
        alreadyChosen = set() #will contain elements that have already been assigned
        
        allowedRange = 1.5

        baselineSum = checkSums[0]
        currentSum = sum(chosenResists) + physResist * 1.5
        minRuns = 3
        while len(alreadyChosen) < len(numbers.ELEMENT_RESIST_NAMES) and (len(alreadyChosen) <= minRuns or baselineSum - allowedRange < currentSum < baselineSum + allowedRange):
            elementResistWeights = [] #these weights will be used to calculate which resist value is used
            
            #these weights are used to decide the elements based on the not already chosen ones
            elementWeights = [1 if numbers.ELEMENT_RESIST_NAMES[index] not in alreadyChosen else 0 for index,v in enumerate(chosenResists) ]
            element = random.choices(numbers.ELEMENT_RESIST_NAMES,elementWeights)[0]
            alreadyChosen.add(element)
            
            if configSettings.scaleResistToCheck:
                if element == "dark" or "light":
                    elementResistWeights = copy.deepcopy(numbers.BOSS_LD_RESIST_DISTRIBUTION[math.ceil(replacementDemon.level / 10)])
                else:
                    elementResistWeights = copy.deepcopy(numbers.BOSS_FIEF_RESIST_DISTRIBUTION[math.ceil(replacementDemon.level / 10)])
            else:
                if element == "dark" or "light":
                    elementResistWeights = copy.deepcopy(numbers.BOSS_LD_RESIST_DISTRIBUTION[0])
                else:
                    elementResistWeights = copy.deepcopy(numbers.BOSS_FIEF_RESIST_DISTRIBUTION[0])
            
            
            if configSettings.diverseBossResists:
                for index, value in enumerate(TOTAL_BOSS_RESIST_MAP[element].values()):
                    if 1 +value > TOTAL_BOSS_RESIST_MAP["count"] / numbers.DIVERSE_RESIST_FACTOR and index != 4:# neutral resists are not subject to diverseResist setting
                        elementResistWeights[index] /= 2
            
            elementResist = random.choices(numbers.SIMPLE_RESIST_VALUES,elementResistWeights)[0]
            chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = elementResist
            currentSum = sum(chosenResists) + physResist * 1.5
            
        ailmentResists = [] #the ailment resist results will be saved here
        for _ in numbers.AILMENT_NAMES:
            ailmentResists.append(1)
        alreadyChosen = set()

        #ailments count half because they are should be worth less than elemental ones
        currentSum = sum(chosenResists) + physResist * 1.5 + sum(ailmentResists)/2
        minRuns = 3
        baselineSum += checkSums[1]
        while len(alreadyChosen) < len(numbers.AILMENT_NAMES) and (len(alreadyChosen) <= minRuns or baselineSum - allowedRange < currentSum < baselineSum + allowedRange):
            ailmentResistWeights = []
            ailmentWeights = [1 if numbers.AILMENT_NAMES[index] not in alreadyChosen else 0 for index,v in enumerate(ailmentResists) ]
            ailment = random.choices(numbers.AILMENT_NAMES,ailmentWeights)[0]
            alreadyChosen.add(ailment)

            if configSettings.scaleResistToCheck:
                ailmentResistWeights = copy.deepcopy(numbers.BOSS_AILMENT_RESIST_DISTRIBUTION[math.ceil(replacementDemon.level / 10)])
            else:
                ailmentResistWeights = copy.deepcopy(numbers.BOSS_AILMENT_RESIST_DISTRIBUTION[0])
            
            if configSettings.diverseBossResists:
                for index, value in enumerate(TOTAL_BOSS_RESIST_MAP[ailment].values()):
                    if 1 +value > TOTAL_BOSS_RESIST_MAP["count"] / numbers.DIVERSE_RESIST_FACTOR and index != 4:
                        ailmentResistWeights[index] /= 2

            ailmentResist = random.choices(list(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS.keys()),ailmentResistWeights)[0]
            ailmentResists[numbers.AILMENT_NAMES.index(ailment)] = ailmentResist
            currentSum = sum(chosenResists) + physResist * 1.5 + sum(ailmentResists)/2
        
        attempts = 100
        #try to make sum fit into range limits, to achieve somewhat balanced resist profiles
        while currentSum < baselineSum - allowedRange or currentSum > baselineSum + allowedRange:
            attempts -= 1
            if attempts <= 0:
                print("Something went wrong in resist rando at level " + str(replacementDemon.level) + "for demon " + str(replacementDemon.name))
                break
            if currentSum < baselineSum - allowedRange:
                #add weaknesses/ make resist worse, Increase value
                
                randomTypes = {}
                # types that only have weaknesses cannot be added, since no value to increase
                if chosenResists.count(1.5) != len(chosenResists):
                    randomTypes.update({"Elements" : (numbers.BOSS_FIEF_RESIST_DISTRIBUTION[0][5] + numbers.BOSS_LD_RESIST_DISTRIBUTION[0][5])/2})
                if ailmentResists.count(1.5) != len(ailmentResists):
                    randomTypes.update({"Ailments" : numbers.BOSS_AILMENT_RESIST_DISTRIBUTION[0][-1]})
                if len(randomTypes) == 0: #not checking for phys weakness here, since physWeak would make it highly likely for this occur anyway
                    randomTypes.update({"Physical": numbers.BOSS_PHYS_RESIST_DISTRIBUTION[0][5]})
                if physResist == -1.5 and ailmentResists.count(1.5) != len(ailmentResists): #if phys is a drain add ailments with higher weights to reduce cases where most elements are weaknesses
                    randomTypes.update({"Ailments" : numbers.BOSS_AILMENT_RESIST_DISTRIBUTION[0][-1]* 2} )
                changeType = random.choices(list(randomTypes.keys()), list(randomTypes.values()))[0]

                if changeType == "Ailments":
                    #weaks cannot be increased further
                    chooseAilmentWeights = [0 if r == 1.5 else 10 for r in ailmentResists]
                    ailment = random.choices(numbers.AILMENT_NAMES,chooseAilmentWeights)[0]
                    ailmentResist = ailmentResists[numbers.AILMENT_NAMES.index(ailment)]
                    resistIndex = min(len(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS.keys())-1,list(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS.keys()).index(ailmentResist)  +1)
                    ailmentResists[numbers.AILMENT_NAMES.index(ailment)] = list(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS.keys())[resistIndex]
                elif changeType == "Physical":
                    element = "physical"
                    resistIndex = min(len(numbers.SIMPLE_RESIST_VALUES)-1,numbers.SIMPLE_RESIST_VALUES.index(physResist)  +1)
                    if configSettings.diverseBossResists:
                        
                        while resistIndex +1 < len(numbers.SIMPLE_RESIST_VALUES):
                            if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                if TOTAL_BOSS_RESIST_MAP[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > TOTAL_BOSS_RESIST_MAP["count"] / numbers.DIVERSE_RESIST_FACTOR:
                                    resistIndex += 1
                                else:
                                    break
                            else:
                                break
                    physResist = numbers.SIMPLE_RESIST_VALUES[resistIndex]        
                else:
                    chooseElementWeights = [0 if r == 1.5 else 10 for r in chosenResists]
                    element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
                    elementResist = chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)]
                    resistIndex = min(len(numbers.SIMPLE_RESIST_VALUES)-1,numbers.SIMPLE_RESIST_VALUES.index(elementResist)  +1)
                    # Avoid overpopulating resistances if diverseResists is enabled
                    if configSettings.diverseBossResists:
                        
                        while resistIndex +1 < len(numbers.SIMPLE_RESIST_VALUES):
                            if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                if TOTAL_BOSS_RESIST_MAP[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > TOTAL_BOSS_RESIST_MAP["count"] / numbers.DIVERSE_RESIST_FACTOR:
                                    resistIndex += 1
                                else:
                                    break
                            else:
                                break
                    chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = numbers.SIMPLE_RESIST_VALUES[resistIndex]          
            elif currentSum > baselineSum + allowedRange:
                #add resists/make weakness worse, decrease value
                randomTypes = {}
                if chosenResists.count(-1.5) != len(chosenResists):
                    randomTypes.update({"Elements" : (numbers.BOSS_FIEF_RESIST_DISTRIBUTION[0][5] + numbers.BOSS_LD_RESIST_DISTRIBUTION[0][5])/2})
                if ailmentResists.count(0) != len(ailmentResists): #ailments cannot have repel/drain
                    randomTypes.update({"Ailments" : numbers.BOSS_AILMENT_RESIST_DISTRIBUTION[0][-1]})
                if len(randomTypes) == 0:
                    randomTypes.update({"Physical": numbers.BOSS_PHYS_RESIST_DISTRIBUTION[0][5]})
                changeType = random.choices(list(randomTypes.keys()), list(randomTypes.values()))[0]

                if changeType == "Ailments":
                    chooseAilmentWeights = [0 if r == 0 else 10  for r in ailmentResists]
                    ailment = random.choices(numbers.AILMENT_NAMES,chooseAilmentWeights)[0]
                    ailmentResist = ailmentResists[numbers.AILMENT_NAMES.index(ailment)]
                    #ailments cannot have repel/drain
                    resistIndex = max(0,list(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS.keys()).index(ailmentResist) -1)
                    #TODO: Diversity?
                    ailmentResists[numbers.AILMENT_NAMES.index(ailment)] =list(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS.keys())[resistIndex]
                elif changeType == "Physical":
                    element = "physical"
                    resistIndex = max(0,numbers.SIMPLE_RESIST_VALUES.index(physResist) -1)
                    if configSettings.diverseBossResists:
                        while resistIndex -1 > 0:
                            if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                if TOTAL_BOSS_RESIST_MAP[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > TOTAL_BOSS_RESIST_MAP["count"] / numbers.DIVERSE_RESIST_FACTOR:
                                    resistIndex -= 1
                                else:
                                    break
                            else:
                                break

                    physResist = numbers.SIMPLE_RESIST_VALUES[resistIndex ]
                else:
                    chooseElementWeights = [0 if r == -1.5 else 10  for r in chosenResists]
                    element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
                    elementResist = chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)]
                    resistIndex = max(0,numbers.SIMPLE_RESIST_VALUES.index(elementResist) -1)
                    if configSettings.diverseBossResists:
                        while resistIndex -1 > 0:
                            if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                if TOTAL_BOSS_RESIST_MAP[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > TOTAL_BOSS_RESIST_MAP["count"] / numbers.DIVERSE_RESIST_FACTOR:
                                    resistIndex -= 1
                                else:
                                    break
                            else:
                                break

                    chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = numbers.SIMPLE_RESIST_VALUES[resistIndex ]
            currentSum = sum(chosenResists) + physResist * 1.5 + sum(ailmentResists) / 2 

        allChosenResists = [physResist] + chosenResists
        
        if configSettings.consistentWeakCount:
            ogWeakCount = 0

            if configSettings.scaleResistToCheck:
                countDemon = referenceDemon
            else:
                countDemon = replacementDemon
            
            for attr in vars(countDemon.resist):
                if attr not in numbers.AILMENT_NAMES and 100 < getattr(countDemon.resist, attr, None).value < 900:
                    ogWeakCount += 1
            
            
            if countDemon.ind in STANDARD_RESIST_BOSSES:
                ogWeakCount /= 2
            
            oldChosenResists = copy.deepcopy(chosenResists)
            
            while(allChosenResists.count(1.5) < ogWeakCount):
                chooseElementWeights = [0 if r == 1.5 else r + 3 for r in chosenResists]
                if sum(chooseElementWeights) == 0: #Essentially should only happen for Masakado
                    ogWeakCount /= 2
                    chosenResists = oldChosenResists
                else:
                    element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
                    chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = 1.5
                allChosenResists = [physResist] + chosenResists



            # weakAdded = False
            # if not any(1.5 == r for r in allChosenResists): #Add random weakness
            #     chooseElementWeights = [r + 3 for r in chosenResists] #neutrals have highest chance to become weak, drains the lowest
            #     element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
            #     chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = 1.5
            #     allChosenResists = [physResist] + chosenResists
            #     weakAdded = True
            # if not any(r < 1 for r in allChosenResists): #Add random resistance for element that is not random weakness if it was added
            #     weaknessCount = allChosenResists.count(1.5)
            #     #null out weaknesses if there is only one, and prevent overwriting the potentially previously added one
            #     chooseElementWeights = [ 0 if (weaknessCount < 2 and r==1.5 ) or (weakAdded and index == numbers.ELEMENT_RESIST_NAMES.index(element))else -(r - 3) for index,r in enumerate(chosenResists)]
            #     element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
            #     chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = 0.5
            #     allChosenResists = [physResist] + chosenResists



        #Apply resist to demon and increase values in totalResistMap
        referenceDemon.resist.physical = Translated_Value(numbers.SIMPLE_RESIST_RESULTS[physResist],translation.translateResist(numbers.SIMPLE_RESIST_RESULTS[physResist]))
        TOTAL_BOSS_RESIST_MAP["physical"][physResist] += +1

        for index, element in enumerate(numbers.ELEMENT_RESIST_NAMES):
            TOTAL_BOSS_RESIST_MAP[element][chosenResists[index]] += 1
            value = numbers.SIMPLE_RESIST_RESULTS[chosenResists[index]]
            if replacementDemon.ind in STRONG_WEAKNESS_BOSSES and value == 1.5:
                value *= 2
            referenceDemon.resist.__setattr__(element,Translated_Value(value,translation.translateResist(numbers.SIMPLE_RESIST_RESULTS[chosenResists[index]])))
        resistProfiles.append([physResist] + chosenResists + ailmentResists)
        for index, ailment in enumerate(numbers.AILMENT_NAMES):
            TOTAL_BOSS_RESIST_MAP[ailment][ailmentResists[index]] += 1
            referenceDemon.resist.__setattr__(ailment,Translated_Value(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS[ailmentResists[index]],translation.translateResist(numbers.SIMPLE_BOSS_AILMENT_RESIST_RESULTS[ailmentResists[index]])))    
        #print(replacementDemon.name +" "+ str(replacementDemon.level) + ": " + str(checkSums) + "-> " + str(currentSum) + " from " + str(referenceDemon.name))
        endResist = referenceDemon.resist
    if configSettings.bossNoEarlyPhysImmunity and referenceDemon.level < numbers.EARLY_BOSS_LEVEL_LIMIT and not 0< endResist.physical.value < 150:
        endResist.physical.value = 100
    return endResist   

'''
Calculates the resistance total values for elemental and ailment resists for a boss.
    Parameters:
        demonID(Number): id of the demon
        demon(Enemy_Demon): the boss in question
    Returns a dictionary with demonID: [elementalSum, ailementSum]
'''
def calculateResistTotals(demonID, demon):
    elements = 0
    resistValue = demon.resist.physical.value
    if resistValue not in list(numbers.SIMPLE_RESIST_RESULTS.values()):
        elements += resistValue / 100
    else:
        elements += list(numbers.SIMPLE_RESIST_RESULTS.keys())[list(numbers.SIMPLE_RESIST_RESULTS.values()).index(resistValue)]
    elements = elements* 1.5
    ailments = 0
    for element in numbers.ELEMENT_RESIST_NAMES:
        resistValue = demon.resist.__getattribute__(element).value
        if resistValue not in list(numbers.SIMPLE_RESIST_RESULTS.values()):
            if(demonID in STANDARD_RESIST_BOSSES or demonID in STRONG_WEAKNESS_BOSSES) and resistValue == 300:
                simple =  resistValue / 300
            else:
                simple = resistValue / 100
        else:
            simple = list(numbers.SIMPLE_RESIST_RESULTS.keys())[list(numbers.SIMPLE_RESIST_RESULTS.values()).index(resistValue)]
        elements += simple
    for ailment in numbers.AILMENT_NAMES:
        resistValue = demon.resist.__getattribute__(ailment).value
        if resistValue not in list(numbers.SIMPLE_RESIST_RESULTS.values()):
            simple = resistValue / 100
        else:
            simple = list(numbers.SIMPLE_RESIST_RESULTS.keys())[list(numbers.SIMPLE_RESIST_RESULTS.values()).index(resistValue)]
        ailments += simple
    ailments /= 2
    return {demonID: [elements,ailments]}

'''
Adjust the resistance values of the demon to match potential resist skills
    Parameters:
        demon(Enemy_Demon): the demon in question
'''
def adjustForResistSkills(demon):
    for skill in demon.skills:
        #check for resistance skills (those do not work on enemies) and apply resistance accordingly
        if skill.ind in numbers.RESIST_SKILLS.keys():
            resistElement = numbers.RESIST_SKILLS[skill.ind][0]
            value = numbers.RESIST_SKILLS[skill.ind][1]

            oldValue = getattr(demon.resist, resistElement).value
            if numbers.compareResistValues(oldValue,value) == 1: #if new value is a stronger resist use it
                demon.resist.__setattr__(resistElement, Translated_Value(value,translation.translateResist(value)))
                    
def randomizeSkills(demon, skillReplacementMap):
    #TODO: Can#t work like this since bosses that use the same ai would need the same skills (Two abdiels for example)
    newSkills = []
    skillReplacementMap[demon.ind] = {}
    if demon.ind in MISSING_SKILLS_IN_LIST.keys():
        fullSkillList = demon.skills + [Translated_Value(skill,"") for skill in MISSING_SKILLS_IN_LIST[demon.ind]]
    else:
        fullSkillList = demon.skills
    for index, skill in enumerate(fullSkillList):
        if skill != 0:
            #TODO: Actual skill rando code instead of this test thing
            newSkill = 999 + index
            newSkills.append(Translated_Value(newSkill,""))
            skillReplacementMap[demon.ind].update({skill.ind: newSkill})
    demon.skills = newSkills

def adjustHealingSkills(replacementDemon, skillReplacementMap):
    pass
    #TODO: adjusts healing skills of bosses to fit level / put enemy versions in skill list