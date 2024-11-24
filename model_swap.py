from base_classes.script import Script_Function_Type,Script_Uasset,Bytecode
from base_classes.file_lists import UMap_File, UMap_File_List, Script_File, Script_File_List
from base_classes.demon_assets import Demon_Model, Position
from util.binary_table import readBinaryTable
from base_classes.model_swap_data import *
import util.paths as paths
import util.numbers as numbers
import util.jsonExports as jsonExports
import pandas as pd
import copy
import datetime
import random

DEBUG_SWAP_PRINT = False
DEBUG_BIG_MODEL_TEST = False
DEBUG_MODELS = [565,525,520]

DEVIL_PREFIX = "/Devil/"
NPC_PREFIX = "/NPC/"
NPC_MODEL_START = 600
LAHMU_2ND_FORM_ID = 236

#Model IDs that use Dev Class Blueprints but are in NPC folder otherwise
NPC_MODELS_DEV_BLUEPRINT = [621,622,625,626,627,641,642,643,646,647,648,649,650,651]
FOLDER_SWITCH_RESTRICTIONS = ["LV_E0905","LV_E0965"]

MODEL_NAMES = {}
DEMON_ID_MODEL_ID = {}
HAS_SIMPLE_BP = {}
DEMON_MODELS={}


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
            model.modelName = row['Model'].split('_', 1)[1]
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
        mapSymbolArr(List): list of map symbol data
        config (Config_Settings): settings set for the randomizer
'''
def updateEventModels(encounterReplacements, bossReplacements, scriptFiles: Script_File_List, mapSymbolFile, config):
    mapSymbolTable = mapSymbolFile.json["Exports"][0]["Table"]["Data"]
    originalMapSymbolTable = mapSymbolFile.originalJson["Exports"][0]["Table"]["Data"]
    initDemonModelData()
    startTime = datetime.datetime.now()
    umapList = UMap_File_List()
    totalScripts = len(EVENT_SCRIPT_MODELS.keys())
    currentScriptIndex = 0
    for script, syncDemons in EVENT_SCRIPT_MODELS.items():
        currentScriptIndex += 1
        replacementMap = {}
        for syncDemon in syncDemons:
            originalDemonID = syncDemon.ind
            syncDemonID = syncDemon.sync
            if syncDemonID in numbers.SCRIPT_JOIN_DEMONS.values() and not config.ensureDemonJoinLevel: #If demon isn't getting replaced ignore it
                continue
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
            try: #Does replacement boss use a different model that has no tie to their id
                replacementID = MODEL_SYNC[replacementID]
            except KeyError:
                #replacementID = 934 #Testing stuff for event hit scaling
                pass 
            try: #Does original boss use a different model that has no tie to their id
                originalDemonID = MODEL_SYNC[originalDemonID]
            except KeyError:
                #replacementID = 934 #Testing stuff for event hit scaling
                pass
            if DEBUG_BIG_MODEL_TEST:
                replacementID = random.choice(DEBUG_MODELS) #Testing big demon models (Tiamat, Abdiel Naho, Nuwa Naho)
            # if originalDemonID in replacementMap.values():
            #     print("Causes Chain replacement: " + str(originalDemonID) + " " + str(replacementID) )
            replacementMap[originalDemonID] = replacementID
        
        file = scriptFiles.getFile(script)
        hitboxUpdated = False
        rawCode = prepareScriptFileForModelReplacement(script, file)
        if rawCode: #script does not have byte code so continue with next one (Debug print happens elsewhere)
            continue
        scale = 1
        currentScale = 1
        for originalDemonID, replacementID in replacementMap.items():
            currentMapSymbolTable = mapSymbolTable
            if file.relevantFunctionExps[0] == []:
                currentMapSymbolTable = originalMapSymbolTable
            try:
                og = next(d for x, d in enumerate(currentMapSymbolTable) if d["Value"][0]["Value"] == originalDemonID)
                replacement = next(d for x, d in enumerate(currentMapSymbolTable) if d["Value"][0]["Value"] == replacementID)
                baseCollision = Position(og["Value"][5]["Value"],og["Value"][6]["Value"],og["Value"][7]["Value"])
                replacementCollision = Position(replacement["Value"][5]["Value"],replacement["Value"][6]["Value"],replacement["Value"][7]["Value"])
                scalingFactor = baseCollision.stretchToBox(replacementCollision)
                #scalingFactor = og.encountCollision.stretchToBox(replacement.encountCollision, ignoreY = True)
                if scalingFactor != 0:
                    #print(scalingFactor)
                    scale = scalingFactor
                elif scalingFactor < 1:
                    scale = 1
                else:
                    scale = 1.5 #Increase by 50%
            except StopIteration:
                scale = 1.5 #Increase by 50%
                if file.relevantFunctionExps[0] == [] and script in REQUIRES_HIT_UPDATE:
                    # if is never scaled to symbol scale and no valid scaling found skip model replacement
                    print("CANNOT CALCULATE SCALING AND NO SYMBOL SCALE ADJUSTED IN :" + script + " for replacment " + str(replacementID))
                    continue
            if (scale > 6 and script in REQUIRES_HIT_UPDATE) or (scale > 3 and file.relevantFunctionExps[0] == [] and script in REQUIRES_HIT_UPDATE): #do not update hitbox size if scale would be smaller
                #TODO: Number values could maybe be fine tuned
                #do not double if there is no modelScaling in code and update is needed
                #print("REPLACEMENT MODEL SIZE IS TOO LARGE:" + script + " " + str(originalDemonID) + "->" + str(replacementID) + " = " + str(scale))
                continue
            if scale > 1.5 and script in OVERLAPPING_SCRIPTS:
                #print("OVERLAP PREVENTION " + script)
                #minimum measure to prevent important overlap
                continue
            #Need to make sure that it is updated for biggest demon in file
            if scale != 1 and (not hitboxUpdated or scale >= currentScale) and script in REQUIRES_HIT_UPDATE and script in LEVEL_UASSETS.keys():
                umap = umapList.getFile(LEVEL_UASSETS[script])
                hitboxUpdated = True
                umap = updateEventHitScaling(umap,script,scale)
                currentScale = scale
            elif scale != 1 and (not hitboxUpdated or scale >= currentScale) and script in REQUIRES_HIT_UPDATE: #no umap for event exists, update all others this way for safety
                successful = updateEventHitGen(file,scale,script)
                currentScale = scale
                if not successful:
                    #print("FAILED TO UPDATE HIT SCALE IN:" + script)
                    continue
            
            file = replaceDemonModelInScript(script, file, originalDemonID, replacementID)   
        
        scriptFiles.setFile(script,file)
        scriptFiles.writeFile(script,file)
        print("Swapped Models for " + str(currentScriptIndex) + " of " + str(totalScripts) + " Scripts", end='\r')
    endTime = datetime.datetime.now()
    print(endTime - startTime)
    
    umapList.writeFiles()
    updateCutsceneModels(encounterReplacements, bossReplacements,config)

'''
Prepares the given script file by preparing data that gets used in the model swap process.
'''
def prepareScriptFileForModelReplacement(script, file: Script_File):
    jsonData = file.json
    if file.originalNameMap is None: #use original name map to prevent chain replacements
        file.originalNameMap = copy.deepcopy(jsonData['NameMap'])
    file.exportIndex = None
    try: #get bytecode and bytecode size for main portion if UAssetAPI can parse it
        file.exportNameList = [exp['ObjectName'] for exp in jsonData["Exports"]]
        file.executeUbergraph = "ExecuteUbergraph_" + script
        file.exportIndex = file.exportNameList.index(file.executeUbergraph)
        bytecode = Bytecode(jsonData["Exports"][file.exportIndex]['ScriptBytecode'])
        byteCodeSize = jsonData["Exports"][file.exportIndex]['ScriptBytecodeSize']
    except KeyError: #otherwise stop and note error
        print("Script Byte Code only in raw form: " + script)
        return True
    
    if file.originalByteCodeSize is None: 
        file.originalByteCodeSize = byteCodeSize#Set bytecode size to not replace bytecode moved to the end
        file.originalBytecode = copy.deepcopy(bytecode)#Also use original bytecode to prevent chain replacements
    
    #Find cases where the function name is explicitly in the code
    file.relevantFunctionExps = []
    file.relevantFunctionNames = ['BPL_AdjustMapSymbolScale']
    for func in file.relevantFunctionNames:
        expressions = file.originalBytecode.findExpressionUsage("UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVirtualFunction", virtualFunctionName= func)
        file.relevantFunctionExps.append(expressions)
    
    #Build import list
    file.importNameList = [imp['ObjectName'] for imp in jsonData['Imports']]
    file.relevantImportNames = ['LoadAsset','PrintString','LoadAssetClass','TargetBinding']
    file.relevantImports = {}
    for imp in file.relevantImportNames: #Determine import id for relevant import names which is always negative
        if imp in file.importNameList:
            file.relevantImports[imp] = -1 * file.importNameList.index(imp) -1
    #print(file.relevantImports.keys())
    #Find cases where function name is not explicit in code due to being an import
    file.relevantImportExps = {}
    for imp,stackNode in file.relevantImports.items():
        
        expressions = file.originalBytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
        expressions.reverse()
        file.relevantImportExps[stackNode] = expressions



'''
Replaces the a demon model with the model of another demon in the given script.
    Parameters:
        script(String): the name of the script
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
        ogDemonID (Integer): the id of the demon that should be replaced
        replacementDemonID (Integer): the id of the replacement demon
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
        #TODO: Think about how to optimize this function: Maybe rewrite to use API for all and not modify json
'''
def replaceDemonModelInScript(script, file: Script_File, ogDemonID, replacementDemonID):
    jsonData = file.json
    #Get the Strings corresponding to the old demon and the prefixes
    oldIDString = DEMON_ID_MODEL_ID[ogDemonID]
    oldName = MODEL_NAMES[oldIDString]
    oldFolderPrefix = DEVIL_PREFIX
    oldPrefix = "dev"
    oldPrefixVariant = "Dev"
    if int(oldIDString) > NPC_MODEL_START:
        oldFolderPrefix = NPC_PREFIX
        oldPrefix = "npc"
        oldPrefixVariant = "Npc"
    #Get the Strings corresponding to the new demon and the prefixes
    try:
        newIDString = DEMON_ID_MODEL_ID[replacementDemonID]
    except KeyError:
        print(str(replacementDemonID) + " needs a model tied to it. Stopping replacement")
        return file
    newName = MODEL_NAMES[newIDString]
    newPrefix = "dev"
    newFolderPrefix = DEVIL_PREFIX
    newPrefixVariant = "Dev"
    if int(newIDString) > NPC_MODEL_START:
        newPrefix = "npc"
        newFolderPrefix = NPC_PREFIX
        newPrefixVariant = "Npc"
    if replacementDemonID == LAHMU_2ND_FORM_ID:
        lahmuSuffix = "_3rd"
    else:
        lahmuSuffix = ""
    if DEBUG_SWAP_PRINT:
        print("SWAP: " + oldPrefix +"/" +  oldName + " -> " + newPrefix +"/"+ newName + " in " + script)

    #There are some special cases for these class blueprints
    classOldFolderPrefix = copy.deepcopy(oldFolderPrefix)
    classOldPrefix = copy.deepcopy(oldPrefix)
    classOldPrefixVariant = copy.deepcopy(oldPrefixVariant)
    classNewFolderPrefix = copy.deepcopy(newFolderPrefix)
    classNewPrefix = copy.deepcopy(newPrefix)
    classNewPrefixVariant = copy.deepcopy(newPrefixVariant)
    if int(newIDString) in NPC_MODELS_DEV_BLUEPRINT:
        #only new is exception that use devil instead of npc for this
        classNewFolderPrefix = DEVIL_PREFIX
        classNewPrefix = "dev"
        classNewPrefixVariant = "Dev"
        
    elif int(oldIDString) in NPC_MODELS_DEV_BLUEPRINT and script not in FOLDER_SWITCH_RESTRICTIONS:
        #old is exception that use devil instead of npc for this
        classOldFolderPrefix = DEVIL_PREFIX
        classOldPrefix = "dev"
        classOldPrefixVariant = "Dev"
    
    
    for index, name in enumerate(file.originalNameMap):
        if "DevilBaseLight" in name and 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] :
            #Applies to CoC Nuwa Gate, Kunitsukami Fight, Dagda, 4 Heavenly Kings, Pisaca Quest Anahita Event, Konohana Sakuya, Nozuchi, Huang Long
            #print("DEVIL BASE LIGHT CRASH POSSIBLE FOR:" + script)
            return file # since we might run into softlocks otherwise
    #print("NO DEVIL BASE LIGHT CRASH POSSIBLE FOR:" + script)

    

    for index, name in enumerate(file.originalNameMap): #change occurences of oldDemonID and oldDemonName in all names in the uasset
        nameEntry = file.getNameAtIndex(index)
        if script in name:
            #Do not change names for Main File Exports if DemonId or Name is in script
            continue
        if oldIDString in name and ("/Blueprints/Character" in name or "_C" in name): 
            nameEntry = nameEntry.replace(classOldFolderPrefix + classOldPrefix + oldIDString, classNewFolderPrefix + classNewPrefix +newIDString).replace(classOldPrefix + oldIDString, classNewPrefix +newIDString)
            nameEntry = nameEntry.replace(classOldFolderPrefix + classOldPrefixVariant + oldIDString, classNewFolderPrefix + classNewPrefixVariant +newIDString).replace(classOldPrefixVariant + oldIDString, classNewPrefixVariant +newIDString)
            if 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] and "_Simple" in name: #change bp name if demon does not have simple blueprint
                nameEntry = nameEntry.replace("_Simple","")
        elif oldIDString in name and not "Spawn" in name: #to just get the model names since sometimes DevXXX or devXXX
            nameEntry = nameEntry.replace(oldFolderPrefix + oldPrefix + oldIDString, newFolderPrefix + newPrefix +newIDString).replace(oldPrefix + oldIDString, newPrefix +newIDString)
            nameEntry = nameEntry.replace(oldFolderPrefix + oldPrefixVariant + oldIDString, newFolderPrefix + newPrefixVariant +newIDString).replace(oldPrefixVariant + oldIDString, newPrefixVariant +newIDString)
            if 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] and "_Simple" in name: #change bp name if demon does not have simple blueprint
                nameEntry = nameEntry.replace("_Simple","")
        if oldName in name and ("Character" in name or "Anim" in name): #to prevent stuff like replacing set(seth) in LoadAsset
            #print(nameEntry)
            nameEntry = nameEntry.replace(oldName,newName)
        # elif oldName in name:
        #     print("EXTRA CHECK Necessary? " + nameEntry)
        if "Anim/" in name or name[:3] == "AN_":
            nameEntry = replaceNonExistentAnimations(script, nameEntry,newIDString,newName, classOldFolderPrefix, classOldPrefix, classNewFolderPrefix, classNewPrefix, lahmuSuffix)
        file.setNameAtIndex(index,nameEntry)
        
        
    
    #get updated jsonData
    jsonData = file.updateJsonWithUasset()

    #get the bytecode and size and export name listanew
    bytecode = Bytecode(jsonData["Exports"][file.exportIndex]['ScriptBytecode'])
    #Adjust cases where demon ID is in function call
    for index,func in enumerate(file.relevantFunctionNames):
        for exp in file.relevantFunctionExps[index]:
            if func == "BPL_AdjustMapSymbolScale":
                modelValue = exp['Parameters'][1].get('Value')
                #print(modelValue)
                if modelValue == ogDemonID: #Only change demonID for the oldDemon
                    newExpression = bytecode.json[bytecode.getIndex(exp)]
                    #print(newExpression['$type'])
                    newExpression['ContextExpression']['Parameters'][1]['Value'] = replacementDemonID

    # get serialized bytecode to calculate statement indeces
    serializedByteCode = file.getSerializedScriptBytecode(file.exportIndex,jsonData)
    
    '''
    Replaces ids in animation or blueprint class strings
    '''
    def replaceOldIDinString(string):
        if ("/Blueprints/Character" in string or "_C" in string):
            nstring = string.replace(classOldFolderPrefix + classOldPrefix + oldIDString, classNewFolderPrefix + classNewPrefix +newIDString).replace(classOldPrefix + oldIDString, classNewPrefix +newIDString)
            nstring = nstring.replace(classOldFolderPrefix + classOldPrefixVariant + oldIDString, classNewFolderPrefix + classNewPrefixVariant +newIDString).replace(classOldPrefixVariant + oldIDString, classNewPrefixVariant +newIDString)
            nstring = replaceNonExistentAnimations(script, nstring,newIDString,newName, classOldFolderPrefix, classOldPrefix, classNewFolderPrefix, classNewPrefix, lahmuSuffix)
        else:
            nstring = string.replace(oldFolderPrefix + oldPrefix + oldIDString, newFolderPrefix + newPrefix +newIDString).replace(oldPrefix + oldIDString, newPrefix +newIDString)
            nstring = nstring.replace(oldFolderPrefix + oldPrefixVariant + oldIDString, newFolderPrefix + newPrefixVariant +newIDString).replace(oldPrefixVariant + oldIDString, newPrefixVariant +newIDString)
            nstring = replaceNonExistentAnimations(script, nstring,newIDString,newName, oldFolderPrefix, oldPrefix, newFolderPrefix, newPrefix, lahmuSuffix)
        return nstring

    # for all cases where the function is an import and the id or name is in a string
    for imp,stackNode in file.relevantImports.items():
        expressions = file.relevantImportExps[stackNode]
        for expIndex, exp in enumerate(expressions):
            if bytecode.getIndex(exp) is None:
                # First case: Nested expression (will be fixed at some point)
                # Second case: Expression has already been modified in the new one, so we can skip it here
                continue
            currentStatementIndex = serializedByteCode[bytecode.getIndex(exp)]["StatementIndex"]
            
            
            if currentStatementIndex > file.originalByteCodeSize: #to not potentially move or adjust code that has been moved already!
                continue
            if imp == 'PrintString' or imp == "TargetBinding": 
                stringValue = exp['Parameters'][1].get('Value')
                if stringValue[:3] in ["dev","Dev","npc","Npc"]:
                    stringValue = replaceOldIDinString(stringValue)
                    newExpression = bytecode.json[bytecode.getIndex(exp)]
                    newExpression['Parameters'][1]['Value'] = stringValue
            elif imp == 'LoadAsset' or imp == 'LoadAssetClass':
                try:
                    stringValue = exp['Parameters'][1].get('Value').get('Value')
                except AttributeError:
                    continue
                if oldIDString not in stringValue and oldName not in stringValue:
                    #if neither oldID or oldName are in the string go to next exp
                    continue
                #print(stringValue)
                originalLength = len(stringValue)
                #create new string here for calculation of lenghtDifference
                newString = replaceOldIDinString(stringValue).replace(oldName,newName)
                if ("/Blueprints/Character" in stringValue or "_C" in stringValue):
                    newString = replaceNonExistentAnimations(script, newString,newIDString,newName, classOldFolderPrefix, classOldPrefix, classNewFolderPrefix, classNewPrefix, lahmuSuffix)
                else:
                    newString = replaceNonExistentAnimations(script, newString,newIDString,newName, oldFolderPrefix, oldPrefix, newFolderPrefix, newPrefix, lahmuSuffix)#exp['Parameters'][1]['Value']['Value'] = stringValue
                    
                if imp == "LoadAssetClass" and "Simple" in newString and 'FALSE' == HAS_SIMPLE_BP[replacementDemonID]:
                    newString = newString.replace("_Simple","")

                lengthDifference = len(newString) - originalLength

                if stringValue == newString:
                    #No change in string
                    continue

                if oldIDString in stringValue and lengthDifference == 0: 
                    #if the oldID is there in string format, replace with new string
                    stringValue= replaceOldIDinString(stringValue)
                    
                if oldName in stringValue and lengthDifference == 0:
                    #length is the same so can swap name and anim
                    stringValue = stringValue.replace(oldName,newName)
                    if ("/Blueprints/Character" in stringValue or "_C" in stringValue):
                        stringValue = replaceNonExistentAnimations(script, stringValue,newIDString,newName, classOldFolderPrefix, classOldPrefix, classNewFolderPrefix, classNewPrefix, lahmuSuffix)
                    else:
                        stringValue = replaceNonExistentAnimations(script, stringValue,newIDString,newName, oldFolderPrefix, oldPrefix, newFolderPrefix, newPrefix, lahmuSuffix)#exp['Parameters'][1]['Value']['Value'] = stringValue
                    if imp == "LoadAssetClass" and "Simple" in stringValue and 'FALSE' == HAS_SIMPLE_BP[replacementDemonID]:
                        stringValue = newString.replace("_Simple","")
                    newExpression = bytecode.json[bytecode.getIndex(exp)]
                    newExpression['Parameters'][1]['Value']['Value'] = stringValue
                elif lengthDifference != 0:
                    #length is not the same so need to move expression around
                    #recalc new string just in case
                    stringValue = replaceOldIDinString(stringValue)
                    newString = stringValue.replace(oldName,newName)
                    newString = replaceOldIDinString(newString)
                    if imp == "LoadAssetClass" and "Simple" in newString and 'FALSE' == HAS_SIMPLE_BP[replacementDemonID]:
                        newString = newString.replace("_Simple","")

                    nextStatementIndex = serializedByteCode[bytecode.getIndex(exp)+1]["StatementIndex"]
                    lastStatementIndex = file.calcLastStatementIndex(file.exportIndex,serializedByteCode[-1]["StatementIndex"], jsonData)
                    statementLength = nextStatementIndex - currentStatementIndex
                    
                    #Copy and change values and append to the end
                    newExpression = copy.deepcopy(exp)
                    newExpression['Parameters'][1]['Value']['Value'] = newString
                    bytecode.json.append(newExpression)
                    jumpBack = copy.deepcopy(jsonExports.BYTECODE_JUMP)
                    jumpBack['CodeOffset'] = nextStatementIndex
                    bytecode.json.append(jumpBack)

                    #change original expression to be jump
                    expReplacement = copy.deepcopy(jsonExports.BYTECODE_JUMP)
                    expReplacement['CodeOffset'] = lastStatementIndex #last one is either EndOfScript or jump if already inserted something and we want to start after that
                    # fill with nothing 
                    nothingInsts = []
                    amount = statementLength - 5 #(due to jump)
                    for i in range(amount):
                        nothingInsts.append(jsonExports.BYTECODE_NOTHING)

                    bytecode.replace(exp, expReplacement, nothingInsts)
                    #Updated serializedByteCodeList for new statement indeces
                    #TODO: This seems to be the main cause of why the whole process takes long, can I use this less aka calculate index myself again?
                    serializedByteCode = file.getSerializedScriptBytecode(file.exportIndex,jsonData)
                else: #oldName not in String, save id swaps
                    newExpression = bytecode.json[bytecode.getIndex(exp)]
                    newExpression['Parameters'][1]['Value']['Value'] = stringValue
                
    file.updateFileWithJson(jsonData)
    return file
'''
Replaces the animation in a string with a designated replacement animation if required.
    Parameters:
        script(String): the name of the script file
        string(String): the string for the animation that might be changed
        replacementID(String): the id of the demon that replaced the old one
        replacementName(String): the name of the demon that replaced the old one
'''
def replaceNonExistentAnimations(script, string, replacementID,replacementName, oFPrefix, oPrefix, nFPrefix, nPrefix,lahmuSuffix= ""):
    try:
        animations = SCRIPT_ANIMS_REPLACEMENTS[script]
    except KeyError: #Script does not have any special animations that can be replaced
        return string
    for animSync in animations: #go through animations to potentially replace in script
        animation = animSync.ind
        replacementAnim = animSync.sync
        if animation in DEMON_MODELS[replacementID].animations or ('/' not in animation and animation not in string):
            #Animation exists for the new demon therefore string is fine
            continue
        if 'Anim/' not in string and string[:3] == "AN_":
            if '/' in animation: #Is Animation in Subfolder?
                animationParts = animation.split("/")
            else:
                animationParts = ["",animation] #I'm lazy so fake list it is
            searchString = "AN_"+oPrefix + replacementID + lahmuSuffix + "_" + animationParts[1]
            if searchString in string:
                if '/' in replacementAnim: #Is Animation in Subfolder?
                    animationParts = replacementAnim.split("/")
                else:
                    animationParts = ["",replacementAnim] #I'm lazy so fake list it is
                replacementString = "AN_"+nPrefix + replacementID+ lahmuSuffix + "_" + animationParts[1]
                string = string.replace(searchString,replacementString)
        elif 'Anim/' not in string:
            return string
        #Animation does not exist for the new demon therefore string needs to be changed
        if '/' in animation: #Is Animation in Subfolder?
            animationParts = animation.split("/")
            searchString = "/Game/Design/Character"+oFPrefix+oPrefix + replacementID + "_" + replacementName + "/Anim/" + animationParts[0] + "/" + "AN_"+oPrefix + replacementID + lahmuSuffix + "_" + animationParts[1]
            if '.' in string:
                searchString += "." + "AN_"+oPrefix + replacementID + lahmuSuffix+ "_" + animationParts[1]
        else:
            searchString = "/Game/Design/Character"+oFPrefix+oPrefix + replacementID + "_" + replacementName + "/Anim/" + "AN_"+oPrefix + replacementID+ lahmuSuffix + "_" + animation
            if '.' in string:
                searchString += "." + "AN_"+oPrefix + replacementID+ lahmuSuffix + "_" + animation

        if searchString in string: #Is the Animation the one in the current string
            if '/' in replacementAnim: #Is new Animation in Subfolder?
                animationParts = replacementAnim.split("/")
                replacementString = "/Game/Design/Character"+nFPrefix+nPrefix + replacementID + "_" + replacementName + "/Anim/" + animationParts[0] + "/" + "AN_"+nPrefix + replacementID+ lahmuSuffix + "_" + animationParts[1]
                if '.' in string:
                    replacementString += "." + "AN_"+nPrefix + replacementID+ lahmuSuffix + "_" + animationParts[1]
            else:
                replacementString = "/Game/Design/Character"+nFPrefix+nPrefix + replacementID + "_" + replacementName + "/Anim/" + "AN_"+nPrefix + replacementID+ lahmuSuffix + "_" + replacementAnim
                if '.' in string:
                    replacementString += "." + "AN_"+nPrefix + replacementID + lahmuSuffix+ "_" + replacementAnim
            string = string.replace(searchString,replacementString)
    return string


'''
Modifies the scaling for the event hit trigger of the given script by the scale given.
    umap(UMap_File): file containing the umap and uexp data
    script(String): name of the script the event hit should be updated for
    scale(Float): by what the current scale should be multiplied
'''
def updateEventHitScaling(umap: UMap_File,script,scale):
    asset = umap.uasset
    exports = umap.json['Exports']

    scriptExport = next(exp for exp in exports if script in exp['ObjectName'])
    eventHitExportID = next(data['Value'] for data in scriptExport['Data'] if data['Name'] == 'EventHit')
    eventHitExport = exports[eventHitExportID -1]

    try:
        relativeScale3D = next(data['Value'] for data in eventHitExport['Data'] if data['Name'] == 'RelativeScale3D')
        
    except StopIteration: #has no relativeScale3D #TODO: Base scale parameters what should they be??
        eventHitExport['Data'].append(copy.deepcopy(jsonExports.RELATIVE_SCALE_3D))
        relativeScale3D = eventHitExport['Data'][-1]['Value']
    
    vectorValues = relativeScale3D[0]['Value']

    vectorValues['X'] *= scale
    vectorValues['Y'] *= scale
    vectorValues['Z'] *= scale

    return umap

'''
Updates the EventHit_GEN_VARIABLE export of a script file.
    Parameters:
        file(Script_File): file of the script
        scale(Float): modifier for the event hit scale
        script(String): name of the script
'''
def updateEventHitGen(file, scale, script):
    exports = file.json['Exports']
    try:
        hitGenExport = next(exp for exp in exports if 'EventHit_GEN_VARIABLE' in exp['ObjectName'])
    except StopIteration:
        # has no hitgen 
        #print(script + " has no hitgen")
        return False
    try:
        relativeScale3D = next(data['Value'] for data in hitGenExport['Data'] if data['Name'] == 'RelativeScale3D')

    except StopIteration:
        #print(script + " added relativeScale to it and nameMap")
        #has no relativeScale3D
        hitGenExport['Data'].append(copy.deepcopy(jsonExports.RELATIVE_SCALE_3D))
        relativeScale3D = hitGenExport['Data'][-1]['Value']
        file.json['NameMap'].append("RelativeScale3D")
    
    vectorValues = relativeScale3D[0]['Value']

    vectorValues['X'] *= scale
    vectorValues['Y'] *= scale
    vectorValues['Z'] *= scale
    
    file.updateFileWithJson(file.json)
    return True

def updateCutsceneModels(encounterReplacements, bossReplacements, config):
    startTime = datetime.datetime.now()
    cutsceneFiles = Script_File_List()
    totalFiles = len(EVENT_CUTSCENES.keys())
    currentFileIndex = 0
    for event, syncDemons in EVENT_CUTSCENES.items():
        replacementMap = {}
        currentFileIndex += 1
        for syncDemon in syncDemons:
            originalDemonID = syncDemon.ind
            syncDemonID = syncDemon.sync
            if syncDemonID in numbers.SCRIPT_JOIN_DEMONS.values() and not config.ensureDemonJoinLevel: #If demon isn't getting replaced ignore it
                continue
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
            try: #Does replacement boss use a different model that has no tie to their id
                replacementID = MODEL_SYNC[replacementID]
            except KeyError:
                #replacementID = 934 #Testing stuff for event hit scaling
                pass 
            try: #Does original boss use a different model that has no tie to their id
                originalDemonID = MODEL_SYNC[originalDemonID]
            except KeyError:
                #replacementID = 934 #Testing stuff for event hit scaling
                pass
            if DEBUG_BIG_MODEL_TEST:
                replacementID = random.choice(DEBUG_MODELS) #Testing big demon models (Tiamat, Abdiel Naho, Nuwa Naho)
            # if originalDemonID in replacementMap.values():
            #     print("Causes Chain replacement: " + str(originalDemonID) + " " + str(replacementID) )
            if replacementID not in replacementMap.values(): #This is because if two different models get replaced by the same, they cannot be differentiated in sequences. TODO: Figure out a way to to what events with multiple copies do aka DevXXX_Y for the variable/export names
                replacementMap[originalDemonID] = replacementID


        file = cutsceneFiles.getFile(event)
        
        
        rawCode = prepareScriptFileForModelReplacement(event, file)
        if rawCode: #script does not have byte code so continue with next one (Debug print happens elsewhere)
            continue
        #TODO:Also might be problematic if replacement is a demon that is already in event, but not swapped EX: Dead Powers in the Nuwa I event
        for originalDemonID, replacementID in replacementMap.items():
            file = replaceDemonModelInScript(event, file, originalDemonID, replacementID)
        cutsceneFiles.setFile(event,file)
        
        if event in LV_SEQUENCES.keys():
            for seq in LV_SEQUENCES[event]:
                fileSeq = cutsceneFiles.getFile(seq)
                for originalDemonID, replacementID in replacementMap.items():
                    fileSeq = replaceDemonInSequence(seq,fileSeq,originalDemonID,replacementID,event)
            cutsceneFiles.setFile(seq,fileSeq)
            cutsceneFiles.writeFile(seq,fileSeq)
        
        print("Swapped Models for " + str(currentFileIndex) + " of " + str(totalFiles) + " Cutscenes", end='\r')
        cutsceneFiles.writeFile(event,file)
    cutsceneFiles.writeFiles()
    del cutsceneFiles
    endTime = datetime.datetime.now()
    print(endTime - startTime)


def replaceDemonInSequence(seq, file:Script_File, ogDemonID, replacementDemonID,event):
    
    '''
    Replaces ids in animation or blueprint class strings
    '''
    def replaceOldIDinString(string):
        if ("/Blueprints/Character" in string or "_C" in string):
            nstring = string.replace(classOldFolderPrefix + classOldPrefix + oldIDString, classNewFolderPrefix + classNewPrefix +newIDString).replace(classOldPrefix + oldIDString, classNewPrefix +newIDString)
            nstring = nstring.replace(classOldFolderPrefix + classOldPrefixVariant + oldIDString, classNewFolderPrefix + classNewPrefixVariant +newIDString).replace(classOldPrefixVariant + oldIDString, classNewPrefixVariant +newIDString)
            nstring = replaceNonExistentAnimations(seq, nstring,newIDString,newName, classOldFolderPrefix, classOldPrefix, classNewFolderPrefix, classNewPrefix, lahmuSuffix)
        else:
            nstring = string.replace(oldFolderPrefix + oldPrefix + oldIDString, newFolderPrefix + newPrefix +newIDString).replace(oldPrefix + oldIDString, newPrefix +newIDString)
            nstring = nstring.replace(oldFolderPrefix + oldPrefixVariant + oldIDString, newFolderPrefix + newPrefixVariant +newIDString).replace(oldPrefixVariant + oldIDString, newPrefixVariant +newIDString)
            nstring = replaceNonExistentAnimations(seq, nstring,newIDString,newName, oldFolderPrefix, oldPrefix, newFolderPrefix, newPrefix, lahmuSuffix)
        return nstring

    jsonData = file.json
    if file.originalNameMap is None: #use original name map to prevent chain replacements
        file.originalNameMap = copy.deepcopy(jsonData['NameMap'])
        file.exportNameList = [exp['ObjectName'] for exp in jsonData["Exports"]]
    #Get the Strings corresponding to the old demon and the prefixes
    oldIDString = DEMON_ID_MODEL_ID[ogDemonID]
    oldName = MODEL_NAMES[oldIDString]
    oldFolderPrefix = DEVIL_PREFIX
    oldPrefix = "dev"
    oldPrefixVariant = "Dev"
    if int(oldIDString) > NPC_MODEL_START :
        oldFolderPrefix = NPC_PREFIX
        oldPrefix = "npc"
        oldPrefixVariant = "Npc"
    #Get the Strings corresponding to the new demon and the prefixes
    try:
        newIDString = DEMON_ID_MODEL_ID[replacementDemonID]
    except KeyError:
        print(str(replacementDemonID) + " needs a model tied to it. Stopping replacement")
        return file
    newName = MODEL_NAMES[newIDString]
    newPrefix = "dev"
    newFolderPrefix = DEVIL_PREFIX
    newPrefixVariant = "Dev"
    if int(newIDString) > NPC_MODEL_START:
        newPrefix = "npc"
        newFolderPrefix = NPC_PREFIX
        newPrefixVariant = "Npc"
    if replacementDemonID == LAHMU_2ND_FORM_ID:
        lahmuSuffix = "_3rd"
    else:
        lahmuSuffix = ""
    if DEBUG_SWAP_PRINT:
        print("SWAP: " + oldPrefix +"/" +  oldName + " -> " + newPrefix +"/"+ newName + " in " + seq)

    #There are some special cases for these class blueprints
    classOldFolderPrefix = copy.deepcopy(oldFolderPrefix)
    classOldPrefix = copy.deepcopy(oldPrefix)
    classOldPrefixVariant = copy.deepcopy(oldPrefixVariant)
    classNewFolderPrefix = copy.deepcopy(newFolderPrefix)
    classNewPrefix = copy.deepcopy(newPrefix)
    classNewPrefixVariant = copy.deepcopy(newPrefixVariant)
    if int(newIDString) in NPC_MODELS_DEV_BLUEPRINT:
        #only new is exception that use devil instead of npc for this
        classNewFolderPrefix = DEVIL_PREFIX
        classNewPrefix = "dev"
        classNewPrefixVariant = "Dev"
        
    elif int(oldIDString) in NPC_MODELS_DEV_BLUEPRINT and event not in FOLDER_SWITCH_RESTRICTIONS:
        #old is exception that use devil instead of npc for this
        classOldFolderPrefix = DEVIL_PREFIX
        classOldPrefix = "dev"
        classOldPrefixVariant = "Dev"
    
    
    for index, name in enumerate(file.originalNameMap):
        if "DevilBaseLight" in name and 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] :
            #Applies to CoC Nuwa Gate, Kunitsukami Fight, Dagda, 4 Heavenly Kings, Pisaca Quest Anahita Event, Konohana Sakuya, Nozuchi, Huang Long
            #print("DEVIL BASE LIGHT CRASH POSSIBLE FOR:" + script)
            return file # since we might run into softlocks otherwise
    #print("NO DEVIL BASE LIGHT CRASH POSSIBLE FOR:" + script)

    

    for index, name in enumerate(file.originalNameMap): #change occurences of oldDemonID and oldDemonName in all names in the uasset
        nameEntry = file.getNameAtIndex(index)
        if seq in name:
            #Do not change names for Main File Exports if DemonId or Name is in script
            continue
        if oldIDString in name and ("/Blueprints/Character" in name or "_C" in name): 
            nameEntry = nameEntry.replace(classOldFolderPrefix + classOldPrefix + oldIDString, classNewFolderPrefix + classNewPrefix +newIDString).replace(classOldPrefix + oldIDString, classNewPrefix +newIDString)
            nameEntry = nameEntry.replace(classOldFolderPrefix + classOldPrefixVariant + oldIDString, classNewFolderPrefix + classNewPrefixVariant +newIDString).replace(classOldPrefixVariant + oldIDString, classNewPrefixVariant +newIDString)
            if 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] and "_Simple" in name: #change bp name if demon does not have simple blueprint
                nameEntry = nameEntry.replace("_Simple","")
        elif oldIDString in name and not "Spawn" in name: #to just get the model names since sometimes DevXXX or devXXX
            nameEntry = nameEntry.replace(oldFolderPrefix + oldPrefix + oldIDString, newFolderPrefix + newPrefix +newIDString).replace(oldPrefix + oldIDString, newPrefix +newIDString)
            nameEntry = nameEntry.replace(oldFolderPrefix + oldPrefixVariant + oldIDString, newFolderPrefix + newPrefixVariant +newIDString).replace(oldPrefixVariant + oldIDString, newPrefixVariant +newIDString)
            if 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] and "_Simple" in name: #change bp name if demon does not have simple blueprint
                nameEntry = nameEntry.replace("_Simple","")
        if oldName in name and ("Character" in name or "Anim" in name): #to prevent stuff like replacing set(seth) in LoadAsset
            #print(nameEntry)
            nameEntry = nameEntry.replace(oldName,newName)
        # elif oldName in name:
        #     print("EXTRA CHECK Necessary? " + nameEntry)
        if "Anim/" in name or name[:3] == "AN_":
            nameEntry = replaceNonExistentAnimations(event, nameEntry,newIDString,newName, classOldFolderPrefix, classOldPrefix, classNewFolderPrefix, classNewPrefix, lahmuSuffix)
        file.setNameAtIndex(index,nameEntry)

    
    movieSceneName = "MovieScene_0"
    file.exportIndex = file.exportNameList.index(movieSceneName)

    dataNames = [exp['Name'] for exp in file.originalJson["Exports"][file.exportIndex]["Data"]]
    possessables = file.uasset.Exports[file.exportIndex].Data[dataNames.index("Possessables")]
    objectBindings = file.uasset.Exports[file.exportIndex].Data[dataNames.index('ObjectBindings')]

    for i,possessable in enumerate(possessables.Value):
        if oldIDString in file.originalJson["Exports"][file.exportIndex]["Data"][dataNames.index("Possessables")]["Value"][i]["Value"][2]["Value"]:
            possessable.Value[2].Value.Value = replaceOldIDinString(possessable.Value[2].Value.Value)
    
    for i,objectBinding in enumerate(objectBindings.Value):
        if oldIDString in file.originalJson["Exports"][file.exportIndex]["Data"][dataNames.index("ObjectBindings")]["Value"][i]["Value"][1]["Value"]:
            objectBinding.Value[1].Value.Value = replaceOldIDinString(objectBinding.Value[1].Value.Value)
    if seq == 'SEQ_E2297_C20':
        file.exportIndex = file.exportNameList.index('SEQ_E2297_c20')
    else:
        file.exportIndex = file.exportNameList.index(seq)
    bindList = file.uasset.Exports[file.exportIndex].Data[1].Value[0].Value
    for i,entry in enumerate(bindList):
        try:
            if oldIDString in file.originalJson["Exports"][file.exportIndex]["Data"][1]["Value"][0]["Value"][i][1]["Value"][0]["Value"][0]["Value"][0]["Value"][0]["Value"]["SubPathString"]:
                entry.Value.Value[0].Value[0].Value[0].Value[0].Value.SubPathString.Value = replaceOldIDinString(entry.Value.Value[0].Value[0].Value[0].Value[0].Value.SubPathString.Value)
        except (TypeError, AttributeError) as e:
            #not bad error, just too lazy to stop differently
            pass
    return file
