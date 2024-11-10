from base_classes.encounters import Encounter, Event_Encounter, Mixed_Boss_Encounter
from util import numbers
import copy
import random

#Encounter IDs that should not be randomized
BANNED_BOSSES = [0, 7, 32, #Dummy Abbadon, Tutorial Pixie, Tutorial Daemon
                 #33, #Hydra (game hangs when supposed to lose limbs)
                 #TODO: Encounter 45 has a copy of mara boss for the virtual trainer, that version of mara is the same except for their AI
                 #57, 58, 59, 60, 63, 64, 65, #School dungeon fights with overlapping demons(Temp)
                 #129, 159, 160, #Mananangal/Incubus overlap with school(Temp), Zhens in gasser sidequest that overlap with each other(Temp)
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
    843: [885], #Danu - Mandrake
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
DUMMY_EVENT_ENCOUNTERS = [141]
#TODO: Since we only have one we have a problem, we could add a slot to the eventEncountTable but that's pretty much it?

# Map of bosses who summon a set number of minions at a time, used to calculate total press turns
PRESS_TURN_MAX_SUMMONS = {
    934: 3, # Demi-Fiend
    681: 3, # Satan
    760: 2, # Samael
    845: 3, # Shiva
    828: 1, # Arahabaki
    839: 2, # Huang Long
}

# Map of boss summons that are summoned in groups of more than one, like Arioch's 2 decarabias
SUMMONED_DEMON_COUNTS = {
    464: 2, # Decarabia
    935: 2, # Rider summons (Except Legions from Black Rider)
    936: 2,
    938: 2,
    885: 2, # Mandrake
}


class Boss_Metadata(object):
    def __init__(self, demons):
        self.summons = [] #List(number)
        self.totalHP = 0
        self.totalEXP = 0
        self.totalMacca = 0
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
        for demon, count in self.countPerDemon.items():
            if demon == 0:
                continue
            self.totalHP += demonReferenceArr[demon].stats.HP * count
            self.totalEXP += demonReferenceArr[demon].experience * count
            self.totalMacca += demonReferenceArr[demon].money * count
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
        balancePressTurns (Bool): Whether the press turns of the new encounter should match the old encounter's press turns
'''
def balanceBossEncounter(oldEncounter, newEncounter, demonReferenceArr, bossArr, oldEncounterID, newEncounterID, balancePressTurns, balanceInstakillRates):
    oldEncounterData = Boss_Metadata(oldEncounter)
    newEncounterData = Boss_Metadata(newEncounter)
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
        
    if balancePressTurns:
        adjustBossPressTurns(oldEncounterData, newEncounterData, demonReferenceArr, bossArr)
        
    if balanceInstakillRates:
        adjustInstakillRatesToCheck(oldEncounterData, newEncounterData, demonReferenceArr, bossArr)
    
    if oldEncounterData.minionType and newEncounterData.minionType:
        balanceMinionToMinion(oldEncounterData, newEncounterData, demonReferenceArr, bossArr)
    elif oldEncounterData.partnerType and newEncounterData.partnerType:
        balancePartnerToPartner(oldEncounterData, newEncounterData, demonReferenceArr, bossArr)
    else:
        balanceMismatchedBossEncounter(oldEncounterData, newEncounterData, demonReferenceArr, bossArr)
        
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
'''
def balanceMismatchedBossEncounter(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    oldHPPool = calculateHPPool(oldEncounterData, newEncounterData)
    newDemons = newEncounterData.getAllUniqueDemonsInEncounter()
    oldDemons = oldEncounterData.getAllUniqueDemonsInEncounter()
    for index, ind in enumerate(newDemons):
        replacementDemon = bossArr[ind]
        referenceDemon = demonReferenceArr[oldDemons[0]]
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
        

'''
Balances two boss encounters that feature minions. The main new demon will get its stats from the old main demon
The old minion pool is shuffled, and if there are more new minions than old minions, the old pool will be stacked and shuffled until there's enough
Minion HP and stats will be taken from random old minions
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
'''
def balanceMinionToMinion(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    newDemons = newEncounterData.getAllUniqueDemonsInEncounter()
    oldDemons = oldEncounterData.getAllUniqueDemonsInEncounter()
    shuffledMinions = [0] + sorted(oldDemons[1:], key=lambda x: random.random())
    while len(shuffledMinions) < len(newDemons):
        shuffledMinions = shuffledMinions + sorted(oldDemons[1:], key=lambda x: random.random())
    for index, ind in enumerate(newDemons):
        replacementDemon = bossArr[ind]
        if index == 0:
            referenceDemon = demonReferenceArr[oldDemons[0]]
            replacementDemon.experience = oldEncounterData.totalEXP // newEncounterData.countPerDemon[ind]
            replacementDemon.money = oldEncounterData.totalMacca // newEncounterData.countPerDemon[ind]
        else:
            referenceDemon = demonReferenceArr[shuffledMinions[index]]
            replacementDemon.experience = 0
            replacementDemon.money = 0
        replacementDemon.stats = copy.deepcopy(referenceDemon.stats)
        replacementDemon.level = referenceDemon.level
        replacementDemon.damageMultiplier = referenceDemon.damageMultiplier
        

'''
Balances two boss encounters that feature multiple demons. Each new demon will get its stats from one of the old ones randomly
The old demon pool is shuffled, and if there are more new demons than old demons, the old pool will be stacked and shuffled until there's enough
If the number of demons is equal between the two encounters, HP will be transfered directly between demons, otherwise the HP pool formula from the default function is used
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
'''
def balancePartnerToPartner(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    oldHPPool = calculateHPPool(oldEncounterData, newEncounterData)
    newDemons = newEncounterData.getAllUniqueDemonsInEncounter()
    oldDemons = oldEncounterData.getAllUniqueDemonsInEncounter()
    if len(newDemons) != len(oldDemons):
        oldHPPool = oldHPPool // len(newDemons)
    shuffledOldDemons = sorted(oldDemons[1:], key=lambda x: random.random())
    while len(shuffledOldDemons) < len(newDemons):
        shuffledOldDemons = shuffledOldDemons + sorted(oldDemons[1:], key=lambda x: random.random())
    for index, ind in enumerate(newDemons):
        replacementDemon = bossArr[ind]
        referenceDemon = demonReferenceArr[shuffledOldDemons[index]]
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
'''
def patchSpecialBossDemons(bossArr, configSettings):
    for base, duplicates in REVIVED_DEMON_DUPLICATE_MAP.items():
        referenceDemon = bossArr[base]
        for duplicate in duplicates:
            demonToPatch = bossArr[duplicate]
            demonToPatch.stats = copy.deepcopy(referenceDemon.stats)
            demonToPatch.pressTurns = referenceDemon.pressTurns
            demonToPatch.instakillRate = referenceDemon.instakillRate
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
    bossPools = []
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
    if configSettings.mixedRandomizeNormalBosses:
        mixedPool = mixedPool + normalPool
    elif configSettings.selfRandomizeNormalBosses:
        bossPools.append(normalPool)
    if configSettings.mixedRandomizeSuperbosses:
        mixedPool = mixedPool + superbossPool
    elif configSettings.selfRandomizeSuperbosses:
        bossPools.append(superbossPool)
    if configSettings.mixedRandomizeAbscessBosses:
        mixedPool = mixedPool + abscessPool
    elif configSettings.selfRandomizeAbscessBosses:
        bossPools.append(abscessPool)   
    if configSettings.mixedRandomizeOverworldBosses:
        mixedPool = mixedPool + punishingPool
    elif configSettings.selfRandomizeOverworldBosses:
        bossPools.append(punishingPool)
    if configSettings.mixedRandomizeMinibosses:
        mixedPool = mixedPool + minibossPool
    elif configSettings.selfRandomizeMinibosses:
        bossPools.append(minibossPool)
    if mixedPool:
        bossPools.append(mixedPool)
    return formatBossPools(bossPools)


'''
Converts the mixed normal and event encounter boss pools to a single format of Mixed_Boss_Encounter
    Parameters:
        bossPools (List of lists)
    Returns:
       The formatted List of List of Mixed_Boss_Encounter
'''
def formatBossPools(bossPools):
    formattedBossPools = []
    for pool in bossPools:
        formattedPool = []
        for boss in pool:
            formattedPool.append(formatBossEncounter(boss))
        formattedBossPools.append(formattedPool)
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
Balances the press turns of a boss encounter to match the check it replaces
All demons will receive at least one press turn
If it's impossible to exactly match the check's press turns, the new encounter will get the closest amount of turns that's lower than the old check's turns
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
'''
def adjustBossPressTurns(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    targetTurns = calculateEncounterPressTurns(oldEncounterData, demonReferenceArr)
    currentPressTurns = calculateEncounterPressTurns(newEncounterData, demonReferenceArr)
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