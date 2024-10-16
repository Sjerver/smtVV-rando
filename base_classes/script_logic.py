import random
import os
from util.binary_table import Table
import util.paths as paths
import util.numbers as numbers
from enum import IntEnum
from base_classes.quests import Mission_Reward, Fake_Mission
from base_classes.uasset import UAsset
import copy
import pandas as pd


class Script_Function_Type(IntEnum):
    IMPORT = 0
    NAME = 1

class Script_Uasset(UAsset):
    def __init__(self, binaryTable: Table):
        UAsset.__init__(self, binaryTable)
    
    '''
    Returns a list of offsets for all function calls in uexp of the given function where the specified parameter is passed.
        Parameter:
            uexp (Table): the uexp binary data where the function calls are searched in
            functionName (String): the name of the function to search for
            type (Script_Function_Type): in which mapping the functions id is located in
            paramNumber (Integer): which parameter of the function call to return the offset off
            bonusBytes (Integer): extra bytes to add on the offset
        Returns a list of offsets where the specified parameter is in a call of the function
    '''    
    def getOffsetsForParamXFromFunctionCalls(self, uexp: Table, functionName, type, paramNumber, bonusBytes = 0):
        additionalBytes = paramNumber * 5 + bonusBytes
        
        result = []

        #TODO: Decide if it's fine like this or remove type and just check import first and then names
        if type == Script_Function_Type.NAME and functionName in self.nameMap.keys():
            additionalBytes = additionalBytes + 4
            functionIndex = self.nameMap[functionName]
        elif type == Script_Function_Type.IMPORT and functionName in self.reverseImportMap.keys():
            functionIndex = self.reverseImportMap[functionName]
        else:
            return result
        
        result = uexp.findWordOffsets(functionIndex)

        for index, value in enumerate(result):
            result[index] = result[index] + additionalBytes
        return result
    
    '''
    Returns a list of offsets for all rows in the data table in the uexp where the given nameEntry appears.
        Parameter:
            uexp (Table): the uexp binary data where the nameEntry is searched in
            nameEntry (String): the name of a nameEntry to search for
            type (Script_Function_Type): in which mapping the functions id is located in
            bonusBytes (Integer): How many bytes later the desired column value is stored
        Returns a list of offsets where the specified parameter is in a call of the function
    '''  
    def getOffsetsForRowInNPCDataTable(self, uexp: Table, nameEntry,type , bonusBytes = 0):
        additionalBytes = bonusBytes
        
        result = []

        #TODO: Decide if it's fine like this or remove type and just check import first and then names
        if type == Script_Function_Type.NAME and nameEntry in self.nameMap.keys():
            functionIndex = self.nameMap[nameEntry]
        elif type == Script_Function_Type.IMPORT and nameEntry in self.reverseImportMap.keys():
            functionIndex = self.reverseImportMap[nameEntry]
        else:
            return result
        
        result = uexp.findWordOffsets(functionIndex)

        for index, value in enumerate(result):
            result[index] = result[index] + additionalBytes
        return result

EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event'
SCRIPT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script' 
SUBMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission'
MAINMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission'
MAINMISSION_M061_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission_M061' 
M061_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061'
M062_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M062'
M060_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M060'  
M063_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M063'  
M064_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M064'
MAIN_M016_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M016' 
M016_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M016'
M035_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M035' 
M036_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M036'
M030_FOLDER =  'rando/Project/Content/Blueprints/Event/Script/SubMission/M030'
M050_FOLDER =  'rando/Project/Content/Blueprints/Event/Script/SubMission/M050'
SHOP_EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/ShopEvent'
M061_EM1710_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM1710'
GARDEN_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/Garden'
MINATO_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m061'
SHINAGAWA_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m062'
CHIYODA_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m063'
SHINJUKU_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m064'
TAITO_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m060'
TOKYO_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_TokyoMap'
EMPYREAN_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m016'
MAIN_M060_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M060'
MAIN_M064_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M064'

#Key: EventScriptName, Value: List(Numbers) byte offsets where demon join is decided/checked
SCRIPT_JOIN_BYTES = {
    'MM_M061_EM1630': [149119,211659], # The Water Nymph 
    'MM_M061_EM1640': [165053,204312], # The Spirit of Love 
    'MM_M062_EM1660': [172224], # Holding The Line
    'MM_M062_EM1650': [191531], # Those Seeking Sanctuary
    'MM_M060_EM1690': [177252], # Raid on Tokyo, Files are same but I got 177252 instead for the Adrammelech location
    'MM_M060_EM1700': [172675], # In Defense of Tokyo
    'MM_M063_EM1670': [165799], # Black Frost Strikes Back
    'MM_M063_EM1680': [165807], # A Sobering Standoff
    'MM_M064_EM2310': [412261], # Reclaim the Golden Stool 
    'MM_M064_EM2320': [436569], # Liberate the Golden Stool
    'MM_M064_EM2270': [211353,313712], # The Vampire in Black
    'MM_M064_EM2280': [252862,364581], # The Hunter in White
    'MM_M060_EM1420': [166254,171324], # Fionn's Resolve
    'MM_M060_EM1602': [18867,19704], # The Destined Leader (Amanazako Could't Join Initially), not 100% sure on v1.02 locations
    'MM_M060_EM1601': [192337,188908], # The Destined Leader 
    'MM_M016_E0885': [24849,27932], #Hayataro CoC Chaos
    'MM_M016_E0885_Direct': [34729,35684], #Hayataro CoC Chaos
    'MM_M016_EM1450': [160681,156336], # A Plot Revealed
    'MM_M035_EM1480': [103495,100673], # The Seraph's Return
    'MM_M036_EM1490': [104705,107527], # The Red Dragon's Invitation
    'MM_M061_EM1781': [102474,108977], # Rage of a Queen
    'MM_M061_EM2613_HitAction': [161413,117165], # Holy Will and Profane Dissent
    'MM_M030_EM1769': [619541], # Bethel Researcher giving DLC Demons
    'MM_M061_EM1791': [137156,138009], # A Goddess in Training
    'MM_M061_EM2601': [212904], # Sakura Cinders of the East
    'MM_M063_EM2170': [326663], # Guardian of Tokyo
}

#List of which demon join is in which script
SCRIPT_JOINS = {
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
    'MM_M061_EM2613_HitAction': 4, # Dagda
    'MM_M030_EM1769': 78, # Mephisto (Can only join this way)
    'MM_M061_EM1791': 31, # Artemis
    'MM_M061_EM2601': 32, # Konohana Sakuya
    'MM_M063_EM2170': 227 # Masakado
}

#List of which folder each script is in, due to sometimes not being obvious based on file name
SCRIPT_FOLDERS = {
    'MM_M061_EM1630': M061_FOLDER, # The Water Nymph 
    'MM_M061_EM1640': M061_FOLDER, # The Spirit of Love
    'MM_M062_EM1660': M062_FOLDER, # Holding The Line
    'MM_M062_EM1650': M062_FOLDER, #Those Seeking Sanctuary
    'MM_M060_EM1690': M060_FOLDER, # Raid on Tokyo
    'MM_M060_EM1700': M060_FOLDER, # In Defense of Tokyo
    'MM_M063_EM1670': M063_FOLDER, # Black Frost Strikes Back
    'MM_M063_EM1680': M063_FOLDER, # A Sobering Standoff
    'MM_M064_EM2310': M064_FOLDER, # Reclaim the Golden Stool 
    'MM_M064_EM2320': M064_FOLDER, # Liberate the Golden Stool
    'MM_M064_EM2270': M064_FOLDER, # The Vampire in Black
    'MM_M064_EM2280': M064_FOLDER, # The Hunter in White
    'MM_M060_EM1420': M060_FOLDER, # Fionn's Resolve
    'MM_M060_EM1602': M060_FOLDER, # The Destined Leader (Amanazako Could't Join Initially)
    'MM_M060_EM1601': M060_FOLDER, # The Destined Leader
    'MM_M016_E0885': MAIN_M016_FOLDER, #Hayataro CoC Chaos
    'MM_M016_E0885_Direct': MAIN_M016_FOLDER, #Hayataro CoC Chaos
    'MM_M016_EM1450': M016_FOLDER, # A Plot Revealed
    'MM_M035_EM1480': M035_FOLDER, # The Seraph's Return
    'MM_M036_EM1490': M036_FOLDER, # The Red Dragon's Invitation
    'MM_M061_EM1781': M030_FOLDER, # Rage of a Queen
    'MM_M030_EM1769': M030_FOLDER, # Bethel Researcher giving DLC Demons 
    'MM_M061_EM1791': M030_FOLDER, # A Goddess in Training
    'MM_M061_EM2613_HitAction': M030_FOLDER, # Holy Will and Profane Dissent
    'MM_M061_EM2601': M061_FOLDER, # Sakura Cinders of the East
    'MM_M063_EM2170': M063_FOLDER, # Guardian of Tokyo
    'MM_M061_EM1030': M061_FOLDER, # Cursed Mermaids
    'MM_M050_EM2050': M050_FOLDER, # Picture-Perfect Debut
    'MM_M060_EM1310': M060_FOLDER, # Downtown Rock 'n Roll
    'MM_M060_EM1370': M060_FOLDER, # Keeper of the North
    'MM_M061_EM1360': M061_FOLDER, # Keeper of the West
    'MM_M062_EM1340': M062_FOLDER, # Keeper of the South
    'MM_M063_EM1350': M063_FOLDER, # Keeper of the East
    'MM_M061_EM1715': M061_EM1710_FOLDER, # Movin' on Up
    'MM_M060_EM1460': M060_FOLDER, # Gold Dragon's Arrival
    'MM_M063_EM1592': M063_FOLDER, # A Power Beyond Control 
    'MM_M030_EM2600': M030_FOLDER, # Sakura Cinders of the East (Periapt Event)
    'MM_M030_EM2610': M030_FOLDER, # Holy Will and Profane Dissent (Periapt Event
    'MM_M060_EM2351': GARDEN_FOLDER, # Rascal of the Norse
    'EM_M061_DevilTalk' : MAINMISSION_M061_FOLDER, # Tutorial Pixie Event
    'esNPC_m061_31a' : MINATO_NPC_FOLDER, #Rakshasa on Diet Building Roof
    'esNPC_m061_30a' : MINATO_NPC_FOLDER, #Slime near Qing Long
    'esNPC_m061_34a' : MINATO_NPC_FOLDER, #Pixie in Kamiyacho
    'BP_esNPC_TokyoMap_15b': TOKYO_NPC_FOLDER, #Tokyo NPC Mischievous Mascot Periapt
    'esNPC_m062_32a': SHINAGAWA_NPC_FOLDER, #Nue in Container
    'esNPC_m062_33a': SHINAGAWA_NPC_FOLDER, #Angel after Loup-garou/Eisheth 
    'esNPC_m062_40a': SHINAGAWA_NPC_FOLDER, #Slime in Shinagawa
    'esNPC_m063_20a': CHIYODA_NPC_FOLDER, #Yurlungur NPC
    'esNPC_m063_21a': CHIYODA_NPC_FOLDER, #Setanta NPC
    'esNPC_m060_10a': TAITO_NPC_FOLDER, #Orthrus NPC
    'esNPC_m016_01a': EMPYREAN_NPC_FOLDER, #Ongyo-Ki NPC
    'MM_M062_EM1132': M062_FOLDER, #Cait Sith in Fairy Village
    'MM_M060_EM1370_Direct': M060_FOLDER, #Fighting Bishamonten without Quest(shares reward with quest)
    'MM_M061_E2610': MAINMISSION_M061_FOLDER, #Isis Event in CoV
    'MM_M060_E0763': MAIN_M060_FOLDER, #Tao Talisman Event at the beginning of Taito
    'MM_M064_E2797': MAIN_M064_FOLDER, #Qadistu Talisman/Periapt
    'MM_M064_E2795_Direct': MAIN_M064_FOLDER, #Tsukuyomi Talisman
    'BP_JakyoEvent': SHOP_EVENT_FOLDER, #Cathedral of Shadows Event
    'MM_M061_EM0020': M061_FOLDER, # The Angel's Request
}

#List of additional rewards in fake missions
EXTRA_MISSION_REWARDS = {
    -1 : Mission_Reward(826, 1), #Fury Talisman
    -2: Mission_Reward(711, 1), #Exalted Seraphim Periapt
    -3: Mission_Reward(712, 1), #Macabre Family Periapt
    -4: Mission_Reward(506, 1), #Mermaid Essence
    -5: Mission_Reward(600, 1), #Amabie's Essence
    -6: Mission_Reward(390, 1), #Fafnir's Essence
    -7: Mission_Reward(440, 1), # Bishamonten's Essence
    -8: Mission_Reward(442, 1), # Koumokuten's Essence
    -9: Mission_Reward(443, 1), # Zouchouten's Essence
    -10: Mission_Reward(441, 1), # Jikokuten's Essence
    -11: Mission_Reward(713, 1), # Siblings of Olympus Periapt
    -12: Mission_Reward(807, 1), #Raptor Talisman
    -13: Mission_Reward(714, 1), # Cardinal Deity Periapt
    -14: Mission_Reward(338, 1), # Amanozako's Essence
    -15: Mission_Reward(721, 1), # Seeds of Dana Periapt
    -16: Mission_Reward(732, 1), # Mountain Gods Periapt
    -17: Mission_Reward(709, 1), # Asgardian Kin Periapt
    -18: Mission_Reward(716, 1), # Heavenly Kings Periapt
    -19: Mission_Reward(716, 1), # Heavenly Kings Periapt(Duplicate)
    -20: Mission_Reward(827, 1), # Lady Talisman(Duplicate of real Mission)
    -21: Mission_Reward(719, 1), # Servants of Heaven Periapt
}
#Dict of which scripts are handled via fake missions
EXTRA_MISSION_IDS = {
    'MM_M060_EM1601': [-1], # The Destined Leader
    'MM_M035_EM1480': [-2], # The Seraph's Return
    'MM_M036_EM1490': [-3], # The Red Dragon's Invitation
    'MM_M061_EM1030': [-4], # Cursed Mermaids
    'MM_M050_EM2050': [-5], # Picture-Perfect Debut
    'MM_M060_EM1310': [-6], # Downtown Rock 'n Roll
    'MM_M060_EM1370': [-7,-18], # Keeper of the North
    'MM_M061_EM1360': [-8], # Keeper of the West
    'MM_M062_EM1340': [-9], # Keeper of the South
    'MM_M063_EM1350': [-10], # Keeper of the East
    'MM_M016_EM1450': [-11], # A Plot Revealed
    'MM_M061_EM1715': [-12], # Movin' on Up
    'MM_M060_EM1460': [-13], # Gold Dragon's Arrival
    'MM_M063_EM1592': [-14], # A Power Beyond Control
    'MM_M030_EM2610': [-15], # Holy Will and Profane Dissent
    'MM_M030_EM2600': [-16], # Sakura Cinders of the East (Periapt Event)
    'MM_M060_EM2351': [-17], # Rascal of the Norse
    'MM_M060_EM1370_Direct': [-19], # Fighting Bishamonten without Quest(shares reward with quest)
    'MM_M061_E2610' : [-20], #Isis Story Event in CoV
    'MM_M061_EM0020': [-21], #The Angel's Request

}

#List of which areas rewards of fake missions are scaled after
EXTRA_MISSION_REWARD_AREAS = {
  16: [-2, -3, -11], #Empyrean
  35: [], #Temple of Eternity
  36: [], #Demon Kings Castle / Shakan
  38: [], #Demon Kings Castle / Shakan
  60: [-1,-6,-7,-8,-9,-10,-13, -15, -17, -18,-19], #Taito
  61: [-4,-12,-21], #Minato
  62: [-5], #Shinagawa
  63: [-14, -16], #Chiyoda
  64: [-20], #Shinjuku
  107: [] #Demi-Fiend Area: same as Empyrean
}

#Items being gifted in each script
BASE_GIFT_ITEMS = {
    'esNPC_m061_31a': 824, #Jaki Talisman
    'esNPC_m061_30a': 838, #Foul Talisman
    'esNPC_m061_34a': 717, #Pixie Periapt
    'BP_esNPC_TokyoMap_15b': 708, #Mischievous Mascot Periapt
    'esNPC_m062_32a': 825, #Wilder Talisman
    'esNPC_m062_33a': 811, #Divine Talisman
    'esNPC_m062_40a': 718, #Amorphous Periapt
    'esNPC_m063_20a': 835, #Snake Talisman
    'esNPC_m063_21a': 710, #Shadow Warrior Periapt
    'esNPC_m060_10a': 707, #Children of Echidna Periapt
    'esNPC_m016_01a': 715, #Elemental Oni Periapt
    'MM_M062_EM1132': 706, #Grimalkin Periapt
    'MM_M060_E0763': 845, #Panagia Talisman
    'MM_M064_E2797': 842, #Qadistu Talisman
    'MM_M064_E2797_PERIAPT': 731, #Qadistu Periapt
    'MM_M064_E2795_Direct': 839, #Tsukuyomi Talisman
    'BP_JakyoEvent': 844, #Devil Talisman
    'BP_JakyoEvent_Comp_Complete': 720, #Twinned Throne Periapt
}
# Areas the gifts are scaled after if they are not containing a key item
GIFT_AREAS = {
  16: ['esNPC_m016_01a','BP_JakyoEvent','BP_JakyoEvent_Comp_Complete'], #Empyrean
  35: [], #Temple of Eternity
  36: ['MM_M064_E2797','MM_M064_E2797_PERIAPT','MM_M064_E2795_Direct'], #Demon Kings Castle / Shakan
  38: [], #Demon Kings Castle / Shakan
  60: ['esNPC_m060_10a','MM_M062_EM1132','MM_M060_E0763'], #Taito
  61: ['esNPC_m061_31a','esNPC_m061_30a','esNPC_m061_34a'], #Minato
  62: ['esNPC_m062_32a','esNPC_m062_33a','esNPC_m062_40a'], #Shinagawa
  63: ['BP_esNPC_TokyoMap_15b','esNPC_m063_20a','esNPC_m063_21a'], #Chiyoda
  64: [], #Shinjuku
  107: [] #Demi-Fiend Area: same as Empyrean
} 
# Scripts with the same reward
GIFT_EQUIVALENT_SCRIPTS = {
    'esNPC_m061_31a' : ['esNPC_m061b_31a'],
    'esNPC_m061_30a' : ['esNPC_m061b_30a'],
    'esNPC_m062_32a': ['esNPC_m062b_32a'],
    'esNPC_m062_33a' : ['esNPC_m062b_33a'],
    'BP_esNPC_TokyoMap_15b' : ['BP_esNPC_TokyoMap_15b2','BP_esNPC_TokyoMap_15c'],
    'esNPC_m016_01a' : ['esNPC_m016_01b'],
    'MM_M060_E0763' : ['MM_M060_E3001_Direct'],
}
# Scripts that use the same script file, for different rewards
# Extra -> Original
GIFT_EXTRA_SCRIPTS = {
    'MM_M064_E2797_PERIAPT' : 'MM_M064_E2797',
    'BP_JakyoEvent_Comp_Complete': 'BP_JakyoEvent',
}

#Odds that a non key gift contains an essence
GIFT_ESSENCE_ODDS = 0.7 #Completely made up, but essence should be more likely for now since amount is fixed currently

#List of gifts only obtainable in canon of vengeance
VENGEANCE_EXCLUSIVE_GIFTS = ['MM_M064_E2797','MM_M064_E2797_PERIAPT','MM_M064_E2795_Direct']
#List of gifts that require a cleared game file
NEWGAMEPLUS_GIFTS = ['BP_JakyoEvent_Comp_Complete', 'BP_JakyoEvent']
#Script for the Tsukuyomi Talisman
TSUKUYOMI_TALISMAN_SCRIPT = 'MM_M064_E2795_Direct'

'''
Returns the original script that is used as the base for a script with equivalent reward.
'''
def getEquivalentSource(name):
    for key,valueList in GIFT_EQUIVALENT_SCRIPTS.items():
        for value in valueList:
            if value == name:
                return key
    return name

'''
Returns dictionary lining out to which reward are each gift belongs
'''
def getGiftRewardAreas():
    giftRewardAreas = {}
    for key in GIFT_AREAS.keys():
        for value in GIFT_AREAS[key]:
            giftRewardAreas[value] = key
    return giftRewardAreas

'''
Randomizes free demon joins based on the original joins level by adjusting the values in the corresponding event scripts.
Parameters:
    comp List(Compendium_Demon): list of all playable demons
    randomDemons (Boolean): whether to randomize the demon joins or set them to vanilla
    #TODO: Consider rewrite via uasset method (that way scripts should keep working even if future update changes them and we don't need to adjust the bytes manually)
'''
def randomizeDemonJoins(comp, randomDemons):
    writeFolder(EVENT_FOLDER)
    writeFolder(SCRIPT_FOLDER)
    writeFolder(SUBMISSION_FOLDER)
    writeFolder(MAINMISSION_FOLDER)
    writeFolder(M061_FOLDER)
    writeFolder(M062_FOLDER)
    #These demons appear in multiple scripts and should be the same in both
    amanozako = None
    hayataro = None
    cleopatra = None
    dagda = None

    #for every script and its offsets to write to
    for script, offsets in SCRIPT_JOIN_BYTES.items():
        #Read folder depending on sub or main mission
        if 'EM' in script:
            scriptData = readBinaryTable('base/Scripts/SubMission/' + script + '.uexp')
        else:
            scriptData = readBinaryTable('base/Scripts/MainMission/' + script + '.uexp')
        
        if randomDemons:

            referenceDemon = comp[SCRIPT_JOINS[script]]
            filteredComp = [d for d in comp if "Mitama" not in d.name and not d.name.startswith('NOT') and not d.ind in numbers.BAD_IDS]
            sameLevel = [demon for demon in filteredComp if demon.level.value == referenceDemon.level.original]
            if len(sameLevel) <1:
                #if no demon of same level exists, use all valid demons
                sameLevel = filteredComp
            newDemon = random.choice(sameLevel)

            #Save demon if it is needed in another script or use the saved demon
            if script == 'MM_M060_EM1601':
                newDemon = amanozako
            elif script == 'MM_M060_EM1602':
                amanozako = newDemon
            elif script == 'MM_M016_E0885':
                hayataro = newDemon
            elif script == 'MM_M016_E0885_Direct':
                newDemon = hayataro
            elif script == 'MM_M061_EM1781':
                cleopatra = newDemon
            elif script == 'MM_M061_EM2613_HitAction':
                dagda = newDemon

            for offset in offsets:
                scriptData.writeHalfword(newDemon.ind,offset)
        
            #Exception for Dagda/Cleo not being recruited during their Quest but at the researcher instead
            if script == 'MM_M030_EM1769':
                scriptData.writeHalfword(dagda.ind,619565)
                scriptData.writeHalfword(cleopatra.ind,619553)

        writeBinaryTable(scriptData.buffer, SCRIPT_FOLDERS[script] + '/' + script + '.uexp', SCRIPT_FOLDERS[script] )

'''
#TODO: Adjust for rewrite and comment
'''
def adjustFirstMimanEventReward(config, compendium, itemNames):
    scriptData = readBinaryTable('base/Scripts/ShopEvent/BP_ShopEvent.uexp')
    #byteList = [14113, 26035, 11754, 14361,14407, 21063,21109] #Old list for 1.0.2
    
    uassetData = Script_Uasset(readBinaryTable('base/Scripts/ShopEvent/BP_ShopEvent.uasset'))

    ogEssenceID = 496
    essenceID = 496 #Onmorakis Essence
    onmorakiLevel = 4
    if config.randomizeMimanRewards and not config.scaleItemsToArea:
        validEssences = []
        for itemID, itemName in enumerate(itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
            if 'Essence' in itemName and 'Aogami' not in itemName and 'Tsukuyomi' not in itemName and 'Demi-fiend' not in itemName:
                validEssences.append(itemID)
        essenceID = random.choice(validEssences)
    elif (config.randomDemonLevels or config.randomizeMimanRewards) and config.scaleItemsToArea:
        essenceNames = [demon.name + "'s Essence" for demon in compendium if demon not in numbers.BAD_IDS and 'Mitama' not in demon.name and demon.level.value == onmorakiLevel]
        validEssences = []
        for itemID, itemName in enumerate(itemNames): 
            if itemName in essenceNames:
                validEssences.append(itemID)
        essenceID = random.choice(validEssences)

    # for byte in byteList:
    #     scriptData.writeHalfword(essenceID, byte)

    updateItemRewardInScript(uassetData, scriptData, ogEssenceID, essenceID)
    
    writeBinaryTable(scriptData.buffer, SHOP_EVENT_FOLDER + '/BP_ShopEvent.uexp', SHOP_EVENT_FOLDER)

'''
Reads a file containing game data into a Table with a bytearray
    Parameters:
        filePath (string): The path to the file to read.
     Returns: 
        The buffer containing file data as a Table
'''
def readBinaryTable(filePath):
    fileContents = Table(filePath)
    return fileContents

'''
Writes the given Buffer to the file specified by filePath
    Parameters:
        result (Buffer): The data to write
        filePath (string): The path to write the file at
        folderPath (string): The path the folder where the file is, used to check if the folder exists
'''
def writeBinaryTable(result, filePath, folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    with open(filePath, 'wb') as file:
        file.write(result)

def writeFolder(folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)      

'''
Finds the byte offsets relating to the rewarding of items in the script.
    Parameters:
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
    Returns a list of offsets where item ids need to be changed so the items given through the script change
'''
def getItemRewardByteLocation(uassetData: Script_Uasset, uexpData: Table):
    byteList = []
    importedFunctions = {
        'ItemGet': 1,
        'ItemGetNum': 1,
        }

    namedFunctions = {
        'IItemWindowSetParameter': 1,
        'IMsgSetRichTextValueParam': 2 #Second parameter is itemID
    }

    for name, number in importedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.IMPORT, number)
    for name, number in namedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.NAME, number)

    
    return byteList

def getDemonModelAssetStringByteLocation(uassetData: Script_Uasset, uexpData: Table):
    byteList = []
    importedFunctions = {
        'LoadAsset': 1,
        }

    namedFunctions = {

    }

    bonusBytes = {
        'LoadAsset': 2,
    }

    for name, number in importedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.IMPORT, number,bonusBytes[name] )
    for name, number in namedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.NAME, number, bonusBytes[name])

    
    return byteList

def getDemonModelIDByteLocation(uassetData: Script_Uasset, uexpData: Table):
    byteList = []
    importedFunctions = {
        
        }

    namedFunctions = {
        'BPL_AdjustMapSymbolScale': 2,
    }

    bonusBytes = {
        'BPL_AdjustMapSymbolScale': 12,
    }

    for name, number in importedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.IMPORT, number,bonusBytes[name] )
    for name, number in namedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.NAME, number, bonusBytes[name])

    
    return byteList

'''
Finds the byte offsets relating to the rewarding of items in the npc data table.
    Parameters:
        uassetData (Script_Uasset): the uasset data of the npc data table
        uexpData (Table): the binary data of the uexp of the npc data table
    Returns a list of offsets where item ids need to be changed so the items given through the script change
'''
def getNPCGiftItemByteLocation(uassetData: Script_Uasset, uexpData: Table):
    byteList = []
    importedFunctions = [
        
    ]

    namedFunctions = [
        'E_EVENT_SCRIPT_TYPE::NewEnumerator52', #Enum entry ItemAdd2 per E_EVENT_SCRIPT_TYPE.uasset
    ]

    bonusBytes = {
        'E_EVENT_SCRIPT_TYPE::NewEnumerator52': 33,
    }

    for name in importedFunctions:
        byteList = byteList + uassetData.getOffsetsForRowInNPCDataTable(uexpData,name,Script_Function_Type.IMPORT,bonusBytes[name] )
    for name in namedFunctions:
        byteList = byteList + uassetData.getOffsetsForRowInNPCDataTable(uexpData,name,Script_Function_Type.NAME, bonusBytes[name])

    
    return byteList

'''
Updates the old item given through the script to the new item.
    Parameters:
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        #TODO: Include amount??
'''
def updateItemRewardInScript(uassetData, uexpData, oldItemID, newItemID):
    byteList = getItemRewardByteLocation(uassetData, uexpData)

    toRemove = []
    for offset in byteList:
        if uexpData.readHalfword(offset) != oldItemID:
            toRemove.append(offset)
    
    for offset in toRemove:
        byteList.remove(offset)
    
    # if len(byteList) > 0:
    #    print(str(oldItemID) + " -> " + str(newItemID) + " (" + str(len(byteList)))

    for byte in byteList:
        uexpData.writeHalfword(newItemID, byte)

'''
Updates the old item given through the script at the given paths to the new item.
    Parameters:
        uassetPath (String): the path to the uasset of the script
        uexpPath (String): the path to the b the uexp of the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
'''
def updateItemRewardInScriptPaths(uassetPath, uexpPath, oldItemID, newItemID):
    uexpData = readBinaryTable(uexpPath)
    uassetData = Script_Uasset(readBinaryTable(uassetPath))
    return updateItemRewardInScript(uassetData, uexpData, oldItemID, newItemID)

'''
Creates fake missions from certain event scripts involving quests.
    Returns a list of fake missions
'''
def createFakeMissionsForEventRewards():
    fakeMissions = []

    for script, indeces in EXTRA_MISSION_IDS.items():
        for index in indeces:
            fakeMission = Fake_Mission()
            fakeMission.ind = index
            fakeMission.reward = EXTRA_MISSION_REWARDS[fakeMission.ind]
            fakeMission.originalReward = copy.deepcopy(fakeMission.reward)
            
            if 'EM' in script: #is mission from a main story or not
                uexpData = readBinaryTable('base/Scripts/SubMission/' + script + '.uexp')
                uassetData = Script_Uasset(readBinaryTable('base/Scripts/SubMission/' + script + '.uasset'))
            else:
                uexpData = readBinaryTable('base/Scripts/MainMission/' + script + '.uexp')
                uassetData = Script_Uasset(readBinaryTable('base/Scripts/MainMission/' + script + '.uasset'))

            fakeMission.uexp = uexpData
            fakeMission.uasset = uassetData
            fakeMission.script = script
            
            fakeMissions.append(fakeMission)

    return fakeMissions

'''
Writes the updated reward data to the event scripts and removes the fake missions from the mission array.
    Parameters:
        missionArr (List(Mission)): a list of all missions and fake missions
    Returns list with all fake missions removed
'''
def updateAndRemoveFakeMissions(missionArr):
    writeFolder(EVENT_FOLDER)
    writeFolder(SCRIPT_FOLDER)
    writeFolder(SUBMISSION_FOLDER)
    writeFolder(MAINMISSION_FOLDER)
    toRemove = []
    for index, mission in enumerate(missionArr):
        if mission.ind < 0:
            
            #print(str(mission.ind) + ": " + str(mission.originalReward.ind) + " -> " + str(mission.reward.ind) )
            updateItemRewardInScript(mission.uasset, mission.uexp, mission.originalReward.ind, mission.reward.ind)

            writeFolder(SCRIPT_FOLDERS[mission.script])
            writeBinaryTable(mission.uexp.buffer, SCRIPT_FOLDERS[mission.script] + '/' + mission.script + '.uexp', SCRIPT_FOLDERS[mission.script])

            toRemove.append(mission)
    for mission in toRemove:
        missionArr.remove(mission)
    return missionArr



def replaceDemonModelInScript(script, uassetData: Script_Uasset, uexpData, ogDemonID, replacementDemonID):
    '''
    #TODO: This does not quite work like this for multiple reasons:
        - a version of the name of the demon appears in the path of animation files
        - the id of the demon is also given as a parameter in the uexpData
        - the name of the demon also shows up in pre-defined name Strings in the uexpData
    What would therefore at least be needed to make this work?
        - making a list of the names of models for the paths to animation files
        - getting and replacing the functions where either the demon's id or a name String are parameters
        - updating size related stuff (lengths and offsets) in uasset and uexp
    '''

    #TODO: Figure out where to better read the csv data
    modelNameMap = pd.read_csv(paths.MODEL_NAMES, dtype=str)
    modelNames = {}
    demonIDModelID = {}
    for index, row in modelNameMap.iterrows():
        if type(row['MainDemonID']) is str:
             modelNames[row['Number']] = row['folderName']
             demonIDModelID[int(row['MainDemonID'])] = row['Number']

    oldID = demonIDModelID[ogDemonID]
    oldName = modelNames[oldID]

    newID = demonIDModelID[replacementDemonID]
    newName = modelNames[newID]

    for index, name in enumerate(uassetData.nameList):
        if oldID in name:
            uassetData.nameList[index] = name.replace(oldID,newID)
        if oldName in name:
            uassetData.nameList[index] = name.replace(oldName,newName)
    
    uassetData.updateNameMap()

    demonModelIDBytes = getDemonModelIDByteLocation(uassetData, uexpData)
    demonModelAssetStringBytes = getDemonModelAssetStringByteLocation(uassetData, uexpData)

    #TODO: Code that changes the values in uexp, but


    writeBinaryTable(uexpData.buffer, SCRIPT_FOLDERS[script] + '/' + script + '.uexp', SCRIPT_FOLDERS[script])
    uassetData.writeDataToBinaryTable()
    writeBinaryTable(uassetData.binaryTable.buffer, SCRIPT_FOLDERS[script] + '/' + script + '.uasset', SCRIPT_FOLDERS[script])


def replaceTutorialPixieModel(replacementDemonID):
    script = 'EM_M061_DevilTalk'
    uexpData = readBinaryTable('base/Scripts/MainMission/' + script + '.uexp')
    uassetData = Script_Uasset(readBinaryTable('base/Scripts/MainMission/' + script + '.uasset'))

    replaceDemonModelInScript(script, uassetData, uexpData, 59, replacementDemonID)

'''
Updates all script data regarding item gifts.
    Parameters:
    gifts(List(Gift_Item)): list of all gifts
'''
def updateGiftScripts(gifts):
    uexpCorrection = {} #dict to save uexp which get modified multiple times
    for gift in gifts:
        if gift.script in GIFT_EQUIVALENT_SCRIPTS.keys(): #if script has script with same reward add copy of gift with new script to gift list
            for script in GIFT_EQUIVALENT_SCRIPTS[gift.script]:
                vengeanceGift = copy.deepcopy(gift)
                vengeanceGift.script = script
                gifts.append(vengeanceGift)
        correctScript = gift.script
        if gift.script in GIFT_EXTRA_SCRIPTS.keys(): #if script is handling an additional item in a script, get the original script
            correctScript = GIFT_EXTRA_SCRIPTS[gift.script]
        if 'NPC' in correctScript: #NPC data tables are handled here   
            uexpData = readBinaryTable('base/Scripts/NPC/' + correctScript + '.uexp')
            uassetData = Script_Uasset( readBinaryTable('base/Scripts/NPC/' + correctScript + '.uasset'))
            if gift.script in GIFT_EXTRA_SCRIPTS.values(): # add uexp to dict if script has additional versions
                uexpCorrection[gift.script] = uexpData
            if correctScript in uexpCorrection.keys(): #get already modified uexp from correct script
                uexpData = uexpCorrection[correctScript]
            if any(gift.script in scripts for scripts in GIFT_EQUIVALENT_SCRIPTS.values()): #if script was copied as equivalent, use original base item
                equivalentScript = getEquivalentSource(gift.script)
                updateNPCGiftInScript(BASE_GIFT_ITEMS[equivalentScript], gift.item.ind, uassetData, uexpData)
            else:
                updateNPCGiftInScript(BASE_GIFT_ITEMS[gift.script], gift.item.ind, uassetData, uexpData)
        else: #else it is an event script
            if correctScript in ['BP_JakyoEvent']:
                missionType = 'ShopEvent/'
            elif 'EM' in correctScript:
                missionType = 'SubMission/'
            else: 
                missionType = 'MainMission/'
            uexpData = readBinaryTable('base/Scripts/' + missionType + correctScript + '.uexp')
            uassetData = Script_Uasset( readBinaryTable('base/Scripts/' + missionType + correctScript + '.uasset'))
            if gift.script in GIFT_EXTRA_SCRIPTS.values(): # add uexp to dict if script has additional versions
                uexpCorrection[gift.script] = uexpData
            if correctScript in uexpCorrection.keys(): #get already modified uexp from correct script
                uexpData = uexpCorrection[correctScript]
            if any(gift.script in scripts for scripts in GIFT_EQUIVALENT_SCRIPTS.values()): #if script was copied as equivalent, use original base item
                equivalentScript = getEquivalentSource(gift.script)
                updateItemRewardInScript(uassetData,uexpData,BASE_GIFT_ITEMS[equivalentScript],gift.item.ind)
            else:
                #print(gift.script + ": " + str(BASE_GIFT_ITEMS[gift.script]) + " -> " + str(gift.item.ind) )
                updateItemRewardInScript(uassetData,uexpData,BASE_GIFT_ITEMS[gift.script],gift.item.ind)

        if gift.script in SCRIPT_FOLDERS.keys(): #if script has folder listed use it
            writeBinaryTable(uexpData.buffer, SCRIPT_FOLDERS[gift.script] + '/' + gift.script + '.uexp', SCRIPT_FOLDERS[gift.script])
        elif correctScript in SCRIPT_FOLDERS.keys():
            writeBinaryTable(uexpData.buffer, SCRIPT_FOLDERS[correctScript] + '/' + correctScript + '.uexp', SCRIPT_FOLDERS[correctScript])
        else: #use folder of equivalent otherwise
            equivalentScript = getEquivalentSource(gift.script)
            writeBinaryTable(uexpData.buffer, SCRIPT_FOLDERS[equivalentScript] + '/' + gift.script + '.uexp', SCRIPT_FOLDERS[equivalentScript])    

'''
Updates the old item given through the npc script to the new item.
    Parameters:
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        #TODO: Include amount??
'''   
def updateNPCGiftInScript(oldItemID, newItemID, uassetData, uexpData):
    byteList = getNPCGiftItemByteLocation(uassetData, uexpData)

    toRemove = []
    for offset in byteList:
        if uexpData.readHalfword(offset) != oldItemID:
            toRemove.append(offset)
    
    for offset in toRemove:
        byteList.remove(offset)

    for byte in byteList:
        uexpData.writeHalfword(newItemID, byte)