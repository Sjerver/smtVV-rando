import random
import os
from util.binary_table import Table, readBinaryTable, writeBinaryTable, writeFolder
import util.paths as paths
import util.numbers as numbers
from base_classes.script import Script_Function_Type, Script_Uasset, Script_Join_Type
from base_classes.quests import Mission_Reward, Fake_Mission
from base_classes.uasset import UAsset
import copy
import pandas as pd

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
    'MM_M061_EM2050': M050_FOLDER, # Picture-Perfect Debut
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
    'esNPC_m016_02a': EMPYREAN_NPC_FOLDER, #Ongyo-Ki NPC
    'MM_M062_EM1132': M062_FOLDER, #Cait Sith in Fairy Village
    'MM_M060_EM1370_Direct': M060_FOLDER, #Fighting Bishamonten without Quest(shares reward with quest)
    'MM_M061_E2610': MAINMISSION_M061_FOLDER, #Isis Event in CoV
    'MM_M060_E0763': MAIN_M060_FOLDER, #Tao Talisman Event at the beginning of Taito
    'MM_M064_E2797': MAIN_M064_FOLDER, #Qadistu Talisman/Periapt
    'MM_M064_E2795_Direct': MAIN_M064_FOLDER, #Tsukuyomi Talisman
    'BP_JakyoEvent': SHOP_EVENT_FOLDER, #Cathedral of Shadows Event
    'MM_M061_EM0020': M061_FOLDER, # The Angel's Request
    'BP_ShopEvent': SHOP_EVENT_FOLDER, #First Miman Reward
}

#Key: EventScriptName, Value: Type for what and where to search for values to be changed
SCRIPT_JOIN_TYPES = {
    'MM_M061_EM1630': Script_Join_Type.CODE, # The Water Nymph 
    'MM_M061_EM1640': Script_Join_Type.CODE, # The Spirit of Love 
    'MM_M062_EM1660': Script_Join_Type.ENTRYDEVILID, # Holding The Line
    'MM_M062_EM1650': Script_Join_Type.ENTRYDEVILID, # Those Seeking Sanctuary
    'MM_M060_EM1690': Script_Join_Type.ENTRYDEVILID, # Raid on Tokyo, Files are same but I got 177252 instead for the Adrammelech location
    'MM_M060_EM1700': Script_Join_Type.ENTRYDEVILID, # In Defense of Tokyo
    'MM_M063_EM1670': Script_Join_Type.ENTRYDEVILID, # Black Frost Strikes Back
    'MM_M063_EM1680': Script_Join_Type.ENTRYDEVILID, # A Sobering Standoff
    'MM_M064_EM2310': Script_Join_Type.ENTRYNKMID, # Reclaim the Golden Stool 
    'MM_M064_EM2320': Script_Join_Type.ENTRYNKMID, # Liberate the Golden Stool
    'MM_M064_EM2270': Script_Join_Type.CODE, # The Vampire in Black
    'MM_M064_EM2280': Script_Join_Type.CODE, # The Hunter in White
    'MM_M060_EM1420': Script_Join_Type.CODE, # Fionn's Resolve
    'MM_M060_EM1602': Script_Join_Type.CODE, # The Destined Leader (Amanazako Could't Join Initially), not 100% sure on v1.02 locations
    'MM_M060_EM1601': Script_Join_Type.CODE, # The Destined Leader 
    'MM_M016_E0885': Script_Join_Type.CODE, #Hayataro CoC Chaos
    'MM_M016_E0885_Direct': Script_Join_Type.CODE, #Hayataro CoC Chaos
    'MM_M016_EM1450': Script_Join_Type.CODE, # A Plot Revealed
    'MM_M035_EM1480': Script_Join_Type.CODE, # The Seraph's Return
    'MM_M036_EM1490': Script_Join_Type.CODE, # The Red Dragon's Invitation
    'MM_M061_EM1781': Script_Join_Type.CODE, # Rage of a Queen
    'MM_M061_EM2613_HitAction': Script_Join_Type.CODE, # Holy Will and Profane Dissent
    'MM_M030_EM1769': Script_Join_Type.MEPHISTO, # Bethel Researcher giving DLC Demons
    'MM_M061_EM1791': Script_Join_Type.CODE, # A Goddess in Training
    'MM_M061_EM2601': Script_Join_Type.NKMID, # Sakura Cinders of the East
    'MM_M063_EM2170': Script_Join_Type.MASAKADO, # Guardian of Tokyo
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
    #'MM_M061_EM2050': [-5], # Picture-Perfect Debut TODO:Neither the M061 nor the M050 version seem to edit the item correctly
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
    'MM_M061_E2610' : [-20], #Isis Story Event in CoV (Part of Quest: Rescue Miyazu Atsuta)
    'MM_M061_EM0020': [-21], #The Angel's Request
}
#Ids of missions where the reward of fake mission should be added to info screen
EXTRA_MISSION_MISSION_INFO_IDS = {
    -1: [74], # The Destined Leader
    -2: [50,221], # The Seraph's Return
    -3: [51,222], #The Red Dragon's Invitation
    -4: [8], # Cursed Mermaids
    -5: [153],# Picture-Perfect Debut
    -6: [33], #Downtown Rock 'n Roll
    -7: [39], #Keeper of the North
    -8: [38], #Keeper of the West
    -9: [36], #Keeper of the South
    -10: [35], #Keeper of the East
    -11: [47],#A Plot Revealed
    -12: [86], #Movin' on Up
    -13: [48], #Gold Dragon's Arrival
    -14: [73,147], #A Power Beyond Control
    -15: [209], #Holy Will and Profane Dissent
    -16: [208], #Sakura Cinders of the East
    -17: [183], #Rascal of the Norse
    -18: [39], #Keeper of the North(Periapt)
    -20: [111], #Rescue Miyazu Atsuta
    -21: [5], #The Angel's Request
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
    'esNPC_m016_02a': 715, #Elemental Oni Periapt
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
  16: ['esNPC_m016_02a','BP_JakyoEvent','BP_JakyoEvent_Comp_Complete'], #Empyrean
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
    'esNPC_m016_02a' : ['esNPC_m016_02b'],
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
  
class Script_File_List:
    def __init__(self):
        self.files = []
        self.fileNames = []
        self.nameCorrections = {}

    '''
    Returns a script_file for the given script name. 
    If there is no script_file for the given name in the list, the file is created by reading the uasset and uexp.
    '''
    def getFile(self,name):
        if name not in self.fileNames:
            self.readFile(name)

        index = self.fileNames.index(name)
        return self.files[index]

    '''
    Set the file of the given script name to the given script_file.
    '''
    def setFile(self,name,file):
        index = self.fileNames.index(name)
        self.files[index] = file

    '''
    Writes the uasset and uexp for every file in the list to their respective folder.
    '''
    def writeFiles(self):
        for index, name in enumerate(self.fileNames):
            folderKey = name
            if folderKey not in SCRIPT_FOLDERS.keys():
                folderKey = getEquivalentSource(name)
            
            file = self.files[index]
            writeBinaryTable(file.uexp.buffer, SCRIPT_FOLDERS[folderKey] + '/' + name + '.uexp', SCRIPT_FOLDERS[folderKey])
            writeBinaryTable(file.uasset.binaryTable.buffer, SCRIPT_FOLDERS[folderKey] + '/' + name + '.uasset', SCRIPT_FOLDERS[folderKey])
    
    '''
    Read the binary data of the files belonging to the script of the given name and create a Script_File and add it to the list.
    '''
    def readFile(self,name):
        if 'NPC' in name:
            scriptPath = 'NPC/'
        elif 'ShopEvent' in name or 'JakyoEvent' in name:
            scriptPath = 'ShopEvent/'
        elif 'EM' in name and not 'DevilTalk' in name:
            scriptPath = 'SubMission/'
        else:
            scriptPath = 'MainMission/'
        uexp = readBinaryTable('base/Scripts/' + scriptPath + name + '.uexp')
        uassetData = Script_Uasset(readBinaryTable('base/Scripts/' +scriptPath + name + '.uasset'))
        self.fileNames.append(name)
        self.files.append((Script_File(uassetData,uexp)))

class Script_File:
    def __init__(self,uasset, uexp):
        self.uasset = uasset 
        self.uexp = uexp

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
    scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
'''
def randomizeDemonJoins(replacements, randomDemons,scriptFiles):
    #These demons appear in multiple scripts and should be the same in both
    amanozako = None
    hayataro = None
    cleopatra = None
    dagda = None

    for script, type in SCRIPT_JOIN_TYPES.items():
        #Get Script from script list
        file = scriptFiles.getFile(script)
        uexpData = file.uexp
        uassetData = file.uasset
        
        if randomDemons:#randomize the join demons, otherwise values stay the same as OG and potential output files are overwritten with vanilla files
            oldDemon = numbers.SCRIPT_JOIN_DEMONS[script]
            newDemon = replacements[oldDemon]

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

            updateDemonJoinInScript(uassetData,uexpData,oldDemon,newDemon,type)
        
            #Exception for Dagda/Cleo not being recruited during their Quest in some cases but at the researcher instead, which is a different script
            if script == 'MM_M030_EM1769':
                updateDemonJoinInScript(uassetData,uexpData,numbers.SCRIPT_JOIN_DEMONS['MM_M061_EM1781'],cleopatra,Script_Join_Type.CLEOPATRA)
                updateDemonJoinInScript(uassetData,uexpData,numbers.SCRIPT_JOIN_DEMONS['MM_M061_EM2613_HitAction'],dagda,Script_Join_Type.DAGDA )

        #Update script entry in list with changed file
        scriptFiles.setFile(script,file)

'''
Updates the old demon that joins in the script to the new demon.
    Parameters:
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        joinType (Script_Join_Type): the type that decides which functions to search for in the uexp
'''
def updateDemonJoinInScript(uassetData: Script_Uasset, uexpData: Table, oldDemonID, newDemonID, joinType):
    byteList = []
    if joinType == Script_Join_Type.CODE: #Functions are in the script bytecode directly
        importedFunctions = {#In the Import Map and therefore have a negative index
            'IsEntryNkm' : 1,
            'EntryNkmBlank' : 1
            }

        namedFunctions = {}#none #In the Name Map and have positive index
        bonusBytes = {}#Additional extra bytes that apply to some functions from the name list
    else: #Functions are not in the bytecode directly and the value of joinType is equal to the searched function in the name map
        #Function or name searched is still in the Uexp
        entry = joinType.value
        importedFunctions = {}
        namedFunctions = {
            entry : 1
        }
        if joinType == Script_Join_Type.MEPHISTO or joinType == Script_Join_Type.CLEOPATRA or joinType == Script_Join_Type.DAGDA:
            #Have a different amount of bytes than all others
            bonusBytes = {
                entry : -1
            }
        else: #Normal amount of bytes between name and id
            bonusBytes = {
                entry : 16
            }

    for name, number in importedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.IMPORT, number)
    for name, number in namedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.NAME, number, bonusBytes[name])

    for offset in byteList: #find bytes that were found but don't correspond to the oldDemonID
        if uexpData.readWord(offset) != oldDemonID:
            continue
        uexpData.writeWord(newDemonID, offset)

'''
Changes the reward for collecting the first miman which is rewarded via an reward.
    Parameters:
        config (Settings): randomization settings
        itemNames (List(String)): list of names of items
        replacements (Dict): dictionary listing which demon replaces which demon
        essenceArr (List(Essence)): list of essences
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
'''
def adjustFirstMimanEventReward(config, itemNames, replacements, essenceArr, scriptFiles):
    #Grab file from file list
    file = scriptFiles.getFile('BP_ShopEvent')
    scriptData = file.uexp
    uassetData = file.uasset

    ogEssenceID = 496 #Id for Onmoraki's Essence
    essenceID = 496 #Start with Onmoraki's Essence and change value later
    if config.randomizeMimanRewards and not config.scaleItemsToArea:
        #Grab random essence if item rewards not scaling
        validEssences = []
        for itemID, itemName in enumerate(itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
            if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES:
                validEssences.append(itemID)
        essenceID = random.choice(validEssences)
    elif (config.randomDemonLevels or config.randomizeMimanRewards) and config.scaleItemsToArea:
        #Grab essence for Onmoraki's Replacement
        demonID = replacements[290]
        for essence in essenceArr:
            if essence.demon.value == demonID:
                essenceID = essence.ind

    updateItemRewardInScript(uassetData, scriptData, ogEssenceID, essenceID)
    scriptFiles.setFile('BP_ShopEvent',file)

'''
Updates the old item given through the script to the new item.
    Parameters:
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        #TODO: Include amount??
'''
def updateItemRewardInScript(uassetData: Script_Uasset, uexpData: Table, oldItemID, newItemID):
    
    byteList = []
    
    #FunctionName : desired Parameter
    importedFunctions = { #In the Import Map and therefore have a negative index
        'ItemGet': 1,
        'ItemGetNum': 1,
        }
    namedFunctions = { #In the Name Map and have positive index
        'IItemWindowSetParameter': 1,
        'IMsgSetRichTextValueParam': 2 #Second parameter is itemID
    }
    
    #Get the offsets where the function is called or used in the bytecode
    for name, number in importedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.IMPORT, number)
    for name, number in namedFunctions.items():
        byteList = byteList + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.NAME, number)

    for offset in byteList:
        if uexpData.readHalfword(offset) != oldItemID:
            continue #skip offsets where the oldItemID is not set
        uexpData.writeHalfword(newItemID, offset) #update with newItemID else
        #print(str(oldItemID) + " -> " + str(newItemID) + " (" + str(len(byteList)))

'''
Creates fake missions from certain event scripts involving quests, that have more than one reward.
    Parameters:
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
    Returns a list of fake missions
'''
def createFakeMissionsForEventRewards(scriptFiles):
    fakeMissions = []

    for script, indeces in EXTRA_MISSION_IDS.items():
        for index in indeces:
            fakeMission = Fake_Mission()
            fakeMission.ind = index
            fakeMission.reward = EXTRA_MISSION_REWARDS[fakeMission.ind]
            fakeMission.originalReward = copy.deepcopy(fakeMission.reward)

            file = scriptFiles.getFile(script)
            uexpData = file.uexp
            uassetData = file.uasset 

            fakeMission.uexp = uexpData
            fakeMission.uasset = uassetData
            fakeMission.script = script
            
            fakeMissions.append(fakeMission)

    return fakeMissions

'''
Writes the updated reward data to the event scripts and removes the fake missions from the mission array.
    Parameters:
        missionArr (List(Mission)): a list of all missions and fake missions
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
    Returns list of all fake missions after being removed from missionArr
'''
def updateAndRemoveFakeMissions(missionArr,scriptFiles):
    toRemove = []
    fakeMissions = []
    for index, mission in enumerate(missionArr):
        if mission.ind < 0: #if mission is fake mission
            try: #add fakemission and their info mission ids to list
                mission.infoInds = EXTRA_MISSION_MISSION_INFO_IDS[mission.ind]
                fakeMissions.append(mission)
            except KeyError:
                pass

            file = scriptFiles.getFile(mission.script)

            #print(str(mission.ind) + ": " + str(mission.originalReward.ind) + " -> " + str(mission.reward.ind) )
            updateItemRewardInScript(file.uasset, file.uexp, mission.originalReward.ind, mission.reward.ind)

            scriptFiles.setFile(mission.script,file)

            toRemove.append(mission)
    for mission in toRemove:
        missionArr.remove(mission)
    return fakeMissions

'''
Replaces the a demon model with the model of another demon in the given script.
    Parameters:
        script(String): the name of the script
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
        ogDemonID (Integer): the id of the demon that should be replaced
        replacementDemonID (Integer): the id of the replacement demon
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
'''
def replaceDemonModelInScript(script, file: Script_File, ogDemonID, replacementDemonID, scriptFiles: Script_File_List):
    uexpData = file.uexp
    uassetData = file.uasset

    #TODO: Figure out where to better read the csv data
    modelNameMap = pd.read_csv(paths.MODEL_NAMES, dtype=str)
    modelNames = {}
    demonIDModelID = {}
    hasSimpleBP = {}
    hasIdleB = {}
    for index, row in modelNameMap.iterrows():
        if type(row['MainDemonID']) is str:
             modelNames[row['Number']] = row['folderName']
             demonIDModelID[int(row['MainDemonID'])] = row['Number']
             hasSimpleBP[int(row['MainDemonID'])] = row['HasSimpleBP']
             hasIdleB[int(row['MainDemonID'])] = row['HasIdleB']

    #Get the Strings corresponding to the old demon
    oldIDString = demonIDModelID[ogDemonID]
    oldName = modelNames[oldIDString]
    #Get the Strings corresponding to the new demon
    newIDString = demonIDModelID[replacementDemonID]
    newName = modelNames[newIDString]
    #print("CHECK: " + oldName + " -> " + newName)

    lengthDifference = len(newName) - len(oldName)

    for index, name in enumerate(uassetData.nameList): #change occurences of oldDemonID and oldDemonName in all names in the uasset
        if oldIDString in name:
            uassetData.nameList[index] = uassetData.nameList[index].replace(oldIDString,newIDString)
        if oldName in name:
            uassetData.nameList[index] = uassetData.nameList[index].replace(oldName,newName)
        
    if 'False' == hasSimpleBP[replacementDemonID]:
        #If the demon does not have a simple model blueprint use the general model blueprint
        for index, name in enumerate(uassetData.nameList): 
            if "_Simple" in name and newIDString in name:
                uassetData.nameList[index] = uassetData.nameList[index].replace("_Simple","")
    #Update maps in uasset before moving on
    uassetData.updateNameMap()
    
    #Find offsets for where the demonID needs to be updated in function calls
    demonModelIDBytes =[]
    namedFunctions = {
        'BPL_AdjustMapSymbolScale': 2,
    }
    bonusBytes = {
        'BPL_AdjustMapSymbolScale': 12,
    }
    for name, number in namedFunctions.items():
        demonModelIDBytes = demonModelIDBytes + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.NAME, number, bonusBytes[name])

    
    for offset in demonModelIDBytes: #remove bytes that were mistakingly found and do not set the ogDemonID in number form
        if uexpData.readWord(offset) != ogDemonID:
            continue
        uexpData.writeWord(replacementDemonID, offset)
    
    #Find potential offsets for where the the asset paths need to be updated with the new demon info
    demonModelAssetStringBytes = []
    importedFunctions = {
        'LoadAsset': 1,
        'PrintString' : 1,
        }
    bonusBytes = {
        'LoadAsset': 2,
        'PrintString': 1,
    }

    for name, number in importedFunctions.items():
        demonModelAssetStringBytes = demonModelAssetStringBytes + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.IMPORT, number,bonusBytes[name] )
    
    demonModelAssetStringBytes.sort(reverse=True) #sort offsets so that inserting/removing bytes does not effect offsets that come after in the list
    for offset in demonModelAssetStringBytes:
        offsetString = uexpData.readUntilEmptyByte(offset).decode('ascii')
        if oldIDString in offsetString: 
            #if the oldID is there in string format, replace with new string
            offsetString = offsetString.replace(oldIDString,newIDString)
        if oldName not in offsetString: 
            #if oldName is not in string, nothing else needs to be updated and string can be written
            offsetString = offsetString.encode('ascii')
            uexpData.writeXChars(offsetString, len(offsetString), offset)  
        elif oldName in offsetString: 
            #oldName is in string so needs to be updated
            if lengthDifference != 0:#newName is not the same length
                #Main script bytecode function is executeUbergraph which always starts by jumping to the whatever "EntryPoint" is set to
                
                # This happens at the beginning and is therefore a set byte distance away from where the ScriptByteCodeSize (how many statements) 
                # and the Amount of Bytes of the Script byte code has in total is which is th true goal 
                executeUbergraphNameID = uassetData.nameMap["EntryPoint"]
                potentialEntryPointOffsets = uexpData.findWordOffsets(executeUbergraphNameID) #Potential offsets
                entryPointGoToOffset = potentialEntryPointOffsets[0]
                for ep in potentialEntryPointOffsets:
                    check = uexpData.readWord(ep -4)
                    check2 = uexpData.readHalfword(ep -6)
                    if check == 1 and check2 == 78: #These bytes for the computated entryPoint jump are always in front of it, so the correct one needs to have them
                        entryPointGoToOffset = ep
                        break
                #print(entryPointGoToOffset)
                
                scriptByteCodeSize = uexpData.readWord(entryPointGoToOffset - 19) #Descripes how many instructions the bytecode contains(I believe)
                scriptByteCodeByteSize = uexpData.readWord(entryPointGoToOffset - 15)#Describes how many bytes the bytecode takes up

                
               
                #Create the new String with the newDemonName and transform to bytes at the end
                newString = offsetString.replace(oldName,newName)
                #TODO: Animation check if length is different
                #Change Animation if the demon does not have the required animation
                if '02idleB' in newString  and 'False' == hasIdleB[replacementDemonID]:
                    newString = newString.replace('02idleB','05attack')
                stringBytes = newString.encode('ascii')


                #Grab 8 bytes pre string, the original string, and 49 bytes post string
                ogStringBytes = uexpData.getXBytes(offset, len(offsetString))
                preStringBytes = uexpData.getXBytes(offset-8,8)
                postStringBytes = uexpData.getXBytes(offset + len(offsetString), 49)
                #TODO: Currently takes the popexecutionflow with them but if there is an event where there is no popexecutionflow after loading the asset this wouldn't work
                #Create bytearrays of the original and the new
                originalTotalBytes = preStringBytes + ogStringBytes + postStringBytes
                totalBytes = preStringBytes + stringBytes +postStringBytes

                # Figure out end of bytecode by checking where the next export begins and looking backwards
                endInsertOffset = uassetData.exports[1].serialOffset - len(uassetData.binaryTable.buffer) - 12
                
                #Insert new string at the end
                uexpData.insertBytes(endInsertOffset,totalBytes)

                #jumpBack = bytearray(5)
                #uexpData.insertBytes(endInsertOffset + len(totalBytes),jumpBack)
                #uexpData.writeByte(6,endInsertOffset + len(totalBytes))
                #TODO: Figuring out if there is a way to find out where to jump back to the original location of the asset loading. Preferably without having to count the instructions from the start
                #uexpData.writeWord(21024,endInsertOffset + len(totalBytes) +1)
                #uexpData.writeWord(len(totalBytes) - len(preStringBytes) + ,endInsertOffset + len(totalBytes) +1)
                #additionalLength = len(totalBytes) + 5 #Jump back is 5
                additionalLength = len(totalBytes) 

                #Replace original bytes with jump to newly inserted and fill rest with nothing instructions so statement index is the same
                startOffset = offset - 8
                uexpData.writeByte(6,startOffset) #6 indicates a jump instruction, with a word long offset to jump to afterwards
                uexpData.insertBytes(startOffset +1, bytearray(4)) 
                additionalLength += 4
                uexpData.writeWord(scriptByteCodeSize,startOffset +1)

                for i in range(len(originalTotalBytes) - 1):
                    uexpData.writeByte(0xB, startOffset +5 + i)# 0xB indicates a nothing instruction, one byte long
                
                #Update script byte code sizes
                scriptByteCodeSize = scriptByteCodeSize + additionalLength
                scriptByteCodeByteSize = scriptByteCodeByteSize + additionalLength
                uexpData.writeWord(scriptByteCodeSize,entryPointGoToOffset - 19)
                uexpData.writeWord(scriptByteCodeByteSize,entryPointGoToOffset - 15)

                #update export data in uasset
                uassetData.updateExportSizeAndOffsets(offset,additionalLength)
            else:
                # if length is the same just replace it and write it afterwards
                offsetString = offsetString.replace(oldIDString,newIDString).replace(oldName,newName)
                offsetString = offsetString.encode('ascii')
                uexpData.writeXChars(offsetString, len(offsetString), offset)

    #update data in uasset and its binary table and then set the file to the script file list        
    uassetData.writeDataToBinaryTable()
    scriptFiles.setFile(script,file)

'''
Replaces the model of the talk tutorial pixie with the demon who the given ID belongs to.
    Parameters:
        replacementDemonID (Integer): id of the demon to replace pixie model
'''
def replaceTutorialPixieModel(replacementDemonID,scriptFiles):
    script = 'EM_M061_DevilTalk'
    file = scriptFiles.getFile(script)
    replaceDemonModelInScript(script, file, 59, replacementDemonID,scriptFiles)

'''
Updates all script data regarding item gifts.
    Parameters:
    gifts(List(Gift_Item)): list of all gifts
    scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
'''
def updateGiftScripts(gifts, scriptFiles):
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
        #print(correctScript + " " + str(gift.item.ind))
        if 'NPC' in correctScript: #NPC data tables are handled here   
            file = scriptFiles.getFile(correctScript)
            uexpData = file.uexp
            uassetData = file.uasset
            if gift.script in GIFT_EXTRA_SCRIPTS.values(): # add uexp to dict if script has additional versions
                uexpCorrection[gift.script] = uexpData
            if correctScript in uexpCorrection.keys(): #get already modified uexp from correct script
                uexpData = uexpCorrection[correctScript]
            if any(gift.script in scripts for scripts in GIFT_EQUIVALENT_SCRIPTS.values()): #if script was copied as equivalent, use original base item
                equivalentScript = getEquivalentSource(gift.script)
                #print(gift.script + " -> EQ " + equivalentScript +" " +  str(gift.item.ind))
                updateNPCGiftInScript(BASE_GIFT_ITEMS[equivalentScript], gift.item.ind, uassetData, uexpData)
            else:
                #print(gift.script + " "+ str(gift.item.ind))
                updateNPCGiftInScript(BASE_GIFT_ITEMS[gift.script], gift.item.ind, uassetData, uexpData)
        else: #else it is an event script
            file = scriptFiles.getFile(correctScript)
            uexpData = file.uexp
            uassetData = file.uasset
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

        scriptFiles.setFile(correctScript,file)

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
    byteList = []
    namedFunctions = [
        'E_EVENT_SCRIPT_TYPE::NewEnumerator52', #Enum entry ItemAdd2 per E_EVENT_SCRIPT_TYPE.uasset
    ]
    bonusBytes = {
        'E_EVENT_SCRIPT_TYPE::NewEnumerator52': 33,
    }
    for name in namedFunctions:
        byteList = byteList + uassetData.getOffsetsForRowInNPCDataTable(uexpData,name,Script_Function_Type.NAME, bonusBytes[name])

    for offset in byteList:
        if uexpData.readHalfword(offset) != oldItemID:
            continue
        uexpData.writeHalfword(newItemID, offset)
