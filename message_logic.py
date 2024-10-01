
import util.numbers as numbers
import re
from base_classes.message import Message_File, Demon_Sync

MAX_LINE_LENGTH = 50 #Arbitray Number 

OUTPUT_FOLDERS = {
    'ItemName' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
    'SkillHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Battle/Skill/',
    'MissionFolder' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Mission/MissionEvent/',
    'ItemHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
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
    'mm_em0151': [Demon_Sync(43)],#A Preta Predicament (Apsaras) TODO: Handle case if guest demons do not join at same level (always apsaras, etc)
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
    'mm_em1390': [Demon_Sync(181, 829), Demon_Sync(76, 831), Demon_Sync(7, 516), Demon_Sync(82, 463)],#The Winged-Sun Crest (Asura, Amon, Khonsu, Arioch) TODO: Add Mithras 830, who is named but not the first demon in a boss encounter
    'mm_em1401': [Demon_Sync(15, 519), Demon_Sync(7, 516), Demon_Sync(13, 864)],#Khonsu Ra CoC Quest (Khonsu Ra, Khonsu, Horus)
    'mm_em1410': [Demon_Sync(84, 832)],#Abbadon's Assault (Abaddon)
    'mm_em1420': [Demon_Sync(35)],#Fionn 2 Quest (Fionn)
    'mm_em1430': [Demon_Sync(243, 836), Demon_Sync(242, 841)],#3 Seraphim Quest (Gabriel, Michael): Add Uriel 834 and Raphael 835, who are named but not the first demon in a boss encounter
    'mm_em1440': [Demon_Sync(17, 837), Demon_Sync(86, 804), Demon_Sync(85, 816), Demon_Sync(81, 483), Demon_Sync(2, 537)],#Baal Quest (Baal, Belphegor, Moloch, Beelzebub, Lucifer)
    'mm_em1450': [Demon_Sync(8, 838), Demon_Sync(19)],#A Plot Unveiled (Zeus, Demeter)
    'mm_em1460': [Demon_Sync(94, 839)],#The Gold Dragon's Arrival (Huang Long)
    'mm_em1480': [Demon_Sync(83, 840), Demon_Sync(242), Demon_Sync(82, 463)],#Side with Michael (Belial, Michael, Arioch)
    'mm_em1490': [Demon_Sync(242, 841), Demon_Sync(83), Demon_Sync(82, 463)],#Side with Belial (Michael, Belial, Arioch)
    'mm_em1500': [Demon_Sync(30, 842), Demon_Sync(188, 843), Demon_Sync(189, 844)],#Seed of Life Quest (Maria, Danu, Innana)
    'mm_em1530': [Demon_Sync(178, 845), Demon_Sync(111, 468)],#A Universe in Peril (Shiva, Vasuki)
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
}

VOICE_REGEX = '<voice.*>\n'
NAME_REGEX = '<chara.*>\n'
HINT_BOSS_PLACEHOLDER = '<BOSSNAME>'

#Various hint messages that include <BOSSNAME> where the replacement boss name will go
HINT_MESSAGES = ["I'm detecting the presence of <BOSSNAME> ahead.\nWe should proceed with caution.", #0 - Generic Aogami Warning
                 "Us <BOSSNAME>s are always hungry,\nno matter how much we put away.", #1 - A Preta Predicament
                 "<BOSSNAME> has appeared there,\ndwelling at <c look_begin>the peak of a mountain<c look_end>.", #2 - The Tyrant of Tennozu
                 "I have a hunch there might be\n<BOSSNAME> in there.", #3 - Nekomata dialogue for king frost quest
                 "Prove your ability by defeating us. If you can do\nthat, then I, <BOSSNAME>, shall add my power to you.", #4 - Okuninushi dialogue before Kunitsu fight
                 "That reminds me, a fellow demon told me there is a<c look_begin><BOSSNAME><c look_end> somewhere in this area...", #5 - Chimera Quest (Demeter Dialogue)
                 "How about it? Will you slay <BOSSNAME> for me?", #6 - Roar of Hatred
                 "<pc_given>, we may be forced to\nfight <BOSSNAME>. Are you ready?", #7 - Khonsu Ra CoC Quest
                 "Can you overcome <BOSSNAME> at full\npower? What say we find out?"] #8 - Fionn 2 Dialogue

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
TODO: Fix out of bounds related assertion error related when reading some mission files
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
'''
def updateMissionEvents(encounterReplacements, bossReplacements, demonNames):
    for missionEvent,syncDemons in MISSION_EVENTS_DEMON_IDS.items():
        try:
            file = Message_File(missionEvent,'/MissionEvent/',OUTPUT_FOLDERS['MissionFolder'])
            missionText = file.getMessageStrings()

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

                #print(str(originalDemonID) + " " + originalName + " -> " + str(replacementID) + " " + replacementName)
            
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
    return message

'''
Returns a hint message using a direct string by replacing <BOSSNAME> in a placeholder hint message
'''
def createHintMessageWithID(bossID, hintIndex):
    message = HINT_MESSAGES[hintIndex]
    message = message.replace(HINT_BOSS_PLACEHOLDER, '<c look_begin><enemy ' + str(bossID) + '><c look_end>')
    return message