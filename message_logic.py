
import util.numbers as numbers
import re
from base_classes.message import Message_File, Demon_Sync

MAX_LINE_LENGTH = 50 #Arbitray Number ( at least correct for missionInfo Text)

OUTPUT_FOLDERS = {
    'ItemName' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
    'SkillHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Battle/Skill/',
    'MissionFolder' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Mission/MissionEvent/',
    'ItemHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
    'MissionInfo' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Mission/'
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

#Message files for events and what demon(name/id) needs to be updated in them
#Demon_Sync(demonID mentioned in text, IF applicable id of demon to use replacement for) since boss mentions just use normal enemy ids
MISSION_EVENTS_DEMON_IDS = {
    'mm_em2030': [Demon_Sync(117)],#Brawny Ambitions (Zhu Tun She)
    'mm_em1300': [Demon_Sync(864),Demon_Sync(453),Demon_Sync(463)],#Falcon's Head (Horus Punishing Foe,Shinagawa Station Lahmu II, Arioch)
    'mm_em1400': [Demon_Sync(864)],#Isis Dialogue (Either for other quest or in Minato) (Horus Punishing Foe)
    'mm_em1020': [Demon_Sync(115,432),Demon_Sync(281,802)], #The Ultimate Omelet (Hydra, Jatayu)
    'mm_em1120': [Demon_Sync(147,nameVariant="Mothmen")], #Can I Keep Them? (Mothman)
    'mm_em0060': [Demon_Sync(80, 454)],#Hellfire Highway (Surt)
    'mm_em0070': [Demon_Sync(80, 454), Demon_Sync(25, 455)],#Ishtar Quest (Surt and Ishtar)
    'mm_em0143': [Demon_Sync(111, 468), Demon_Sync(178, 845)],#Taito India Amanozako dialogue (Vasuki and Shiva)
    'mm_em0145': [Demon_Sync(8, 469)],#Taito Greek Amanozako dialogue (Zeus)
    'mm_em0147': [Demon_Sync(9, 470)],#Taito Norse Amanozako dialogue (Odin)
    'mm_em0151': [Demon_Sync(43)],#A Preta Predicament (Apsaras)
    'mm_em0152': [Demon_Sync(345, 889)],#A Preta Predicament (Preta)
    'mm_em0170': [Demon_Sync(318, 888)],#Moving on up (Oni, 4 quest files)
    'mm_em0171': [Demon_Sync(318, 888)],
    'mm_em0173': [Demon_Sync(318, 888)],
    'mm_em0174': [Demon_Sync(318, 888)],
    'mm_em1031': [Demon_Sync(233, 801)],#The Cursed Mermaids (Pazuzu)
    'mm_em1040': [Demon_Sync(20, 803)],#Anahita Quest (Anahita, 2 quest files)
    'mm_em1041': [Demon_Sync(20, 803)],
    'mm_em1050': [Demon_Sync(311, 820)],#Talisman Hunt (Shiki Ouji)
    'mm_em1140': [Demon_Sync(342, 809)],#Kumbhanda Quest (Kumbhanda)
    'mm_em1150': [Demon_Sync(89, 810)],#A Goddess Stolen (Loki, 2 quest files)
    'mm_em1151': [Demon_Sync(89, 810)],
    'mm_em1160': [Demon_Sync(86, 804)],#The Tyrant of Tennozu (Belphegor, 2 quest files)
    'mm_em1161': [Demon_Sync(86, 804)],
    'mm_em1180': [Demon_Sync(87, 821)],#King Frost Quest (King Frost, 2 quest files)
    'mm_em1182': [Demon_Sync(87, 821)],
    'mm_em1210': [Demon_Sync(212, 826), Demon_Sync(80, 454)],#Oyamatsumi Quest (Oyamatsumi and Surt)
    'mm_em1250': [Demon_Sync(215, 822), Demon_Sync(212, 826)],#Kunitsukami Fight Quest (Okuninushi and Oyamatsumi)
    'mm_em1260': [Demon_Sync(127, 812)], #Chimera Quest (Chimera)
    'mm_em1270': [Demon_Sync(322, 813)], #Hecaton Quest (Hecaton)
    'mm_em1280': [Demon_Sync(248, 814)], #The Archangel of Destruction (Camael, Abdiel is mentioned but there's not one specific boss to pull her from)
    'mm_em1290': [Demon_Sync(85, 816), Demon_Sync(86, 804)],#Roar of Hatred (Moloch, Belphegor)
    'mm_em1320': [Demon_Sync(232, 827)],#Girimehkala Quest (Girimehkala)
    'mm_em1330': [Demon_Sync(211, 828), Demon_Sync(206, 860), Demon_Sync(205, 861), Demon_Sync(204, 862), Demon_Sync(203, 863)],#Lord's Sword Quest (Arahabaki, Zouchouten, Koumokuten, Jikokuten, Bishamonten)
    'mm_em1340': [Demon_Sync(206, 860)],#Zouchouten Event Battle Dialogue
    'mm_em1350': [Demon_Sync(205, 861)],#Koumokuten Event Battle Dialogue
    'mm_em1360': [Demon_Sync(204, 862)],#Jikokuten Event Battle Dialogue
    'mm_em1370': [Demon_Sync(203, 863)],#Bishamonten Event Battle Dialogue
    'mm_em1380': [Demon_Sync(7, 516), Demon_Sync(82, 463)],#Khonsu CoC Quest (Khonsu, Arioch)
    'mm_em1390': [Demon_Sync(181, 829), Demon_Sync(88, 830), Demon_Sync(76, 831), Demon_Sync(7, 516), Demon_Sync(82, 463)],#The Winged-Sun Crest (Asura, Mithras, Amon, Khonsu, Arioch)
    'mm_em1401': [Demon_Sync(15, 519), Demon_Sync(7, 516), Demon_Sync(13, 864)],#Khonsu Ra CoC Quest (Khonsu Ra, Khonsu, Horus)
    'mm_em1410': [Demon_Sync(84, 832)],#Abbadon's Assault (Abaddon)
    'mm_em1420': [Demon_Sync(35)],#Fionn 2 Quest (Fionn)
    'mm_em1430': [Demon_Sync(243, 836), Demon_Sync(247, 834), Demon_Sync(245, 835), Demon_Sync(242, 841)],#3 Seraphim Quest (Gabriel, Uriel, Raphael, Michael):
    'mm_em1440': [Demon_Sync(17, 837), Demon_Sync(86, 804), Demon_Sync(85, 816), Demon_Sync(81, 483), Demon_Sync(2, 537)],#Baal Quest (Baal, Belphegor, Moloch, Beelzebub, Lucifer)
    'mm_em1450': [Demon_Sync(8, 838), Demon_Sync(19)],#A Plot Unveiled (Zeus, Demeter)
    'mm_em1460': [Demon_Sync(94, 839)],#The Gold Dragon's Arrival (Huang Long)
    'mm_em1480': [Demon_Sync(83, 840), Demon_Sync(242), Demon_Sync(82, 463)],#Side with Michael (Belial, Michael, Arioch)
    'mm_em1490': [Demon_Sync(242, 841), Demon_Sync(83), Demon_Sync(82, 463)],#Side with Belial (Michael, Belial, Arioch)
    'mm_em1500': [Demon_Sync(30, 842), Demon_Sync(188, 843), Demon_Sync(189, 844)],#Seed of Life Quest (Maria, Danu, Innana)
    'mm_em1530': [Demon_Sync(178, 845), Demon_Sync(111, 468)],#A Universe in Peril (Shiva, Vasuki)
    'mm_em1570': [Demon_Sync(845)],#Sarasvati Collection Quest (Shiva)
    'mm_em1590': [Demon_Sync(876), Demon_Sync(453)],#Berserk Amanozako Quest (Amanozako, 3 Quest Files, Final Lahmu)
    'mm_em1591': [Demon_Sync(876)],
    'mm_em1592': [Demon_Sync(876)],
    'mm_em1600': [Demon_Sync(38), Demon_Sync(454)], #Final Amanozako Quest (Amanozako, 4 Quest Files, Surt)
    'mm_em1601': [Demon_Sync(38)],
    'mm_em1602': [Demon_Sync(38), Demon_Sync(877)], #Zaou-Gongen Mentioned here and in 1603
    'mm_em1603': [Demon_Sync(38), Demon_Sync(877)],
    'mm_em1630': [Demon_Sync(868), Demon_Sync(305), Demon_Sync(867)], #Side with Leanan (Apsaras, Leanan, Ippon Datara)
    'mm_em1640': [Demon_Sync(866), Demon_Sync(43)], #Side with Apsaras (Leanan, Apsaras)
    'mm_em1641': [Demon_Sync(43), Demon_Sync(889)], #Apsaras' Followers Dialogue (Apsaras, 2 Quest Files, Preta)
    'mm_em1642': [Demon_Sync(43)],
    'mm_em1650': [Demon_Sync(879), Demon_Sync(67)], #Side with Lilim (Principality, Lilim)
    'mm_em1660': [Demon_Sync(880), Demon_Sync(257)], #Side with Principality (Lilim, Principality)
    'mm_em1670': [Demon_Sync(881), Demon_Sync(72)], #Side with Black Frost (Dionysus, Black Frost)
    'mm_em1680': [Demon_Sync(882), Demon_Sync(183)], #Side with Dionysus (Black Frost, Dionysus)
    'mm_em1690': [Demon_Sync(883), Demon_Sync(265)], #Side with Adramelech (Futsunushi, Adramelech)
    'mm_em1700': [Demon_Sync(884), Demon_Sync(201)], #Side with Futsunushi (Adramelech, Futsunushi)
    'mm_em1769': [Demon_Sync(78), Demon_Sync(295), Demon_Sync(31), Demon_Sync(4), Demon_Sync(528)], #Tokyo Diet Building Researcher (Mephisto, Cleopatra, Artemis, Dagda, Tsukuyomi) TODO: Differentiate between boss and summonable versions. Optionally add Yuzuru and Yoko/Tehom?
    'mm_em1770': [Demon_Sync(78)], #Mephisto Quest (Mephisto)
    'mm_em1780': [Demon_Sync(295)], #Cleopatra Quest (Cleopatra)
    'mm_em1790': [Demon_Sync(31), Demon_Sync(933), Demon_Sync(432), Demon_Sync(838)], #Artemis Quest (Artemis, Queztalcoatl, Hydra, Zeus 2 for fun)
    'mm_em1802': [Demon_Sync(921)], #Matador, 2 Quest Files
    'mm_em1803': [Demon_Sync(921)],
    'mm_em1805': [Demon_Sync(922)], #Daisoujou
    'mm_em1807': [Demon_Sync(923)], #Hell Biker
    'mm_em1810': [Demon_Sync(924)], #White Rider, 2 Quest Files
    'mm_em1811': [Demon_Sync(924)],
    'mm_em1812': [Demon_Sync(925)], #Red Rider, 2 Quest Files
    'mm_em1813': [Demon_Sync(925)],
    'mm_em1814': [Demon_Sync(926)], #Black Rider, 2 Quest Files
    'mm_em1815': [Demon_Sync(926)],
    'mm_em1817': [Demon_Sync(927)], #Pale Rider
    'mm_em1820': [Demon_Sync(928)], #Mother Harlot
    'mm_em1821': [Demon_Sync(929)], #Trumpeter, 2 Quest Files
    'mm_em1822': [Demon_Sync(929), Demon_Sync(934)], #Demi-Fiend named here as well
    'mm_em1823': [Demon_Sync(934)], #Demi-Fiend, 3 Quest Files
    'mm_em1824': [Demon_Sync(934)],
    'mm_em1825': [Demon_Sync(934)],
    'mm_em2020': [Demon_Sync(752), Demon_Sync(336)], #Nozuchi Queset (Nozuchi, Normal Enemy Kodama)
    'mm_em2040': [Demon_Sync(803)], #Pisaca Quest part 1 (Anahita)
    'mm_em2111': [Demon_Sync(769)], #Vouivre Quest (Vouivre)
    'mm_em2130': [Demon_Sync(113), Demon_Sync(41), Demon_Sync(386)], #Basilisk Hunt Quest (Basilisk, Anansi, Onyankopon)
    'mm_em2170': [Demon_Sync(227)], #Masakado Quest (Masakado)
    'mm_em2190': [Demon_Sync(552), Demon_Sync(888)], #Halphas Quest (Oni, Glasya-Labolas 1)
    'mm_em2240': [Demon_Sync(519), Demon_Sync(566), Demon_Sync(561, nameVariant='Yuzuru'), Demon_Sync(864), Demon_Sync(577), Demon_Sync(578)], #Vengeance Khonsu-Ra Quest (Khonsu Ra, Khonsu, Yuzuru, Horus, Fallen Abdiel, Dazai)
    'mm_em2270': [Demon_Sync(772), Demon_Sync(40)], #Side with Kresnik (Kudlak, Kresnik)
    'mm_em2280': [Demon_Sync(774), Demon_Sync(346)], #Side with Kudlak (Kresnik, Kudlak)
    'mm_em2290': [Demon_Sync(890)], #Gogmagog Quest (Gogmagog)
    'mm_em2310': [Demon_Sync(770), Demon_Sync(41)], #Side with Onyankopon (Onyankopon, Anansi) - Swapped boss/recruit versions due to the way these 2 join compared to others
    'mm_em2320': [Demon_Sync(771), Demon_Sync(386)], #Side with Anansi (Anansi, Onyankopon)
    'mm_em2350': [Demon_Sync(778)], #Idun Haunt Quest (Thor)
    'mm_em2370': [Demon_Sync(865)], #Siegfried Quest (Garuda)
    'mm_em2390': [Demon_Sync(776), Demon_Sync(227)], #Cironnup Quest (Atavaka, Masakado)
    'mm_em2400': [Demon_Sync(760), Demon_Sync(537)], #Samael Quest (Samael, Lucifer)
    'mm_em2420': [Demon_Sync(681), Demon_Sync(760), Demon_Sync(537), Demon_Sync(596)], #Satan Quest (Satan, Samael, Lucifer, Mastema)
    'mm_em2460': [Demon_Sync(892)], #Mara Quest (Mara)
    'mm_em2470': [Demon_Sync(754, nameVariant='TURBO GRANNY')], #Turbo Granny Quest (Turbo Granny)
    'mm_em2490': [Demon_Sync(122)], #Hare of Inaba 2 Quest (Xiezhai) TODO: Replace Puncture Punch with updated skill
    'mm_em2500': [Demon_Sync(215), Demon_Sync(122), Demon_Sync(214)], #Hare of Inaba 3 Quest (Okuninushi, Xiezhai, Sukona Hikona for fun)
    'mm_em2530': [Demon_Sync(751, nameVariant='DORMARTH')], #Dormarth Quest (Dormarth)
    'mm_em2540': [Demon_Sync(891)], #Gurulu  Quest (Gurulu)
    'mm_em2550': [Demon_Sync(756, nameVariant='ZHEn')], #Part Time Quest (Zhen) Optionally add the other 2 encounters you can get here but eh
    'mm_em2570': [Demon_Sync(779), Demon_Sync(838)], #Moirae Haunt Quest (Norn, Zeus 2 for fun)
    'mm_em2580': [Demon_Sync(776, nameVariant='Daigensui Myouou')], #Yoshitsune Haunt Quest (Atavaka)
    'mm_em2600': [Demon_Sync(32), Demon_Sync(826)], #Konohana Sakuya Quest (Konohana Sakuya, Oyamatsumi)
    'mm_em2610': [Demon_Sync(4), Demon_Sync(843)], #Dagda Quest (Dagda, Danu for fun)
    'mm_em2620': [Demon_Sync(775, nameVariant='Orochi'), Demon_Sync(528)], #Orochi Quest (Orochi, Tsukuyomi)
    'mm_em2630': [Demon_Sync(782), Demon_Sync(481), Demon_Sync(837)], #Saturnus Quest (Saturnus, CoV Zeus, Baal)
    'mm_em2640': [Demon_Sync(569), Demon_Sync(564)], #Package Delivery Quest (Lilith, Vengeance Abdiel) Optionally add Yoko Hiromine as Tehom?
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

#Message files for events containing boss checks, which message is the hint message, and what boss demon(name/id) needs to be updated in them
#Value format: [(messageIndex, originalDemonID, hintMessageID), ...]
MISSION_CHECKS_ORIGINAL_IDS = {
    'mm_em0021': [(8, 433, 0)],#Eligor (and Andras)
    'mm_em0020': [(42, 435, 0)],#Snake Nuwa
    'mm_em0043': [(2, 450, 0)],#Loup Garou
    'mm_em0060': [(62, 454, 0), (66, 465, 0)],#Surt, Yakumo (Surt is mentioned by name in 2 other messages)
    'mm_em0070': [(49, 455, 0)],#Ishtar (Surt and Ishtar's name are mentioned lots elsewhere)
    'mm_em0150': [(8, 889, 1)],#A Preta Predicament (just one instance currently)
    'mm_em0173': [(16, 888, 0)],#Moving On Up (Oni)
    'mm_em1031': [(10, 801, 0)],#The cursed mermaids (Pazuzu), he says his name elsewhere but with his normal enemy version id
    'mm_em1151': [(35, 810, 0)],#A Goddess Stolen (Loki)
    'mm_em1160': [(8, 804, 2)],#The Tyrant of Tennozu (Belphegor), he says his name with normal enemy version id in 1161
    'mm_em1180': [(6, 821, 3)],#King Frost Quest
    'mm_em1250': [(4, 822, 4)],#Kunitsukami Fight Quest
    'mm_em1260': [(8, 812, 5)],#Chimera Quest
    'mm_em1290': [(8, 816, 6)],#Roar of Hatred
    'mm_em1401': [(1, 519, 7)],#Khonsu Ra CoC
    'mm_em1420': [(17, 833, 8)],#Fionn 2 Quest
    'mm_em1602': [(13, 877, 0), (14, 877, 0)],#Final Amanozako Quest (Zaou-Gongen)
    'mm_em1770': [(73, 932, 9)],#Mephisto Quest
    'mm_em1780': [(14, 931, 9)],#Cleopatra Quest
    'mm_em1790': [(33, 930, 10)],#Artemis Quest
    'mm_em2040': [(26, 755, 11)],#Pisaca Quest
    'mm_em2170': [(53, 757, 12), (76, 757, 12), (77, 758, 13)],#Masakdo Quest, make sure this works as a dialogue choice with or without Kiou sword
    'mm_em2240': [(34, 519, 0)],#Khonsu Ra CoV
    'mm_em2250': [(2, 822, 14)],#VR Kunitsukami Quest
    'mm_em2380': [(121, 781, 0)],#Mo Shuvuu Quest (Andras)
    'mm_em2440': [(3, 768, 15)],#Yaksini Quest
    'mm_em2600': [(39, 948, 16)],#Konohana Sakuya Quest
    'mm_em2610': [(27, 947, 17)],#Dagda Quest
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
                 "Now, in this new land, he intends to become\nthe being <BOSSNAME>."] #17 - Danu dialogue in Dagda quest

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
    74: [Demon_Sync(38), Demon_Sync(37,878)], #The Destined Leader (Amanozako, Kurama) #TODO: Ensure Kurama replacement works
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
    103: [Demon_Sync(236,556)], #Elimate Lahmu (Lahmu) CoV
    106: [Demon_Sync(89,810)], #A Golden Opportunity (Loki) CoV
    109: [Demon_Sync(7,566)], #Investigate the Salt Incidents (Khonsu)
    111: [Demon_Sync(7,566)], #Rescue Miyazu Atsuta (Khonsu)
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
    175: [Demon_Sync(40),Demon_Sync(346,772)], #The Hunter in White (Kresnik, Kudlak Boss)
    176: [Demon_Sync(49,774),Demon_Sync(346)], #The Vampire in Black (Kresnik Boss, Kudlak)
    177: [Demon_Sync(337,890)], #As God Wills (Gogmagog)
    179: [Demon_Sync(386), Demon_Sync(41,771)], #Reclaim the Golden Stool CoV (Onyankopon, Anansi Boss)
    180: [Demon_Sync(386,770),Demon_Sync(41)], #Liberate the Golden Stool CoV (Onyankopon Boss, Anans
    183: [Demon_Sync(200,778)], #Rascal of the Norse (Thor)
    185: [Demon_Sync(278,865)], #Maker of Myth (Garuda)
    188: [Demon_Sync(118,760)], #The Serpent King (Samael)
    189: [Demon_Sync(175,754)], #Supersonic Racing (Turbo Granny)
    190: [Demon_Sync(1,681)], #The Great Adversary (Satan)
    194: [Demon_Sync(77,892)], #Devotion to Order (Mara)
    197: [Demon_Sync(122)], #Brawny Ambitions II (Xiezhai)
    201: [Demon_Sync(141,751)], #Knocking on Death's Door (Dormarth)
    202: [Demon_Sync(291,891)], #The Disgraced Bird God (Gurulu)
    205: [Demon_Sync(22,779)], #Goddesses of Fate (Norn)
    206: [Demon_Sync(12,776)], #Will of the Samurai (Atavaka)
    208: [Demon_Sync(212,826),Demon_Sync(32)], #Sakura Cinders of the East (Oyamatsumi, Konohana Sakuya)
    209: [Demon_Sync(4)], #Holy Will and Profane Dissent (Dagda)
    210: [Demon_Sync(103,775)], #Heroes of Heaven and Earth (Yamata-no-Orochi)
    211: [Demon_Sync(8,481),Demon_Sync(237,782)], #God of Old, Devourer of Kin (Zeus, Saturnus)
    221: [Demon_Sync(242),Demon_Sync(83,840)], #The Seraph's Return CoV (Michael, Belial Boss)
    222: [Demon_Sync(242,841),Demon_Sync(83)], #The Red Dragon's Invitation CoV (Michael Boss, Belial)
}

'''
Changes the names and descriptions of items with demon names in them to that of their replacement if there is any
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
        comp(List(Compendium_Demon)): list of demons
'''
def updateItemTextWithDemonNames(encounterReplacements, bossReplacements, demonNames, comp):  
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
def updateMissionEvents(encounterReplacements, bossReplacements, demonNames, randomizeQuestJoinDemons):
    for missionEvent,syncDemons in MISSION_EVENTS_DEMON_IDS.items():
        try:
            file = Message_File(missionEvent,'/MissionEvent/',OUTPUT_FOLDERS['MissionFolder'])
            missionText = file.getMessageStrings()

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

                #print(str(originalDemonID) + " " + originalName + " -> " + str(replacementID) + " " + replacementName + " for mission " + missionEvent)
            
                for index, box in enumerate(missionText): #for every dialogue box
                    if originalName in box: #Name is plain text
                        box = box.replace(originalName, replacementName)
                    if 'enemy ' + str(originalDemonID).zfill(3) in box: #name is talked about via ID
                        box = box.replace('enemy ' + str(originalDemonID).zfill(3), 'enemy ' + str(replacementID).zfill(3))
                        #box = box.replace('<enemy ' + str(originalDemonID) + '>', replacementName)
                        #print(box)
                    if syncDemon.nameVariant and syncDemon.nameVariant in box:#Name is a variant on normal name (Mothmen instead of Mothman)
                        box = box.replace(syncDemon.nameVariant, replacementName)
                    #TODO: Dialogue issues i was having was not due too line length, but still might be necessary once I actually find a case where it's relevant
                    # lines = box.split("\n")
                    # for line in lines:
                    #     pass

                    missionText[index] = box
            file.setMessageStrings(missionText)
            file.writeToFiles()
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)


'''
Adds hint messages for various checks
Parameters:
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
'''
def addHintMessages(bossReplacements, demonNames):
    for missionEvent,hints in MISSION_CHECKS_ORIGINAL_IDS.items():
        try:
            file = Message_File(missionEvent,'/MissionEvent/',OUTPUT_FOLDERS['MissionFolder'])
            missionText = file.getMessageStrings()
            for hintInfo in hints:
                messageIndex = hintInfo[0]
                originalDemonID = hintInfo[1]
                hintIndex = hintInfo[2]
                originalName = demonNames[originalDemonID]
                try:
                    replacementID = bossReplacements[originalDemonID]
                except KeyError:
                    pass
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
            file.setMessageStrings(missionText)
            file.writeToFiles()
        except AssertionError:
            print("Error during message read for mission file " + missionEvent)

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
def updateMissionInfo(encounterReplacements, bossReplacements, demonNames, brawnyAmbition2Skill, fakeMissions, itemNames):
    file = Message_File('MissionInfo','/',OUTPUT_FOLDERS['MissionInfo'])

    missionText = file.getMessageStrings()
    
    commonEntries = 3 #first 3 are common for all missions
    missionTextCount = 7 #Name,Client, Reward, Explain, Help, Report, Completed
    
    for missionIndex, syncDemons in MISSION_INFO_DEMON_IDS.items():
        for syncDemon in syncDemons:
            originalDemonID = syncDemon.ind #id of demon mentionend in text
            syncDemonID = syncDemon.sync #id of demon that replacement should be gotten for
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
            explainText = missionText[3 + missionID * 7 + 3]
            newItemName = itemNames[mission.reward.ind]

            addOn = "Additional Reward: <c look_begin>" + newItemName + "<c look_end>\n　\n"

            explainText = addOn + explainText
            missionText[3 + missionID * 7 + 3] = explainText
    return missionText

            



