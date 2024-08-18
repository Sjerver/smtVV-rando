from base_classes.encounters import Encounter, Event_Encounter, Mixed_Boss_Encounter
from util import numbers
import copy
import random

#Encounter IDs that should not be randomized
BANNED_BOSSES = [0, 7, 32, #Dummy Abbadon, Tutorial Pixie, Tutorial Daemon
                 #33, #Hydra (game hangs when supposed to lose limbs)
                 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, #Normal Cleopatra, Dummy Pretas x 5, Normal Andras, Dummy Mandrake, Attis, Shiva, King Frost, then all 4,
                 #57, 58, 59, 60, 63, 64, 65, #School dungeon fights with overlapping demons(Temp)
                 89, #Dummy Demi-Fiend
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
    760: [761, 762, 764, 766], #Samael - Lilith's Shadow, Agrat's Shadow, Eisheth's Shadow, Naamah's Shadow
    569: [570, 572, 574], #Lilith - Agrat, Eisheth, Naamah
    473: [474, 475], #Alilat - Flauros, Ose
    681: [682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693], #Satan - Arahabaki, Titania, Sarasvati, Yatagarasu, Ganesha, Kumphanda, Fafnir, Mada, Sraosha, Hariti, Kaiwan, Macabre
    463: [464], #Arioch - Decarabia
    924: [935], #White Rider - Dominion
    925: [936], #Red Rider - Power
    926: [937], #Black Rider - Legion
    927: [938], #Pale Rider - Loa
}

#Boss IDs (first in the encounter) with multiple enemies of equal strength
PARTNER_BOSSES = [433, #Eligor(Andras)
    442, 443, 444, 445, 446, 447, 448, 449, #All enemies during the school dungeon
    463, 471, 481, 485, 554, 561, 567,  #Arioch(Decarabias), Melchizedeks, Zeus(Odin), Dominion(Power), Naamah(GL), Yuzuru(Hayataro), Yakumo(Nuwa)
    577, 579, 602, 752, 772, #Fallen Abdiel(Dazai), Isis(Lamias), Makamis(Feng Huangs), Nozuchi(Kodamas), Kudlak(Black Oozes) 
    779, 814, 822, 829, 836, 866, 868] #Norn(Dis), Camael(Powers), Okuninushi(Kunitsu), Asura(Mithras), Gabriel(Uriel/Raphael), Leannan(Ippon), Apsaras(Agathions)

#Boss IDs (first in the encounter) with a single strong enemy and multiple weaker enemies
MINION_BOSSES = [452, 473, 519, 520, 525, #Lahmu(Tentacles), Alilat(Flauros/Ose), Khonsu Ra(Anubis/Thoth), Nuwa Nahobino(Thunder Bits), Abdiel Nahobino(Depraved arm/wing),
                 529, 537, 556, 565, 569, 681, #True Lucifer(Stars), Lucifer(Stars), Lahmu again(Tentacles), Tiamat(Heads), Lilith(Qadistu), Satan(Arahabaki/Friends),
                 760, 776, 816, 839, 845, #Samael(Shadows), Atavaka(Rakshasa), Moloch(Orobos/Flauros), Huang Long(Holy Beasts), Shiva(Ananta/Friends),
                 877, 924, 925, 926, 927, 934] #Zaou-Gongen(Kurama), All Four Riders(Call X), Demi-Fiend(Pixie/Friends)

#For bosses that can die and be resummoned (Hayataro etc), there's a second copy of the demon that needs to match stats with the original
REVIVED_DEMON_DUPLICATE_MAP = {
    562: 563, #Hayataro
    570: 571, #Agrat
    572: 573, #Eisheth
    574: 575, #Naamah
    762: 763, #Agrat's Shadow
    764: 765, #Eisheth's Shadow
    766: 767  #Naamah's Shadow
}

#Phase 1, 2, and 3 of Lucifer need to have their HP and stats synced (Phase 3 has triple the HP of the others)
LUCIFER_PHASES = [529, 534, 535]

#HP Penalty for single target bosses/bonus for multi-target bosses to account for AOE skills
GROUP_HP_MODIFIER = 0.8

#Event Encounter IDs that contain Lucifer (normal and true version), excluding VR battle duplicates
LUCIFER_ENCOUNTERS = [6, 12]

#Event Encounter IDs that contain superbosses (Shiva, Demi-Fiend, Satan, Masakado x2)
SUPERBOSS_ENCOUNTERS = [88, 121, 157, 168, 169]

BOSS_HP_MODIFIERS = {
    435: 0.5, #Snake Nuwa's replacement should have half HP
    529: 3 #True Lucifer's replacement will have triple HP (not completely accurate but fine for now)
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
'''
def balanceBossEncounter(oldEncounter, newEncounter, demonReferenceArr, bossArr, oldEncounterID, newEncounterID):
    oldEncounterData = Boss_Metadata(oldEncounter)
    newEncounterData = Boss_Metadata(newEncounter)
    oldEncounterData.calculateTotals(demonReferenceArr)
    newEncounterData.calculateTotals(demonReferenceArr)

    #Halve HP of Snake Nuwa Check
    if oldEncounterID == 35:
        oldEncounterData.totalHP = oldEncounterData.totalHP // 2
    #Double HP if Snake Nuwa is Replacement
    if newEncounterID == 35:
        oldEncounterData.totalHP = oldEncounterData.totalHP * 2

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
TODO: Calculate proper HP ratios for the new encounter and split the HP pool that way, add a hp bonus for multi-demon encounters to account for AOE skills
TODO: Account for 'revive' demons (Hayataro etc) that are effectively duplicates that currently bloat the hp pool
    Parameters:
            oldEncounter (List(Boss_Metadata)): The original demons at the check
            newEncounter (List(Boss_Metadata)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
'''
def balanceMismatchedBossEncounter(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    oldHPPool = calculateHPPool(oldEncounterData, newEncounterData)
    newDemons = newEncounterData.getAllDemonsInEncounter()
    oldDemons = oldEncounterData.getAllDemonsInEncounter()
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
    newDemons = newEncounterData.getAllDemonsInEncounter()
    oldDemons = oldEncounterData.getAllDemonsInEncounter()
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
    newDemons = newEncounterData.getAllDemonsInEncounter()
    oldDemons = oldEncounterData.getAllDemonsInEncounter()
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
        multiplier = multiplier / modifier
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
    for base, duplicate in REVIVED_DEMON_DUPLICATE_MAP.items():
        referenceDemon = bossArr[base]
        demonToPatch = bossArr[duplicate]
        demonToPatch.stats = copy.deepcopy(referenceDemon.stats)
    if configSettings.randomizeLucifer:
        luciferPhase1 = bossArr[LUCIFER_PHASES[0]]
        luciferPhase2 = bossArr[LUCIFER_PHASES[1]]
        luciferPhase3 = bossArr[LUCIFER_PHASES[2]]
        luciferPhase2.stats = copy.deepcopy(luciferPhase1.stats) #Lucifer has some stat variance between phases but eh
        luciferPhase3.stats = copy.deepcopy(luciferPhase1.stats)
        luciferPhase3.stats.HP = luciferPhase2.stats.HP * 3
    

'''
Creates the pools of boss encounters that should be randomized within themselves
TODO: Handle duplicate Abscesses
    Parameters:
        eventEncountArr (List(Event_Encounter)): The list of event encounters containing most bosses
        encountArr (List(Encounter)): The list of normal encounters containing bosses from Abscesses and Punishing Foes
        bossDuplicateMap (Dict(int, int)): A dict that maps duplicate encounters to their original version
        configSettings (Settings): Settings determining what types of bosses should be randomized
    Returns:
        A List of lists containing deep copied Mixed Boss Encounters to randomize
'''
def createBossEncounterPools(eventEncountArr, encountArr, uniqueSymbolArr, abscessArr, bossDuplicateMap, configSettings):
    bossPools = []
    mixedPool = []
    abscessPool = []
    punishingPool = []
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
                    and index not in LUCIFER_ENCOUNTERS and index not in SUPERBOSS_ENCOUNTERS and index not in foundEventEncounters]
    if configSettings.randomizeLucifer:
        normalPool = normalPool + [copy.deepcopy(e) for index, e in enumerate(eventEncountArr) if index in LUCIFER_ENCOUNTERS]
    superbossPool = [copy.deepcopy(e) for index, e in enumerate(eventEncountArr) if index in SUPERBOSS_ENCOUNTERS]
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