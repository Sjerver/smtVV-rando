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

    updateItemRewardInScript(file, ogEssenceID, essenceID, 'BP_ShopEvent')
    scriptFiles.setFile('BP_ShopEvent',file)

'''
Updates the old item given through the script to the new item.
    Parameters:
        file (Script_File): the file for the script
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        scriptName (String): the name of the script file
        #TODO: Include amount??
'''
def updateItemRewardInScript(file, oldItemID, newItemID,scriptName):
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
    importNameList = [imp['ObjectName'] for imp in jsonData['Imports']]
    #These Imports are functions where the demon id to join gets passed as parameter
    relevantImportNames = ['ItemGet','ItemGetNum']
    relevantImports = {}
    for imp in relevantImportNames: #Determine import id for relevant import names which is always negative
        relevantImports[imp] = -1 * importNameList.index(imp) -1
    for imp,stackNode in relevantImports.items():
            expressions = bytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
            for exp in expressions:
                itemValue = exp['Parameters'][0].get('Value')
                if itemValue == oldItemID:
                    exp['Parameters'][0]['Value']= newItemID
                    #print(scriptName + ": " + str(oldItemID) + " -> " + str(newItemID))
                    if imp == 'ItemGet':
                        #TODO: 2nd Value is amount
                        pass
    
    relevantFunctionNames = ['IItemWindowSetParameter', 'IMsgSetRichTextValueParam']
    for func in relevantFunctionNames:
        expressions = bytecode.findExpressionUsage("UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVirtualFunction", virtualFunctionName= func)
        for exp in expressions:
            if func == 'IItemWindowSetParameter':
                itemValue = exp['Parameters'][0].get('Value')
                if itemValue == oldItemID:
                    exp['Parameters'][0]['Value']= newItemID
                    #print(scriptName + ": " + str(oldItemID) + " -> " + str(newItemID))
            if func == 'IMsgSetRichTextValueParam':
                itemValue = exp['Parameters'][1].get('Value')
                if itemValue == oldItemID:
                    exp['Parameters'][1]['Value']= newItemID
                    #print(scriptName + ": " + str(oldItemID) + " -> " + str(newItemID))
    file.updateFileWithJson(jsonData)

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
            updateItemRewardInScript(file, mission.originalReward.ind, mission.reward.ind, mission.script)

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
'''
def updateGiftScripts(gifts, scriptFiles):
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
                updateNPCGiftInScript(BASE_GIFT_ITEMS[equivalentScript], gift.item.ind, file, correctScript)
            else:
                #print(gift.script + " "+ str(gift.item.ind))
                updateNPCGiftInScript(BASE_GIFT_ITEMS[gift.script], gift.item.ind, file, correctScript)
        else: #else it is an event script
            file = scriptFiles.getFile(correctScript)
            if any(gift.script in scripts for scripts in GIFT_EQUIVALENT_SCRIPTS.values()): #if script was copied as equivalent, use original base item
                equivalentScript = getEquivalentSource(gift.script)
                updateItemRewardInScript(file,BASE_GIFT_ITEMS[equivalentScript],gift.item.ind, correctScript)
            else:
                #print(gift.script + ": " + str(BASE_GIFT_ITEMS[gift.script]) + " -> " + str(gift.item.ind) )
                updateItemRewardInScript(file,BASE_GIFT_ITEMS[gift.script],gift.item.ind,correctScript)

        scriptFiles.setFile(correctScript,file)

'''
Updates the old item given through the npc script to the new item.
    Parameters:
        oldItemID (Integer): the id of the old item to overwrite
        newItemID (Integer): the id of the new item that overwrites the old one
        file (Script_File): the file for script data
        script (String): the name of the script
        #TODO: Include amount??
'''   
def updateNPCGiftInScript(oldItemID, newItemID, file, script):
    jsonData = file.json
    #Find export for script name
    export = next(exp for exp in jsonData['Exports'] if exp['ObjectName'] == script)

    dataList = export['Table']['Data']
    for data in dataList: #go through table to find correct script type to change value for
        values = data['Value']
        if values[0].get('EnumValue') == 'E_EVENT_SCRIPT_TYPE::NewEnumerator52':
            if values[1].get('Value') == oldItemID:
                values[1]['Value'] = newItemID
                #print(script + ": " + str(oldItemID) + " -> " + str(newItemID))
                #values[2] would then be amount
    file.updateFileWithJson(jsonData)
