
import util.numbers as numbers
import copy
import re
from base_classes.message import Message_File, Demon_Sync
from randomizer import RACE_ARRAY

MAX_LINE_LENGTH = 48 #Arbitray Number ( at least correct for missionInfo Text)
BRAWNY_AMBITIONS_2 = 'mm_em2490'

OUTPUT_FOLDERS = {
    'ItemName' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
    'SkillHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Battle/Skill/',
    'MissionFolder' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Mission/MissionEvent/',
    'ItemHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
    'MissionInfo' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Mission/',
    'EventMessage' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Event/EventMessage/',
    'Garden': 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Garden/'
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
        'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Mission',
        'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Event',
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

#IDs of demons that show up in Item Descriptions
ITEM_DESC_SYNC_DEMON_IDS = {
    755 : 4, #A magic staff carved from a sacred tree. It contains Dagda's power
    758 : 808, #A feather from a Thunderbird. It feels like soft metal, and emits electricity.
    761 : 809, #A large bottle that drains life from humans. Kumbhanda wants you to deliver it to Succubus.
    764 : 826, #A godly stone that could very well be used as a divine housing shrine. The Kunitsu Oyamatsumi's power is held within.
    773 : 807, #The head of Girimekhala. This will supposedly be made into a watering can.
    778 : 138, #A head of the Beast Inugami. A powerful grudge restlessly stirs within.
    779 : 146, #A horn of the Wilder Bicorn. It is supposedly used to make a form of hexing medicine.
    781 : 78, #A contract written in an unknown script. It holds the power of the Tyrant Mephisto.
    782 : 295, #Makeup that is applied around one's eyes. It holds the power of the Femme Cleopatra.
}

#Times where the demon's race is also mentioned in the description
ITEM_DESC_DEMON_RACE = {
    778 : 'Beast',
    779 : 'Wilder',
    781 : 'Tyrant',
    782 : 'Femme',
    }

SKILL_DESC_CHANGES = {
    295 : '(Unique) Significantly raises Accuracy/Evasion of <skill_tgt> by 2 ranks for 3 turns.', #Red Capote Boss Version
    255 : 'Immense <skill_elm 0> attack to <skill_tgt>. Ignores affinity resistance and Pierces through.', #Moonlight Frost Boss Version
    335 : 'More than severe Strength-based <skill_elm 0> attack to <skill_tgt>. High chance of landing Critical hits.', #Freikugel Lucifer Ver.
    370 : 'Severe Strength-based <skill_elm 0> attack to <skill_tgt>. Higher chance of landing Critical hits and hitting.', #Freikugel Demifiend Boss
    830 : '(Unique) Immense <skill_elm 0> attack to <skill_tgt>. Ignores affinity resistance and Pierces through.', #Gaea Rage Demifiend Guest
    902 : 'Summon demon for weak <skill_elm 0> attack to <skill_tgt>.', #Bufu Yuzuru
    903 : 'Summon demon that lowers Defense of <skill_tgt> by 1 rank for 3 turns.', #Rakunda Yuzuru
    904 : 'Summon demon for weak <skill_elm 0> attack to <skill_tgt>. High chance of landing Critical hits.', #Gram Slice Yuzuru
    905 : 'Summon demon that greatly increases the damage of the next Strength-based attack for <skill_tgt>.', #Charge Yuzuru
    906 : 'Summon demon for medium <skill_elm 0> attack to <skill_tgt>.', #Yuzuru Bufula
    908 : '(Unique) Summon demon for heavy <skill_elm 0> attack to <skill_tgt>. Greater effect if Critical.', #Carnage Fang Yuzuru
    909 : '(Unique) Summon demon for moderate HP recovery and cures ailments for <skill_tgt>.', #Sun's Radiance Yuzuru
    910 : "(Unique) Summon demon that draws enemy hostility, but raises user's Accuracy/Evasion by 2 ranks for 3 turns.", #Witness Me Yuzuru
    911 : 'Summon demon for weak <skill_elm 0> attack to <skill_tgt>. Chance of instakill when striking weakness.', #Hama (Apparently Yuzuru?)
    912 : 'Summon demon for heavy <skill_elm 0> attack to <skill_tgt>. Chance of instakill when striking weakness.', #Mahamaon Dazai
    913 : '(Unique) Summon demon for medium <skill_elm 0> attack to <skill_tgt>. Chance of inflicting <skill_bst 0>.', #Mirage Shot Dazai
    914 : 'Summon demon for medium <skill_elm 0> attack to <skill_tgt>.', #Zanma Dazai
    915 : 'Summon demon that guarantees escape from escapable battles.', #Trafuri Dazai
    916 : '(Unique) Summon demon that raises Defense/Accuracy/Evasion of <skill_tgt> by 1 rank for 3 turns.', #Cautious Cheer Dazai
    917 : 'Summon demon for chance of inflicting <skill_bst 0> to <skill_tgt>.', #Toxic Cloud Dazai
}

#Message files for mission events and what demon(name/id) needs to be updated in them
#Demon_Sync(demonID mentioned in text, IF applicable id of demon to use replacement for) since boss mentions just use normal enemy ids
MISSION_EVENTS_DEMON_IDS = {
    'mm_em2030': [Demon_Sync(117)],#Brawny Ambitions (Zhu Tun She)
    'mm_em1300': [Demon_Sync(864),Demon_Sync(453),Demon_Sync(463)],#Falcon's Head (Horus Punishing Foe,Shinagawa Station Lahmu II, Arioch)
    'mm_em1400': [Demon_Sync(864)],#Isis Dialogue (Either for other quest or in Minato) (Horus Punishing Foe)
    'mm_em1020': [Demon_Sync(115,432),Demon_Sync(281,802)], #The Ultimate Omelet (Hydra, Jatayu)
    'mm_em1120': [Demon_Sync(147,nameVariant="Mothmen")], #Can I Keep Them? (Mothman)
    'mm_em0041': [Demon_Sync(136, 450)],#Loup Garou dialogue (Loup Garou)
    'mm_em0044': [Demon_Sync(452)],#Saving the Students misc dialogue (Lahmu)
    'mm_em0050_b': [Demon_Sync(559), Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(561, nameVariant='Atsuta')],#Golden apple quest vengeance (Eisheth, Yuzuru)
    'mm_em0051': [Demon_Sync(810)],#Golden apple quest Idun dialogue (Loki)
    'mm_em0060': [Demon_Sync(80, 454), Demon_Sync(215, 822), Demon_Sync(214, 823), Demon_Sync(216, 824)],#Hellfire Highway (Surt, Okuninushi, Sukuna Hikona, Minakata)
    'mm_em0070': [Demon_Sync(80, 454), Demon_Sync(25, 455)],#Ishtar Quest (Surt and Ishtar)
    'mm_em0143': [Demon_Sync(111, 468), Demon_Sync(178, 845)],#Taito India Amanozako dialogue (Vasuki and Shiva)
    'mm_em0145': [Demon_Sync(8, 469)],#Taito Greek Amanozako dialogue (Zeus)
    'mm_em0147': [Demon_Sync(9, 470)],#Taito Norse Amanozako dialogue (Odin)
    'mm_em0150': [Demon_Sync(345, 889)], # A Preta Predicament (Preta)
    'mm_em0151': [Demon_Sync(43)],#A Preta Predicament (Apsaras)
    'mm_em0152': [Demon_Sync(345, 889)],#A Preta Predicament (Preta)
    'mm_em0170': [Demon_Sync(318, 888)],#Moving on up (Oni, 5 quest files)
    'mm_em0171': [Demon_Sync(318, 888)],
    'mm_em0172': [Demon_Sync(318, 888)],
    'mm_em0173': [Demon_Sync(318, 888)],
    'mm_em0174': [Demon_Sync(318, 888)],
    'mm_em1031': [Demon_Sync(233, 801)],#The Cursed Mermaids (Pazuzu)
    'mm_em1040': [Demon_Sync(20, 803)],#Anahita Quest (Anahita, 2 quest files)
    'mm_em1041': [Demon_Sync(20, 803)],
    'mm_em1050': [Demon_Sync(311, 820)],#Talisman Hunt (Shiki Ouji)
    'mm_em1140': [Demon_Sync(342, 809)],#Kumbhanda Quest (Kumbhanda)
    'mm_em1150': [Demon_Sync(89, 810)],#A Goddess Stolen (Loki, 2 quest files)
    'mm_em1151': [Demon_Sync(89, 810)],
    'mm_em1160': [Demon_Sync(19)],#The Tyrant of Tennozu Demeter lines (Demeter)
    'mm_em1161': [Demon_Sync(86, 804)],#The Tyrant of Tennozu Belphegor lines (Belphegor)
    'mm_em1180': [Demon_Sync(87, 821)],#King Frost Quest (King Frost, 2 quest files)
    'mm_em1182': [Demon_Sync(87, 821)],
    'mm_em1210': [Demon_Sync(212, 826), Demon_Sync(216, 824), Demon_Sync(80, 454)],#Oyamatsumi Quest (Oyamatsumi, Minakata, Surt)
    'mm_em1250': [Demon_Sync(215, 822), Demon_Sync(214, 823), Demon_Sync(212, 826)],#Kunitsukami Fight Quest (Okuninushi, Sukuna Hikona, Oyamatsumi)
    'mm_em1260': [Demon_Sync(19), Demon_Sync(127, 812)], #Chimera Quest (Demeter, Chimera)
    'mm_em1270': [Demon_Sync(322, 813)], #Hecaton Quest (Hecaton)
    'mm_em1280': [Demon_Sync(248, 814), Demon_Sync(467)], #The Archangel of Destruction (Camael, Creation Abdiel)
    'mm_em1290': [Demon_Sync(19), Demon_Sync(85, 816), Demon_Sync(86, 804)],#Roar of Hatred (Demeter, Moloch, Belphegor)
    'mm_em1320': [Demon_Sync(232, 827)],#Girimehkala Quest (Girimehkala)
    'mm_em1330': [Demon_Sync(211, 828), Demon_Sync(206, 860), Demon_Sync(205, 861), Demon_Sync(204, 862), Demon_Sync(203, 863), Demon_Sync(215, 822)],#Lord's Sword Quest (Arahabaki, Zouchouten, Koumokuten, Jikokuten, Bishamonten, Okuninushi)
    'mm_em1340': [Demon_Sync(206, 860)],#Zouchouten Event Battle Dialogue
    'mm_em1350': [Demon_Sync(205, 861)],#Koumokuten Event Battle Dialogue
    'mm_em1360': [Demon_Sync(204, 862)],#Jikokuten Event Battle Dialogue
    'mm_em1370': [Demon_Sync(203, 863)],#Bishamonten Event Battle Dialogue
    'mm_em1380': [Demon_Sync(7, 516), Demon_Sync(82, 463)],#Khonsu CoC Quest (Khonsu, Arioch)
    'mm_em1390': [Demon_Sync(181, 829), Demon_Sync(88, 830), Demon_Sync(76, 831), Demon_Sync(7, 516), Demon_Sync(463)],#The Winged-Sun Crest (Asura, Mithras, Amon, Khonsu, Arioch)
    'mm_em1401': [Demon_Sync(15, 519), Demon_Sync(7, 516), Demon_Sync(13, 864)],#Khonsu Ra CoC Quest (Khonsu Ra, Khonsu, Horus)
    'mm_em1410': [Demon_Sync(84, 832)],#Abbadon's Assault (Abaddon)
    'mm_em1420': [Demon_Sync(35)],#Fionn 2 Quest (Fionn)
    'mm_em1430': [Demon_Sync(243, 836), Demon_Sync(247, 834), Demon_Sync(245, 835), Demon_Sync(242, 841), Demon_Sync(17, 837)],#3 Seraphim Quest (Gabriel, Uriel, Raphael, Michael, Baal):
    'mm_em1440': [Demon_Sync(19), Demon_Sync(17, 837), Demon_Sync(86, 804), Demon_Sync(85, 816), Demon_Sync(81, 483), Demon_Sync(2, 537)],#Baal Quest (Demeter, Baal, Belphegor, Moloch, Beelzebub, Lucifer)
    'mm_em1450': [Demon_Sync(8, 838), Demon_Sync(19)],#A Plot Unveiled (Zeus, Demeter)
    'mm_em1460': [Demon_Sync(94, 839)],#The Gold Dragon's Arrival (Huang Long)
    'mm_em1470': [Demon_Sync(94, 839)],#Huang Long Fight (Huang Long)
    'mm_em1480': [Demon_Sync(83, 840), Demon_Sync(242), Demon_Sync(82, 463)],#Side with Michael (Belial, Michael, Arioch)
    'mm_em1490': [Demon_Sync(242, 841), Demon_Sync(83), Demon_Sync(82, 463)],#Side with Belial (Michael, Belial, Arioch)
    'mm_em1500': [Demon_Sync(30, 842), Demon_Sync(188, 843), Demon_Sync(189, 844)],#Seed of Life Quest (Maria, Danu, Innana)
    'mm_em1530': [Demon_Sync(178, 845), Demon_Sync(111, 468)],#A Universe in Peril (Shiva, Vasuki)
    'mm_em1570': [Demon_Sync(845)],#Sarasvati Collection Quest (Shiva)
    'mm_em1590': [Demon_Sync(876), Demon_Sync(453)],#Berserk Amanozako Quest (Amanozako, 3 Quest Files, Final Lahmu)
    'mm_em1591': [Demon_Sync(38, 876)],
    'mm_em1592': [Demon_Sync(38, 876)],
    'mm_em1600': [Demon_Sync(38), Demon_Sync(454)], #Final Amanozako Quest (Amanozako, 4 Quest Files, Surt)
    'mm_em1601': [Demon_Sync(38)],
    'mm_em1602': [Demon_Sync(38), Demon_Sync(877)], #Zaou-Gongen Mentioned here and in 1603
    'mm_em1603': [Demon_Sync(38), Demon_Sync(877)],
    'mm_em1630': [Demon_Sync(43, 868), Demon_Sync(305), Demon_Sync(316, 867)], #Side with Leanan (Apsaras, Leanan, Ippon Datara)
    'mm_em1640': [Demon_Sync(306, 866), Demon_Sync(43)], #Side with Apsaras (Leanan, Apsaras)
    'mm_em1641': [Demon_Sync(43), Demon_Sync(345, 889)], #Apsaras' Followers Dialogue (Apsaras, 2 Quest Files, Preta)
    'mm_em1642': [Demon_Sync(43)],
    'mm_em1650': [Demon_Sync(257, 879), Demon_Sync(67)], #Side with Lilim (Principality, Lilim)
    'mm_em1660': [Demon_Sync(67, 880), Demon_Sync(257)], #Side with Principality (Lilim, Principality)
    'mm_em1670': [Demon_Sync(183, 881), Demon_Sync(72)], #Side with Black Frost (Dionysus, Black Frost)
    'mm_em1680': [Demon_Sync(72, 882), Demon_Sync(183)], #Side with Dionysus (Black Frost, Dionysus)
    'mm_em1690': [Demon_Sync(201, 883), Demon_Sync(265)], #Side with Adramelech (Futsunushi, Adramelech)
    'mm_em1700': [Demon_Sync(265, 884), Demon_Sync(201)], #Side with Futsunushi (Adramelech, Futsunushi)
    'mm_em1769': [Demon_Sync(78), Demon_Sync(295), Demon_Sync(31), Demon_Sync(4), Demon_Sync(528), Demon_Sync(561)], #Tokyo Diet Building Researcher (Mephisto, Cleopatra, Artemis, Dagda, Tsukuyomi, Yuzuru) TODO: Differentiate between boss and summonable versions.
    'mm_em1770': [Demon_Sync(78)], #Mephisto Quest (Mephisto)
    'mm_em1780': [Demon_Sync(295)], #Cleopatra Quest (Cleopatra)
    'mm_em1790': [Demon_Sync(31), Demon_Sync(933), Demon_Sync(432), Demon_Sync(8, 838)], #Artemis Quest (Artemis, Queztalcoatl, Hydra, Zeus 2 for fun) Note: If Artemis's speaker voice is changed the game crashes
    'mm_em1802': [Demon_Sync(359, 921)], #Matador, 2 Quest Files
    'mm_em1803': [Demon_Sync(921)],
    'mm_em1804': [Demon_Sync(357, 922)], #Daisoujou
    'mm_em1805': [Demon_Sync(922)],
    'mm_em1806': [Demon_Sync(356, 923)], #Hell Biker
    'mm_em1807': [Demon_Sync(923)],
    'mm_em1810': [Demon_Sync(354, 924)], #White Rider
    'mm_em1811': [Demon_Sync(924)],
    'mm_em1812': [Demon_Sync(353, 925)], #Red Rider
    'mm_em1813': [Demon_Sync(925)],
    'mm_em1814': [Demon_Sync(352, 926)], #Black Rider
    'mm_em1815': [Demon_Sync(926)],
    'mm_em1816': [Demon_Sync(358, 927)], #Pale Rider
    'mm_em1817': [Demon_Sync(927)],
    'mm_em1819': [Demon_Sync(351, 928)], #Mother Harlot
    'mm_em1820': [Demon_Sync(928)],
    'mm_em1821': [Demon_Sync(350, 929)], #Trumpeter, 2 Quest Files
    'mm_em1822': [Demon_Sync(929), Demon_Sync(934)], #Demi-Fiend named here as well
    'mm_em1823': [Demon_Sync(934)], #Demi-Fiend, 3 Quest Files
    'mm_em1824': [Demon_Sync(934)],
    'mm_em1825': [Demon_Sync(934)],
    'mm_em2020': [Demon_Sync(107, 752, nameVariant='NOZUCHI'), Demon_Sync(336, nameVariant='KODAMA')], #Nozuchi Queset (Nozuchi, Normal Enemy Kodama)
    'mm_em2040': [Demon_Sync(20, 803)], #Pisaca Quest part 1 (Anahita)
    'mm_em2090': [Demon_Sync(561), Demon_Sync(562)], #Yuzuru Supply Run Quest (Yuzuru, Hayataro)
    'mm_em2111': [Demon_Sync(108, 769)], #Vouivre Quest (Vouivre)
    'mm_em2130': [Demon_Sync(113), Demon_Sync(41), Demon_Sync(386)], #Basilisk Hunt Quest (Basilisk, Anansi, Onyankopon)
    'mm_em2170': [Demon_Sync(227)], #Masakado Quest (Masakado)
    'mm_em2190': [Demon_Sync(552), Demon_Sync(318, 888)], #Halphas Quest (Glasya-Labolas 1, Oni)
    'mm_em2240': [Demon_Sync(15, 519), Demon_Sync(7, 566), Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(864), Demon_Sync(577), Demon_Sync(578)], #Vengeance Khonsu-Ra Quest (Khonsu Ra, Khonsu, Yuzuru, Horus, Fallen Abdiel, Dazai)
    'mm_em2270': [Demon_Sync(346, 772), Demon_Sync(40)], #Side with Kresnik (Kudlak, Kresnik)
    'mm_em2280': [Demon_Sync(40, 774), Demon_Sync(346)], #Side with Kudlak (Kresnik, Kudlak)
    'mm_em2290': [Demon_Sync(890)], #Gogmagog Quest (Gogmagog)
    'mm_em2310': [Demon_Sync(386, 770), Demon_Sync(41)], #Side with Onyankopon (Onyankopon, Anansi) - Swapped boss/recruit versions due to the way these 2 join compared to others
    'mm_em2320': [Demon_Sync(41, 771), Demon_Sync(386)], #Side with Anansi (Anansi, Onyankopon)
    'mm_em2350': [Demon_Sync(200, 778)], #Idun Haunt Quest (Thor)
    'mm_em2370': [Demon_Sync(278, 865), Demon_Sync(564), Demon_Sync(468), Demon_Sync(481)], #Siegfried Quest (Garuda, Vengeance Abdiel, Vasuki, Vengeance Zeus) Odin is mentioned but the same text box is used in both routes
    'mm_em2390': [Demon_Sync(776), Demon_Sync(227)], #Cironnup Quest (Atavaka, Masakado)
    'mm_em2400': [Demon_Sync(118, 760), Demon_Sync(537)], #Samael Quest (Samael, Lucifer)
    'mm_em2420': [Demon_Sync(1, 681), Demon_Sync(760), Demon_Sync(537), Demon_Sync(250, 596)], #Satan Quest (Satan, Samael, Lucifer, Mastema)
    'mm_em2460': [Demon_Sync(77, 892)], #Mara Quest (Mara)
    'mm_em2470': [Demon_Sync(175, 754, nameVariant='TURBO GRANNY')], #Turbo Granny Quest (Turbo Granny)
    'mm_em2490': [Demon_Sync(122)], #Hare of Inaba 2 Quest (Xiezhai) TODO: Replace Puncture Punch with updated skill
    'mm_em2500': [Demon_Sync(215), Demon_Sync(122), Demon_Sync(214)], #Hare of Inaba 3 Quest (Okuninushi, Xiezhai, Sukona Hikona for fun)
    'mm_em2530': [Demon_Sync(141, 751, nameVariant='DORMARTH')], #Dormarth Quest (Dormarth)
    'mm_em2540': [Demon_Sync(291, 891)], #Gurulu Quest (Gurulu)
    'mm_em2550': [Demon_Sync(756, nameVariant='ZHEn')], #Part Time Quest (Zhen) Optionally add the other 2 encounters you can get here but eh
    'mm_em2570': [Demon_Sync(22, 779), Demon_Sync(838)], #Moirae Haunt Quest (Norn, Zeus 2 for fun)
    'mm_em2580': [Demon_Sync(12, 776, nameVariant='Daigensui Myouou')], #Yoshitsune Haunt Quest (Atavaka)
    'mm_em2600': [Demon_Sync(32), Demon_Sync(826)], #Konohana Sakuya Quest (Konohana Sakuya, Oyamatsumi)
    'mm_em2610': [Demon_Sync(4), Demon_Sync(188, 843)], #Dagda Quest (Dagda, Danu for fun)
    'mm_em2620': [Demon_Sync(775, nameVariant='Orochi'), Demon_Sync(510, 528)], #Orochi Quest (Orochi, Tsukuyomi)
    'mm_em2630': [Demon_Sync(237, 782), Demon_Sync(481), Demon_Sync(837)], #Saturnus Quest (Saturnus, CoV Zeus, Baal)
    'mm_em2640': [Demon_Sync(569), Demon_Sync(564)], #Package Delivery Quest (Lilith, Vengeance Abdiel)
    'mm_em2700': [Demon_Sync(207)], #Marici Quest (Marici)
}

#Message files for story events and what demon(name/id) needs to be updated in them
#Demon_Sync(demonID mentioned in text, IF applicable id of demon to use replacement for) since boss mentions just use normal enemy ids
EVENT_MESSAGE_DEMON_IDS = {
    'e0180': [Demon_Sync(345, 431)],#Triple Preta Pre-fight dialogue (Preta)
    'e0262': [Demon_Sync(537)],#Pre-Hydra dialogue (Lucifer)
    'e0300': [Demon_Sync(432, nameVariant='hydra')],#Return Pillar cutscene (Hydra)
    'e0310': [Demon_Sync(115, 432)],#Unused? Hydra dialogue (Hydra)
    'e0330': [Demon_Sync(75, 435)],#Snake Nuwa Pre-fight dialogue (Nuwa)
    'e0340': [Demon_Sync(512, 465, nameVariant='Yakumo'), Demon_Sync(75, 435)],#Snake Nuwa Post-fight dialogue creation (Yakumo, Nuwa)
    'e0350': [Demon_Sync(240, 467)],#Meeting Abdiel creation (Abdiel)
    'e0375': [Demon_Sync(152)],#Hayataro in area 2 (Hayataro)
    'e0377': [Demon_Sync(452)],#Aogami asks what to do with Sahori (Lahmu)
    'e0378': [Demon_Sync(837), Demon_Sync(511, 467)],#Dazai/Abdiel talk in area 2 creation (Baal, Abdiel)
    'e0379': [Demon_Sync(35, 451)],#Fionn 1 Pre-fight dialogue (Fionn)
    'e0380': [Demon_Sync(35, 451), Demon_Sync(452)],#Fionn 1 Post-fight dialogue (Fionn, Lahmu)
    'e0390': [Demon_Sync(451, nameVariant='Fionn')],#First Miyazu dialogue in fairy village (Fionn)
    'e0431': [Demon_Sync(236, 441)],#Lahmu 1 Post-fight dialogue (Lahmu) Note: Lahmu mentions will switch from Lahmu 1 to final Lahmu once you enter area 2
    'e0432': [Demon_Sync(236, 441)],#Lahmu 1 Pre-fight dialogue (Lahmu)
    'e0435': [Demon_Sync(441)],#Arriving at overrun school (Lahmu)
    'e0470': [Demon_Sync(236, 441)],#Lahmu meets Sahori (Lahmu)
    'e0473': [Demon_Sync(152)],#Meeting Hayataro creation (Hayataro)
    'e0480': [Demon_Sync(236, 441)],#Sahori kills her bullies (Lahmu)
    'e0490': [Demon_Sync(236, 452)],#Final Lahmu Pre-fight dialogue (Lahmu) TODO: Make shaking text decisions work maybe
    'e0491': [Demon_Sync(236, 453)],#Final Lahmu between phases dialogue (Lahmu) Note: Start using second phase Lahmu for mentions once phase 1 is dead
    'e0510': [Demon_Sync(453)],#Final Lahmu Post-fight dialogue (Lahmu)
    'e0525': [Demon_Sync(845), Demon_Sync(467)],#Pre-summit Koshimitzu? Dialogue (Shiva, Creation Abdiel)
    'e0530': [Demon_Sync(240, 467), Demon_Sync(463)],#Pre-summit Abdiel/Koshimitzu talk (Creation Abdiel, Arioch)
    'e0550': [Demon_Sync(453)],#Koshimitzu debrief after area 2 (Lahmu)
    'e0560': [Demon_Sync(453)],#Dazai/Yuzuru talk after area 2 (Lahmu)
    'e0570': [Demon_Sync(453)],#Learning about armies of chaos before area 3 (Lahmu)
    'e0580': [Demon_Sync(240, 467)],#Meeting Abdiel in Chiyoda (Abdiel)
    'e0590': [Demon_Sync(80, 454)],#Surt introduction (Surt)
    'e0595': [Demon_Sync(80, 454)],#Surt Pre-fight dialogue (Surt)
    'e0598': [Demon_Sync(25, 455)],#Ishtar Pre-fight dialogue (Ishtar)
    'e0600': [Demon_Sync(8, 469), Demon_Sync(9, 470), Demon_Sync(111, 468), Demon_Sync(7, 516), Demon_Sync(845), Demon_Sync(240, 467), Demon_Sync(454), Demon_Sync(455), Demon_Sync(463), Demon_Sync(537)],#First Bethel summit cutscene (Zeus, Odin, Vasuki, Khonsu, Shiva, Abdiel, Surt, Ishtar, Arioch, Lucifer)
    'e0602': [Demon_Sync(8, 469), Demon_Sync(9, 470), Demon_Sync(111, 468), Demon_Sync(7, 516), Demon_Sync(845), Demon_Sync(467)],#Talking to faction leaders at summit (Zeus, Odin, Vasuki, Khonsu, Shiva, Abdiel)
    'e0603': [Demon_Sync(8, 469), Demon_Sync(9, 470), Demon_Sync(111, 468), Demon_Sync(7, 516), Demon_Sync(845), Demon_Sync(240, 467)],#Abdiel pre-fight dialogue at summit (Zeus, Odin, Vasuki, Khonsu, Shiva, Abdiel)
    'e0604': [Demon_Sync(8, 469), Demon_Sync(9, 470), Demon_Sync(111, 468), Demon_Sync(7, 516), Demon_Sync(845), Demon_Sync(510, 528), Demon_Sync(240, 467)],#Abdiel post-fight dialogue at summit (Zeus, Odin, Vasuki, Khonsu, Shiva, Tsukuyomi, Abdiel)
    'e0610': [Demon_Sync(467)],#Angels giving directions to DKC (Abdiel)
    'e0620': [Demon_Sync(512, 465), Demon_Sync(75, 435)],#Yakumo pre-fight dialogue (Yakumo, Nuwa)
    'e0625': [Demon_Sync(512, 465), Demon_Sync(75, 435), Demon_Sync(453)],#Yakumo post-fight dialogue (Yakumo, Nuwa, Lahmu)
    'e0627': [Demon_Sync(453)],#Aogami dialogue after Yakumo fight (Lahmu)
    'e0628': [Demon_Sync(467)],#Dazai dialogue after Surt (Abdiel)
    'e0630': [Demon_Sync(240, 467)],#Abdiel dialogue before DKC (Abdiel)
    'e0640': [Demon_Sync(182, 466), Demon_Sync(467)],#Chernobog related dialogue (Chernobog, Abdiel)
    'e0650': [Demon_Sync(240, 467)],#Abdiel/Dazai talk in DKC (Abdiel)
    'e0660': [Demon_Sync(82, 463)],#Arioch pre-fight dialogue (Arioch)
    'e0670': [Demon_Sync(82, 463)],#Arioch post-fight dialogue (Arioch)
    'e0675': [Demon_Sync(512, 465, nameVariant='Yakumo'), Demon_Sync(75, 435), Demon_Sync(463)],#Yakumo talk after Arioch (Yakumo, Nuwa, Arioch)
    'e0680': [Demon_Sync(240, 467), Demon_Sync(463)],#Abdiel celebrates Arioch's death (Abdiel, Arioch)
    'e0690': [Demon_Sync(467), Demon_Sync(528)],#Koshimitzu meeting after area 3 (Abdiel, Tsukuyomi)
    'e0730': [Demon_Sync(837), Demon_Sync(537), Demon_Sync(510, 528)],#Regarding the war of the gods dialogue (Baal, Lucifer, Tsukuyomi)
    'e0735': [Demon_Sync(467)],#Dazai dialogue after summit (Abdiel)
    'e0736': [Demon_Sync(511, 467)],#Dazai/Abdiel talk after summit (Abdiel)
    'e0762': [Demon_Sync(512, 465, nameVariant='Yakumo'), Demon_Sync(75, 520)],#Nuwa in area 4 (Yakumo, Nuwa) Note: I guess start referencing nahobino nuwa/abdiel in area 4?
    'e0765': [Demon_Sync(525)],#Dazai hat scene (Abdiel)
    'e0770': [Demon_Sync(468), Demon_Sync(845)],#Bethel India demon dialogue (Vasuki, Shiva)
    'e0770_b': [Demon_Sync(468), Demon_Sync(845), Demon_Sync(483)],#Bethel India vengeance demon dialogue (Vasuki, Shiva, Beelzebub)
    'e0775': [Demon_Sync(111, 468), Demon_Sync(845)],#Vasuki pre-fight dialogue (Vasuki, Shiva)
    'e0780': [Demon_Sync(469, nameVariant='ZEUS')],#Bethel Greek demon creation? dialogue (Zeus)
    'e0780_b': [Demon_Sync(481, nameVariant='ZEUS')],#Bethel Greek demon vengeance? dialogue (Zeus)
    'e0785': [Demon_Sync(8, 469), Demon_Sync(528)],#Zeus pre-fight dialogue (Zeus, Tsukuyomi)
    'e0800': [Demon_Sync(470)],#Bethel Norse demon creation dialogue (Odin)
    'e0800_b': [Demon_Sync(482), Demon_Sync(481)],#Bethel Norse demon vengeance dialogue (Odin, Zeus)
    'e0805': [Demon_Sync(9, 470)],#Odin pre-fight dialogue (Odin)
    'e0825': [Demon_Sync(477)],#Metatron pre-fight dialogue (Metatron)
    'e0841': [Demon_Sync(510, 528)],#Chaos rep overview pre-empyrean (Tsukuyomi)
    'e0842': [Demon_Sync(240, 525)],#Law rep overview pre-empyrean (Abdiel)
    'e0850': [Demon_Sync(510, 528), Demon_Sync(469), Demon_Sync(470), Demon_Sync(240, 525), Demon_Sync(512, 465), Demon_Sync(75, 520)],#Argument before Empyrean (Tsukuyomi, Zeus, Odin, Abdiel, Yakumo, Nuwa)
    'e0870': [Demon_Sync(528), Demon_Sync(240, 525)],#Joining Dazai in Empyrean (Tsukuyomi, Abdiel) Note: test this specifically
    'e0880': [Demon_Sync(510, 528), Demon_Sync(525), Demon_Sync(152)],#Joining Tsukuyomi in Empyrean (Tsukuyomi, Abdiel, Hayataro) Abdiel spread out text
    'e0885': [Demon_Sync(152)],#Hayataro joins you (Hayataro)
    'e0891': [Demon_Sync(471)],#Empyrean minibosses dialogue (Melchizedek)
    'e0900': [Demon_Sync(240, 525), Demon_Sync(510, 528)],#Dazai/Abdiel lose to Tsukuyomi (Abdiel, Tsukuyomi)
    'e0910': [Demon_Sync(240, 525), Demon_Sync(510, 528)],#Tsukuyomi loses to Dazai/Abdiel (Abdiel, Tsukuyomi)
    'e0920': [Demon_Sync(240, 525), Demon_Sync(512, 465, nameVariant='Yakumo'), Demon_Sync(75, 520)],#Yakumo/Nuwa loses to Dazai/Abdiel (Abdiel, Yakumo, Nuwa)
    'e0930': [Demon_Sync(465, nameVariant='Yakumo'), Demon_Sync(75, 520)],#Nuwa true ending dialogue after Abdiel (Yakumo, Nuwa)
    'e0940': [Demon_Sync(512, 465), Demon_Sync(75, 520)],#Nahobino Nuwa pre-fight dialogue (Yakumo, Nuwa)
    'e0945': [Demon_Sync(75, 520)],#Nahobino Nuwa post-fight dialogue (Nuwa)
    'e0960': [Demon_Sync(510, 528)],#Tsukuyomi neutral route pre-fight dialogue (Tsukuyomi)
    'e0965': [Demon_Sync(530, 528)],#Tsukuyomi neutral route post-fight dialogue (Tsukuyomi)
    'e1000': [Demon_Sync(529, 537)],#Lucifer pre-fight dialogue (Normal Lucifer)
    'e1020': [Demon_Sync(529)],#Aogami says goodbye in true neutral ending (True Lucifer)
    'e2010': [Demon_Sync(552), Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(578, nameVariant='Dazai')],#Labolas 1 pre-fight dialogue (Labolas, Yuzuru, Dazai) Note: For vengeance dialogue replacing mentions of Yuzuru/Dazai, but not Yoko for now
    'e2015': [Demon_Sync(505, 561)],#Labolas 1 post-fight dialogue (Yuzuru)
    'e2018': [Demon_Sync(43), Demon_Sync(305)],#Possibly unused Yoko dialogue about Apsaras/Leanan (Apsaras, Leanan)
    'e2020': [Demon_Sync(393, 553)],#Naamah pre-fight dialogue 1 (Naamah)
    'e2022': [Demon_Sync(393, 553)],#Naamah pre-fight dialogue 2 (Naamah)
    'e2025': [Demon_Sync(393, 553)],#Naamah post-fight dialogue (Naamah)
    'e2029': [Demon_Sync(512, 567, nameVariant='Yakumo'), Demon_Sync(75, 435)],#Nuwa post-fight dialogue vengeance (Yakumo, Nuwa)
    'e2030': [Demon_Sync(506, 578), Demon_Sync(505, 561, nameVariant="Yuzuru freakin' Atsuta"), Demon_Sync(561, nameVariant='Atsuta')],#Dazai in diet building vengeance (Dazai, Yuzuru)
    'e2035': [Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(561, nameVariant='Atsuta')],#Returning to Tokyo from area 1 vengeance (Yuzuru)
    'e2040': [Demon_Sync(240, 564), Demon_Sync(506, 578), Demon_Sync(505, 561)],#Meeting Abdiel vengeance (Abdiel, Dazai, Yuzuru)
    'e2043': [Demon_Sync(505, 561, nameVariant='Atsuta'), Demon_Sync(506, 578, nameVariant='Dazai')],#Tao meeting after area 1 vengeance (Yuzuru, Dazai)
    'e2046': [Demon_Sync(505, 561)],#Misc Yuzuru/Yoko text after area 1 (Yuzuru)
    'e2160': [Demon_Sync(393, 554)],#Labolas 2 pre-fight dialogue (Naamah)
    'e2164': [Demon_Sync(393, 554)],#Labolas 2 post-fight dialogue (Naamah)
    'e2165': [Demon_Sync(554), Demon_Sync(512, 567), Demon_Sync(513, 435)],#Yakumo talk after Labolas 2 (Naamah, Yakumo, Nuwa)
    'e2170': [Demon_Sync(556), Demon_Sync(432, nameVariant='hydra')],#Jojozi temple during invasion vengeance (Lahmu, Hydra)
    'e2190': [Demon_Sync(556)],#Tao joins you during invasion vengeance (Lahmu)
    'e2210': [Demon_Sync(152, 562), Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(578, nameVariant='Dazai')],#Meeting Hayataro vengeance (Hayataro, Yuzuru, Dazai)
    'e2240': [Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(506, 578, nameVariant='Ichiro'), Demon_Sync(578, nameVariant='Dazai')],#Dazai scared during invasion vengeance (Yuzuru, Dazai)
    'e2250': [Demon_Sync(236, 556)],#Vengeance Lahmu pre-fight dialogue (Lahmu)
    'e2255': [Demon_Sync(556), Demon_Sync(391, 569)],#Lilith kills Sahori (Lahmu, Lilith)
    'e2260': [Demon_Sync(505, 561, nameVariant='Atsuta'), Demon_Sync(506, 578, nameVariant='Dazai')],#Dazai/Yuzuru first argument (Yuzuru, Dazai)
    'e2270': [Demon_Sync(505, 561), Demon_Sync(506, 578), Demon_Sync(562)],#Arriving in area 2 vengeance (Yuzuru, Dazai, Hayataro)
    'e2275': [Demon_Sync(837), Demon_Sync(511, 564), Demon_Sync(506, 578, nameVariant='Dazai')],#Dazai/Abdiel talk in area 2 vengeance (Baal, Abdiel, Dazai)
    'e2288': [Demon_Sync(554), Demon_Sync(569)],#Yoko/Tao speculate on Eistheth's identity (Naamah, Lilith)
    'e2290': [Demon_Sync(394, 559)],#Eisheth pre-fight dialogue (Eisheth)
    'e2295': [Demon_Sync(394, 559)],#Eisheth post-fight dialogue (Eisheth)
    'e2298': [Demon_Sync(559), Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(517, 451)],#Fionn post-fight dialogue vengeance (Eisheth, Yuzuru, Fionn)
    'e2300': [Demon_Sync(506, 578), Demon_Sync(561, nameVariant='Atsuta')],#Dazai stops you in area 2 (Dazai, Yuzuru)
    'e2301': [Demon_Sync(578)],#Aogami talk about Dazai in area 2 (Dazai)
    'e2305': [Demon_Sync(451, nameVariant='Fionn'), Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(559)],#Arriving in fairy village vengeance (Fionn, Yuzuru, Eisheth)
    'e2310': [Demon_Sync(506, 578, nameVariant='Dazai'), Demon_Sync(561, nameVariant='Atsuta')],#Dazai loses to Eisheth (Dazai, Yuzuru)
    'e2320': [Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(394, 559), Demon_Sync(509, 562)],#Yuzuru pre-fight dialogue (Yuzuru, Eisheth, Hayataro)
    'e2325': [Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(561, nameVariant='Atsutaaa'), Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(506, 578, nameVariant='Dazai'), Demon_Sync(394, 559), Demon_Sync(554), Demon_Sync(392, 568)],#Yuzuru post-fight dialogue (Yuzuru, Dazai, Eisheth, Naamah, Agrat)
    'e2400': [Demon_Sync(562)],#Aogami talk about Agra after area 2 (Hayataro)
    'e2410': [Demon_Sync(561, nameVariant='Atsuta')],#Koshimizu meeting after area 2 vengeance (Yuzuru)
    'e2420': [Demon_Sync(505, 561)],#Yuzuru apologizes for attacking you (Yuzuru)
    'e2435': [Demon_Sync(562)],#Koshimizu meeting after salt investigation (Hayataro)
    'e2445': [Demon_Sync(509, 562), Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(578, nameVariant='Dazai')],#Koshimizu discovers shinjuku (Hayataro, Yuzuru, Dazai)
    'e2450': [Demon_Sync(506, 578), Demon_Sync(564)],#Dazai goes to Chiyoda (Dazai, Abdiel)
    'e2500': [Demon_Sync(562)],#Arriving in Shinjuku (Hayataro)
    'e2520': [Demon_Sync(513, 550), Demon_Sync(512, 567), Demon_Sync(486, nameVariant='Cherubim')],#First Nuwa/Yakumo scene in Shinjuku (Nuwa, Yakumo, Cherub)
    'e2531': [Demon_Sync(486, nameVariant='Cherubim')],#Cherubim are called after Power gauntlet (Cherub)
    'e2535': [Demon_Sync(567, nameVariant='Yakumo')],#Yoko/Tao talk where Cherub used to be (Yakumo)
    'e2560': [Demon_Sync(512, 567)],#Nuwa/Yakumo talk at Mastema's hill 1 (Yakumo)
    'e2562': [Demon_Sync(512, 567, nameVariant='Yakumo'), Demon_Sync(513, 550)],#Nuwa/Yakumo talk at Mastema's hill 2 (Yakumo, Nuwa)
    'e2575': [Demon_Sync(506, 578, nameVariant='Dazai'), Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(564)],#Dazai talk when Miyazu goes to Khonsu (Dazai, Yuzuru, Abdiel)
    'e2600': [Demon_Sync(566), Demon_Sync(578, nameVariant='Dazai'), Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(567)],#Koshimizu meeting about Khonsu (Khonsu, Dazai, Yuzuru, Yakumo)
    'e2603': [Demon_Sync(506, 578), Demon_Sync(505, 561, nameVariant='Atsuta')],#Dazai/Yuzuru in dorm room (Dazai, Yuzuru)
    'e2605': [Demon_Sync(506, 578, nameVariant='Ichiro'), Demon_Sync(578, nameVariant='Dazai'), Demon_Sync(505, 561, nameVariant='Yuzuru')],#Dazai and Yuzuru become friends (Dazai, Yuzuru)
    'e2608': [Demon_Sync(561, nameVariant='Yuzuru')],#Aogami comments on Yuzuru's distress (Yuzuru)
    'e2610': [Demon_Sync(193, 579), Demon_Sync(506, 578, nameVariant='Ichiro'), Demon_Sync(505, 561, nameVariant='Yuzuru')],#Isis pre-fight dialogue (Isis, Dazai, Yuzuru)
    'e2615': [Demon_Sync(193, 579), Demon_Sync(566), Demon_Sync(505, 561)],#Isis post-fight dialogue (Isis, Khonsu, Yuzuru)
    'e2620': [Demon_Sync(514, 566), Demon_Sync(505, 561)],#Khonsu pre-fight dialogue vengeance part 1 (Khonsu, Yuzuru)
    'e2623': [Demon_Sync(514, 566), Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(506, 578)],#Khonsu pre-fight dialogue vengeance part 2 (Khonsu, Yuzuru, Dazai)
    'e2625': [Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(514, 566), Demon_Sync(564), Demon_Sync(596)],#Khonsu post-fight dialogue vengeance (Yuzuru, Khonsu, Abdiel, Mastema)
    'e2630': [Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(506, 578)],#Yuzuru talk after Khonsu incident (Yuzuru, Dazai)
    'e2631': [Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(566)],#Aogami discusses Khonsu incident (Yuzuru, Khonsu)
    'e2633': [Demon_Sync(566)],#Yoko discusses Khonsu incident (Khonsu)
    'e2635': [Demon_Sync(506, 578)],#Dazai joins to see Mastema 1 (Dazai)
    'e2638': [Demon_Sync(506, 578, nameVariant='Dazai'), Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(596)],#Dazai joins to see Mastema 2 (Dazai, Yuzuru, Mastema)
    'e2640': [Demon_Sync(566), Demon_Sync(596)],#Arriving at Mastema's hill (Khonsu, Mastema)
    'e2642': [Demon_Sync(566), Demon_Sync(250, 596)],#Meeting Mastema (Khonsu, Mastema)
    'e2643': [Demon_Sync(506, 578, nameVariant='Dazai')],#Dazai turns to salt (Dazai)
    'e2644': [Demon_Sync(250, 596)],#Mastema sends you to Shinjuku (Mastema)
    'e2645': [Demon_Sync(250, 596), Demon_Sync(506, 578, nameVariant='Dazai'), Demon_Sync(578, nameVariant='Ichiro')],#Mastema brainwashes Dazai (Mastema, Dazai)
    'e2648': [Demon_Sync(393, 554)],#Naamah in Shinjuku (Naamah)
    'e2650': [Demon_Sync(512, 567), Demon_Sync(513, 550), Demon_Sync(596)],#Nuwa/Yakumo talk after seeing Naamah (Yakumo, Nuwa, Mastema)
    'e2660': [Demon_Sync(596), Demon_Sync(505, 561)],#Koshimizu meeting before Yakumo fight (Mastema, Yuzuru)
    'e2670': [Demon_Sync(528), Demon_Sync(505, 561)],#Yuzuru wants to be a Nahobino (Tsukuyomi, Yuzuru)
    'e2680': [Demon_Sync(505, 561), Demon_Sync(512, 567), Demon_Sync(513, 550)],#Yakumo pre-fight dialogue (Yuzuru, Yakumo, Nuwa)
    'e2685': [Demon_Sync(505, 561), Demon_Sync(512, 567, nameVariant='Yakumo'), Demon_Sync(513, 550)],#Yakumo post-fight dialogue (Yuzuru, Yakumo, Nuwa)
    'e2688': [Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(561, nameVariant='Atsuta')],#Koshimizu meeting after Yakumo fight (Yuzuru)
    'e2700': [Demon_Sync(392, 568), Demon_Sync(567, nameVariant='Yakumo'), Demon_Sync(559), Demon_Sync(554)],#Meeting Agrat (Agrat, Yakumo, Eisheth, Naamah)
    'e2703': [Demon_Sync(392, 568)],#Agrat pre-fight dialogue (Agrat)
    'e2705': [Demon_Sync(392, 568), Demon_Sync(394, 559), Demon_Sync(393, 554)],#Agrat post-fight dialogue (Agrat, Eisheth, Naamah)
    'e2713': [Demon_Sync(391, 569)],#Lilith pre-fight dialogue (Lilith)
    'e2717': [Demon_Sync(391, 569), Demon_Sync(392, 568), Demon_Sync(394, 559), Demon_Sync(393, 554), Demon_Sync(565)],#Lilith post-fight dialogue (Lilith, Agrat, Eisheth, Naamah, Tiamat)
    'e2718': [Demon_Sync(391, 569), Demon_Sync(565)],#Lilith lectures Yoko (Lilith, Tiamat)
    'e2740': [Demon_Sync(506, 578, nameVariant='Ichiro'), Demon_Sync(505, 561, nameVariant='Yuzuru'), Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(511, 564)],#Dazai hat cutscene vengeance (Dazai, Yuzuru, Abdiel)
    'e2760': [Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(564)],#Koshimizu mourns Yuzuru (Yuzuru, Abdiel)
    'e2770': [Demon_Sync(528)],#Koshimizu reveals he's Tsukuyomi (Tsukuyomi)
    'e2790': [Demon_Sync(530, 528)],#Tsukuyomi dialogue after fusing with mc (Tsukuyomi)
    'e2795': [Demon_Sync(530, 528), Demon_Sync(569)],#Qadistu talisman text (Tsukuyomi, Lilith)
    'e2900': [Demon_Sync(530, 528), Demon_Sync(250, 596), Demon_Sync(578, nameVariant='Dazai'), Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(564), Demon_Sync(565)],#Mastema sends you to Shakan (Tsukuyomi, Mastema, Dazai, Yuzuru, Abdiel, Tiamat)
    'e2902': [Demon_Sync(530, 528), Demon_Sync(578, nameVariant='Dazai'), Demon_Sync(596), Demon_Sync(565)],#Tsukuyomi agrees to go to Shakan (Tsukuyomi, Dazai, Mastema, Tiamat)
    'e2910': [Demon_Sync(530, 528)],#Arriving in Shakan (Tsukuyomi)
    'e2912': [Demon_Sync(530, 528), Demon_Sync(578), Demon_Sync(564), Demon_Sync(565)],#Dark block bros pre-fight (Tsukuyomi, Dazai, Abdiel, Tiamat)
    'e2915': [Demon_Sync(530, 528), Demon_Sync(565), Demon_Sync(569), Demon_Sync(559), Demon_Sync(561, nameVariant='Atsuta')],#Shakan angels gossiping (Tsukuyomi, Tiamat, Lilith, Eisheth, Yuzuru)
    'e2917': [Demon_Sync(530, 528)],#Cherub fight dialogue (Tsukuyomi)
    'e2920': [Demon_Sync(530, 528), Demon_Sync(511, 564), Demon_Sync(561, nameVariant='Atsuta')],#Abdiel in Shakan pre-fight dialogue (Tsukuyomi, Abdiel, Yuzuru)
    'e2930': [Demon_Sync(530, 528), Demon_Sync(511, 564), Demon_Sync(565), Demon_Sync(596)],#Abdiel in Shakan post-fight dialogue (Tsukuyomi, Abdiel, Tiamat, Mastema)
    'e2950': [Demon_Sync(530, 528), Demon_Sync(250, 596), Demon_Sync(564)],#Mastema dialogue after Shakan (Tsukuyomi, Mastema, Abdiel)
    'e2953': [Demon_Sync(510, 528)],#Tsukuyomi pre-meeting before area 4 vengeance (Tsukuyomi)
    'e2955': [Demon_Sync(837), Demon_Sync(537), Demon_Sync(510, 528)],#Tsukuyomi meeting before area 4 vengeance (Baal, Lucifer, Tsukuyomi)
    'e2970': [Demon_Sync(528)],#Meeting Goddess Tao vengeance (Tsukuyomi)
    'e2980': [Demon_Sync(510, 528)],#Tsukuyomi meets Goddess Tao (Tsukuyomi)
    'e3000': [Demon_Sync(510, 528)],#Arriving in area 4 vengeance (Tsukuyomi)
    'e3005': [Demon_Sync(530, 528)],#Tsukuyomi senses the keys (Tsukuyomi)
    'e3010': [Demon_Sync(512, 567), Demon_Sync(565)],#Yakumo in area 4 vengeance part 1 (Yakumo, Tiamat)
    'e3015': [Demon_Sync(513, 550)],#Unused? Nuwa line in Yakumo area 4 cutscene (Nuwa)
    'e3020': [Demon_Sync(550), Demon_Sync(512, 567)],#Yakumo in area 4 vengeance part 2 (Nuwa, Yakumo)
    'e3021': [Demon_Sync(567, nameVariant='Yakumo')],#Yakumo background check (Yakumo) includes spread out text
    'e3022': [Demon_Sync(510, 528), Demon_Sync(567, nameVariant='Yakumo')],#Tsukuyomi comments on Yakumo's past (Tsukuyomi, Yakumo)
    'e3030': [Demon_Sync(510, 528), Demon_Sync(512, 567)],#Yakumo saves a student (Tsukuyomi, Yakumo)
    'e3040': [Demon_Sync(512, 567), Demon_Sync(550), Demon_Sync(568), Demon_Sync(510, 528)],#Yakumo in Jojozi (Yakumo, Nuwa, Agrat, Tsukuyomi)
    'e3100': [Demon_Sync(81, 483), Demon_Sync(111, 468), Demon_Sync(845), Demon_Sync(537)],#Beelzebub pre-fight dialogue (Beelzebub, Vasuki, Shiva, Lucifer)
    'e3110': [Demon_Sync(81, 483)],#Beelzebub post-fight dialogue (Beelzebub)
    'e3120': [Demon_Sync(8, 481), Demon_Sync(9, 482)],#Zeus + Odin pre-fight dialogue (Zeus, Odin)
    'e3130': [Demon_Sync(8, 481), Demon_Sync(9, 482)],#Zeus + Odin post-fight dialogue (Zeus, Odin)
    'e3300': [Demon_Sync(530, 528), Demon_Sync(506, 578, nameVariant='Dazai'), Demon_Sync(577)],#Dazai pre-fight dialogue (Tsukuyomi, Dazai, Abdiel)
    'e3310': [Demon_Sync(530, 528), Demon_Sync(561), Demon_Sync(506, 578, nameVariant='Dazai'), Demon_Sync(511, 577)],#Dazai post-fight dialogue (Tsukuyomi, Yuzuru, Dazai, Abdiel)
    'e3330': [Demon_Sync(565), Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(567, nameVariant='Yakumo'), Demon_Sync(578, nameVariant='Dazai')],#Yoko shows up in Empyrean (Tiamat, Yuzuru, Yakumo, Dazai)
    'e3350': [Demon_Sync(565)],#Yoko uses Tiamat on you (Tiamat)
    'e3352': [Demon_Sync(510, 528), Demon_Sync(565)],#Tiamat post-fight dialogue law (Tsukuyomi, Tiamat)
    'e3355': [Demon_Sync(597)],#Tehom pre-fight dialogue (Tehom)
    'e3400': [Demon_Sync(250, 596), Demon_Sync(565)],#Siding with Yoko (Mastema, Tiamat)
    'e3410': [Demon_Sync(250, 596)],#Mastema uses Tiamat on you (Mastema)
    'e3415': [Demon_Sync(530, 528), Demon_Sync(250, 596), Demon_Sync(565)],#Tiamat post-fight dialogue chaos (Tsukuyomi, Mastema, Tiamat)
    'e3420': [Demon_Sync(250, 596)],#Mastema pre-fight dialogue (Mastema)
    'e3425': [Demon_Sync(250, 596)],#Mastema post-fight dialogue (Mastema)
    'e3475': [Demon_Sync(529, 537)],#Lucifer chaos ending dialogue (Lucifer)
    'es035_m063_01': [Demon_Sync(35)],#Fionn dialogue in area 3/4 (Fionn)
    'es152_m062_01': [Demon_Sync(152)],#Hayataro dialogue in fairy village (Hayataro)
    'es152_m063_01': [Demon_Sync(152)],#Hayataro dialogue in Chiyoda (Hayataro)
    'es609_m062_01': [Demon_Sync(452)],#Yuzuru dialogue in fairy village (Lahmu)
    'es611_m063_01': [Demon_Sync(467)],#Dazai dialogue in Chiyoda (Abdiel)
    'es611_m085_01': [Demon_Sync(467)],#Dazai dialogue before Chiyoda (Abdiel)
    'es617_m085b_01': [Demon_Sync(561, nameVariant='Atsuta'), Demon_Sync(578, nameVariant='Dazai')],#Koshimizu dialogue throughout Shinjuku (Yuzuru, Dazai)
    'es618_es418': [Demon_Sync(512, 465, nameVariant='Yakumo'), Demon_Sync(513, 435)],#Misc Nuwa/Yakumo dialogue creation (Yakumo, Nuwa)
    'es632_m062_01': [Demon_Sync(452)],#Goko? Area 2 dialogue (Lahmu)
    'es632_m087_01': [Demon_Sync(452), Demon_Sync(837), Demon_Sync(463)],#Unused researcher or Goko dialogue? (Lahmu, Baal, Arioch)
    'npc_m016': [Demon_Sync(577), Demon_Sync(528), Demon_Sync(596)],#NPC text in Empyrean (Abdiel(Vengeance), Tsukuyomi, Mastema
    'npc_m030': [Demon_Sync(463)],#NPC text in Diet Building (Arioch)
    'npc_m036': [Demon_Sync(467), Demon_Sync(463)],#NPC text in Demon King's Castle (Abdiel, Arioch)
    'npc_m038': [Demon_Sync(596), Demon_Sync(564), Demon_Sync(463)],#NPC text in Shakan (Mastema, Abdiel, Arioch)
    'npc_m060': [Demon_Sync(831), Demon_Sync(566), Demon_Sync(463), Demon_Sync(565), Demon_Sync(509, 152)],#NPC text in Area 4 (Amon, Khonsu(Vengeance), Arioch, Tiamat, Hayataro)
    'npc_m061': [Demon_Sync(537), Demon_Sync(432), Demon_Sync(516), Demon_Sync(870)],#NPC text in Area 1 creation (Lucifer, Hydra, Khonsu, Seth)
    'npc_m061_b': [Demon_Sync(537), Demon_Sync(432), Demon_Sync(566), Demon_Sync(870), Demon_Sync(193, 579)],#NPC text in Area 1 vengeance (Lucifer, Hydra, Khonsu, Seth, Isis)
    'npc_m061_navi': [Demon_Sync(801)],#Navigator text in Area 1 (Pazuzu)
    'npc_m062': [Demon_Sync(452), Demon_Sync(451, nameVariant='Fionn')],#NPC text in Area 2 creation (Lahmu, Fionn)
    'npc_m062_b': [Demon_Sync(556), Demon_Sync(827), Demon_Sync(506, 578)],#NPC text in Area 2 vengeance (Lahmu, Fionn, Girimehkala, Dazai)
    'npc_m063': [Demon_Sync(454), Demon_Sync(455), Demon_Sync(467)],#NPC text in Chiyoda (Surt, Ishtar, Abdiel)
    'npc_m064': [Demon_Sync(463), Demon_Sync(564), Demon_Sync(183, 881), Demon_Sync(775), Demon_Sync(596), Demon_Sync(822), Demon_Sync(772, nameVariant='kuDLaK'), Demon_Sync(505, 561)],#NPC text in Shinjuku (Arioch, Abdiel, Dionysus, Orochi, Mastema, Okuninushi, Kudlak, Yuzuru)
    'npc_m085': [Demon_Sync(578), Demon_Sync(463), Demon_Sync(841)],#NPC text in research lab (Dazai, Arioch, Michael)
    'npc_TokyoMap': [Demon_Sync(465, nameVariant='Yakumo')],#NPC text in world map creation (Yakumo)
    'npc_TokyoMap_b': [Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(567, nameVariant='Yakumo')],#NPC text in world map vengeance (Yuzuru, Yakumo)
}

#Alternative names to use for demons with names longer than 11 characters
DEMON_NAMES_SHORT = {
    'Fionn mac Cumhaill' : 'Fionn',
    'Yamata-no-Orochi' : 'Orochi',
    "Jack-o'-Lantern" : 'Jack-o',
    'Konohana Sakuya' : 'Sakuya',
    'Hecatoncheires' : 'Hecaton',
    'Kushinada-Hime' : 'Kushinada',
    'Glasya-Labolas' : 'Labolas',
    'Yuzuru Atsuta' : 'Yuzuru',
    'Shohei Yakumo' : 'Yakumo',
    'Hare of Inaba' : 'Hare',
    'Mother Harlot' : 'Harlot',
    'Take-Minakata' : 'Minakata',
    'Sukuna-Hikona' : 'Sukuna',
    'Ichiro Dazai' : 'Dazai',
    'Kaya-no-Hime' : 'Kaya',
    'Karasu Tengu' : 'Karasu',
    'Ippon-Datara' : 'Ippon',
    'Leanan Sidhe' : 'Leanan',
    'Principality' : 'Principal',
    'Turbo Granny' : 'Granny',
    'Kurama Tengu' : 'Kurama',
    'Ame-no-Uzume' : 'Uzume',
}

#Demon IDS of bosses mentioned during Aogami conversations in the demon haunt
#Demon_Sync(demonID mentioned in text, IF applicable id of demon to use replacement for) since boss mentions just use normal enemy ids
HAUNT_BENCH_DEMON_IDS = [
    Demon_Sync(450),#Loup Garou
    Demon_Sync(559),#Eisheth
    Demon_Sync(451, nameVariant='Fionn'),#Fionn 1
    Demon_Sync(453),#Final Lahmu
    Demon_Sync(454),#Surt
    Demon_Sync(455),#Ishtar
    Demon_Sync(566),#Khonsu (Vengeance)
    Demon_Sync(561, nameVariant='Yuzuru'),#Yuzuru
    Demon_Sync(596),#Mastema
    Demon_Sync(468),#Vasuki
    Demon_Sync(469),#Zeus
    Demon_Sync(470),#Odin
    Demon_Sync(537),#Lucifer
    Demon_Sync(528),#Tsukuyomi
    Demon_Sync(578, nameVariant='Ichiro'),#Dazai
    Demon_Sync(432),#Hydra
    Demon_Sync(433),#Eligor
    Demon_Sync(434),#Andras
    Demon_Sync(554),#Naamah
    Demon_Sync(466),#Chernobog
    Demon_Sync(568),#Agrat
    Demon_Sync(486),#Cherub
    Demon_Sync(565)#Tiamat
]

#Demon IDS of bosses mentined in the haunt that share a name with other bosses, paired with the text box index they appear in
HAUNT_BENCH_DEMON_IDS_BY_INDEX = [
    (Demon_Sync(467), 49),#Creation Abdiel
    (Demon_Sync(577), 98),#Fallen Abdiel
    (Demon_Sync(577), 101),
    (Demon_Sync(465), 185),#Creation Yakumo
    (Demon_Sync(567, nameVariant='Yakumo'), 58),#Vengeance Yakumo
    (Demon_Sync(567, nameVariant='Yakumo'), 60),
]

#Message files for mission events containing boss checks, which message is the hint message, and what boss demon(name/id) needs to be updated in them
#Value format: [(messageIndex, originalDemonID, hintMessageID), ...]
MISSION_CHECKS_ORIGINAL_IDS = {
    'mm_em0021': [(8, 433, 0)],#Eligor (and Andras)
    'mm_em0020': [(42, 435, 0)],#Snake Nuwa
    'mm_em0043': [(2, 450, 0)],#Loup Garou
    'mm_em0044': [(3, 451, 29)],#Fionn 1 (Creation route)
    'mm_em0060': [(62, 454, 0), (66, 465, 0)],#Surt, Yakumo (Surt is mentioned by name in 2 other messages)
    'mm_em0070': [(49, 455, 0)],#Ishtar (Surt and Ishtar's name are mentioned lots elsewhere)
    'mm_em0150': [(8, 889, 1)],#A Preta Predicament (just one instance currently)
    'mm_em0173': [(16, 888, 0)],#Moving On Up (Oni)
    'mm_em1030': [(5, 801, 26)],#The cursed mermaids (Pazuzu)
    #'mm_em1031': [(10, 801, 0)],#The cursed mermaids (Pazuzu), This message used in several locations
    'mm_em1151': [(35, 810, 0)],#A Goddess Stolen (Loki)
    'mm_em1160': [(8, 804, 2)],#The Tyrant of Tennozu (Belphegor), he says his name with normal enemy version id in 1161
    'mm_em1180': [(6, 821, 3)],#King Frost Quest
    'mm_em1250': [(4, 822, 4)],#Kunitsukami Fight Quest
    'mm_em1260': [(8, 812, 5)],#Chimera Quest
    'mm_em1280': [(32, 564, 33),(33, 564, 34)],#Archangel of Destruction (Vengeance Abdiel)
    'mm_em1290': [(8, 816, 6)],#Roar of Hatred
    'mm_em1401': [(1, 519, 7)],#Khonsu Ra CoC
    'mm_em1420': [(17, 833, 8)],#Fionn 2 Quest
    'mm_em1602': [(13, 877, 0), (14, 877, 0)],#Final Amanozako Quest (Zaou-Gongen)
    'mm_em1770': [(73, 932, 9)],#Mephisto Quest
    'mm_em1780': [(14, 931, 9)],#Cleopatra Quest
    'mm_em1790': [(39, 930, 10)],#Artemis Quest Note: For some reason, the indexing is off on this file
    'mm_em2040': [(26, 755, 11)],#Pisaca Quest
    'mm_em2170': [(76, 757, 12), (77, 758, 13)],#Masakdo Quest, make sure this works as a dialogue choice with or without Kiou sword
    'mm_em2240': [(34, 519, 0)],#Khonsu Ra CoV
    'mm_em2250': [(2, 822, 14)],#VR Kunitsukami Quest
    'mm_em2380': [(121, 781, 0)],#Mo Shuvuu Quest (Andras)
    'mm_em2440': [(3, 768, 15), (254, 768, 15)],#Yaksini Quest
    'mm_em2600': [(39, 948, 16)],#Konohana Sakuya Quest
    'mm_em2610': [(27, 947, 17)],#Dagda Quest
    'mm_em2700': [(84, 783, 35)],#Marici Quest
}

#Message files for story events containing boss checks, which message is the hint message, and what boss demon(name/id) needs to be updated in them
#Value format: [(messageIndex, originalDemonID, hintMessageID), ...]
EVENT_CHECKS_ORIGINAL_IDS = {
    'e0425': [(8, 439, 0), (9, 441, 18)],# Anzus + Lahmu 1
    'e0485': [(1, 452, 0), (2, 453, 18)],#Lahmu 2 (both phases)
    'e0640': [(4, 463, 31), (9, 466, 0)],#Chernobog and Arioch
    'e0715': [(2, 467, 0)],#Creation Abdiel
    'e0825': [(7, 477, 0)],#Metatron
    'e1001': [(3, 537, 9), (10, 537, 19), (11, 529, 20)],#Lucifer
    'e2005': [(1, 431, 0)],#Triple Preta
    'e2008': [(1, 552, 21)],#Labolas 1
    'e2019': [(3, 553, 27)],#Naamah 1
    'e2060': [(8, 554, 28)],#Naamah 2
    'e2245': [(1, 556, 22)],#Vengeance Lahmu
    'e2288': [(13, 559, 30)],#Eisheth
    'e2296': [(3, 451, 29)],#Fionn 1 (Vengeance route)
    'e2500': [(2, 484, 0)],#Power 1, TODO make sure this is the correct power and not a dummy demon replacement
    'e2610': [(1, 579, 0)],#Isis
    'e2708': [(1, 569, 0)],#Lilith
    'e3005': [(3, 483, 32)],#Beelzebub
    'e3352': [(13, 597, 23)],#Tehom
    'em0013': [(10, 889, 24)],#Quest Preta
    'em0025': [(4, 432, 0)],#Hydra
    'npc_m016': [(3, 525, 25)],#Nahobino Abdiel
}

VOICE_REGEX = '<voice.*>\n'
NAME_REGEX = '<chara.*>\n'
HINT_BOSS_PLACEHOLDER = '<BOSSNAME>'
HINT_BOSS_PLACEHOLDER_PLAIN_TEXT = '<BOSSNAMEPLAINTEXT>' #For hint messages that should not use colored text

#Various hint messages that include <BOSSNAME> where the replacement boss name will go
HINT_MESSAGES = ["I'm detecting the presence of <BOSSNAME> ahead.\nWe should proceed with caution.", #0 - Generic Aogami Warning
                 "Us <BOSSNAME>s are always hungry,\nno matter how much we put away.", #1 - A Preta Predicament
                 "<BOSSNAME> has appeared there,\ndwelling at <c look_begin>the peak of a mountain<c look_end>.", #2 - The Tyrant of Tennozu
                 "I have a hunch there might be\n<BOSSNAME> in there.", #3 - Nekomata dialogue for king frost quest
                 "Prove your ability by defeating us. If you can do\nthat, then I, <BOSSNAME>, shall add my power to you.", #4 - Okuninushi dialogue before Kunitsu fight
                 "That reminds me, a fellow demon told me there is a<c look_begin><BOSSNAME><c look_end> somewhere in this area...", #5 - Chimera Quest (Demeter Dialogue)
                 "How about it? Will you slay <BOSSNAME> for me?", #6 - Roar of Hatred
                 "<pc_given>, we may be forced to\nfight <BOSSNAME>. Are you ready?", #7 - Khonsu Ra CoC Quest
                 "Can you overcome <BOSSNAME> at full\npower? What say we find out?", #8 - Fionn 2 Dialogue
                 "I'm detecting the presence of <BOSSNAME> ahead.\nAre you ready to fight?", #9 - Aogami Warning with Confirmation
                 "Let's find out: I ask that you face <BOSSNAME>.\nSpeak to me when you are ready.", #10 - Artemis dialogue, make sure this works properly in game
                 "I ask that you convey my words to humanity\nand slay the demon <BOSSNAME>.", #11 - Armati dialogue in Pisaca Quest
                 "Fight <BOSSNAMEPLAINTEXT>.", #12 - Normal Masakdo
                 "Fight the true <BOSSNAMEPLAINTEXT>.", #13 - The True Masakado
                 "We've received permission to use the data that will allow\nus to simulate a battle against <BOSSNAME> for you.", #14 - VR Kunitsukami Quest
                 "So, uh... I was following Atsuta, but I saw\n<BOSSNAME> around here.", #15 - Dazai dialogue in Yaksini quest
                 "Then it is time for the final test!\nI, <BOSSNAME>, shall judge your power for myself!", #16 - Konohana Sakuya Quest
                 "Now, in this new land, he intends to become\nthe being <BOSSNAME>.", #17 - Danu dialogue in Dagda quest
                 "I'm also detecting the presence of <BOSSNAME>\nbehind the first reading.", #18 - Two-part boss warning
                 "A powerful <BOSSNAMEPLAINTEXT>.", #19 - Normal Lucifer
                 "An extremely powerful <BOSSNAMEPLAINTEXT>.", #20 - True Lucifer
                 "I think I'm detecting <BOSSNAME> ahead.\nIt may ambush us at the train.", #21 - Labolas warning that plays in both routes unfortunately
                 "I'm detecting <BOSSNAME>...? That can't...", #22 - Tao dialogue before vengeance Lahmu
                 "Yoko will turn into <BOSSNAME>.\nWe should probably prepare while we can.", #23 - Tehom
                 "Young man, I'm detecting several\n<BOSSNAME>s within the cave.", #24 - Preta
                 "Naturally, those of Bethel stand with Archangel <BOSSNAME>.", #25 - Abdiel mentioned by Dominion in Empyrean because vengeance Abdiel is in the same file
                 "But one day, <BOSSNAME> arrived.", #26 - Mermaid dialogue in Pazuzu quest
                 "Next we will have to face <BOSSNAME>.\nShe's one of the Qadistu.", #27 - Yoko dialogue after Hydra
                 "Tomorrow morning, you will encounter <BOSSNAME>\non the way to school.", #28 - Yoko dialogue when she transfers to Jouin
                 "<BOSSNAME> detected.\nIt's distant, but I've marked its location.", #29 - Marking Fionn's location on the map
                 "Sounded like they were all\nattacked by <BOSSNAME>.", #30 - Yoko/Tao dialogue after rescuing students attacked by Eisheth
                 "A shame you will never reach\ndemon king <BOSSNAME>...", #31 - Chernobog dialogue
                 "We may even encounter <BOSSNAME>, the lord of the flies.", #32 - Tsukuyomi dialogue about the 3 keys
                 "You have squandered the mercy\ngranted by my fellow archangel, <BOSSNAME>.", #33 - Camael dialogue vengeance
                 "You leave me no choice. As the angel of\ndestruction, I shall slay you in <BOSSNAME>'s stead.", #34 - Camael dialogue vengeance part 2
                 "Speak to me and face <BOSSNAME>."] #35 - Goko dialogue in Marici quest

MISSION_INFO_DEMON_IDS = {
    7: [Demon_Sync(281,802)], #The Ultimate Omelet (Jatayu)
    8: [Demon_Sync(233,801)], #The Cursed Mermaid (Pazuzu)
    9: [Demon_Sync(20,803)], #The Demon of the Spring (Anahita)
    12: [Demon_Sync(89,810)], #A Golden Opportunity (Loki)
    13: [Demon_Sync(311,820)], #Talisman Hunt (Shiki-Ouji)
    15: [Demon_Sync(147,nameVariant="Mothmen")], #Can I Keep Them? (Mothman)
    17: [Demon_Sync(342, 809)], #Kumhanda's Bottle (Kumbhanda)
    18: [Demon_Sync(89,810)], #A Goddess Stolen (Loki)
    22: [Demon_Sync(80,454)], #Hellfire Highway (Surt)
    23: [Demon_Sync(25,455)], #The Augmented Goddess (Ishtar)
    24: [Demon_Sync(212,826)], #The Search for Oyamatsumi (Oyamatsumi)
    28: [Demon_Sync(215,822)], #Clash with the Kunitsukami (Okuninushi)
    30: [Demon_Sync(322,813)], #He of a Hundred Hands (Hecatoncheires)
    31: [Demon_Sync(248,814)], #The Angel of Destruction (Camael)
    34: [Demon_Sync(232,827)], #An Unusual Forecast (Girimekhala)
    35: [Demon_Sync(211,828),Demon_Sync(215,822)], #The Ancient Guardian (Arahabaki,Okuninushi)
    36: [Demon_Sync(206,860)], #Keeper of the South (Zouchouten)
    37: [Demon_Sync(204,862)], #Keeper of the East (Jikokuten)
    38: [Demon_Sync(205,861)], #Keeper of the West (Koumokuten)
    39: [Demon_Sync(203,859)], #Keeper of the North (Bishamonten)
    40: [Demon_Sync(7,516)], #The Egyptians' Fate (Khonsu)
    41: [Demon_Sync(76,831),Demon_Sync(88, 830),Demon_Sync(181,829),Demon_Sync(7,516)], #The Winged Sun (Khonsu,Amons,Mithras,Asura)
    42: [Demon_Sync(7,516)], #The Succession of Ra (Khonsu)
    43: [Demon_Sync(84,832)], #Abaddon's Assault (Abaddon)
    44: [Demon_Sync(35, nameVariant = "Fionn")], #Fionn's Resolve (Fionn)
    45: [Demon_Sync(242, 841)], #The Holy Ring (Michael)
    46: [Demon_Sync(17,837)], #The Bull God's Lineage (Baal)
    47: [Demon_Sync(8,838), Demon_Sync(19)], #A Plot Revealed (Zeus, Demeter)
    48: [Demon_Sync(94,839)], #The Golden Dragon's Arrival (Huang Long)
    49: [Demon_Sync(94,839)], #The Benevolent One (Huang Long)
    50: [Demon_Sync(242),Demon_Sync(83,840)], #The Seraph's Return (Michael, Belial Boss)
    51: [Demon_Sync(242,841),Demon_Sync(83)], #The Red Dragon's Invitation (Michael Boss, Belial)
    52: [Demon_Sync(30,842)], #The Compassionate Queen (Maria)
    53: [Demon_Sync(188,843)], #The Noble Queen (Danu)
    54: [Demon_Sync(189,844)], #The Wrathful Queen (Inanna)
    55: [Demon_Sync(178,845)], #A Universe in Peril (Shiva)
    70: [Demon_Sync(305),Demon_Sync(43,868)], #The Water Nymph (Leanan Sidhe, Apsaras Boss)
    71: [Demon_Sync(305,866),Demon_Sync(43)], #The Spirit of Love (Leanan Sidhe Boss, Apsaras)
    72: [Demon_Sync(13,864)], #The Falcon's Head (Horus)
    73: [Demon_Sync(38,876)], #A Power Beyond Control (Amanozako)
    74: [Demon_Sync(38), Demon_Sync(37,878)], #The Destined Leader (Amanozako, Kurama)
    75: [Demon_Sync(67),Demon_Sync(257,879)], #Those Seeking Sanctuary (Lilim, Principality Boss)
    76: [Demon_Sync(67,880),Demon_Sync(257)], #Holding the Line (Lilim Boss, Principality)
    77: [Demon_Sync(72),Demon_Sync(183,881)], #Black Frost Strikes Back (Black Frost, Dionysus Boss)
    78: [Demon_Sync(72,882),Demon_Sync(183)], #A Sobering Standoff (Black Frost Boss, Dionysus)
    79: [Demon_Sync(265),Demon_Sync(201,883)], #The Raid on Tokyo (Adramelech, Futsunushi Boss)
    80: [Demon_Sync(265,884),Demon_Sync(201)], #In Defense of Tokyo (Adramelech Boss, Futsunushi)
    81: [Demon_Sync(78)], #The Doctor's Last Wish (Mephisto)
    82: [Demon_Sync(295)], #The Rage of a Queen (Cleopatra)
    83: [Demon_Sync(95,933),Demon_Sync(31)], #A Goddess in Training (Quetzacotl, Artemis)
    84: [Demon_Sync(359,921),Demon_Sync(357,922),Demon_Sync(356,923),Demon_Sync(354,924),Demon_Sync(353,925),Demon_Sync(352,926),Demon_Sync(358,927),Demon_Sync(351,928),
            Demon_Sync(350,929),Demon_Sync(934)], #Return of the True Demon (Matador, Daisoujou, Hell Biker, White Rider, Red Rider, Black Rider, Pale Rider, Mother Harlot, Trumpeter, Demi-fiend)
    86: [Demon_Sync(318,888)], #Movin' On Up (Oni)
    87: [Demon_Sync(345,889)], #A Preta Predicament (Preta)
    88: [Demon_Sync(111,468),Demon_Sync(8,469),Demon_Sync(9,470)], #The Three Keys (Vasuki, Zeus, Odin)
    91: [Demon_Sync(441)], #Defending Jozoji Temple (Lahmu)
    92: [Demon_Sync(452)], #Eliminate Lahmu (Lahmu)
    93: [Demon_Sync(25,455),Demon_Sync(80,454),Demon_Sync(82,463)], #Defeat the Demon King's Armies (Surt, Ishtar, Arioch)
    94: [Demon_Sync(240,467)], #Escort the Prime Minister (Abdiel)
    103: [Demon_Sync(236,556),Demon_Sync(391,569)], #Elimate Lahmu (Lahmu, Lilith) CoV
    106: [Demon_Sync(89,810)], #A Golden Opportunity (Loki) CoV
    107: [Demon_Sync(561,nameVariant = "Yuzuru"), Demon_Sync(578,nameVariant = "Dazai")], #Go to Yuzuru's Aid (Yuzuru, Ichiro)
    109: [Demon_Sync(7,566),Demon_Sync(250,596)], #Investigate the Salt Incidents (Khonsu, Mastema)
    111: [Demon_Sync(7,566)], #Rescue Miyazu Atsuta (Khonsu)
    113: [Demon_Sync(565)], #Qadistu Showdown (Tiamat)
    114: [Demon_Sync(565),Demon_Sync(250,596)], #Chase through Shakan (Mastema, Tiamat)
    115: [Demon_Sync(8,481),Demon_Sync(9, 482),Demon_Sync(81,483)], #The Three Keys (Zeus, Odin, Beelzebub)
    138: [Demon_Sync(386), Demon_Sync(41,771)], #Reclaim the Golden Stool (Onyankopon, Anansi Boss)
    139: [Demon_Sync(386,770),Demon_Sync(41)], #Liberate the Golden Stool (Onyankopon Boss, Anansi)
    142: [Demon_Sync(248,814)], #The Angel of Destruction (Camael)
    143: [Demon_Sync(76,831),Demon_Sync(88, 830),Demon_Sync(181,829)], #The Winged Sun (Amons,Mithras,Asura) CoV
    144: [Demon_Sync(359,921),Demon_Sync(357,922),Demon_Sync(356,923),Demon_Sync(354,924),Demon_Sync(353,925),Demon_Sync(352,926),Demon_Sync(358,927),Demon_Sync(351,928),
            Demon_Sync(350,929),Demon_Sync(934)], #Return of the True Demon CoV (Matador, Daisoujou, Hell Biker, White Rider, Red Rider, Black Rider, Pale Rider, Mother Harlot, Trumpeter, Demi-fiend)
    147: [Demon_Sync(38,876)], #A Power Beyond Control CoV (Amanozako)
    148: [Demon_Sync(232,827)], #An Unusual Forecast CoV (Girimekhala)
    150: [Demon_Sync(336),Demon_Sync(107,752)], #Beastly Battle of Wits (Nozuchi, Kodama(Not the ones in the boss fight)
    151: [Demon_Sync(117)], #Brawny Ambitions (Zhu Tun She)
    159: [Demon_Sync(108,769)], #Heart of Garnet (Vouivre)
    161: [Demon_Sync(113),Demon_Sync(41), Demon_Sync(386)], #Tough Love (Basilisk, Onyankopon, Anansi)
    165: [Demon_Sync(227)], #Guardian of Tokyo (Masakado)
    167: [Demon_Sync(318,888)], #Home Sweet Home (Oni)
    172: [Demon_Sync(7,566)], #Rite of Resurrection (Khonsu)
    175: [Demon_Sync(40),Demon_Sync(346,772)], #The Hunter in White (Kresnik, Kudlak Boss)
    176: [Demon_Sync(49,774),Demon_Sync(346)], #The Vampire in Black (Kresnik Boss, Kudlak)
    177: [Demon_Sync(337,890)], #As God Wills (Gogmagog)
    179: [Demon_Sync(386), Demon_Sync(41,771)], #Reclaim the Golden Stool CoV (Onyankopon, Anansi Boss)
    180: [Demon_Sync(386,770),Demon_Sync(41)], #Liberate the Golden Stool CoV (Onyankopon Boss, Anans
    183: [Demon_Sync(200,778)], #Rascal of the Norse (Thor)
    185: [Demon_Sync(278,865)], #Maker of Myth (Garuda)
    188: [Demon_Sync(118,760),Demon_Sync(250,596)], #The Serpent King (Samael, Mastema)
    189: [Demon_Sync(175,754)], #Supersonic Racing (Turbo Granny)
    190: [Demon_Sync(1,681),Demon_Sync(250,596)], #The Great Adversary (Satan, Mastema)
    194: [Demon_Sync(77,892)], #Devotion to Order (Mara)
    197: [Demon_Sync(122)], #Brawny Ambitions II (Xiezhai)
    201: [Demon_Sync(141,751)], #Knocking on Death's Door (Dormarth)
    202: [Demon_Sync(291,891)], #The Disgraced Bird God (Gurulu)
    203: [Demon_Sync(288,756)], #Part-Time Gasser (Zhen)
    205: [Demon_Sync(22,779)], #Goddesses of Fate (Norn)
    206: [Demon_Sync(12,776)], #Will of the Samurai (Atavaka)
    208: [Demon_Sync(212,826),Demon_Sync(32)], #Sakura Cinders of the East (Oyamatsumi, Konohana Sakuya)
    209: [Demon_Sync(4)], #Holy Will and Profane Dissent (Dagda)
    210: [Demon_Sync(103,775)], #Heroes of Heaven and Earth (Yamata-no-Orochi)
    211: [Demon_Sync(8,481),Demon_Sync(237,782)], #God of Old, Devourer of Kin (Zeus, Saturnus)
    218: [Demon_Sync(207)], #Guardian of Light (Marici)
    219: [Demon_Sync(207)], #Guardian of Light (Marici)
    221: [Demon_Sync(242),Demon_Sync(83,840)], #The Seraph's Return CoV (Michael, Belial Boss)
    222: [Demon_Sync(242,841),Demon_Sync(83)], #The Red Dragon's Invitation CoV (Michael Boss, Belial)
}

#Lists of missions without reward page
MISSIONS_WITHOUT_REWARD_PAGE = [147,148]

COLOR_PATTERN = '<c.*?>'
MISSION_CONDITION_DATA_PATTERN = '<mission_cond_name.*?>'
FLAG_PATTERN = "<flag.*?>"
POST_DEMON_REGEX = r"(?:')?" + r"(?:s)?" + r"(?:{})?".format(COLOR_PATTERN) + r"(?:{})?".format(FLAG_PATTERN) + r"(?:')?" + r"(?:s)?" + r"(?:\.)?(?:,)?(?: )?"

MISSION_CONDITION_REPLACEMAX = "Fionn MacCumhaill Capture Pot"
LONGEST_DEMON_NAME = "Fionn MacCumhaill" #written wrong to allow for better regex stuff


SKILL_PATTERN = "<MAGATSUHI_SKILL>"
RACE_PATTERN = "<RACE>"
DEMON_LIST_PATTERN = "<DEMONS>"
ALIGNMENT_PATTERN = "<ALIGNMENT>"
TALISMAN_PATTERN = "Allows you to use the <RACE> Magatsuhi Skill <MAGATSUHI_SKILL>."
PERIAPT_DEMON_PATTERN = "Enables the Magatsuhi Skill <MAGATSUHI_SKILL> when <DEMONS> are brought together."
PERIAPT_ALIGNMENT_PATTERN = "Enables the Magatsuhi Skill <MAGATSUHI_SKILL> when two demons of the <ALIGNMENT> alignment are brought together"

ALIGNMENT_NAMES = {
    1: "NEUTRAL",
    2: "LIGHT",
    3: "DARK",
    4: "LAW",
    5: "CHAOS"
}

#Races and which Key Item ID Talisman belongs to them
RACE_TALISMANS = {
   35 :	806,	#	Haunt Talisman
   8 :	807,    #	Raptor Talisman
   2 :	808,	#	Herald Talisman
    3 :	809,	#	Megami Talisman
   4 :	810,	#	Avian Talisman
   5 :	811,	#	Divine Talisman
   6 :	812,	#	Yoma Talisman
   7 :	813,	#	Vile Talisman
   10 :	814,	#	Deity Talisman
   11 :	815,	#	Wargod Talisman
   12 :	816,	#	Avatar Talisman
   13 :	817,	#	Holy Talisman
   14 :	818,	#	Genma Talisman
   15 :	819,	#	Element Talisman
   17 :	820,	#	Fairy Talisman
   18 :	821,	#	Beast Talisman
   19 :	822,	#	Jirae Talisman
   20 :	823,	#	Fiend Talisman
   21 :	824,	#	Jaki Talisman
   22 :	825,	#	Wilder Talisman
   23 :	826,	#	Fury Talisman
   24 :	827,	#	Lady Talisman
   25 :	828,	#	Dragon Talisman
   26 :	829,	#	Kishin Talisman
   27 :	830,	#	Kunitsu Talisman
   28 :	831,	#	Femme Talisman
   29 :	832,	#	Brute Talisman
   30 :	833,	#	Fallen Talisman
   31 :	834,	#	Night Talisman
   32 :	835,	#	Snake Talisman
   33 :	836,	#	Tyrant Talisman
   34 :	837,	#	Drake Talisman
   36 :	838,	#	Foul Talisman
   40 :	839,	#	Tsukuyomi Talisman
   45 :	840,	#	UMA Talisman
   44 :	841,	#	Enigma Talisman
   46 :	842,	#	Qadištu Talisman
   48 :	843,	#	Primal Talisman
   38 :	844,	#	Devil Talisman
   43 :	845,	#	Panagia Talisman
   37 :	846,	#	Chaos Talisman
}

#Map of demon ID to speaker box name ID for characters without normal enemy demon counterparts
SPECIAL_SPEAKER_IDS = {
    561: 505, # Yuzuru
    528: 510, # Tsukuyomi/Koshimizu
    467: 511, # Abdiels
    525: 511,
    564: 511,
    577: 511,
    465: 512, # Yakumos
    567: 512,
    584: 506, # Dazai
    601: 25, #Abcess Jack Frost (Jack Frost is also Dummy Name)
    25: 25, # Normal Jack Frost
}

'''
Changes the names and descriptions of items with demon names in them to that of their replacement if there is any.
Also adjust the descriptions of talismans and periapts.
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
        comp(List(Compendium_Demon)): list of demons
        fusionSkillIDs (List(Integer)): list of skill ids that are fusion skills 
        fusionSkillReqs (List(Fusion_Requirements)): list of fusion skill requirements
        skillNames (List(String)): list of skill names
        magatsuhiRaceSkills (List(Active_Skill)): list of skills that are magatsuhi race skills
        config (Config_Settings): object containing chosen settings of the randomizer
        TODO: Add Code comments
'''
def updateItemText(encounterReplacements, bossReplacements, demonNames, comp,fusionSkillIDs, fusionSkillReqs, skillNames, magatsuhiRaceSkills, config):  
    itemFile = Message_File('ItemName','',OUTPUT_FOLDERS['ItemName'])

    itemNames = itemFile.getMessageStrings()
    
    for itemName,originalDemonID in ITEM_NAME_SYNC_DEMON_IDS.items():
        if itemName in itemNames:
            if originalDemonID > numbers.NORMAL_ENEMY_COUNT:
                originalName = demonNames[originalDemonID]
                try:
                    replacementID = bossReplacements[originalDemonID]
                except KeyError:
                    continue
            else:
                originalName = demonNames[originalDemonID]
                try:
                    replacementID = encounterReplacements[originalDemonID]
                except KeyError:
                    continue
            if replacementID > numbers.NORMAL_ENEMY_COUNT:
                replacementName = demonNames[replacementID]
            else:
                replacementName = demonNames[replacementID]
            index = itemNames.index(itemName)
            itemNames[index] = itemNames[index].replace(originalName, replacementName)
            #print(str(index) + " " + itemNames[index])
    
    itemFile.setMessageStrings(itemNames)
    itemFile.writeToFiles()

    itemDescFile = Message_File('ItemHelpMess','',OUTPUT_FOLDERS['ItemHelpMess'])

    itemDescs = itemDescFile.getMessageStrings()

    for oldItemID, originalDemonID in ITEM_DESC_SYNC_DEMON_IDS.items():
        if originalDemonID > numbers.NORMAL_ENEMY_COUNT:
            originalName = demonNames[originalDemonID]
            try:
                replacementID = bossReplacements[originalDemonID]
            except KeyError:
                continue
        else:
            originalName = demonNames[originalDemonID]
            try:
                replacementID = encounterReplacements[originalDemonID]
            except KeyError:
                continue
        if replacementID > numbers.NORMAL_ENEMY_COUNT:
            replacementName = demonNames[replacementID]
        else:
            replacementName = demonNames[replacementID]
        
        if oldItemID in ITEM_DESC_DEMON_RACE.keys():#if race is also mentioned
            oldRace = ITEM_DESC_DEMON_RACE[oldItemID]
            newRace = comp[replacementID].race.translation
            itemDescs[oldItemID] = itemDescs[oldItemID].replace(oldRace, newRace)

        itemDescs[oldItemID] = itemDescs[oldItemID].replace(originalName, replacementName)
        #print(itemDescs[oldItemID])
    for skillID in numbers.MAGATSUHI_SKILLS:
        if (skillID == 60 and not config.includeOmagatokiCritical) or (skillID == 928 and not config.includeOmnipotentSuccession): 
            #no need to adjust critical or succession if they aren't in rando pool
            continue
        description = ""
        if skillID in fusionSkillIDs: #skill is fusion skill
            reqs = next(skill for skill in fusionSkillReqs if skill.ind == skillID)
            itemID = reqs.itemID
            if reqs.demons[0] > 0: #skill has demon requirement
                skillDemons = ""
                for demon in reqs.demons:
                    if demon > 0:
                        skillDemons = skillDemons + demonNames[demon] + ", "
                    else:
                        skillDemons = skillDemons[:-2] + " "
                        break
                description = PERIAPT_DEMON_PATTERN.replace(DEMON_LIST_PATTERN, skillDemons).replace(SKILL_PATTERN,skillNames[skillID])
            else: #skill is alignment based
                alignment1 = ALIGNMENT_NAMES[reqs.alignments[0][0]]
                alignment2 = ALIGNMENT_NAMES[reqs.alignments[0][1]]
                description = PERIAPT_ALIGNMENT_PATTERN.replace(ALIGNMENT_PATTERN, alignment1 + " - " + alignment2).replace(SKILL_PATTERN,skillNames[skillID])
            itemDescs[itemID] = description
        else:
            #print(skillID)
            skillObject = next(skill for skill in magatsuhiRaceSkills if skill.ind == skillID)
            if skillObject.magatsuhi.race1.value > 0:
                race = skillObject.magatsuhi.race1.value
                itemID = RACE_TALISMANS[race]

                description=TALISMAN_PATTERN.replace(RACE_PATTERN,RACE_ARRAY[race]).replace(SKILL_PATTERN,skillNames[skillID])
                itemDescs[itemID] = description
            if skillObject.magatsuhi.race2.value > 0:
                race = skillObject.magatsuhi.race2.value
                itemID = RACE_TALISMANS[race]

                description2=TALISMAN_PATTERN.replace(RACE_PATTERN,RACE_ARRAY[race]).replace(SKILL_PATTERN,skillNames[skillID])
                itemDescs[itemID] = description2

    itemDescFile.setMessageStrings(itemDescs)
    itemDescFile.writeToFiles()


'''
Changes the skill descriptions of skills with the same name to differentiate them.
'''
def changeSkillDescriptions(file: Message_File):

    skillDescriptions = file.getMessageStrings()

    for skillID, newDesc in SKILL_DESC_CHANGES.items():
        #print(skillDescriptions[skillID-1])
        skillDescriptions[skillID-1] = newDesc
    
    file.setMessageStrings(skillDescriptions)
    return file

'''
Updates skill descriptions of skills with the same name and updates the unique signifier.
Parameters:
    skillData(List(List)): lists of active, passive and innate skills
'''
def updateSkillDescriptions(skillData):
    file = Message_File('SkillHelpMess','', OUTPUT_FOLDERS['SkillHelpMess'])
    file = changeSkillDescriptions(file)
    file = addSkillOwnershipToDesc(file, skillData)
    file.writeToFiles()

'''
Updates the (Unique) text for skills according to the owner of the skill.
Parameters:
    file(Message_File): the message file to edit
    skillData(List(List)): lists of active, passive and innate skills
'''
def addSkillOwnershipToDesc(file: Message_File, skillData):
    skillDescriptions = file.getMessageStrings()
    for skillTypeList in skillData:#for active skill list, passive skill list and innate skill list
        for skill in skillTypeList:
            owner = skill.owner
            if owner == None: #skip dummy skills
                continue
            if '(Unique)' in skillDescriptions[skill.ind -1] or '(Nahobino)' in skillDescriptions[skill.ind  -1]: #if skill is marked as unique
                if owner.ind == 0:#skill is no longer unique
                    skillDescriptions[skill.ind -1] = skillDescriptions[skill.ind -1].replace('(Unique) ','')
                    skillDescriptions[skill.ind -1] = skillDescriptions[skill.ind -1].replace('(Nahobino) ','')
                elif owner.ind == -1: #skill is nahobino skill
                    skillDescriptions[skill.ind -1] = skillDescriptions[skill.ind -1].replace('(Unique) ','(Nahobino) ')
                elif owner.ind == -3: #skill is enemy only skill
                    skillDescriptions[skill.ind -1] = skillDescriptions[skill.ind -1].replace('(Unique) ','(Enemy) ')
                    skillDescriptions[skill.ind -1] = skillDescriptions[skill.ind -1].replace('(Nahobino) ','(Enemy) ')
                else: #skill owner is actual demon
                    skillDescriptions[skill.ind -1] = skillDescriptions[skill.ind -1].replace('(Unique) ','(' + owner.name + ') ')
                    skillDescriptions[skill.ind -1] = skillDescriptions[skill.ind -1].replace('(Nahobino) ','(' + owner.name + ') ')
            elif owner.ind != 0: #skill is not marked as unique/Nahobino but has an owner
                if owner.ind == -1: #skill is nahobino skill
                    skillDescriptions[skill.ind -1] = '(Nahobino) ' + skillDescriptions[skill.ind -1]
                elif owner.ind == -3: #skill is enemy only skill
                    skillDescriptions[skill.ind -1] = '(Enemy) ' + skillDescriptions[skill.ind -1]
                else: #skill owner is actual demon
                    skillDescriptions[skill.ind -1] = '(' + owner.name + ') ' + skillDescriptions[skill.ind -1]
    file.setMessageStrings(skillDescriptions)
    return file

'''
Update the mention of demon names in mission events.
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
        randomizeQuestJoinDemons(bool): Whether demons that join in quests are randomized to a demon with the same level or kept vanilla
'''
def updateMissionEvents(encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons, brawnyAmbitions2SkillName):
    updateHauntBenchText(encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons)
    updateEventMessages(encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons)
    for missionEvent,syncDemons in MISSION_EVENTS_DEMON_IDS.items():
        try:
            file = Message_File(missionEvent,'/MissionEvent/',OUTPUT_FOLDERS['MissionFolder'])
            missionText = file.getMessageStrings()
            originalMissionText = copy.deepcopy(missionText)
            updateDemonsInTextFile(missionText, originalMissionText, syncDemons,encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons)
            speakerNames = file.getSpeakerNames();
            originalSpeakerNames = copy.deepcopy(speakerNames)
            updateSpeakerNamesInFile(speakerNames, originalSpeakerNames, syncDemons,encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons)
            
            if missionEvent in MISSION_CHECKS_ORIGINAL_IDS.keys():
                hints = MISSION_CHECKS_ORIGINAL_IDS[missionEvent]
                addHintMessagesInFile(missionText, hints, bossReplacements, demonNames)
            if missionEvent == BRAWNY_AMBITIONS_2:
                updateSkillNameInFile(missionText, brawnyAmbitions2SkillName)
            file.setMessageStrings(missionText)
            file.setSpeakerNames(speakerNames)
            file.writeToFiles()
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)
    for missionEvent,hints in MISSION_CHECKS_ORIGINAL_IDS.items():
        if missionEvent in MISSION_EVENTS_DEMON_IDS.keys():
            continue
        try:
            file = Message_File(missionEvent,'/MissionEvent/',OUTPUT_FOLDERS['MissionFolder'])
            missionText = file.getMessageStrings()
            addHintMessagesInFile(missionText, hints, bossReplacements, demonNames)
            file.setMessageStrings(missionText)
            file.writeToFiles()
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)
            
'''
Update the mention of demon names in story event messages.
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
        randomizeQuestJoinDemons(bool): Whether demons that join in quests are randomized to a demon with the same level or kept vanilla
'''
def updateEventMessages(encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons):
    for missionEvent,syncDemons in EVENT_MESSAGE_DEMON_IDS.items():
        try:
            file = Message_File(missionEvent,'/EventMessage/',OUTPUT_FOLDERS['EventMessage'])
            missionText = file.getMessageStrings()
            originalMissionText = copy.deepcopy(missionText)
            updateDemonsInTextFile(missionText, originalMissionText, syncDemons,encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons)
            speakerNames = file.getSpeakerNames();
            originalSpeakerNames = copy.deepcopy(speakerNames)
            updateSpeakerNamesInFile(speakerNames, originalSpeakerNames, syncDemons,encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons)
            if missionEvent in EVENT_CHECKS_ORIGINAL_IDS.keys():
                hints = EVENT_CHECKS_ORIGINAL_IDS[missionEvent]
                addHintMessagesInFile(missionText, hints, bossReplacements, demonNames)
            
            file.setMessageStrings(missionText)
            file.setSpeakerNames(speakerNames)
            file.writeToFiles()
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)
    for missionEvent,hints in EVENT_CHECKS_ORIGINAL_IDS.items():
        if missionEvent in EVENT_MESSAGE_DEMON_IDS.keys():
            continue
        try:
            file = Message_File(missionEvent,'/EventMessage/',OUTPUT_FOLDERS['EventMessage'])
            missionText = file.getMessageStrings()
            addHintMessagesInFile(missionText, hints, bossReplacements, demonNames)
            file.setMessageStrings(missionText)
            file.writeToFiles()
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)
            

'''
Update the mention of demon names for the bench in demon haunts.
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
        randomizeQuestJoinDemons(bool): Whether demons that join in quests are randomized to a demon with the same level or kept vanilla
'''
def updateHauntBenchText(encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons):
        file = Message_File('GardenMsg_PlayerTalk','',OUTPUT_FOLDERS['Garden'])
        missionText = file.getMessageStrings()
        originalMissionText = copy.deepcopy(missionText)
        updateDemonsInTextFile(missionText, originalMissionText,HAUNT_BENCH_DEMON_IDS,encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons)
        for syncDemon, index in HAUNT_BENCH_DEMON_IDS_BY_INDEX:
            originalDemonID = syncDemon.ind #id of demon mentionend in text
            syncDemonID = syncDemon.sync #id of demon that replacement should be gotten for
            originalName = demonNames[originalDemonID]
            try:
                replacementID = encounterReplacements[syncDemonID]
            except KeyError:
                continue
            #replacementID = 451 #Fionn is the longes Demon Name so use it as Test Case
            replacementName = demonNames[replacementID]
            if originalName in originalMissionText[index]: #Name is plain text
                box = box.replace(originalName, replacementName)
            if 'enemy ' + str(originalDemonID).zfill(3) in originalMissionText[index]: #name is talked about via ID
                box = box.replace('enemy ' + str(originalDemonID).zfill(3), 'enemy ' + str(replacementID).zfill(3))
            if syncDemon.nameVariant and syncDemon.nameVariant in originalMissionText[index]:#Name is a variant on normal name (Mothmen instead of Mothman)
                box = box.replace(syncDemon.nameVariant, replacementName)
        file.setMessageStrings(missionText)
        file.writeToFiles()

'''
Update the mention of demon names in a single event message file
    Parameters:
        missionText(List(String)): List of all text boxes in the file to update
        originalMissionText(List(String)): Unchanging version of the text boxes to find original demon names to replace
        syncDemons(List(Demon_Sync)): List of all demons that need to be updated to their replacements
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
        randomizeQuestJoinDemons(bool): Whether demons that join in quests are randomized to a demon with the same level or kept vanilla
'''
def updateDemonsInTextFile(missionText, originalMissionText, syncDemons, encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons):
    for syncDemon in syncDemons:
        originalDemonID = syncDemon.ind #id of demon mentionend in text
        syncDemonID = syncDemon.sync #id of demon that replacement should be gotten for
        if syncDemonID in numbers.SCRIPT_JOIN_DEMONS.values() and not randomizeQuestJoinDemons: #If demon isn't getting replaced ignore it
            continue
        originalName = demonNames[originalDemonID]
        if syncDemonID > numbers.NORMAL_ENEMY_COUNT: # if demon to get replacement from is a normal enemy
            try:
                replacementID = bossReplacements[syncDemonID]
            except KeyError:
                #print("Key Error: " + str(syncDemonID))
                continue
        else: #else it is a boss
            try:
                replacementID = encounterReplacements[syncDemonID]
            except KeyError:
                #print("Key Error: " + str(syncDemonID))
                continue
        #replacementID = 451 #Fionn is the longes Demon Name so use it as Test Case
        replacementName = demonNames[replacementID]

        #print(str(originalDemonID) + " " + originalName + " -> " + str(replacementID) + " " + replacementName)
        for index, box in enumerate(missionText): #for every dialogue box
            
            if originalName in originalMissionText[index]: #Name is plain text
                box = box.replace(originalName, replacementName)
            if 'enemy ' + str(originalDemonID).zfill(3) in originalMissionText[index]: #name is talked about via ID
                box = box.replace('enemy ' + str(originalDemonID).zfill(3), 'enemy ' + str(replacementID).zfill(3))
                #box = box.replace('<enemy ' + str(originalDemonID) + '>', replacementName)
                #print(box)
            if syncDemon.nameVariant and syncDemon.nameVariant in originalMissionText[index]:#Name is a variant on normal name (Mothmen instead of Mothman)
                box = box.replace(syncDemon.nameVariant, replacementName)
            if 'chara ' + str(originalDemonID) + '>' in originalMissionText[index]: #Replace 'speaker' name
                box = box.replace('chara ' + str(originalDemonID) + '>', 'chara ' + str(normalEnemyIDForBoss(replacementID, demonNames)) + '>')
                #if originalDemonID == 43:
                #    print(box)
            #lines = box.split("\n")
            #for line in lines:
            #     pass

            missionText[index] = box
            
'''
Update the mention of text box speaker names in a single event message file
    Parameters:
        speakerNames(List(String)): List of all names in the file to update
        originalSpeakerNames(List(String)): Unchanging version of the names to find original demon names to replace
        syncDemons(List(Demon_Sync)): List of all demons that need to be updated to their replacements
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
        randomizeQuestJoinDemons(bool): Whether demons that join in quests are randomized to a demon with the same level or kept vanilla
'''
def updateSpeakerNamesInFile(speakerNames, originalSpeakerNames, syncDemons, encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons):
    for syncDemon in syncDemons:
        originalDemonID = syncDemon.ind #id of demon mentioned in text
        syncDemonID = syncDemon.sync #id of demon that replacement should be gotten for
        if syncDemonID in numbers.SCRIPT_JOIN_DEMONS.values() and not randomizeQuestJoinDemons: #If demon isn't getting replaced ignore it
            continue
        #originalName = demonNames[originalDemonID]
        if syncDemonID > numbers.NORMAL_ENEMY_COUNT: # if demon to get replacement from is a normal enemy
            try:
                replacementID = bossReplacements[syncDemonID]
            except KeyError:
                continue
        else: #else it is a boss
            try:
                replacementID = encounterReplacements[syncDemonID]
            except KeyError:
                continue
        #replacementID = 451 #Fionn is the longes Demon Name so use it as Test Case
        #replacementName = demonNames[replacementID]
        replacementID = normalEnemyIDForBoss(replacementID, demonNames)

        #print(str(originalDemonID) + " " + originalName + " -> " + str(replacementID) + " " + replacementName)
        for index, name in enumerate(speakerNames): #for every text box name
            if bytes(str(originalDemonID), 'utf-8') + b'\x00' == bytes(originalSpeakerNames[index]):
                speakerNames[index] = bytes(str(replacementID), 'utf-8') + b'\x00' #Add null byte to end of demon ID

'''
Adds hint messages for checks related to mission events
Parameters:
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
'''
def addHintMessages(bossReplacements, demonNames):
    addStoryHintMessages(bossReplacements, demonNames)
    for missionEvent,hints in MISSION_CHECKS_ORIGINAL_IDS.items():
        try:
            file = Message_File(missionEvent,'/MissionEvent/',OUTPUT_FOLDERS['MissionFolder'])
            missionText = file.getMessageStrings()
            addHintMessagesInFile(missionText, hints, bossReplacements, demonNames)
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)
            
'''
Adds hint messages for checks related to story events
Parameters:
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
'''
def addStoryHintMessages(bossReplacements, demonNames):
    for missionEvent,hints in EVENT_CHECKS_ORIGINAL_IDS.items():
        try:
            file = Message_File(missionEvent,'/EventMessage/',OUTPUT_FOLDERS['EventMessage'])
            missionText = file.getMessageStrings()
            addHintMessagesInFile(missionText, hints, bossReplacements, demonNames)
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)
            
'''
Adds hint messages for a single text file
Parameters:
        missionText(List(String)): List of all text boxes in the file to update
        hints(List((messageIndex, originalDemonID, hintMessageID))): List of all hints for the file including the boss IDs to replace
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
'''
def addHintMessagesInFile(missionText, hints, bossReplacements, demonNames):
    for hintInfo in hints:
        messageIndex = hintInfo[0]
        originalDemonID = hintInfo[1]
        hintIndex = hintInfo[2]
        originalName = demonNames[originalDemonID]
        try:
            replacementID = bossReplacements[originalDemonID]
        except KeyError:
            continue
        #replacementID = 451 #Fionn is the longes Demon Name so use it as Test Case
        replacementName = demonNames[replacementID]
        
        #print(str(originalDemonID) + " " + originalName + " -> " + str(replacementID) + " " + replacementName)
        
        
        #for index, box in enumerate(missionText):
        #    print(index)
        #    print(box)
            
        hintBox = missionText[messageIndex]
        #print(hintBox)
        match = re.search(VOICE_REGEX, hintBox)
        boxMetadata = ""
        if match:
            splitIndex = match.span()[1]
            boxMetadata = hintBox[:splitIndex]
            #print(boxMetadata)
        else:
            match = re.search(NAME_REGEX, hintBox)
            if match:
                splitIndex = match.span()[1]
                boxMetadata = hintBox[:splitIndex]
        hintMessage = boxMetadata + createHintMessageWithID(replacementID, hintIndex) #TODO - Differentiate bosses with the same name using the non-ID version of this function
        missionText[messageIndex] = hintMessage
        #print(hintMessage)

'''
Returns a hint message using a direct string by replacing <BOSSNAME> in a placeholder hint message
'''
def createHintMessage(bossName, hintIndex):
    message = HINT_MESSAGES[hintIndex]
    message = message.replace(HINT_BOSS_PLACEHOLDER, bossName)
    message = message.replace(HINT_BOSS_PLACEHOLDER_PLAIN_TEXT, bossName)
    return message

'''
Returns a hint message using a direct string by replacing <BOSSNAME> in a placeholder hint message
'''
def createHintMessageWithID(bossID, hintIndex):
    message = HINT_MESSAGES[hintIndex]
    message = message.replace(HINT_BOSS_PLACEHOLDER, '<c look_begin><enemy ' + str(bossID) + '><c look_end>')
    message = message.replace(HINT_BOSS_PLACEHOLDER_PLAIN_TEXT, '<enemy ' + str(bossID) + '>')
    return message

'''
Updates the mission info file with randomized demon replacements and adds additional rewards to description.
    Parameters:
        encounterReplacements(Dict): map of normal demon ids and their replacements
        bossReplacements(Dict): map of boss demon ids and their replacements
        demonNames(List(String)): list of names of demons
        brawnyAmbition2Skill(String): name of the skill required for Brawny Ambition II
        fakeMissions(List(Fake_Mission)): list of fake missions to add rewards to description for
        itemNames(List(String)): list of item names
'''
def updateMissionInfo(encounterReplacements, bossReplacements, demonNames, brawnyAmbition2Skill, fakeMissions, itemNames, randomizeQuestJoinDemons):
    file = Message_File('MissionInfo','/',OUTPUT_FOLDERS['MissionInfo'])

    missionText = file.getMessageStrings()
    
    commonEntries = 3 #first 3 are common for all missions
    missionTextCount = 7 #Name,Client, Reward, Explain, Help, Report, Completed
    
    for missionIndex, syncDemons in MISSION_INFO_DEMON_IDS.items():
        for syncDemon in syncDemons:
            originalDemonID = syncDemon.ind #id of demon mentionend in text
            syncDemonID = syncDemon.sync #id of demon that replacement should be gotten for
            if syncDemonID in numbers.SCRIPT_JOIN_DEMONS.values() and not randomizeQuestJoinDemons: #If demon isn't getting replaced ignore it
                continue
            originalName = demonNames[originalDemonID]
            if syncDemonID > numbers.NORMAL_ENEMY_COUNT: # if demon to get replacement from is a normal enemy
                try:
                    replacementID = bossReplacements[syncDemonID]
                except KeyError:
                    continue
            else: #else it is a boss
                try:
                    replacementID = encounterReplacements[syncDemonID]
                except KeyError:
                    continue
            #replacementID = 451 #Fionn is the longes Demon Name so use it as Test Case
            replacementName = demonNames[replacementID]

            for index in range(missionTextCount):
                messageComponent = missionText[commonEntries + index + 7 * (missionIndex)]
                #print(str(missionIndex) + "/" + str(index) + " " + messageComponent)
                if originalName in messageComponent: #Name is plain text
                    messageComponent = messageComponent.replace(originalName, replacementName)
                if 'enemy ' + str(originalDemonID).zfill(3) in messageComponent: #name is talked about via ID
                    messageComponent = messageComponent.replace('enemy ' + str(originalDemonID).zfill(3), 'enemy ' + str(replacementID).zfill(3))
                if syncDemon.nameVariant and syncDemon.nameVariant in messageComponent:#Name is a variant on normal name (Mothmen instead of Mothman)
                    messageComponent = messageComponent.replace(syncDemon.nameVariant, replacementName)
                if numbers.BRAWNY_AMBITIONS2_SKILL in messageComponent:
                    messageComponent = messageComponent.replace(numbers.BRAWNY_AMBITIONS2_SKILL, brawnyAmbition2Skill)

                lines = messageComponent.split("\n") #Split at line break
                messageComponent = ""
                for lineIndex,line in enumerate(lines):
                    if len(replacementName) > len(originalName) and ("<enemy" in line or replacementName in line):
                        #replacement's name is longer and name is in line
                
                        replacedText = re.sub(COLOR_PATTERN,"",line) #Replace color patterns
                        replacedText = re.sub(FLAG_PATTERN,"",replacedText) #Replace flag patterns
                        
                        replacedText = re.sub(MISSION_CONDITION_DATA_PATTERN,MISSION_CONDITION_REPLACEMAX,replacedText) #Replace mission condition patterns with the maximum value they can have (I think?)
                
                        replacedNew = re.sub('<enemy ' + str(replacementID).zfill(3) + '>',replacementName,replacedText) #put replacement name where it should be

                        if "<enemy" in replacedNew: #if there are potential names left, put longest possible name
                            replacedNew = re.sub('<enemy.*?>',LONGEST_DEMON_NAME,replacedNew)
                
                        if len(replacedNew) > MAX_LINE_LENGTH: #after replacements line is still too long
                            if "<enemy " + str(replacementID).zfill(3) + '>' in line: #enemy call is in line
                                match = re.search('<enemy ' + str(replacementID).zfill(3) + '>' + POST_DEMON_REGEX,line)
                                replacedMatch = re.search(replacementName,replacedNew)
                            elif MISSION_CONDITION_DATA_PATTERN in line: #if some text is gotten via mission condition name
                                match = re.search(MISSION_CONDITION_DATA_PATTERN,line)
                                replacedMatch = re.search(MISSION_CONDITION_REPLACEMAX,replacedNew)
                            else: #name is plaintext
                               match = re.search(replacementName + POST_DEMON_REGEX,line)
                               replacedMatch = re.search(replacementName,replacedNew)
                            if match: #found enemy of current replacement demon
                                replacedIndex = replacedMatch.start()
                                startIndex = match.start()
                                endIndex = match.end()
                                if replacedIndex < len(replacedNew) /2: #is in first half of line
                                    line = line[:endIndex]+ '\n' + line[endIndex:] #put line break after
                                else: #is in second half of line
                                    line = line[:startIndex] + '\n' + line[startIndex:] #put line break before
                            
                    if lineIndex +1 < len(lines): #is not last line
                        messageComponent = messageComponent + line + "\n"
                    else:
                        messageComponent = messageComponent + line
                missionText[commonEntries + index + 7 * (missionIndex)] = messageComponent
    
    missionText = addAdditionalRewardsToMissionInfo(fakeMissions, missionText, itemNames)

    try:
        file.setMessageStrings(missionText)
        file.writeToFiles()
    except UnicodeEncodeError:
        print("Error encoding mission info")

'''
Adds additional rewards to the missions description.
    Parameters:
        fakeMissions(List(Fake_Mission)): list of fake missions to add rewards to description for
        itemNames(List(String)): list of item names
'''
def addAdditionalRewardsToMissionInfo(fakeMissions, missionText, itemNames):
    for mission in fakeMissions:
        for missionID in mission.infoInds: #List of mission ids to add the reward of this fake mission to
            explainIndex = missionText.index('NOT USED:mis_info_' + str(missionID).zfill(4) +'_report') -2
            explainText = missionText[explainIndex]
            
            newItemName = itemNames[mission.reward.ind]
            if 'NOT' in newItemName:
                print(str(mission.reward.ind) + " " + newItemName)

            addOn = "Additional Reward: <c look_begin>" + newItemName + "<c look_end>\n　\n"

            explainText = addOn + explainText
            missionText[explainIndex] = explainText
    return missionText
          
'''
Finds the earliest ID of a demon's name that is used for dialogue box speaker names in 'chara' tags'
If the demon uses a specific name ID instead of their normal enemy version, the specific one is returned instead
    Parameters:
        bossID (number): The boss ID to find an earlier version of
        demonNames (List(String)): List of enemy demon names
'''
def normalEnemyIDForBoss(bossID, demonNames):
    if bossID in SPECIAL_SPEAKER_IDS.keys():
        return SPECIAL_SPEAKER_IDS[bossID]
    earliestID = demonNames.index(demonNames[bossID])
    #if earliestID > 394:
    #    print(demonNames[earliestID] + " " + str(earliestID))
    return earliestID

'''
Updates occurences of Puncture Punch with the new skill name.
'''
def updateSkillNameInFile(missionText, skillName):
    for index, box in enumerate(missionText): #for every dialogue box
        if numbers.BRAWNY_AMBITIONS2_SKILL in box:
            box = box.replace(numbers.BRAWNY_AMBITIONS2_SKILL, skillName)
        missionText[index] = box
