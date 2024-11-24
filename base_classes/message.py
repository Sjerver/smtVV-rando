from base_classes.uasset_custom import UAsset_Custom
from util.binary_table import Table
from script_logic import readBinaryTable, writeBinaryTable, writeFolder

class Demon_Sync:
    def __init__(self,ind, sync=None, nameVariant=None):
        self.ind = ind
        self.sync = ind
        if sync:
            self.sync = sync
        self.nameVariant = nameVariant

class Message_Uasset(UAsset_Custom):
    def __init__(self, binaryTable: Table):
        UAsset_Custom.__init__(self, binaryTable)

class Message_Uexp():
    def __init__(self, binaryTable: Table):
        self.binaryTable = binaryTable

        self.fileSize = binaryTable.readWord(0x10)
        self.arraySize = binaryTable.readWord(0x21) # amounts to number of messages
        self.structSize = binaryTable.readWord(0x35)

class Page_Data():
    def __init__(self):
        self.name = None
        self.voice = None
        self.cue = None
        self.lipSync = None

class Message():
    def __init__(self):
        self.pageDataSize = None
        self.metadataSize = None
        self.pages = []
        self.ind = None
        self.label = None
        self.pageDataArray = []
        self.pageDataCount = None
        self.pageCount = None
        self.pageless = None

class Message_Page():
    def __init__(self):
        self.textEntries = []

    '''
    Returns the actual text of the message.
    '''
    def getText(self):
        return self.textEntries[2].string

    '''
    Set the text of the message and recalculate the it in bytes form.
        Parameters:
            text(String): the text this message should have
    '''
    def setText(self, text):
        # print(self.textEntries[2].encoding)
        self.textEntries[2].string = text
        self.textEntries[2].bytes = self.textEntries[2].encode()


class Message_Page_Text_Entry():
    def __init__(self, bytes, encoding):
        self.bytes = bytes
        self.encoding = encoding
        self.string = self.decode()

    '''
    Obtain the string contained in the bytes of this page.
    '''
    def decode(self):
        if self.encoding == 'ascii':
            return self.bytes.decode('ascii')[:-1]
        else:
            return self.bytes.decode("utf-16-le")[:-1]
    
    '''
    Obtain the bytes of the pages string.
    '''
    def encode(self):
        string = self.string + '\x00'
        try:
            return string.encode(self.encoding)
        except UnicodeEncodeError:
            self.encoding = "utf-16-le"
        return string.encode(self.encoding)


class Message_File:
    def __init__(self, fileName, baseFolder, outputFolder):
        #print("READ: " + fileName)
        self.messages = []
        self.fileName = fileName
        self.randoFolder = outputFolder
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
            message.pageCount = uexpBinary.readWord(currentOffset + additionalBytes - 9)
            message.pageDataSize = uexpBinary.readDblword(currentOffset + additionalBytes - 26)
            message.pageless = 255 == uexpBinary.readByte(currentOffset + additionalBytes -1)
            if message.pageless:
                currentOffset =currentOffset -8
            else:
                for pageIndex in range(message.pageCount):
                    page = Message_Page()
                    for i in range(3):
                        #print(message.label)
                        pageSize = uexpBinary.readWord(currentOffset + additionalBytes + 4* i + 17 * pageIndex)
                        encoding = 'ascii' 
                        if pageSize < 0: #2 byte chars
                            pageSize = pageSize * -2
                            encoding = 'utf-16-le' 
                        bytes = uexpBinary.readXChars(pageSize, currentOffset + additionalBytes + 4* i + 4 + 17 * pageIndex)
                        pageTextEntry = Message_Page_Text_Entry(bytes,encoding)
                        page.textEntries.append(pageTextEntry)
                        additionalBytes = additionalBytes + pageSize
                    message.pages.append(page)
            
           
            currentOffset =currentOffset + 8 * 3 + 17*message.pageCount + 4
            message.pageDataCount = uexpBinary.readWord(currentOffset+ additionalBytes)
            message.metadataSize = uexpBinary.readWord(currentOffset+ additionalBytes-17)
            currentOffset = currentOffset + 78 #name Size
            for i in range(message.pageDataCount):
                pageData = Page_Data()

                nameSize = uexpBinary.readWord(currentOffset + additionalBytes)
                pageData.name = uexpBinary.readXChars(nameSize,currentOffset + additionalBytes + 4)
                additionalBytes = additionalBytes + nameSize

                currentOffset = currentOffset + 4 + 25#voice Size
                voiceSize = uexpBinary.readWord(currentOffset + additionalBytes)
                pageData.voice = uexpBinary.readXChars(nameSize,currentOffset + additionalBytes + 4)
                additionalBytes = additionalBytes + voiceSize

                currentOffset = currentOffset + 4 + 21 + 4#value 2 of cue
                pageData.cue = self.uasset.nameList[uexpBinary.readWord(currentOffset + additionalBytes)]

                currentOffset = currentOffset + 8 + 21 + 4 + 4#value 2 of lipsync
                pageData.lipSync = self.uasset.nameList[uexpBinary.readWord(currentOffset + additionalBytes)]

                message.pageDataArray.append(pageData)
                if message.pageDataCount -1 > i:
                    currentOffset = currentOffset + 45

            currentOffset = currentOffset + 8 + 102 +4

            messages.append(message)

    '''
    Returns a list of this files message strings.
    '''
    def getMessageStrings(self):
        array = []
        for message in self.messages:
            for page in message.pages:
                array.append(page.getText())
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
    Sets this files message strings to the ones in the passed list.
        Parameters:
            newMessages(List(String)): a list of strings that the message with the same index should be set to
    '''
    def setMessageStrings(self, newMessages):
        currentIndex = 0
        for index, message in enumerate(self.messages):
            for page in message.pages:
                page.setText(newMessages[currentIndex])
                currentIndex += 1
                
    '''
    Sets this files speaker names to the ones in the passed list.
        Parameters:
            newNames(List(String)): a list of strings that the speaker name with the same index should be set to
    '''
    def setSpeakerNames(self, newNames):
        currentIndex = 0
        for index, message in enumerate(self.messages):
            if len(message.pageDataArray) > 0:
                oldNameSize = len(message.pageDataArray[0].name) 
                newNameSize = len(newNames[currentIndex])
                nameSizeDiff = newNameSize - oldNameSize
                message.metadataSize += nameSizeDiff * len(message.pageDataArray)
                #print(nameSizeDiff)
                #message.pageDataSize += nameSizeDiff #Update pageDataSize value, unsure if this is correct (I think it's not)
            for pageData in message.pageDataArray:
                pageData.name = newNames[currentIndex]
                currentIndex += 1
            
                
    
    '''
    Writes the data of this message file to both the uexp and uasset, and outputs it to the appropriate rando subfolders.
    '''
    def writeToFiles(self):
        sizeDiff = self.updateUexp()

        #self.uasset.binaryTable.writeWord(self.uasset.exports[0].serialSize + sizeDiff , self.uasset.exportOffset + 28)
        self.uasset.exports[0].serialSize = self.uasset.exports[0].serialSize + sizeDiff
        self.uasset.bulkDataOffset = self.uasset.bulkDataOffset  + sizeDiff
        
        self.uasset.writeDataToBinaryTable()
        
        writeBinaryTable(self.uexp.binaryTable.buffer, self.randoFolder + self.fileName + '.uexp', self.randoFolder)
        writeBinaryTable(self.uasset.binaryTable.buffer, self.randoFolder + self.fileName + '.uasset', self.randoFolder)

    '''
    Update the binary table for the uexp with the current data.
    '''
    def updateUexp(self):
        #print("WRITE: " + self.fileName)
        sizeDifference = 0 #How much the file differs from the original file
        uexpBinary = self.uexp.binaryTable

        start = 0x56
        currentOffset = start
        additionalBytes = 0 #Additional bytes from String length for modular offsets
        for testIndex,message in enumerate(self.messages):
            #print(message.label + " " + str(currentOffset + additionalBytes))
            currentOffset = currentOffset + 104  #just before page start
            messageSizeDiff = 0 #How much this message differs in size 
            messageAddBytes = 0 #How many bytes the strings from this message add to the modular offsets
            if message.pageless:
                    uexpBinary.writeDblword(messageSizeDiff + message.pageDataSize, currentOffset + additionalBytes - messageAddBytes - 26)
                    currentOffset =currentOffset -8
            for pageIndex, page in enumerate(message.pages):
                for index,pageTextEntry in enumerate(page.textEntries):
                    pageSize = uexpBinary.readWord(currentOffset + additionalBytes + 4* index + 17 * (pageIndex))
                    if pageSize < 0: #2 byte chars
                        pageSize = pageSize * -2
                    originalString = uexpBinary.readXChars(pageSize, currentOffset + additionalBytes + 4* index + 4 + 17 * (pageIndex))
                    if index != 2 or pageTextEntry.bytes == originalString : #Only page 2 is of relevance and only if it has changed 
                        additionalBytes = additionalBytes + pageSize
                        messageAddBytes = messageAddBytes + pageSize
                    else: # there is a need to rewrite the string in the uexp
                        if pageSize < len(pageTextEntry.bytes): #New string is larger than old one
                            messageSizeDiff = messageSizeDiff +  len(pageTextEntry.bytes) - pageSize
                            for i in range(len(pageTextEntry.bytes) - pageSize):
                                uexpBinary.buffer.insert(currentOffset+ additionalBytes + 4*index + 4 + 17 * (pageIndex),0)
                            if pageTextEntry.encoding == 'ascii':
                                uexpBinary.writeWord(len(pageTextEntry.bytes),currentOffset + additionalBytes + 4* index + 17 * (pageIndex))
                            else:
                                uexpBinary.writeWord(len(pageTextEntry.bytes) // -2,currentOffset + additionalBytes + 4* index + 17 * (pageIndex))
                        elif pageSize > len(pageTextEntry.bytes): #New string is smaller than old one
                            messageSizeDiff = messageSizeDiff + (len(pageTextEntry.bytes) - pageSize)
                            for i in range(pageSize - len(pageTextEntry.bytes)):
                                uexpBinary.buffer.pop(currentOffset + additionalBytes + 4*index + 4 + 17 * (pageIndex))
                            if pageTextEntry.encoding == 'ascii':
                                uexpBinary.writeWord(len(pageTextEntry.bytes),currentOffset + additionalBytes + 4* index + 17 * (pageIndex))
                            else:
                                uexpBinary.writeWord(len(pageTextEntry.bytes) // -2,currentOffset + additionalBytes + 4* index + 17 * (pageIndex))
                        pageSize = len(pageTextEntry.bytes)
                        uexpBinary.writeXChars(pageTextEntry.bytes, pageSize, currentOffset + additionalBytes + 4* index + 4 + 17 * (pageIndex))
                        additionalBytes = additionalBytes + pageSize
                        messageAddBytes = messageAddBytes + pageSize
                        
                uexpBinary.writeDblword(messageSizeDiff + message.pageDataSize, currentOffset + additionalBytes - messageAddBytes - 26)
            sizeDifference = sizeDifference + messageSizeDiff

            #TODO: Add code for writing if voice is changed later, currently only read for offset calc
            currentOffset =currentOffset + 8 * 3 + 17*message.pageCount + 4 + 78#name Size
            uexpBinary.writeWord(message.metadataSize, currentOffset + additionalBytes - 78 - 17)
            uexpBinary.writeWord(message.metadataSize-53, currentOffset + additionalBytes - 78 - 17 + 37) #Magic number 53 less than the metadata size
            for i, page in enumerate(message.pageDataArray):
                oldNameSize = uexpBinary.readWord(currentOffset + additionalBytes)
                newNameSize = len(page.name)
                nameSizeDiff = newNameSize - oldNameSize
                uexpBinary.writeWord(newNameSize, currentOffset + additionalBytes)
                uexpBinary.writeByte(newNameSize + 4, currentOffset + additionalBytes - 9) #The byte 9 before the name size word is equal to the name size + 4
                if nameSizeDiff > 0: #New string is larger than old one
                    sizeDifference = sizeDifference + nameSizeDiff
                    for j in range(nameSizeDiff):
                        uexpBinary.buffer.insert(currentOffset + additionalBytes + 4 ,0)
                elif nameSizeDiff < 0: #New string is smaller than old one
                    sizeDifference = sizeDifference + nameSizeDiff
                    for j in range(-nameSizeDiff):
                        uexpBinary.buffer.pop(currentOffset + additionalBytes + 4)
                uexpBinary.writeXChars(page.name, newNameSize,currentOffset + additionalBytes + 4) #Update speaker name
                additionalBytes = additionalBytes + newNameSize

                currentOffset = currentOffset + 4 + 25#voice Size
                voiceSize = uexpBinary.readWord(currentOffset + additionalBytes)
                additionalBytes = additionalBytes + voiceSize

                currentOffset = currentOffset + 4 + 21 + 4 + 8 + 21 + 4 + 4
                if message.pageDataCount -1 > i:
                    currentOffset = currentOffset + 45

            currentOffset = currentOffset + 8+ 102 +4
            
        self.uexp.fileSize = self.uexp.fileSize + sizeDifference
        self.uexp.structSize = self.uexp.structSize + sizeDifference
        uexpBinary.writeWord(self.uexp.fileSize, 0x10)
        uexpBinary.writeWord(self.uexp.structSize, 0x35)
            
        return sizeDifference