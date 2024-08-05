import copy
import random
import math

#Boss IDs that summon other enemies
BOSS_SUMMONS = {
    519: [517, 518],    #Khonsu Ra - Anubis and Thoth
    845: [871, 872, 873, 874, 875], #Shiva - Ganesha, Kali, Dakini, Ananta and Parvati
    934: [940, 941, 942, 943, 944, 945, 946], #Demi-Fiend - Cerberus, Jack Frost, Pixie, Thor, Girimekhala, Parvati, Cu Chulainn
    529: [531, 532, 533], #Lucifer True Ending - Brimstone Star, Cocytus Star, Morning Star
    537: [538, 539], #Lucifer Normal Endings - Brimstone Star, Cocytus Star
    839: [846, 847, 848, 849], #Huang Long - Qing Long, Zhuque, Baihu, Xuanwu
    760: [761, 762, 763, 764, 765, 766, 767], #Samael - Lilith's Shadow, Agrat's Shadow x2, Eisheth's Shadow x2, Naamah's Shadow x2
    569: [570, 571, 572, 573, 574, 575], #Lilith - Agrat x2, Eisheth x2, Naamah x2
    473: [474, 475], #Alilat - Flauros, Ose
    681: [682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693], #Satan - Arahabaki, Titania, Sarasvati, Yatagarasu, Ganesha, Kumphanda, Fafnir, Mada, Sraosha, Hariti, Kaiwan, Macabre
    463: [464], #Arioch - Decarabia
    924: [935], #White Rider - Dominion
    925: [936], #Red Rider - Power
    926: [937], #Black Rider - Legion
    927: [938], #Pale Rider - Loa
    561: [563], #Yuzuru - Second copy of Hayataro that gives 0 exp
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


class Boss_Metadata(object):
    def __init__(self, demons):
        self.summons = [] #List(Number)
        self.totalHP = 0
        self.totalEXP = 0
        self.totalMacca = 0
        self.demons = demons #List(Translated_Value)
        if demons[0].value in BOSS_SUMMONS.keys():
            self.summons = BOSS_SUMMONS[demons[0].value]
        self.partnerType = demons[0].value in PARTNER_BOSSES
        self.minionType = demons[0].value in MINION_BOSSES
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
            self.totalHP = demonReferenceArr[self.demons[0].value].stats.HP * self.countPerDemon[self.demons[0].value]

    '''
    Returns a List of demon IDs that are present in the encounter in order whether at the start or through a summon
    '''
    def getAllDemonsInEncounter(self):
        allDemons = []
        for demon in self.demons:
            if demon.value > 0:
                allDemons.append(demon.value)
        allDemons = allDemons + self.summons
        return allDemons

'''
Balances the stats of boss demons, including summoned adds to their new location
    Parameters:
        oldEncounter (List(Translated_Value)): The original demons at the check
        newEncounter (List(Translated_Value)): The demons replacing the old encounter
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
            oldEncounter (List(Translated_Value)): The original demons at the check
            newEncounter (List(Translated_Value)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
'''
def balanceMismatchedBossEncounter(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    oldHPPool = oldEncounterData.totalHP
    newDemons = newEncounterData.getAllDemonsInEncounter()
    oldDemons = oldEncounterData.getAllDemonsInEncounter()
    #print(newDemons)
    if not newEncounterData.minionType:
        oldHPPool = oldHPPool // len(newDemons)
    for index, ind in enumerate(newDemons):
        replacementDemon = bossArr[ind]
        referenceDemon = demonReferenceArr[oldDemons[0]]
        if oldEncounterData.partnerType:
            referenceDemon = demonReferenceArr[random.choice(oldDemons)]
        newHP = oldHPPool // newEncounterData.countPerDemon[ind]
        if newEncounterData.minionType and index > 0:
            newHP = newHP * demonReferenceArr[ind].stats.HP // demonReferenceArr[newDemons[0]].stats.HP
        replacementDemon.stats = copy.deepcopy(referenceDemon.stats)
        replacementDemon.stats.HP = newHP
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
            oldEncounter (List(Translated_Value)): The original demons at the check
            newEncounter (List(Translated_Value)): The demons replacing the old encounter
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
            oldEncounter (List(Translated_Value)): The original demons at the check
            newEncounter (List(Translated_Value)): The demons replacing the old encounter
            demonReferenceArr (List(Enemy_Demon)): An immutable list of enemy demons containing information about stats, etc
            bossArr (List(Enemy_Demon)): The list of enemy demons to be modified
'''
def balancePartnerToPartner(oldEncounterData, newEncounterData, demonReferenceArr, bossArr):
    oldHPPool = oldEncounterData.totalHP
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
            replacementDemon.stats.HP = oldHPPool // newEncounterData.countPerDemon[ind]
        replacementDemon.level = referenceDemon.level