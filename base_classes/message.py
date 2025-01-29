from base_classes.uasset_custom import UAsset_Custom
from util.binary_table import Table
from script_logic import readBinaryTable, writeBinaryTable, writeFolder
from .file_lists import General_UAsset
import re

CUE_BASE_PATH = '/Game/Sound/CueSheet/Devil/Devil_vo/'
DEMON_ID_OF_CUE_REGEX = '(?<=dev)(.*)(?=_vo)'
SPECIAL_VOICE_TYPES = ['04'] #Voice type numbers that require additional name map data

class Demon_Sync:
    def __init__(self,ind, sync=None, nameVariant=None, isNavi=False):
        self.ind = ind
        self.sync = ind
        if sync:
            self.sync = sync
        self.nameVariant = nameVariant
        self.isNavi = isNavi

class Page_Data():
    def __init__(self):
        self.name = None
        self.voice = None
        self.cue = None
        self.lipSync = None

class Message():
    def __init__(self):
        self.pages = []
        self.ind = None
        self.label = None
        self.pageDataArray = []
        self.pageDataCount = None
        self.pageCount = None

'''
Constructs one or more filepaths to a cue using a demon filename ID. Path differs based on where in the uasset json the file path should go
    Parameters:
        demonID (string): the ID to find the folder from in 3-digit string form
        demonFilenames (dict): keys(string) - numerical filename IDs. values(string) - demon name in the files
        voice (string): The specific voice file to pull. If none, returns the demonID folder path instead
        isNameMap (boolean): If false, appends the full voice after the period instead of just the demon ID
'''
def getCuePath(demonID, demonFilenames, voice=None, isNameMap = False):
    paths = []
    folderName = 'dev' + demonID + '_vo_' + demonFilenames[demonID] + '/'
    path = CUE_BASE_PATH + folderName
    if voice == None:
        paths.append(path + 'dev' + demonID + '_vo')
    elif isNameMap:
        voiceType = voice[10:]
        if voiceType in SPECIAL_VOICE_TYPES:
            paths.append(path + voice)
            paths.append(path + voice + '.' + voice)
        else:
            paths.append(path + voice + '.dev' + demonID + '_vo')
    else:
        paths.append(path + voice + '.' + voice)
    return paths

class Message_File:
    def __init__(self, fileName, baseFolder, outputFolder):
        #print("READ: " + fileName)
        self.messages = []
        self.fileName = fileName
        self.randoFolder = outputFolder
        self.baseFolder = baseFolder
        self.apiUasset = General_UAsset(fileName, outputFolder, readPath='base/LN10/'+baseFolder)
        
        self.initializeMessages()
    
    '''
    Initializes all messages in this message asset file.
    '''
    def initializeMessages(self):
        json = self.apiUasset.json
        table = json["Exports"][0]["Data"][0]["Value"]
        for entry in table:
            message = Message()
            message.ind = entry["Value"][0]["Value"]
            message.label = entry["Value"][1]["Value"]
            message.pageCount = len(entry["Value"][2]["Value"])
            message.pageDataCount = len(entry["Value"][3]["Value"])
            if message.pageCount != message.pageDataCount:
                print("Huge massive issues!")
            for pageJson in entry["Value"][2]["Value"]:
                message.pages.append(pageJson["CultureInvariantString"])
            for pageDataJson in entry["Value"][3]["Value"]:
                pageData = Page_Data()
                pageData.name = pageDataJson["Value"][0]["Value"]
                pageData.voice = pageDataJson["Value"][1]["Value"]
                pageData.cue = pageDataJson["Value"][2]["Value"]["AssetPath"]["AssetName"]
                pageData.lipSync = pageDataJson["Value"][3]["Value"]["AssetPath"]["AssetName"]
                message.pageDataArray.append(pageData)
            self.messages.append(message)

    '''
    Returns a list of this files message strings.
    '''
    def getMessageStrings(self):
        array = []
        for message in self.messages:
            for page in message.pages:
                array.append(page)
        return array
    
    '''
    Returns a list of this files message speaker names.
    '''
    def getSpeakerNames(self):
        array = []
        for message in self.messages:
            for pageData in message.pageDataArray:
                array.append(pageData.name)
        return array

    '''
    Returns a list of this files voices.
    '''
    def getVoices(self):
        array = []
        for message in self.messages:
            for pageData in message.pageDataArray:
                array.append(pageData.voice)
        return array

    '''
    Sets this files message strings to the ones in the passed list.
        Parameters:
            newMessages(List(String)): a list of strings that the message with the same index should be set to
    '''
    def setMessageStrings(self, newMessages):
        currentIndex = 0
        for message in self.messages:
            for pageIndex, _ in enumerate(message.pages):
                message.pages[pageIndex] = newMessages[currentIndex]
                currentIndex += 1
                
    '''
    Sets this files speaker names to the ones in the passed list.
        Parameters:
            newNames(List(string)): a list of strings that the speaker name with the same index should be set to
    '''
    def setSpeakerNames(self, newNames):
        currentIndex = 0
        for message in self.messages:
            for pageData in message.pageDataArray:
                pageData.name = newNames[currentIndex]
                currentIndex += 1
            
    '''
    Sets this files voices and cues to the ones in the passed list.
        Parameters:
            newVoices(List(string)): a list of strings that the voice with the same index should be set to
            demonFilenames
    '''
    def setVoices(self, newVoices, demonFilenames):
        currentIndex = 0
        demonSet = set()
        voiceSet = set()
        for message in self.messages:
            for pageData in message.pageDataArray:
                currentVoice = newVoices[currentIndex]
                pageData.voice = currentVoice
                if currentVoice is not None:
                    match = re.search(DEMON_ID_OF_CUE_REGEX, currentVoice) #Only update cues and files of demon voices, not event voices
                    if match:
                        voiceSet.add(currentVoice)
                        demonID = match.group()
                        demonSet.add(demonID)
                        pageData.cue = getCuePath(demonID, demonFilenames, voice=currentVoice)[0]
                currentIndex += 1
        json = self.apiUasset.json
        nameMap = json["NameMap"]
        nameMap[:] = [x for x in nameMap if not (CUE_BASE_PATH in x and x.endswith("_vo"))] #Remove old cues
        #print(voiceSet)
        for demonID in demonSet:
            nameMap.append(getCuePath(demonID, demonFilenames, isNameMap=True)[0])
        for voiceID in voiceSet:
            demonID = re.search(DEMON_ID_OF_CUE_REGEX, voiceID).group()
            cuePaths = getCuePath(demonID, demonFilenames, voice=voiceID, isNameMap=True)
            for cuePath in cuePaths:
                nameMap.append(cuePath)
        #print(nameMap)

    
    '''
    Writes the data of this message file to both the uexp and uasset, and outputs it to the appropriate rando subfolders.
    '''
    def writeToFiles(self):
        self.updateJson()
        self.apiUasset.write()

    '''
    Updates the UAssetAPI json with the current data
    '''
    def updateJson(self):
        json = self.apiUasset.json
        table = json["Exports"][0]["Data"][0]["Value"]
        for index, message in enumerate(self.messages):
            for pageIndex, page in enumerate(message.pages):
                table[index]["Value"][2]["Value"][pageIndex]["CultureInvariantString"] = page
                table[index]["Value"][3]["Value"][pageIndex]["Value"][0]["Value"] = str(message.pageDataArray[pageIndex].name)
                table[index]["Value"][3]["Value"][pageIndex]["Value"][1]["Value"] = str(message.pageDataArray[pageIndex].voice)
                table[index]["Value"][3]["Value"][pageIndex]["Value"][2]["Value"]["AssetPath"]["AssetName"] = message.pageDataArray[pageIndex].cue