from script_logic import Script_File, Script_File_List
from base_classes.script import Script_Function_Type,Script_Uasset
from base_classes.umap import UMap_File, UMap_File_List
from base_classes.message import Demon_Sync
from base_classes.uasset import UAsset
from util.binary_table import readBinaryTable
import util.paths as paths
import util.numbers as numbers
import pandas as pd

MODEL_NAMES = {}
DEMON_ID_MODEL_ID = {}
HAS_SIMPLE_BP = {}
HAS_IDLE_B = {}
HAS_SKILL_COMPOSITE = {}

#List of which level umaps event scripts use for their location and sizes
#To find out, look at which MapEventID the Script has in its File and then take a look at map event data
LEVEL_UASSETS = {
    'EM_M061_DevilTalk' : 'LV_MainMission_M061',
    'MM_M061_EM1630': 'LV_EventMission_M061',
    'MM_M061_EM1631': 'LV_EventMission_M061',
    'MM_M061_EM1640': 'LV_EventMission_M061',
    'MM_M061_EM1640_Hit': 'LV_EventMission_M061',
}

#List of events that require updated scaling to trigger events with large demons
REQUIRES_HIT_UPDATE = [
    'MM_M061_EM1630','MM_M061_EM1631', 'MM_M061_EM1640'
]

#Script files for events and what demon models need to be updated in htem
#Demon_Sync(demonID in file, if different from demonID in file: demonID to take replacement from)
EVENT_SCRIPT_MODELS = {
    'EM_M061_DevilTalk': [Demon_Sync(59)], #Talk Tutorial (Pixie)
    'MM_M061_EM1630': [Demon_Sync(305)], # The Water Nymph (Leanan)
    'MM_M061_EM1631': [Demon_Sync(316,867)], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Demon_Sync(43)], # The Spirit of Love (Apsaras)
    'MM_M061_EM1640_Hit': [Demon_Sync(43)], # The Spirit of Love First Entry (Apsaras)
}

#For bosses that do not use their own model, which model they should use instead
MODEL_SYNC = {
    775: 103, #Yamata-no-Orochi 8 turn
    476: 249, #Melchizedek
    487: 114, #Copy of School Aitvaras
    442: 114, #School Aitvaras
    431: 305, #Three Pretas
    805: 206, #Zochouten 2 Press Turns
    455: 25, #Ishtar
    830: 88, #Mithras
    888: 318, #Oni
    755: 341, #Pisaca
    880: 67, #Lilim
    #TODO: Complete before this can truly work for bosses
}



'''
Reads data about models from the model names csv and fills dictionaries.
'''
def initDemonModelData():
    modelNameMap = pd.read_csv(paths.MODEL_NAMES, dtype=str)
    for index, row in modelNameMap.iterrows():
        if type(row['MainDemonID']) is str:
             MODEL_NAMES[row['Number']] = row['folderName']
             DEMON_ID_MODEL_ID[int(row['MainDemonID'])] = row['Number']
             HAS_SIMPLE_BP[int(row['MainDemonID'])] = row['HasSimpleBP']
             HAS_IDLE_B[int(row['MainDemonID'])] = row['HasIdleB']
             try:
                HAS_SKILL_COMPOSITE[int(row['MainDemonID'])] = row['HasSkillComposite']
             except KeyError:
                 continue  

'''
Updates the models used in events.
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
'''
def updateEventModels(encounterReplacements, bossReplacements, scriptFiles):
    initDemonModelData()
    umapList = UMap_File_List()
    for script, syncDemons in EVENT_SCRIPT_MODELS.items():
        file = scriptFiles.getFile(script)
        umap = umapList.getFile(LEVEL_UASSETS[script])
        for syncDemon in syncDemons:
            
            originalDemonID = syncDemon.ind
            syncDemonID = syncDemon.sync
            if syncDemonID > numbers.NORMAL_ENEMY_COUNT: # if demon to get replacement from is a normal enemy
                try:
                    replacementID = bossReplacements[syncDemonID]
                except KeyError:
                    #print("Key Error: " + str(syncDemonID))
                    continue
            else: #else it is a boss
                try:
                    replacementID = encounterReplacements[syncDemonID]
                except KeyError:
                    #print("Key Error: " + str(syncDemonID))
                    continue
            try:
                replacementID = MODEL_SYNC[replacementID]
            except KeyError:
                pass
            #TODO: Multiple demon model swaps do not work yet??
            file = replaceDemonModelInScript(script, file, originalDemonID, replacementID, scriptFiles)
            
           
            if script in REQUIRES_HIT_UPDATE: #TODO: add hitbox size checks, aka only if hitbox of demon is larger
                #TODO: add calculation for scaling based on hitbox increase
                scale = 2 #For now just double event hit size
                umap = updateEventHitScaling(umap,script,scale)
        
        scriptFiles.setFile(script,file)
    umapList.writeFiles()




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

    #Get the Strings corresponding to the old demon
    oldIDString = DEMON_ID_MODEL_ID[ogDemonID]
    oldName = MODEL_NAMES[oldIDString]
    #Get the Strings corresponding to the new demon
    try:
        newIDString = DEMON_ID_MODEL_ID[replacementDemonID]
    except KeyError:
        print(str(replacementDemonID) + " needs a model tied to it. Stopping replacement")
        return file
    newName = MODEL_NAMES[newIDString]
    print("SWAP: " + oldName + " -> " + newName + " in " + script)

    #TODO: Duplicate Name Map Entries, aka two demons in one file get replaced by the same one
    for index, name in enumerate(uassetData.nameList): #change occurences of oldDemonID and oldDemonName in all names in the uasset
        if oldIDString in name:
            uassetData.nameList[index] = uassetData.nameList[index].replace(oldIDString,newIDString)
        if oldName in name:
            uassetData.nameList[index] = uassetData.nameList[index].replace(oldName,newName)
        
    if 'False' == HAS_SIMPLE_BP[replacementDemonID]:
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
    importedFunctions = { #each parameter is 5 bytes after
        'LoadAsset': 1,
        'PrintString' : 1,
        'LoadAssetClass': 1,
        }
    bonusBytes = {
        'LoadAsset': 2,
        'PrintString': 1,
        'LoadAssetClass': 2,
    }

    for name, number in importedFunctions.items():
        demonModelAssetStringBytes = demonModelAssetStringBytes + uassetData.getOffsetsForParamXFromFunctionCalls(uexpData,name,Script_Function_Type.IMPORT, number,bonusBytes[name] )
    
    demonModelAssetStringBytes.sort(reverse=True) #sort offsets so that inserting/removing bytes does not effect offsets that come after in the list
    for offset in demonModelAssetStringBytes:
        offsetString = uexpData.readUntilEmptyByte(offset).decode('ascii')
        newString = offsetString.replace(oldName,newName)
        #Change Animation if the demon does not have the required animation
        newString = replaceNonExistentAnimations(newString, replacementDemonID)
        
        lengthDifference = len(newString) - len(offsetString)
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
                newString = replaceNonExistentAnimations(newString, replacementDemonID)
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
    return file

def replaceNonExistentAnimations(string, replacementDemonID):
    #TODO: Maybe make this depending on script??
    #TODO: Find a better way to define what animations each demon has
    if '02idleB' in string  and 'False' == HAS_IDLE_B[replacementDemonID]:
        string = string.replace('02idleB','05attack')
    if '06skill_Composite' in string  and 'False' == HAS_SKILL_COMPOSITE[replacementDemonID]:
        string = string.replace('06skill_Composite','06skill')
    return string


'''
Modifies the scaling for the event hit trigger of the given script by the scale given.
    umap(UMap_File): file containing the umap and uexp data
    script(String): name of the script the event hit should be updated for
    scale(Float): by what the current scale should be multiplied
'''
def updateEventHitScaling(umap: UMap_File,script,scale):
    uasset = umap.uasset
    uexp = umap.uexp
    
    #Get NameID for EventHit
    eventHitNameID = uasset.nameList.index('EventHit')

    #Find export for the script data and find which export handles it's eventhit
    scriptExport = next(exp for exp in uasset.exports if exp.objectName == script)
    calculatedOffset = scriptExport.serialOffset - len(uasset)
    nextEventHitNameOffset = uexp.findNextWordOffsetFromOffset(eventHitNameID, calculatedOffset) + 0x19
    eventHitExportID = uexp.readWord(nextEventHitNameOffset) - 1
    eventHitExport = uasset.exports[eventHitExportID]

    #Get scaling parameters, update and then write them
    scalingOffsets = eventHitExport.serialOffset - len(uasset) + 0xA8
    scalingParam1 = uexp.readFloat(scalingOffsets)
    scalingParam2 = uexp.readFloat(scalingOffsets+4)
    scalingParam3 = uexp.readFloat(scalingOffsets+8)

    scalingParam1 *= scale
    scalingParam1 *= scale
    scalingParam1 *= scale

    uexp.writeFloat(scalingParam1, scalingOffsets)
    uexp.writeFloat(scalingParam2, scalingOffsets + 4)
    uexp.writeFloat(scalingParam3, scalingOffsets + 8)


    return umap