import random
import os
from util.binary_table import Table, readBinaryTable, writeBinaryTable, writeFolder
import util.paths as paths
import util.numbers as numbers
from base_classes.script import Script_Function_Type, Script_Uasset, Script_Join_Type, Bytecode
from base_classes.quests import Mission_Reward, Fake_Mission
from base_classes.uasset_custom import UAsset_Custom
import copy
import json
import csv

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
    'MM_M061_EM2705': Script_Join_Type.CODE, # Guardian of Light
    'MM_M061_EM1782': Script_Join_Type.CODE, # Cleopatra Quest (Full Party Event)
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
    'MM_M087_E2450_Direct': 4, #Bead (Dazai Gift Temple CoV)
    'MM_M061_EM0181': 4, #Bead (Amanozako Event)
}
# Areas the gifts are scaled after if they are not containing a key item
GIFT_AREAS = {
  16: ['esNPC_m016_02a','BP_JakyoEvent','BP_JakyoEvent_Comp_Complete'], #Empyrean
  35: [], #Temple of Eternity
  36: ['MM_M064_E2797','MM_M064_E2797_PERIAPT','MM_M064_E2795_Direct'], #Demon Kings Castle / Shakan
  38: [], #Demon Kings Castle / Shakan
  60: ['esNPC_m060_10a','MM_M062_EM1132','MM_M060_E0763'], #Taito
  61: ['esNPC_m061_31a','esNPC_m061_30a','esNPC_m061_34a','MM_M061_EM0181'], #Minato
  62: ['esNPC_m062_32a','esNPC_m062_33a','esNPC_m062_40a'], #Shinagawa
  63: ['BP_esNPC_TokyoMap_15b','esNPC_m063_20a','esNPC_m063_21a','MM_M087_E2450_Direct'], #Chiyoda
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
VENGEANCE_EXCLUSIVE_GIFTS = ['MM_M064_E2797','MM_M064_E2797_PERIAPT','MM_M064_E2795_Direct','MM_M087_E2450_Direct']
#List of gifts that require a cleared game file
NEWGAMEPLUS_GIFTS = ['BP_JakyoEvent_Comp_Complete', 'BP_JakyoEvent']
#List of gifts that can be missed
MISSABLE_GIFTS = ['MM_M061_EM0181']
#Script for the Tsukuyomi Talisman
TSUKUYOMI_TALISMAN_SCRIPT = 'MM_M064_E2795_Direct'

#Message files for the event in which item names need to be replaced
ITEM_MESSAGE_REPLACEMENTS = {
    'MM_M061_EM0181': 'em0181'
}

#Stores original expressions from script calls
ORIGINAL_SCRIPT_FUNCTION_CALLS = {}

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
        jsonData = file.json
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

            updateDemonJoinInScript(file,oldDemon,newDemon,type,script)
        
            #Exception for Dagda/Cleo not being recruited during their Quest in some cases but at the researcher instead, which is a different script
            if script == 'MM_M030_EM1769':
                updateDemonJoinInScript(file,numbers.SCRIPT_JOIN_DEMONS['MM_M061_EM1781'],cleopatra,Script_Join_Type.CLEOPATRA,script)
                updateDemonJoinInScript(file,numbers.SCRIPT_JOIN_DEMONS['MM_M061_EM2613_HitAction'],dagda,Script_Join_Type.DAGDA,script )

        #Update script entry in list with changed file
        scriptFiles.setFile(script,file)

'''
Updates the old demon that joins in the script to the new demon.
    Parameters:
        file (Script_File): file of the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        joinType (Script_Join_Type): the type that decides which functions to search for in the uexp
        scriptName (String): name of the script
'''
def updateDemonJoinInScript(file, oldDemonID, newDemonID, joinType,scriptName):
    jsonData = file.json
    if joinType == Script_Join_Type.CODE: #Demon ID is set in the script bytecode
        bytecode = None
        try: #get bytecode if UAssetAPI can parse it
            bytecode = Bytecode(jsonData["Exports"][0]['ScriptBytecode'])
        except KeyError: #otherwise stop and note error
            print("Script Byte Code only in raw form")
            return
        
        importNameList = [imp['ObjectName'] for imp in jsonData['Imports']]
        #These Imports are functions where the demon id to join gets passed as parameter
        relevantImportNames = ['IsEntryNkm','EntryNkmBlank']
        relevantImports = {}
        for imp in relevantImportNames: #Determine import id for relevant import names which is always negative
            relevantImports[imp] = -1 * importNameList.index(imp) -1
        
        # go through functions and find where expressions call them
        for imp,stackNode in relevantImports.items():
            expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
            expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_FinalFunction', stackNode))
            for exp in expressions:
                demonValue = exp['Parameters'][0]['Value']
                if demonValue == oldDemonID: #only replace old demonID with new one
                    exp['Parameters'][0]['Value'] = newDemonID
                    #print(scriptName + ": (DEMON) " + str(oldDemonID) + " -> " + str(newDemonID))
    else: #Demon ID is set as Data for an export
        searchName = joinType.value #value of join type is the name of the data we search for
        relevantExportName = "Default__" + scriptName + "_C" #Export name for script data

        relevantExport = next(exp for exp in jsonData["Exports"] if exp['ObjectName'] == relevantExportName)
        
        for data in relevantExport['Data']:
            if data['Name'] == searchName: #The value here is unique per script so no need to check for old demon ID
                data['Value'] = newDemonID
                #print(scriptName + ": (DEMON) " + str(oldDemonID) + " -> " + str(newDemonID))
            if data['Name'] == 'CanEntryDevil_Label_to_ID': #Exception for demons that join at researcher
                for subData in data['Value']:
                    if subData[0]['Value'] == searchName:
                        subData[1]['Value'] = newDemonID
                        #print(scriptName + ": (DEMON) " + str(oldDemonID) + " -> " + str(newDemonID))
                        break
    file.updateFileWithJson(jsonData)                    

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

    ogEssenceID = 496 #Id for Onmoraki's Essence
    # essenceID = 496 #Start with Onmoraki's Essence and change value later
    # if config.randomizeMimanRewards and not config.scaleItemsToArea:
    #     #Grab random essence if item rewards not scaling
    #     validEssences = []
    #     for itemID, itemName in enumerate(itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
    #         if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES:
    #             validEssences.append(itemID)
    #     essenceID = random.choice(validEssences)
    # elif (config.randomDemonLevels or config.randomizeMimanRewards) and config.scaleItemsToArea:
    #     #Grab essence for Onmoraki's Replacement
    #     demonID = replacements[290]
    #     for essence in essenceArr:
    #         if essence.demon.value == demonID:
    #             essenceID = essence.ind
    #TODO: What are we doing with actual return pillar spawn?
    essenceID = 70 #Return Pillar

    updateItemRewardInScript(file, ogEssenceID, essenceID, 'BP_ShopEvent')
    scriptFiles.setFile('BP_ShopEvent',file)

'''
Updates the old item given through the script to the new item.
    Parameters:
        file (Script_File): the file for the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        scriptName (String): the name of the script file
        newItemAmount (Number): amount for the new item
'''
def updateItemRewardInScript(file, oldItemID, newItemID,scriptName,newItemAmount = 1):
    jsonData = file.json
    bytecode = None
    try: #get bytecode if UAssetAPI can parse it
        exportNameList = [exp['ObjectName'] for exp in jsonData["Exports"]]
        executeUbergraph = "ExecuteUbergraph_" + scriptName
        exportIndex = exportNameList.index(executeUbergraph)

        bytecode = Bytecode(jsonData["Exports"][exportIndex]['ScriptBytecode'])
    except KeyError: #otherwise stop and note error
        print("Script Byte Code only in raw form")
        return
    
    relevantImportNames = ['ItemGet','ItemGetNum']
    relevantFunctionNames = ['IItemWindowSetParameter', 'IMsgSetRichTextValueParam']

    #grab original function calls, so that only calls for the original item get replaced to prevent chain replacements
    if scriptName not in ORIGINAL_SCRIPT_FUNCTION_CALLS.keys():
        ogFunctionCalls = getOriginalFunctionCalls(jsonData,bytecode, relevantImportNames,relevantFunctionNames)
        ORIGINAL_SCRIPT_FUNCTION_CALLS[scriptName] = ogFunctionCalls
    else:
        ogFunctionCalls = ORIGINAL_SCRIPT_FUNCTION_CALLS[scriptName]
    importNameList = [imp['ObjectName'] for imp in jsonData['Imports']]
    #These Imports are functions where the demon id to join gets passed as parameter
    
    relevantImports = {}
    for imp in relevantImportNames: #Determine import id for relevant import names which is always negative
        if imp in importNameList:
            relevantImports[imp] = -1 * importNameList.index(imp) -1
    for imp,stackNode in relevantImports.items():
            expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
            expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_FinalFunction', stackNode))
            ogExpressions = ogFunctionCalls[imp]
            for index,exp in enumerate(expressions):
                ogItemValue = ogExpressions[index]['Parameters'][0].get('Value')
                if ogItemValue == oldItemID:
                    exp['Parameters'][0]['Value']= newItemID
                    #print(scriptName + ": " + str(oldItemID) + " -> " + str(newItemID))
                    if imp == 'ItemGet':
                        exp['Parameters'][1]['Value']= newItemAmount
    
    
    for func in relevantFunctionNames:
        expressions = bytecode.findExpressionUsage("UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVirtualFunction", virtualFunctionName= func)
        ogExpressions = ogFunctionCalls[func]
        for index,exp in enumerate(expressions):
            if func == 'IItemWindowSetParameter':
                ogItemValue = ogExpressions[index]['Parameters'][0].get('Value')
                itemValue = exp['Parameters'][0].get('Value')
                if ogItemValue == oldItemID:
                    exp['Parameters'][0]['Value']= newItemID
                    #print(scriptName + ": " + str(oldItemID) + " -> " + str(newItemID))
            if func == 'IMsgSetRichTextValueParam':
                ogItemValue = ogExpressions[index]['Parameters'][1].get('Value')
                itemValue = exp['Parameters'][1].get('Value')
                if ogItemValue == oldItemID:
                    exp['Parameters'][1]['Value']= newItemID
                    #print(scriptName + ": " + str(oldItemID) + " -> " + str(newItemID))
    file.updateFileWithJson(jsonData)

'''
Returns a copy of function calls in the bytecode.
Parameters:
    jsonData (json): jsonData form of the uasset file
    bytecode (Bytecode): bytecode object of the bytecode instructions
    relevantImportNames (List(String)): list of imported functions to get calls from
    relevantFunctionNames (List(String)): list of virtual functions to get calls from
'''
def getOriginalFunctionCalls(jsonData,bytecode,relevantImportNames,relevantFunctionNames):
    functionCalls = {}
    importNameList = [imp['ObjectName'] for imp in jsonData['Imports']]
    relevantImports = {}
    for imp in relevantImportNames: #Determine import id for relevant import names which is always negative
        if imp in importNameList:
            relevantImports[imp] = -1 * importNameList.index(imp) -1
    for imp,stackNode in relevantImports.items():
            expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
            expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_FinalFunction', stackNode))
            functionCalls[imp] = copy.deepcopy(expressions)
    for func in relevantFunctionNames:
        expressions = bytecode.findExpressionUsage("UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVirtualFunction", virtualFunctionName= func)
        functionCalls[func] = copy.deepcopy(expressions)  

    return functionCalls


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
            jsonData = file.json
            uassetData = file.uasset 

            fakeMission.json = jsonData
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
            updateItemRewardInScript(file, mission.originalReward.ind, mission.reward.ind, mission.script, mission.reward.amount)

            scriptFiles.setFile(mission.script,file)

            toRemove.append(mission)
    for mission in toRemove:
        missionArr.remove(mission)
    return fakeMissions

'''
Updates all script data regarding item gifts.
    Parameters:
    gifts(List(Gift_Item)): list of all gifts
    scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
    itemReplacementMap(Dict): Mapping of what items replace what items in events
'''
def updateGiftScripts(gifts, scriptFiles, itemReplacementMap):
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
            if any(gift.script in scripts for scripts in GIFT_EQUIVALENT_SCRIPTS.values()): #if script was copied as equivalent, use original base item
                equivalentScript = getEquivalentSource(gift.script)
                #print(gift.script + " -> EQ " + equivalentScript +" " +  str(gift.item.ind))
                updateNPCGiftInScript(BASE_GIFT_ITEMS[equivalentScript], gift.item.ind, file, correctScript,gift.item.amount)
            else:
                #print(gift.script + " "+ str(gift.item.ind))
                updateNPCGiftInScript(BASE_GIFT_ITEMS[gift.script], gift.item.ind, file, correctScript,gift.item.amount)
        else: #else it is an event script
            file = scriptFiles.getFile(correctScript)
            if any(gift.script in scripts for scripts in GIFT_EQUIVALENT_SCRIPTS.values()): #if script was copied as equivalent, use original base item
                equivalentScript = getEquivalentSource(gift.script)
                updateItemRewardInScript(file,BASE_GIFT_ITEMS[equivalentScript],gift.item.ind, correctScript, gift.item.amount)
                if equivalentScript in ITEM_MESSAGE_REPLACEMENTS.keys():
                    itemReplacementMap.update({ITEM_MESSAGE_REPLACEMENTS[equivalentScript] : {BASE_GIFT_ITEMS[equivalentScript] : gift.item.ind}})
            else:
                #print(gift.script + ": " + str(BASE_GIFT_ITEMS[gift.script]) + " -> " + str(gift.item.ind) )
                updateItemRewardInScript(file,BASE_GIFT_ITEMS[gift.script],gift.item.ind,correctScript,gift.item.amount)
                if gift.script in ITEM_MESSAGE_REPLACEMENTS.keys():
                    itemReplacementMap.update({ITEM_MESSAGE_REPLACEMENTS[gift.script] : {BASE_GIFT_ITEMS[gift.script] : gift.item.ind}})

        scriptFiles.setFile(correctScript,file)

'''
Updates the old item given through the npc script to the new item.
    Parameters:
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        file (Script_File): the file for script data
        script (String): the name of the script
'''   
def updateNPCGiftInScript(oldItemID, newItemID, file, script,newItemAmount = 1):
    jsonData = file.json
    #Find export for script name
    export = next(exp for exp in jsonData['Exports'] if exp['ObjectName'] == script)

    dataList = export['Table']['Data']
    for data in dataList: #go through table to find correct script type to change value for
        values = data['Value']
        if values[0].get('EnumValue') == 'E_EVENT_SCRIPT_TYPE::NewEnumerator52':
            if values[1].get('Value') == oldItemID:
                values[1]['Value'] = newItemID
                values[2]['Value'] = newItemAmount
                #print(script + ": " + str(oldItemID) + " -> " + str(newItemID))
                #values[2] would then be amount
    file.updateFileWithJson(jsonData)

'''
Updates the usage of skills in an ai script file.
    Parameters:
        file (Script_File): the file for the script
        skillReplacements (Dict): map skills and their replacement skills
        scriptName (String): the name of the script file
    Returns debug dictionary for script skill results.
'''
def updateSkillsInAIScript(file, skillReplacements, scriptName):
    #print(scriptName)
    jsonData = file.json
    bytecode = None
    exportNameList = [exp['ObjectName'] for exp in jsonData["Exports"]]
    totalRelevantInstanceVars = set() #saves the total list of all relevant instance variables for the whole script file

    #Debug dictionary that saves information about the replacement process
    potentiallyUnchangedExps =  {
        "SkillNotInList" : [],
        "BI_ActSkill Param": [],
        'BI_ChkMyUsedSkillIDAct Param': [],
        'InstanceVar Param': [],
        'LocalVar Param': [],
        'MemberStruct Param': [],
        'Array Param': [],
        'InstanceVar Initial': [],
        'SkillInList': [],
    }
    #Functions from certain AI scripts that output a skillID in some form
    localFuncOutParams = [
            'BtlAI_e064_KsmOrDeath',
            'BtlAI_e096_SkillList',
            'BtlAIe098_SelectSkill',
            'BtlAIe123_SkillList',
            'GetChangeNormalAtk',
            'GetSkillRate_LusterCandy',
            'GetUseSkill_SecondAct',
            'SelMudoOrLfDrin',
            'SelBarionSkill',
            'ChkRakusei',
            'GetPtnAndSkills',
            'SelUseSkill',
            'BtlAIe121_ChkSukukaja',
            'BtlAIe121_NormalAct',
            'BtlAI_e064_YoroiOrZetu',
            'GetSkillRate',
            'GetUseSkillforTgt' #AI 199
        ]
    #Common names of properties in exports that represent skillIDs
    commonPropertyNames = [
        'UseSkill','Var_UseSkill','UseSkillID','SkillAID','SkillBID'

    ]
    for mainIndex, export in enumerate(exportNameList):
        
        try: #get bytecode if UAssetAPI can parse it
            bytecode = Bytecode(jsonData["Exports"][mainIndex]['ScriptBytecode'])
        except KeyError: #errors seemed to be irrelevant so just kip here
            #print("Script Byte Code only in raw form")
            continue

        #storing names of relevant variables that contain skillIDs
        relevantLocalVars = set()
        relevantInstanceVars = set() 
        relevantStructMemberContexts = set()

        relevantStructMemberContexts.add("m_SkillId") #used in structs for quite a lot of things
        relevantLocalVars.add('Lo_SkillId') #otherwise not found in AI 140 and some others
        
        # storing names of variables that contain skillIDs and have been already processed
        processedInstanceVars  = set()
        processedLocalVars   = set()
        processedStructMembers   = set()
        
        if export in localFuncOutParams: #check if export outputs skillID   
            for property in jsonData["Exports"][mainIndex]['LoadedProperties']:
                if 'CPF_OutParm' in property['PropertyFlags']:
                    relevantLocalVars.add(property['Name'])
        

        #Names of imported functions that might contain skill ids in their parameters
        relevantImportNames = [
            'Array_Get', #used in at least AI 140
            'EqualEqual_IntInt',#
            'NotEqual_IntInt', #
            'Array_Add', #AI 099, 199
        ]
        #Names of virtual functions that might contain skill ids in their first parameters
        relevantFunctionNames = [ 
            'BI_ActSkill','BI_ChkMyUsedSkillIDAct',
            'BI_ChkENUsedSkillIDTurn', #Only Amanozako (AI 119)
            'BI_ChkMyUsedSkillID', #AI (141, 134)
            'BI_ChkMyUsedSkillIDTurn',
            'BI_Chk_ENUsedSkillID',
            #'BI_Chk_PLUsedSkillID', Checks if player uses certain skills
            'BI_GetHojoSkillValidTarget',
            'BI_GetPLNumVaildSkill',
            'BI_GetPLNumVaildSkill_ENAnalyze',
            'BI_GetSelUseSkill',
            'CallActSkill', # AI 140
            'UseSkillTarRand', #AI 054
            'BI_GetSkillHaveBst', #AI 007 (Might be problematic if skill does not inflict status?)
            'MyUseSkill', #AI 021
            'SelectAction', #AI 165
            'UseSkillTarRand', #AI 047,111
            'ActSkill', #AI 122,177
            'SelUseSkill', #AI 202 First Parameter ChkSkillID
            'CallActSkill_DevilId', #AI 139
            'CallActSkill_Random', #AI 139,
            'CallActSkill_ENAnalyze', #AI 139
            'Act_FirstAttack', #AI 150,149,148,153,147
            'Act_ChohatuCure', #AI 149
            'Act_Chohatsu', #AI 150,152,149,151,153,147
            "Act Add", #AI 189,190,191
            "Act Ohmaga0", #AI 189,190,191
            "Act Ohmaga1", #AI 189,190,191
            "Act Ohmaga2", #AI 189,190,191
            'DecideUseSkill', #AI 192
            'UseSkillTarID', #AI 154
            'BtlAIe121_NormalAct', #AI 121
            'GetSkillRate', #AI 140
            'UpDate_UseSkillData', #AI 137
        ] 
        #Virtual functions where the skillID is not (only) in the first parameter
        specificParameters = {
            'Act_Chohatsu': [1,2],
            "Act Add": [0,1],
            "Act Ohmaga0": [0,1],
            "Act Ohmaga1": [0,1],
            "Act Ohmaga2": [0,1],
            'DecideUseSkill': [1,2],
            'BtlAIe121_NormalAct': [0,3],
        }               
        
        #Misceallenous notes
        #AI 024 has check for 386 Diarama (Thoth in Khonsu Ra Fight(No one there has diarama or uses it?))
        #AI 171 has check for 148 Impaler's Animus (Dazai (Impaler's is only on Abdiel))
        
        #Okuninushi(822) 041 has check for 139 (from Oyamatsumi 825)
        #Orobas(817) 016 has checks for 214/216 (from Moloch 816)
        #Flauros(818) 023 has checks for 214/216/3 (from Moloch 816) and for 10 from Oroboas 817
        #Anubis(517) 010 has check for 323 from Khonsu Ra  519
        #Thoth(518) 024 has check for 323 from Khonsu Ra  519
        #Amanozako(876) 119 has check for 117 Heavenly Counter Active Part
        
        #Demi-fiend(934) 139 uses skillID 372 to check if 397 can hit everything?

        #TODO: NKMBase AI for Demifiend/Satan/Tiamat??
        #Not yet analyzed AI files?, (Lucifer P2/3, Tsukuyomi Clones)

        #grab original function calls, so that only calls for the original item get replaced to prevent chain replacements
        if scriptName + export not in ORIGINAL_SCRIPT_FUNCTION_CALLS.keys():
            ogFunctionCalls = getOriginalFunctionCalls(jsonData,bytecode, relevantImportNames,relevantFunctionNames)
            ORIGINAL_SCRIPT_FUNCTION_CALLS[scriptName+ export] = ogFunctionCalls
        else:
            ogFunctionCalls = ORIGINAL_SCRIPT_FUNCTION_CALLS[scriptName+export]
        
        importNameList = [imp['ObjectName'] for imp in jsonData['Imports']]
        relevantImports = {}
        for imp in relevantImportNames: #Determine import id for relevant import names which is always negative
            if imp in importNameList:
                relevantImports[imp] = -1 * importNameList.index(imp) -1

        
        relevantExportName = scriptName + "_C" #Export name for main object class data
        relevantExport = next(exp for exp in jsonData["Exports"] if exp['ObjectName'] == relevantExportName)
        for property in relevantExport['LoadedProperties']:
            if property['Name'] in commonPropertyNames:
                relevantInstanceVars.add(property['Name'])
                
        

        relevantExportName = "Default__" + scriptName + "_C" #Export name for default main object class data
        relevantExport = next(exp for exp in jsonData["Exports"] if exp['ObjectName'] == relevantExportName)
        for data in relevantExport['Data']:
            if data['$type'] == 'UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI':
                if 'pattern' not in data['Name']: #Exception for Surt 019 and Decarabia 027
                    relevantInstanceVars.add(data['Name'])
            elif data['$type'] == 'UAssetAPI.PropertyTypes.Objects.ArrayPropertyData, UAssetAPI':
                if data['Name'] == 'OhmagaHPArray':
                    #Exception for Arahabaki AI054 who has both skill 80 and an array with hp threshold
                    continue
                if data['Value'][0]['$type'] == 'UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI':
                    relevantInstanceVars.add(data['Name']) 
        
        '''
        Processes Expression to check for skillIds to replace.
            Parameters:
                parameter(Expression): the parameter of the given expression to process
                exp(Expression): the original version of the parameter that should not be changed
                func(String): the name of the current function
        '''
        def processExpression(parameter, exp, func):
            #print(func + " " + scriptName)
            if parameter['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_IntConst, UAssetAPI':
                ogSkillValue = parameter.get('Value')
                if ogSkillValue in skillReplacements:
                    newSkill = skillReplacements[ogSkillValue]
                    exp['Value'] = newSkill
                    potentiallyUnchangedExps["SkillInList"].append(str(ogSkillValue) + " from " + func + " Param")
                else:
                    potentiallyUnchangedExps["SkillNotInList"].append(str(ogSkillValue) + " from " + func + " Param")
            
            elif parameter['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_InstanceVariable, UAssetAPI':
                pathList = parameter['Variable']['New']['Path']
                for path in pathList:
                    relevantInstanceVars.add(path)
            
            elif parameter['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVariable, UAssetAPI' or parameter['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalOutVariable, UAssetAPI':
                pathList = parameter['Variable']['New']['Path']
                for path in pathList:
                    relevantLocalVars.add(path)
                
            elif parameter['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_SwitchValue, UAssetAPI':
                cases = parameter['Cases']
                for caseIndex, case in enumerate(cases):
                    caseContent = case['CaseTerm']
                    processExpression(caseContent, exp['Cases'][caseIndex]['CaseTerm'], func)

            elif parameter['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_SetArray, UAssetAPI':
                elementList = parameter['Elements']
                if all(element['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_IntConst, UAssetAPI' for element in elementList) and all(element['Value'] in skillReplacements.keys() or element['Value'] == 0 for element in elementList):
                    for elementIndex, element in enumerate(elementList):
                        processExpression(element,exp['Elements'][elementIndex],func + " Elements")
                else:
                    for elementIndex, element in enumerate(elementList):
                        potentiallyUnchangedExps['Array Param'].append(element)

            else:
                if func + " Param" not in potentiallyUnchangedExps.keys():
                    potentiallyUnchangedExps[func + " Param"] = []
                potentiallyUnchangedExps[func + " Param"].append(parameter)

        '''
        Processes a list of relevant variables of a given type.
            Parameters:
                relevantVars(List(String)): list of names of relevant variables
                type(String): type of the variables
        '''
        def processRelevantVars(relevantVars, type):
            for var in relevantVars:
                #print(type + " " + var + " " + scriptName)
                if type == 'LocalVar':
                    expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_Let,', localVariable=var)
                    expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_SetArray,', array=var))
                    expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_Let,', localOutVar=var))
                elif type == 'InstanceVar':
                    expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_Let,', instanceVariable=var)
                    expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_SetArray,', array=var))
                elif type == 'MemberStruct':
                    expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_Let,', structMemberContext=var)
                    expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_SetArray,', array=var))

                if not expressions:
                    continue
                ogExpressions = copy.deepcopy(expressions)
                ORIGINAL_SCRIPT_FUNCTION_CALLS[scriptName + export].update({var + export: ogExpressions})
                for index, exp in enumerate(expressions):
                    if ogExpressions[index]['$type'] == 'UAssetAPI.Kismet.Bytecode.Expressions.EX_Let, UAssetAPI':
                        valueExpression = ogExpressions[index]['Expression']
                        processExpression(valueExpression, exp['Expression'],var + " " +type)
                    elif ogExpressions[index]['$type'] =='UAssetAPI.Kismet.Bytecode.Expressions.EX_SetArray, UAssetAPI':
                        valueExpression = ogExpressions[index]
                        processExpression(valueExpression, exp,var + " " +type)
                    # else:
                    #     print(ogExpressions[index]['$type'])

        # go through relevant imported functions
        for imp,stackNode in relevantImports.items(): 
                expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
                expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_FinalFunction', stackNode))
                ogExpressions = ogFunctionCalls[imp]
                for index,exp in enumerate(expressions):
                    if imp == 'Array_Get': 
                        parameters = ogExpressions[index]['Parameters']
                        for parameterIndex, parameter in enumerate(parameters):
                            processExpression(parameter,exp['Parameters'][parameterIndex],imp)
                    elif imp == 'Array_Add': 
                        parameters = ogExpressions[index]['Parameters']
                        for parameterIndex, parameter in enumerate(parameters):
                            processExpression(parameter,exp['Parameters'][parameterIndex],imp)
        
         # go through relevant virtual functions
        for func in relevantFunctionNames:
            expressions = bytecode.findExpressionUsage("UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVirtualFunction", virtualFunctionName= func)
            ogExpressions = ogFunctionCalls[func]
            for index,exp in enumerate(expressions):
                if ogExpressions[index].get('Parameters'):
                    if func in specificParameters.keys():
                        for paramIndex in specificParameters[func]:
                            parameter = ogExpressions[index]['Parameters'][paramIndex]
                            processExpression(parameter,exp['Parameters'][paramIndex],func)
                    else:
                        parameter = ogExpressions[index]['Parameters'][0]
                        processExpression(parameter,exp['Parameters'][0],func)

        breakCondition = True
        while breakCondition: #process variables until there are no more left to process
            instanceVars = [var for var in relevantInstanceVars if var not in processedInstanceVars]
            localVars = [var for var in relevantLocalVars if var not in processedLocalVars]
            memberStructs = [var for var in relevantStructMemberContexts if var not in processedStructMembers]

            processRelevantVars(instanceVars, 'InstanceVar')
            processRelevantVars(localVars, 'LocalVar')
            processRelevantVars(memberStructs, 'MemberStruct')

            processedInstanceVars.update(instanceVars)
            processedLocalVars.update(localVars)
            processedStructMembers.update(memberStructs)

            if len(processedInstanceVars) >= len(relevantInstanceVars) and len(processedLocalVars) >= len(relevantLocalVars) and len(processedStructMembers) >= len(relevantStructMemberContexts):
                breakCondition = False
        totalRelevantInstanceVars.update(processedInstanceVars)

        # go through relevant imported functions, this time handle comparisons for which we need to know relevant variables
        for imp,stackNode in relevantImports.items(): 
            expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
            expressions.extend(bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_FinalFunction', stackNode))
            ogExpressions = ogFunctionCalls[imp]
            for index,exp in enumerate(expressions):
                if imp == 'EqualEqual_IntInt' or imp == 'NotEqual_IntInt':
                    parameters = ogExpressions[index]['Parameters']
                    if parameters[0].get("Variable"):
                        varname = parameters[0]["Variable"]["New"]["Path"][0]
                        if varname in processedInstanceVars or varname in processedLocalVars:
                            processExpression(parameters[1],exp['Parameters'][1],imp)
                    elif parameters[1].get("Variable"):
                        varname = parameters[1]["Variable"]["New"]["Path"][0]
                        if varname in processedInstanceVars or varname in processedLocalVars:
                            processExpression(parameters[0],exp['Parameters'][0],imp)
   
 
        # Some AI files might also relate to others (the ones for Arioch & Decarabia I believe for example)
        
    
    #initial values for instance variables
    # relevantExportName = "Default__" + scriptName + "_C" #Export name for script data
    # relevantExport = next(exp for exp in jsonData["Exports"] if exp['ObjectName'] == relevantExportName)
    for data in relevantExport['Data']:
        if data['Name'] == 'OhmagaHPArray':
            #Exception for Arahabaki AI054 who has both skill 80 and an array with hp threshold
            continue
        if data['Name'] in totalRelevantInstanceVars:
            #print(data['Name']) 
            if data['$type'] == 'UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI':
                ogSkillValue = data['Value']
                if ogSkillValue in skillReplacements.keys():
                    newSkill = skillReplacements[ogSkillValue]
                    data['Value'] = newSkill
                    potentiallyUnchangedExps["SkillInList"].append(str(ogSkillValue) + " from " + data['Name'] + " Initial ")
                else:
                    potentiallyUnchangedExps["SkillNotInList"].append(str(ogSkillValue) + " from " + data['Name'] + " Initial")
            elif data['$type'] == 'UAssetAPI.PropertyTypes.Objects.ArrayPropertyData, UAssetAPI':
                for element in data['Value']:
                    if element['$type'] == 'UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI':
                        ogSkillValue = element['Value']
                        if ogSkillValue in skillReplacements.keys():
                            newSkill = skillReplacements[ogSkillValue]
                            element['Value'] = newSkill
                            potentiallyUnchangedExps["SkillInList"].append(str(ogSkillValue) + " from " + data['Name'] + " Initial ")
                        else:
                            potentiallyUnchangedExps["SkillNotInList"].append(str(ogSkillValue) + " from " + data['Name'] + " Initial")

            

            
    file.updateFileWithJson(jsonData)
    return potentiallyUnchangedExps


'''
Updates ai scripts according to the skill replacement map.
    Parameters:
        skillReplacements (Dict): map of bosses and their skills and replacement skills
        bossArr(List(Enemy_Demon)): list of bosses
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
'''
def aiUpdate(skillReplacementMap, bossArr, scriptFiles):
    infoDict = {}
    for demonID in skillReplacementMap.keys():
        demon = bossArr[demonID]
        ai = str(demon.AI).zfill(3)
        if ai in ["000","055"]:
            #000 is for lahmu tentacles, or nuwa thunder bits
            #055 is random so no need to modify it at all
            continue

        #print(demon.name + " " + ai)

        fileName = "BtlAI_e" + ai
        if fileName in scriptFiles.fileNames:
            #To prevent chain replacements for bosses that use the same AI (example: Abdiel in CoC/CoV)
            continue
        file = scriptFiles.getFile(fileName)
        infoDict.update({demon.name + "(" + str(demon.ind) + ")" + " " + ai  : updateSkillsInAIScript(file,skillReplacementMap[demonID],fileName)})
        scriptFiles.setFile(fileName,file)
        scriptFiles.writeFile(fileName,file)

    with open(paths.SKILL_REPLACEMENT_FAILS, "w") as file:
        for demon, categories in infoDict.items():
            file.write(f"### {demon} ###\n")
            for category, values in categories.items():
                file.write(f"{category}:\n")
                if isinstance(values, list):
                    for item in values:
                        file.write(f"  - {item}\n")
                else:
                    file.write(f"  {values}\n")
            file.write("\n")
    with open(paths.SKILL_REPLACEMENTS, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Demon Name","Script File", "Original Skill ID", "New Skill ID"])  # Header

        for demon, replacements in skillReplacementMap.items():
            for old_skill, new_skill in replacements.items():
                writer.writerow([bossArr[demon].name,"BtlAI_e" +str(bossArr[demon].AI).zfill(3), old_skill, new_skill])