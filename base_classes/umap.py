from base_classes.uasset import UAsset_Custom
from util.binary_table import readBinaryTable, writeBinaryTable, Table
import json
import os
import sys
from pythonnet import load

base_path = os.path.join(os.getcwd(), r'base')

os.environ["PATH"] += os.pathsep + base_path
sys.path.append(base_path)

runtime_config_path = os.path.join(base_path, 'UAssetAPI.runtimeconfig.json')

coreclrpath = os.path.join(base_path, 'coreclr.dll')

try:
    load("coreclr")
    print("CoreCLR loaded successfully")
except Exception as e:
    print("Failed to load CoreCLR:", str(e))
    sys.exit(1)  # Exit if the runtime fails to load

import clr
try:
    clr.AddReference('UAssetAPI')
    print("UAssetAPI DLL loaded successfully")
except Exception as e:
    print("Failed to load UAssetAPI DLL:", str(e))
    sys.exit(1)  


from UAssetAPI import UAsset  # type: ignore
from UAssetAPI.UnrealTypes import EngineVersion  # type: ignore

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
            stringy = json.dumps(file.json)
            
            file.uasset = file.uasset.DeserializeJson(stringy)
            file.uasset.Write(UMAP_FOLDERS[folderKey] + '/' + name + '.umap')
            #writeBinaryTable(file.uexp.buffer, UMAP_FOLDERS[folderKey] + '/' + name + '.uexp', UMAP_FOLDERS[folderKey])
            #writeBinaryTable(file.uasset.binaryTable.buffer, UMAP_FOLDERS[folderKey] + '/' + name + '.umap', UMAP_FOLDERS[folderKey])
    
    '''
    Read the binary data of the files belonging to the umap of the given name and create a UMap_File and add it to the list.
    '''
    def readFile(self,name):
        # uexp = readBinaryTable('base/Level/' + name + '.uexp')
        # uassetData = UAsset_Custom(readBinaryTable('base/Level/' + name + '.umap'))
        my_asset = UAsset('base/Level/' +  name+ '.umap', EngineVersion.VER_UE4_27)

        # Step 2: Serialize the asset to JSON
        json_serialized_asset = my_asset.SerializeJson()
        json_object = json.loads(json_serialized_asset)
        self.fileNames.append(name)
        self.files.append(UMap_File(my_asset,json_object))
        

class UMap_File:
    def __init__(self,uasset: UAsset, joson):
        self.uasset = uasset 
        self.json = joson