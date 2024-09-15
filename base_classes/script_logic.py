import random
import os
from util.binary_table import Table
import util.paths as paths
import util.numbers as numbers
from enum import IntEnum
from base_classes.quests import Mission_Reward, Fake_Mission
import copy

class Import_Entry:
    def __init__(self):
        self.classPackageIndex = None
        self.classNameIndex = None
        self.classPackage = None
        self.className = None
        self.outerIndex = None
        self.objectNameIndex = None
        self.objectName = None

class Script_Function_Type(IntEnum):
    IMPORT = 0
    NAME = 1

class Script_Uasset:
    def __init__(self, binaryTable: Table):
        self.nameCount = binaryTable.readWord(0x29)
        self.nameOffset = binaryTable.readWord(0x2D)
        
        self.importCount = binaryTable.readWord(0x41)
        self.importOffset = binaryTable.readWord(0x45)

        self.nameList = []#Index -> Name
        self.nameMap = {}#Name -> Index
        currentOffset = self.nameOffset
        for index in range(self.nameCount): # get all names
            stringSize = binaryTable.readWord(currentOffset)
            if stringSize < 0: #indicates whether chars are two or one byte
                #Includes japanese characters, and is therfore originally negative and needs to be doubled since they are 2 bytes each
                stringSize = stringSize * -2
                name = binaryTable.readXChars(stringSize,currentOffset + 4)
                name = name.decode("utf-16")
            else:
                name = binaryTable.readXChars(stringSize,currentOffset + 4)
                name = str(name)[2:-5]
            
            self.nameList.append(name) #Index -> Name
            self.nameMap[name] = index #Name -> Index

            currentOffset = currentOffset + stringSize + 8

        self.importMap = {} #Index -> Import
        self.reverseImportMap = {} #Import ObjectName -> Index
        currentOffset = self.importOffset

        for index in range(self.importCount): #get all imports
            newImport = Import_Entry()
            newImport.classPackageIndex = binaryTable.readWord(currentOffset)
            newImport.classNameIndex = binaryTable.readWord(currentOffset + 8)
            newImport.outerIndex = binaryTable.readWord(currentOffset + 16)
            newImport.objectNameIndex = binaryTable.readWord(currentOffset + 20)

            newImport.classPackage = self.nameList[newImport.classPackageIndex]
            newImport.className = self.nameList[newImport.classNameIndex]
            newImport.objectName = self.nameList[newImport.objectNameIndex]

            self.importMap[-1 * index -1] = newImport #Index -> Import
            self.reverseImportMap[newImport.objectName] = -1* index -1 #Import ObjectName -> Index

            currentOffset = currentOffset + 28

    '''
    Returns a list of offsets for all function calls in uexp of the given function where the specified parameter is passed.
        Parameter:
            uexp (Table): the uexp binary data where the function calls are searched in
            functionName (String): the name of the function to search for
            type (Script_Function_Type): in which mapping the functions id is located in
            paramNumber (Integer): which parameter of the function call to return the offset off
        Returns a list of offsets where the specified parameter is in a call of the function
    '''    
    def getOffsetsForParamXFromFunctionCalls(self, uexp: Table, functionName, type, paramNumber):
        additionalBytes = paramNumber * 5
        
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



EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event'
SCRIPT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script' 
SUBMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission'
MAINMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission' 
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
}

EXTRA_MISSION_REWARDS = {
    'MM_M060_EM1601': Mission_Reward(826, 1), #Fury Talisman
    'MM_M035_EM1480': Mission_Reward(711, 1), #Exalted Seraphim Periapt
    'MM_M036_EM1490': Mission_Reward(712, 1), #Macabre Family Periapt
    'MM_M061_EM1030': Mission_Reward(506, 1), #Mermaid Essence
    'MM_M050_EM2050': Mission_Reward(600, 1), #Amabie's Essence
    'MM_M060_EM1310': Mission_Reward(390, 1), #Fafnir's Essence
    'MM_M060_EM1370': Mission_Reward(440, 1), # Bishamonten's Essence
    'MM_M061_EM1360': Mission_Reward(442, 1), # Koumokuten's Essence
    'MM_M062_EM1340': Mission_Reward(443, 1), # Zouchouten's Essence
    'MM_M063_EM1350': Mission_Reward(441, 1), # Jikokuten's Essence
    'MM_M016_EM1450': Mission_Reward(713, 1), # Siblings of Olympus Periapt
    'MM_M061_EM1715': Mission_Reward(807, 1), #Raptor Talisman
    'MM_M060_EM1460': Mission_Reward(714, 1), # Cardinal Deity Periapt
    'MM_M063_EM1592': Mission_Reward(338, 1), # Amanozako's Essence
    'MM_M030_EM2610': Mission_Reward(721, 1), # Seeds of Dana Periapt
    'MM_M030_EM2600': Mission_Reward(732, 1), # Mountain Gods Periapt
    'MM_M060_EM2351': Mission_Reward(709, 1), # Asgardian Kin Periapt
}

EXTRA_MISSION_IDS = {
    'MM_M060_EM1601': -1, # The Destined Leader
    'MM_M035_EM1480': -2, # The Seraph's Return
    'MM_M036_EM1490': -3, # The Red Dragon's Invitation
    'MM_M061_EM1030': -4, # Cursed Mermaids
    'MM_M050_EM2050': -5, # Picture-Perfect Debut
    'MM_M060_EM1310': -6, # Downtown Rock 'n Roll
    'MM_M060_EM1370': -7, # Keeper of the North
    'MM_M061_EM1360': -8, # Keeper of the West
    'MM_M062_EM1340': -9, # Keeper of the South
    'MM_M063_EM1350': -10, # Keeper of the East
    'MM_M016_EM1450': -11, # A Plot Revealed
    'MM_M061_EM1715': -12, # Movin' on Up
    'MM_M060_EM1460': -13, # Gold Dragon's Arrival
    'MM_M063_EM1592': -14, # A Power Beyond Control
    'MM_M030_EM2610': -15, # Holy Will and Profane Dissent
    'MM_M030_EM2600': -16, # Sakura Cinders of the East (Periapt Event)
    'MM_M060_EM2351': -17, # Rascal of the Norse
}

EXTRA_MISSION_REWARD_AREAS = {
  16: [-2, -3, -11], #Empyrean
  35: [], #Temple of Eternity
  36: [], #Demon Kings Castle / Shakan
  38: [], #Demon Kings Castle / Shakan
  60: [-1,-6,-7,-8,-9,-10,-13, -15, -17], #Taito
  61: [-4,-12], #Minato
  62: [-5], #Shinagawa
  63: [-14, -16], #Chiyoda
  64: [], #Shinjuku
  107: [] #Demi-Fiend Area: same as Empyrean
}



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
    
    #if len(byteList) > 0:
    #    print(str(oldItemID) + " -> " + str(newItemID))

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

    for script, index in EXTRA_MISSION_IDS.items():
        fakeMission = Fake_Mission()
        fakeMission.ind = index
        fakeMission.reward = EXTRA_MISSION_REWARDS[script]
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
            
            updateItemRewardInScript(mission.uasset, mission.uexp, mission.originalReward.ind, mission.reward.ind)

            writeFolder(SCRIPT_FOLDERS[mission.script])
            writeBinaryTable(mission.uexp.buffer, SCRIPT_FOLDERS[mission.script] + '/' + mission.script + '.uexp', SCRIPT_FOLDERS[mission.script])

            toRemove.append(mission)
    for mission in toRemove:
        missionArr.remove(mission)
    return missionArr


