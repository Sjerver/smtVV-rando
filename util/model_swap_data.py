from base_classes.message import Demon_Sync
from pathlib import Path
from collections import defaultdict
import re

class Anim_Sync():
    def __init__(self,ind, sync=None):
        self.ind = ind
        self.sync = ind
        if sync:
            self.sync = sync

class Model_Swap_Demon():
    def __init__(self,originalDemonID,replacementID):
        self.originalDemonID = originalDemonID
        self.replacementID = replacementID
        self.oldIDString = None
        self.oldName = None
        self.oldFolderPrefix = DEVIL_PREFIX
        self.oldPrefix = "dev"
        self.oldPrefixVariant = "Dev"
        self.newIDString = None
        self.newName = None
        self.newPrefix = "dev"
        self.newFolderPrefix = DEVIL_PREFIX
        self.newPrefixVariant = "Dev"
        self.classOldFolderPrefix = None
        self.classOldPrefix = None
        self.classNewFolderPrefix = None
        self.classNewPrefix = None
        self.classOldPrefixVariant = None
        self.classNewPrefixVariant = None
        self.lahmuSuffix = None

DEVIL_PREFIX = "/Devil/"
NPC_PREFIX = "/NPC/"

#List of which level umaps event scripts use for their location and sizes
#To find out, look at which MapEventID the Script has in its File and then take a look at map event data
LEVEL_UASSETS = {
    'MM_M061_EM1630': 'LV_EventMission_M061',
    'MM_M061_EM1631': 'LV_EventMission_M061',
    'MM_M061_EM1640': 'LV_EventMission_M061',
}

#List of events that require updated scaling to trigger events with large demons
#TODO: Maybe change this by getting all possible event hits from the files and using a csv instead
REQUIRES_HIT_UPDATE = [
    'MM_M016_E0885','MM_M038_E2912','MM_M060_Npc609Talk',
    'MM_M063_EM0061','MM_M064_E2512','MM_M064_E2540','MM_M085_E0690','MM_M085_E0730',
    "MM_M064_E2690",
    'MM_M085_E2660','MM_M085_E2688',
    'MM_M088_E0602_Abdiel','MM_M088_E0602_Khons','MM_M088_E0602_Koshimizu','MM_M088_E0602_Vasuki','MM_M088_E0602_Odin','MM_M088_E0602_Zeus',
    'MM_M092_EM101_','MM_M092_EM102_','MM_M092_EM105_1','MM_M092_EM106_','MM_M092_EM110',
    'MM_M016_EM1450','MM_M016_EM1500',
    'MM_M061_EM1782','MM_M061_EM1791','MM_M061_EM2611','MM_M107_EM1824','MM_M107_EM1825_Dev651','MM_M107_EM1825_Hit','MM_M061_EM1020','MM_M061_EM1030',
    'MM_M035_EM1480','MM_M035_EM1491','MM_M036_EM1490','MM_M036_EM1481',
    'MM_M061_EM1041','MM_M061_EM1050_New','MM_M061_EM1360','MM_M061_EM1630','MM_M061_EM1640', 'MM_M061_EM2190','MM_M061_EM2531',
    'MM_M061_EM0151','MM_M061_EM0152','MM_M061_EM0154','MM_M061_EM1710','MM_M061_EM2240','MM_M061_EM2245',
    'MM_M062_EM1160','MM_M062_EM1161_A','MM_M062_EM1181','MM_M062_EM1331','MM_M062_EM1340','MM_M062_EM1401','MM_M062_EM1650','MM_M062_EM1660','MM_M062_EM2090','MM_M062_EM2110_Enemy','MM_M062_EM0051','MM_M062_E2305_2','MM_M062_EM2430',
    'MM_M063_EM1210','MM_M063_EM1250','MM_M063_EM1260','MM_M063_EM1291','MM_M063_EM1350','MM_M063_EM1670','MM_M063_EM1680','MM_M063_EM2170',
    'MM_M064_EM1260','MM_M064_EM1261','MM_M064_EM1291','MM_M064_EM2130','MM_M064_EM2270','MM_M064_EM2280','MM_M064_EM2310','MM_M064_EM2320','MM_M064_EM2400','MM_M064_EM2402','MM_M064_EM2552','MM_M064_EM2621',
    'MM_M060_EM1370','MM_M060_EM1381','MM_M060_EM1390','MM_M060_EM1390_NewRoute','MM_M060_EM1420','MM_M060_EM1441','MM_M060_EM1600','MM_M060_EM1601','MM_M060_EM1602','MM_M060_EM1690','MM_M060_EM1700','MM_M060_EM2630',
    'BP_es035_m063_01','BP_es152_m062_01','BP_es152_m063_01','BP_es416_m060_01','BP_es618_m060_01','BP_es418_m063_01','BP_es618_m063_01',
    'esNPC_em1650_01','esNPC_em1650_02','esNPC_em1650_03','esNPC_em1650_04','esNPC_em1650_05','esNPC_em1650_06','esNPC_em0150_02','esNPC_em0150_03','esNPC_em0150_04','esNPC_em0150_05','esNPC_em0150_06','MM_M061_EM1631',
]

OVERLAPPING_SCRIPTS = [
    'esNPC_em1650_01','esNPC_em1650_02','esNPC_em1650_03','esNPC_em1650_04','esNPC_em1650_05','esNPC_em1650_06','esNPC_em0150_02','esNPC_em0150_03','esNPC_em0150_04','esNPC_em0150_05','esNPC_em0150_06','MM_M061_EM1631',
]

EVENT_CUTSCENES = {
    'LV_E0180': [Demon_Sync(431), Demon_Sync(38, isNavi=True)], #UMAP Triple Preta Cutscene
    'LV_E0181': [Demon_Sync(38, isNavi=True)], #UMAP Post Triple Preta Cutscene
    'LV_E0310': [Demon_Sync(-432,432)], #Hydra Cutscene
    'LV_E0330': [Demon_Sync(75,550),Demon_Sync(435)], #UMAP Snake Nuwa Pre-fight Cutscene (Nuwa (CoV w/Yakumo), Snake Nuwa)
    'LV_E0340': [Demon_Sync(465),Demon_Sync(75,550),Demon_Sync(435)], #UMAP Snake Nuwa Post-fight Cutscene (Yakumo, Nuwa (CoV w/Yakumo), Snake Nuwa)
    'LV_E0350': [Demon_Sync(467)], #UMAP Meeting Abdiel Cutscene
    'LV_E0375': [Demon_Sync(152)], #UMAP Hayataro in Beginning of Shinagawa Cutscene
    'LV_E0379': [Demon_Sync(451)], #UMAP Fionn 1 Cutscene
    
    'LV_E0431': [Demon_Sync(236,441)], #UMAP Lahmu 1 Post-fight dialogue (Lahmu) 
    'LV_E0432': [Demon_Sync(236,441)], #UMAP Lahmu 1 Pre-fight dialogue (Lahmu) 
    'LV_E0470': [Demon_Sync(236,441)], #UMAP Lahmu meets Sayori (Lahmu)
    'LV_E0473': [Demon_Sync(152)], #UMAP Meeting Hayataro creation (Hayataro)
    'LV_E0480': [Demon_Sync(236,441)], #UMAP Sahori kills her bullies (Lahmu) 
    'LV_E0490': [Demon_Sync(236,452)], #UMAP Final Lahmu Pre-fight dialogue 
    'LV_E0530': [Demon_Sync(467),Demon_Sync(-617,528)], #Pre-summit Abdiel/Koshimitzu talk 
    'LV_E0580': [Demon_Sync(467)], #Meeting Abdiel in Chiyoda (Abdiel)
    'LV_E0595': [Demon_Sync(454)], #Surt Pre-fight
    'LV_E0598': [Demon_Sync(455)], #Ishtar Pre-fight
    'LV_E0600': [Demon_Sync(469),Demon_Sync(470),Demon_Sync(468),Demon_Sync(467),Demon_Sync(516),Demon_Sync(-617,528)], #First Bethel summit cutscene (Zeus, Odin, Vasuki, Abdiel, Khonsu, Koshimizu as Tsukuyomi)
    'LV_E0603': [Demon_Sync(469),Demon_Sync(470),Demon_Sync(468),Demon_Sync(467),Demon_Sync(516),Demon_Sync(-617,528)], #Abdiel pre-fight summit cutscene (Zeus, Odin, Vasuki, Abdiel, Khonsu, Koshimizu as Tsukuyomi)
    'LV_E0604': [Demon_Sync(469),Demon_Sync(470),Demon_Sync(468),Demon_Sync(467),Demon_Sync(516),Demon_Sync(-617,528)], #Abdiel post-fight summit cutscene (Zeus, Odin, Vasuki, Abdiel, Khonsu, Koshimizu as Tsukuyomi)
    'LV_E0620': [Demon_Sync(465), Demon_Sync(75, 435)], #Yakumo pre-fight (Yakumo, Nuwa 1)
    'LV_E0630': [Demon_Sync(467)], #Abdiel dialogue before DKC (Abdiel) 
    'LV_E0660': [Demon_Sync(82,463)], #UMAP Arioch Cutscene
    'LV_E0736': [Demon_Sync(467)],#Dazai/Abdiel talk after summit
    'LV_E0750': [Demon_Sync(365)], #Tao reveals herself as goddes in CoC (Tao Panagia)
    'LV_E0760': [Demon_Sync(365)], #Tao talking about area 4 (Tao Panagia)
    'LV_E0830': [Demon_Sync(365)], #Top floor of Empyrean Warning (Tao Panagia)
    'LV_E0775': [Demon_Sync(468)], #UMAP Vasuki Cutscene
    'LV_E0785': [Demon_Sync(469)], #UMAP Zeus CoC Cutscene
    'LV_E0805': [Demon_Sync(470)], #UMAP Odin CoC Cutscene
    'LV_E0841': [Demon_Sync(-617,528)], #Chaos rep overview pre-empyrean (Tsukuyomi) 
    'LV_E0842': [Demon_Sync(240, 467)], #Law rep overview pre-empyrean (Abdiel (Summit Boss)) 
    'LV_E0850': [Demon_Sync(240, 467),Demon_Sync(264, 525),Demon_Sync(75, 520),Demon_Sync(465),Demon_Sync(-617,528),Demon_Sync(365)], #Argument before Empyrean (Abdiel as Summit Boss, Abdiel Fallen, Nuwa as Naho, Yakumo, Tsukuyomi, Tao(Panagia))
    'LV_E0860': [Demon_Sync(365)], #Tao upon entering Empyrean (Tao Panagia)
    'LV_E0870': [Demon_Sync(264, 525)], #Joining Dazai in Empyrean (Abdiel)
    'LV_E0880': [Demon_Sync(-617,528),Demon_Sync(152)], #Joining Tsukuyomi in Empyrean (Tsukuyomi, Hayataro)
    'LV_E0900': [Demon_Sync(264, 525),Demon_Sync(528)],#Dazai/Abdiel lose to Tsukuyomi (koshimizu form unchanged) 
    'LV_E0905': [Demon_Sync(528)],#Tsukuyomi death scene? (koshimizu form unchanged) 
    'LV_E0910': [Demon_Sync(467),Demon_Sync(525),Demon_Sync(-617,528)],#Tsukuyomi loses to Dazai/Abdiel (Abdiel, Tsukuyomi) (koshimizu form unchanged) 
    'LV_E0915': [Demon_Sync(467),Demon_Sync(525)],#Abdiel death Scene? 
    'LV_E0920': [Demon_Sync(467),Demon_Sync(525),Demon_Sync(465),Demon_Sync(75, 520)], #Yakumo/Nuwa loses to Dazai/Abdiel (Abdiel, Yakumo, Nuwa)
    'LV_E0930': [Demon_Sync(75, 520)],#Nuwa true ending dialogue after Abdiel (Nuwa)
    'LV_E0940': [Demon_Sync(520),Demon_Sync(75, 435),Demon_Sync(465)],#Nahobino Nuwa pre-fight dialogue (Yakumo, Nuwa as Nuwa 1 AND Nahobino Form)
    'LV_E0945': [Demon_Sync(520),Demon_Sync(75, 435),Demon_Sync(465)],#Nahobino Nuwa post-fight dialogue (Yakumo, Nuwa as Nuwa 1 AND Nahobino Form)
    'LV_E0955': [Demon_Sync(-617,528)], #Tsukuyomi death scene (TNE?) (as koshimizu)
    'LV_E0957': [Demon_Sync(264, 525)], #Abdiel death scene (TNE?) (Fallen ABdiel)
    'LV_E0960': [Demon_Sync(528)], #Tsukuyomi neutral route pre-fight dialogue (Tsukuyomi) (no koshimizu change)
    'LV_E0965': [Demon_Sync(528)], #Tsukuyomi neutral route post-fight dialogue (Tsukuyomi)
    'LV_E0975': [Demon_Sync(240, 525)], #Abdiel is in here? as her first form
    #'LV_E1000': [Demon_Sync(-500, 537)],#Lucifer pre-fight (Blue one)(Does not do anything, no idea how the luci model appears here)
    'LV_E1010': [Demon_Sync(529, 537)],#Lucifer pre-fight
    'LV_E1015': [Demon_Sync(529, 537)],#Lucifer pre-fight II

    'LV_E1100': [Demon_Sync(934)],#Demi-fiend Pre Fight I think
   
    'LV_E2000': [Demon_Sync(1157)], #Creation choice cutscene (Yoko)
    'LV_E2010': [Demon_Sync(552),Demon_Sync(561,1150),Demon_Sync(1157)],#Labolas 1 pre-fight (Labolas, Yuzuru, Yoko)
    'LV_E2015': [Demon_Sync(552),Demon_Sync(561,1150),Demon_Sync(1157)],#Labolas 1 post-fight (Labolas, Yuzuru, Yoko)
    'LV_E2020': [Demon_Sync(393, 553),Demon_Sync(1157)],#Naamah pre-fight dialogue 1 (Naamah,Yoko)
    'LV_E2022': [Demon_Sync(393, 553),Demon_Sync(1157)],#Naamah pre-fight dialogue 2 (Naamah,Yoko)
    'LV_E2025': [Demon_Sync(393, 553),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(-395, 569),Demon_Sync(1157)],#Naamah post-fight dialogue (Naamah,Agrat,Eisheth,Lilith,Yoko)
    'LV_E2029': [Demon_Sync(567),Demon_Sync(75,550),Demon_Sync(435),Demon_Sync(1157)],#Nuwa post-fight dialogue vengeance (Yoko)
    'LV_E2030': [Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1157)],#Dazai in diet building vengeance (Dazai, Yuzuru,Yoko)
    'LV_E2035': [Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1157)],#Returning to Tokyo from area 1 vengeance (Dazai, Yuzuru,Yoko)
    'LV_E2040': [Demon_Sync(240, 564),Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)],#Meeting Abdiel vengeance (Abdiel, Dazai, Yuzuru, Tao,Yoko)
    'LV_E2043': [Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)],#Tao meeting after area 1 vengeance (Dazai,Yuzuru, Tao,Yoko)
    'LV_E2051': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(391, 569)],#Qadistu Dream (Naamah II ,Agrat,Eisheth,Lilith)
    'LV_E2060': [Demon_Sync(1152),Demon_Sync(1157)], #Yoko joining as transfer student (Tao,Yoko)
    'LV_E2130': [Demon_Sync(1152),Demon_Sync(1157)], #Tao on dorm roof Vengenace (Tao,Yoko)
    'LV_E2160': [Demon_Sync(393, 554),Demon_Sync(555)], #Labolas 2 pre-fight dialogue (Naamah,Labolas)
    'LV_E2164': [Demon_Sync(393, 554)],#Labolas 2 post-fight dialogue (Naamah)
    'LV_E2180': [Demon_Sync(1157)], #Yoko in front of school invasion
    'LV_E2210': [Demon_Sync(152, 562), Demon_Sync(561,1150),Demon_Sync(-606,1152),Demon_Sync(1152),Demon_Sync(1157)],#Meeting Hayataro vengeance (Hayataro, Yuzuru, Tao,Yoko)
    'LV_E2250': [Demon_Sync(236,556),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Vengeance Lahmu pre-fight dialogue (Lahmu, Tao,Yoko)
    'LV_E2255': [Demon_Sync(236,556),Demon_Sync(391, 569),Demon_Sync(1152),Demon_Sync(1157)], #Lilith kills Sahori (Lahmu, Lilith, Tao)
    'LV_E2260': [Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)], #Dazai/Yuzuru first argument (Dazai,Yuzuru, Tao, Yoko)
    'LV_E2270': [Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(152, 562),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Arriving in area 2 vengeance (Dazai,Yuzuru, Hayataro, Tao,Yoko)
    'LV_E2290': [Demon_Sync(394, 559),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)],#Eisheth pre-fight dialogue (Eisheth, Tao, Yoko)
    #'LV_E2295': [Demon_Sync(394, 559),Demon_Sync(1152)], #Eisheth post-fight (Tao) #TODO:Test (has no LV file???)
    'LV_E2297': [Demon_Sync(451),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)],#Fionn pre(?)-fight vengeance (Tao,Yoko)
    #'LV_E2306': [Demon_Sync(1157)], #Unknown (Yoko)
    'LV_E2310': [Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)],#Dazai loses to Eisheth (Dazai, Tao,Yoko)
    'LV_E2320': [Demon_Sync(561),Demon_Sync(394, 559),Demon_Sync(152, 562),Demon_Sync(1152),Demon_Sync(1157)],#Yuzuru pre-fight dialogue (Yuzuru, Eisheth, Hayataro, Tao,Yoko)
    'LV_E2325': [Demon_Sync(561),Demon_Sync(394, 559),Demon_Sync(152, 562),Demon_Sync(1151),Demon_Sync(-396, 568),Demon_Sync(7,566),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Yuzuru post-fight dialogue (Yuzuru,Eisheth,Hayataro, Dazai, Agrat, Khonsu, Tao,Yoko)
    'LV_E2330': [Demon_Sync(1151),Demon_Sync(561), Demon_Sync(57, isNavi=True),Demon_Sync(1152),Demon_Sync(1157)],#Discovering Salted Village (Dazai, Yuzuru, navi Pyro Jack,Tao,Yoko)
    'LV_E2440': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(391, 569)], #Qadistu Dream ??? (Naamah II ,Agrat,Eisheth,Lilith)
    'LV_E2500': [Demon_Sync(1152),Demon_Sync(1157)], #After Hayataro has location of crow (Tao,Yoko)
    #'LV_E2514': [Demon_Sync(1152),Demon_Sync(1157)], #Powers detect intruders (Tao,Yoko) #TODO: Has no LV file??
    'LV_E2519': [Demon_Sync(550), Demon_Sync(567),Demon_Sync(1152),Demon_Sync(1157)],#First Nuwa/Yakumo scene in Shinjuku(Nuwa, Yakumo, Tao,Yoko)
    'LV_E2560': [Demon_Sync(550), Demon_Sync(567),Demon_Sync(1152),Demon_Sync(1157)],#Nuwa/Yakumo talk at Mastema's hill 1(Nuwa, Yakumo, Tao, Yoko)
    'LV_E2605': [Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)],#Dazai and Yuzuru become friends (Dazai, Yuzuru, Tao, Yoko)
    'LV_E2623': [Demon_Sync(7,566),Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)], #Khonsu pre-fight dialogue vengeance part 2 (Khonsu, Yuzuru, Dazai, Tao, Yoko)
    'LV_E2633': [Demon_Sync(1157)], #Yoko dialogue if demons can be trusted (Yoko)
    'LV_E2640': [Demon_Sync(596),Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(1157)],#Arriving at Mastema's hill (Mastema,Dazai,Tao,Yoko)
    'LV_E2643': [Demon_Sync(596),Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(1157)],#Dazai turns to salt (Mastema,Dazai,Tao,Yoko)
    'LV_E2645': [Demon_Sync(596),Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(1157)], #Mastema brainwashes Dazai (Mastema, Dazai,Tao,Yoko)
    'LV_E2648': [Demon_Sync(393, 554),Demon_Sync(1152),Demon_Sync(1157)],#Naamah in Shinjuku (Naamah, Tao, Yoko)
    'LV_E2680': [Demon_Sync(561,1150),Demon_Sync(567), Demon_Sync(550),Demon_Sync(1152),Demon_Sync(1157)],#Yakumo COV pre-fight dialogue (Yuzuru, Yakumo, Nuwa, Tao, Yoko)
    'LV_E2685': [Demon_Sync(561,1150),Demon_Sync(567), Demon_Sync(550),Demon_Sync(1152),Demon_Sync(1157)],#Yakumo COV post-fight dialogue (Yuzuru, Yakumo, Nuwa, Tao,Yoko)
    'LV_E2700': [Demon_Sync(-396,568),Demon_Sync(1152),Demon_Sync(1157)],#Meeting Agrat (Agrat(Copy), Tao,Yoko)
    'LV_E2703': [Demon_Sync(568),Demon_Sync(1152),Demon_Sync(1157)],#Agrat pre-fight (Agrat, Tao, Yoko)
    'LV_E2705': [Demon_Sync(568),Demon_Sync(394, 559),Demon_Sync(393, 554),Demon_Sync(1152),Demon_Sync(1157)],#Agrat post-fight dialogue (Agrat, Eisheth, Naamah, Tao, Yoko)
    'LV_E2710': [Demon_Sync(1152),Demon_Sync(1157)], #Arriving at Government Building (Tao, Yoko)
    'LV_E2713': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(-395, 569),Demon_Sync(1152),Demon_Sync(1157)],#Lilith pre-fight dialogue (Naamah II ,Agrat,Eisheth,Lilith, Tao,Yoko)
    'LV_E2717': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(-395, 569),Demon_Sync(1152),Demon_Sync(1157)],#Lilith post-fight dialogue (Naamah II ,Agrat,Eisheth,Lilith,Tao,Yoko)
    'LV_E2720': [Demon_Sync(596),Demon_Sync(-459,565),Demon_Sync(550),Demon_Sync(564),Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(550)],#Timat Unleashed (Mastema,Tiamat,Nuwa,Abdiel,Dazai,Yuzuru,Yakumo)
    'LV_E2730': [Demon_Sync(1152)], #After being killed by Lilith (Tao)
    'LV_E2735': [Demon_Sync(1152)], #Tao reviving Nahobino (Tao)
    'LV_E2740': [Demon_Sync(578),Demon_Sync(561,1150),Demon_Sync(564)],#Dazai hat cutscene vengeance (Dazai (Hatless), Yuzuru, Abdiel) 
    'LV_E2920': [Demon_Sync(564),Demon_Sync(1157)], #Abdiel in Shakan pre-fight dialogue (Abdiel, Yoko)
    'LV_E2970': [Demon_Sync(1152),Demon_Sync(365)], #Tao at dorm roof after Shakan (Tao(Guest), Tao(Panagia))
    'LV_E2980': [Demon_Sync(365)], #Panagia Tao talking to Koshimizu (Tao Panagia)
    'LV_E3000': [Demon_Sync(365)], #Tao talking about keys (Tao Panagia)
    'LV_E3040': [Demon_Sync(567)], #Yakumo in Jojozi (Yakumo)
    'LV_E3100': [Demon_Sync(483),Demon_Sync(468)], #Beelzebub pre-fight dialogue(Beelzebub, Vasuki)
    'LV_E3120': [Demon_Sync(482),Demon_Sync(481)], #Zeus + Odin pre-fight dialogue (Odin,Zeus)
    'LV_E3250': [Demon_Sync(365)], #Tao at top floor of TOE (Tao Panagia)
    'LV_E3300': [Demon_Sync(578),Demon_Sync(577),Demon_Sync(365)], #Dazai pre-fight dialogue (Dazai, Abdiel, Tao(Panagia))
    'LV_E3310': [Demon_Sync(578),Demon_Sync(577),Demon_Sync(365)],#Dazai post-fight dialogue (Dazai, Abdiel, Tao(Panagia))
    'LV_E3320': [Demon_Sync(365)], #Tao upon entering Empyrean (Tao Panagia)
    'LV_E3330': [Demon_Sync(365),Demon_Sync(366)], #Tao at the Throne of Creation when Yoko shows up (Tao Panagia, Yoko Panagia)
    'LV_E3340': [Demon_Sync(365),Demon_Sync(366)], #Siding with Tao (Tao Panagia, Yoko Panagia)
    'LV_E3350': [Demon_Sync(-459,565),Demon_Sync(365),Demon_Sync(366)], #Yoko uses Tiamat on you (Tiamat, Tao Panagia, Yoko Panagia)
    'LV_E3352': [Demon_Sync(-459,565),Demon_Sync(365),Demon_Sync(366)], #Tiamat post-fight (Tiamat, Tao Panagia, Yoko Panagia)
    'LV_E3355': [Demon_Sync(597),Demon_Sync(365),Demon_Sync(366)],#Tehom pre-fight dialogue (Tehom, Tao Panagia, Yoko Panagia)
    'LV_E3358': [Demon_Sync(597),Demon_Sync(365)],#Tehom post?-fight dialogue (Tehom, Tao Panagia)
    'LV_E3360': [Demon_Sync(365)], #CoV Law Ending (Tao Panagia)
    'LV_E3390': [Demon_Sync(596),Demon_Sync(1157)],#Siding with Yoko (Mastema, Yoko)
    'LV_E3400': [Demon_Sync(596),Demon_Sync(365),Demon_Sync(366)],#Siding with Yoko (Mastema, Tao Panagia, Yoko Panagia)
    'LV_E3410': [Demon_Sync(596),Demon_Sync(-459,565),Demon_Sync(366)],#Mastema uses Tiamat on you (Mastema,Tiamat, Yoko Panagia)
    'LV_E3415': [Demon_Sync(596),Demon_Sync(-459,565),Demon_Sync(366)],#Tiamat post-fight chaos (Mastema,Tiamat, Yoko Panagia)
    'LV_E3420': [Demon_Sync(596),Demon_Sync(366)],#Mastema pre-fight dialogue (Mastema, Yoko Panagia)
    'LV_E3425': [Demon_Sync(596),Demon_Sync(366)],#Mastema post-fight dialogue (Mastema,Yoko Panagia)
    'LV_E3450': [Demon_Sync(366)], #Amitaba calling for world recreation Yoko Side (Yoko Panagia)
    'LV_E3480': [Demon_Sync(391, 569),Demon_Sync(1157)], #Some CoV Chaos Ending Cutscene (Lilith, Yoko)

}   

#Script files for events and what demon models need to be updated in htem
#Demon_Sync(demonID in file, if different from demonID in file: demonID to take replacement from)
EVENT_SCRIPT_MODELS = {
    #Battle Event
    'EB_GAKUEN_LAHMU2_BattleStart': [Demon_Sync(1152),Demon_Sync(1157)], #CoV Lahmu Battle Event (Tao,Yoko)
    #Initial & Mainmission M061 (Minato)
    'EM_M061_DevilTalk': [Demon_Sync(59)], #Talk Tutorial (Pixie)
    'MM_M061_E2610' : [Demon_Sync(193,579),Demon_Sync(561,1150),Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(1157)], #CoV Isis Event Bethel Egypt (Isis, Yuzuru,Dazai, Tao,Yoko)
    'MM_M061_E2620': [Demon_Sync(561,1150),Demon_Sync(1151),Demon_Sync(7,566),Demon_Sync(1152),Demon_Sync(1157)], #CoV Khonsu Event Bethel Egypt (Khonsu,Yuzuru,Dazai, Tao,Yoko)
    'MM_M061_E2625_Direct': [Demon_Sync(193,579),Demon_Sync(7,566),Demon_Sync(561,1150),Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(1157)], #CoV Khonsu Event Post Fight Bethel Egypt (Isis,Khonsu,Yuzuru,Dazai,Tao,Yoko)
    'MM_M061_EM0026': [Demon_Sync(1157)], #After beating Hydra (Yoko)
    'MM_M061_EM0181': [Demon_Sync(38, isNavi=True)], #Amanozako gives you a bead
    'MM_M061_EM0182': [Demon_Sync(38, isNavi=True)], #Amanozako becomes your navigator
    'EM_M061_Q0019': [Demon_Sync(38, isNavi=True)], #Amanozako leaves in area 1
    'EM_M061_TutorialNavi02': [Demon_Sync(38, isNavi=True),Demon_Sync(1157)], #Amanazako first partner spot (Yoko)
    'EM_M061_TutorialGuest2': [Demon_Sync(1157)], #Yoko dialogue after Glasya-Labolas (Yoko)
    'MM_M200_EN0100': [Demon_Sync(1157)], #Yoko after Naamah fight (Yoko)
    #Mainmission M016 (Empyrean)
    'MM_M016_E0885': [Demon_Sync(152)], #CoC Chaos Route Empyrean Hayataro Joins After Stock is Full (Hayataro)
    'MM_M016_E0885_Direct': [Demon_Sync(152)], #CoC Chaos Route Empyrean Hayataro Joins Stock is Full so wait (Hayataro)
    'MM_M016_E0890_Direct': [Demon_Sync(365)], #Tao rewarding you in CoC for picking an ending according to your alignment (Tao Panagia)
    'MM_M016_E0891': [Demon_Sync(249,471)], #Empyrean Melchizedek
    'MM_M016_E0892': [Demon_Sync(244,472)], #Empyrean Sraosha
    'MM_M016_E0893': [Demon_Sync(198,473)], #Empyrean Alilat
    'MM_M016_E0906': [Demon_Sync(365)], #Some Tao dialogue (Tao Panagaia)
    #Mainmission M035 & 36 (Temple of Eternity & DKC)
    'MM_M035_E0825': [Demon_Sync(241,477)], #Temple of Eternity Metatron
    'MM_M036_E0644': [Demon_Sync(182,466)], #DKC Pre Chernobog
    'MM_M036_E0650': [Demon_Sync(240,467)], #DKC Abdiel & Dazai Event
    'MM_M036_E0670': [Demon_Sync(465),Demon_Sync(82,463),Demon_Sync(240,467),Demon_Sync(75,435)], #DKC Post Arioch(Yakumo,Arioch,Abdiel)
    'MM_M035_E3220': [Demon_Sync(365)], #Temple of Eternity Tao Scene before entering Empyrean (Tao Panagia)
    #Mainmission M038 (Shakan)
    'MM_M038_E2912': [Demon_Sync(256,484),Demon_Sync(255,485)], #Shakan Dark Block Bros
    'MM_M038_E2917': [Demon_Sync(260,486)], #Shakan Cherub
    'MM_M038_E2930_Direct': [Demon_Sync(240,564)], #Shakan Abdiel Post Fight
    #Mainmission M060 (Taito)
    'MM_M060_E0762': [Demon_Sync(75,520),Demon_Sync(465)], #Nuwa in area 4 at the gate (Uses Replacement for Nahobino Nuwa, Yakumo)
    'MM_M060_E0763': [Demon_Sync(365)], #Tao joining you in area 4 creation (Tao Panagia)
    'MM_M060_E0764': [Demon_Sync(365)], #Tao joining you in area 4 creation (If slots were filled previously) (Tao Panagia)
    'MM_M060_E0778': [Demon_Sync(468),Demon_Sync(37,878),Demon_Sync(365)], #Vasuki Post Fight Event (Vasuki, Kurama Tengu, Tao (Panagia))
    'MM_M060_E0785': [Demon_Sync(8,469)], #CoC Taito Zeus Appears
    'MM_M060_E0790': [Demon_Sync(8,469),Demon_Sync(37,878),Demon_Sync(365)],#CoC Taito Zeus PostFight (Zeus, Kurama Tengu, Tao (Panagia))
    'MM_M060_E0810': [Demon_Sync(9,470),Demon_Sync(37,878),Demon_Sync(365)],#CoC Odin PostFight (Odin, Kurama Tengu, Tao (Panagia))
    'MM_M060_E0820': [Demon_Sync(365)], # Tao before entering Temple of eternity (Tao Panagia)
    'MM_M060_E3001_Direct': [Demon_Sync(365)], #Tao joining you in area 4 vengeance (Tao Panagia)
    'MM_M060_E3002': [Demon_Sync(365)], #Tao joining you in area 4 vengeance (If slots were filled previously) (Tao Panagia)
    'MM_M060_E3010': [Demon_Sync(465,567),Demon_Sync(365)], #Yakumo in area 4 vengeance (Yakumo, Tao (Panagia))
    'MM_M060_E3020': [Demon_Sync(465,567),Demon_Sync(365)], #Yakumo in area 4 vengeance part 2 (Yakumo, Tao (Panagia))
    'MM_M060_E3110_Direct': [Demon_Sync(81,483),Demon_Sync(365)], #CoV Beelzebub (Beelzebub, Tao (Panagia))
    'MM_M060_E3130_Direct': [Demon_Sync(482),Demon_Sync(481),Demon_Sync(365)], #CoV Zeus + Odin (Zeus, Odin, Tao (Panagia))
    'MM_M060_E3200': [Demon_Sync(365)], #Tao before entering Temple of eternity vengeance (Tao Panagia)
    'MM_M060_Npc609Talk': [Demon_Sync(152)], #CoC Yuzuru Hayataro NPC Event? (Hayataro)
    'MM_M060_EM0140': [Demon_Sync(38, isNavi=True),Demon_Sync(365)], #Amanozako rejoins in area 4 creation (Amanozako, Tao (Panagia)) #Tao did not work here????
    #Mainmission M062 (Shinagawa)  
    'MM_M062_EM0050': [Demon_Sync(57, isNavi=True)], #Golden Apple Quest part 1 creation (Pyro Jack)
    'MM_M062_EM0051': [Demon_Sync(23, isNavi=True)], #Idun in Golden Apple Quest creation (Idun)
    'MM_M062_EM0120_Direct': [Demon_Sync(38, isNavi=True)], #Amanozako rejoins in area 2
    'MM_M062_EM0122': [Demon_Sync(38, isNavi=True),Demon_Sync(1157),Demon_Sync(-606,1152)], #Amanozako car event (Amanozako, Yoko,Tao (Guest))
    'MM_M062_EM0123': [Demon_Sync(38, isNavi=True),Demon_Sync(1157),Demon_Sync(-606,1152)], #Amanozako railroad event (Amanozako, Yoko,Tao(Guest))
    'MM_M062_EM0124': [Demon_Sync(38, isNavi=True),Demon_Sync(1157),Demon_Sync(-606,1152)], #Amanozako container event (Amanozako, Yoko,Tao(Guest))
    'MM_M062_EM0125': [Demon_Sync(38, isNavi=True)], #Amanozako leaves in area 2
    'MM_M062_E0378': [Demon_Sync(467)], #Dazai/Abdiel talk in area 2 creation (Abdiel)
    'MM_M062_E0380': [Demon_Sync(35,451)], #Fionn 1 Post-fight (Fionn)
    'MM_M062_E0492': [Demon_Sync(453)], #Final Lahmu (Lahmu Phase 2)
    'MM_M062_EM0041': [Demon_Sync(450)], #Loup-garous Event
    'MM_M062_E2271_Direct': [Demon_Sync(-606,1152),Demon_Sync(1157)], #Arriving in area 2 vengeance (Tao, Yoko)
    'MM_M062_E2272_Hit': [Demon_Sync(-606,1152),Demon_Sync(1157)], #Sensing other students Vengeance (Tao, Yoko)
    'MM_M062_E2275': [Demon_Sync(564),Demon_Sync(1151)], #Dazai/Abdiel talk in area 2 vengeance (Abdiel,Dazai)
    'MM_M062_E228x': [Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Rescuing Students Vengeance (Tao, Yoko)
    'MM_M062_E2295_Direct': [Demon_Sync(559),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Eisheth pre-fight (Eisheth, Tao,Yoko)
    'MM_M062_E2298_Direct': [Demon_Sync(451),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Fionn post-fight Vengeance (Fionn, Tao, Yoko)
    'MM_M062_E2300': [Demon_Sync(1151)], #Dazai Pre-Blocker Vengeance
    'MM_M062_E2302': [Demon_Sync(561,1150),Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Arriving in fairy village vengeance (Yuzuru,Dazai,Tao,Yoko)
    'MM_M062_E2305': [Demon_Sync(57, isNavi=True),Demon_Sync(-606,1152),Demon_Sync(1157)], #Golden Apple Quest part 1 vengeance (Pyro Jack, Tao(Bag),Yoko)
    'MM_M062_E2305_2': [Demon_Sync(23, isNavi=True),Demon_Sync(-606,1152),Demon_Sync(1157)], #Idun in Golden Apple Quest vengeance (Idun, Tao(Bag),Yoko)
    'MM_M062_E2312_Direct': [Demon_Sync(-606,1152),Demon_Sync(1157)], #After Dazai reporting Miyazu's Capture (Tao(Bag),Yoko)
    'MM_M062_E2326_Direct': [Demon_Sync(57, isNavi=True),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Dialogue when fairy village is salted (Pyro Jack, Tao, Yoko)
    #Mainmission M063 (Chiyoda)
    'MM_M063_E0625': [Demon_Sync(465),Demon_Sync(75,435)], #Yakumo post-fight Chiyoda (Yakumo, Nuwa)
    'MM_M063_EM0061': [Demon_Sync(822),Demon_Sync(823),Demon_Sync(824)], #Hellfire Highway (Okuninushi, Sukuna Hikona, Minakata)
    'MM_M063_EM0070': [Demon_Sync(273, isNavi=True)], #Decarabia in Ishtar Quest (Decarabia)
    'MM_M063_EM0079': [Demon_Sync(455), Demon_Sync(273, isNavi=True)], #Ishtar Post Fight
    'MM_M063_EM0130': [Demon_Sync(38, isNavi=True)], #Amanozako in Chiyoda
    'MM_M063_M0680': [Demon_Sync(467)],#Abdiel celebrates Arioch's death (Abdiel)
    #Mainmission M064 (Shinjuku)
    'MM_M064_E2510_Direct': [Demon_Sync(503),Demon_Sync(1152),Demon_Sync(1157)], #First Power Fight in Shinjuku (Power,Tao,Yoko)
    'MM_M064_E2512': [Demon_Sync(504),Demon_Sync(1152),Demon_Sync(1157)], #Second Power Fight in Shinjuku (PowerII,Tao,Yoko)
    'MM_M064_E2514': [Demon_Sync(505),Demon_Sync(1152),Demon_Sync(1157)], #Powers detecting other intruders (uses Triple Power Fight Replacement,Tao,Yoko)
    'MM_M064_E2516': [Demon_Sync(1152),Demon_Sync(1157)], #Talking to Sandman after seeing Powers (Tao,Yoko)
    'MM_M064_E2520_Direct': [Demon_Sync(550),Demon_Sync(567),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #First Nuwa/Yakumo scene in Shinjuku (Nuwa,Yakumo,Tao,Yoko)
    'MM_M064_E2540': [Demon_Sync(506),Demon_Sync(1152),Demon_Sync(1157)], #Power Gauntlet (uses last Power Fight Replacement,Tao,Yoko)
    'MM_M064_E2550': [Demon_Sync(486),Demon_Sync(1152),Demon_Sync(1157)], #Cherub Blocker in Shinjuku (Cherub,Tao,Yoko)
    'MM_M064_E2560': [Demon_Sync(550),Demon_Sync(567),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Nuwa/Yakumo talk at Mastema's hill (Nuwa,Yakuma,Tao,Yoko)
    'MM_M064_E2562_Direct': [Demon_Sync(550),Demon_Sync(567),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #Nuwa/Yakumo talk at Mastema's hill 2 
    'MM_M064_E2638': [Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(1157)], #Dazai joins to see Mastema 2 (Dazai,Tao,Yoko)
    'MM_M064_E2642_Direct': [Demon_Sync(1151),Demon_Sync(596),Demon_Sync(1152),Demon_Sync(1157)], #Meeting Mastema (Dazai,Mastema,Tao,Yoko)
    'MM_M064_E2644_Direct': [Demon_Sync(596),Demon_Sync(1152),Demon_Sync(1157)], #Dazai got salted (Mastema,Tao,Yoko)
    'MM_M064_E2646_Direct': [Demon_Sync(1152),Demon_Sync(1157)], #Tao/Yoko talking about Angels salting people
    'MM_M064_E2647': [Demon_Sync(38, isNavi=True)], #Amanozako in Shinjuku
    'MM_M064_E2650_Direct': [Demon_Sync(550),Demon_Sync(567),Demon_Sync(1152),Demon_Sync(1157)], #Nuwa/Yakumo talk after seeing Naamah (Nuwa, Yakumo,Tao,Yoko)
    'MM_M064_E2709': [Demon_Sync(1157)], #Yoko asking metaphorial question
    'MM_M064_E2690': [Demon_Sync(486)], #Dead Cherubim
    'MM_M064_E2900': [Demon_Sync(596)],#Mastema sends you to Shakan
    'MM_M064_E2950_Direct': [Demon_Sync(596)],#Mastema after Shakan
    #Mainmission M080 (Dorm Roof) 
    'MM_M080_E2670_Direct': [Demon_Sync(561,1150)], #Yuzuru wants to be a Nahobino
    #Mainmission M082 (School Outside)
    'MM_M082_E3030_Direct': [Demon_Sync(561,1150)],#Yakumo saves a student
    #Mainmission M083 (Shinagawa Station Real Tokyo ) 
    'MM_M083_E2160_Direct': [Demon_Sync(75,435),Demon_Sync(567)], #Labolas 2 post-fight (Yakumo,Nuwa)
    'MM_M083_EM2434': [Demon_Sync(1152),Demon_Sync(1157)], #Salt investigation Station Attendant (Tao;Yoko)
    #Mainmission M085 (Top Room of Tokyo Building whose name I do not remember)
    'MM_M085_E0360': [Demon_Sync(1157)], #Koshimizu meeting after area 1 (Yoko)
    'MM_M085_E0360Simple': [Demon_Sync(1152),Demon_Sync(1157)], #Koshimizu meeting after area 1 (Tao,Yoko) #TODO Does this affect only vengeance? If yes only do Yoko!
    'MM_M085_E0360_Yoko': [Demon_Sync(1157)], #Yoko at Koshimizu meeting after Area 1(Yoko)
    'MM_M085_E0690': [Demon_Sync(-617,528)], #Koshimizu meeting after area 3 CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E0730': [Demon_Sync(-617,528)], #Regarding the war of the gods scene CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E0730_ready': [Demon_Sync(-617,528)], #End of Regarding the war of the gods scene CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E2410': [Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)], #Koshimizu meeting after area 2 CoV (Yuzuru,Tao,Yoko)
    'MM_M085_E2420': [Demon_Sync(561,1150)],#Yuzuru apologizes for attacking you (Yuzuru) (NOT YET TESTED IN GAME)
    'MM_M085_E2435': [Demon_Sync(1152),Demon_Sync(1157)], #Koshimizu meeting during salt investigation (Tao,Yoko)
    'MM_M085_E2445': [Demon_Sync(152,562),Demon_Sync(1157)],#Koshimizu meeting after salt investigation (Hayataro,Yoko) (NOT YET TESTED IN GAME)
    'MM_M085_E2575_Direct': [Demon_Sync(1151),Demon_Sync(-606,1152),Demon_Sync(1157)], #Dazai talk when Miyazu goes to Khonsu (Dazai, Tao(Bag),Yoko) (NOT YET TESTED IN GAME)
    'MM_M085_E2600': [Demon_Sync(1152),Demon_Sync(1157)], #Koshimizu meeting Miyazu kidnapped (Tao,Yoko)
    'MM_M085_E2630_Direct': [Demon_Sync(1151),Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)],#Yuzuru talk after Khonsu incident (Yuzuru, Dazai,Tao,Yoko)
    'MM_M085_E2635_Direct': [Demon_Sync(1151),Demon_Sync(1152),Demon_Sync(1157)], #Dazai joins to see Mastema 1 (Dazai,Tao,Yoko)
    'MM_M085_E2660': [Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)], #Koshimizu meeting before Yakumo fight(Yuzuru,Tao,Yoko)
    'MM_M085_E2688': [Demon_Sync(561,1150),Demon_Sync(1152),Demon_Sync(1157)], #Koshimizu meeting after Yakumo fight (Yuzuru,Tao,Yoko)
    #Mainmission M087 (Shrine Vengeance (Normal Lightning)) (NOT YET TESTED)
    'MM_M087_E2430_Direct': [Demon_Sync(1152),Demon_Sync(1157)], #Salt investigation female researcher (Tao,Yoko)
    'MM_M087_E2431': [Demon_Sync(1152),Demon_Sync(1157)], #Salt investigation Frantic Woman (Tao,Yoko)
    'MM_M087_E2432': [Demon_Sync(1152),Demon_Sync(1157)], #Salt investigation Female Worker (Tao,Yoko)
    'MM_M087_E2433': [Demon_Sync(1152),Demon_Sync(1157)], #Salt investigation concluded (Tao,Yoko)
    'MM_M087_E2450_Direct': [Demon_Sync(1151)],#Dazai goes to Chiyoda 
    'MM_M087_E2490': [Demon_Sync(1152),Demon_Sync(1157)], #Tao wants to go to Shinjuku (Tao,Yoko)
    #Mainmission M088 (Summit)
    'MM_M088_E0602_Abdiel': [Demon_Sync(467)], #Summmit (Abdiel)
    'MM_M088_E0602_Khons': [Demon_Sync(516)], #Summmit (Khonsu)
    'MM_M088_E0602_Koshimizu': [Demon_Sync(-617,528)], #Summmit (Koshimizu as Tsukuyomi Replacement)
    'MM_M088_E0602_Vasuki': [Demon_Sync(468)], #Summmit (Vasuki)
    'MM_M088_E0602_Odin': [Demon_Sync(470)], #Summmit (Odin)
    'MM_M088_E0602_Zeus': [Demon_Sync(469)], #Summmit (Zeus)
    #Mainmission M092 (School Attacked)
    'MM_M092_E0476': [Demon_Sync(1157),Demon_Sync(1152)], #Yoko after Dazai scene (Tao,Yoko)
    'MM_M092_EM101_': [Demon_Sync(446)], #School Oni [63] (Down in the Direction where Jack is looking)
    'MM_M092_EM102_': [Demon_Sync(488),Demon_Sync(491),Demon_Sync(-606,1152),Demon_Sync(1157)], #School Andras + Rakshasa [56] (First Floor Hallway) (Tao with Bag,Yoko)
    'MM_M092_EM104': [Demon_Sync(496),Demon_Sync(1152),Demon_Sync(-606,1152),Demon_Sync(1157)], #School Incubus [58] (Fake School Girl) (Tao,Yoko)
    'MM_M092_EM105_1': [Demon_Sync(449),Demon_Sync(-606,1152),Demon_Sync(1152),Demon_Sync(1157)], #School Tsuchigumo [62] (Second Floor Hallway) (Tao,Yoko)
    'MM_M092_EM106_': [Demon_Sync(501),Demon_Sync(448)], #School Manananggal +Shiki Ouji [66] (CoV 3rd Floor Corner from Far 2nd Floor Staircase, CoC 3rd Floor Hallway)
    'MM_M092_EM107_': [Demon_Sync(492),Demon_Sync(495),Demon_Sync(-606,1152),Demon_Sync(1157)], #School Rakshasa + Incubus [57] (Left at the Entrance) (Tao,Yoko)
    'MM_M092_EM108_': [Demon_Sync(493)], #School Rakshasa [59] (2nd Floor Corner)
    'MM_M092_EM109_a': [Demon_Sync(500)], #School Save Jack Frost (Manananggal) [64]
    'MM_M092_EM110': [Demon_Sync(497)], #School Incubus [61] (CoV 3rd Floor Hallway, CoC  3rd Floor Corner from Far 2nd Floor Staircase)
    'MM_M092_EM111': [Demon_Sync(487),Demon_Sync(502)], #School Aitvaras + Shiki Ouji [61][65] (4th Floor, Encounter depends on choice)
    'MM_M092_EM112_': [Demon_Sync(502),Demon_Sync(447),Demon_Sync(443)], #School Optional Multiple Fights [65][129][60] (Manananggal,Shiki Ouji,Andras) (4th Floor Far Corner)
    'MM_M092_E2186_Direct': [Demon_Sync(1157)], #Yoko after Lahmu takes out Students (Yoko)
    'MM_M092_E2190_hit': [Demon_Sync(-606,1152),Demon_Sync(1157)], #Tao joins during school attack (Tao with Bag, Yoko)
    'MM_M092_Npc_0': [Demon_Sync(-606,1152),Demon_Sync(1157)], # Tao learns that Sahori attacked students (Tao with Bag, Yoko)
    #Mainmission M115 (Dorm Room) 
    'MM_M115_E2405_Direct': [Demon_Sync(1157)], #Yoko in dorm room (Yoko)
    'MM_M115_E2603_Direct': [Demon_Sync(1151), Demon_Sync(561,1150)], #Dazai/Yuzuru in dorm room
    #Mainmission M203 (Qadistu Dimension)
    'MM_M203_E2718_Direct': [Demon_Sync(569),Demon_Sync(1152),Demon_Sync(1157)], #Lilith post-fight lecture (Lilith, Tao, Yoko)

    #SubMission M016 (Empyrean)
    'MM_M016_EM1450': [Demon_Sync(8, 838), Demon_Sync(19)], # A Plot Unveiled (Zeus, Demeter)
    'MM_M016_EM1500': [Demon_Sync(30, 842), Demon_Sync(188, 843), Demon_Sync(189, 844)], #Seed of Life Quest (Maria, Danu, Innana)
    'MM_M016_EM1531': [Demon_Sync(178, 845)], # A Universe in Peril (Shiva)
    
    #Submission M030 (Diet Building)
    'MM_M060_EM1819': [Demon_Sync(928)], # Mother Harlot Fiend Fight
    'MM_M060_EM1819_NewRoute': [Demon_Sync(928)], # Mother Harlot Fiend Fight (Vengeance)
    'MM_M060_EM1821': [Demon_Sync(929)], # Trumpeter Fiend Fight
    'MM_M060_EM1821_NewRoute': [Demon_Sync(929)], # Trumpeter Fiend Fight
    'MM_M061_EM1771': [Demon_Sync(78)], #Mephisto Quest (Mephisto)
    'MM_M061_EM1781': [Demon_Sync(295)], #Cleopatra Quest (Cleopatra)
    'MM_M061_EM1782': [Demon_Sync(295)], #Cleopatra Quest (Cleopatra) Couldn't join due to full party
    'MM_M061_EM1791': [Demon_Sync(31),Demon_Sync(8, 838)], #Artemis Quest (Artemis, Zeus 2 for fun)
    'MM_M061_EM1802': [Demon_Sync(921)], # Matador Fiend Fight
    'MM_M061_EM1802_NewRoute': [Demon_Sync(921)], # Matador Fiend Fight
    'MM_M061_EM2611': [Demon_Sync(188, 843)], #Dagda Quest Danu Event (Danu for fun)
    'MM_M061_EM2613_HitAction': [Demon_Sync(4),Demon_Sync(188, 843)], #Dagda Quest (Dagda, Danu for fun)
    'MM_M062_EM1804': [Demon_Sync(922)], #Daisoujou Fiend Fight
    'MM_M062_EM1804_NewRoute': [Demon_Sync(922)], #Daisoujou Fiend Fight
    'MM_M062_EM1806': [Demon_Sync(923)], #Hell Biker Fiend Fight
    'MM_M062_EM1806_NewRoute': [Demon_Sync(923)], #Hell Biker Fiend Fight
    'MM_M063_EM1809': [Demon_Sync(924),Demon_Sync(925),Demon_Sync(926),Demon_Sync(927)], #Inital Rider Meeting Chiyoda (White Rider,Red Rider,Black Rider,Pale Rider)
    'MM_M063_EM1810': [Demon_Sync(924)], #White Rider Fight Chiyoda
    'MM_M063_EM1812': [Demon_Sync(925)], #Red Rider Fight Chiyoda
    'MM_M063_EM1814': [Demon_Sync(926)], #Black Rider Fight Chiyoda
    'MM_M063_EM1816': [Demon_Sync(927)], #Pale Rider Fight Chiyoda
    'MM_M064_EM1809': [Demon_Sync(924),Demon_Sync(925),Demon_Sync(926),Demon_Sync(927)], #Inital Rider Meeting Shinjuku (White Rider,Red Rider,Black Rider,Pale Rider)
    'MM_M064_EM1810': [Demon_Sync(924)], #White Rider Fight Shinjuku
    'MM_M064_EM1812': [Demon_Sync(925)], #Red Rider Fight Shinjuku
    'MM_M064_EM1814': [Demon_Sync(926)], #Black Rider Fight Shinjuku
    'MM_M064_EM1816': [Demon_Sync(927)], #Pale Rider Fight Shinjuku
    'MM_M107_EM1824': [Demon_Sync(934)], #Demi-Fiend
    'MM_M107_EM1825_Dev651': [Demon_Sync(934)], #Demi-Fiend (Post Fight)
    'MM_M107_EM1825_Direct': [Demon_Sync(934)], #Demi-Fiend (End of Fight)
    'MM_M107_EM1825_Hit': [Demon_Sync(934,1161)], #Demi-Fiend (Fight/Join Prompt) (Seemingly Boss Replacement Anyway)

    #SubMission M035 & M036 (Empyrean & DKC)
    'MM_M035_EM1480': [Demon_Sync(242)], # The Seraph's Return (Michael)
    'MM_M035_EM1491': [Demon_Sync(242)], # The Red Dragon's Invitation (Michael)
    'MM_M036_EM1490': [Demon_Sync(83)], # The Red Dragon's Invitation (Belial)
    'MM_M036_EM1481': [Demon_Sync(83)], # The Seraph's Return (Belial)

    #SubMission M050 (Tokyo Map)
    'MM_M201_EM2411': [Demon_Sync(754)], #Turbo Granny Quest (Turbo Granny)
    'MM_M061_EM2050': [Demon_Sync(387, isNavi=True)], #Picture-Perfect Debut (Amabie??

    #SubMission M061 (Minato)
    'MM_M061_EM0021': [Demon_Sync(433),Demon_Sync(434),Demon_Sync(1157)], #Eligor and Andras Event
    'MM_M061_EM1010': [Demon_Sync(1157)], #No Stone Unturned (Yoko)
    'MM_M061_EM1020': [Demon_Sync(114, isNavi=True)], #The Ultimate Omelet (Aitvaras)
    'MM_M061_EM1030': [Demon_Sync(304, isNavi=True)], #The Cursed Mermaids Mermaid Part
    'MM_M061_EM1031': [Demon_Sync(801)], #Pazuzu Event Mermaid Quest
    'MM_M061_EM1041': [Demon_Sync(803)], #Anahita Event Mermaid Quest 2
    'MM_M061_EM1050_New': [Demon_Sync(820)], #Talisman Hunt (Shiki Ouji)
    'MM_M061_EM1360': [Demon_Sync(861)], #Koumokuten Event Battle Dialogue
    'MM_M061_EM1383': [Demon_Sync(870)], #Seth Event Battle Dialogue
    'MM_M061_EM1630': [Demon_Sync(305),Demon_Sync(43),Demon_Sync(1157)], # The Water Nymph (Leanan (also Apsaras maybe??),Yoko)
    'MM_M061_EM1631': [Demon_Sync(316,867)], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Demon_Sync(43),Demon_Sync(44,869),Demon_Sync(1157)], # The Spirit of Love (Apsaras, Agathion,Yoko)
    'MM_M061_EM1640_Hit': [Demon_Sync(43)], # The Spirit of Love First Area Entry (Apsaras)
    'MM_M061_EM2190': [Demon_Sync(888)], #Halphas Quest (Oni) 
    'MM_M061_EM2531': [Demon_Sync(751)], #Dormarth Quest (Dormarth)
    'MM_M061_EM2601': [Demon_Sync(32)], #Konohana Sakuya Quest (Konohana Sakuya) 
    'esNPC_em0150_02': [Demon_Sync(889)], # A Preta Predicament (Preta) 
    'esNPC_em0150_03': [Demon_Sync(889)], # A Preta Predicament (Preta) 
    'esNPC_em0150_04': [Demon_Sync(889)], # A Preta Predicament (Preta) 
    'esNPC_em0150_05': [Demon_Sync(889)], # A Preta Predicament (Preta) 
    'esNPC_em0150_06': [Demon_Sync(889)], # A Preta Predicament (Preta) 
    'MM_M061_EM0151': [Demon_Sync(889)], # A Preta Predicament (Preta)
    'MM_M061_EM0152': [Demon_Sync(889)], # A Preta Predicament (Preta) 
    'MM_M061_EM0154': [Demon_Sync(889)], # A Preta Predicament (Preta)
    'MM_M061_EM1710': [Demon_Sync(888)], # Moving on up (Oni)
    'MM_M061_EM1715': [Demon_Sync(888)], # Moving on up (Oni) (Oni Outside Event)
    'MM_M061_EM2020': [Demon_Sync(752)], #Nozuchi Queset (Nozuchi) 
    'MM_M061_EM2030': [Demon_Sync(117)], #Brawny Ambitions (Zhu Tun She)
    'MM_M201_EM2040': [Demon_Sync(755)], #Pisaca Quest
    'MM_M061_EM2240': [Demon_Sync(519),Demon_Sync(566)], #CoV Khonsu Ra Quest (Khonsu Ra, Khonsu) 
    'MM_M061_EM2242': [Demon_Sync(579)], #CoV Khonsu Ra Quest (Isis)
    'MM_M061_EM2245': [Demon_Sync(566)], #CoV Khonsu Ra Quest (Khonsu)
    'MM_M061_EM2380': [Demon_Sync(781), Demon_Sync(289, isNavi=True)], #Mo Shuvuu Quest (Andras, Navi Mo Shuvuu)
    'MM_M061_EM2382': [Demon_Sync(289, isNavi=True)], #Mo Shuvuu Quest part 3 (Mo Shuvuu)
    'MM_M061_EM2383': [Demon_Sync(781), Demon_Sync(289, isNavi=True)], #Mo Shuvuu Quest part 4 (Mo Shuvuu, Andras)

    #SubMission M062 (Shinagawa)
    'MM_M062_EM1141': [Demon_Sync(809)], #Kumbhanda Bottle Quest (Kumbhanda)
    'MM_M062_EM1150': [Demon_Sync(23, isNavi=True),Demon_Sync(1157),Demon_Sync(-606,1152)], #A Goddess Stolen part 1 (Idun,Yoko,Tao) #TODO:Check Tao Creation?
    'MM_M062_EM1151_Hit': [Demon_Sync(810), Demon_Sync(23, isNavi=True)], #A Goddess Stolen (Loki, Idun)
    'MM_M062_EM1160': [Demon_Sync(19)], #The Tyrant of Tennozu (Demeter)
    'MM_M062_EM1161_A': [Demon_Sync(804)], #The Tyrant of Tennozu  (Belphegor)
    'MM_M062_EM1180': [Demon_Sync(-606,1152),Demon_Sync(1157)], #King Frost Quest Nekomata(Tao with Bag)
    'MM_M062_EM1181': [Demon_Sync(821)], #King Frost Quest (King Frost) 
    'MM_M062_EM1331': [Demon_Sync(828)],#Lord's Sword Quest (Arahabaki)  
    'MM_M062_EM1340': [Demon_Sync(860)], #Zouchouten Event Battle  
    'MM_M062_EM1401': [Demon_Sync(519),Demon_Sync(516)], #Khonsu Ra CoC Quest (Khonsu Ra, Khonsu)  
    'MM_M062_EM1402': [Demon_Sync(519),Demon_Sync(516)], #Khonsu Ra CoC Quest (Khonsu Ra, Khonsu)  
    'MM_M062_EM1650': [Demon_Sync(67),Demon_Sync(-606,1152),Demon_Sync(1157)], # Lilim/Principality Quest (Lilim, Tao with bag,Yoko)
    'MM_M062_EM1660': [Demon_Sync(257),Demon_Sync(-606,1152),Demon_Sync(1157)], # Lilim/Principality Quest (Principality, Tao with bag,Yoko)
    'MM_M062_EM2040': [Demon_Sync(803)], #Pisaca Quest part 1 (Anahita)  #TODO: where is this event even?
    'MM_M062_EM2090': [Demon_Sync(561,1150),Demon_Sync(562)],  #Yuzuru Supply Run Quest (Yuzuru, Hayataro) 
    'MM_M062_EM2490': [Demon_Sync(122)], #Brawny Ambitions II (Xiezhai)
    'esNPC_em1650_01': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_02': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_03': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_04': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_05': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_06': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim)
    'MM_M062_EM2110_Enemy': [Demon_Sync(769),Demon_Sync(-606,1152),Demon_Sync(1157)], #Vouivre Quest (Vouivre, Tao with bag,Yoko) 
    'MM_M062_EM2430': [Demon_Sync(59, isNavi=True)], #Pixie on the Case (Pixie)
    'MM_M062_EM2432': [Demon_Sync(59, isNavi=True)], #Pixie on the Case npc Pixies (Pixie)
    'MM_M062_EM2440': [Demon_Sync(768), Demon_Sync(38, isNavi=True)], #Amanozako Control Quest(Yakshini, Amanozako)
    'MM_M062_EM2441': [Demon_Sync(38, isNavi=True)], #Amanozako Control Quest part 2 (Amanozako)
    'MM_M062_EM2442': [Demon_Sync(38, isNavi=True)], #Amanozako Control Quest part 3 (Amanozako)
    'MM_M062_EM2443': [Demon_Sync(38, isNavi=True)], #Amanozako Control Quest part 4 (Amanozako)
    'MM_M062_EM2444': [Demon_Sync(38, isNavi=True)], #Amanozako Control Quest part 5 (Amanozako)
    'MM_M062_EM2446': [Demon_Sync(38, isNavi=True)], #Amanozako Control Quest part 7 (Amanozako)

    #SubMission M063 (Chiyoda)
    'MM_M063_EM1210': [Demon_Sync(824),Demon_Sync(826)], #Oyamatsumi Quest (Take-Minakata,Oyamatsumi)
    'MM_M063_EM1211': [Demon_Sync(826)], #Oyamatsumi Quest (Oyamatsumi)
    'MM_M063_EM1230_HitAAction': [Demon_Sync(333, isNavi=True)], #Hua Po Quest (Hua Po)
    'MM_M063_EM1231': [Demon_Sync(333, isNavi=True)], #Hua Po Quest end
    'MM_M063_EM1241_Navi': [Demon_Sync(273, isNavi=True)], #Chiyoda Gem Quest (Decarabia)
    'MM_M063_EM1250': [Demon_Sync(822)],#Kunitsukami Fight Quest (Okuninushi) 
    'MM_M063_EM1251': [Demon_Sync(823)],#Kunitsukami Fight Quest (Sukuna Hikona)
    'MM_M063_EM1260': [Demon_Sync(19)], #Demeter Defeat Chimera (Demeter) 
    'MM_M063_EM1281': [Demon_Sync(814)], #The Archangel of Destruction (Camael)
    'MM_M063_EM1291': [Demon_Sync(816)], #Roar of Hatred (Moloch) 
    'MM_M063_EM1350': [Demon_Sync(862)], #Jikoukuten Event Battle 
    'MM_M063_EM1592': [Demon_Sync(876)], #Berserk Amanozako Quest (Amanozako Runaway) 
    'MM_M063_EM1670': [Demon_Sync(72)], #Black Frost Dionysus Quest (Black Frost) 
    'MM_M063_EM1680': [Demon_Sync(183)], #Black Frost Dionysus Quest (Dionysus)
    'MM_M063_EM2170': [Demon_Sync(227)], #Masakado Quest
    'MM_M063_EM2390': [Demon_Sync(128, isNavi=True)], #Cironnup Quest (Cironnup)
    'MM_M063_EM2390_Start': [Demon_Sync(128, isNavi=True)], #Cironnup Quest start (Cironnup)
    'MM_M063_EM2397': [Demon_Sync(128, isNavi=True)], #Cironnup Quest part 8 (Cironnup)
    'MM_M063_EM2580': [Demon_Sync(776)], #Yoshitsune Haunt Quest (Atavaka)

    #SubMission M064 (Shinjuku)
    'MM_M064_EM1260': [Demon_Sync(19),Demon_Sync(-606,1152),Demon_Sync(1157)], #Demeter Defeat Chimera Shinjuku (Demeter, Tao with Bag,Yoko)
    'MM_M064_EM1261': [Demon_Sync(812)], #Demeter Defeat Chimera Shinjuku (Chimera)
    'MM_M064_EM1281': [Demon_Sync(814)], #The Archangel of Destruction Shinjuku(Camael)
    'MM_M064_EM1291': [Demon_Sync(816)], #Roar of Hatred Shinjuku(Moloch)
    'MM_M064_EM1391': [Demon_Sync(829),Demon_Sync(830)], #Winged Sun (Mithras, Asura) 
    'MM_M064_EM2130': [Demon_Sync(41), Demon_Sync(386)], #Basilisk Hunt Quest (Anansi, Onyankopon)
    'MM_M064_EM2131': [Demon_Sync(41)], #Basilisk Hunt Quest (Anansi)
    'MM_M064_EM2270': [Demon_Sync(40),Demon_Sync(-606,1152),Demon_Sync(1157)], #Kresnik Kudlak Quest (Kresnik, Tao with Bag,Yoko) 
    'MM_M064_EM2280': [Demon_Sync(346),Demon_Sync(-606,1152),Demon_Sync(1157)], #Kresnik Kudlak Quest (Kudlak, Tao with Bag,Yoko)
    'MM_M064_EM2306': [Demon_Sync(387, isNavi=True)], #Amabie in Macabre Quest (Amabie)
    'MM_M064_EM2360': [Demon_Sync(355, isNavi=True)], #Alice Quest (Alice)
    'MM_M064_EM2360_Event': [Demon_Sync(355, isNavi=True)], #Alice Quest Event (Alice)
    'MM_M064_EM2361': [Demon_Sync(355, isNavi=True)], #Alice Quest part 2 (Alice)
    'MM_M064_EM2363': [Demon_Sync(355, isNavi=True)], #Alice Quest part 4 (Alice)
    'MM_M064_EM2364': [Demon_Sync(355, isNavi=True)], #Alice Quest part 5 (Alice)
    'MM_M064_EM2366': [Demon_Sync(355, isNavi=True)], #Alice Quest part 7 (Alice)
    'MM_M064_EM2310': [Demon_Sync(386, 770), Demon_Sync(41),Demon_Sync(-606,1152),Demon_Sync(1157)], #Onyakopon Anansi Quest (Onyakopon Side) (Tao with Bag,Yoko)
    'MM_M064_EM2320': [Demon_Sync(41, 771), Demon_Sync(386),Demon_Sync(-606,1152),Demon_Sync(1157)], #Onyakopon Anansi Quest (Anansi Side) (Tao with Bag,Yoko)
    'MM_M064_EM2400': [Demon_Sync(596)], #Samael Quest (Mastema) 
    'MM_M064_EM2402': [Demon_Sync(760)], #Samael Quest (Samael) 
    'MM_M064_EM2421_Direct': [Demon_Sync(681)], #Satan Quest (Satan) 
    'MM_M064_EM2461': [Demon_Sync(892),Demon_Sync(-606,1152),Demon_Sync(1157)], #Mara Quest (Mara, Tao with Bag,Yoko) 
    'MM_M064_EM2500': [Demon_Sync(215)], #Brawny Ambitions III (Okuninushi) 
    'MM_M064_EM2521_Navi': [Demon_Sync(273, isNavi=True)], #Shinjuku Gem Quest (Decarabia)
    'MM_M064_EM2552': [Demon_Sync(509)], #MadGasser Quest (Zhen (3xCopy))
    'MM_M064_EM2620': [Demon_Sync(365)], #Orochi Quest Kushinada & Co Part (Tao Panagia)
    'MM_M064_EM2621': [Demon_Sync(775)], #Orochi Quest (Orochi) 

    #SubMission M060 (Taito)
    'MM_M060_EM1370': [Demon_Sync(863)], #Bishamonten Event Battle 
    'MM_M060_EM1381': [Demon_Sync(516)], #Khonsu CoC Quest (Khonsu) 
    'MM_M060_EM1390': [Demon_Sync(831),Demon_Sync(516)], #Winged Sun CoC (Amon,Khonsu)  
    'MM_M060_EM1390_NewRoute': [Demon_Sync(831)], #Winged Sun CoV (Amon) 
    'MM_M060_EM1391': [Demon_Sync(829),Demon_Sync(830)], #Winged Sun CoC(Mithras, Asura) 
    'MM_M060_EM1420': [Demon_Sync(35)], #Fionn 2 Quest (Fionn) 
    'MM_M060_EM1431': [Demon_Sync(836),Demon_Sync(834),Demon_Sync(835)], #Holy Ring Quest (Uriel, Raphael,Gabriel) 
    'MM_M060_EM1440': [Demon_Sync(19)], #Baal Quest (Demeter) 
    'MM_M060_EM1441': [Demon_Sync(837)], #Baal Quest (Baal) 
    'MM_M060_EM1460': [Demon_Sync(839)], #The Gold Dragon's Arrival (Huang Long) 
    'MM_M060_EM1580': [Demon_Sync(280, isNavi=True)], #On Bended Knees (Yatagarasu)
    'MM_M060_EM1600': [Demon_Sync(878)],  #Final Amanozako Quest (Kurama Tengu) 
    'MM_M060_EM1601': [Demon_Sync(878),Demon_Sync(38),Demon_Sync(877)], #Final Amanozako Quest (Kurama Tengu,Amanozako, Zaou Gongen)
    'MM_M060_EM1602': [Demon_Sync(38)],  #Final Amanozako Quest (Amanozako) 
    'MM_M060_EM1690': [Demon_Sync(265),Demon_Sync(365)],  #Adramelech Futsunushi Quest (Adramalech, Tao Panagia) 
    'MM_M060_EM1700': [Demon_Sync(201),Demon_Sync(365)],  #Adramelech Futsunushi Quest (Futsunushi, Tao Panagia) 
    'MM_M060_EM2371': [Demon_Sync(865)],  #Garuda Quest (Garuda) 
    'MM_M060_EM2480': [Demon_Sync(60, isNavi=True)], #Nahobiho Quest (Nahobiho)
    'MM_M060_EM2481': [Demon_Sync(60, isNavi=True)], #Nahobiho Quest part 2 (Nahobiho)
    'MM_M060_EM2482': [Demon_Sync(60, isNavi=True)], #Nahobiho Quest part 3 (Nahobiho)
    'MM_M060_EM2483': [Demon_Sync(60, isNavi=True)], #Nahobiho Quest part 4 (Nahobiho)
    'MM_M060_EM2484': [Demon_Sync(60, isNavi=True)], #Nahobiho Quest part 5 (Nahobiho)
    'MM_M060_EM2570': [Demon_Sync(22, 779),Demon_Sync(365)], #Moirae Haunt Quest (Norn, Tao Panagia)
    'MM_M060_EM2630': [Demon_Sync(782)],  #Saturnus Quest(Saturnus) #TODO: Has Zeus(Likely  Zeus in party replace?)
    'MM_M061_EM2705': [Demon_Sync(207)], # The Guardian of Light (Marici)

    #Submission M082 (Outside School)
    'MM_M082_EM2053': [Demon_Sync(1152)], #Give Amabie Photo to Tao (Tao)
    'MM_M082_EM2055': [Demon_Sync(1157)], #Give Amabie Photo to Yoko

    #Garden SubMission
    'MM_M060_EM2351': [Demon_Sync(778)],  #Idun Haunt Quest (Thor)

    #NPCs
    'BP_es035_m063_01': [Demon_Sync(35)],#Fionn area 3 (Fionn) 
    'BP_es152_m062_01': [Demon_Sync(152)],#Hayataro area 2 (Hayataro) 
    'BP_es152_m063_01': [Demon_Sync(152)],#Hayataro area 3 (Hayataro) 
    'BP_es416_m060_01': [Demon_Sync(75, 435)],#Nuwa in Area 4 
    'BP_es618_m060_01': [Demon_Sync(465)],#Yakumo in Area 4 
    'BP_es418_m063_01': [Demon_Sync(75, 435)],#Nuwa in Area 3 #TODO No clue where they are
    'BP_es618_m063_01': [Demon_Sync(465)],#Yakumo in Area 3 #TODO No clue where they are
    'esNPC_m061_32_Navi': [Demon_Sync(316, isNavi=True)], #Navi Ippon Datara
    'esNPC_m061_33_Navi': [Demon_Sync(304, isNavi=True)], #Navi Mermaid
    'esNPC_m061_37_Navi': [Demon_Sync(356, isNavi=True)], #Navi Hell Biker
    'esNPC_m061_38_Navi': [Demon_Sync(295, isNavi=True)], #Navi Cleopatra
    'esNPC_m062_NaviDevil_01': [Demon_Sync(44, isNavi=True)], #Navi Agathion
    'esNPC_m062_NaviDevil_41': [Demon_Sync(147, isNavi=True)], #Navi Mothman
    'esNPC_m062_NaviDevil_42': [Demon_Sync(23, isNavi=True)], #Navi Idun
    'esNPC_m064_NaviDevil_01': [Demon_Sync(214, isNavi=True)], #Navi Sukuna Hikona
    'esNPC_m060_08_Navi': [Demon_Sync(144, isNavi=True)], #Navi Bugs
    'esNPC_m060_14_Navi': [Demon_Sync(77, isNavi=True)], #Navi Mara
    'esNPC_m060_15_Navi': [Demon_Sync(35, isNavi=True)], #Navi Fionn
    'esNPC_m083_10': [Demon_Sync(1157)], #Yoko in Station? #TODO: Where and what?

    #Playable Demons
    'Pla038': [Demon_Sync(38, isNavi=True)], #Player Amanozako
    'Pla038_AnimBP': [Demon_Sync(38, isNavi=True)], #Player Amanozako Animations
    'Pla059': [Demon_Sync(59, isNavi=True)], #Player Pixie
    'Pla059_AnimBP': [Demon_Sync(59, isNavi=True)], #Player Pixie Animations
    'Pla060': [Demon_Sync(60, isNavi=True)], #Player Nahobiho
    'Pla060_AnimBP': [Demon_Sync(60, isNavi=True)], #Player Nahobiho Animations
    'Pla128': [Demon_Sync(128, isNavi=True)], #Player Cironnup
    'Pla128_AnimBP': [Demon_Sync(128, isNavi=True)], #Player Cironnup Animations
    'Pla289': [Demon_Sync(289, isNavi=True)], #Player Mo Shuvuu
    'Pla289_AnimBP': [Demon_Sync(289, isNavi=True)], #Player Mo Shuvuu Animations
    'Pla355': [Demon_Sync(355, isNavi=True)], #Player Alice
    'Pla355_AnimBP': [Demon_Sync(355, isNavi=True)], #Player Alice Animations
}

#Which animations are being played in scripts that might not be available to every demon and which to use instead
#Beware Capitalization!!
SCRIPT_ANIMS_REPLACEMENTS = {
    'EM_M061_DevilTalk': [Anim_Sync('02idleB','05attack')], #Talk Tutorial (Pixie)
    'MM_M061_EM1630': [Anim_Sync('06skill_Composite','06skill')], # The Water Nymph (Leanan)
    'MM_M061_EM1631': [Anim_Sync('map/700000_event_idle', '01idleA')], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Anim_Sync('06skill_Composite','06skill')], # The Spirit of Love (Apsaras)
    'MM_M061_EM1640_Hit': [Anim_Sync('map/700000_event_idle', '01idleA')], # The Spirit of Love First Entry (Apsaras)
    'MM_M061_E2625_Direct': [Anim_Sync('map/700000_dying','04dying')], #CoV Khonsu Event Post Fight Bethel Egypt (Isis,Khonsu,Yuzuru,Dazai)
    'MM_M061_EM0181': [Anim_Sync('Event/EVT_v_sit_loop','01idleA'),Anim_Sync('map/700007_sit_idleA','04dying')], #Amanozako gives you a bead
    'MM_M061_EM0182': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700002_doya','05attack'),Anim_Sync('map/700004_yuudou_in','11run'),Anim_Sync('map/700005_yuudou_loop','04dying'),Anim_Sync('map/001000_run','11run'),Anim_Sync('map/700007_sit_idleA','04dying')], #Amanozako becomes your navigator
    'EM_M061_Q0019': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700005_yuudou_loop','04dying')], #Amanozako leaves in area 1
    'EM_M061_TutorialNavi02': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('Event/EVT_v_action_loop','05attack'),Anim_Sync('Event/EVT_v_action_inout','11run'),Anim_Sync('map/700000_yes','51yes')], #Amanozako first partner spot
    'MM_M038_E2930_Direct': [Anim_Sync('Event/EVT_E0604c01m_loop','04dying')], #Shakan Abdiel Post Fight
    'MM_M060_E762': [Anim_Sync('map/700000_event_idle', '01idleA')],#Nuwa in area 4 at the gate
    'MM_M060_E3020': [Anim_Sync('Event/EVT_v_turnwalk_inout','11run')], #Yakumo in area 4 vengeance part 2
    'MM_M062_EM0120_Direct': [Anim_Sync('map/700002_doya','05attack'),Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/001000_run','11run')], #Amanozako rejoins in area 2
    'MM_M062_EM0122': [Anim_Sync('Event/EVT_v_idle_loop','01idleA')], #Amanozako car event
    'MM_M062_EM0123': [Anim_Sync('map/700002_doya','05attack'),Anim_Sync('Event/EVT_v_idle_loop','01idleA')], #Amanozako railroad event
    'MM_M062_EM0124': [Anim_Sync('map/700000_yes','51yes'),Anim_Sync('Event/EVT_v_idle_loop','01idleA'),Anim_Sync('Event/EVT_v_run_loop','11run')], #Amanozako container event
    'MM_M062_EM0125': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700005_yuudou_loop','04dying'),Anim_Sync('map/001000_run','11run')], #Amanozako leaves in area 2
    'MM_M062_E0380': [Anim_Sync('Map/700002_event_idle','01idleA')], #Fionn 1 Post-fight (Fionn)
    'MM_M062_E0492': [Anim_Sync('3rd_01idleA','01idleA'),Anim_Sync('3rd_41encount','41encount')], #Final Lahmu (Lahmu Phase 2)
    #'MM_M062_EM0041': [Anim_Sync('Event/EVT_SlowEncount_inout','41encount')], #Loup-garous Event
    'MM_M062_E2295_Direct': [Anim_Sync('02idleB','05attack')],#Eisheth pre-fight
    'MM_M062_E2298_Direct': [Anim_Sync('Map/700002_event_idle','01idleA')], #Fionn 1 Post-fight Vengeance (Fionn)
    'MM_M063_EM0130': [Anim_Sync('map/700006_yuudou_out','11run'),Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/001000_run','11run')], #Amanozako in Chiyoda
    'MM_M064_E2647': [Anim_Sync('Event/EVT_v_idle_loop','01idleA'),Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700004_yuudou_in','11run'),Anim_Sync('map/700005_yuudou_loop','04dying'),Anim_Sync('Event/EVT_E0180c03m_loop','06skill'),Anim_Sync('map/001000_run','11run')], #Amanozako in Shinjuku
    'MM_M064_E2690': [Anim_Sync('map/700000_dead01','04dying'),Anim_Sync('map/700001_dead02','04dying')], #Dead Cherubim
    'MM_M060_EM0140': [Anim_Sync('Event/EVT_E0180c03m_loop','06skill'),Anim_Sync('map/700002_doya','05attack'),Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/001000_run','11run')], #Amanozako rejoins in area 4 Creation
    'MM_M092_EM107_': [Anim_Sync('06skill_a','06skill'),Anim_Sync('06skill_b','06skill'),Anim_Sync('06skill_c','06skill')], #School Rakshasa + Incubus
    'MM_M092_EM109_a': [Anim_Sync('02idleB','05attack')], #School Save Jack Frost (Manananggal)

    'MM_M016_EM1450': [Anim_Sync('02idleB','41encount'),Anim_Sync('41encount','05attack'),Anim_Sync('51yes','51yes_Composite')], #A Plot Unveiled
    'MM_M016_EM1500': [Anim_Sync('06skill_Composite','06skill'),Anim_Sync('51yes','51yes_Composite')], #A Universe in Peril
    'MM_M016_EM1531': [Anim_Sync('41encount','05attack'),Anim_Sync('51yes','51yes_Composite')], #A Universe in Peril
    'MM_M060_EM1819': [Anim_Sync('51yes','05attack')], #Mother Harlot Fight
    'MM_M060_EM1819_NewRoute': [Anim_Sync('51yes','05attack')], #Mother Harlot Fight (Vengeance?)
    'MM_M061_EM1781': [Anim_Sync('02idleB','05attack')], #Cleopatra Quest 
    'MM_M061_EM1791': [Anim_Sync('02idleB','05attack'),Anim_Sync('map/700000_event_idle', '01idleA')], #Artemis Quest 
    'MM_M061_EM2613_HitAction': [Anim_Sync('02idleB','41encount'),Anim_Sync('Sub/Sub_13skill_ex1','06skill')], #Dagda Quest
    'MM_M061_EM2380': [Anim_Sync('20skillA','06skill')], #Mo Shuvuu Quest
    'MM_M061_EM2382': [Anim_Sync('20skillA','06skill')], #Mo Shuvuu Quest part 3
    'MM_M062_EM1806': [Anim_Sync('06skill_Composite','06skill')], # Hell Biker Fight
    'MM_M062_EM1806_NewRoute': [Anim_Sync('06skill_Composite','06skill')], # Hell Biker Fight
    'MM_M063_EM1810': [Anim_Sync('06skill_Composite','06skill')], #White Rider Fight Chiyoda
    'MM_M063_EM1812': [Anim_Sync('06skill_Composite','06skill')], #Red Rider Fight Chiyoda
    'MM_M063_EM1814': [Anim_Sync('06skill_a','06skill'),Anim_Sync('06skill_b','06skill'),Anim_Sync('06skill_c','06skill'),Anim_Sync('06skill_d','06skill')], #Black Rider Fight Chiyoda
    'MM_M064_EM1810': [Anim_Sync('06skill_Composite','06skill')], #White Rider Fight Shinjuku
    'MM_M064_EM1812': [Anim_Sync('06skill_Composite','06skill')], #Red Rider Fight Shinjuku
    'MM_M064_EM1814': [Anim_Sync('06skill_a','06skill'),Anim_Sync('06skill_b','06skill'),Anim_Sync('06skill_c','06skill'),Anim_Sync('06skill_d','06skill')], #Black Rider Fight Shinjuku
    'MM_M061_EM0021': [Anim_Sync('09skill_d','06skill'),Anim_Sync('08skill_c','06skill')], #Eligor and Andras Event
    'MM_M061_EM1031': [Anim_Sync('09skill_d','06skill'),Anim_Sync('08skill_c','06skill')], #Pazuzu Event Mermaid Quest
    'MM_M061_EM1041': [Anim_Sync('02idleB','05attack')], #Anahita Event Mermaid Quest 2
    'esNPC_em0150_02': [Anim_Sync('map/700002_event_idle','03dmg')], # A Preta Predicament (Preta) 
    'esNPC_em0150_03': [Anim_Sync('map/700003_event_idle','04dying')], # A Preta Predicament (Preta)
    'esNPC_em0150_04': [Anim_Sync('map/700005_event_idle','11run')], # A Preta Predicament (Preta)
    'esNPC_em0150_05': [Anim_Sync('map/700007_event_idle','51yes')], # A Preta Predicament (Preta)
    'esNPC_em0150_06': [Anim_Sync('map/700006_event_idle','14command')], # A Preta Predicament (Preta) 
    'MM_M061_EM0151': [Anim_Sync('map/700000_event_idle','01idleA')], # A Preta Predicament (Preta)
    'MM_M061_EM0152': [Anim_Sync('map/700006_event_idle','14command'),Anim_Sync('map/700007_event_idle','51yes'),Anim_Sync('map/700005_event_idle','11run'),Anim_Sync('map/700003_event_idle','04dying'),Anim_Sync('map/700002_event_idle','03dmg')], # A Preta Predicament (Preta) event idles 2,3,4,5,6,7,8,9
    'MM_M061_EM0154': [Anim_Sync('map/700005_event_idle','11run')], # A Preta Predicament (Preta) event idle 5
    'MM_M061_EM1710': [Anim_Sync('map/700000_event_idle', '01idleA')], # Moving on up (Oni)
    'MM_M061_EM1715': [Anim_Sync('07skill_b','06skill')], # Moving on up (Oni) (Oni Outside Event)
    'MM_M061_EM2020': [Anim_Sync('map/700010_jitabata','11run')], # Nozuchi Quest
    'MM_M061_EM1650': [Anim_Sync('02idleB','05attack')], # Lilim/Principality Quest (Lilim)
    'esNPC_em1650_02': [Anim_Sync('map/700003_event_idle','03dmg')], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_03': [Anim_Sync('map/700001_event_idle','11run')], # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_04': [Anim_Sync('map/700004_event_idle','14command')], # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_05': [Anim_Sync('map/700002_event_idle','51yes')], # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_06': [Anim_Sync('map/700000_event_idle','04dying')], # Lilim/Principality Quest NPCs (Lilim) 
    'MM_M063_EM1210': [Anim_Sync('06skill_Composite','06skill')], #Kunitsu Quest (Take-Minakata,Oyamatsumi)
    'MM_M063_EM1281': [Anim_Sync('21skillB','06skill')],#The Archangel of Destruction (Camael)
    'MM_M062_EM0050': [Anim_Sync('map/000000_idleA','01idleA')],#Idun in Golden Apple Quest creation
    'MM_M062_E2305_2': [Anim_Sync('map/000000_idleA','01idleA')],#Idun in Golden Apple Quest vengeance
    'MM_M062_EM2440': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/001000_run','11run'),Anim_Sync('map/700001_no','03dmg')],#Amanozako Control Quest
    'MM_M062_EM2440': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/001000_run','11run'),Anim_Sync('map/700001_no','03dmg')],#Amanozako Control Quest
    'MM_M062_EM2441': [Anim_Sync('map/700001_no','03dmg'),Anim_Sync('Event/EVT_v_run_loop','11run'),Anim_Sync('map/001000_run','11run'),Anim_Sync('Event/EVT_v_idle_loop','01idleA'),Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700000_yes','51yes')],#Amanozako Control Quest part 2
    'MM_M062_EM2442': [Anim_Sync('map/700002_doya','05attack'),Anim_Sync('map/700000_yes','51yes'),Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700003_homeru','06skill')],#Amanozako Control Quest part 3
    'MM_M062_EM2443': [Anim_Sync('map/000000_idleA','01idleA')],#Amanozako Control Quest part 4
    'MM_M062_EM2444': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700001_no','03dmg')],#Amanozako Control Quest part 5
    'MM_M062_EM2446': [Anim_Sync('map/000000_idleA','01idleA'),Anim_Sync('map/700000_yes','51yes'),Anim_Sync('map/700002_doya','05attack')],#Amanozako Control Quest part 7
    'MM_M064_EM1281': [Anim_Sync('21skillB','06skill')],#The Archangel of Destruction Shinjuku (Camael)
    'MM_M064_EM2130': [Anim_Sync('02idleB','05attack'),Anim_Sync('map/700020_stick','14command'),Anim_Sync('map/700010_laugh','14command')], #Basilisk Hunt Quest (Anansi, Onyankopon)
    'MM_M064_EM2306': [Anim_Sync('map/700000_dance','51yes')],#Amabie in Macabre Quest
    'MM_M064_EM2360': [Anim_Sync('map/700000_event_idle_in','51yes'),Anim_Sync('map/700002_event_idle_out','14command'),Anim_Sync('map/700001_event_idle_loop','01idleA'),Anim_Sync('07skill_b','06skill'),Anim_Sync('06skill_a','06skill')],#Alice Quest
    'MM_M064_EM2360_Event': [Anim_Sync('map/700000_event_idle_in','51yes'),Anim_Sync('map/700001_event_idle_loop','01idleA')],#Alice Quest Event
    'MM_M064_EM2366': [Anim_Sync('map/700000_event_idle_in','51yes'),Anim_Sync('map/700001_event_idle_loop','01idleA')],#Alice Quest part 7
    'MM_M064_EM2310': [Anim_Sync('02idleB','05attack')],#Onyakopon Anansi Quest (Onyakopon Side)
    'MM_M064_EM2400': [Anim_Sync('13skill_ex2','06skill')], #Samael Quest (Mastema)
    'MM_M064_EM2421_Direct': [Anim_Sync('13skill_ex3_Composite','05attack')], #Satan Quest (Satan)
    'MM_M064_EM2552': [Anim_Sync('map/700002_event_idle','11run'),Anim_Sync('map/700000_event_idle','02idleB'),Anim_Sync('map/700001_event_notice','05attack')], #MadGasser Quest (Zhen (3xCopy))
    'MM_M060_EM1381': [Anim_Sync('09skill_d','06skill'),Anim_Sync('09skill_c','06skill'),Anim_Sync('02idleB','14command')], #Winge Sun CoC (Amon,Khonsu)
    'MM_M060_EM1420': [Anim_Sync('Map/700002_event_idle','14command'),Anim_Sync('Map/700000_event_idle','51yes')], #Fionn 2 Quest (Fionn)
    'MM_M060_EM1440': [Anim_Sync('02idleB','14command')], #Baal Quest (Demeter)
    'MM_M060_EM2480': [Anim_Sync('01idleA_field','01idleA'),Anim_Sync('Map/700001_awawa','03dmg'),Anim_Sync('Map/700000_encount_loop','41encount')], #Nahobiho Quest
    'MM_M060_EM2481': [Anim_Sync('01idleA_field','01idleA'),Anim_Sync('Map/700001_awawa','03dmg')], #Nahobiho Quest part 2
    'MM_M060_EM2482': [Anim_Sync('01idleA_field','01idleA')], #Nahobiho Quest part 3
    'MM_M060_EM2483': [Anim_Sync('Map/700001_awawa','03dmg')], #Nahobiho Quest part 4
    'MM_M060_EM2483': [Anim_Sync('01idleA_field','01idleA')], #Nahobiho Quest part 5
    'Pla038_AnimBP': [Anim_Sync('map/000000_idleA','01idleA')], #Player Amanozako Animations
    'Pla060_AnimBP': [Anim_Sync('01idleA_field','01idleA'),Anim_Sync('81twistPoseAsset','51yes')], #Player Nahobiho Animations
    'Pla289_AnimBP': [Anim_Sync('11run_EvtRemote','11run'),Anim_Sync('81twist_PoseAsset','51yes')], #Player Mo Shuvuu Animations
}

#For bosses that do not use their own model, which model they should use instead
MODEL_SYNC = {
    434: 272, # 2 Andras from Eligor
    832: 84, #Abaddon
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
    488: 272, # Andras (School Copy) with 491 Rakshasa
    489: 272, # Andras (School Copy)
    490: 272, # Andras (School Copy)
    443: 272, # Andras (School)
    434: 272, # Andras (With Eligor)
    517: 120, # Anubis (CoC Summon)
    439: 287, # Anzu (Jozoji)
    728: 287, # Anzu (Single Abcess)
    606: 287, # Anzu (with Mishaguji)
    868: 43, # Apsaras
    828: 211, #Arahabaki
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
    804: 86, #Belphegor
    859: 203, # Bishamonten (2 Turn)
    863: 203, # Bishamonten (4 Turn)
    882: 72, #Black Frost
    773: 171, # Black Ooze
    926: 352, # Black Rider
    814: 248, # Camael
    812: 127, # Chimera
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
    827: 232, # Girimekhala 
    552: 142, # Glaysa-Labolas (I)
    555: 142, # Glasya-Labolas (with Naamah)
    890: 337, #Gogmagog
    891: 291, #Gurulu
    608: 34, # Hanuman
    562: 152, # Hayataro
    813: 322, #Hecatoncheires
    923: 356, # Hell Biker
    864: 13, # Horus
    839: 94, # Huang Long
    432: 115, #Hydra
    844: 189, # Inanna
    495: 68, # Incubus (School Copy)
    496: 68, # Incubus (School Copy) with 489 Andras
    497: 68, # Incubus (School Copy)
    498: 68, # Incubus (School Copy)
    445: 68, # Incubus (School)
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
    821: 87, #King Frost
    516: 7, # Khonsu (CoC)
    566: 7, # Khonsu (CoV)
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
    501: 302, # Manananggal (School Copy) with 448 Shiki Ouji
    447: 302, # Manananggal (School)
    705: 45, # Mandrake
    892: 77, #Mara (Punishing)
    893: 77, #Mara (Virtual Trainer)
    842: 30, # Maria
    783: 207, # Marici
    784: 207, # Conquering Mirage
    785: 207, # Stitching Mirage
    786: 207, # Warding Mirage
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
    816: 85, #Moloch
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
    446: 318, # Oni (School) with 444 Rakshasa
    706: 290, # Onmoraki
    770: 386, # Onyankopon
    731: 139, # Orobas (Abcess)
    817: 139, # Orobas (With Moloch)
    726: 135, # Orthrus
    475: 269, # Ose (Summon)
    826: 212, # Oyamatsumi (Punishing)
    825: 212, # Oyamatsumi (With Kunitsu)
    927: 358, # Pale Rider
    801: 233, # Pazuzu
    755: 341, # Pisaca
    622: 59, # Pixie
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
    621: 173, # Slime
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
    808: 283, #Thunderbird
    929: 350, # Trumpeter
    449: 331, # Tsuchigumo (School) with 499 Oni
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
    521: 520, # Thunder Bit (use Nahobino Nuwa)
    522: 520, # Thunder Bit (use Nahobino Nuwa)
    523: 520, # Thunder Bit (use Nahobino Nuwa)
    524: 520, # Thunder Bit (use Nahobino Nuwa)
    526: 525, # Depraved Arm (use Nahobino Abdiel)
    527: 525, # Depraved Wing (use Nahobino Abdiel)
    576: 392, # Agrat Illusion
    1161: 934, #Demi-fiend (Guest)
    1150: 561, #Yuzuru (Guest ID to Boss ID)
}

'''
Creates a dictionary of all LV event files and their SEQ files.

'''
def build_lv_sequences(script_dir: Path):
    lv_sequences = defaultdict(list)

    for file in script_dir.iterdir():
        if not file.is_file() or file.suffix != ".uasset":
            continue

        name = file.stem
        SEQ_RE = re.compile(r"^SEQ_(E\d{4})_*")
        match = SEQ_RE.match(name)
        if not match:
            continue

        event_id = match.group(1)        
        lv_key = f"LV_{event_id}"        

        lv_sequences[lv_key].append(name)

    for lv in lv_sequences:
        lv_sequences[lv].sort()

    return dict(lv_sequences)
LV_SEQUENCES = build_lv_sequences(Path('base/Design Event/'))