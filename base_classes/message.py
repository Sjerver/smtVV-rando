from base_classes.uasset_custom import UAsset_Custom
from util.binary_table import Table
from script_logic import readBinaryTable, writeBinaryTable, writeFolder
from .file_lists import General_UAsset

class Demon_Sync:
    def __init__(self,ind, sync=None, nameVariant=None):
        self.ind = ind
        self.sync = ind
        if sync:
            self.sync = sync
        self.nameVariant = nameVariant

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
            newNames(List(Bytes)): a list of byte strings that the speaker name with the same index should be set to
    '''
    def setSpeakerNames(self, newNames):
        currentIndex = 0
        for message in self.messages:
            for pageData in message.pageDataArray:
                pageData.name = newNames[currentIndex]
                currentIndex += 1
            
    '''
    Sets this files voices to the ones in the passed list.
        Parameters:
            newVoices(List(Bytes)): a list of byte strings that the voice with the same index should be set to
    '''
    def setVoices(self, newVoices):
        currentIndex = 0
        for message in self.messages:
            for pageData in message.pageDataArray:
                pageData.voice = newVoices[currentIndex]
                currentIndex += 1   
    
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
                #table[index]["Value"][3]["Value"][pageIndex]["Value"][2]["Value"]["AssetPath"]["AssetName"] = message.pageDataArray[pageIndex].cue