from base_classes.message import Demon_Sync

class Anim_Sync():
    def __init__(self,ind, sync=None):
        self.ind = ind
        self.sync = ind
        if sync:
            self.sync = sync


#List of which level umaps event scripts use for their location and sizes
#To find out, look at which MapEventID the Script has in its File and then take a look at map event data
LEVEL_UASSETS = {
    'MM_M061_EM1630': 'LV_EventMission_M061',
    'MM_M061_EM1631': 'LV_EventMission_M061',
    'MM_M061_EM1640': 'LV_EventMission_M061',
}

#List of events that require updated scaling to trigger events with large demons
REQUIRES_HIT_UPDATE = [
    'MM_M016_E0885','MM_M038_E2912','MM_M060_Npc609Talk',
    'MM_M063_EM0061','MM_M064_E2512','MM_M064_E2540','MM_M085_E0690','MM_M085_E0730',
    "MM_M064_E2690",
    'MM_M085_E2660','MM_M085_E2688',
    'MM_M088_E0602_Abdiel','MM_M088_E0602_Khons','MM_M088_E0602_Koshimizu','MM_M088_E0602_Vasuki','MM_M088_E0602_Odin','MM_M088_E0602_Zeus',
    'MM_M092_EM101_','MM_M092_EM102_','MM_M092_EM105_1','MM_M092_EM106_','MM_M092_EM110',
    'MM_M016_EM1450','MM_M016_EM1500',
    'MM_M061_EM1782','MM_M061_EM1791','MM_M061_EM2611','MM_M107_EM1824','MM_M107_EM1825_Dev651','MM_M107_EM1825_Hit',
    'MM_M035_EM1480','MM_M035_EM1491','MM_M036_EM1490','MM_M036_EM1481',
    'MM_M061_EM1041','MM_M061_EM1050_New','MM_M061_EM1360','MM_M061_EM1630','MM_M061_EM1640', 'MM_M061_EM2190','MM_M061_EM2531',
    'MM_M061_EM0151','MM_M061_EM0152','MM_M061_EM0154','MM_M061_EM1710','MM_M061_EM2240','MM_M061_EM2245',
    'MM_M062_EM1160','MM_M062_EM1161_A','MM_M062_EM1181','MM_M062_EM1331','MM_M062_EM1340','MM_M062_EM1401','MM_M062_EM1650','MM_M062_EM1660','MM_M062_EM2090','MM_M062_EM2110_Enemy',
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
    'LV_E0180': [Demon_Sync(431)], #UMAP Triple Preta Cutscene
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
    'LV_E0775': [Demon_Sync(468)], #UMAP Vasuki Cutscene
    'LV_E0785': [Demon_Sync(469)], #UMAP Zeus CoC Cutscene
    'LV_E0805': [Demon_Sync(470)], #UMAP Odin CoC Cutscene
    'LV_E0841': [Demon_Sync(-617,528)], #Chaos rep overview pre-empyrean (Tsukuyomi) 
    'LV_E0842': [Demon_Sync(240, 525)], #Law rep overview pre-empyrean (Abdiel) 
    'LV_E0850': [Demon_Sync(240, 467),Demon_Sync(264, 525),Demon_Sync(75, 520),Demon_Sync(465),Demon_Sync(-617,528)], #Argument before Empyrean (Abdiel as Summit Boss, Abdiel Fallen, Nuwa as Naho, Yakumo, Tsukuyomi)
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
   
    'LV_E2010': [Demon_Sync(552),Demon_Sync(561)],#Labolas 1 pre-fight (Labolas, Yuzuru, Dazai)
    'LV_E2015': [Demon_Sync(552),Demon_Sync(561)],#Labolas 1 post-fight (Labolas, Yuzuru, Dazai)
    'LV_E2020': [Demon_Sync(393, 553)],#Naamah pre-fight dialogue 1 (Naamah)
    'LV_E2022': [Demon_Sync(393, 553)],#Naamah pre-fight dialogue 2 (Naamah)
    'LV_E2025': [Demon_Sync(393, 553),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(-395, 569)],#Naamah post-fight dialogue (Naamah,Agrat,Eisheth,Lilith)
    'LV_E2029': [Demon_Sync(567),Demon_Sync(75,550),Demon_Sync(435)],#Nuwa post-fight dialogue vengeance
    'LV_E2030': [Demon_Sync(1151,578),Demon_Sync(561)],#Dazai in diet building vengeance (Dazai, Yuzuru)
    'LV_E2035': [Demon_Sync(1151,578),Demon_Sync(561)],#Returning to Tokyo from area 1 vengeance (Dazai, Yuzuru)
    'LV_E2040': [Demon_Sync(240, 564),Demon_Sync(1151,578),Demon_Sync(561)],#Meeting Abdiel vengeance (Abdiel, Dazai, Yuzuru)
    'LV_E2043': [Demon_Sync(1151,578),Demon_Sync(561)],#Tao meeting after area 1 vengeance (Dazai,Yuzuru)
    'LV_E2051': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(391, 569)],#Qadistu Dream (Naamah II ,Agrat,Eisheth,Lilith)
    'LV_E2160': [Demon_Sync(393, 554),Demon_Sync(555)], #Labolas 2 pre-fight dialogue (Naamah,Labolas)
    'LV_E2164': [Demon_Sync(393, 554)],#Labolas 2 post-fight dialogue (Naamah)
    'LV_E2210': [Demon_Sync(152, 562), Demon_Sync(561)],#Meeting Hayataro vengeance (Hayataro, Yuzuru)
    'LV_E2250': [Demon_Sync(236,556)], #Vengeance Lahmu pre-fight dialogue (Lahmu)
    'LV_E2255': [Demon_Sync(236,556),Demon_Sync(391, 569)], #Lilith kills Sahori (Lahmu, Lilith)
    'LV_E2260': [Demon_Sync(1151,578),Demon_Sync(561)], #Dazai/Yuzuru first argument (Dazai,Yuzuru )
    'LV_E2270': [Demon_Sync(1151,578),Demon_Sync(561),Demon_Sync(152, 562)], #Arriving in area 2 vengeance (Dazai,Yuzuru, Hayataro)
    'LV_E2290': [Demon_Sync(394, 559)],#Eisheth pre-fight dialogue (Eisheth)
    'LV_E2297': [Demon_Sync(451)],#Fionn pre(?)-fight vengeance
    'LV_E2310': [Demon_Sync(1151,578)],#Dazai loses to Eisheth (Dazai)
    'LV_E2320': [Demon_Sync(561),Demon_Sync(394, 559),Demon_Sync(152, 562)],#Yuzuru pre-fight dialogue (Yuzuru, Eisheth, Hayataro)
    'LV_E2325': [Demon_Sync(561),Demon_Sync(394, 559),Demon_Sync(152, 562),Demon_Sync(1151,578),Demon_Sync(-396, 568),Demon_Sync(7,566)], #Yuzuru post-fight dialogue (Yuzuru,Eisheth,Hayataro, Dazai, Agrat, Khonsu)
    'LV_E2330': [Demon_Sync(1151,578),Demon_Sync(561)],#Discovering Salted Village (Dazai, Yuzuru)
    'LV_E2440': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(391, 569)], #Qadistu Dream ??? (Naamah II ,Agrat,Eisheth,Lilith)
    'LV_E2519': [Demon_Sync(550), Demon_Sync(567)],#First Nuwa/Yakumo scene in Shinjuku(Nuwa, Yakumo)
    'LV_E2560': [Demon_Sync(550), Demon_Sync(567)],#Nuwa/Yakumo talk at Mastema's hill 1(Nuwa, Yakumo)
    'LV_E2605': [Demon_Sync(1151,578),Demon_Sync(561)],#Dazai and Yuzuru become friends (Dazai, Yuzuru)
    'LV_E2623': [Demon_Sync(7,566),Demon_Sync(1151,578),Demon_Sync(561)], #Khonsu pre-fight dialogue vengeance part 2 (Khonsu, Yuzuru, Dazai)
    'LV_E2640': [Demon_Sync(596),Demon_Sync(1151,578)],#Arriving at Mastema's hill (Mastema,Dazai)
    'LV_E2643': [Demon_Sync(596),Demon_Sync(1151,578)],#Dazai turns to salt (Mastema,Dazai)
    'LV_E2645': [Demon_Sync(596),Demon_Sync(1151,578)], #Mastema brainwashes Dazai (Mastema, Dazai)
    'LV_E2648': [Demon_Sync(393, 554)],#Naamah in Shinjuku (Naamah)
    'LV_E2680': [Demon_Sync(561),Demon_Sync(567), Demon_Sync(550)],#Yakumo COV pre-fight dialogue (Yuzuru, Yakumo, Nuwa)
    'LV_E2685': [Demon_Sync(561),Demon_Sync(567), Demon_Sync(550)],#Yakumo COV post-fight dialogue (Yuzuru, Yakumo, Nuwa)
    'LV_E2700': [Demon_Sync(-396,568)],#Meeting Agrat
    'LV_E2703': [Demon_Sync(568)],#Agrat pre-fight
    'LV_E2705': [Demon_Sync(568),Demon_Sync(394, 559),Demon_Sync(393, 554)],#Agrat post-fight dialogue (Agrat, Eisheth, Naamah)
    'LV_E2713': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(-395, 569)],#Lilith pre-fight dialogue (Naamah II ,Agrat,Eisheth,Lilith)
    'LV_E2717': [Demon_Sync(393, 554),Demon_Sync(392, 568),Demon_Sync(559),Demon_Sync(-395, 569)],#Lilith post-fight dialogue (Naamah II ,Agrat,Eisheth,Lilith)
    'LV_E2720': [Demon_Sync(596),Demon_Sync(-459,565),Demon_Sync(550),Demon_Sync(564),Demon_Sync(1151,578),Demon_Sync(561),Demon_Sync(550)],#Timat Unleashed (Mastema,Tiamat,Nuwa,Abdiel,Dazai,Yuzuru,Yakumo)
    'LV_E2740': [Demon_Sync(578),Demon_Sync(561),Demon_Sync(564)],#Dazai hat cutscene vengeance (Dazai (Hatless), Yuzuru, Abdiel) 
    'LV_E2920': [Demon_Sync(564)], #Abdiel in Shakan pre-fight dialogue 
    'LV_E3040': [Demon_Sync(567)], #Yakumo in Jojozi (Yakumo)
    'LV_E3100': [Demon_Sync(483),Demon_Sync(468)], #Beelzebub pre-fight dialogue(Beelzebub, Vasuki)
    'LV_E3120': [Demon_Sync(482),Demon_Sync(481)], #Zeus + Odin pre-fight dialogue (Odin,Zeus)
    'LV_E3300': [Demon_Sync(578),Demon_Sync(577)], #Dazai pre-fight dialogue (Dazai, Abdiel)
    'LV_E3310': [Demon_Sync(578),Demon_Sync(577)],#Dazai post-fight dialogue (Dazai, Abdiel)
    'LV_E3350': [Demon_Sync(-459,565)], #Yoko uses Tiamat on you (Tiamat)
    #'LV_E3352': [Demon_Sync(-459,565)], #Tiamat post-fight (Tiamat) #Json erialization crashes, but is error with UassetAPI (consider re-adding if rewrite without json serialization)
    'LV_E3355': [Demon_Sync(597)],#Tehom pre-fight dialogue (Tehom)
    'LV_E3358': [Demon_Sync(597)],#Tehom post?-fight dialogue (Tehom)
    'LV_E3390': [Demon_Sync(596)],#Siding with Yoko (Mastema)
    'LV_E3400': [Demon_Sync(596)],#Siding with Yoko (Mastema)
    'LV_E3410': [Demon_Sync(596),Demon_Sync(-459,565)],#Mastema uses Tiamat on you (Mastema,Tiamat)
    #'LV_E3415': [Demon_Sync(596),Demon_Sync(-459,565)],#Tiamat post-fight chaos (Mastema,Tiamat)
    'LV_E3420': [Demon_Sync(596)],#Mastema pre-fight dialogue (Mastema)
    'LV_E3425': [Demon_Sync(596)],#Mastema post-fight dialogue (Mastema)
    'LV_E3480': [Demon_Sync(391, 569)], #Some CoV Chaos Ending Cutscene (Lilith)

}   

#Script files for events and what demon models need to be updated in htem
#Demon_Sync(demonID in file, if different from demonID in file: demonID to take replacement from)
EVENT_SCRIPT_MODELS = {
    #Initial & Mainmission M061 (Minato)
    'EM_M061_DevilTalk': [Demon_Sync(59)], #Talk Tutorial (Pixie)
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
    'MM_M060_Npc609Talk': [Demon_Sync(152)], #CoC Yuzuru Hayataro NPC Event? (Hayataro)
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
    'MM_M064_E2644_Direct': [Demon_Sync(596)], #Dazai got salted (Mastema)
    'MM_M064_E2650_Direct': [Demon_Sync(550),Demon_Sync(567)], #Nuwa/Yakumo talk after seeing Naamah (Nuwa, Yakumo)
    'MM_M064_E2690': [Demon_Sync(486)], #Dead Cherubim
    'MM_M064_E2900': [Demon_Sync(596)],#Mastema sends you to Shakan
    'MM_M064_E2950_Direct': [Demon_Sync(596)],#Mastema after Shakan
    #Mainmission M080 (Dorm Roof) 
    'MM_M080_E2670_Direct': [Demon_Sync(561)], #Yuzuru wants to be a Nahobino
    #Mainmission M082 (School Outside)
    'MM_M082_E3030_Direct': [Demon_Sync(561)],#Yakumo saves a student
    #Mainmission M083 (Shinagawa Station Real Tokyo ) 
    'MM_M083_E2160_Direct': [Demon_Sync(75,435),Demon_Sync(567)], #Labolas 2 post-fight (Yakumo,Nuwa)
    #Mainmission M085 (Top Room of Tokyo Building whose name I do not remember)
    'MM_M085_E0690': [Demon_Sync(-617,528)], #Koshimizu meeting after area 3 CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E0730': [Demon_Sync(-617,528)], #Regarding the war of the gods scene CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E0730_ready': [Demon_Sync(-617,528)], #End of Regarding the war of the gods scene CoC (Koshimizu using Tsukuyomi Replacement)
    'MM_M085_E2420': [Demon_Sync(561)],#Yuzuru apologizes for attacking you (Yuzuru) (NOT YET TESTED IN GAME)
    'MM_M085_E2445': [Demon_Sync(152,562)],#Koshimizu meeting after salt investigation (Hayataro) (NOT YET TESTED IN GAME)
    'MM_M085_E2575_Direct': [Demon_Sync(1151,578)], #Dazai talk when Miyazu goes to Khonsu (Dazai) (NOT YET TESTED IN GAME)
    'MM_M085_E2630_Direct': [Demon_Sync(1151,578),Demon_Sync(561)],#Yuzuru talk after Khonsu incident (Yuzuru, Dazai)
    'MM_M085_E2635_Direct': [Demon_Sync(1151,578)], #Dazai joins to see Mastema 1 
    'MM_M085_E2660': [Demon_Sync(561)], #Koshimizu meeting before Yakumo fight(Yuzuru)
    'MM_M085_E2688': [Demon_Sync(561)], #Koshimizu meeting after Yakumo fight (Yuzuru)
    #Mainmission M087 (Shrine Vengeance (Normal Lightning)) (NOT YET TESTED)
    'MM_M087_E2450_Direct': [Demon_Sync(1151,578)],#Dazai goes to Chiyoda #TODO: This has a bead that Could be included as event item randomization
    #Mainmission M088 (Summit)
    'MM_M088_E0602_Abdiel': [Demon_Sync(467)], #Summmit (Abdiel)
    'MM_M088_E0602_Khons': [Demon_Sync(516)], #Summmit (Khonsu)
    'MM_M088_E0602_Koshimizu': [Demon_Sync(-617,528)], #Summmit (Koshimizu as Tsukuyomi Replacement)
    'MM_M088_E0602_Vasuki': [Demon_Sync(468)], #Summmit (Vasuki)
    'MM_M088_E0602_Odin': [Demon_Sync(470)], #Summmit (Odin)
    'MM_M088_E0602_Zeus': [Demon_Sync(469)], #Summmit (Zeus)
    #Mainmission M092 (School Attacked)
    'MM_M092_EM101_': [Demon_Sync(446)], #School Oni [63] (Down in the Direction where Jack is looking)
    'MM_M092_EM102_': [Demon_Sync(488),Demon_Sync(491)], #School Andras + Rakshasa [56] (First Floor Hallway)
    'MM_M092_EM104': [Demon_Sync(496)], #School Incubus [58] (Fake School Girl)
    'MM_M092_EM105_1': [Demon_Sync(449)], #School Tsuchigumo [62] (Second Floor Hallway)
    'MM_M092_EM106_': [Demon_Sync(501),Demon_Sync(448)], #School Manananggal +Shiki Ouji [66] (CoV 3rd Floor Corner from Far 2nd Floor Staircase, CoC 3rd Floor Hallway)
    'MM_M092_EM107_': [Demon_Sync(492),Demon_Sync(495)], #School Rakshasa + Incubus [57] (Left at the Entrance)
    'MM_M092_EM108_': [Demon_Sync(493)], #School Rakshasa [59] (2nd Floor Corner)
    'MM_M092_EM109_a': [Demon_Sync(500)], #School Save Jack Frost (Manananggal) [64]
    'MM_M092_EM110': [Demon_Sync(497)], #School Incubus [61] (CoV 3rd Floor Hallway, CoC  3rd Floor Corner from Far 2nd Floor Staircase)
    'MM_M092_EM111': [Demon_Sync(487),Demon_Sync(502)], #School Aitvaras + Shiki Ouji [61][65] (4th Floor, Encounter depends on choice)
    'MM_M092_EM112_': [Demon_Sync(502),Demon_Sync(447),Demon_Sync(443)], #School Optional Multiple Fights [65][129][60] (Manananggal,Shiki Ouji,Andras) (4th Floor Far Corner)
    #Mainmission M115 (Dorm Room) 
    'MM_M115_E2603_Direct': [Demon_Sync(1151,578), Demon_Sync(561)], #Dazai/Yuzuru in dorm room
    #Mainmission M203 (Qadistu Dimension)
    'MM_M203_E2718_Direct': [Demon_Sync(569)], #Lilith post-fight lecture

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
    'MM_M107_EM1825_Hit': [Demon_Sync(934)], #Demi-Fiend (Fight/Join Prompt)

    #SubMission M035 & M036 (Empyrean & DKC)
    'MM_M035_EM1480': [Demon_Sync(242)], # The Seraph's Return (Michael)
    'MM_M035_EM1491': [Demon_Sync(242)], # The Red Dragon's Invitation (Michael)
    'MM_M036_EM1490': [Demon_Sync(83)], # The Red Dragon's Invitation (Belial)
    'MM_M036_EM1481': [Demon_Sync(83)], # The Seraph's Return (Belial)

    #SubMission M050 (Tokyo Map)
    'MM_M201_EM2411': [Demon_Sync(754)], #Turbo Granny Quest (Turbo Granny)

    #SubMission M061 (Minato)
    'MM_M061_EM0021': [Demon_Sync(433),Demon_Sync(434)], #Eligor and Andras Event
    'MM_M061_EM1031': [Demon_Sync(801)], #Pazuzu Event Mermaid Quest
    'MM_M061_EM1041': [Demon_Sync(803)], #Anahita Event Mermaid Quest 2
    'MM_M061_EM1050_New': [Demon_Sync(820)], #Talisman Hunt (Shiki Ouji)
    'MM_M061_EM1360': [Demon_Sync(861)], #Koumokuten Event Battle Dialogue
    'MM_M061_EM1383': [Demon_Sync(870)], #Seth Event Battle Dialogue
    'MM_M061_EM1630': [Demon_Sync(305),Demon_Sync(43)], # The Water Nymph (Leanan (also Apsaras maybe??))
    'MM_M061_EM1631': [Demon_Sync(316,867)], # The Water Nymph (Ippon-Datara)
    'MM_M061_EM1640': [Demon_Sync(43),Demon_Sync(44,869)], # The Spirit of Love (Apsaras, Agathion)
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
    'MM_M061_EM2380': [Demon_Sync(781)], #Mo Shuvuu Quest (Andras)

    #SubMission M062 (Shinagawa)
    'MM_M062_EM1141': [Demon_Sync(809)], #Kumbhanda Bottle Quest (Kumbhanda)
    'MM_M062_EM1151_Hit': [Demon_Sync(810)], #A Goddess Stolen (Loki)
    'MM_M062_EM1160': [Demon_Sync(19)], #The Tyrant of Tennozu (Demeter)
    'MM_M062_EM1161_A': [Demon_Sync(804)], #The Tyrant of Tennozu  (Belphegor)
    'MM_M062_EM1181': [Demon_Sync(821)], #King Frost Quest (King Frost) 
    'MM_M062_EM1331': [Demon_Sync(828)],#Lord's Sword Quest (Arahabaki)  
    'MM_M062_EM1340': [Demon_Sync(860)], #Zouchouten Event Battle  
    'MM_M062_EM1401': [Demon_Sync(519),Demon_Sync(516)], #Khonsu Ra CoC Quest (Khonsu Ra, Khonsu)  
    'MM_M062_EM1402': [Demon_Sync(519),Demon_Sync(516)], #Khonsu Ra CoC Quest (Khonsu Ra, Khonsu)  
    'MM_M062_EM1650': [Demon_Sync(67)], # Lilim/Principality Quest (Lilim)
    'MM_M062_EM1660': [Demon_Sync(257)], # Lilim/Principality Quest (Principality)
    'MM_M062_EM2040': [Demon_Sync(803)], #Pisaca Quest part 1 (Anahita)  #TODO: where is this event even?
    'MM_M062_EM2090': [Demon_Sync(561),Demon_Sync(562)],  #Yuzuru Supply Run Quest (Yuzuru, Hayataro) 
    'MM_M062_EM2490': [Demon_Sync(122)], #Brawny Ambitions II (Xiezhai)
    'esNPC_em1650_01': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_02': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_03': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_04': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim)
    'esNPC_em1650_05': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim) 
    'esNPC_em1650_06': [Demon_Sync(880)], # Lilim/Principality Quest NPCs (Lilim)
    'MM_M062_EM2110_Enemy': [Demon_Sync(769)], #Vouivre Quest (Vouivre) 
    'MM_M062_EM2440': [Demon_Sync(768)], #Amanozako Control Quest(Yakshini)

    #SubMission M063 (Chiyoda)
    'MM_M063_EM1210': [Demon_Sync(824),Demon_Sync(826)], #Oyamatsumi Quest (Take-Minakata,Oyamatsumi)
    'MM_M063_EM1211': [Demon_Sync(826)], #Oyamatsumi Quest (Oyamatsumi)
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
    'MM_M063_EM2580': [Demon_Sync(776)], #Yoshitsune Haunt Quest (Atavaka)

    #SubMission M064 (Shinjuku)
    'MM_M064_EM1260': [Demon_Sync(19)], #Demeter Defeat Chimera Shinjuku (Demeter)
    'MM_M064_EM1261': [Demon_Sync(812)], #Demeter Defeat Chimera Shinjuku (Chimera)
    'MM_M064_EM1281': [Demon_Sync(814)], #The Archangel of Destruction Shinjuku(Camael)
    'MM_M064_EM1291': [Demon_Sync(816)], #Roar of Hatred Shinjuku(Moloch)
    'MM_M064_EM1391': [Demon_Sync(829),Demon_Sync(830)], #Winged Sun (Mithras, Asura) 
    'MM_M064_EM2130': [Demon_Sync(41), Demon_Sync(386)], #Basilisk Hunt Quest (Anansi, Onyankopon)
    'MM_M064_EM2131': [Demon_Sync(41)], #Basilisk Hunt Quest (Anansi)
    'MM_M064_EM2270': [Demon_Sync(40)], #Kresnik Kudlak Quest (Kresnik) 
    'MM_M064_EM2280': [Demon_Sync(346)], #Kresnik Kudlak Quest (Kudlak)
    'MM_M064_EM2310': [Demon_Sync(386, 770), Demon_Sync(41)], #Onyakopon Anansi Quest (Onyakopon Side)
    'MM_M064_EM2320': [Demon_Sync(41, 771), Demon_Sync(386)], #Onyakopon Anansi Quest (Anansi Side)
    'MM_M064_EM2400': [Demon_Sync(596)], #Samael Quest (Mastema) 
    'MM_M064_EM2402': [Demon_Sync(760)], #Samael Quest (Samael) 
    'MM_M064_EM2421_Direct': [Demon_Sync(681)], #Satan Quest (Satan) 
    'MM_M064_EM2461': [Demon_Sync(892)], #Mara Quest (Mara) 
    'MM_M064_EM2500': [Demon_Sync(215)], #Brawny Ambitions III (Okuninushi) 
    'MM_M064_EM2552': [Demon_Sync(509)], #MadGasser Quest (Zhen (3xCopy))
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
    'MM_M060_EM1600': [Demon_Sync(878)],  #Final Amanozako Quest (Kurama Tengu) 
    'MM_M060_EM1601': [Demon_Sync(878),Demon_Sync(38),Demon_Sync(877)], #Final Amanozako Quest (Kurama Tengu,Amanozako, Zaou Gongen)
    'MM_M060_EM1602': [Demon_Sync(38)],  #Final Amanozako Quest (Amanozako) 
    'MM_M060_EM1690': [Demon_Sync(265)],  #Adramelech Futsunushi Quest (Adramalech) 
    'MM_M060_EM1700': [Demon_Sync(201)],  #Adramelech Futsunushi Quest (Futsunushi) 
    'MM_M060_EM2371': [Demon_Sync(865)],  #Garuda Quest (Garuda) 
    'MM_M060_EM2570': [Demon_Sync(22, 779)], #Moirae Haunt Quest (Norn)
    'MM_M060_EM2630': [Demon_Sync(782)],  #Saturnus Quest(Saturnus) 
    'MM_M061_EM2705': [Demon_Sync(207)], # The Guardian of Light (Marici)

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
    'MM_M038_E2930_Direct': [Anim_Sync('Event/EVT_E0604c01m_loop','04dying')], #Shakan Abdiel Post Fight
    'MM_M060_E762': [Anim_Sync('map/700000_event_idle', '01idleA')],#Nuwa in area 4 at the gate
    'MM_M060_E3020': [Anim_Sync('Event/EVT_v_turnwalk_inout','11run')], #Yakumo in area 4 vengeance part 2
    'MM_M062_E0380': [Anim_Sync('Map/700002_event_idle','01idleA')], #Fionn 1 Post-fight (Fionn)
    'MM_M062_E0492': [Anim_Sync('3rd_01idleA','01idleA'),Anim_Sync('3rd_41encount','41encount')], #Final Lahmu (Lahmu Phase 2)
    #'MM_M062_EM0041': [Anim_Sync('Event/EVT_SlowEncount_inout','41encount')], #Loup-garous Event
    'MM_M062_E2295_Direct': [Anim_Sync('02idleB','05attack')],#Eisheth pre-fight
    'MM_M062_E2298_Direct': [Anim_Sync('Map/700002_event_idle','01idleA')], #Fionn 1 Post-fight Vengeance (Fionn)
    'MM_M064_E2690': [Anim_Sync('map/700000_dead01','04dying'),Anim_Sync('map/700001_dead02','04dying')], #Dead Cherubim
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
    'MM_M062_EM1680': [Anim_Sync('06skill_Composite','06skill')],#Black Frost Dionysus Quest (Dionysus)
    'MM_M064_EM1281': [Anim_Sync('21skillB','06skill')],#The Archangel of Destruction Shinjuku (Camael)
    'MM_M064_EM2130': [Anim_Sync('02idleB','05attack'),Anim_Sync('map/700020_stick','14command'),Anim_Sync('map/700010_laugh','14command')], #Basilisk Hunt Quest (Anansi, Onyankopon)
    'MM_M064_EM2310': [Anim_Sync('02idleB','05attack')],#Onyakopon Anansi Quest (Onyakopon Side)
    'MM_M064_EM2400': [Anim_Sync('13skill_ex2','06skill')], #Samael Quest (Mastema)
    'MM_M064_EM2421_Direct': [Anim_Sync('13skill_ex3_Composite','05attack')], #Satan Quest (Satan)
    'MM_M064_EM2552': [Anim_Sync('map/700002_event_idle','11run'),Anim_Sync('map/700000_event_idle','02idleB'),Anim_Sync('map/700001_event_notice','05attack')], #MadGasser Quest (Zhen (3xCopy))
    'MM_M060_EM1381': [Anim_Sync('09skill_d','06skill'),Anim_Sync('09skill_c','06skill'),Anim_Sync('02idleB','14command')], #Winge Sun CoC (Amon,Khonsu)
    'MM_M060_EM1420': [Anim_Sync('Map/700002_event_idle','14command'),Anim_Sync('Map/700000_event_idle','51yes')], #Fionn 2 Quest (Fionn)
    'MM_M060_EM1440': [Anim_Sync('02idleB','14command')], #Baal Quest (Demeter)
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

}


LV_SEQUENCES = {
    'LV_E0180': ['SEQ_E0180_c01','SEQ_E0180_c02','SEQ_E0180_c03','SEQ_E0180_c04','SEQ_E0180_c05','SEQ_E0180_c06','SEQ_E0180_c07','SEQ_E0180_c08','SEQ_E0180_c09'], #Triple Preta Cutscene
    'LV_E0310': ['SEQ_E0310_c01', 'SEQ_E0310_c02', 'SEQ_E0310_c03', 'SEQ_E0310_c05', 'SEQ_E0310_c06', 'SEQ_E0310_c07', 'SEQ_E0310_c08', 'SEQ_E0310_c09'],
    'LV_E0330': ['SEQ_E0330_c01','SEQ_E0330_c02','SEQ_E0330_c03','SEQ_E0330_c04','SEQ_E0330_c06','SEQ_E0330_c08','SEQ_E0330_c09','SEQ_E0330_c10','SEQ_E0330_c10B','SEQ_E0330_c11','SEQ_E0330_c13','SEQ_E0330_c14','SEQ_E0330_c15','SEQ_E0330_c16','SEQ_E0330_c17','SEQ_E0330_c20'], #UMAP Snake Nuwa Pre-fight Cutscene (Nuwa, Snake Nuwa)
    'LV_E0340': ['SEQ_E0340_c01','SEQ_E0340_c02','SEQ_E0340_c02B','SEQ_E0340_c04','SEQ_E0340_c04B','SEQ_E0340_c05','SEQ_E0340_c06','SEQ_E0340_c07','SEQ_E0340_c08','SEQ_E0340_c09','SEQ_E0340_c11','SEQ_E0340_c12','SEQ_E0340_c13',], #UMAP Snake Nuwa Post-fight Cutscene (Yakumo, Nuwa, Snake Nuwa)
    'LV_E0350': ['SEQ_E0350_c01','SEQ_E0350_c02','SEQ_E0350_c03','SEQ_E0350_c04','SEQ_E0350_c06','SEQ_E0350_c07','SEQ_E0350_c08','SEQ_E0350_c09B','SEQ_E0350_c10','SEQ_E0350_c11','SEQ_E0350_c12','SEQ_E0350_c13','SEQ_E0350_c14','SEQ_E0350_c14A','SEQ_E0350_c14B','SEQ_E0350_c15','SEQ_E0350_c16','SEQ_E0350_c16B','SEQ_E0350_c17','SEQ_E0350_c18','SEQ_E0350_c19'], #UMAP Meeting Abdiel Cutscene
    'LV_E0375': ['SEQ_E0375_c01','SEQ_E0375_c01B','SEQ_E0375_c02','SEQ_E0375_c03','SEQ_E0375_c04','SEQ_E0375_c05','SEQ_E0375_c06','SEQ_E0375_c07','SEQ_E0375_c08','SEQ_E0375_c09','SEQ_E0375_c10','SEQ_E0375_c11','SEQ_E0375_c12','SEQ_E0375_c13','SEQ_E0375_c14','SEQ_E0375_c15',], #UMAP Hayataro in Beginning of Shinagawa Cutscene
    'LV_E0379': ['SEQ_E0379_c01','SEQ_E0379_c02','SEQ_E0379_c03','SEQ_E0379_c04','SEQ_E0379_c05','SEQ_E0379_c06','SEQ_E0379_c07','SEQ_E0379_c08','SEQ_E0379_c08B','SEQ_E0379_c09','SEQ_E0379_c10',], #UMAP Fionn 1 Cutscene
    'LV_E0431': ['SEQ_E0431_c01', 'SEQ_E0431_c02', 'SEQ_E0431_c02B', 'SEQ_E0431_c03', 'SEQ_E0431_c04', 'SEQ_E0431_c04B', 'SEQ_E0431_c04C', 'SEQ_E0431_c05', 'SEQ_E0431_c05B', 'SEQ_E0431_c05C', 'SEQ_E0431_c07', 'SEQ_E0431_c08', 'SEQ_E0431_c09', 'SEQ_E0431_c10'],
    'LV_E0432': ['SEQ_E0432_c03', 'SEQ_E0432_c05', 'SEQ_E0432_c06', 'SEQ_E0432_c08', 'SEQ_E0432_c10'],
    'LV_E0470': ['SEQ_E0470_c01', 'SEQ_E0470_c02', 'SEQ_E0470_c03', 'SEQ_E0470_c04', 'SEQ_E0470_c04B', 'SEQ_E0470_c05', 'SEQ_E0470_c06A', 'SEQ_E0470_c07', 'SEQ_E0470_c08', 'SEQ_E0470_c09', 'SEQ_E0470_c10', 'SEQ_E0470_c11', 'SEQ_E0470_c12', 'SEQ_E0470_c13', 'SEQ_E0470_c14', 'SEQ_E0470_c15'],
    'LV_E0473': ['SEQ_E0473_c01', 'SEQ_E0473_c02', 'SEQ_E0473_c03', 'SEQ_E0473_c04', 'SEQ_E0473_c05', 'SEQ_E0473_c06', 'SEQ_E0473_c07'],
    'LV_E0480': ['SEQ_E0480_c01', 'SEQ_E0480_c02', 'SEQ_E0480_c04', 'SEQ_E0480_c05', 'SEQ_E0480_c06', 'SEQ_E0480_c07', 'SEQ_E0480_c07B', 'SEQ_E0480_c08', 'SEQ_E0480_c10', 'SEQ_E0480_c11', 'SEQ_E0480_c12', 'SEQ_E0480_c12B', 'SEQ_E0480_c13', 'SEQ_E0480_c14', 'SEQ_E0480_c14B', 'SEQ_E0480_c15', 'SEQ_E0480_c16', 'SEQ_E0480_c17', 'SEQ_E0480_c17B', 'SEQ_E0480_c18', 'SEQ_E0480_c19', 'SEQ_E0480_c20', 'SEQ_E0480_c20B', 'SEQ_E0480_c20C', 'SEQ_E0480_c20D', 'SEQ_E0480_c21', 'SEQ_E0480_c21B', 'SEQ_E0480_c22', 'SEQ_E0480_c23', 'SEQ_E0480_c24B', 'SEQ_E0480_c27'],
    'LV_E0490': ['SEQ_E0490_c01', 'SEQ_E0490_c02', 'SEQ_E0490_c02B', 'SEQ_E0490_c03', 'SEQ_E0490_c04', 'SEQ_E0490_c05', 'SEQ_E0490_c06', 'SEQ_E0490_c07', 'SEQ_E0490_c08', 'SEQ_E0490_c09A', 'SEQ_E0490_c09B', 'SEQ_E0490_c10', 'SEQ_E0490_c11', 'SEQ_E0490_c12', 'SEQ_E0490_c13', 'SEQ_E0490_c14', 'SEQ_E0490_c15', 'SEQ_E0490_c16', 'SEQ_E0490_c17'],
    'LV_E0530': ['SEQ_E0530_c01', 'SEQ_E0530_c02', 'SEQ_E0530_c03', 'SEQ_E0530_c04', 'SEQ_E0530_c05', 'SEQ_E0530_c07', 'SEQ_E0530_c08', 'SEQ_E0530_c09', 'SEQ_E0530_c10', 'SEQ_E0530_c10B', 'SEQ_E0530_c10C', 'SEQ_E0530_c10D', 'SEQ_E0530_c10E', 'SEQ_E0530_c11', 'SEQ_E0530_c12'],
    'LV_E0580': ['SEQ_E0580_c01', 'SEQ_E0580_c02', 'SEQ_E0580_c03', 'SEQ_E0580_c08', 'SEQ_E0580_c09', 'SEQ_E0580_c10', 'SEQ_E0580_c11', 'SEQ_E0580_c12', 'SEQ_E0580_c13', 'SEQ_E0580_c14', 'SEQ_E0580_c15'],
    'LV_E0595': ['SEQ_E0595_c01', 'SEQ_E0595_c01A', 'SEQ_E0595_c01C', 'SEQ_E0595_c02', 'SEQ_E0595_c03', 'SEQ_E0595_c04'],
    'LV_E0598': ['SEQ_E0598_c01', 'SEQ_E0598_c02', 'SEQ_E0598_c03', 'SEQ_E0598_c04', 'SEQ_E0598_c05', 'SEQ_E0598_c06'],
    'LV_E0600': ['SEQ_E0600_c00', 'SEQ_E0600_c00B', 'SEQ_E0600_c01', 'SEQ_E0600_c01B', 'SEQ_E0600_c02', 'SEQ_E0600_c03', 'SEQ_E0600_c04', 'SEQ_E0600_c05', 'SEQ_E0600_c06', 'SEQ_E0600_c08', 'SEQ_E0600_c08B', 'SEQ_E0600_c09'],
    'LV_E0603': ['SEQ_E0603_c01', 'SEQ_E0603_c02', 'SEQ_E0603_c03', 'SEQ_E0603_c04', 'SEQ_E0603_c05', 'SEQ_E0603_c06', 'SEQ_E0603_c06B', 'SEQ_E0603_c07', 'SEQ_E0603_c08', 'SEQ_E0603_c09', 'SEQ_E0603_c10', 'SEQ_E0603_c10B', 'SEQ_E0603_c10C', 'SEQ_E0603_c10D', 'SEQ_E0603_c11', 'SEQ_E0603_c12'],
    'LV_E0604': ['SEQ_E0604_c01', 'SEQ_E0604_c02', 'SEQ_E0604_c03', 'SEQ_E0604_c04', 'SEQ_E0604_c05', 'SEQ_E0604_c06', 'SEQ_E0604_c07', 'SEQ_E0604_c08', 'SEQ_E0604_c09', 'SEQ_E0604_c10', 'SEQ_E0604_c11', 'SEQ_E0604_c12', 'SEQ_E0604_c16'],
    'LV_E0620': ['SEQ_E0620_c01', 'SEQ_E0620_c01B', 'SEQ_E0620_c02', 'SEQ_E0620_c03', 'SEQ_E0620_c04', 'SEQ_E0620_c05', 'SEQ_E0620_c05A', 'SEQ_E0620_c05B', 'SEQ_E0620_c06', 'SEQ_E0620_c07', 'SEQ_E0620_c08', 'SEQ_E0620_c09', 'SEQ_E0620_c10', 'SEQ_E0620_c12', 'SEQ_E0620_c13', 'SEQ_E0620_c14'],
    'LV_E0630': ['SEQ_E0630_c01', 'SEQ_E0630_c02', 'SEQ_E0630_c03', 'SEQ_E0630_c04', 'SEQ_E0630_c05', 'SEQ_E0630_c06', 'SEQ_E0630_c07', 'SEQ_E0630_c08', 'SEQ_E0630_c09A', 'SEQ_E0630_c09B', 'SEQ_E0630_c10', 'SEQ_E0630_c11'],
    'LV_E0660': ['SEQ_E0660_c01', 'SEQ_E0660_c03', 'SEQ_E0660_c04', 'SEQ_E0660_c05', 'SEQ_E0660_c06', 'SEQ_E0660_c07', 'SEQ_E0660_c08'],
    'LV_E0736': ['SEQ_E0736_c01', 'SEQ_E0736_c02', 'SEQ_E0736_c03', 'SEQ_E0736_c04', 'SEQ_E0736_c04B', 'SEQ_E0736_c05', 'SEQ_E0736_c06', 'SEQ_E0736_c07', 'SEQ_E0736_c07B', 'SEQ_E0736_c08', 'SEQ_E0736_c08B', 'SEQ_E0736_c09', 'SEQ_E0736_c10', 'SEQ_E0736_c11', 'SEQ_E0736_c12', 'SEQ_E0736_c12B', 'SEQ_E0736_c13', 'SEQ_E0736_c14', 'SEQ_E0736_c14B', 'SEQ_E0736_c14C'],
    'LV_E0775': ['SEQ_E0775_c01', 'SEQ_E0775_c02', 'SEQ_E0775_c03', 'SEQ_E0775_c04', 'SEQ_E0775_c05'],
    'LV_E0785': ['SEQ_E0785_c01', 'SEQ_E0785_c02', 'SEQ_E0785_c02B', 'SEQ_E0785_c03', 'SEQ_E0785_c04', 'SEQ_E0785_c05'],
    'LV_E0805': ['SEQ_E0805_c01', 'SEQ_E0805_c02', 'SEQ_E0805_c03', 'SEQ_E0805_c03A', 'SEQ_E0805_c03B', 'SEQ_E0805_c03s', 'SEQ_E0805_c04', 'SEQ_E0805_c05'],
    'LV_E0841': ['SEQ_E0841_c01', 'SEQ_E0841_c02a', 'SEQ_E0841_c02b', 'SEQ_E0841_c03', 'SEQ_E0841_c04', 'SEQ_E0841_c05'],
    'LV_E0842': ['SEQ_E0842_c01', 'SEQ_E0842_c03', 'SEQ_E0842_c04', 'SEQ_E0842_c05', 'SEQ_E0842_c07', 'SEQ_E0842_c08', 'SEQ_E0842_c09'],
    'LV_E0850': ['SEQ_E0850_c01', 'SEQ_E0850_c02', 'SEQ_E0850_c03', 'SEQ_E0850_c04', 'SEQ_E0850_c05', 'SEQ_E0850_c06', 'SEQ_E0850_c07', 'SEQ_E0850_c08', 'SEQ_E0850_c09', 'SEQ_E0850_c10', 'SEQ_E0850_c11', 'SEQ_E0850_c12', 'SEQ_E0850_c13', 'SEQ_E0850_c14', 'SEQ_E0850_c15', 'SEQ_E0850_c19', 'SEQ_E0850_c20', 'SEQ_E0850_c21', 'SEQ_E0850_c23', 'SEQ_E0850_c23B', 'SEQ_E0850_c25', 'SEQ_E0850_c26', 'SEQ_E0850_c27', 'SEQ_E0850_c29', 'SEQ_E0850_c30', 'SEQ_E0850_c30B', 'SEQ_E0850_c30C', 'SEQ_E0850_c33', 'SEQ_E0850_c34', 'SEQ_E0850_c49', 'SEQ_E0850_c50', 'SEQ_E0850_c50B', 'SEQ_E0850_c50C', 'SEQ_E0850_c51', 'SEQ_E0850_c52', 'SEQ_E0850_c53', 'SEQ_E0850_c53B', 'SEQ_E0850_c54', 'SEQ_E0850_c54C'],
    'LV_E0870': ['SEQ_E0870_c01', 'SEQ_E0870_c02', 'SEQ_E0870_c03', 'SEQ_E0870_c04', 'SEQ_E0870_c05', 'SEQ_E0870_c06', 'SEQ_E0870_c06B', 'SEQ_E0870_c07', 'SEQ_E0870_c08', 'SEQ_E0870_c09', 'SEQ_E0870_c10', 'SEQ_E0870_c11', 'SEQ_E0870_c12'],
    'LV_E0880': ['SEQ_E0880_c01', 'SEQ_E0880_c02', 'SEQ_E0880_c03', 'SEQ_E0880_c04', 'SEQ_E0880_c05', 'SEQ_E0880_c05B', 'SEQ_E0880_c06', 'SEQ_E0880_c07', 'SEQ_E0880_c08'],
    'LV_E0900': ['SEQ_E0900_c01', 'SEQ_E0900_c02', 'SEQ_E0900_c02B', 'SEQ_E0900_c03', 'SEQ_E0900_c04', 'SEQ_E0900_c05', 'SEQ_E0900_c05D', 'SEQ_E0900_c06', 'SEQ_E0900_c07', 'SEQ_E0900_c08C', 'SEQ_E0900_c10', 'SEQ_E0900_c11', 'SEQ_E0900_c12', 'SEQ_E0900_c13', 'SEQ_E0900_c14', 'SEQ_E0900_c15', 'SEQ_E0900_c16', 'SEQ_E0900_c17', 'SEQ_E0900_c18', 'SEQ_E0900_c19', 'SEQ_E0900_c20', 'SEQ_E0900_c21'],
    'LV_E0905': ['SEQ_E0905_c01', 'SEQ_E0905_c02', 'SEQ_E0905_c03', 'SEQ_E0905_c04', 'SEQ_E0905_c05'],
    'LV_E0910': ['SEQ_E0910_c01', 'SEQ_E0910_c02', 'SEQ_E0910_c03', 'SEQ_E0910_c04', 'SEQ_E0910_c05', 'SEQ_E0910_c05B', 'SEQ_E0910_c06', 'SEQ_E0910_c07', 'SEQ_E0910_c07B', 'SEQ_E0910_c08', 'SEQ_E0910_c08B', 'SEQ_E0910_c08C', 'SEQ_E0910_c10', 'SEQ_E0910_c11', 'SEQ_E0910_c12', 'SEQ_E0910_c13', 'SEQ_E0910_c14', 'SEQ_E0910_c16', 'SEQ_E0910_c17', 'SEQ_E0910_c18', 'SEQ_E0910_c19', 'SEQ_E0910_c20', 'SEQ_E0910_c21'],
    'LV_E0915': ['SEQ_E0915_c01', 'SEQ_E0915_c02', 'SEQ_E0915_c03', 'SEQ_E0915_c04', 'SEQ_E0915_c05'],
    'LV_E0920': ['SEQ_E0920_c01', 'SEQ_E0920_c02', 'SEQ_E0920_c03', 'SEQ_E0920_c04', 'SEQ_E0920_c04B', 'SEQ_E0920_c04C', 'SEQ_E0920_c05', 'SEQ_E0920_c05B', 'SEQ_E0920_c06', 'SEQ_E0920_c07', 'SEQ_E0920_c08', 'SEQ_E0920_c08C', 'SEQ_E0920_c09', 'SEQ_E0920_c10', 'SEQ_E0920_c11', 'SEQ_E0920_c110', 'SEQ_E0920_c116', 'SEQ_E0920_c12', 'SEQ_E0920_c13', 'SEQ_E0920_c14', 'SEQ_E0920_c15', 'SEQ_E0920_c16', 'SEQ_E0920_c17', 'SEQ_E0920_c18', 'SEQ_E0920_c19', 'SEQ_E0920_c20', 'SEQ_E0920_c21'],
    'LV_E0930': ['SEQ_E0930_c01', 'SEQ_E0930_c01B', 'SEQ_E0930_c02', 'SEQ_E0930_c03', 'SEQ_E0930_c04', 'SEQ_E0930_c05', 'SEQ_E0930_c06', 'SEQ_E0930_c06B', 'SEQ_E0930_c07', 'SEQ_E0930_c08'],
    'LV_E0940': ['SEQ_E0940_c00', 'SEQ_E0940_c01', 'SEQ_E0940_c02', 'SEQ_E0940_c03', 'SEQ_E0940_c04', 'SEQ_E0940_c05', 'SEQ_E0940_c06', 'SEQ_E0940_c07', 'SEQ_E0940_c08', 'SEQ_E0940_c09', 'SEQ_E0940_c10', 'SEQ_E0940_c11', 'SEQ_E0940_c12', 'SEQ_E0940_c13', 'SEQ_E0940_c14', 'SEQ_E0940_c15', 'SEQ_E0940_c16', 'SEQ_E0940_c17', 'SEQ_E0940_c17B', 'SEQ_E0940_c18', 'SEQ_E0940_c18B', 'SEQ_E0940_c20', 'SEQ_E0940_c21', 'SEQ_E0940_c22'],
    'LV_E0945': ['SEQ_E0945_c01', 'SEQ_E0945_c02', 'SEQ_E0945_c03', 'SEQ_E0945_c04', 'SEQ_E0945_c05'],
    'LV_E0955': ['SEQ_E0955_c01', 'SEQ_E0955_c02', 'SEQ_E0955_c03', 'SEQ_E0955_c04', 'SEQ_E0955_c05', 'SEQ_E0955_c06', 'SEQ_E0955_c07', 'SEQ_E0955_c08', 'SEQ_E0955_c10', 'SEQ_E0955_c15', 'SEQ_E0955_c16'],
    'LV_E0957': ['SEQ_E0957_c01', 'SEQ_E0957_c02', 'SEQ_E0957_c03', 'SEQ_E0957_c04', 'SEQ_E0957_c05', 'SEQ_E0957_c06', 'SEQ_E0957_c07', 'SEQ_E0957_c08', 'SEQ_E0957_c10', 'SEQ_E0957_c15', 'SEQ_E0957_c16'],
    'LV_E0960': ['SEQ_E0960_c00', 'SEQ_E0960_c01', 'SEQ_E0960_c02', 'SEQ_E0960_c03', 'SEQ_E0960_c04', 'SEQ_E0960_c05', 'SEQ_E0960_c06', 'SEQ_E0960_c07', 'SEQ_E0960_c08', 'SEQ_E0960_c09', 'SEQ_E0960_c10', 'SEQ_E0960_c11', 'SEQ_E0960_c12', 'SEQ_E0960_c13', 'SEQ_E0960_c13B', 'SEQ_E0960_c14', 'SEQ_E0960_c14B', 'SEQ_E0960_c15', 'SEQ_E0960_c16', 'SEQ_E0960_c17', 'SEQ_E0960_c18', 'SEQ_E0960_c19', 'SEQ_E0960_c20'],
    'LV_E0965': ['SEQ_E0965_c01', 'SEQ_E0965_c02', 'SEQ_E0965_c03', 'SEQ_E0965_c04', 'SEQ_E0965_c05'],
    'LV_E0975': ['SEQ_E0975_c01', 'SEQ_E0975_c02', 'SEQ_E0975_c03', 'SEQ_E0975_c04', 'SEQ_E0975_c05', 'SEQ_E0975_c06', 'SEQ_E0975_c07', 'SEQ_E0975_c08', 'SEQ_E0975_c10', 'SEQ_E0975_c15', 'SEQ_E0975_c16'],
    'LV_E1000': ['SEQ_E1000_c01', 'SEQ_E1000_c02', 'SEQ_E1000_c03', 'SEQ_E1000_c04', 'SEQ_E1000_c05'],
    'LV_E1010': ['SEQ_E1010_c01', 'SEQ_E1010_c01B', 'SEQ_E1010_c01C', 'SEQ_E1010_c01D', 'SEQ_E1010_c02', 'SEQ_E1010_c02B', 'SEQ_E1010_c03', 'SEQ_E1010_c04', 'SEQ_E1010_c05B', 'SEQ_E1010_c07', 'SEQ_E1010_c08', 'SEQ_E1010_c09'],
    'LV_E1015': ['SEQ_E1015_c01', 'SEQ_E1015_c02', 'SEQ_E1015_c02B', 'SEQ_E1015_c03', 'SEQ_E1015_c05', 'SEQ_E1015_c06', 'SEQ_E1015_c07'],
    'LV_E1100': ['SEQ_E1100_c01', 'SEQ_E1100_c01B', 'SEQ_E1100_c02', 'SEQ_E1100_c02B', 'SEQ_E1100_c03', 'SEQ_E1100_c04', 'SEQ_E1100_c04B', 'SEQ_E1100_c04C', 'SEQ_E1100_c05', 'SEQ_E1100_c06'],
    'LV_E2015': ['SEQ_E2015_c01', 'SEQ_E2015_c02', 'SEQ_E2015_c03', 'SEQ_E2015_c04', 'SEQ_E2015_c06', 'SEQ_E2015_c07', 'SEQ_E2015_c08', 'SEQ_E2015_c09', 'SEQ_E2015_c10', 'SEQ_E2015_c11', 'SEQ_E2015_c12', 'SEQ_E2015_c13', 'SEQ_E2015_c14', 'SEQ_E2015_c15'],
    'LV_E2010': ['SEQ_E2010_c01', 'SEQ_E2010_c02', 'SEQ_E2010_c03', 'SEQ_E2010_c04', 'SEQ_E2010_c05', 'SEQ_E2010_c06', 'SEQ_E2010_c07', 'SEQ_E2010_c07B', 'SEQ_E2010_c08a', 'SEQ_E2010_c08b', 'SEQ_E2010_c09', 'SEQ_E2010_c09B', 'SEQ_E2010_c10', 'SEQ_E2010_c11B', 'SEQ_E2010_c12', 'SEQ_E2010_c20', 'SEQ_E2010_c21', 'SEQ_E2010_c21B', 'SEQ_E2010_c22B', 'SEQ_E2010_c23', 'SEQ_E2010_c24', 'SEQ_E2010_c25', 'SEQ_E2010_c26'],
    'LV_E2020': ['SEQ_E2020_c01', 'SEQ_E2020_c02', 'SEQ_E2020_c03', 'SEQ_E2020_c04B', 'SEQ_E2020_c05', 'SEQ_E2020_c05B', 'SEQ_E2020_c06', 'SEQ_E2020_c08', 'SEQ_E2020_c09', 'SEQ_E2020_c09B'],
    'LV_E2022': ['SEQ_E2022_c01', 'SEQ_E2022_c02', 'SEQ_E2022_c03', 'SEQ_E2022_c03B', 'SEQ_E2022_c04', 'SEQ_E2022_c05', 'SEQ_E2022_c06', 'SEQ_E2022_c07', 'SEQ_E2022_c07B', 'SEQ_E2022_c08', 'SEQ_E2022_c09', 'SEQ_E2022_c10'],
    'LV_E2025': ['SEQ_E2025_c01', 'SEQ_E2025_c02', 'SEQ_E2025_c03', 'SEQ_E2025_c04', 'SEQ_E2025_c05', 'SEQ_E2025_c06', 'SEQ_E2025_c07', 'SEQ_E2025_c08', 'SEQ_E2025_c09', 'SEQ_E2025_c10', 'SEQ_E2025_c11'],
    'LV_E2029': ['SEQ_E2029_c01', 'SEQ_E2029_c02', 'SEQ_E2029_c02B', 'SEQ_E2029_c04', 'SEQ_E2029_c04B', 'SEQ_E2029_c05', 'SEQ_E2029_c06', 'SEQ_E2029_c07', 'SEQ_E2029_c08', 'SEQ_E2029_c08B', 'SEQ_E2029_c09', 'SEQ_E2029_c11', 'SEQ_E2029_c12', 'SEQ_E2029_c13'],
    'LV_E2030': ['SEQ_E2030_C00', 'SEQ_E2030_C01', 'SEQ_E2030_C02', 'SEQ_E2030_C03', 'SEQ_E2030_C03B', 'SEQ_E2030_C04', 'SEQ_E2030_C05', 'SEQ_E2030_C06', 'SEQ_E2030_C06B', 'SEQ_E2030_C07', 'SEQ_E2030_C08', 'SEQ_E2030_C09', 'SEQ_E2030_C10', 'SEQ_E2030_C11', 'SEQ_E2030_C20', 'SEQ_E2030_C21', 'SEQ_E2030_C22'],
    'LV_E2035': ['SEQ_E2035_c01', 'SEQ_E2035_c01B', 'SEQ_E2035_c01C', 'SEQ_E2035_c02', 'SEQ_E2035_c03', 'SEQ_E2035_c04', 'SEQ_E2035_c05'],
    'LV_E2040': ['SEQ_E2040_c01', 'SEQ_E2040_c02', 'SEQ_E2040_c03', 'SEQ_E2040_c04', 'SEQ_E2040_c06', 'SEQ_E2040_c07', 'SEQ_E2040_c08', 'SEQ_E2040_c09B', 'SEQ_E2040_c10', 'SEQ_E2040_c11', 'SEQ_E2040_c12', 'SEQ_E2040_c13', 'SEQ_E2040_c14', 'SEQ_E2040_c14A', 'SEQ_E2040_c14B', 'SEQ_E2040_c15', 'SEQ_E2040_c16', 'SEQ_E2040_c16B', 'SEQ_E2040_c17', 'SEQ_E2040_c18', 'SEQ_E2040_c19', 'SEQ_E2040_c31', 'SEQ_E2040_c32'],
    'LV_E2043': ['SEQ_E2043_c01a', 'SEQ_E2043_c01b', 'SEQ_E2043_c01c', 'SEQ_E2043_c02', 'SEQ_E2043_c03a', 'SEQ_E2043_c05', 'SEQ_E2043_c06', 'SEQ_E2043_c07', 'SEQ_E2043_c08', 'SEQ_E2043_c09', 'SEQ_E2043_c10', 'SEQ_E2043_c11', 'SEQ_E2043_c12a'],
    'LV_E2051': ['SEQ_E2051_c01', 'SEQ_E2051_c02', 'SEQ_E2051_c03', 'SEQ_E2051_c04', 'SEQ_E2051_c05'],
    'LV_E2160': ['SEQ_E2160_c01', 'SEQ_E2160_c02', 'SEQ_E2160_c03', 'SEQ_E2160_c04', 'SEQ_E2160_c05', 'SEQ_E2160_c06', 'SEQ_E2160_c07', 'SEQ_E2160_c10', 'SEQ_E2160_c12', 'SEQ_E2160_c13', 'SEQ_E2160_c14', 'SEQ_E2160_c15', 'SEQ_E2160_c18', 'SEQ_E2160_c19', 'SEQ_E2160_c20', 'SEQ_E2160_c21', 'SEQ_E2160_c22', 'SEQ_E2160_c23', 'SEQ_E2160_c24', 'SEQ_E2160_c25', 'SEQ_E2160_c26', 'SEQ_E2160_c27', 'SEQ_E2160_c28', 'SEQ_E2160_c29', 'SEQ_E2160_c30', 'SEQ_E2160_c31', 'SEQ_E2160_c32', 'SEQ_E2160_c33', 'SEQ_E2160_c33B', 'SEQ_E2160_c34'],
    'LV_E2164': ['SEQ_E2164_c01', 'SEQ_E2164_c02', 'SEQ_E2164_c03', 'SEQ_E2164_c04', 'SEQ_E2164_c05', 'SEQ_E2164_c06', 'SEQ_E2164_c07'],
    'LV_E2210': ['SEQ_E2210_c11', 'SEQ_E2210_c12', 'SEQ_E2210_c13', 'SEQ_E2210_c14', 'SEQ_E2210_c15', 'SEQ_E2210_c16', 'SEQ_E2210_c17', 'SEQ_E2210_c28', 'SEQ_E2210_c29', 'SEQ_E2210_c30', 'SEQ_E2210_c31'],
    'LV_E2250': ['SEQ_E2250_c01', 'SEQ_E2250_c01B', 'SEQ_E2250_c01C', 'SEQ_E2250_c02', 'SEQ_E2250_c04', 'SEQ_E2250_c05', 'SEQ_E2250_c06', 'SEQ_E2250_c07', 'SEQ_E2250_c07B', 'SEQ_E2250_c08', 'SEQ_E2250_c10', 'SEQ_E2250_c11', 'SEQ_E2250_c11B', 'SEQ_E2250_c12B', 'SEQ_E2250_c12C', 'SEQ_E2250_c12D', 'SEQ_E2250_c12E', 'SEQ_E2250_c13', 'SEQ_E2250_c13B', 'SEQ_E2250_c14', 'SEQ_E2250_c15', 'SEQ_E2250_c15B', 'SEQ_E2250_c16', 'SEQ_E2250_c16B', 'SEQ_E2250_c17', 'SEQ_E2250_c18', 'SEQ_E2250_c19', 'SEQ_E2250_c20', 'SEQ_E2250_c21', 'SEQ_E2250_c21B', 'SEQ_E2250_c22', 'SEQ_E2250_c22B', 'SEQ_E2250_c23', 'SEQ_E2250_c23B', 'SEQ_E2250_c23C', 'SEQ_E2250_c24'],
    'LV_E2255': ['SEQ_E2255_c01', 'SEQ_E2255_c02', 'SEQ_E2255_c03', 'SEQ_E2255_c04', 'SEQ_E2255_c04B', 'SEQ_E2255_c05', 'SEQ_E2255_c06', 'SEQ_E2255_c07', 'SEQ_E2255_c08', 'SEQ_E2255_c09', 'SEQ_E2255_c10', 'SEQ_E2255_c11', 'SEQ_E2255_c12', 'SEQ_E2255_c13', 'SEQ_E2255_c14', 'SEQ_E2255_c15', 'SEQ_E2255_c16', 'SEQ_E2255_c16B', 'SEQ_E2255_c16C', 'SEQ_E2255_c17', 'SEQ_E2255_c18', 'SEQ_E2255_c19', 'SEQ_E2255_c20', 'SEQ_E2255_c30', 'SEQ_E2255_c31', 'SEQ_E2255_c32'],
    'LV_E2260': ['SEQ_E2260_c01C', 'SEQ_E2260_c03', 'SEQ_E2260_c03B', 'SEQ_E2260_c04', 'SEQ_E2260_c04B', 'SEQ_E2260_c07', 'SEQ_E2260_c07B', 'SEQ_E2260_c08', 'SEQ_E2260_c09', 'SEQ_E2260_c10', 'SEQ_E2260_c12', 'SEQ_E2260_c13', 'SEQ_E2260_c14', 'SEQ_E2260_c15', 'SEQ_E2260_c16', 'SEQ_E2260_c17', 'SEQ_E2260_c18', 'SEQ_E2260_c20'],
    'LV_E2270': ['SEQ_E2270_c01', 'SEQ_E2270_c02', 'SEQ_E2270_c03', 'SEQ_E2270_c04', 'SEQ_E2270_c05', 'SEQ_E2270_c20', 'SEQ_E2270_c21', 'SEQ_E2270_c22'],
    'LV_E2290': ['SEQ_E2290_c01', 'SEQ_E2290_c02B', 'SEQ_E2290_c03', 'SEQ_E2290_c04', 'SEQ_E2290_c04B', 'SEQ_E2290_c05', 'SEQ_E2290_c06', 'SEQ_E2290_c06B', 'SEQ_E2290_c06C', 'SEQ_E2290_c07', 'SEQ_E2290_c07B', 'SEQ_E2290_c07C', 'SEQ_E2290_c08'],
    'LV_E2297': ['SEQ_E2297_C20', 'SEQ_E2297_c01', 'SEQ_E2297_c02', 'SEQ_E2297_c03', 'SEQ_E2297_c04', 'SEQ_E2297_c05', 'SEQ_E2297_c06', 'SEQ_E2297_c07', 'SEQ_E2297_c08', 'SEQ_E2297_c08B', 'SEQ_E2297_c09', 'SEQ_E2297_c10', 'SEQ_E2297_c21', 'SEQ_E2297_c22'],
    'LV_E2310': ['SEQ_E2310_c01', 'SEQ_E2310_c02', 'SEQ_E2310_c03', 'SEQ_E2310_c04', 'SEQ_E2310_c05', 'SEQ_E2310_c20', 'SEQ_E2310_c20A', 'SEQ_E2310_c20B'],
    'LV_E2320': ['SEQ_E2320_c01', 'SEQ_E2320_c01B', 'SEQ_E2320_c02', 'SEQ_E2320_c03', 'SEQ_E2320_c04', 'SEQ_E2320_c04B', 'SEQ_E2320_c04C', 'SEQ_E2320_c04D', 'SEQ_E2320_c05', 'SEQ_E2320_c06', 'SEQ_E2320_c06B', 'SEQ_E2320_c06C', 'SEQ_E2320_c08', 'SEQ_E2320_c08B', 'SEQ_E2320_c09', 'SEQ_E2320_c10', 'SEQ_E2320_c11', 'SEQ_E2320_c12B', 'SEQ_E2320_c13'],
    'LV_E2325': ['SEQ_E2325_c01', 'SEQ_E2325_c01B', 'SEQ_E2325_c02', 'SEQ_E2325_c02B', 'SEQ_E2325_c03', 'SEQ_E2325_c03B', 'SEQ_E2325_c03C', 'SEQ_E2325_c04', 'SEQ_E2325_c05', 'SEQ_E2325_c05B', 'SEQ_E2325_c05C', 'SEQ_E2325_c05D', 'SEQ_E2325_c06', 'SEQ_E2325_c07', 'SEQ_E2325_c08', 'SEQ_E2325_c09', 'SEQ_E2325_c11', 'SEQ_E2325_c11B', 'SEQ_E2325_c11C', 'SEQ_E2325_c11D', 'SEQ_E2325_c12', 'SEQ_E2325_c12C', 'SEQ_E2325_c13', 'SEQ_E2325_c13B', 'SEQ_E2325_c13C', 'SEQ_E2325_c15', 'SEQ_E2325_c15B', 'SEQ_E2325_c16', 'SEQ_E2325_c17', 'SEQ_E2325_c18', 'SEQ_E2325_c19', 'SEQ_E2325_c20', 'SEQ_E2325_c21', 'SEQ_E2325_c21B', 'SEQ_E2325_c22', 'SEQ_E2325_c30', 'SEQ_E2325_c31', 'SEQ_E2325_c32', 'SEQ_E2325_c33', 'SEQ_E2325_c33B', 'SEQ_E2325_c33C', 'SEQ_E2325_c34', 'SEQ_E2325_c34B', 'SEQ_E2325_c34C', 'SEQ_E2325_c34D', 'SEQ_E2325_c35', 'SEQ_E2325_c35B'],
    'LV_E2330': ['SEQ_E2330_c01', 'SEQ_E2330_c02', 'SEQ_E2330_c03', 'SEQ_E2330_c04', 'SEQ_E2330_c06', 'SEQ_E2330_c07', 'SEQ_E2330_c08', 'SEQ_E2330_c09', 'SEQ_E2330_c10'],
    'LV_E2440': ['SEQ_E2440_c01', 'SEQ_E2440_c02', 'SEQ_E2440_c03', 'SEQ_E2440_c04', 'SEQ_E2440_c05'],
    'LV_E2519': ['SEQ_E2519_c01', 'SEQ_E2519_c02', 'SEQ_E2519_c02B', 'SEQ_E2519_c03', 'SEQ_E2519_c04'],
    'LV_E2560': ['SEQ_E2560_c01', 'SEQ_E2560_c02', 'SEQ_E2560_c02B', 'SEQ_E2560_c03', 'SEQ_E2560_c04'],
    'LV_E2605': ['SEQ_E2605_c01', 'SEQ_E2605_c02', 'SEQ_E2605_c03', 'SEQ_E2605_c04', 'SEQ_E2605_c05', 'SEQ_E2605_c05B', 'SEQ_E2605_c06', 'SEQ_E2605_c06B', 'SEQ_E2605_c07', 'SEQ_E2605_c07B', 'SEQ_E2605_c08', 'SEQ_E2605_c08A', 'SEQ_E2605_c08B', 'SEQ_E2605_c09'],
    'LV_E2623': ['SEQ_E2623_c01', 'SEQ_E2623_c02', 'SEQ_E2623_c03', 'SEQ_E2623_c04', 'SEQ_E2623_c05', 'SEQ_E2623_c07', 'SEQ_E2623_c08', 'SEQ_E2623_c09', 'SEQ_E2623_c09B', 'SEQ_E2623_c10', 'SEQ_E2623_c11', 'SEQ_E2623_c13'],
    'LV_E2640': ['SEQ_E2640_c01', 'SEQ_E2640_c02', 'SEQ_E2640_c03', 'SEQ_E2640_c03A', 'SEQ_E2640_c03B', 'SEQ_E2640_c04', 'SEQ_E2640_c05', 'SEQ_E2640_c06'],
    'LV_E2643': ['SEQ_E2643_c01A', 'SEQ_E2643_c01B', 'SEQ_E2643_c01C', 'SEQ_E2643_c02A', 'SEQ_E2643_c02B', 'SEQ_E2643_c03', 'SEQ_E2643_c03A', 'SEQ_E2643_c03B', 'SEQ_E2643_c03C', 'SEQ_E2643_c04A', 'SEQ_E2643_c04B'],
    'LV_E2645': ['SEQ_E2645_c01', 'SEQ_E2645_c01A', 'SEQ_E2645_c01B', 'SEQ_E2645_c01C', 'SEQ_E2645_c01D', 'SEQ_E2645_c02', 'SEQ_E2645_c03', 'SEQ_E2645_c03A', 'SEQ_E2645_c03B', 'SEQ_E2645_c03C', 'SEQ_E2645_c03D', 'SEQ_E2645_c04', 'SEQ_E2645_c05', 'SEQ_E2645_c06', 'SEQ_E2645_c06B', 'SEQ_E2645_c06C', 'SEQ_E2645_c06D', 'SEQ_E2645_c07', 'SEQ_E2645_c08', 'SEQ_E2645_c09', 'SEQ_E2645_c10', 'SEQ_E2645_c11', 'SEQ_E2645_c12', 'SEQ_E2645_c13', 'SEQ_E2645_c14', 'SEQ_E2645_c14B', 'SEQ_E2645_c14C'],
    'LV_E2648': ['SEQ_E2648_c01', 'SEQ_E2648_c01A', 'SEQ_E2648_c01B', 'SEQ_E2648_c02', 'SEQ_E2648_c03', 'SEQ_E2648_c04', 'SEQ_E2648_c05', 'SEQ_E2648_c06', 'SEQ_E2648_c07', 'SEQ_E2648_c08', 'SEQ_E2648_c08B', 'SEQ_E2648_c09', 'SEQ_E2648_c10', 'SEQ_E2648_c11', 'SEQ_E2648_c12', 'SEQ_E2648_c13', 'SEQ_E2648_c14'],
    'LV_E2680': ['SEQ_E2680_c01', 'SEQ_E2680_c02', 'SEQ_E2680_c03', 'SEQ_E2680_c04', 'SEQ_E2680_c06', 'SEQ_E2680_c06B', 'SEQ_E2680_c07', 'SEQ_E2680_c08', 'SEQ_E2680_c09', 'SEQ_E2680_c10', 'SEQ_E2680_c10B', 'SEQ_E2680_c11', 'SEQ_E2680_c12', 'SEQ_E2680_c13', 'SEQ_E2680_c14', 'SEQ_E2680_c15', 'SEQ_E2680_c16', 'SEQ_E2680_c17', 'SEQ_E2680_c18', 'SEQ_E2680_c19', 'SEQ_E2680_c20', 'SEQ_E2680_c21', 'SEQ_E2680_c23', 'SEQ_E2680_c24', 'SEQ_E2680_c25', 'SEQ_E2680_c26', 'SEQ_E2680_c27', 'SEQ_E2680_c28', 'SEQ_E2680_c29', 'SEQ_E2680_c30', 'SEQ_E2680_c30B'],
    'LV_E2685': ['SEQ_E2685_c01', 'SEQ_E2685_c02', 'SEQ_E2685_c04', 'SEQ_E2685_c05', 'SEQ_E2685_c05B', 'SEQ_E2685_c06', 'SEQ_E2685_c07', 'SEQ_E2685_c08', 'SEQ_E2685_c09', 'SEQ_E2685_c10', 'SEQ_E2685_c11', 'SEQ_E2685_c12', 'SEQ_E2685_c13', 'SEQ_E2685_c14', 'SEQ_E2685_c15', 'SEQ_E2685_c16', 'SEQ_E2685_c17', 'SEQ_E2685_c18', 'SEQ_E2685_c18B', 'SEQ_E2685_c19', 'SEQ_E2685_c20', 'SEQ_E2685_c21', 'SEQ_E2685_c22', 'SEQ_E2685_c23', 'SEQ_E2685_c23A', 'SEQ_E2685_c24', 'SEQ_E2685_c25', 'SEQ_E2685_c25A', 'SEQ_E2685_c25B', 'SEQ_E2685_c26', 'SEQ_E2685_c27'],
    'LV_E2700': ['SEQ_E2700_c01', 'SEQ_E2700_c02', 'SEQ_E2700_c03', 'SEQ_E2700_c04', 'SEQ_E2700_c04B', 'SEQ_E2700_c05', 'SEQ_E2700_c06', 'SEQ_E2700_c07', 'SEQ_E2700_c07B', 'SEQ_E2700_c08', 'SEQ_E2700_c10', 'SEQ_E2700_c11', 'SEQ_E2700_c12', 'SEQ_E2700_c13', 'SEQ_E2700_c14', 'SEQ_E2700_c15', 'SEQ_E2700_c16', 'SEQ_E2700_c17'],
    'LV_E2703': ['SEQ_E2703_c01', 'SEQ_E2703_c02', 'SEQ_E2703_c03', 'SEQ_E2703_c04', 'SEQ_E2703_c05', 'SEQ_E2703_c06'],
    'LV_E2705': ['SEQ_E2705_c01', 'SEQ_E2705_c02', 'SEQ_E2705_c03', 'SEQ_E2705_c04', 'SEQ_E2705_c04B', 'SEQ_E2705_c04C', 'SEQ_E2705_c04D', 'SEQ_E2705_c05', 'SEQ_E2705_c06', 'SEQ_E2705_c07', 'SEQ_E2705_c08', 'SEQ_E2705_c11', 'SEQ_E2705_c11A', 'SEQ_E2705_c11B'],
    'LV_E2713': ['SEQ_E2713_c01', 'SEQ_E2713_c02', 'SEQ_E2713_c03', 'SEQ_E2713_c04', 'SEQ_E2713_c05', 'SEQ_E2713_c06', 'SEQ_E2713_c07', 'SEQ_E2713_c08', 'SEQ_E2713_c09', 'SEQ_E2713_c10', 'SEQ_E2713_c10B', 'SEQ_E2713_c11', 'SEQ_E2713_c11B', 'SEQ_E2713_c12', 'SEQ_E2713_c13', 'SEQ_E2713_c14', 'SEQ_E2713_c15', 'SEQ_E2713_c16', 'SEQ_E2713_c17', 'SEQ_E2713_c18', 'SEQ_E2713_c19', 'SEQ_E2713_c20', 'SEQ_E2713_c21', 'SEQ_E2713_c22', 'SEQ_E2713_c23', 'SEQ_E2713_c24', 'SEQ_E2713_c25', 'SEQ_E2713_c26', 'SEQ_E2713_c27', 'SEQ_E2713_c28', 'SEQ_E2713_c29', 'SEQ_E2713_c30'],
    'LV_E2717': ['SEQ_E2717_c01', 'SEQ_E2717_c02', 'SEQ_E2717_c03', 'SEQ_E2717_c04', 'SEQ_E2717_c07', 'SEQ_E2717_c08', 'SEQ_E2717_c09', 'SEQ_E2717_c10', 'SEQ_E2717_c11', 'SEQ_E2717_c13', 'SEQ_E2717_c14', 'SEQ_E2717_c15', 'SEQ_E2717_c16', 'SEQ_E2717_c19', 'SEQ_E2717_c20', 'SEQ_E2717_c20B', 'SEQ_E2717_c21', 'SEQ_E2717_c22', 'SEQ_E2717_c23A', 'SEQ_E2717_c23B', 'SEQ_E2717_c23C', 'SEQ_E2717_c23D', 'SEQ_E2717_c24', 'SEQ_E2717_c25', 'SEQ_E2717_c26', 'SEQ_E2717_c27', 'SEQ_E2717_c28', 'SEQ_E2717_c29', 'SEQ_E2717_c30', 'SEQ_E2717_c31', 'SEQ_E2717_c32', 'SEQ_E2717_c33', 'SEQ_E2717_c35', 'SEQ_E2717_c36', 'SEQ_E2717_c36B', 'SEQ_E2717_c37'],
    'LV_E2720': ['SEQ_E2720_c01', 'SEQ_E2720_c02', 'SEQ_E2720_c03', 'SEQ_E2720_c04', 'SEQ_E2720_c05', 'SEQ_E2720_c05B', 'SEQ_E2720_c06', 'SEQ_E2720_c07', 'SEQ_E2720_c08', 'SEQ_E2720_c09', 'SEQ_E2720_c10', 'SEQ_E2720_c11', 'SEQ_E2720_c12', 'SEQ_E2720_c13', 'SEQ_E2720_c14', 'SEQ_E2720_c15', 'SEQ_E2720_c16', 'SEQ_E2720_c17', 'SEQ_E2720_c18', 'SEQ_E2720_c19', 'SEQ_E2720_c20', 'SEQ_E2720_c21', 'SEQ_E2720_c22', 'SEQ_E2720_c23', 'SEQ_E2720_c24', 'SEQ_E2720_c25', 'SEQ_E2720_c26', 'SEQ_E2720_c27', 'SEQ_E2720_c27B', 'SEQ_E2720_c28', 'SEQ_E2720_c29', 'SEQ_E2720_c30'],
    'LV_E2740': ['SEQ_E2740_c01', 'SEQ_E2740_c02', 'SEQ_E2740_c02B', 'SEQ_E2740_c03', 'SEQ_E2740_c03B', 'SEQ_E2740_c04', 'SEQ_E2740_c04B', 'SEQ_E2740_c05', 'SEQ_E2740_c06', 'SEQ_E2740_c07', 'SEQ_E2740_c08', 'SEQ_E2740_c09', 'SEQ_E2740_c10', 'SEQ_E2740_c11', 'SEQ_E2740_c12', 'SEQ_E2740_c13', 'SEQ_E2740_c14', 'SEQ_E2740_c14B', 'SEQ_E2740_c15', 'SEQ_E2740_c15A', 'SEQ_E2740_c15B', 'SEQ_E2740_c16', 'SEQ_E2740_c17', 'SEQ_E2740_c18', 'SEQ_E2740_c19', 'SEQ_E2740_c19B', 'SEQ_E2740_c21', 'SEQ_E2740_c22', 'SEQ_E2740_c23', 'SEQ_E2740_c24', 'SEQ_E2740_c24A', 'SEQ_E2740_c24B', 'SEQ_E2740_c25'],
    'LV_E2920': ['SEQ_E2920_c01', 'SEQ_E2920_c01B', 'SEQ_E2920_c01C', 'SEQ_E2920_c02', 'SEQ_E2920_c03', 'SEQ_E2920_c04', 'SEQ_E2920_c05', 'SEQ_E2920_c05B', 'SEQ_E2920_c06', 'SEQ_E2920_c07', 'SEQ_E2920_c07B', 'SEQ_E2920_c08', 'SEQ_E2920_c09', 'SEQ_E2920_c10', 'SEQ_E2920_c10B', 'SEQ_E2920_c11', 'SEQ_E2920_c12', 'SEQ_E2920_c13', 'SEQ_E2920_c13B', 'SEQ_E2920_c14', 'SEQ_E2920_c15', 'SEQ_E2920_c16', 'SEQ_E2920_c17', 'SEQ_E2920_c18', 'SEQ_E2920_c19', 'SEQ_E2920_c20'],
    'LV_E3040': ['SEQ_E3040_c01', 'SEQ_E3040_c02', 'SEQ_E3040_c03', 'SEQ_E3040_c04', 'SEQ_E3040_c04A', 'SEQ_E3040_c05A', 'SEQ_E3040_c05B', 'SEQ_E3040_c05C', 'SEQ_E3040_c06A', 'SEQ_E3040_c06B', 'SEQ_E3040_c06C', 'SEQ_E3040_c07', 'SEQ_E3040_c08', 'SEQ_E3040_c08A', 'SEQ_E3040_c10', 'SEQ_E3040_c11', 'SEQ_E3040_c12', 'SEQ_E3040_c13', 'SEQ_E3040_c14', 'SEQ_E3040_c15', 'SEQ_E3040_c15A', 'SEQ_E3040_c16'],
    'LV_E3100': ['SEQ_E3100_c01', 'SEQ_E3100_c01B', 'SEQ_E3100_c02', 'SEQ_E3100_c02B', 'SEQ_E3100_c03', 'SEQ_E3100_c03B', 'SEQ_E3100_c04', 'SEQ_E3100_c04B', 'SEQ_E3100_c04C', 'SEQ_E3100_c04D', 'SEQ_E3100_c05', 'SEQ_E3100_c06', 'SEQ_E3100_c06B', 'SEQ_E3100_c06C', 'SEQ_E3100_c07', 'SEQ_E3100_c08', 'SEQ_E3100_c08B', 'SEQ_E3100_c09', 'SEQ_E3100_c09A', 'SEQ_E3100_c09B'],
    'LV_E3120': ['SEQ_E3120_c01', 'SEQ_E3120_c02', 'SEQ_E3120_c02B', 'SEQ_E3120_c03', 'SEQ_E3120_c03A', 'SEQ_E3120_c04', 'SEQ_E3120_c04B', 'SEQ_E3120_c04C', 'SEQ_E3120_c04D', 'SEQ_E3120_c05', 'SEQ_E3120_c05B', 'SEQ_E3120_c06'],
    'LV_E3300': ['SEQ_E3300_c01', 'SEQ_E3300_c02', 'SEQ_E3300_c03', 'SEQ_E3300_c04', 'SEQ_E3300_c05', 'SEQ_E3300_c05A', 'SEQ_E3300_c05B', 'SEQ_E3300_c05C', 'SEQ_E3300_c06', 'SEQ_E3300_c07', 'SEQ_E3300_c08', 'SEQ_E3300_c10', 'SEQ_E3300_c10A', 'SEQ_E3300_c11', 'SEQ_E3300_c12', 'SEQ_E3300_c12B', 'SEQ_E3300_c13', 'SEQ_E3300_c13A', 'SEQ_E3300_c14'],
    'LV_E3310': ['SEQ_E3310_c01', 'SEQ_E3310_c02', 'SEQ_E3310_c03', 'SEQ_E3310_c03B', 'SEQ_E3310_c04', 'SEQ_E3310_c04A', 'SEQ_E3310_c04B', 'SEQ_E3310_c05', 'SEQ_E3310_c06', 'SEQ_E3310_c06A', 'SEQ_E3310_c07', 'SEQ_E3310_c07A', 'SEQ_E3310_c08', 'SEQ_E3310_c08A', 'SEQ_E3310_c08B'],
    'LV_E3350': ['SEQ_E3350_c01', 'SEQ_E3350_c02', 'SEQ_E3350_c03', 'SEQ_E3350_c04', 'SEQ_E3350_c05', 'SEQ_E3350_c06', 'SEQ_E3350_c07', 'SEQ_E3350_c08'],
    'LV_E3352': ['SEQ_E3352_c01', 'SEQ_E3352_c02', 'SEQ_E3352_c02B', 'SEQ_E3352_c03', 'SEQ_E3352_c05', 'SEQ_E3352_c06', 'SEQ_E3352_c07', 'SEQ_E3352_c08', 'SEQ_E3352_c10', 'SEQ_E3352_c11', 'SEQ_E3352_c12', 'SEQ_E3352_c13', 'SEQ_E3352_c14', 'SEQ_E3352_c15', 'SEQ_E3352_c16', 'SEQ_E3352_c16B', 'SEQ_E3352_c16C', 'SEQ_E3352_c17', 'SEQ_E3352_c19', 'SEQ_E3352_c20', 'SEQ_E3352_c22', 'SEQ_E3352_c23', 'SEQ_E3352_c24', 'SEQ_E3352_c25', 'SEQ_E3352_c25B', 'SEQ_E3352_c26', 'SEQ_E3352_c28', 'SEQ_E3352_c28A', 'SEQ_E3352_c28B', 'SEQ_E3352_c28C', 'SEQ_E3352_c29', 'SEQ_E3352_c30', 'SEQ_E3352_c30A', 'SEQ_E3352_c30B', 'SEQ_E3352_c31', 'SEQ_E3352_c32', 'SEQ_E3352_c33', 'SEQ_E3352_c35', 'SEQ_E3352_c37', 'SEQ_E3352_c39', 'SEQ_E3352_c40', 'SEQ_E3352_c41', 'SEQ_E3352_c42', 'SEQ_E3352_c43', 'SEQ_E3352_c44', 'SEQ_E3352_c45', 'SEQ_E3352_c45A', 'SEQ_E3352_c45B', 'SEQ_E3352_c45C', 'SEQ_E3352_c46', 'SEQ_E3352_c47', 'SEQ_E3352_c48', 'SEQ_E3352_c49', 'SEQ_E3352_c50', 'SEQ_E3352_c51', 'SEQ_E3352_c52', 'SEQ_E3352_c53', 'SEQ_E3352_c54', 'SEQ_E3352_c55', 'SEQ_E3352_c56', 'SEQ_E3352_c57', 'SEQ_E3352_c58', 'SEQ_E3352_c59', 'SEQ_E3352_c60', 'SEQ_E3352_c60A', 'SEQ_E3352_c60B', 'SEQ_E3352_c61', 'SEQ_E3352_c62'],
    'LV_E3355': ['SEQ_E3355_c02', 'SEQ_E3355_c03', 'SEQ_E3355_c03A', 'SEQ_E3355_c06', 'SEQ_E3355_c07', 'SEQ_E3355_c08', 'SEQ_E3355_c08A', 'SEQ_E3355_c10', 'SEQ_E3355_c11', 'SEQ_E3355_c13', 'SEQ_E3355_c15', 'SEQ_E3355_c15B', 'SEQ_E3355_c16', 'SEQ_E3355_c17', 'SEQ_E3355_c18', 'SEQ_E3355_c20', 'SEQ_E3355_c21', 'SEQ_E3355_c22', 'SEQ_E3355_c23', 'SEQ_E3355_c23B', 'SEQ_E3355_c24'],
    'LV_E3358': ['SEQ_E3358_c01', 'SEQ_E3358_c01A', 'SEQ_E3358_c01B', 'SEQ_E3358_c02', 'SEQ_E3358_c03', 'SEQ_E3358_c04', 'SEQ_E3358_c05'],
    'LV_E3390': ['SEQ_E3390_c01', 'SEQ_E3390_c02', 'SEQ_E3390_c03', 'SEQ_E3390_c04', 'SEQ_E3390_c05', 'SEQ_E3390_c06'],
    'LV_E3400': ['SEQ_E3400_c01', 'SEQ_E3400_c02', 'SEQ_E3400_c03', 'SEQ_E3400_c05', 'SEQ_E3400_c06', 'SEQ_E3400_c07', 'SEQ_E3400_c08', 'SEQ_E3400_c09', 'SEQ_E3400_c10', 'SEQ_E3400_c11', 'SEQ_E3400_c12', 'SEQ_E3400_c14', 'SEQ_E3400_c15', 'SEQ_E3400_c16', 'SEQ_E3400_c17', 'SEQ_E3400_c18', 'SEQ_E3400_c19', 'SEQ_E3400_c20', 'SEQ_E3400_c21', 'SEQ_E3400_c22', 'SEQ_E3400_c23', 'SEQ_E3400_c24', 'SEQ_E3400_c25', 'SEQ_E3400_c26'],
    'LV_E3410': ['SEQ_E3410_c01', 'SEQ_E3410_c02', 'SEQ_E3410_c03', 'SEQ_E3410_c04', 'SEQ_E3410_c05', 'SEQ_E3410_c06', 'SEQ_E3410_c07', 'SEQ_E3410_c08'],
    'LV_E3415': ['SEQ_E3415_c01', 'SEQ_E3415_c02', 'SEQ_E3415_c02B', 'SEQ_E3415_c03', 'SEQ_E3415_c05', 'SEQ_E3415_c06', 'SEQ_E3415_c07', 'SEQ_E3415_c08', 'SEQ_E3415_c10', 'SEQ_E3415_c11', 'SEQ_E3415_c12', 'SEQ_E3415_c13', 'SEQ_E3415_c14', 'SEQ_E3415_c15', 'SEQ_E3415_c16', 'SEQ_E3415_c16B', 'SEQ_E3415_c16C', 'SEQ_E3415_c17', 'SEQ_E3415_c19', 'SEQ_E3415_c20', 'SEQ_E3415_c22', 'SEQ_E3415_c23', 'SEQ_E3415_c24', 'SEQ_E3415_c25', 'SEQ_E3415_c25B', 'SEQ_E3415_c26', 'SEQ_E3415_c28', 'SEQ_E3415_c28A', 'SEQ_E3415_c28B', 'SEQ_E3415_c28C', 'SEQ_E3415_c29', 'SEQ_E3415_c30', 'SEQ_E3415_c30A', 'SEQ_E3415_c30B', 'SEQ_E3415_c31', 'SEQ_E3415_c32', 'SEQ_E3415_c33', 'SEQ_E3415_c35', 'SEQ_E3415_c37', 'SEQ_E3415_c39', 'SEQ_E3415_c40', 'SEQ_E3415_c41', 'SEQ_E3415_c42', 'SEQ_E3415_c43', 'SEQ_E3415_c44', 'SEQ_E3415_c45', 'SEQ_E3415_c45A', 'SEQ_E3415_c45B', 'SEQ_E3415_c45C', 'SEQ_E3415_c46', 'SEQ_E3415_c47', 'SEQ_E3415_c48', 'SEQ_E3415_c49', 'SEQ_E3415_c50', 'SEQ_E3415_c51', 'SEQ_E3415_c52', 'SEQ_E3415_c53', 'SEQ_E3415_c54', 'SEQ_E3415_c55', 'SEQ_E3415_c56', 'SEQ_E3415_c57', 'SEQ_E3415_c58', 'SEQ_E3415_c59', 'SEQ_E3415_c60', 'SEQ_E3415_c60A', 'SEQ_E3415_c60B', 'SEQ_E3415_c61', 'SEQ_E3415_c62', 'SEQ_E3415_c63'],
    'LV_E3420': ['SEQ_E3420_c01', 'SEQ_E3420_c01A', 'SEQ_E3420_c01B', 'SEQ_E3420_c02'],
    'LV_E3425': ['SEQ_E3425_c01', 'SEQ_E3425_c02', 'SEQ_E3425_c03'],
    'LV_E3480': ['SEQ_E3480_c01', 'SEQ_E3480_c02', 'SEQ_E3480_c03', 'SEQ_E3480_c04', 'SEQ_E3480_c05', 'SEQ_E3480_c06'],
}