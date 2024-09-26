
import util.numbers as numbers
from base_classes.message import Message_File

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
MISSION_EVENTS_DEMON_IDS = {
    'mm_em2030': 117,#Brawny Ambitions (Zhu Tun She)
    'mm_em1300': 864,#Falcon's Head (Horus Punishing Foe)
    'mm_em1400': 864,#Isis Dialogue (Either for other quest or in Minato) (Horus Punishing Foe)
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
'''
def updateSkillDescriptions(config):
    file = Message_File('SkillHelpMess','', OUTPUT_FOLDERS['SkillHelpMess'])
    file = changeSkillDescriptions(file)
    #TODO: Add function to update (Unique) to reflect inheritance setting and demons
    file.writeToFiles()

'''
Update the mention of demon names in mission events.
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
'''
def updateMissionEvents(encounterReplacements, bossReplacements, demonNames):
    for missionEvent,originalDemonID in MISSION_EVENTS_DEMON_IDS.items():
        file = Message_File(missionEvent,'/MissionEvent/',OUTPUT_FOLDERS['MissionFolder'])
        missionText = file.getMessageStrings()

        originalName = demonNames[originalDemonID]
        if originalDemonID > numbers.NORMAL_ENEMY_COUNT:
            try:
                replacementID = bossReplacements[originalDemonID]
            except KeyError:
                continue
        else:
            try:
                replacementID = encounterReplacements[originalDemonID]
            except KeyError:
                continue
        #replacementID = 451 #Fionn is the longes Demon Name so use it as Test Case
        if replacementID > numbers.NORMAL_ENEMY_COUNT:
            replacementName = demonNames[replacementID]
        else:
            replacementName = demonNames[replacementID]
        
        print(str(originalDemonID) + " " + originalName + " -> " + str(replacementID) + " " + replacementName)
        
        
        for index, box in enumerate(missionText):

            if originalName in box: #Name is plain text
                box = box.replace(originalName, replacementName)
            if 'enemy ' + str(originalDemonID) in box: #name is talked about via ID and text is colored
                box = box.replace('enemy ' + str(originalDemonID), 'enemy ' + str(replacementID))
                #box = box.replace('<enemy ' + str(originalDemonID) + '>', replacementName)
            
            #TODO: Dialogue issues i was having was not due too line length, but still might be necessary once I actually find a case where it's relevant
            # lines = box.split("\n")
            # for line in lines:
            #     pass

            missionText[index] = box
        file.setMessageStrings(missionText)
        file.writeToFiles()
