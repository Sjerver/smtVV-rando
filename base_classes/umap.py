from base_classes.uasset import UAsset
from util.binary_table import readBinaryTable, writeBinaryTable, Table

M061_FOLDER = 'rando/Project/Content/Level/Event/M061'

UMAP_FOLDERS = {
    'LV_EventMission_M061': M061_FOLDER,
    'LV_MainMission_M061': M061_FOLDER,
}

class UMap_File_List:
    def __init__(self):
        self.files = []
        self.fileNames = []

    '''
    Returns a umap file for the given file name. 
    If there is no umap file for the given name in the list, the file is created by reading the umap and uexp.
    '''
    def getFile(self,name):
        if name not in self.fileNames:
            self.readFile(name)

        index = self.fileNames.index(name)
        return self.files[index]

    '''
    Set the file of the given umap file name to the given umap file.
    '''
    def setFile(self,name,file):
        index = self.fileNames.index(name)
        self.files[index] = file

    '''
    Writes the umap and uexp for every file in the list to their respective folder.
    '''
    def writeFiles(self):
        for index, name in enumerate(self.fileNames):
            folderKey = name
            
            file = self.files[index]
            writeBinaryTable(file.uexp.buffer, UMAP_FOLDERS[folderKey] + '/' + name + '.uexp', UMAP_FOLDERS[folderKey])
            writeBinaryTable(file.uasset.binaryTable.buffer, UMAP_FOLDERS[folderKey] + '/' + name + '.umap', UMAP_FOLDERS[folderKey])
    
    '''
    Read the binary data of the files belonging to the umap of the given name and create a UMap_File and add it to the list.
    '''
    def readFile(self,name):
        uexp = readBinaryTable('base/Level/' + name + '.uexp')
        uassetData = UAsset(readBinaryTable('base/Level/' + name + '.umap'))
        self.fileNames.append(name)
        self.files.append((UMap_File(uassetData,uexp)))

class UMap_File:
    def __init__(self,uasset: UAsset, uexp: Table):
        self.uasset = uasset 
        self.uexp = uexp