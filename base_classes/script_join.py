import random
import os
from util.binary_table import Table
import util.paths as paths

EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event'
SCRIPT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script' 
SUBMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission' 
M061_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061'  

#Key: EventScriptName, Value: List(Numbers) byte offsets where demon join is decided/checked
SCRIPT_JOIN_BYTES = {
    'MM_M061_EM1630': [149119,211659], # The Water Nymph / Leanan Sidhe
    'MM_M061_EM1640': [165053,204312], # The Spirit of Love / Apsaras
}
# Is this important???
SCRIPT_JOINS = {
    'MM_M061_EM1630': 305, # The Water Nymph / Leanan Sidhe
    'MM_M061_EM1640': 43, # The Spirit of Love / Apsaras
}

def randomizeDemonJoins(comp):
    writeFolder(EVENT_FOLDER)
    writeFolder(SCRIPT_FOLDER)
    writeFolder(SUBMISSION_FOLDER)
    writeFolder(M061_FOLDER)
    for script, offsets in SCRIPT_JOIN_BYTES.items():
        referenceDemon = comp[SCRIPT_JOINS[script]]
        sameLevel = [demon for demon in comp if demon.level.value == referenceDemon.level.original]
        if len(sameLevel) <1:
             sameLevel = comp
        newDemon = random.choice(sameLevel)

        scriptData = readBinaryTable('base/Scripts/SubMission/' + script + '.uexp')

        scriptData.writeHalfword(newDemon.ind, offsets[0])
        scriptData.writeHalfword(newDemon.ind, offsets[1])

        writeBinaryTable(scriptData.buffer, M061_FOLDER + '/' + script + '.uexp', M061_FOLDER)



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
        os.mkdir(folderPath)
    with open(filePath, 'wb') as file:
        file.write(result)

def writeFolder(folderPath):
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)       