from base_classes.uasset_custom import UAsset_Custom
from util.binary_table import readBinaryTable, writeBinaryTable, Table, writeFolder
import json
import os
import sys
from script_logic import getEquivalentSource
from pythonnet import load

base_path = os.path.join(os.getcwd(), r'base')

os.environ["PATH"] += os.pathsep + base_path
sys.path.append(base_path)

try:
    load("coreclr")
    print("CoreCLR loaded successfully")
except Exception as e:
    print("Failed to load CoreCLR:", str(e))
    print("No .net Installation found. Please install .net: https://dotnet.microsoft.com/en-us/download/dotnet/8.0")
    sys.exit(1)  # Exit if the runtime fails to load

import clr
try:
    clr.AddReference('UAssetAPI')
    clr.AddReference('System')
    print("UAssetAPI DLL loaded successfully")
except Exception as e:
    print("Failed to load UAssetAPI DLL:", str(e))
    sys.exit(1)  


from UAssetAPI import UAsset  # type: ignore
from UAssetAPI.UnrealTypes import EngineVersion, FString  # type: ignore
from System.Text import Encoding # type: ignore

LV_M061_FOLDER = 'rando/Project/Content/Level/Event/M061'
EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event'
SCRIPT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script' 
SUBMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission'
MAINMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission'
MAINMISSION_M061_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission_M061' 
M061_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061'
M062_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M062'
M060_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M060'  
M063_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M063'  
M064_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M064'
MAIN_M016_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M016' 
M016_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M016'
M035_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M035' 
M036_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M036'
M030_FOLDER =  'rando/Project/Content/Blueprints/Event/Script/SubMission/M030'
M050_FOLDER =  'rando/Project/Content/Blueprints/Event/Script/SubMission/M050'
SHOP_EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/ShopEvent'
M061_EM1640_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM1640'
M061_EM1710_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM1710'
GARDEN_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/Garden'
MINATO_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m061'
SHINAGAWA_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m062'
CHIYODA_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m063'
SHINJUKU_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m064'
TAITO_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m060'
TOKYO_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_TokyoMap'
EMPYREAN_NPC_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/esNPC_m016'
MAIN_M060_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M060'
MAIN_M064_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M064'

#List of which folder each script is in, due to sometimes not being obvious based on file name
SCRIPT_FOLDERS = {
    'MM_M061_EM1630': M061_FOLDER, # The Water Nymph 
    'MM_M061_EM1640': M061_FOLDER, # The Spirit of Love
    'MM_M062_EM1660': M062_FOLDER, # Holding The Line
    'MM_M062_EM1650': M062_FOLDER, #Those Seeking Sanctuary
    'MM_M060_EM1690': M060_FOLDER, # Raid on Tokyo
    'MM_M060_EM1700': M060_FOLDER, # In Defense of Tokyo
    'MM_M063_EM1670': M063_FOLDER, # Black Frost Strikes Back
    'MM_M063_EM1680': M063_FOLDER, # A Sobering Standoff
    'MM_M064_EM2310': M064_FOLDER, # Reclaim the Golden Stool 
    'MM_M064_EM2320': M064_FOLDER, # Liberate the Golden Stool
    'MM_M064_EM2270': M064_FOLDER, # The Vampire in Black
    'MM_M064_EM2280': M064_FOLDER, # The Hunter in White
    'MM_M060_EM1420': M060_FOLDER, # Fionn's Resolve
    'MM_M060_EM1602': M060_FOLDER, # The Destined Leader (Amanazako Could't Join Initially)
    'MM_M060_EM1601': M060_FOLDER, # The Destined Leader
    'MM_M016_E0885': MAIN_M016_FOLDER, #Hayataro CoC Chaos
    'MM_M016_E0885_Direct': MAIN_M016_FOLDER, #Hayataro CoC Chaos
    'MM_M016_EM1450': M016_FOLDER, # A Plot Revealed
    'MM_M035_EM1480': M035_FOLDER, # The Seraph's Return
    'MM_M036_EM1490': M036_FOLDER, # The Red Dragon's Invitation
    'MM_M061_EM1781': M030_FOLDER, # Rage of a Queen
    'MM_M030_EM1769': M030_FOLDER, # Bethel Researcher giving DLC Demons 
    'MM_M061_EM1791': M030_FOLDER, # A Goddess in Training
    'MM_M061_EM2613_HitAction': M030_FOLDER, # Holy Will and Profane Dissent
    'MM_M061_EM2601': M061_FOLDER, # Sakura Cinders of the East
    'MM_M063_EM2170': M063_FOLDER, # Guardian of Tokyo
    'MM_M061_EM1030': M061_FOLDER, # Cursed Mermaids
    'MM_M061_EM2050': M050_FOLDER, # Picture-Perfect Debut
    'MM_M060_EM1310': M060_FOLDER, # Downtown Rock 'n Roll
    'MM_M060_EM1370': M060_FOLDER, # Keeper of the North
    'MM_M061_EM1360': M061_FOLDER, # Keeper of the West
    'MM_M062_EM1340': M062_FOLDER, # Keeper of the South
    'MM_M063_EM1350': M063_FOLDER, # Keeper of the East
    'MM_M061_EM1715': M061_EM1710_FOLDER, # Movin' on Up
    'MM_M060_EM1460': M060_FOLDER, # Gold Dragon's Arrival
    'MM_M063_EM1592': M063_FOLDER, # A Power Beyond Control 
    'MM_M030_EM2600': M030_FOLDER, # Sakura Cinders of the East (Periapt Event)
    'MM_M030_EM2610': M030_FOLDER, # Holy Will and Profane Dissent (Periapt Event
    'MM_M060_EM2351': GARDEN_FOLDER, # Rascal of the Norse
    'EM_M061_DevilTalk' : MAINMISSION_M061_FOLDER, # Tutorial Pixie Event
    'esNPC_m061_31a' : MINATO_NPC_FOLDER, #Rakshasa on Diet Building Roof
    'esNPC_m061_30a' : MINATO_NPC_FOLDER, #Slime near Qing Long
    'esNPC_m061_34a' : MINATO_NPC_FOLDER, #Pixie in Kamiyacho
    'BP_esNPC_TokyoMap_15b': TOKYO_NPC_FOLDER, #Tokyo NPC Mischievous Mascot Periapt
    'esNPC_m062_32a': SHINAGAWA_NPC_FOLDER, #Nue in Container
    'esNPC_m062_33a': SHINAGAWA_NPC_FOLDER, #Angel after Loup-garou/Eisheth 
    'esNPC_m062_40a': SHINAGAWA_NPC_FOLDER, #Slime in Shinagawa
    'esNPC_m063_20a': CHIYODA_NPC_FOLDER, #Yurlungur NPC
    'esNPC_m063_21a': CHIYODA_NPC_FOLDER, #Setanta NPC
    'esNPC_m060_10a': TAITO_NPC_FOLDER, #Orthrus NPC
    'esNPC_m016_02a': EMPYREAN_NPC_FOLDER, #Ongyo-Ki NPC
    'MM_M062_EM1132': M062_FOLDER, #Cait Sith in Fairy Village
    'MM_M060_EM1370_Direct': M060_FOLDER, #Fighting Bishamonten without Quest(shares reward with quest)
    'MM_M061_E2610': MAINMISSION_M061_FOLDER, #Isis Event in CoV
    'MM_M060_E0763': MAIN_M060_FOLDER, #Tao Talisman Event at the beginning of Taito
    'MM_M064_E2797': MAIN_M064_FOLDER, #Qadistu Talisman/Periapt
    'MM_M064_E2795_Direct': MAIN_M064_FOLDER, #Tsukuyomi Talisman
    'BP_JakyoEvent': SHOP_EVENT_FOLDER, #Cathedral of Shadows Event
    'MM_M061_EM0020': M061_FOLDER, # The Angel's Request
    'BP_ShopEvent': SHOP_EVENT_FOLDER, #First Miman Reward
    'MM_M061_EM1631': M061_FOLDER, # # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640_Hit': M061_EM1640_FOLDER # The Spirit of Love First Entry (Apsaras)
}

#List of which folder each umap should be in when writing output
UMAP_FOLDERS = {
    'LV_EventMission_M061': LV_M061_FOLDER,
    'LV_MainMission_M061': LV_M061_FOLDER,
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
            
            writeFolder(UMAP_FOLDERS[folderKey])

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
        assetobject = UAsset('base/Level/' +  name+ '.umap', EngineVersion.VER_UE4_27)

        jsonstring = assetobject.SerializeJson()
        jsonobject = json.loads(jsonstring)
        self.fileNames.append(name)
        self.files.append(UMap_File(assetobject,jsonobject))
        

class UMap_File:
    def __init__(self,uasset: UAsset, jsonForm=None):
        self.uasset = uasset 
        if jsonForm:
            self.json = jsonForm
        else:
            jsonstring = self.uasset.SerializeJson()
            self.json = json.loads(jsonstring)

class Script_File_List:
    def __init__(self):
        self.files = []
        self.fileNames = []
        self.nameCorrections = {}

    '''
    Returns a script_file for the given script name. 
    If there is no script_file for the given name in the list, the file is created by reading the uasset and uexp.
    '''
    def getFile(self,name):
        if name not in self.fileNames:
            self.readFile(name)

        index = self.fileNames.index(name)
        return self.files[index]

    '''
    Set the file of the given script name to the given script_file.
    '''
    def setFile(self,name,file):
        index = self.fileNames.index(name)
        self.files[index] = file

    '''
    Writes the uasset and uexp for every file in the list to their respective folder.
    '''
    def writeFiles(self):
        for index, name in enumerate(self.fileNames):
            folderKey = name
            if folderKey not in SCRIPT_FOLDERS.keys():
                folderKey = getEquivalentSource(name)
            
            file = self.files[index]
            stringy = json.dumps(file.json)

            writeFolder(SCRIPT_FOLDERS[folderKey])
            
            file.uasset = file.uasset.DeserializeJson(stringy)
            file.uasset.Write(SCRIPT_FOLDERS[folderKey] + '/' + name + '.uasset')
            
            #writeBinaryTable(file.uexp.buffer, SCRIPT_FOLDERS[folderKey] + '/' + name + '.uexp', SCRIPT_FOLDERS[folderKey])
            #writeBinaryTable(file.uasset.binaryTable.buffer, SCRIPT_FOLDERS[folderKey] + '/' + name + '.uasset', SCRIPT_FOLDERS[folderKey])
    
    '''
    Read the file belonging to the script of the given name and create a Script_File and add it to the list.
    '''
    def readFile(self,name):
        if 'NPC' in name:
            scriptPath = 'NPC/'
        elif 'ShopEvent' in name or 'JakyoEvent' in name:
            scriptPath = 'ShopEvent/'
        elif 'EM' in name and not 'DevilTalk' in name:
            scriptPath = 'SubMission/'
        else:
            scriptPath = 'MainMission/'
        #uexp = readBinaryTable('base/Scripts/' + scriptPath + name + '.uexp')
        #uassetData = Script_Uasset(readBinaryTable('base/Scripts/' +scriptPath + name + '.uasset'))
        assetobject = UAsset('base/Scripts/' + scriptPath + name + '.uasset', EngineVersion.VER_UE4_27)

        jsonstring = assetobject.SerializeJson()
        jsonobject = json.loads(jsonstring)
        
        self.fileNames.append(name)
        self.files.append((Script_File(assetobject,jsonobject)))

class Script_File:
    def __init__(self,uasset: UAsset, json):
        self.uasset = uasset 
        self.json = json
    
    '''
    Get the name at the index in the name map of the uasset.
    '''
    def getNameAtIndex(self,index):
        string = self.uasset.GetNameReference(index).ToString()
        return string

    '''
    Set the value of the entry in the nameMap at the index to the given name.
    '''
    def setNameAtIndex(self,index,name):
        encoding = None
        try:
            name.encode('ascii')
            encoding = Encoding.ASCII
        except UnicodeEncodeError:
            encoding = Encoding.Unicode
        self.uasset.SetNameReference(index,FString.FromString(name,encoding))    
    
    '''
    Returns a new JSON based on the current uasset data.
    '''
    def updateJsonWithUasset(self):
        jsonstring = self.uasset.SerializeJson()
        self.json = json.loads(jsonstring)
        return self.json
    
    '''
    Updates the uasset data with the given json and replaces the current json object based on the new uasset.
    '''
    def updateFileWithJson(self, jsonData):
        stringy = json.dumps(jsonData)
        self.uasset = self.uasset.DeserializeJson(stringy)
        jsonstring = self.uasset.SerializeJson()
        self.json = json.loads(jsonstring)

