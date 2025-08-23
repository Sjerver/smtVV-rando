from base_classes.uasset_custom import UAsset_Custom
from util.binary_table import readBinaryTable, writeBinaryTable, Table, writeFolder
import json
import os
import sys
import copy
from pythonnet import load

base_path = os.path.join(os.getcwd(), r'base')

os.environ["PATH"] += os.pathsep + base_path
sys.path.append(base_path)

try:
    load("coreclr")
    print("CoreCLR loaded successfully")
except Exception as e:
    print("Failed to load CoreCLR:", str(e))
    print("No .net Installation found. Please install .net 8.0 SDK : https://dotnet.microsoft.com/en-us/download/dotnet/8.0")
    input('Press [Enter] to exit')
    sys.exit(1)  # Exit if the runtime fails to load

import clr
try:
    clr.AddReference('UAssetAPI')
    clr.AddReference('System')
    print("UAssetAPI DLL loaded successfully")
except Exception as e:
    
    print("Failed to load UAssetAPI DLL:", str(e))
    print("You might have not extracted the base folder to the same directory as the randomizer.exe")
    input('Press [Enter] to exit')
    sys.exit(1)  


from UAssetAPI import UAsset, Import # type: ignore
from UAssetAPI.UnrealTypes import EngineVersion, FString  # type: ignore
from UAssetAPI.Kismet import KismetSerializer #type:ignore
from System.Text import Encoding # type: ignore

BTL_AI_FOLDER = 'rando/Project/Content/Blueprints/Battle/Logic/AI/Enemy'
LV_M061_FOLDER = 'rando/Project/Content/Level/Event/M061'
EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event'
SCRIPT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script' 
SUBMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission'
MAINMISSION_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission'
MAINMISSION_M061_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission_M061' 
M061_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061'
M061_EM0150_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM0150'
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
M050_EM2410_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M050/EM2410'
SHOP_EVENT_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/ShopEvent'
M061_EM1640_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM1640'
M061_EM1710_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM1710'
M061_EM2020_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM2020'
M061_EM2030_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM2030'
M061_EM2040_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM2040'
M061_EM2240_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM2240'
M061_EM2380_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M061/EM2380'
M062_EM1650_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M062/EM1650'
M062_EM2110_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M062/EM2110'
M062_EM2430_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M062/EM2430'
M062_EM2440_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M062/EM2440'
M063_EM2390_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M063/EM2390'
M064_EM2300_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M064/EM2300'
M064_EM2360_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M064/EM2360'
M064_EM2620_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M064/EM2620'
M060_EM2480_FODLER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M060/EM2480'
M060_EM2700_FODLER = 'rando/Project/Content/Blueprints/Event/Script/SubMission/M060/EM2700'
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
MAIN_M035_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M035'
MAIN_M036_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M036'
MAIN_M038_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M038'
MAIN_M062_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M062'
M062_PLEIADES_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M062/Pleiades' 
MAIN_M063_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M063'
MAIN_M080_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M080'
MAIN_M082_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M082'
MAIN_M083_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M083'
MAIN_M085_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M085'
MAIN_M087_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M087'
MAIN_M088_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M088'
MAIN_M092_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M092'
MAIN_M115_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M115'
MAIN_M203_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/MainMission/M203'
DESIGN_EVENT_FOLDER = 'rando/Project/Content/Design/Event/'
ES035_M063_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/es035_m063'
ES152_M062_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/es152_m062'
ES152_M063_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/es152_m063'
ES618_M063_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/es618_m063'
ES618_M060_FOLDER = 'rando/Project/Content/Blueprints/Event/Script/es618_m060'
PLAYER_038_FOLDER = 'rando/Project/Content/Blueprints/Character/Player/Pla038'
PLAYER_059_FOLDER = 'rando/Project/Content/Blueprints/Character/Player/Pla059'
PLAYER_060_FOLDER = 'rando/Project/Content/Blueprints/Character/Player/Pla060'
PLAYER_128_FOLDER = 'rando/Project/Content/Blueprints/Character/Player/Pla128'
PLAYER_289_FOLDER = 'rando/Project/Content/Blueprints/Character/Player/Pla289'
PLAYER_355_FOLDER = 'rando/Project/Content/Blueprints/Character/Player/Pla355'

#List of which folder each script is in, due to sometimes not being obvious based on file name
SCRIPT_FOLDERS = {
    'Btl_AI': BTL_AI_FOLDER,
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
    'MM_M061_EM2705': M060_EM2700_FODLER, #Guardian of Light
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
    'esNPC_m061b_31a' : MINATO_NPC_FOLDER, #Rakshasa on Diet Building Roof (Vengeance)
    'esNPC_m061_30a' : MINATO_NPC_FOLDER, #Slime near Qing Long
    'esNPC_m061b_30a' : MINATO_NPC_FOLDER, #Slime near Qing Long (Vengeance)
    'esNPC_m061_34a' : MINATO_NPC_FOLDER, #Pixie in Kamiyacho
    'esNPC_m061_32_Navi': MINATO_NPC_FOLDER, #Navi Ippon Datara
    'esNPC_m061_33_Navi': MINATO_NPC_FOLDER, #Navi Mermaid
    'esNPC_m061_37_Navi': MINATO_NPC_FOLDER, #Navi Hell Biker
    'esNPC_m061_38_Navi': MINATO_NPC_FOLDER, #Navi Cleopatra
    'BP_esNPC_TokyoMap_15b': TOKYO_NPC_FOLDER, #Tokyo NPC Mischievous Mascot Periapt
    'BP_esNPC_TokyoMap_15b2': TOKYO_NPC_FOLDER, #Tokyo NPC Mischievous Mascot Periapt
    'BP_esNPC_TokyoMap_15c': TOKYO_NPC_FOLDER, #Tokyo NPC Mischievous Mascot Periapt
    'esNPC_m062_32a': SHINAGAWA_NPC_FOLDER, #Nue in Container
    'esNPC_m062_33a': SHINAGAWA_NPC_FOLDER, #Angel after Loup-garou/Eisheth
    'esNPC_m062b_32a': SHINAGAWA_NPC_FOLDER, #Nue in Container (Vengeance)
    'esNPC_m062b_33a': SHINAGAWA_NPC_FOLDER, #Angel after Loup-garou/Eisheth  (Vengeance)
    'esNPC_m062_40a': SHINAGAWA_NPC_FOLDER, #Slime in Shinagawa
    'esNPC_m062_NaviDevil_01': SHINAGAWA_NPC_FOLDER, #Navi Agathion
    'esNPC_m062_NaviDevil_41': SHINAGAWA_NPC_FOLDER, #Navi Mothman
    'esNPC_m062_NaviDevil_42': SHINAGAWA_NPC_FOLDER, #Navi Idun
    'esNPC_m063_20a': CHIYODA_NPC_FOLDER, #Yurlungur NPC
    'esNPC_m063_21a': CHIYODA_NPC_FOLDER, #Setanta NPC
    'esNPC_m064_NaviDevil_01': SHINJUKU_NPC_FOLDER, #Navi Sukuna Hikona
    'esNPC_m060_10a': TAITO_NPC_FOLDER, #Orthrus NPC
    'esNPC_m060_08_Navi': TAITO_NPC_FOLDER, #Navi Bugs
    'esNPC_m060_14_Navi': TAITO_NPC_FOLDER, #Navi Mara
    'esNPC_m060_15_Navi': TAITO_NPC_FOLDER, #Navi Fionn
    'esNPC_m016_02a': EMPYREAN_NPC_FOLDER, #Ongyo-Ki NPC
    'esNPC_m016_02b': EMPYREAN_NPC_FOLDER, #Ongyo-Ki NPC
    'MM_M062_EM1132': M062_FOLDER, #Cait Sith in Fairy Village
    'MM_M060_EM1370_Direct': M060_FOLDER, #Fighting Bishamonten without Quest(shares reward with quest)
    'MM_M061_E2610': MAINMISSION_M061_FOLDER, #Isis Event in CoV
    'MM_M060_E0763': MAIN_M060_FOLDER, #Tao Talisman Event at the beginning of Taito
    'MM_M060_E3001_Direct': MAIN_M060_FOLDER, #Tao Talisman Event at the beginning of Taito (Vengeance)
    'MM_M064_E2797': MAIN_M064_FOLDER, #Qadistu Talisman/Periapt
    'MM_M064_E2795_Direct': MAIN_M064_FOLDER, #Tsukuyomi Talisman
    'BP_JakyoEvent': SHOP_EVENT_FOLDER, #Cathedral of Shadows Event
    'MM_M061_EM0020': M061_FOLDER, # The Angel's Request
    'BP_ShopEvent': SHOP_EVENT_FOLDER, #First Miman Reward
    'MM_M061_EM1631': M061_FOLDER, # # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640_Hit': M061_EM1640_FOLDER, # The Spirit of Love First Entry (Apsaras)
    'MM_M061_E2620': MAINMISSION_M061_FOLDER, #CoV Khonsu Event Bethel Egypt
    'MM_M061_E2625_Direct': MAINMISSION_M061_FOLDER, #CoV Khonsu Event Post Fight Bethel Egypt
    'MM_M061_EM0181': MAINMISSION_M061_FOLDER, #Amanozako gives you a bead
    'MM_M061_EM0182': MAINMISSION_M061_FOLDER, #Amanozako becomes your navigator
    'MM_M061_EM0026': MAINMISSION_M061_FOLDER, #Amanozako congratulating you after hydra defeat
    'EM_M061_Q0019': MAINMISSION_M061_FOLDER, #Amanozako leaves in area 1
    'EM_M061_TutorialNavi02': MAINMISSION_M061_FOLDER, #Amanazako first partner spot
    'EM_M061_MimanTutorial_Stop': MAINMISSION_M061_FOLDER, #Barrier stopping player for Miman Tutorial
    'MM_M016_E0891': MAIN_M016_FOLDER, #Empyrean Melchizedek
    'MM_M016_E0892': MAIN_M016_FOLDER, #Empyrean Sraosha
    'MM_M016_E0893': MAIN_M016_FOLDER, #Empyrean Alilat
    'MM_M035_E0825': MAIN_M035_FOLDER, #Temple of Eternity Metatron
    'MM_M036_E0644': MAIN_M036_FOLDER, #DKC Chernobog
    'MM_M036_E0650': MAIN_M036_FOLDER, #DKC Abdiel
    'MM_M036_E0670': MAIN_M036_FOLDER, #DKC Yakumo Arioch
    'MM_M038_E2912': MAIN_M038_FOLDER, #Shakan Dark Block Bros
    'MM_M038_E2917': MAIN_M038_FOLDER,#Shakan Cherub
    'MM_M038_E2930_Direct': MAIN_M038_FOLDER,#Shakan Abdiel
    'MM_M060_E0762': MAIN_M060_FOLDER, #Nuwa in area 4 at the gate
    'MM_M060_E0778': MAIN_M060_FOLDER, #Vasuki Fight Event?
    'MM_M060_E0785': MAIN_M060_FOLDER, #CoC Taito Zeus Appears
    'MM_M060_E0790': MAIN_M060_FOLDER, #CoC Taito Zeus PostFight?
    'MM_M060_E0810': MAIN_M060_FOLDER, #CoC Odin PostFight?
    'MM_M060_E3010': MAIN_M060_FOLDER, #Yakumo in area 4 vengeance
    'MM_M060_E3020': MAIN_M060_FOLDER, #Yakumo in area 4 vengeance part 2
    'MM_M060_E3110_Direct': MAIN_M060_FOLDER, #CoV Beelzebub
    'MM_M060_E3130_Direct': MAIN_M060_FOLDER, #CoV Zeus + Odin
    'MM_M060_Npc609Talk': MAIN_M060_FOLDER, #CoC Yuzuru Hayataro NPC Event?
    'MM_M060_EM0140': MAIN_M060_FOLDER, #Amanozako rejoins in area 4 creation
    'MM_M062_EM0050': MAIN_M062_FOLDER, # Golden Apple Quest part 1
    'MM_M062_EM0051': MAIN_M062_FOLDER, # Idun in Golden Apple Quest
    'MM_M062_E0378': MAIN_M062_FOLDER, #Dazai/Abdiel talk in area 2 creation (Abdiel)
    'MM_M062_E0380': MAIN_M062_FOLDER, #Fionn 1 Post-fight (Fionn)
    'MM_M062_E0492': MAIN_M062_FOLDER,#Final Lahmu (Lahmu Phase 2)
    'MM_M062_EM0041': MAIN_M062_FOLDER, #Loup-garous Event
    'MM_M062_EM0120_Direct': MAIN_M062_FOLDER, #Amanozako rejoins in area 2
    'MM_M062_EM0122': MAIN_M062_FOLDER, #Amanozako car event
    'MM_M062_EM0123': MAIN_M062_FOLDER, #Amanozako railroad event
    'MM_M062_EM0124': MAIN_M062_FOLDER, #Amanozako container event
    'MM_M062_EM0125': MAIN_M062_FOLDER, #Amanozako leaves in area 2
    'MM_M062_E2275': M062_PLEIADES_FOLDER, #Dazai/Abdiel talk in area 2 vengeance
    'MM_M062_E2295_Direct': M062_PLEIADES_FOLDER, #Eisheth pre-fight
    'MM_M062_E2298_Direct': M062_PLEIADES_FOLDER, #Fionn post-fight Vengeance
    'MM_M062_E2300': M062_PLEIADES_FOLDER,  #Dazai Pre-Blocker Vengeance
    'MM_M062_E2302': M062_PLEIADES_FOLDER, #Arriving in fairy village vengeance
    'MM_M062_E2305': M062_PLEIADES_FOLDER, #Golden Apple Quest start vengeance
    'MM_M062_E2305_2': M062_PLEIADES_FOLDER, #Golden Apple Quest Idun part vengeance
    'MM_M062_E2326_Direct': M062_PLEIADES_FOLDER, #Dialogue when fairy village is salted
    'MM_M063_E0625': MAIN_M063_FOLDER, #Yakumo post-fight Chiyoda 
    'MM_M063_EM0061': MAIN_M063_FOLDER, #Hellfire Highway Shrine Event
    'MM_M063_EM0070': MAIN_M063_FOLDER, #Decarabia in Ishtar Quest
    'MM_M063_EM0079': MAIN_M063_FOLDER, #Ishtar Post Fight
    'MM_M063_EM0130': MAIN_M063_FOLDER, #Amanozako in Chiyoda
    'MM_M063_M0680': MAIN_M063_FOLDER, #Abdiel celebrates Arioch's death
    'MM_M064_E2510_Direct': MAIN_M064_FOLDER, #First Power Fight in Shinjuku
    'MM_M064_E2512': MAIN_M064_FOLDER, #Second Power Fight in Shinjuku
    'MM_M064_E2514': MAIN_M064_FOLDER, #Powers detecting other intruders (uses Triple Power Fight Replacement)
    'MM_M064_E2520_Direct': MAIN_M064_FOLDER, #First Nuwa/Yakumo scene in Shinjuku 
    'MM_M064_E2540': MAIN_M064_FOLDER, #Power Gauntlet (uses last Power Fight Replacement)
    'MM_M064_E2550': MAIN_M064_FOLDER, #Cherub Blocker in Shinjuku (?)
    'MM_M064_E2560': MAIN_M064_FOLDER, #Nuwa/Yakumo talk at Mastema's hill
    'MM_M064_E2562_Direct': MAIN_M064_FOLDER, #Nuwa/Yakumo talk at Mastema's hill 2 
    'MM_M064_E2638': MAIN_M064_FOLDER, #Dazai joins to see Mastema 2 (?)
    'MM_M064_E2642_Direct': MAIN_M064_FOLDER, #Meeting Mastema (Dazai,Mastema)
    'MM_M064_E2644_Direct': MAIN_M064_FOLDER, #Dazai got salted (Dazai,Mastema)
    'MM_M064_E2647': MAIN_M064_FOLDER, #Amanozako in Shinjuku
    'MM_M064_E2650_Direct': MAIN_M064_FOLDER, #Nuwa/Yakumo talk after seeing Naamah (Nuwa, Yakumo)
    'MM_M064_E2690': MAIN_M064_FOLDER, #Dead Cherubim 
    'MM_M064_E2900': MAIN_M064_FOLDER,#Mastema sends you to Shakan
    'MM_M064_E2950_Direct': MAIN_M064_FOLDER,#Mastema after Shakan
    'MM_M080_E2670_Direct': MAIN_M080_FOLDER,#Yuzuru wants to be a Nahobino
    'MM_M082_E3030_Direct': MAIN_M082_FOLDER,#Yakumo saves a student
    'MM_M083_E2160_Direct': MAIN_M083_FOLDER,#Labolas 2 post-fight 
    'MM_M085_E0690': MAIN_M085_FOLDER, #Koshimizu meeting after area 3 CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E0730': MAIN_M085_FOLDER, #Regarding the war of the gods scene CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E0730_ready': MAIN_M085_FOLDER, #End of Regarding the war of the gods scene CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E2420': MAIN_M085_FOLDER,#Yuzuru apologizes for attacking you (Yuzuru)
    'MM_M085_E2445': MAIN_M085_FOLDER,#Koshimizu meeting after salt investigation (Hayataro)
    'MM_M085_E2575_Direct': MAIN_M085_FOLDER, #Dazai talk when Miyazu goes to Khonsu (Dazai)
    'MM_M085_E2630_Direct': MAIN_M085_FOLDER,#Yuzuru talk after Khonsu incident (Yuzuru, Dazai)
    'MM_M085_E2635_Direct': MAIN_M085_FOLDER, #Dazai joins to see Mastema 1 
    'MM_M085_E2660': MAIN_M085_FOLDER, #Koshimizu meeting before Yakumo fight(Yuzuru)
    'MM_M085_E2688': MAIN_M085_FOLDER, #Koshimizu meeting after Yakumo fight (Yuzuru)
    'MM_M087_E2450_Direct': MAIN_M087_FOLDER, #Dazai goes to Chiyoda
    'MM_M088_E0602_Abdiel': MAIN_M088_FOLDER, #Summmit (Abdiel)
    'MM_M088_E0602_Khons': MAIN_M088_FOLDER, #Summmit (Khonsu)
    'MM_M088_E0602_Koshimizu': MAIN_M088_FOLDER, #Summmit (Koshimizu as Tsukuyomi Replacement)
    'MM_M088_E0602_Vasuki': MAIN_M088_FOLDER, #Summmit (Vasuki)
    'MM_M088_E0602_Odin': MAIN_M088_FOLDER, #Summmit (Odin)
    'MM_M088_E0602_Zeus': MAIN_M088_FOLDER, #Summmit (Zeus)
    'MM_M092_EM101_': MAIN_M092_FOLDER, #School Oni [63]
    'MM_M092_EM102_': MAIN_M092_FOLDER, #School Andras + Rakshasa [56]
    'MM_M092_EM104': MAIN_M092_FOLDER, #School Incubus [58]
    'MM_M092_EM105_1': MAIN_M092_FOLDER, #School Tsuchigumo [62]
    'MM_M092_EM106_': MAIN_M092_FOLDER, #School Manananggal +Shiki Ouji [66]
    'MM_M092_EM107_': MAIN_M092_FOLDER, #School Rakshasa + Incubus [57]
    'MM_M092_EM108_': MAIN_M092_FOLDER, #School Rakshasa [59]
    'MM_M092_EM109_a': MAIN_M092_FOLDER, #School Save Jack Frost (Manananggal) [64]
    'MM_M092_EM110': MAIN_M092_FOLDER, #School Incubus (Aitvaras is normal Leader for this one) [61]
    'MM_M092_EM111': MAIN_M092_FOLDER, #School Aitvaras + Shiki Ouji [61][65]
    'MM_M092_EM112_': MAIN_M092_FOLDER, #School Optional Multiple Fights [65][129][60] (Manananggal,Shiki Ouji,Andras)
    'MM_M115_E2603_Direct': MAIN_M115_FOLDER, #Dazai/Yuzuru in dorm room
    'MM_M203_E2718_Direct': MAIN_M203_FOLDER, #Lilith post-fight lecture
    'MM_M016_EM1500': M016_FOLDER, #Seed of Life Quest
    'MM_M016_EM1531': M016_FOLDER, #A Universe in Peril
    'MM_M060_EM1819': M030_FOLDER, # Mother Harlot Fiend Fight
    'MM_M060_EM1819_NewRoute': M030_FOLDER, # Mother Harlot Fiend Fight
    'MM_M060_EM1821': M030_FOLDER, # Trumpeter Fiend Fight
    'MM_M060_EM1821_NewRoute': M030_FOLDER,# Trumpeter Fiend Fight
    'MM_M061_EM1771': M030_FOLDER,#Mephisto Quest
    'MM_M061_EM1782': M030_FOLDER,#Cleopatra Quest (Cleopatra) Couldn't join due to full party
    'MM_M061_EM1791': M030_FOLDER, #Artemis Quest
    'MM_M061_EM1802': M030_FOLDER, # Matador Fiend Fight
    'MM_M061_EM1802_NewRoute': M030_FOLDER, # Matador Fiend Fight
    'MM_M061_EM2611': M030_FOLDER, # Dagda Quest Danu Event
    'MM_M061_EM2613_HitAction': M030_FOLDER,  #Dagda Quest
    'MM_M062_EM1804': M030_FOLDER, #Daisoujou Fiend Fight
    'MM_M062_EM1804_NewRoute': M030_FOLDER, #Daisoujou Fiend Fight
    'MM_M062_EM1806': M030_FOLDER,  #Hell Biker Fiend Fight
    'MM_M062_EM1806_NewRoute': M030_FOLDER,  #Hell Biker Fiend Fight
    'MM_M063_EM1809': M030_FOLDER, #Inital Rider Meeting Chiyoda
    'MM_M063_EM1810': M030_FOLDER,  #White Rider Fight Chiyoda
    'MM_M063_EM1812': M030_FOLDER,  #Red Rider Fight Chiyoda
    'MM_M063_EM1814': M030_FOLDER,  #Black Rider Fight Chiyoda
    'MM_M063_EM1816': M030_FOLDER,  #Pale Rider Fight Chiyoda
    'MM_M064_EM1809': M030_FOLDER, #Inital Rider Meeting Shinjuku
    'MM_M064_EM1810': M030_FOLDER,  #White Rider Fight Shinjuku
    'MM_M064_EM1812': M030_FOLDER,  #Red Rider Fight Shinjuku
    'MM_M064_EM1814': M030_FOLDER,  #Black Rider Fight Shinjuku
    'MM_M064_EM1816': M030_FOLDER,  #Pale Rider Fight Shinjuku
    'MM_M107_EM1824': M030_FOLDER,  #Demi-Fiend
    'MM_M107_EM1825_Dev651': M030_FOLDER,  #Demi-Fiend (Post Fight)
    'MM_M107_EM1825_Direct': M030_FOLDER,  #Demi-Fiend (End of Fight)
    'MM_M107_EM1825_Hit': M030_FOLDER,  #Demi-Fiend (Fight/Join Prompt)
    'MM_M036_EM1481': M036_FOLDER, # The Seraph's Return
    'MM_M035_EM1491': M035_FOLDER, # The Red Dragon's Invitation
    'MM_M201_EM2411': M050_EM2410_FOLDER, # Turbo Granny Quest
    'MM_M061_EM0021': M061_FOLDER, # Eligor and Andras Event
    'MM_M061_EM1020': M061_FOLDER, # The Ultimate Omelet
    'MM_M061_EM1031': M061_FOLDER,  #Pazuzu Event Mermaid Quest
    'MM_M061_EM1041': M061_FOLDER, #Anahita Event Mermaid Quest 2
    'MM_M061_EM1050_New': M061_FOLDER, #Talisman Hunt (Shiki Ouji)
    'MM_M061_EM2190': M061_FOLDER, #Halphas Quest(Oni)
    'MM_M061_EM2531': M061_FOLDER,  #Dormarth Quest (Dormarth)
    'MM_M061_EM1383': M061_FOLDER,  #Seth Event Battle Dialogue
    'esNPC_em0150_02': M061_EM0150_FOLDER, # A Preta Predicament (Preta) 
    'esNPC_em0150_03': M061_EM0150_FOLDER, # A Preta Predicament (Preta) 
    'esNPC_em0150_04': M061_EM0150_FOLDER, # A Preta Predicament (Preta)
    'esNPC_em0150_05': M061_EM0150_FOLDER, # A Preta Predicament (Preta)
    'esNPC_em0150_06': M061_EM0150_FOLDER, # A Preta Predicament (Preta) 
    'MM_M061_EM0151': M061_EM0150_FOLDER, # A Preta Predicament (Preta)
    'MM_M061_EM0152': M061_EM0150_FOLDER, # A Preta Predicament (Preta)
    'MM_M061_EM0154': M061_EM0150_FOLDER, # A Preta Predicament (Preta)
    'MM_M061_EM1710': M061_EM1710_FOLDER, # Movin' on Up
    'MM_M061_EM2020': M061_EM2020_FOLDER, # Nozuchi Quest
    'MM_M061_EM2030': M061_EM2030_FOLDER, #Brawny Ambitions
    'MM_M201_EM2040': M061_EM2040_FOLDER, #Pisaca Quest
    'MM_M061_EM2240': M061_EM2240_FOLDER, #CoV Khonsu Ra Quest
    'MM_M061_EM2242': M061_EM2240_FOLDER, #CoV Khonsu Ra Quest
    'MM_M061_EM2245': M061_EM2240_FOLDER, #CoV Khonsu Ra Quest
    'MM_M061_EM2380': M061_EM2380_FOLDER, #Mo Shuvuu Quest (Andras)
    'MM_M061_EM2382': M061_EM2380_FOLDER, #Mo Shuvuu Quest part 3
    'MM_M061_EM2383': M061_EM2380_FOLDER, #Mo Shuvuu Quest part 4
    'MM_M062_EM1141': M062_FOLDER, #Kumbhanda Bottle Quest
    'MM_M062_EM1150': M062_FOLDER, #A Goddess Stolen part 1
    'MM_M062_EM1151_Hit': M062_FOLDER, #A Goddess Stolen
    'MM_M062_EM1160': M062_FOLDER, #The Tyrant of Tennozu (Demeter)
    'MM_M062_EM1161_A': M062_FOLDER, #The Tyrant of Tennozu  (Belphegor)
    'MM_M062_EM1181': M062_FOLDER, #King Frost Quest (King Frost)
    'MM_M062_EM1331': M062_FOLDER, #Lord's Sword Quest (Arahabaki)
    'MM_M062_EM1401': M062_FOLDER, #Khonsu Ra CoC Quest (Khonsu Ra, Khonsu)
    'MM_M062_EM1402': M062_FOLDER, #Khonsu Ra CoC Quest (Khonsu Ra, Khonsu)
    'MM_M062_EM2040': M062_FOLDER, #Pisaca Quest part 1 (Anahita)
    'MM_M062_EM2090': M062_FOLDER, #Yuzuru Supply Run Quest (Yuzuru, Hayataro)
    'MM_M062_EM2490': M062_FOLDER, #Brawny Ambitions II (Xiezhai)
    'esNPC_em1650_01': M062_EM1650_FOLDER,  # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_02': M062_EM1650_FOLDER,  # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_03': M062_EM1650_FOLDER,  # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_04': M062_EM1650_FOLDER,  # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_05': M062_EM1650_FOLDER,  # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_06': M062_EM1650_FOLDER,  # Lilim/Principality Quest NPCs (Lilim) 
    'MM_M062_EM2110_Enemy': M062_EM2110_FOLDER, #Vouivre Quest (Vouivre) 
    'MM_M062_EM2430': M062_EM2430_FOLDER, #Pixie on the Case
    'MM_M062_EM2432': M062_EM2430_FOLDER, #Pixie on the Case npc Pixies
    'MM_M062_EM2440': M062_EM2440_FOLDER, #Amanozako Control Quest(Yakshini)
    'MM_M062_EM2441': M062_EM2440_FOLDER, #Amanozako Control Quest part 2
    'MM_M062_EM2442': M062_EM2440_FOLDER, #Amanozako Control Quest part 3
    'MM_M062_EM2443': M062_EM2440_FOLDER, #Amanozako Control Quest part 4
    'MM_M062_EM2444': M062_EM2440_FOLDER, #Amanozako Control Quest part 5
    'MM_M062_EM2446': M062_EM2440_FOLDER, #Amanozako Control Quest part 7
    'MM_M063_EM1210': M063_FOLDER, #Oyamatsumi Quest (Take-Minakata,Oyamatsumi)
    'MM_M063_EM1211': M063_FOLDER, #Oyamatsumi Quest (Oyamatsumi)
    'MM_M063_EM1230_HitAAction': M063_FOLDER, #Hua Po Quest start
    'MM_M063_EM1231': M063_FOLDER, #Hua Po Quest end
    'MM_M063_EM1241_Navi': M063_FOLDER, #Chiyoda Gem Quest
    'MM_M063_EM1250': M063_FOLDER,#Kunitsukami Fight Quest (Okuninushi)
    'MM_M063_EM1251': M063_FOLDER,#Kunitsukami Fight Quest (Sukuna Hikona)
    'MM_M063_EM1260': M063_FOLDER, #Demeter Defeat Chimera (Demeter)
    'MM_M063_EM1281': M063_FOLDER, #The Archangel of Destruction (Camael)
    'MM_M063_EM1291': M063_FOLDER, #Roar of Hatred (Moloch)
    'MM_M063_EM1592': M063_FOLDER, #Berserk Amanozako Quest (Amanozako Runaway)
    'MM_M063_EM2170': M063_FOLDER, #Masakado Quest
    'MM_M063_EM2390': M063_EM2390_FOLDER, #Cironnup Quest
    'MM_M063_EM2390_Start': M063_EM2390_FOLDER, #Cironnup Quest start
    'MM_M063_EM2397': M063_EM2390_FOLDER, #Cironnup Quest part 8
    'MM_M063_EM2580': M063_FOLDER, #Yoshitsune Haunt Quest (Atavaka)
    'MM_M064_EM1260': M064_FOLDER, #Demeter Defeat Chimera Shinjuku (Demeter)
    'MM_M064_EM1261': M064_FOLDER, #Demeter Defeat Chimera Shinjuku (Chimera)
    'MM_M064_EM1281': M064_FOLDER, #The Archangel of Destruction Shinjuku(Camael)
    'MM_M064_EM1291': M064_FOLDER, #Roar of Hatred Shinjuku(Moloch)
    'MM_M064_EM1391': M064_FOLDER, #Winged Sun (Mithras, Asura)
    'MM_M064_EM2130': M064_FOLDER, #Basilisk Hunt Quest (Anansi, Onyankopon)
    'MM_M064_EM2131': M064_FOLDER, #Basilisk Hunt Quest (Anansi)
    'MM_M064_EM2306': M064_EM2300_FOLDER, #Amabie in Macabre 
    'MM_M064_EM2360': M064_EM2360_FOLDER, #Alice Quest
    'MM_M064_EM2360_Event': M064_EM2360_FOLDER, #Alice Quest Event
    'MM_M064_EM2361': M064_EM2360_FOLDER, #Alice Quest part 2
    'MM_M064_EM2363': M064_EM2360_FOLDER, #Alice Quest part 4
    'MM_M064_EM2364': M064_EM2360_FOLDER, #Alice Quest part 5
    'MM_M064_EM2366': M064_EM2360_FOLDER, #Alice Quest part 7
    'MM_M064_EM2400': M064_FOLDER, #Samael Quest (Mastema)
    'MM_M064_EM2402': M064_FOLDER, #Samael Quest (Samael)
    'MM_M064_EM2421_Direct': M064_FOLDER, #Satan Quest (Satan)
    'MM_M064_EM2461': M064_FOLDER, #Mara Quest (Mara)
    'MM_M064_EM2500': M064_FOLDER, #Brawny Ambitions III (Okuninushi)
    'MM_M064_EM2521_Navi': M064_FOLDER, #Shinjuku Gem Quest
    'MM_M064_EM2552': M064_FOLDER, #MadGasser Quest (Zhen (3xCopy))
    'MM_M064_EM2621':M064_EM2620_FOLDER , #Orochi Quest (Orochi)
    'MM_M060_EM1381': M060_FOLDER, #Khonsu CoC Quest (Khonsu)
    'MM_M060_EM1390': M060_FOLDER, #Winged Sun CoC (Amon,Khonsu)
    'MM_M060_EM1390_NewRoute': M060_FOLDER, #Winged Sun CoV (Amon)
    'MM_M060_EM1391': M060_FOLDER, #Winged Sun CoC(Mithras, Asura)
    'MM_M060_EM1431': M060_FOLDER, #Holy Ring Quest (Uriel, Raphael,Gabriel)
    'MM_M060_EM1440': M060_FOLDER, #Baal Quest (Demeter)
    'MM_M060_EM1441': M060_FOLDER, #Baal Quest (Baal)
    'MM_M060_EM1580': M060_FOLDER, #On Bended Knees
    'MM_M060_EM1600': M060_FOLDER,  #Final Amanozako Quest (Kurama Tengu)
    'MM_M060_EM2371': M060_FOLDER,  #Garuda Quest (Garuda)
    'MM_M060_EM2480': M060_EM2480_FODLER,  #Nahobiho Quest
    'MM_M060_EM2481': M060_EM2480_FODLER,  #Nahobiho Quest part 2
    'MM_M060_EM2482': M060_EM2480_FODLER,  #Nahobiho Quest part 3
    'MM_M060_EM2483': M060_EM2480_FODLER,  #Nahobiho Quest part 4
    'MM_M060_EM2484': M060_EM2480_FODLER,  #Nahobiho Quest part 5
    'MM_M060_EM2570': M060_FOLDER, #Moirae Haunt Quest (Norn)
    'MM_M060_EM2630': M060_FOLDER,  #Saturnus Quest()
    'MM_M0082_E0171': MAIN_M082_FOLDER,#Event after Naming Protag that handles Students Talking
    'MM_M0082_E0171_First': MAIN_M082_FOLDER,#Event after Naming Protag 
    
    'BP_es035_m063_01': ES035_M063_FOLDER,#Fionn area 3 (Fionn)
    'BP_es152_m062_01': ES152_M062_FOLDER,#,#Hayataro area 2
    'BP_es152_m063_01': ES152_M063_FOLDER,#,#Hayataro area 3
    'BP_es416_m060_01': ES618_M060_FOLDER,#Nuwa in Area 4 
    'BP_es618_m060_01': ES618_M060_FOLDER,#Yakumo in Area 4 
    'BP_es418_m063_01': ES618_M063_FOLDER,#Nuwa in Area 3
    'BP_es618_m063_01': ES618_M063_FOLDER,#Yakumo in Area 3 
    
    'LV_E0660': DESIGN_EVENT_FOLDER, #Arioch Cutscene Test
    'LV_E0180': DESIGN_EVENT_FOLDER, #Triple Preta Cutscene
    'LV_E0181': DESIGN_EVENT_FOLDER, #Post Triple Preta Cutscene
    'LV_E0330': DESIGN_EVENT_FOLDER, #Snake Nuwa Pre-fight Cutscene
    'LV_E0340': DESIGN_EVENT_FOLDER, #Snake Nuwa Post-fight Cutscene
    'LV_E0350': DESIGN_EVENT_FOLDER, #Meeting Abdiel Cutscene
    'LV_E0375': DESIGN_EVENT_FOLDER, #Arioch Hayataro in Beginning of Shinagawa Cutscene
    'LV_E0379': DESIGN_EVENT_FOLDER, #Arioch Fionn 1 Cutscene

    'Pla038': PLAYER_038_FOLDER, #Playable Amanozako
    'Pla038_AnimBP': PLAYER_038_FOLDER, #Playable Amanozako Anims
    'Pla059': PLAYER_059_FOLDER, #Playable Pixie
    'Pla059_AnimBP': PLAYER_059_FOLDER, #Playable Pixie Anims
    'Pla060': PLAYER_060_FOLDER, #Playable Nahobiho
    'Pla060_AnimBP': PLAYER_060_FOLDER, #Playable Nahobiho Anims
    'Pla128': PLAYER_128_FOLDER, #Playable Cironnup
    'Pla128_AnimBP': PLAYER_128_FOLDER, #Playable Cironnup Anims
    'Pla289': PLAYER_289_FOLDER, #Playable Mo Shuvuu
    'Pla289_AnimBP': PLAYER_289_FOLDER, #Playable Mo Shuvuu Anims
    'Pla355': PLAYER_355_FOLDER, #Playable Alice
    'Pla355_AnimBP': PLAYER_355_FOLDER, #Playable Alice Anims

    'LV_EventMission_M061': LV_M061_FOLDER,
    'LV_MainMission_M061': LV_M061_FOLDER,
    'LV_MainMission_M061_P':LV_M061_FOLDER,
}

#List of scripts that are in the main mission folder despite submission naming convention
MAINMISSION_EXCEPTIONS = [
'MM_M062_EM0041','MM_M062_EM0050','MM_M062_EM0051','MM_M063_EM0061','MM_M063_EM0079','MM_M063_EM0070','MM_M061_EM0181',
'MM_M061_EM0182','EM_M061_Q0019','EM_M061_TutorialNavi02','MM_M062_EM0120_Direct','MM_M062_EM0122','MM_M062_EM0123','MM_M062_EM0124','MM_M062_EM0125',
'MM_M063_EM0130','MM_M060_EM0140', "MM_M061_EM0026","EM_M061_MimanTutorial_Stop"
]       

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
    Writes a specific uasset and uexp for every file in the list to their respective folder.
    '''
    def writeFile(self,name,file):
        folderKey = name
        if 'BtlAI' in name:
            folderKey = 'Btl_AI'
        elif 'SEQ' in name:
            subFolder = name.split("_")[1]
            folderKey = "LV_" + subFolder
        elif folderKey not in SCRIPT_FOLDERS.keys() and 'LV_E' not in folderKey:
            raise KeyError(f"No folder mapping found for '{name}' (folderKey = '{folderKey}')")

        
        if 'SEQ' not in name:
            stringy = json.dumps(file.json)
            file.uasset = file.uasset.DeserializeJson(stringy)
        if 'LV_E' in folderKey:
            writeFolder(DESIGN_EVENT_FOLDER)
        else:
            writeFolder(SCRIPT_FOLDERS[folderKey])
        if 'LV_E' in folderKey:
            subFolder = folderKey.split("_")[1]
            writeFolder(DESIGN_EVENT_FOLDER + '/'  + subFolder)
            file.uasset.Write(DESIGN_EVENT_FOLDER + '/'  + subFolder + '/' + name + '.umap')
        elif 'SEQ' in name:
            subFolder = name.split("_")[1]
            writeFolder(SCRIPT_FOLDERS[folderKey] + '/'  + subFolder)
            file.uasset.Write(SCRIPT_FOLDERS[folderKey] + '/'  + subFolder + '/' + name + '.uasset')
        else:
            file.uasset.Write(SCRIPT_FOLDERS[folderKey] + '/' + name + '.uasset')
        index = self.fileNames.index(name)
        self.fileNames.pop(index)
        self.files.pop(index)
        del file
        

    '''
    Writes the uasset and uexp for every file in the list to their respective folder.
    '''
    def writeFiles(self):
        for index, name in enumerate(self.fileNames):
            folderKey = name
            if 'BtlAI' in name:
                folderKey = 'Btl_AI'
            elif 'SEQ' in name:
                subFolder = name.split("_")[1]
                folderKey = "LV_" + subFolder
            elif folderKey not in SCRIPT_FOLDERS.keys() and 'LV_E' not in folderKey:
                raise KeyError(f"No folder mapping found for '{name}' (folderKey = '{folderKey}')")
            
            file = self.files[index]
            if 'SEQ' not in name:
                stringy = json.dumps(file.json)
                file.uasset = file.uasset.DeserializeJson(stringy)
            if 'LV_E' in folderKey and name[5].isnumeric():
                writeFolder(DESIGN_EVENT_FOLDER)
            else:
                writeFolder(SCRIPT_FOLDERS[folderKey])
            if 'LV_E' in folderKey and name[5].isnumeric():
                subFolder = folderKey.split("_")[1]
                writeFolder(DESIGN_EVENT_FOLDER + '/'  + subFolder)
                file.uasset.Write(DESIGN_EVENT_FOLDER + '/'  + subFolder + '/' + name + '.umap')
            elif 'LV_' in folderKey:
                file.uasset = file.uasset.DeserializeJson(stringy)
                file.uasset.Write(SCRIPT_FOLDERS[folderKey] + '/' + name + '.umap')
            elif 'SEQ' in name:
                subFolder = name.split("_")[1]
                writeFolder(SCRIPT_FOLDERS[folderKey] + '/'  + subFolder)
                file.uasset.Write(SCRIPT_FOLDERS[folderKey] + '/'  + subFolder + '/' + name + '.uasset')
            else:
                file.uasset.Write(SCRIPT_FOLDERS[folderKey] + '/' + name + '.uasset')
            #writeBinaryTable(file.uexp.buffer, SCRIPT_FOLDERS[folderKey] + '/' + name + '.uexp', SCRIPT_FOLDERS[folderKey])
            #writeBinaryTable(file.uasset.binaryTable.buffer, SCRIPT_FOLDERS[folderKey] + '/' + name + '.uasset', SCRIPT_FOLDERS[folderKey])
    
    '''
    Read the file belonging to the script of the given name and create a Script_File and add it to the list.
    '''
    def readFile(self,name):
        if 'BtlAI' in name:
            scriptPath = 'AI/'
        elif 'NPC' in name or 'BP_es' in name :
            scriptPath = 'NPC/'
        elif 'ShopEvent' in name or 'JakyoEvent' in name:
            scriptPath = 'ShopEvent/'
        elif name.startswith('Pla'):
            scriptPath = 'Player/'
        elif 'EM' in name and not 'DevilTalk' in name and not 'M092' in name:
            scriptPath = 'SubMission/'
        else:
            scriptPath = 'MainMission/'
        if name in MAINMISSION_EXCEPTIONS:
            scriptPath = 'MainMission/'
        if 'LV_E' == name[:4] and name[5].isnumeric():
            assetobject = UAsset('base/Design Event/' + name + '.umap', EngineVersion.VER_UE4_27)
        elif 'LV_' == name[:3]:
            assetobject = UAsset('base/Level/' +  name+ '.umap', EngineVersion.VER_UE4_27)
        elif 'SEQ' in name:
            assetobject = UAsset('base/Design Event/' + name + '.uasset', EngineVersion.VER_UE4_27)
        else:
        #uexp = readBinaryTable('base/Scripts/' + scriptPath + name + '.uexp')
        #uassetData = Script_Uasset(readBinaryTable('base/Scripts/' +scriptPath + name + '.uasset'))
            assetobject = UAsset('base/Scripts/' + scriptPath + name + '.uasset', EngineVersion.VER_UE4_27)

        jsonstring = assetobject.SerializeJson()
        jsonobject = json.loads(jsonstring)
        
        self.fileNames.append(name)
        self.files.append((Script_File(assetobject,jsonobject)))

class Script_File:
    def __init__(self,uasset: UAsset, jsonData):
        self.uasset = uasset
        self.json = jsonData
        self.originalJson = json.loads(json.dumps(jsonData))
        self.originalByteCodeSize = None
        self.originalBytecode = None
        self.originalNameMap = None

    '''
    Adds an import to the import list of the uasset.
        Parameters:
            classPackage(String): the package of the class of the import
            className(String): the class of the import 
            outerIndex(Integer): import index of the outer class/object, always <= 0
            objectName(String): the name of the import
            importOptional(Boolean): if the import is optional or not
    '''
    def addImport(self, classPackage, className, outerIndex: int, objectName, importOptional):
        # newImport = Import(classPackage, className, outerIndex, objectName, importOptional, self.uasset)
        # self.uasset.addImport(newImport)
        # self.updateJsonWithUasset()
        baseImport = {
            "$type": "UAssetAPI.Import, UAssetAPI",
            "ObjectName": objectName,
            "OuterIndex": outerIndex,
            "ClassPackage": classPackage,
            "ClassName": className,
            "PackageName": None,
            "bImportOptional": importOptional
            }
        self.json["Imports"].append(baseImport)
        self.json["NameMap"].append(objectName)

        self.updateFileWithJson(self.json)
    
    '''
    Returns the index of the given import, which is always negative.
    If the import does not exist it returns 1 instead.
    '''
    def getImportIndex(self, objectName):
        self.importNameList = [imp['ObjectName'] for imp in self.json['Imports']]
        if objectName not in self.importNameList:
            return 1
        else:
            return -1 * self.importNameList.index(objectName) -1
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
    
    def addNameToNameMap(self, name):  
        encoding = None
        try:
            name.encode('ascii')
            encoding = Encoding.ASCII
        except UnicodeEncodeError:
            encoding = Encoding.Unicode
        self.uasset.AddNameReference(FString.FromString(name,encoding),False,False)
    
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
    '''
    Returns a serialized version of the ScriptBytecode that contains Statement indeces.
        Parameters:
            exportIndex(Integer): the index of the export to get the scriptBytecode from
            updateJson(Dict): a dict of the json that should be used to as the base of the uasset 
    '''
    def getSerializedScriptBytecode(self,exportIndex, updatedJson = None):
            KismetSerializer.asset = self.uasset
            if updatedJson:
                    stringy = json.dumps(updatedJson)
                    uasset = self.uasset.DeserializeJson(stringy)
                    serializedCode = KismetSerializer.SerializeScript(uasset.Exports[exportIndex].ScriptBytecode)
            else:
                    serializedCode = KismetSerializer.SerializeScript(self.uasset.Exports[exportIndex].ScriptBytecode)
            jsonstring = serializedCode.ToString()
            serializedCodeObject = json.loads(jsonstring)
            return serializedCodeObject

    '''
    Calculates the last index for an exports scriptByteCode.
        Parameters:
            exportIndex(Integer): the index of the export to get the scriptBytecode from
            preLastIndex(Integer): the index where the last statement in the script starts at
            updateJson(Dict): a dict of the json that should be used to as the base of the uasset 
    '''
    def calcLastStatementIndex(self,exportIndex, preLastIndex,updatedJson = None):
        if updatedJson:
            stringy = json.dumps(updatedJson)
            uasset = self.uasset.DeserializeJson(stringy)
            KismetSerializer.asset = uasset
            newStatementIndex = KismetSerializer.SerializeExpression(uasset.Exports[exportIndex].ScriptBytecode[-1], preLastIndex, True)
        else:
            KismetSerializer.asset = self.uasset
            newStatementIndex = KismetSerializer.SerializeExpression(self.uasset.Exports[exportIndex].ScriptBytecode[-1], preLastIndex, True)
        return newStatementIndex[1]
    
    '''
    Reverses every boolean value for when the specified event flag is set using SetEventFlag.
    '''
    def jsonReverseFlagSetting(self,flagName):
        '''
        Reverses boolean value for the given parameter list of SetEventFlag.
        '''
        def reverseFlagValue(params):
            # Swap EX_True to EX_False and vice versa
            if params[1].get("$type") == "UAssetAPI.Kismet.Bytecode.Expressions.EX_True, UAssetAPI":
                params[1] = {
                    "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_False, UAssetAPI"
                }
            elif params[1].get("$type") == "UAssetAPI.Kismet.Bytecode.Expressions.EX_False, UAssetAPI":
                params[1] = {
                    "$type": "UAssetAPI.Kismet.Bytecode.Expressions.EX_True, UAssetAPI"
                }
        
        importIndex = self.getImportIndex("SetEventFlag")
        if importIndex < 1:
            self.recursiveSetFlag(self.json,importIndex,flagName,reverseFlagValue, 2)
        self.updateFileWithJson(self.json)
    
    '''
    Replaces every instance of a flag being passed as an parameter to either CheckEventFlag or SetEventFlag.
        Parameters:
            flagName(String): the name of the old flag to replace
            newFlagName(String): the name of the replacing flag
            modifySet(Boolean): if SetEventFlag should be modified
            modifyCheck(Boolean): if CheckEventFlag should be modified
    '''
    def jsonReplaceFlag(self, flagName, newFlagName, modifySet = False, modifyCheck = False):
        def replaceFlagName(params):
            params[0]["Value"] = newFlagName
        importIndex = self.getImportIndex("SetEventFlag")
        if importIndex < 1 and modifySet:
            self.recursiveSetFlag(self.json,importIndex,flagName,replaceFlagName,2)
        importIndex = self.getImportIndex("CheckEventFlag")
        if importIndex < 1 and modifyCheck:
            self.recursiveSetFlag(self.json,importIndex,flagName,replaceFlagName)
        self.updateFileWithJson(self.json)

    '''
    Recursively goes through the ScriptByteCode to find use cases of CheckEventFlag or SetEventFlag.
        Parameters:
            obj(Dict): the thing to look at recursively
            importIndex(Integer): the import index of the searched function
            flagName(String): the name of the flag which should be in the parameters of the function
            action(Function): the method that should be performed for the parameters of the found functions
            paramCount(Integer): how many parameters the target function has 
    
    '''
    def recursiveSetFlag(self,obj,importIndex,flagName,action,paramCount = 1):
        if isinstance(obj, dict):
            if obj.get("$type") == "UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath, UAssetAPI":
                params = obj.get("Parameters", [])
                if (len(params) == 2 == paramCount and 
                    params[0].get("$type") == "UAssetAPI.Kismet.Bytecode.Expressions.EX_NameConst, UAssetAPI" and
                    params[0].get("Value") == flagName):

                    action(params)
                elif (len(params) == 1 == paramCount and
                    params[0].get("$type") == "UAssetAPI.Kismet.Bytecode.Expressions.EX_NameConst, UAssetAPI" and
                    params[0].get("Value") == flagName):
                    action(params)

                    

            for value in obj.values():
                self.recursiveSetFlag(value,importIndex, flagName, action,paramCount)

        elif isinstance(obj, list):
            for item in obj:
                self.recursiveSetFlag(item,importIndex, flagName, action,paramCount)

    


            
class General_UAsset:
    def __init__(self,name, writePath, readPath = 'base/'):
        self.uasset =  UAsset(readPath +  name+ '.uasset', EngineVersion.VER_UE4_27)
        self.name = name
        self.writePath = writePath
        jsonstring = self.uasset.SerializeJson()
        self.json = json.loads(jsonstring)
        self.originalJson = json.loads(jsonstring)
    
    def write(self):
        writeFolder(self.writePath)
        stringy = json.dumps(self.json)
        self.uasset = self.uasset.DeserializeJson(stringy)
        self.uasset.Write(self.writePath + self.name +'.uasset')
        self.uasset = None
