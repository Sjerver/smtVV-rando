from base_classes.uasset import UAsset
from util.binary_table import Table
from base_classes.script_logic import readBinaryTable, writeBinaryTable, writeFolder
import util.numbers as numbers

class Message_Uasset(UAsset):
    def __init__(self, binaryTable: Table):
        UAsset.__init__(self, binaryTable)

class Message_Uexp():
    def __init__(self, binaryTable: Table):
        self.binaryTable = binaryTable

        self.fileSize = binaryTable.readWord(0x10)
        self.arraySize = binaryTable.readWord(0x21) # amounts to number of messages
        self.structSize = binaryTable.readWord(0x35)


class Message():
    def __init__(self):
        self.pageDataSize = None
        self.pages = []
        self.ind = None
        self.label = None
        self.name = None
        self.voice = None
        self.cue = None
        self.lipSync = None
    
    '''
    Returns the actual text of the message.
    '''
    def getText(self):
        return self.pages[2].string

    '''
    Set the text of the message and recalculate the it in bytes form.
        Parameters:
            text(String): the text this message should have
    '''
    def setText(self, text):
        self.pages[2].string = text
        self.pages[2].bytes = self.pages[2].encode()


class Message_Page():
    def __init__(self, bytes, encoding):
        self.bytes = bytes
        self.encoding = encoding
        self.string = self.decode()

    '''
    Obtain the string contained in the bytes of this page.
    '''
    def decode(self):
        if self.encoding == 'ascii':
            return str(self.bytes)[2:-5]
        else:
            return self.bytes.decode("utf-16")
    
    '''
    Obtain the bytes of the pages string.
    '''
    def encode(self):
        if self.encoding == 'ascii':
            return bytes(self.string + '\x00' ,'utf-8')
        else:
            return self.string.encode("utf-16")


class Message_File:
    def __init__(self, fileName, baseFolder):
        self.messages = []
        self.fileName = fileName
        self.randoFolder = OUTPUT_FOLDERS[fileName]
        self.baseFolder = baseFolder

        self.uexp = Message_Uexp(readBinaryTable('base/LN10/' + baseFolder + fileName + '.uexp'))
        self.uasset = Message_Uasset(readBinaryTable('base/LN10/' + baseFolder + fileName + '.uasset'))  
        
        self.initializeMessages(self.messages, self.uexp.binaryTable)
    
    '''
    Initializes all messages in this message asset file.
        Parameters:
            messages(List): List to fill with messages
            uexpBinary(Table): the binary of this message file's uexp for easier access
    '''
    def initializeMessages(self, messages, uexpBinary:Table):
        if uexpBinary == None:
            uexpBinary = self.uexp.binaryTable
        start = 0x56
        currentOffset = start
        
        additionalBytes = 0
        for index in range (self.uexp.arraySize):
            message = Message()
            message.ind = uexpBinary.readWord(currentOffset + 25 + additionalBytes)
            message.label = self.uasset.nameList[uexpBinary.readWord(currentOffset + 54 + additionalBytes)]
            currentOffset = currentOffset + 104 #just before page start aka first page size
            message.pageDataSize = uexpBinary.readDblword(currentOffset + additionalBytes - 26)
            for i in range(3):
                
                pageSize = uexpBinary.readWord(currentOffset + additionalBytes + 4* i)
                encoding = 'ascii' 
                if pageSize < 0: #2 byte chars
                    pageSize = pageSize * -2
                    encoding = 'utf-8' 
                bytes = uexpBinary.readXChars(pageSize, currentOffset + additionalBytes + 4* i + 4)
                page = Message_Page(bytes,encoding)
                message.pages.append(page)
                additionalBytes = additionalBytes + pageSize
            
            currentOffset = currentOffset + 8 * 3 + 99#name Size
            nameSize = uexpBinary.readWord(currentOffset + additionalBytes)
            message.name = uexpBinary.readXChars(nameSize,currentOffset + additionalBytes + 4)
            additionalBytes = additionalBytes + nameSize

            currentOffset = currentOffset + 4 + 25#voice Size
            voiceSize = uexpBinary.readWord(currentOffset + additionalBytes)
            message.voice = uexpBinary.readXChars(nameSize,currentOffset + additionalBytes + 4)
            additionalBytes = additionalBytes + voiceSize

            currentOffset = currentOffset + 4 + 21 + 4#value 2 of cue
            message.cue = self.uasset.nameList[uexpBinary.readWord(currentOffset + additionalBytes)]

            currentOffset = currentOffset + 8 + 21 + 4 + 4#value 2 of lipsync
            message.lipSync = self.uasset.nameList[uexpBinary.readWord(currentOffset + additionalBytes)]

            currentOffset = currentOffset + 8 + 102 +4

            messages.append(message)

    '''
    Returns a list of this files message strings.
    '''
    def getMessageStrings(self):
        array = []
        for message in self.messages:
            array.append(message.getText())
        return array

    '''
    Sets this files message strings to the ones in the passed list.
        Parameters:
            newMessages(List(String)): a list of strings that the message with the same index should be set to
    '''
    def setMessageStrings(self, newMessages):
        for index, message in enumerate(self.messages):
            message.setText(newMessages[index])
    
    '''
    Writes the data of this message file to both the uexp and uasset, and outputs it to the appropriate rando subfolders.
    '''
    def writeToFiles(self):
        sizeDiff = self.updateUexp()

        self.uasset.binaryTable.writeWord(self.uasset.exports[0].serialSize + sizeDiff , self.uasset.exportOffset + 28)
        self.uasset.bulkDataOffset = self.uasset.bulkDataOffset  + sizeDiff
        
        self.uasset.writeDataToBinaryTable()

        for folder in FOLDERS_TO_CREATE:
            writeFolder(folder)
        
        writeBinaryTable(self.uexp.binaryTable.buffer, self.randoFolder + self.fileName + '.uexp', self.randoFolder)
        writeBinaryTable(self.uasset.binaryTable.buffer, self.randoFolder + self.fileName + '.uasset', self.randoFolder)
    
    '''
    Update the binary table for the uexp with the current data.
    '''
    def updateUexp(self):
        sizeDifference = 0 #How much the file differs from the original file
        uexpBinary = self.uexp.binaryTable

        start = 0x56
        currentOffset = start
        additionalBytes = 0 #Additional bytes from String length for modular offsets
        for testIndex,message in enumerate(self.messages):
            currentOffset = currentOffset + 104  #just before page start
            messageSizeDiff = 0 #How much this message differs in size 
            messageAddBytes = 0 #How many bytes the strings from this message add to the modular offsets
            for index,page in enumerate(message.pages):
                pageSize = uexpBinary.readWord(currentOffset + additionalBytes + 4* index)
                if pageSize < 0: #2 byte chars
                    pageSize = pageSize * -2
                originalString = uexpBinary.readXChars(pageSize, currentOffset + additionalBytes + 4* index + 4)
                if index != 2 or page.bytes == originalString or page.encoding != 'ascii' : #Only page 2 is of relevance and only if it has changed (and we temporarily ignore changes in utf-16 strings because encoding doesn't quite work right)
                    additionalBytes = additionalBytes + pageSize
                    messageAddBytes = messageAddBytes + pageSize
                else: # there is a need to rewrite the string in the uexp
                    if pageSize < len(page.bytes): #New string is larger than old one
                        messageSizeDiff = messageSizeDiff +  len(page.bytes) - pageSize
                        sizeDifference = sizeDifference + messageSizeDiff
                        for i in range(len(page.bytes) - pageSize):
                            uexpBinary.buffer.insert(currentOffset+ additionalBytes + 4*index + 4 ,0)
                        uexpBinary.writeWord(len(page.bytes),currentOffset + additionalBytes + 4* index)
                    elif pageSize > len(page.bytes): #New string is smaller than old one
                        messageSizeDiff = messageSizeDiff + (len(page.bytes) - pageSize)
                        sizeDifference = sizeDifference + messageSizeDiff
                        for i in range(pageSize - len(page.bytes)):
                            uexpBinary.buffer.pop(currentOffset + additionalBytes + 4*index + 4)
                        uexpBinary.writeWord(len(page.bytes),currentOffset + additionalBytes + 4* index)
                    pageSize = len(page.bytes)
                    uexpBinary.writeXChars(page.bytes, pageSize, currentOffset + additionalBytes + 4* index + 4)
                    additionalBytes = additionalBytes + pageSize
                    messageAddBytes = messageAddBytes + pageSize
            uexpBinary.writeDblword(messageSizeDiff + message.pageDataSize, currentOffset + additionalBytes - messageAddBytes - 26)
            currentOffset = currentOffset + 24 + 99 + 4 + 25 + 25+ 4 + 8+ 25 +4 + 8+ 102 +4
            
        self.uexp.fileSize = self.uexp.fileSize + sizeDifference
        self.uexp.structSize = self.uexp.structSize + sizeDifference
        uexpBinary.writeWord(self.uexp.fileSize, 0x10)
        uexpBinary.writeWord(self.uexp.structSize, 0x35)
            
        return sizeDifference

OUTPUT_FOLDERS = {
    'ItemName' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
    'SkillHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Battle/Skill/',
}

#List of folders that have to be created in the output folder in order of creation
FOLDERS_TO_CREATE = ['rando',
        'rando/Project',
        'rando/Project/Content',
        'rando/Project/Content/L10N',
        'rando/Project/Content/L10N/en',
        'rando/Project/Content/L10N/en/Blueprints',
        'rando/Project/Content/L10N/en/Blueprints/Gamedata',
        'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable',
        'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Battle',
]    

#Dict for items with demon names in them and which demon they should be synced with
ITEM_NAME_SYNC_DEMON_IDS = {
    'Jatayu Egg' : 802, #Punishing Foe Jatayu
    'Bicorn Horn' : 146, #Bicorn
    'Mothman Capture Pot': 147,#Mothman
    "Kumbhanda's Bottle" : 809,#Punishing Foe Kumbhanda
    "Girimekhala's Head" : 827,#Punishing Foe Girimekhala
    "Inugami's Head" : 138,#Inugami
    "Horus's Head" : 864,#Punishing Foe Horus
}

SKILL_DESC_CHANGES = {
    295 : '(Unique) Significantly raises Accuracy/Evasion of <skill_tgt> by 2 ranks for 3 turns.', #Red Capote Boss Version
}

'''
Changes the names of items with demon names in them to that of their replacement if there is any
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        compNames(List(String)): list of demon names
        bossNames(list(String)): list of boss names
'''
def updateItemTextWithDemonNames(encounterReplacements, bossReplacements, compNames, bossNames):  
    
    itemFile = Message_File('ItemName','')

    itemNames = itemFile.getMessageStrings()
    
    for itemName,originalDemonID in ITEM_NAME_SYNC_DEMON_IDS.items():
        if itemName in itemNames:
            if originalDemonID > numbers.NORMAL_ENEMY_COUNT:
                originalName = bossNames[originalDemonID]
                try:
                    replacementID = bossReplacements[originalDemonID]
                except KeyError:
                    continue
            else:
                originalName = compNames[originalDemonID]
                try:
                    replacementID = encounterReplacements[originalDemonID]
                except KeyError:
                    continue
            if replacementID > numbers.NORMAL_ENEMY_COUNT:
                replacementName = bossNames[replacementID]
            else:
                replacementName = compNames[replacementID]
            index = itemNames.index(itemName)
            itemNames[index] = itemNames[index].replace(originalName, replacementName)
            print(str(index) + " " + itemNames[index])
    
    itemFile.setMessageStrings(itemNames)
    itemFile.writeToFiles()

'''
Changes the skill descriptions of skills with the same name to differentiate them.
'''
def changeSkillDescriptions(file: Message_File):

    skillDescriptions = file.getMessageStrings()

    for skillID, newDesc in SKILL_DESC_CHANGES.items():
        print(skillDescriptions[skillID-1])
        skillDescriptions[skillID-1] = newDesc
    
    file.setMessageStrings(skillDescriptions)
    return file

'''
Updates skill descriptions of skills with the same name and updates the unique signifier.
'''
def updateSkillDesriptions():
    file = Message_File('SkillHelpMess','')
    file = changeSkillDescriptions(file)
    #TODO: Add function to update (Unique) to reflect inheritance setting and demons
    file.writeToFiles()



            
            



