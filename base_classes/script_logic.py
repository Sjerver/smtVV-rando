import random
import os
from util.binary_table import Table
import util.paths as paths
import util.numbers as numbers

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
SHOP_EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/ShopEvent'

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
    'MM_M063_EM2170': M063_FOLDER # Guardian of Tokyo
}


'''
Randomizes free demon joins based on the original joins level by adjusting the values in the corresponding event scripts.
Parameters:
    comp List(Compendium_Demon): list of all playable demons
    randomDemons (Boolean): whether to randomize the demon joins or set them to vanilla
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
                scriptData.writeHalfword(dagda.ind,602953)
                scriptData.writeHalfword(cleopatra.ind,602941)

        writeBinaryTable(scriptData.buffer, SCRIPT_FOLDERS[script] + '/' + script + '.uexp', SCRIPT_FOLDERS[script] )


def adjustFirstMimanEventReward(config, compendium, itemNames):
    scriptData = readBinaryTable('base/Scripts/ShopEvent/BP_ShopEvent.uexp')
    byteList = [14113, 26035, 11754, 14361,14407, 21063,21109]

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

    for byte in byteList:
        scriptData.writeHalfword(essenceID, byte)
    
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