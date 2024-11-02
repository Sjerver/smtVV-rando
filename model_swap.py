from base_classes.script import Script_Function_Type,Script_Uasset,Bytecode
from base_classes.file_lists import UMap_File, UMap_File_List, Script_File, Script_File_List
from base_classes.message import Demon_Sync
from base_classes.demon_assets import Demon_Model
from base_classes.uasset_custom import UAsset_Custom
from util.binary_table import readBinaryTable
import util.paths as paths
import util.numbers as numbers
import util.jsonExports as jsonExports
import pandas as pd
import copy
import random

class Anim_Sync():
    def __init__(self,ind, sync=None):
        self.ind = ind
        self.sync = ind
        if sync:
            self.sync = sync

DEBUG_SWAP_PRINT = True

DEVIL_PREFIX = "/Devil/"
NPC_PREFIX = "/NPC/"
NPC_MODEL_START = 600
LAHMU_2ND_FORM_ID = 236

#Model IDs that use Dev Class Blueprints but are in NPC folder otherwise
NPC_MODELS_DEV_BLUEPRINT = [621,622,625,626,627,641,642,643,646,647,648,649,650,651]

MODEL_NAMES = {}
DEMON_ID_MODEL_ID = {}
HAS_SIMPLE_BP = {}
DEMON_MODELS={}

#List of which level umaps event scripts use for their location and sizes
#To find out, look at which MapEventID the Script has in its File and then take a look at map event data
LEVEL_UASSETS = {
    'MM_M061_EM1630': 'LV_EventMission_M061',
    'MM_M061_EM1631': 'LV_EventMission_M061',
    'MM_M061_EM1640': 'LV_EventMission_M061',
}

#List of events that require updated scaling to trigger events with large demons
REQUIRES_HIT_UPDATE = [
    'MM_M061_EM1630','MM_M061_EM1631','MM_M061_EM1640','MM_M016_E0885'
    'MM_M064_E2512'
]

#TODO: Investigate certain events which might have the used models in umaps (example: Arioch Pre-Fight, Odin, Vasuki, Meeting Mastema 2ndHalf)
#Swapping works! but animations might also be possible since they are in the sequence files (need to investigate this in more detail)
EVENT_CUTSCENES = {
    'LV_E0660': [Demon_Sync(82,463)], #UMAP Arioch Event
}

#Script files for events and what demon models need to be updated in htem
#Demon_Sync(demonID in file, if different from demonID in file: demonID to take replacement from)
EVENT_SCRIPT_MODELS = {
    #Initial & Mainmission M061 (Minato)
    'EM_M061_DevilTalk': [Demon_Sync(59)], #Talk Tutorial (Pixie)
    'MM_M061_EM1630': [Demon_Sync(305),Demon_Sync(43)], # The Water Nymph (Leanan (also Apsaras maybe??))
    'MM_M061_EM1631': [Demon_Sync(316,867)], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Demon_Sync(43),Demon_Sync(44,869)], # The Spirit of Love (Apsaras, Agathion)
    'MM_M061_EM1640_Hit': [Demon_Sync(43)], # The Spirit of Love First Entry (Apsaras)
    'MM_M061_E2610' : [Demon_Sync(193,579),Demon_Sync(561),Demon_Sync(1151,578)], #CoV Isis Event Bethel Egypt (Isis, Yuzuru,Dazai)
    'MM_M061_E2620': [Demon_Sync(561),Demon_Sync(1151,578),Demon_Sync(7,566)], #CoV Khonsu Event Bethel Egypt (Khonsu,Yuzuru,Dazai)
    'MM_M061_E2625_Direct': [Demon_Sync(193,579),Demon_Sync(7,566),Demon_Sync(561),Demon_Sync(1151,578)], #CoV Khonsu Event Post Fight Bethel Egypt (Isis,Khonsu,Yuzuru,Dazai)
    #Mainmission M016 (Empyrean)
    'MM_M016_E0885': [Demon_Sync(152)], #CoC Chaos Route Empyrean Hayataro Joins After Stock is Full (Hayataro)
    'MM_M016_E0885_Direct': [Demon_Sync(152)], #CoC Chaos Route Empyrean Hayataro Joins Stock is Full so wait (Hayataro)
    'MM_M016_E0891': [Demon_Sync(249,471)], #Empyrean Melchizedek
    'MM_M016_E0892': [Demon_Sync(244,472)], #Empyrean Sraosha
    'MM_M016_E0893': [Demon_Sync(198,473)], #Empyrean Alilat
    #Mainmission M035 & 36 (Temple of Eternity & DKC)
    'MM_M035_E0825': [Demon_Sync(241,477)], #Temple of Eternity Metatron
    'MM_M036_E0644': [Demon_Sync(182,466)], #DKC Pre Chernobog
    'MM_M036_E0650': [Demon_Sync(240,467)], #DKC Abdiel & Dazai Event
    'MM_M036_E0670': [Demon_Sync(465),Demon_Sync(82,463),Demon_Sync(240,467),Demon_Sync(75,435)], #DKC Post Arioch(Yakumo,Arioch,Abdiel)
    #Mainmission M038 (Shakan)
    'MM_M038_E2912': [Demon_Sync(256,484),Demon_Sync(255,485)], #Shakan Dark Block Bros
    'MM_M038_E2917': [Demon_Sync(260,486)], #Shakan Cherub
    'MM_M038_E2930_Direct': [Demon_Sync(240,564)], #Shakan Abdiel Post Fight
    #Mainmission M060 (Taito)
    'MM_M060_E0762': [Demon_Sync(75,520),Demon_Sync(465)], #Nuwa in area 4 at the gate (Uses Replacement for Nahobino Nuwa, Yakumo)
    'MM_M060_E0778': [Demon_Sync(468),Demon_Sync(37,878)], #Vasuki Post Fight Event (Vasuki, Kurama Tengu)
    'MM_M060_E0785': [Demon_Sync(8,469)], #CoC Taito Zeus Appears
    'MM_M060_E0790': [Demon_Sync(8,469),Demon_Sync(37,878)],#CoC Taito Zeus PostFight (Zeus, Kurama Tengu)
    'MM_M060_E0810': [Demon_Sync(9,470),Demon_Sync(37,878)],#CoC Odin PostFight (Odin, Kurama Tengu)
    'MM_M060_E3010': [Demon_Sync(465,567)], #Yakumo in area 4 vengeance
    'MM_M060_E3020': [Demon_Sync(465,567)], #Yakumo in area 4 vengeance part 2
    'MM_M060_E3110_Direct': [Demon_Sync(81,483)], #CoV Beelzebub
    'MM_M060_E3130_Direct': [Demon_Sync(482),Demon_Sync(481)], #CoV Zeus + Odin
    'MM_M060_Npc609Talk': [Demon_Sync(152)], #CoC Yuzuru Hayataro NPC Event?
    #Mainmission M062 (Shinagawa)
    'MM_M062_E0378': [Demon_Sync(467)], #Dazai/Abdiel talk in area 2 creation (Abdiel)
    'MM_M062_E0380': [Demon_Sync(35,451)], #Fionn 1 Post-fight (Fionn)
    'MM_M062_E0492': [Demon_Sync(453)], #Final Lahmu (Lahmu Phase 2)
    'MM_M062_EM0041': [Demon_Sync(450)], #Loup-garous Event
    'MM_M062_E2275': [Demon_Sync(564),Demon_Sync(1151,578)], #Dazai/Abdiel talk in area 2 vengeance (Abdiel,Dazai)
    'MM_M062_E2295_Direct': [Demon_Sync(559)], #Eisheth pre-fight
    'MM_M062_E2298_Direct': [Demon_Sync(451)], #Fionn post-fight Vengeance
    'MM_M062_E2300': [Demon_Sync(1151,578)], #Dazai Pre-Blocker Vengeance
    'MM_M062_E2302': [Demon_Sync(561),Demon_Sync(1151,578)], #Arriving in fairy village vengeance (Yuzuru,Dazai)
    #Mainmission M063 (Chiyoda)
    'MM_M063_E0625': [Demon_Sync(465),Demon_Sync(75,435)], #Yakumo post-fight Chiyoda (Yakumo, Nuwa)
    'MM_M063_EM0061': [Demon_Sync(822),Demon_Sync(823),Demon_Sync(824)], #Hellfire Highway (Okuninushi, Sukuna Hikona, Minakata)
    'MM_M063_EM0079': [Demon_Sync(455)], #Ishtar Post Fight
    'MM_M063_M0680': [Demon_Sync(467)],#Abdiel celebrates Arioch's death (Abdiel)
    #Mainmission M064 (Shinjuku)
    'MM_M064_E2510_Direct': [Demon_Sync(503)], #First Power Fight in Shinjuku
    'MM_M064_E2512': [Demon_Sync(504)], #Second Power Fight in Shinjuku
    'MM_M064_E2514': [Demon_Sync(505)], #Powers detecting other intruders (uses Triple Power Fight Replacement)
    'MM_M064_E2520_Direct': [Demon_Sync(550),Demon_Sync(567)], #First Nuwa/Yakumo scene in Shinjuku 
    'MM_M064_E2540': [Demon_Sync(506)], #Power Gauntlet (uses last Power Fight Replacement)
    'MM_M064_E2550': [Demon_Sync(486)], #Cherub Blocker in Shinjuku (?)
    'MM_M064_E2560': [Demon_Sync(550),Demon_Sync(567)], #Nuwa/Yakumo talk at Mastema's hill
    'MM_M064_E2562_Direct': [Demon_Sync(550),Demon_Sync(567)], #Nuwa/Yakumo talk at Mastema's hill 2 
    'MM_M064_E2638': [Demon_Sync(1151,578)], #Dazai joins to see Mastema 2 (?)
    'MM_M064_E2642_Direct': [Demon_Sync(1151,578),Demon_Sync(596)], #Meeting Mastema (Dazai,Mastema)
    'MM_M064_E2650_Direct': [Demon_Sync(550),Demon_Sync(567)], #Nuwa/Yakumo talk after seeing Naamah (Nuwa, Yakumo)
    'MM_M064_E2690': [Demon_Sync(486)], #Dead Cherubim 
    'MM_M064_E2900': [Demon_Sync(596)],#Mastema sends you to Shakan
    'MM_M064_E2950_Direct': [Demon_Sync(596)],#Mastema after Shakan
}

#Which animations are being played in scripts that might not be available to every demon and which to use instead
#Beware Capitalization!!
#TODO: A lot of story events have very specific animations that all would most likely just be replaced by IdleA which in most cases seems to be playing on default anyway so they can be skipped?
SCRIPT_ANIMS_REPLACEMENTS = {
    'EM_M061_DevilTalk': [Anim_Sync('02idleB','05attack')], #Talk Tutorial (Pixie)
    'MM_M061_EM1630': [Anim_Sync('06skill_Composite','06_skill')], # The Water Nymph (Leanan)
    'MM_M061_EM1631': [Anim_Sync('map/700000_event_idle', '01idleA')], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Anim_Sync('06skill_Composite','06_skill')], # The Spirit of Love (Apsaras)
    'MM_M061_EM1640_Hit': [Anim_Sync('map/700000_event_idle', '01idleA')], # The Spirit of Love First Entry (Apsaras)
    'MM_M061_E2625_Direct': [Anim_Sync('map/700000_dying','04dying')], #CoV Khonsu Event Post Fight Bethel Egypt (Isis,Khonsu,Yuzuru,Dazai)
    'MM_M038_E2930_Direct': [Anim_Sync('EVT_E0604c01m_loop','04dying')], #Shakan Abdiel Post Fight
    'MM_M060_E762': [Anim_Sync('map/700000_event_idle', '01idleA')],#Nuwa in area 4 at the gate
    'MM_M060_E3020': [Anim_Sync('Event/EVT_v_turnwalk_inout','11run')], #Yakumo in area 4 vengeance part 2
    'MM_M062_E0380': [Anim_Sync('Map/700002_event_idle','01idleA')], #Fionn 1 Post-fight (Fionn)
    'MM_M062_E0492': [Anim_Sync('3rd_01idleA','01idleA'),Anim_Sync('3rd_41encount','41encount')], #Final Lahmu (Lahmu Phase 2)
    #'MM_M062_EM0041': [Anim_Sync('Event/EVT_SlowEncount_inout','41encount')], #Loup-garous Event
    'MM_M062_E2295_Direct': [Anim_Sync('02idleB','05attack')],#Eisheth pre-fight
    'MM_M062_E2298_Direct': [Anim_Sync('Map/700002_event_idle','01idleA')], #Fionn 1 Post-fight Vengeance (Fionn)
    'MM_M064_E2690': [Anim_Sync('map/700000_dead01','04dying'),Anim_Sync('map/700001_dead02','04dying')], #Dead Cherubim
}

#For bosses that do not use their own model, which model they should use instead
MODEL_SYNC = {
    434: 272, # 2 Andras from Eligor
    577: 264, # Abdiel (Fallen)
    564: 240, # Abdiel (Shakan)
    467: 240, # Abdiel (Summit)
    884: 265, # Adramelech
    869: 44, # Agathion (with Apsaras)
    568: 392, # Agrat
    487: 114, # Aitvaras (School Copy)
    442: 114, # Aitvaras (School)
    473: 198, # Alilat
    831: 76, # Amon
    803: 20, # Anahita
    771: 41, # Anansi
    781: 272, # Andras (3x)
    488: 272, # Andras (School Copy)
    489: 272, # Andras (School Copy)
    490: 272, # Andras (School Copy)
    443: 272, # Andras (School)
    517: 120, # Anubis (CoC Summon)
    439: 287, # Anzu (Jozoji)
    728: 287, # Anzu (Single Abcess)
    606: 287, # Anzu (with Mishaguji)
    868: 43, # Apsaras
    463: 82, # Arioch
    930: 31, # Artemis
    829: 181, # Asura
    628: 12, # Atavaka
    776: 12, # Atavaka (with Rakshasa)
    837: 17, # Baal
    856: 126, # Baihu
    746: 235, # Baphomet
    629: 119, # Barong
    738: 113, # Basilisk
    483: 81, # Beelzebub
    840: 83, # Belial
    859: 203, # Bishamonten (2 Turn)
    863: 203, # Bishamonten (4 Turn)
    773: 171, # Black Ooze
    926: 352, # Black Rider
    814: 248, # Camael
    466: 182, # Chernobog
    486: 260, # Cherub
    931: 295, # Cleopatra
    612: 36, # Cu Chulainn
    619: 191, # Cybele
    947: 4, # Dagda
    922: 357, # Daisoujou
    613: 297, # Dakini
    843: 188, # Danu
    464: 273, # Decarabia (Summon)
    881: 183, # Dionysus
    780: 46, # Dís
    485: 255, # Dominion
    751: 141, # Dormarth
    725: 141, # Dormarth (Abcess)
    730: 47, # Efreet
    559: 394, # Eisheth
    433: 270, # Eligor
    603: 282, # Feng Huang
    833: 35, # Fionn mac Cumhaill (2nd)
    451: 35, # Fionn mac Cumhaill (First)
    732: 266, # Flauros (Abcess)
    474: 266, # Flauros (Summon)
    818: 266, # Flauros (With Moloch)
    883: 201, # Futsunushi
    836: 243, # Gabriel
    865: 278, # Garuda
    555: 142, # Glasya-Labolas (with Naamah)
    608: 34, # Hanuman
    562: 152, # Hayataro
    923: 356, # Hell Biker
    864: 13, # Horus
    844: 189, # Inanna
    495: 68, # Incubus (School Copy)
    496: 68, # Incubus (School Copy)
    497: 68, # Incubus (School Copy)
    498: 68, # Incubus (School Copy)
    720: 316, # Ippon-Datara (Abcess)
    867: 316, # Ippon-Datara (with Leanan)
    455: 25, # Ishtar
    579: 193, # Isis
    611: 193, # Isis (Abcess)
    601: 58, # Jack Frost (Abcess)
    802: 281, # Jatayu
    858: 204, # Jikokuten
    862: 204, # Jikokuten (4 Turn)
    607: 66, # Kaiwan
    516: 7, # Khonsu (CoC)
    566: 7, # Khonsu (CoC)
    519: 15, # Khonsu Ra
    753: 336, # Kodama
    948: 32, # Konohana Sakuya
    819: 205, # Koumokuten (2 Turn)
    861: 205, # Koumokuten (4 Turn)
    774: 40, # Kresnik
    772: 346, # Kudlak
    809: 342, # Kumbhanda
    723: 342, # Kumbhanda (Abcess)
    878: 37, # Kurama Tengu (with Zaou)
    616: 213, # Kushinada-Hime
    557: 236, # Lahmu (School 2nd TODO: Why did I find you???)
    556: 441, # Lahmu (School)
    452: 441, # Lahmu (Shinagawa 1st)
    453: 236, # Lahmu (Shinagawa 2nd)
    727: 303, # Lamia (Abcess)
    440: 303, # Lamia (Jozoji)
    580: 303, # Lamia (with Isis)
    710: 305, # Leanan Sidhe (Abcess)
    866: 305, # Leanan Sidhe (with Ippon)
    880: 67, # Lilim
    569: 391, # Lilith
    810: 89, # Loki
    450: 136, # Loup-garou
    537: 529, # Lucifer
    729: 174, # Mad Gasser
    602: 121, # Makami
    500: 302, # Manananggal (School Copy)
    501: 302, # Manananggal (School Copy)
    705: 45, # Mandrake
    842: 30, # Maria
    757: 227, # Masakado
    758: 227, # Masakado (True)
    596: 250, # Mastema
    921: 359, # Matador
    471: 249, # Melchizedek
    476: 249, # Melchizedek (No EXP Revive)
    932: 78, # Mephisto
    610: 304, # Mermaid
    477: 241, # Metatron
    841: 242, # Michael
    605: 234, # Mishaguji
    830: 88, # Mithras
    625: 11, # Mitra
    928: 351, # Mother Harlot
    722: 289, # Muu Shuwuu
    553: 393, # Naamah
    554: 393, # Naamah (with GL)
    604: 104, # Naga Raja
    779: 22, # Norn
    752: 107, # Nozuchi
    435: 197, # Nuwa (Snake)
    550: 75, # Nuwa (with Yakumo)
    609: 52, # Oberon
    470: 9, # Odin (CoC)
    482: 9, # Odin (CoV)
    822: 215, # Okuninushi
    888: 318, # Oni (Quest)
    499: 318, # Oni (School Copy)
    446: 318, # Oni (School)
    706: 290, # Onmoraki
    770: 386, # Onyankopon
    731: 139, # Orobas (Abcess)
    817: 139, # Orobas (With Moloch)
    726: 135, # Orthrus
    475: 269, # Ose (Summon)
    825: 212, # Oyamatsumi (With Kunitsu)
    927: 358, # Pale Rider
    801: 233, # Pazuzu
    755: 341, # Pisaca
    621: 59, # Pixie
    506: 256, # Power (5x Copy)
    504: 256, # Power (Double Copy)
    503: 256, # Power (Single Copy)
    505: 256, # Power (Triple Copy)
    815: 256, # Power (with Camael)
    484: 256, # Power (With Dominions)
    713: 345, # Preta (Abcess)
    889: 345, # Preta (Quest)
    879: 257, # Principality
    854: 96, # Qing Long
    933: 95, # Quetzalcoatl
    492: 324, # Rakshasa (School Copy)
    493: 324, # Rakshasa (School Copy)
    494: 324, # Rakshasa (School Copy)
    444: 324, # Rakshasa (School)
    777: 324, # Rakshasa (with Atavaka)
    491: 324, # Rakshasa(School Copy)
    626: 296, # Rangda
    835: 245, # Raphael
    925: 353, # Red Rider
    760: 118, # Samael
    614: 24, # Sarasvati
    681: 1, # Satan
    782: 237, # Saturnus
    618: 26, # Scathach
    724: 130, # Senri
    870: 112, # Seth
    750: 129, # Shiisaa
    820: 311, # Shiki-Ouji (Quest)
    502: 311, # Shiki-Ouji (School Copy)
    448: 311, # Shiki-Ouji (School)
    845: 178, # Shiva
    630: 222, # Siegfried
    615: 53, # Silky
    627: 192, # Skadi
    622: 173, # Slime
    472: 244, # Sraosha
    721: 65, # Succubus
    718: 335, # Sudama (Abcess)
    823: 214, # Sukuna-Hikona
    824: 216, # Take-Minakata
    778: 200, # Thor
    734: 14, # Thoth (Abcess)
    518: 14, # Thoth (CoC Summon)
    431: 345, # Three Pretas
    624: 254, # Throne
    929: 350, # Trumpeter
    449: 331, # Tsuchigumo (School)
    754: 175, # Turbo Granny
    834: 247, # Uriel
    468: 111, # Vasuki
    769: 108, # Vouivre
    733: 99, # Vritra
    924: 354, # White Rider
    857: 97, # Xuanwu
    768: 299, # Yakshini
    775: 103, # Yamata-no-Orochi (8 Turn)
    620: 103, # Yamata-no-Orochi (Abcess)
    623: 280, # Yatagarasu
    617: 105, # Yurlungur
    877: 180, # Zaou-Gongen
    469: 8, # Zeus (CoC)
    481: 8, # Zeus (CoV)
    838: 8, # Zeus (Demeter Quest)
    509: 288, # Zhen (3x Copy)
    510: 288, # Zhen (4x Copy)
    756: 288, # Zhen (5x)
    855: 279, # Zhuque
    805: 206, # Zouchouten (2 Turn)
    860: 206, # Zouchouten (4 Turn)
    558: 441, # Tentacle (use Lahmu model instead)
    424: 441, # Tentacle (use Lahmu model instead)
    593: 565, # Dragon Head (use Tiamat)
    594: 565, # Goat Head (use Tiamat)
    595: 565, # Camel Head (use Tiamat)
    567: 465, # Shohei Yakumo (Vengeance)
    521: 627, # Thunder Bit (use Nahobino Nuwa)
    522: 627, # Thunder Bit (use Nahobino Nuwa)
    523: 627, # Thunder Bit (use Nahobino Nuwa)
    524: 627, # Thunder Bit (use Nahobino Nuwa)
    526: 525, # Depraved Arm (use Nahobino Abdiel)
    527: 525, # Depraved Wing (use Nahobino Abdiel)

    #TODO: Should be complete? With the exception of bosses who use NPC Models
}



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
def updateEventModels(encounterReplacements, bossReplacements, scriptFiles, mapSymbolArr, config):
    initDemonModelData()
    umapList = UMap_File_List()
    for script, syncDemons in EVENT_SCRIPT_MODELS.items():
        
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
            #replacementID = random.choice([441,236]) #Testing stuff
            # if originalDemonID in replacementMap.values():
            #     print("Causes Chain replacement: " + str(originalDemonID) + " " + str(replacementID) )
            replacementMap[originalDemonID] = replacementID
        
        file = scriptFiles.getFile(script)
        hitboxUpdated = False
            
        for originalDemonID, replacementID in replacementMap.items():
            if not hitboxUpdated:
                try:
                    og = next(d for x, d in enumerate(mapSymbolArr) if d.demonID == originalDemonID)
                    replacement = next(d for x, d in enumerate(mapSymbolArr) if d.demonID == replacementID)
                    scalingFactor = og.encountCollision.stretchToBox(replacement.encountCollision, ignoreY = True)
                    if scalingFactor != 0:
                        #print(scalingFactor)
                        scale = scalingFactor
                    else:
                        scale = 1.5 #Increase by 50%
                except StopIteration:
                    scale = 1.5 #Increase by 50%
            if scale <= 1: #do not update hitbox size if scale would be smaller
                continue
            if not hitboxUpdated and script in REQUIRES_HIT_UPDATE and script in LEVEL_UASSETS.keys(): #TODO: How to deal with overlap issues
                umap = umapList.getFile(LEVEL_UASSETS[script])
                hitboxUpdated = True
                umap = updateEventHitScaling(umap,script,scale)
            elif not hitboxUpdated and script in REQUIRES_HIT_UPDATE: #no umap for event exists
                updateEventHitGen(file,scale,script)

            file = replaceDemonModelInScript(script, file, originalDemonID, replacementID, scriptFiles)   
        
        scriptFiles.setFile(script,file)
    umapList.writeFiles()




'''
Replaces the a demon model with the model of another demon in the given script.
    Parameters:
        script(String): the name of the script
        uassetData (Script_Uasset): the uasset data of the script
        uexpData (Table): the binary data of the uexp of the script
        ogDemonID (Integer): the id of the demon that should be replaced
        replacementDemonID (Integer): the id of the replacement demon
        scriptFiles (Script_File_List): list of scripts to store scripts for multiple edits
        #TODO: Think about how to optimize this function
'''
def replaceDemonModelInScript(script, file: Script_File, ogDemonID, replacementDemonID, scriptFiles: Script_File_List):
    jsonData = file.json
    #Get the Strings corresponding to the old demon
    oldIDString = DEMON_ID_MODEL_ID[ogDemonID]
    oldName = MODEL_NAMES[oldIDString]
    oldFolderPrefix = DEVIL_PREFIX
    oldPrefix = "dev"
    oldPrefixVariant = "Dev"
    if int(oldIDString) > NPC_MODEL_START:
        oldFolderPrefix = NPC_PREFIX
        oldPrefix = "npc"
        oldPrefixVariant = "Npc"
    #Get the Strings corresponding to the new demon
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
        
    elif int(oldIDString) in NPC_MODELS_DEV_BLUEPRINT:
        #old is exception that use devil instead of npc for this
        classOldFolderPrefix = DEVIL_PREFIX
        classOldPrefix = "dev"
        classOldPrefixVariant = "Dev"

    if file.originalNameMap is None: #use original name map to prevent chain replacements
        file.originalNameMap = copy.deepcopy(jsonData['NameMap'])

    for index, name in enumerate(file.originalNameMap): #change occurences of oldDemonID and oldDemonName in all names in the uasset
        nameEntry = file.getNameAtIndex(index)
        #TODO: Add something for anims which are in this name map
        if oldIDString in name and ("/Blueprints/Character" in name or "_C" in name): 
            nameEntry = nameEntry.replace(classOldFolderPrefix + classOldPrefix + oldIDString, classNewFolderPrefix + classNewPrefix +newIDString).replace(classOldPrefix + oldIDString, classNewPrefix +newIDString)
            nameEntry = nameEntry.replace(classOldFolderPrefix + classOldPrefixVariant + oldIDString, classNewFolderPrefix + classNewPrefixVariant +newIDString).replace(classOldPrefixVariant + oldIDString, classNewPrefixVariant +newIDString)
            if 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] and "_Simple" in name: #change bp name if demon does not have simple blueprint
                nameEntry = nameEntry.replace("_Simple","")
        elif oldIDString in name: #to just get the model names since sometimes DevXXX or devXXX
            nameEntry = nameEntry.replace(oldFolderPrefix + oldPrefix + oldIDString, newFolderPrefix + newPrefix +newIDString).replace(oldPrefix + oldIDString, newPrefix +newIDString)
            nameEntry = nameEntry.replace(oldFolderPrefix + oldPrefixVariant + oldIDString, newFolderPrefix + newPrefixVariant +newIDString).replace(oldPrefixVariant + oldIDString, newPrefixVariant +newIDString)
            if 'FALSE' == HAS_SIMPLE_BP[replacementDemonID] and "_Simple" in name: #change bp name if demon does not have simple blueprint
                nameEntry = nameEntry.replace("_Simple","")
        file.setNameAtIndex(index,nameEntry)
        if oldName in name:
            nameEntry = file.getNameAtIndex(index)
            nameEntry = nameEntry.replace(oldName,newName)
            file.setNameAtIndex(index,nameEntry)
    
    #get updated jsonData
    jsonData = file.updateJsonWithUasset()

    bytecode = None
    byteCodeSize = None
    exportIndex = None
    try: #get bytecode and bytecode size for main portion if UAssetAPI can parse it
        exportNameList = [exp['ObjectName'] for exp in jsonData["Exports"]]
        executeUbergraph = "ExecuteUbergraph_" + script
        exportIndex = exportNameList.index(executeUbergraph)

        bytecode = Bytecode(jsonData["Exports"][exportIndex]['ScriptBytecode'])
        byteCodeSize = jsonData["Exports"][exportIndex]['ScriptBytecodeSize']
    except KeyError: #otherwise stop and note error
        print("Script Byte Code only in raw form")
        return
    
    if file.originalByteCodeSize is None: 
        file.originalByteCodeSize = byteCodeSize#Set bytecode size to not replace bytecode moved to the end
        file.originalBytecode = copy.deepcopy(bytecode)#Also use original bytecode to prevent chain replacements

    #Adjust cases where the function name is explicitly in the code
    relevantFunctionNames = ['BPL_AdjustMapSymbolScale']
    for func in relevantFunctionNames:
        expressions = file.originalBytecode.findExpressionUsage("UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVirtualFunction", virtualFunctionName= func)
        for exp in expressions:
            modelValue = exp['Parameters'][1].get('Value')
            if modelValue == ogDemonID: #Only change demonID for the oldDemon
                exp['Parameters'][1]['Value'] = replacementDemonID

    serializedByteCode = file.getSerializedScriptBytecode(exportIndex,jsonData)
    
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

    importNameList = [imp['ObjectName'] for imp in jsonData['Imports']]
    relevantImportNames = ['LoadAsset','PrintString','LoadAssetClass']
    relevantImports = {}
    for imp in relevantImportNames: #Determine import id for relevant import names which is always negative
        if imp in importNameList:
            relevantImports[imp] = -1 * importNameList.index(imp) -1
    #Adjust cases where function name is not explicit in code due to being an import
    for imp,stackNode in relevantImports.items():
        expressions = file.originalBytecode.findExpressionUsage('UAssetAPI.Kismet.Bytecode.Expressions.EX_CallMath', stackNode)
        expressions.reverse()
        for expIndex, exp in enumerate(expressions):
            if bytecode.getIndex(exp) is None:
                # First case: Nested expression (will be fixed at some point)
                # Second case: Expression has already been modified in the new one, so we can skip it here
                continue
            if imp == 'PrintString': #likely not necessary but do it anyway
                stringValue = exp['Parameters'][1].get('Value')
                stringValue = stringValue.replace(oldIDString,newIDString)
                newExpression = bytecode.json[bytecode.getIndex(exp)]
                newExpression['Parameters'][1]['Value'] = stringValue
            elif imp == 'LoadAsset' or imp == 'LoadAssetClass':
                try:
                    stringValue = exp['Parameters'][1].get('Value').get('Value')
                except AttributeError:
                    continue
                originalLength = len(stringValue)
                #create new string here for calculation of lenghtDifference
                newString = replaceOldIDinString(stringValue).replace(oldName,newName)
                lengthDifference = len(newString) - originalLength

                if oldIDString in stringValue and lengthDifference == 0: 
                    #if the oldID is there in string format, replace with new string
                    stringValue= replaceOldIDinString(stringValue)
                    
                if oldName in stringValue and lengthDifference == 0:
                    #length is the same so can swap name and anim
                    stringValue = stringValue.replace(oldName,newName)
                    if ("/Blueprints/Character" in stringValue or "_C" in stringValue):
                        stringValue = replaceNonExistentAnimations(script, newString,newIDString,newName, classOldFolderPrefix, classOldPrefix, classNewFolderPrefix, classNewPrefix, lahmuSuffix)
                    else:
                        stringValue = replaceNonExistentAnimations(script, stringValue,newIDString,newName, oldFolderPrefix, oldPrefix, newFolderPrefix, newPrefix, lahmuSuffix)#exp['Parameters'][1]['Value']['Value'] = stringValue
                    newExpression = bytecode.json[bytecode.getIndex(exp)]
                    newExpression['Parameters'][1]['Value']['Value'] = stringValue
                elif lengthDifference != 0:
                    #length is not the same so need to move expression around
                    #recalc new string just in case
                    stringValue = replaceOldIDinString(stringValue)
                    newString = stringValue.replace(oldName,newName)
                    newString = replaceOldIDinString(newString)

                    currentStatementIndex = serializedByteCode[bytecode.getIndex(exp)]["StatementIndex"]
                    nextStatementIndex = serializedByteCode[bytecode.getIndex(exp)+1]["StatementIndex"]
                    lastStatementIndex = file.calcLastStatementIndex(exportIndex,serializedByteCode[-1]["StatementIndex"], jsonData)
                    statementLength = nextStatementIndex - currentStatementIndex
                    
                    if currentStatementIndex > file.originalByteCodeSize: #to not move code that has been moved already!
                        continue
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
                    serializedByteCode = file.getSerializedScriptBytecode(exportIndex,jsonData)
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
        if animation in DEMON_MODELS[replacementID].animations:
            #Animation exists for the new demon therefore string is fine
            return string
        #Animation does not exist for the new demon therefore string needs to be changed
        if '/' in animation: #Is Animation in Subfolder?
            animationParts = animation.split("/")
            searchString = "/Game/Design/Character/"+oFPrefix+"/"+oPrefix + replacementID + "_" + replacementName + "/Anim/" + animationParts[0] + "/" + "AN_"+oPrefix + replacementID + lahmuSuffix + "_" + animationParts[1]+ "." + "AN_"+oPrefix + replacementID + lahmuSuffix+ "_" + animationParts[1]
        else:
            searchString = "/Game/Design/Character/"+oFPrefix+"/"+oPrefix + replacementID + "_" + replacementName + "/Anim/" + "AN_"+oPrefix + replacementID+ lahmuSuffix + "_" + animation+ "." + "AN_"+oPrefix + replacementID+ lahmuSuffix + "_" + animation
        if searchString in string: #Is the Animation the one in the current string
            if '/' in replacementAnim: #Is new Animation in Subfolder?
                animationParts = replacementAnim.split("/")
                replacementString = "/Game/Design/Character/"+nFPrefix+"/"+nPrefix + replacementID + "_" + replacementName + "/Anim/" + animationParts[0] + "/" + "AN_"+nPrefix + replacementID+ lahmuSuffix + "_" + animationParts[1]+ "." + "AN_"+nPrefix + replacementID+ lahmuSuffix + "_" + animationParts[1]
            else:
                replacementString = "/Game/Design/Character/"+nFPrefix+"/"+nPrefix + replacementID + "_" + replacementName + "/Anim/" + "AN_"+nPrefix + replacementID+ lahmuSuffix + "_" + replacementAnim+ "." + "AN_"+nPrefix + replacementID + lahmuSuffix+ "_" + replacementAnim
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
        relativeScale3D = next(data['Value'] for data in hitGenExport['Data'] if data['Name'] == 'RelativeScale3D')
        vectorValues = relativeScale3D[0]['Value']
        vectorValues['X'] *= scale
        vectorValues['Y'] *= scale
        vectorValues['Z'] *= scale

    except StopIteration:
        print("Could not perform scale update on EventHitGen for: " + script)
    
    file.updateFileWithJson(file.json)
    
