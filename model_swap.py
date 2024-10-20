from script_logic import Script_File, Script_File_List
from base_classes.script import Script_Function_Type,Script_Uasset
from base_classes.umap import UMap_File, UMap_File_List
from base_classes.message import Demon_Sync
from base_classes.demon_assets import Demon_Model
from base_classes.uasset import UAsset
from util.binary_table import readBinaryTable
import util.paths as paths
import util.numbers as numbers
import pandas as pd

class Anim_Sync():
    def __init__(self,ind, sync=None):
        self.ind = ind
        self.sync = ind
        if sync:
            self.sync = sync

MODEL_NAMES = {}
DEMON_ID_MODEL_ID = {}
HAS_SIMPLE_BP = {}
DEMON_MODELS={}

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
    'MM_M061_EM1630','MM_M061_EM1631',
    #'MM_M061_EM1640', #Does not have relativeScale3D in their EventHit TODO: ;ayne figure out how to add that? Otherwise big models make talking impossible
]

#Script files for events and what demon models need to be updated in htem
#Demon_Sync(demonID in file, if different from demonID in file: demonID to take replacement from)
EVENT_SCRIPT_MODELS = {
    'EM_M061_DevilTalk': [Demon_Sync(59)], #Talk Tutorial (Pixie)
    'MM_M061_EM1630': [Demon_Sync(305),Demon_Sync(43)], # The Water Nymph (Leanan)
    'MM_M061_EM1631': [Demon_Sync(316,867)], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Demon_Sync(43)], # The Spirit of Love (Apsaras)
    'MM_M061_EM1640_Hit': [Demon_Sync(43)], # The Spirit of Love First Entry (Apsaras)
    'MM_M061_E2610' : [Demon_Sync(193,579)], #CoV Isis Event Bethel Egypt #TODO:Dazai/Yuzuru are NPC Models how do they work
}

#Which animations are being played in scripts that might not be available to every demon and which to use instead
#Beware Capitalization!!
SCRIPT_ANIMS_REPLACEMENTS = {
    'EM_M061_DevilTalk': [Anim_Sync('02idleB','05attack')], #Talk Tutorial (Pixie)
    'MM_M061_EM1630': [Anim_Sync('06skill_Composite','06_skill')], # The Water Nymph (Leanan)
    'MM_M061_EM1631': [Anim_Sync('map/700000_event_idle', '01idleA')], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Anim_Sync('06skill_Composite','06_skill')], # The Spirit of Love (Apsaras)
    'MM_M061_EM1640_Hit': [Anim_Sync('map/700000_event_idle', '01idleA')], # The Spirit of Love First Entry (Apsaras)
    'MM_M061_E2610' : [], #CoV Isis Event Bethel Egypt
}

#For bosses that do not use their own model, which model they should use instead
MODEL_SYNC = {
    434: 272, # 2 Andras from Eligor
    577: 264, # Abdiel (Fallen)
    564: 240, # Abdiel (Shakan)
    467: 240, # Abdiel (Summit)
    884: 265, # Adramelech
    869: 44, # Agathion (with Apsaras)
    568: 392, # Agrat
    487: 114, # Aitvaras (School Copy)
    442: 114, # Aitvaras (School)
    473: 198, # Alilat
    831: 76, # Amon
    803: 20, # Anahita
    771: 41, # Anansi
    781: 272, # Andras (3x)
    488: 272, # Andras (School Copy)
    489: 272, # Andras (School Copy)
    490: 272, # Andras (School Copy)
    443: 272, # Andras (School)
    517: 120, # Anubis (CoC Summon)
    439: 287, # Anzu (Jozoji)
    728: 287, # Anzu (Single Abcess)
    605: 287, # Anzu (with Mishaguji)
    868: 43, # Apsaras
    463: 82, # Arioch
    930: 31, # Artemis
    829: 181, # Asura
    627: 12, # Atavaka
    776: 12, # Atavaka (with Rakshasa)
    837: 17, # Baal
    856: 126, # Baihu
    746: 235, # Baphomet
    628: 119, # Barong
    738: 113, # Basilisk
    483: 81, # Beelzebub
    840: 83, # Belial
    859: 203, # Bishamonten (2 Turn)
    863: 203, # Bishamonten (4 Turn)
    773: 171, # Black Ooze
    926: 352, # Black Rider
    814: 248, # Camael
    466: 182, # Chernobog
    486: 260, # Cherub
    931: 295, # Cleopatra
    611: 36, # Cu Chulainn
    618: 191, # Cybele
    947: 4, # Dagda
    922: 357, # Daisoujou
    612: 297, # Dakini
    843: 188, # Danu
    464: 273, # Decarabia (Summon)
    881: 183, # Dionysus
    780: 46, # Dís
    485: 255, # Dominion
    751: 141, # Dormarth
    725: 141, # Dormarth (Abcess)
    730: 47, # Efreet
    559: 394, # Eisheth
    433: 270, # Eligor
    602: 282, # Feng Huang
    833: 35, # Fionn mac Cumhaill (2nd)
    451: 35, # Fionn mac Cumhaill (First)
    732: 266, # Flauros (Abcess)
    474: 266, # Flauros (Summon)
    818: 266, # Flauros (With Moloch)
    883: 201, # Futsunushi
    836: 243, # Gabriel
    865: 278, # Garuda
    555: 142, # Glasya-Labolas (with Naamah)
    607: 34, # Hanuman
    562: 152, # Hayataro
    923: 356, # Hell Biker
    864: 13, # Horus
    844: 189, # Inanna
    495: 68, # Incubus (School Copy)
    496: 68, # Incubus (School Copy)
    497: 68, # Incubus (School Copy)
    498: 68, # Incubus (School Copy)
    720: 316, # Ippon-Datara (Abcess)
    867: 316, # Ippon-Datara (with Leanan)
    455: 25, # Ishtar
    579: 193, # Isis
    610: 193, # Isis (Abcess)
    802: 281, # Jatayu
    858: 204, # Jikokuten
    862: 204, # Jikokuten (4 Turn)
    606: 66, # Kaiwan
    516: 7, # Khonsu (CoC)
    566: 7, # Khonsu (CoC)
    519: 15, # Khonsu Ra
    753: 336, # Kodama
    948: 32, # Konohana Sakuya
    819: 205, # Koumokuten (2 Turn)
    861: 205, # Koumokuten (4 Turn)
    774: 40, # Kresnik
    772: 346, # Kudlak
    809: 342, # Kumbhanda
    723: 342, # Kumbhanda (Abcess)
    878: 37, # Kurama Tengu (with Zaou)
    615: 213, # Kushinada-Hime
    557: 236, # Lahmu (School 2nd TODO: Why did I find you???)
    556: 441, # Lahmu (School)
    452: 441, # Lahmu (Shinagawa 1st)
    453: 236, # Lahmu (Shinagawa 2nd)
    727: 303, # Lamia (Abcess)
    440: 303, # Lamia (Jozoji)
    580: 303, # Lamia (with Isis)
    710: 305, # Leanan Sidhe (Abcess)
    866: 305, # Leanan Sidhe (with Ippon)
    880: 67, # Lilim
    569: 391, # Lilith
    810: 89, # Loki
    450: 136, # Loup-garou
    537: 529, # Lucifer
    729: 174, # Mad Gasser
    601: 121, # Makami
    500: 302, # Manananggal (School Copy)
    501: 302, # Manananggal (School Copy)
    705: 45, # Mandrake
    842: 30, # Maria
    757: 227, # Masakado
    758: 227, # Masakado (True)
    596: 250, # Mastema
    921: 359, # Matador
    471: 249, # Melchizedek
    476: 249, # Melchizedek (No EXP Revive)
    932: 78, # Mephisto
    609: 304, # Mermaid
    477: 241, # Metatron
    841: 242, # Michael
    604: 234, # Mishaguji
    830: 88, # Mithras
    624: 11, # Mitra
    928: 351, # Mother Harlot
    722: 289, # Muu Shuwuu
    553: 393, # Naamah
    554: 393, # Naamah (with GL)
    603: 104, # Naga Raja
    779: 22, # Norn
    752: 107, # Nozuchi
    435: 197, # Nuwa (Snake)
    550: 75, # Nuwa (with Yakumo)
    608: 52, # Oberon
    470: 9, # Odin (CoC)
    482: 9, # Odin (CoV)
    822: 215, # Okuninushi
    888: 318, # Oni (Quest)
    499: 318, # Oni (School Copy)
    446: 318, # Oni (School)
    706: 290, # Onmoraki
    770: 386, # Onyankopon
    731: 139, # Orobas (Abcess)
    817: 139, # Orobas (With Moloch)
    726: 135, # Orthrus
    475: 269, # Ose (Summon)
    825: 212, # Oyamatsumi (With Kunitsu)
    927: 358, # Pale Rider
    801: 233, # Pazuzu
    755: 341, # Pisaca
    621: 59, # Pixie
    506: 256, # Power (5x Copy)
    504: 256, # Power (Double Copy)
    503: 256, # Power (Single Copy)
    505: 256, # Power (Triple Copy)
    815: 256, # Power (with Camael)
    484: 256, # Power (With Dominions)
    713: 345, # Preta (Abcess)
    889: 345, # Preta (Quest)
    879: 257, # Principality
    854: 96, # Qing Long
    933: 95, # Quetzalcoatl
    492: 324, # Rakshasa (School Copy)
    493: 324, # Rakshasa (School Copy)
    494: 324, # Rakshasa (School Copy)
    444: 324, # Rakshasa (School)
    777: 324, # Rakshasa (with Atavaka)
    491: 324, # Rakshasa(School Copy)
    625: 296, # Rangda
    835: 245, # Raphael
    925: 353, # Red Rider
    760: 118, # Samael
    614: 24, # Sarasvati
    681: 1, # Satan
    782: 237, # Saturnus
    617: 26, # Scathach
    724: 130, # Senri
    870: 112, # Seth
    750: 129, # Shiisaa
    820: 311, # Shiki-Ouji (Quest)
    502: 311, # Shiki-Ouji (School Copy)
    448: 311, # Shiki-Ouji (School)
    845: 178, # Shiva
    629: 222, # Siegfried
    613: 53, # Silky
    626: 192, # Skadi
    620: 173, # Slime
    472: 244, # Sraosha
    721: 65, # Succubus
    718: 335, # Sudama (Abcess)
    823: 214, # Sukuna-Hikona
    824: 216, # Take-Minakata
    778: 200, # Thor
    734: 14, # Thoth (Abcess)
    518: 14, # Thoth (CoC Summon)
    431: 345, # Three Pretas
    623: 254, # Throne
    929: 350, # Trumpeter
    449: 331, # Tsuchigumo (School)
    754: 175, # Turbo Granny
    834: 247, # Uriel
    468: 111, # Vasuki
    769: 108, # Vouivre
    733: 99, # Vritra
    924: 354, # White Rider
    857: 97, # Xuanwu
    768: 299, # Yakshini
    775: 103, # Yamata-no-Orochi (8 Turn)
    619: 103, # Yamata-no-Orochi (Abcess)
    622: 280, # Yatagarasu
    616: 105, # Yurlungur
    877: 180, # Zaou-Gongen
    469: 8, # Zeus (CoC)
    481: 8, # Zeus (CoV)
    838: 8, # Zeus (Demeter Quest)
    509: 288, # Zhen (3x Copy)
    510: 288, # Zhen (4x Copy)
    756: 288, # Zhen (5x)
    855: 279, # Zhuque
    805: 206, # Zouchouten (2 Turn)
    860: 206, # Zouchouten (4 Turn)
    #TODO: Should be complete? With the exception of bosses who use NPC Models
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
    demonModelAnimMap = pd.read_csv(paths.MODEL_ANIMS, dtype=str)
    for index, row in demonModelAnimMap.iterrows():
        model = Demon_Model()
        if type(row['Model']) is str:
            model.modelName = row['Model']
        for animation in demonModelAnimMap.columns[1:]:  # Skip the 'Model' column
            if row[animation] == '1':  # If the model has this animation (value is 1)
                model.animations.append(animation)  # Add the animation to the list
        DEMON_MODELS.update({model.modelName[3:6] : model})
            

'''
Updates the models used in events.
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
'''
def updateEventModels(encounterReplacements, bossReplacements, scriptFiles, mapSymbolArr):
    initDemonModelData()
    umapList = UMap_File_List()
    for script, syncDemons in EVENT_SCRIPT_MODELS.items():
        file = scriptFiles.getFile(script)
        hitboxUpdated = False
            
        for syncDemon in syncDemons:
            
            originalDemonID = syncDemon.ind
            syncDemonID = syncDemon.sync
            if syncDemonID > numbers.NORMAL_ENEMY_COUNT: # if demon to get replacement from is boss
                try:
                    replacementID = bossReplacements[syncDemonID]
                except KeyError:
                    #print("Key Error: " + str(syncDemonID))
                    continue
            else: #else it is a normal demon
                try:
                    replacementID = encounterReplacements[syncDemonID]
                except KeyError:
                    #print("Key Error: " + str(syncDemonID))
                    continue
            if replacementID == originalDemonID: #do not need to swap models if replacement is the same as originalDemonID
                continue
            try: #Does boss use a different model that has no tie to their id
                replacementID = MODEL_SYNC[replacementID]
            except KeyError:
                #replacementID = 103 #Testing stuff
                pass
                
            if not hitboxUpdated and script in REQUIRES_HIT_UPDATE: #TODO: How to deal with overlap issues
                umap = umapList.getFile(LEVEL_UASSETS[script])
                try:
                    og = next(d for x, d in enumerate(mapSymbolArr) if d.demonID == originalDemonID)
                    replacement = next(d for x, d in enumerate(mapSymbolArr) if d.demonID == replacementID)
                    scalingFactor = og.encountCollision.stretchToBox(replacement.encountCollision, ignoreY = True)
                    if scalingFactor != 0:
                        print(scalingFactor)
                        scale = scalingFactor
                    else:
                        scale = 1.5 #Increase by 50%
                except StopIteration:
                    scale = 1.5 #Increase by 50%
                hitboxUpdated = True
                umap = updateEventHitScaling(umap,script,scale)

            #TODO: Multiple demon model swaps do work, but need to deal with chain replacements,(A->B B->C)
            file = replaceDemonModelInScript(script, file, originalDemonID, replacementID, scriptFiles)   
        
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

    for index, name in enumerate(uassetData.nameList): #change occurences of oldDemonID and oldDemonName in all names in the uasset
        if "ev" + oldIDString in name: #to just get the model names since sometimes DevXXX or devXXX
            uassetData.nameList[index] = uassetData.nameList[index].replace(oldIDString,newIDString)
        if oldName in name:
            uassetData.nameList[index] = uassetData.nameList[index].replace(oldName,newName)
        
    if 'FALSE' == HAS_SIMPLE_BP[replacementDemonID]:
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
        newString = offsetString.replace(oldName,newName).replace(oldIDString,newIDString)
        #Change Animation if the demon does not have the required animation
        newString = replaceNonExistentAnimations(script, newString,newIDString,newName)
        lengthDifference = len(newString) - len(offsetString)
       
        if oldIDString in offsetString: 
            #if the oldID is there in string format, replace with new string
            offsetString = offsetString.replace(oldIDString,newIDString)
            if oldName not in offsetString: 
                #if oldName is not in string, nothing else needs to be updated and string can be written
                offsetString = offsetString.encode('ascii')
                uexpData.writeXChars(offsetString, len(offsetString), offset)
                continue  
        if oldName in offsetString: 
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
                newString = replaceNonExistentAnimations(script, newString, newIDString,newName)
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

'''
Replaces the animation in a string with a designated replacement animation if required.
    Parameters:
        script(String): the name of the script file
        string(String): the string for the animation that might be changed
        replacementID(String): the id of the demon that replaced the old one
        replacementName(String): the name of the demon that replaced the old one
'''
def replaceNonExistentAnimations(script, string, replacementID,replacementName):
    animations = SCRIPT_ANIMS_REPLACEMENTS[script]
    for animSync in animations: #go through animations to potentially replace in script
        animation = animSync.ind
        replacementAnim = animSync.sync
        if animation in DEMON_MODELS[replacementID].animations:
            #Animation exists for the new demon therefore string is fine
            return string
        #Animation does not exist for the new demon therefore string needs to be changed
        if '/' in animation: #Is Animation in Subfolder?
            animationParts = animation.split("/")
            searchString = "/Game/Design/Character/Devil/dev" + replacementID + "_" + replacementName + "/Anim/" + animationParts[0] + "/" + "AN_dev" + replacementID + "_" + animationParts[1]+ "." + "AN_dev" + replacementID + "_" + animationParts[1]
        else:
            searchString = "/Game/Design/Character/Devil/dev" + replacementID + "_" + replacementName + "/Anim/" + "AN_dev" + replacementID + "_ " + animation+ "." + "AN_dev" + replacementID + "_" + animation
        if searchString in string: #Is the Animation the one in the current string
            if '/' in replacementAnim: #Is new Animation in Subfolder?
                animationParts = replacementAnim.split("/")
                replacementString = "/Game/Design/Character/Devil/dev" + replacementID + "_" + replacementName + "/Anim/" + animationParts[0] + "/" + "AN_dev" + replacementID + "_ " + animationParts[1]+ "." + "AN_dev" + replacementID + "_" + animationParts[1]
            else:
                replacementString = "/Game/Design/Character/Devil/dev" + replacementID + "_" + replacementName + "/Anim/" + "AN_dev" + replacementID + "_" + replacementAnim+ "." + "AN_dev" + replacementID + "_" + replacementAnim
            string = string.replace(searchString,replacementString)

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

    #print(scalingParam1)
    #print(scalingParam2)
    #print(scalingParam3)
    #print("SCALE NOW")

    scalingParam1 *= scale
    scalingParam2 *= scale
    scalingParam3 *= scale

    #print(scalingParam1)
    #print(scalingParam2)
    #print(scalingParam3)

    uexp.writeFloat(scalingParam1, scalingOffsets)
    uexp.writeFloat(scalingParam2, scalingOffsets + 4)
    uexp.writeFloat(scalingParam3, scalingOffsets + 8)


    return umap