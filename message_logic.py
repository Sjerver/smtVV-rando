
import util.numbers as numbers
from base_classes.message import Message_File

MAX_LINE_LENGTH = 50 #Arbitray Number 

OUTPUT_FOLDERS = {
    'ItemName' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Item/',
    'SkillHelpMess' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Battle/Skill/',
    'MissionFolder' : 'rando/Project/Content/L10N/en/Blueprints/Gamedata/BinTable/Mission/MissionEvent/',
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

SKILL_DESC_CHANGES = {
    295 : '(Unique) Significantly raises Accuracy/Evasion of <skill_tgt> by 2 ranks for 3 turns.', #Red Capote Boss Version
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
Changes the names of items with demon names in them to that of their replacement if there is any
    Parameters:
        encounterReplacements(Dict): map for which demon replaces which demon as normal encounter
        bossReplacements(Dict): map for which boss replaces which boss
        demonNames(list(String)): list of demon names
'''
def updateItemTextWithDemonNames(encounterReplacements, bossReplacements, demonNames):  
    
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
def updateSkillDescriptions():
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
