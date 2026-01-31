from configparser import ConfigParser
from util.binary_table import Table, writeBinaryTable, writeFolder, copyFile, readBinaryTable
from base_classes.demons import Compendium_Demon, Enemy_Demon, Stat, Stats, Item_Drop, Item_Drops, Demon_Level, Boss_Flags, Duplicate, Encounter_Spawn
from base_classes.skills import Active_Skill, Passive_Skill, Skill_Condition, Skill_Conditions, Skill_Level, Skill_Owner, Fusion_Requirements
from base_classes.fusions import Normal_Fusion, Special_Fusion, Fusion_Chart_Node
from base_classes.encounters import Encounter_Symbol, Encounter, Possible_Encounter, Event_Encounter, Battle_Event, Unique_Symbol_Encounter, Ambush_Type
from base_classes.base import Translated_Value, Weight_List
from base_classes.nahobino import Nahobino, LevelStats
from base_classes.item import *
from base_classes.quests import Mission, Mission_Reward, Mission_Condition, Mission_Container
from base_classes.settings import Settings
from base_classes.miracles import Abscess, Miracle
from base_classes.demon_assets import Asset_Entry, Position, UI_Entry, Talk_Camera_Offset_Entry
from base_classes.map_demons import Map_Demon
from base_classes.map_event import Map_Event
from base_classes.navigators import Navigator
from base_classes.file_lists import Script_File_List, General_UAsset
from util.jsonExports import BASE_MAPSYMBOLPARAMS, VOICEMAP_ESCAPE, VOICEMAP_FIND
from pprint import pprint
import script_logic as scriptLogic
import message_logic as message_logic
import model_swap
import util.numbers as numbers
from util.numbers import RACE_ARRAY, Canon
import util.paths as paths
import util.translation as translation
import boss_logic as bossLogic
import base_classes.message as message
import math
import os
import random
import gui
import string
import pandas as pd
import copy
import shutil
import traceback
import csv

DEV_CHEATS = False

class Randomizer:
    def __init__(self):
        self.maccaMod = numbers.getMaccaValues()
        self.expMod = numbers.getExpValues()

        self.compendiumNames = [] #TODO: Remove
        self.skillNames = []
        self.itemNames = []
        self.originalItemNames = []

        self.compendiumArr = []
        self.skillArr = []
        self.passiveSkillArr = []
        self.innateSkillArr = []
        self.normalFusionArr = []
        self.fusionChartArr = []
        self.specialFusionArr = []
        self.enemyArr = []
        self.encountSymbolArr = []
        self.encountArr = []
        self.consumableArr = []
        self.essenceArr = []
        self.shopArr = []
        self.eventEncountArr = []
        self.staticEventEncountArr = []
        self.bossArr = []
        self.playerBossArr = []
        self.enemyNames = []
        self.staticBossArr = []
        self.bossFlagArr = []
        self.bossDuplicateMap = {}
        self.mimanRewardsArr = []
        self.vendingMachineArr = []
        self.battleEventArr = []
        self.devilAssetArr = []
        self.overlapCopies = []
        self.missionArr = []
        self.abscessArr = []
        self.devilUIArr = []
        self.talkCameraOffsets = []
        self.miracleArr = []
        self.uniqueSymbolArr = []
        self.staticUniqueSymbolArr = []
        self.updatedNormalEncounters = []
        self.chestArr = []
        self.mapSymbolArr = []
        self.mapSymbolFile = General_UAsset("MapSymbolParamTable","rando/Project/Content/Blueprints/Map/Encount/Mover/ParamTable/")
        self.bossSymbolReplacementMap = {}
        self.validBossDemons = set()
        self.essenceBannedBosses = set()
        self.checkBossInfo = {}
        self.updatedMissionConditionIDs = []
        self.encounterReplacements = {}
        self.bossReplacements = {}
        self.pressTurnChance = 0
        self.brawnyAmbitions2SkillName = "Puncture Punch"
        self.fusionSkillIDs = []
        self.fusionSkillReqs = []
        self.alreadyAssignedSkills = set()
        self.scriptFiles = Script_File_List()
        self.mapEventArr = []
        self.navigatorArr = []
        self.navigatorVoiceIDs = [] #IDs of demon voices in 3-digit string form that have 13 (navi find) and 14 (navi go) voice lines
        self.naviReplacementMap = {}
        self.naviParamFile = General_UAsset("NaviDevilParamTable", "rando/Project/Content/Blueprints/Map/Gimic/Daath/")
        self.voiceMapFile = General_UAsset("BP_DevilVoiceAssetMap","rando/Project/Content/Sound/DevilVoice/")
        self.nahobino = Nahobino()
        self.totalResistMap = {} #stores all assigned resistances for each element 
        self.itemReplacementMap = {}
        self.skillReplacementMap = {}
        self.eventFlagNames = {}
        
        self.configSettings = Settings()
        self.textSeed = ""

        self.elementals = [155,156,157,158]
        self.specialFusionDemonIDs = []
        self.guestReplacements = {}

        self.dummyEventIndex = 0
        self.itemDebugList = {}
        self.progressionItemNewChecks = {}
        self.nonRedoableItemIDs = []
        self.itemValidityMap = {}
        self.essenceValidityMap = {}
        self.originalEssenceValidityMap = {}
        self.relicValidityMap = {}
    
    '''
    Reads the text file containing Character Names and filters out just the names and saves all names in array compendiumNames.
        Returns: 
            The buffer containing CharacterNames
    '''
    def readDemonNames(self):
        #TODO: No longer needed!
        with open(paths.CHARACTER_NAME_IN, 'r') as file:
            fileContents = file.read()   
            tempArray = fileContents.split("MessageLabel=")
            tempArray.pop(0)
            for element in tempArray:
                sliceStart = element.find("MessageTextPages_3=")
                sliceEnd = element.find("Voice=")
                self.compendiumNames.append(element[sliceStart + 19:sliceEnd - 7])
        return fileContents
    
    '''
    Reads the text file containing Skill Names and filters out just the names and saves all names in array skillNames.
        Returns: 
            The buffer containing SkillNames
    '''
    def readSkillNames(self):
        with open(paths.SKILL_NAME_IN, 'r', encoding="utf-8") as file:
            fileContents = file.read()   
            tempArray = fileContents.split("MessageLabel=")
            for element in tempArray:
                sliceStart = element.find("MessageTextPages_3=")
                sliceEnd = element.find("Voice=")
                self.skillNames.append(element[sliceStart + 19:sliceEnd - 7])
        return fileContents
    
    '''
    Reads the text file containing Item Names and filters out just the names and saves all names in array itemNames.
        Returns: 
            The buffer containing itemNames
    '''
    def readItemNames(self):
        with open(paths.ITEM_NAME_IN, 'r', encoding="utf-8") as file:
            fileContents = file.read()   
            tempArray = fileContents.split("MessageLabel=")
            tempArray.pop(0)
            for element in tempArray:
                sliceStart = element.find("MessageTextPages_3=")
                sliceEnd = element.find("Voice=")
                self.itemNames.append(element[sliceStart + 19:sliceEnd - 7])
        self.originalItemNames =copy.deepcopy(self.itemNames)
        return fileContents
    
    '''
    Reads the csv file contaning names for all enemy demons including bosses and saves all names in list enemyNames
        Returns: 
            The list of enemy names
    '''
    def readDataminedEnemyNames(self):
        df = pd.read_csv(paths.NKM_CSV_IN, skiprows=4)
        self.enemyNames = df['Name'].values.tolist()

    '''
    Reads the csv file contaning names for all enemy demons including bosses and saves all names in list enemyNames
        Returns: 
            The list of enemy names
    '''
    def readEventFlagNames(self):
        df = pd.read_csv(paths.EVENT_FLAG_NAMES)
        for index, row in df.iterrows():
            name = row['Flag']
            ind = row['ID']
            self.eventFlagNames[name] = ind

    '''
    Returns the demons current Name from their ID.
    Parameters:
        demonID (Integer): the id of the demon
    '''
    def getDemonsCurrentNameByID(self,demonID):
        if demonID >= len(self.compendiumArr):
            name = self.compendiumNames[self.playerBossArr[demonID].nameID]
        else:
            name = self.compendiumNames[self.compendiumArr[demonID].nameID]
        return name
            
    '''
    Fills the array compendiumArr with data extracted from the Buffer NKMBaseTable.
    The end array contains data on all demons which are registered in the compendium and usable by the player.
        Parameters:
            NKMBaseTable (Table): the buffer to get the demon data from
    '''
    def fillCompendiumArr(self, NKMBaseTable):
        #For all demons in the compendium...
        for index in range(numbers.NORMAL_ENEMY_COUNT):
            demon = self.createCompendiumDemon(NKMBaseTable, index, False)
            #Add read demon data to compendium
            self.compendiumArr.append(demon)
        self.defineLevelForUnlockFlags(self.compendiumArr)
    
    '''
    Creates a compendium demon object using the NKMBaseTable buffer and the given demon index
        Parameters:
            NKMBaseTable (Table): the buffer to get the demon data from
            index (Number): The demon's index in the table
            isBoss (Bool): True if the demon is being sent to the player boss array, false otherwise
        Returns:
            The finished Compendium_Demon object
    '''
    def createCompendiumDemon(self, NKMBaseTable, index, isBoss):
        startValue = 0x69
        raceOffset = 0x0C
        demonOffset = 0x1D0
        #First define all relevant offsets
        offset = startValue + demonOffset * index
        locations = {
            'race': offset - raceOffset,
            'alignment': offset - raceOffset + 7,
            'nameID': offset - 0x10,
            'level': offset,
            'HP': offset + 0x1C,
            'firstSkill': offset + 0x70,
            'firstLearnedLevel': offset + 0xA0,
            'fusability': offset + 0x56,
            'unlockFlags': offset + 0x60,
            'tone': offset + 0x58,
            'innate': offset + 0x100,
            'potential': offset + 0X174,
            'encounterSpawn': offset + 0x1AC,
            'descriptionID': offset + 0x3C
        }
        #Then read the list of initial skills learned
        listOfSkills = []
        for i in range(8):
            skillID = NKMBaseTable.readWord(locations['firstSkill'] + 4 * i)
            if skillID != 0:
                listOfSkills.append(Translated_Value(skillID, translation.translateSkillID(skillID, self.skillNames)))
        #Read the list of learnable skills 
        listOfLearnedSkills = []
        for i in range(8):
            #print(locations['firstLearnedLevel'])
            skillID = NKMBaseTable.readWord(locations['firstLearnedLevel'] + 8 * i + 4)
            if skillID != 0:
                listOfLearnedSkills.append(Translated_Value(skillID, translation.translateSkillID(skillID, self.skillNames),
                                                            level=NKMBaseTable.readWord(locations['firstLearnedLevel'] + 8 * i)))
        demon = Compendium_Demon()
        demon.ind = index
        demon.nameID = NKMBaseTable.readWord(locations['nameID'])
        if demon.nameID == 58 and index != 58:
            # Placeholder Jack Frosts
            demon.name = "NOT USED"
        else:
            demon.name = self.enemyNames[demon.ind]
        demon.descriptionID = NKMBaseTable.readWord(locations['descriptionID'] )
        demon.offsetNumbers = locations
        demon.race = Translated_Value(NKMBaseTable.readByte(locations['race']), RACE_ARRAY[NKMBaseTable.readByte(locations['race'])])
        demon.alignment = NKMBaseTable.readByte(locations['alignment'] +1)
        demon.tendency = NKMBaseTable.readByte(locations['alignment'])
        demon.level = Demon_Level(NKMBaseTable.readWord(locations['level']), NKMBaseTable.readWord(locations['level']))
        demon.registerable = NKMBaseTable.readWord(locations['HP'] - 4)
        demon.fusability = NKMBaseTable.readHalfword(locations['fusability'])
        demon.unlockFlags = [NKMBaseTable.readByte(locations['unlockFlags']), NKMBaseTable.readByte(locations['unlockFlags'] + 1)]
        demon.tone = Translated_Value(NKMBaseTable.readByte(locations['tone']), '', secondary=NKMBaseTable.readByte(locations['tone'] + 1))
        demon.resist.physical = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4)))
        demon.resist.fire = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 2),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 2)))
        demon.resist.ice = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 3),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 3)))
        demon.resist.elec = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 4),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 4)))
        demon.resist.force = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 5),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 5)))
        demon.resist.light = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 6),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 6)))
        demon.resist.dark = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 7),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 7)))
        demon.resist.almighty = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 8),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 8)))
        demon.resist.poison = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 9),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 9)))
        demon.resist.confusion = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 11),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 11)))
        demon.resist.charm = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 12),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 12)))
        demon.resist.sleep = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 13),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 13)))
        demon.resist.seal = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 14),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 14)))
        demon.resist.mirage = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 21),
                                                    translation.translateResist(NKMBaseTable.readWord(locations['innate'] + 4 * 21)))
        demon.potential.physical = NKMBaseTable.readWord(locations['potential'])
        demon.potential.fire = NKMBaseTable.readWord(locations['potential'] + 4 * 1)
        demon.potential.ice = NKMBaseTable.readWord(locations['potential'] + 4 * 2)
        demon.potential.elec = NKMBaseTable.readWord(locations['potential'] + 4 * 3)
        demon.potential.force = NKMBaseTable.readWord(locations['potential'] + 4 * 4)
        demon.potential.light = NKMBaseTable.readWord(locations['potential'] + 4 * 5)
        demon.potential.dark = NKMBaseTable.readWord(locations['potential'] + 4 * 6)
        demon.potential.almighty = NKMBaseTable.readWord(locations['potential'] + 4 * 7)
        demon.potential.ailment = NKMBaseTable.readWord(locations['potential'] + 4 * 8)
        demon.potential.recover = NKMBaseTable.readWord(locations['potential'] + 4 * 10)
        demon.potential.support = NKMBaseTable.readWord(locations['potential'] + 4 * 9)
        demonHP = Stat(NKMBaseTable.readWord(locations['HP'] + 4 * 0), NKMBaseTable.readWord(locations['HP'] + 4 * 2), NKMBaseTable.readWord(locations['HP'] + 4 * 0))
        demonMP = Stat(NKMBaseTable.readWord(locations['HP'] + 4 * 1), NKMBaseTable.readWord(locations['HP'] + 4 * 3),  NKMBaseTable.readWord(locations['HP'] + 4 * 1))
        demonStr = Stat(NKMBaseTable.readWord(locations['HP'] + 4 * 4), NKMBaseTable.readWord(locations['HP'] + 4 * 9),  NKMBaseTable.readWord(locations['HP'] + 4 * 4))
        demonVit = Stat(NKMBaseTable.readWord(locations['HP'] + 4 * 5), NKMBaseTable.readWord(locations['HP'] + 4 * 10),  NKMBaseTable.readWord(locations['HP'] + 4 * 5))
        demonMag = Stat(NKMBaseTable.readWord(locations['HP'] + 4 * 6), NKMBaseTable.readWord(locations['HP'] + 4 * 11),  NKMBaseTable.readWord(locations['HP'] + 4 * 6))
        demonAgi = Stat(NKMBaseTable.readWord(locations['HP'] + 4 * 7), NKMBaseTable.readWord(locations['HP'] + 4 * 12),  NKMBaseTable.readWord(locations['HP'] + 4 * 7))
        demonLuk = Stat(NKMBaseTable.readWord(locations['HP'] + 4 * 8), NKMBaseTable.readWord(locations['HP'] + 4 * 13),  NKMBaseTable.readWord(locations['HP'] + 4 * 8))
        demon.stats = Stats(demonHP, demonMP, demonStr, demonVit, demonMag, demonAgi, demonLuk)
        demon.innate = Translated_Value(NKMBaseTable.readWord(locations['innate']),
                                        translation.translateSkillID(NKMBaseTable.readWord(locations['innate']), self.skillNames))
        demon.skills = listOfSkills
        demon.learnedSkills = listOfLearnedSkills
        demon.preventDeletionFlag = NKMBaseTable.readWord(locations['encounterSpawn'] - 8)
        demon.creationSpawn.mapNameID = NKMBaseTable.readWord(locations['encounterSpawn'])
        demon.creationSpawn.zoneNameID = NKMBaseTable.readWord(locations['encounterSpawn'] + 4)
        demon.vengeanceSpawn.mapNameID = NKMBaseTable.readWord(locations['encounterSpawn'] + 8)
        demon.vengeanceSpawn.zoneNameID = NKMBaseTable.readWord(locations['encounterSpawn'] + 12)
        demon.compCostModifier = NKMBaseTable.readWord(locations['firstSkill'] -12)
        return demon
        
    '''
    Fills the arrays skillArr, passiveSkillArr and innateSkillArr with data extracted from the Buffer skillData.
    The end arrays contain data on all skills of their respective type.
        Parameters:
            skillData (Table): the buffer to get the skill data from
    '''
    def fillSkillArrs(self, skillData):
        #Define start locations for batches of skills and how much data each skill has
        startValue = 0x85
        passiveStartValue = 0x132E5
        skillOffset = 0xC4
        passiveOffset = 0x6C
        secondBatchStart = 0x1E305

        #Because the skill table starts with id=1, we need an filler object in the array to keep id & index consistent.
        fillerObject = Active_Skill()
        fillerObject.ind = 0
        fillerObject.name = 'Filler'
        self.skillArr.append(fillerObject)

        #For every skill (there are 950 skills in Vanilla)...
        for index in range(950):
            #check if skill is in passive area 
            if index >= 400 and index < 800:
                offset = passiveStartValue + passiveOffset * (index - 400)
                locations = {
                    'hpIncrease': offset,
                    'survive': offset + 15,
                    'element': offset + 17,
                    'physResist': offset + 34,
                    'effect': offset + 52,
                    'owner': offset - 4,
                }
                #check if innate
                skillType2 = ''
                if index >= 530:
                    skillType2 = 'innate'
                else:
                    skillType2 = 'passive'
                #Create the object to push
                toPush = Passive_Skill()
                toPush.ind = index + 1
                toPush.name = translation.translateSkillID(index + 1, self.skillNames)
                toPush.skillType = skillType2
                toPush.offsetNumber = locations
                
                ownerID = skillData.readWord(locations['owner'])
                if ownerID == -1:
                    ownerName = "Nahobino"
                elif ownerID == -2:
                    ownerName = "Demon Only"
                elif ownerID == -3:
                    ownerName = "Enemy"
                else:
                    ownerName = self.compendiumNames[ownerID]
                toPush.owner = Skill_Owner(ownerID, ownerName)
                
                toPush.hpIncrease = skillData.readByte(locations['hpIncrease'])
                toPush.mpIncrease = skillData.readByte(locations['hpIncrease'] + 1)
                toPush.counterChance = skillData.readByte(locations['hpIncrease'] + 3)
                toPush.survive = skillData.readByte(locations['survive'])
                toPush.element = Translated_Value(skillData.readByte(locations['element']),
                                                  translation.translatePassiveElementType(skillData.readByte(locations['element'])))
                toPush.resists.type = Translated_Value(skillData.readByte(locations['element'] + 1),
                                                       translation.translatePassiveResist(skillData.readByte(locations['element'] + 1)))
                toPush.resists.physical = skillData.readByte(locations['physResist'])
                toPush.resists.fire = skillData.readByte(locations['physResist'] + 1)
                toPush.resists.ice = skillData.readByte(locations['physResist'] + 2)
                toPush.resists.elec = skillData.readByte(locations['physResist'] + 3)
                toPush.resists.force = skillData.readByte(locations['physResist'] + 4)
                toPush.resists.dark = skillData.readByte(locations['physResist'] + 5)
                toPush.resists.light = skillData.readByte(locations['physResist'] + 6)
                toPush.effect1 = skillData.readHalfword(locations['effect'])
                toPush.effect1Amount = skillData.readHalfword(locations['effect'] + 2)
                toPush.effect2 = skillData.readHalfword(locations['effect'] + 4)
                toPush.effect2Amount = skillData.readHalfword(locations['effect'] + 6)
                #If skill is in the innate area push to innateSkillArr else push to passiveSkillArr
                if (index >= 530):
                    self.innateSkillArr.append(toPush)
                else:
                    self.passiveSkillArr.append(toPush)

            else:
                #console.log(index)
                offset = startValue + skillOffset * index
                #Skill ID is now read from the data
                #skillID = index + 1
                if (index < 800):
                    skillID = skillData.readDblword(offset)

                #if skill is in the second batch of active skills, we calculate the offset directly
                if (index >= 800):
                    skillName = translation.translateSkillID(index , self.skillNames)
                    offset = secondBatchStart + skillOffset * (index  - 800)
                    skillID = skillData.readDblword(offset)
                skillName = translation.translateSkillID(skillID, self.skillNames)
                locations = {
                    'cost': offset + 8,
                    'skillType': offset + 10,
                    'element': offset + 12,
                    'owner': offset +  24,
                    'icon': offset + 28,
                    'target': offset + 0x22,
                    'minHit': offset + 0x24,
                    'maxHit': offset + 0x25,
                    'critRate': offset + 0x26,
                    'power': offset + 0x28,
                    'hitRate': offset + 0x34,
                    'ailmentFlag': offset + 0x35,
                    'ailmentChance': offset + 0x48,
                    'healing': {
                        'overMaxHP': offset + 0x45,
                        'effect': offset + 0x49
                    },
                    'pierce': offset + 0x46,
                    'buffstimer': offset + 75,
                    'resistEnable': offset + 0x60,
                    'hpDrain': offset + 109,
                    'magatsuhiFlag': offset + 115,
                    'modifier1': offset + 136,
                    'condition1': offset + 140,
                    'animation': offset - 0x20
                }
                toPush = Active_Skill()
                toPush.ind = skillID
                toPush.name = skillName
                toPush.offsetNumber = locations

                ownerID = skillData.readWord(locations['owner'])
                if ownerID == -1:
                    ownerName = "Nahobino"
                elif ownerID == -2:
                    ownerName = "Demon Only"
                elif ownerID == -3:
                    ownerName = "Enemy"
                else:
                    ownerName = self.compendiumNames[ownerID]
                toPush.owner = Skill_Owner(ownerID, ownerName)

                toPush.cost = skillData.readHalfword(locations['cost'])
                toPush.rank = skillData.readByte(locations['hpDrain'] + 3)
                toPush.skillType = Translated_Value(skillData.readByte(locations['skillType']),
                                                  translation.translateSkillType(skillData.readByte(locations['skillType'])))
                toPush.potentialType = Translated_Value(skillData.readByte(locations['icon'] + 1),
                                                        translation.translatePotentialType(skillData.readByte(locations['icon'] + 1)))
                toPush.element = Translated_Value(skillData.readByte(locations['element']),
                                                  translation.translateSkillElement(skillData.readByte(locations['element'])))
                toPush.skillIcon = skillData.readByte(locations['icon'])
                toPush.target = Translated_Value(skillData.readByte(locations['target']),
                                                 translation.translateTarget(skillData.readByte(locations['target'])))
                toPush.minHits = skillData.readByte(locations['minHit'])
                toPush.maxHits = skillData.readByte(locations['maxHit'])
                toPush.crit = skillData.readByte(locations['critRate'])
                toPush.power = skillData.readWord(locations['power'])
                toPush.hit = skillData.readByte(locations['hitRate'])
                toPush.ailmentFlags.instakill = skillData.readByte(locations['ailmentFlag'])
                toPush.ailmentFlags.poison = skillData.readByte(locations['ailmentFlag'] + 1)
                toPush.ailmentFlags.confusion = skillData.readByte(locations['ailmentFlag'] + 3)
                toPush.ailmentFlags.charm = skillData.readByte(locations['ailmentFlag'] + 4)
                toPush.ailmentFlags.sleep = skillData.readByte(locations['ailmentFlag'] + 5)
                toPush.ailmentFlags.seal = skillData.readByte(locations['ailmentFlag'] + 6)
                toPush.ailmentFlags.mirage = skillData.readByte(locations['ailmentFlag'] + 9)
                toPush.ailmentFlags.mud = skillData.readByte(locations['ailmentFlag'] + 14)
                toPush.ailmentFlags.shroud = skillData.readByte(locations['ailmentFlag'] + 15)
                toPush.healing.overMaxHP = skillData.readByte(locations['healing']['overMaxHP'])
                toPush.healing.effect = skillData.readByte(locations['healing']['effect'])
                toPush.healing.flag = skillData.readWord(locations['resistEnable'] + 8)
                toPush.healing.percent = skillData.readByte(locations['resistEnable'] + 12)
                toPush.pierce = skillData.readByte(locations['pierce'])
                toPush.ailmentChance = skillData.readByte(locations['ailmentChance'])
                toPush.buff.timer = skillData.readByte(locations['buffstimer'])
                toPush.buff.physical = skillData.readWord(locations['buffstimer'] + 1)
                toPush.buff.magical = skillData.readWord(locations['buffstimer'] + 5)
                toPush.buff.defense = skillData.readWord(locations['buffstimer'] + 9)
                toPush.buff.accEva = skillData.readWord(locations['buffstimer'] + 13)
                toPush.resists.enable = skillData.readByte(locations['resistEnable'])
                toPush.resists.physical = Translated_Value(skillData.readByte(locations['resistEnable'] + 1),
                        translation.translatePassiveResist(skillData.readByte(locations['resistEnable'] + 1)))
                toPush.resists.fire = Translated_Value(skillData.readByte(locations['resistEnable'] + 2),
                        translation.translatePassiveResist(skillData.readByte(locations['resistEnable'] + 2)))
                toPush.resists.ice = Translated_Value(skillData.readByte(locations['resistEnable'] + 3),
                        translation.translatePassiveResist(skillData.readByte(locations['resistEnable'] + 3)))
                toPush.resists.elec = Translated_Value(skillData.readByte(locations['resistEnable'] + 4),
                        translation.translatePassiveResist(skillData.readByte(locations['resistEnable'] + 4)))
                toPush.resists.force = Translated_Value(skillData.readByte(locations['resistEnable'] + 5),
                        translation.translatePassiveResist(skillData.readByte(locations['resistEnable'] + 5)))
                toPush.resists.light = Translated_Value(skillData.readByte(locations['resistEnable'] + 6),
                        translation.translatePassiveResist(skillData.readByte(locations['resistEnable'] + 6)))
                toPush.resists.dark = Translated_Value(skillData.readByte(locations['resistEnable'] + 7),
                        translation.translatePassiveResist(skillData.readByte(locations['resistEnable'] + 7)))
                toPush.hpDrain = skillData.readByte(locations['hpDrain']),
                toPush.mpDrain = skillData.readByte(locations['hpDrain'] + 1)
                toPush.magatsuhi.enable = skillData.readByte(locations['magatsuhiFlag'])
                toPush.magatsuhi.race1 = Translated_Value(skillData.readWord(locations['magatsuhiFlag'] + 1),
                        RACE_ARRAY[skillData.readByte(locations['magatsuhiFlag'] + 1)])
                toPush.magatsuhi.race2 = Translated_Value(skillData.readWord(locations['magatsuhiFlag'] + 5),
                        RACE_ARRAY[skillData.readByte(locations['magatsuhiFlag'] + 3)])
                toPush.modifiers.modifier1 = Translated_Value(skillData.readByte(locations['modifier1']),
                        translation.translateModifier(skillData.readByte(locations['modifier1'])))
                toPush.modifiers.modifier2 = Translated_Value(skillData.readByte(locations['modifier1'] + 1),
                        translation.translateModifier(skillData.readByte(locations['modifier1'] + 1)))
                toPush.modifiers.modifier3 = Translated_Value(skillData.readByte(locations['modifier1'] + 2),
                        translation.translateModifier(skillData.readByte(locations['modifier1'] + 2)))
                toPush.modifiers.modifier4 = Translated_Value(skillData.readByte(locations['modifier1'] + 3),
                        translation.translateModifier(skillData.readByte(locations['modifier1'] + 3)))
                condition1 = Skill_Condition()
                condition1.value = skillData.readByte(locations['condition1'])
                condition1.ailmentCondition = skillData.readByte(locations['condition1'] + 1)
                condition1.effect = skillData.readHalfword(locations['condition1'] + 2)
                condition1.amount = skillData.readHalfword(locations['condition1'] + 4)
                condition2 = Skill_Condition()
                condition2.value = skillData.readByte(locations['condition1'] + 8)
                condition2.ailmentCondition = skillData.readByte(locations['condition1'] + 9)
                condition2.effect = skillData.readHalfword(locations['condition1'] + 11)
                condition2.amount = skillData.readHalfword(locations['condition1'] + 13)
                toPush.conditions = Skill_Conditions(condition1, condition2)
                toPush.animation = skillData.read32chars(locations['animation'])
                self.skillArr.append(toPush)
                
    '''
    Fills the array normalFusionArr with data extracted from the Buffer fusionData.
    The end array contains data on all normal fusions between two registerable demons.
        Parameters:
            fusionData (Table): the buffer to get the fusion data from
    '''
    def fillNormalFusionArr(self, fusionData):
        #Define Starting point and difference to next fsion
        startValue = 0xC5
        fusionOffset = 0x7C

        #For every fusion (37401 = ((n-1)*(n))/2 with n being the number of fusable(excludes Tao/Yoko for example) registerable demons)
        for index in range(38226):
            offset = startValue + index * fusionOffset
            locations = {
                'firstDemon': offset,
                'secondDemon': offset + 0x1D,
                'result': offset + 0x57
            }
            firstDemon = Translated_Value(fusionData.readWord(locations['firstDemon']),
                self.compendiumArr[fusionData.readWord(locations['firstDemon'])].name)
            secondDemon = Translated_Value(fusionData.readWord(locations['secondDemon']),
                self.compendiumArr[fusionData.readWord(locations['secondDemon'])].name)
            result = Translated_Value(fusionData.readWord(locations['result']),
                self.compendiumArr[fusionData.readWord(locations['result'])].name)
            self.normalFusionArr.append(Normal_Fusion(locations, firstDemon, secondDemon, result))
            
    '''
    Fills the array fusionChartArray with data extracted from the Buffer fusionData.
    The end array contains data on what the normal result of a fusion between two races should be.
        Parameters:
            fusionData (Table): the buffer to get the fusion chart data from
    '''
    def fillFusionChart(self, fusionData):

        startValue = 0x95

        for index in range(609):
            offset = startValue + index * 4
            race1 = Translated_Value(fusionData.readByte(offset), RACE_ARRAY[fusionData.readByte(offset)])
            race2 = Translated_Value(fusionData.readByte(offset + 1), RACE_ARRAY[fusionData.readByte(offset + 1)])
            result = Translated_Value(fusionData.readByte(offset + 2), RACE_ARRAY[fusionData.readByte(offset + 2)])
            self.fusionChartArr.append(Fusion_Chart_Node(offset, race1, race2, result))
            #print(race1.translation + " + " + race2.translation + " = " + result.translation)
            
    '''
    Fills the array fusionChartArray with data extracted from the Buffer fusionData.
    The end array contains data on the results and ingredients of all special fusions
        Parameters:
            fusionData (Table): the buffer to get the special fusion data from
    '''
    def fillSpecialFusionArr(self, fusionData):

        startValue = 0xCC5
        fusionOffset = 0xC

        for index in range(62):
            offset = startValue + index * fusionOffset
            fusion = Special_Fusion()
            fusion.ind = fusionData.readHalfword(offset)
            fusion.resultLevel = self.compendiumArr[fusionData.readHalfword(offset + 10)].level.original
            fusion.baseOffset = offset
            fusion.demon1 = Translated_Value(fusionData.readHalfword(offset + 2), self.compendiumArr[fusionData.readHalfword(offset + 2)].name)
            fusion.demon2 = Translated_Value(fusionData.readHalfword(offset + 4), self.compendiumArr[fusionData.readHalfword(offset + 4)].name)
            fusion.demon3 = Translated_Value(fusionData.readHalfword(offset + 6), self.compendiumArr[fusionData.readHalfword(offset + 6)].name)
            fusion.demon4 = Translated_Value(fusionData.readHalfword(offset + 8), self.compendiumArr[fusionData.readHalfword(offset + 8)].name)
            fusion.result = Translated_Value(fusionData.readHalfword(offset + 10), self.compendiumArr[fusionData.readHalfword(offset + 10)].name)
            self.specialFusionDemonIDs.append(fusion.result.value)
            self.specialFusionArr.append(fusion)
            
    '''
    Fills the Array enemyArr with data for all basic enemy versions of playable demons.
        Parameters:
            enemyData (Table): the buffer to get the enemy data from 
    '''
    def fillBasicEnemyArr(self, enemyData):
        #For all Enemy version of playable demon indeces
        for index in range(numbers.NORMAL_ENEMY_COUNT):
            demon = self.createEnemyDemon(enemyData, index)
            self.enemyArr.append(demon)
            
    '''
    Creates an enemy demon object using the enemyData buffer and the given demon index
        Parameters:
            enemyData (Table): the buffer to get the demon data from
            index (Number): The demon's index in the table
        Returns:
            The finished Enemy_Demon object
    '''
    def createEnemyDemon(self, enemyData, index):
        #First define all relevant offsets
        startValue = 0x88139
        enemyOffset = 0x170
        offset = startValue + enemyOffset * index
        locations = {
            'level': offset,
            'nameID': 0x69 + 0x1D0 * index - 0x10,
            'HP': offset + 4,
            'pressTurns': offset + 0x2B,
            'experience': offset + 0x44,
            'item': offset + 0x64,
            'firstSkill': offset + 0x88,
            'innate': offset + 0xB8,
            'resist': offset + 0xBB,
            'potential': offset + 0x12C
        }
        
        listOfSkills = []
        for i in range(8):
            skillID = enemyData.readWord(locations['firstSkill'] + 4 * i)
            if skillID != 0:
                listOfSkills.append(Translated_Value(skillID, translation.translateSkillID(skillID, self.skillNames)))       
        demon = Enemy_Demon()
        demon.ind = index
        demon.nameID = enemyData.readWord(locations['nameID'])
        if demon.nameID == 58 and (index != 58 and index!= 941):
            # Placeholder Jack Frosts
            demon.name = "NOT USED"
        else:
            demon.name = self.enemyNames[demon.nameID]
        demon.offsetNumbers = locations
        demon.level = enemyData.readWord(locations['level'])
        demon.stats = Stats(enemyData.readWord(locations['HP']), enemyData.readWord(locations['HP'] + 4), enemyData.readWord(locations['HP'] + 8),
                                enemyData.readWord(locations['HP'] + 12), enemyData.readWord(locations['HP'] + 16),
                                enemyData.readWord(locations['HP'] + 20), enemyData.readWord(locations['HP'] + 24)) #HP, MP, str, vit, mag, agi, luk
        demon.analyze = enemyData.readByte(locations['HP'] + 28)
        demon.levelDMGCorrection = enemyData.readByte(locations['HP'] + 30)
        demon.AI = enemyData.readWord(locations['experience'] + 12) #55 for normal encounters
        demon.recruitable = enemyData.readByte(locations['HP'] + 33)
        demon.pressTurns = enemyData.readByte(locations['pressTurns'])
        demon.damageMultiplier = enemyData.readWord(locations['pressTurns'] + 9)
        demon.experience = enemyData.readWord(locations['experience'])
        demon.money = enemyData.readWord(locations['experience'] + 4)
        demon.skills = listOfSkills
        demon.instakillRate = enemyData.readByte(locations['item'] - 1)
        itemDrop1 = Item_Drop(enemyData.readWord(locations['item']), translation.translateItem(enemyData.readWord(locations['item']),self.itemNames),
                                                    enemyData.readWord(locations['item'] + 4), enemyData.readWord(locations['item'] + 8))
        itemDrop3 = Item_Drop(enemyData.readWord(locations['item'] + 12), translation.translateItem(enemyData.readWord(locations['item'] + 12),self.itemNames),
                                                    enemyData.readWord(locations['item'] + 16), enemyData.readWord(locations['item'] + 20))
        itemDrop2 = Item_Drop(enemyData.readWord(locations['item'] + 24), translation.translateItem(enemyData.readWord(locations['item'] + 24),self.itemNames),
                                                    enemyData.readWord(locations['item'] + 28), enemyData.readWord(locations['item'] + 32))
        demon.drops = Item_Drops(itemDrop1, itemDrop2, itemDrop3)
        demon.innate = Translated_Value(enemyData.readWord(locations['innate']), self.obtainSkillFromID(enemyData.readWord(locations['innate'])).name)
        demon.resist.physical = Translated_Value(enemyData.readWord(locations['innate'] + 4),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4)))
        demon.resist.fire = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 2),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 2)))
        demon.resist.ice = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 3),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 3)))
        demon.resist.elec = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 4),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 4)))
        demon.resist.force = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 5),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 5)))
        demon.resist.light = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 6),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 6)))
        demon.resist.dark = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 7),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 7)))
        demon.resist.almighty = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 8),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 8)))
        demon.resist.poison = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 9),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 9)))
        demon.resist.confusion = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 11),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 11)))
        demon.resist.charm = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 12),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 12)))
        demon.resist.sleep = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 13),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 13)))
        demon.resist.seal = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 14),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 14)))
        demon.resist.mirage = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 21),
                                                    translation.translateResist(enemyData.readWord(locations['innate'] + 4 * 21)))
        demon.potential.physical = enemyData.readWord(locations['potential'])
        demon.potential.fire = enemyData.readWord(locations['potential'] + 4 * 1)
        demon.potential.ice = enemyData.readWord(locations['potential'] + 4 * 2)
        demon.potential.elec = enemyData.readWord(locations['potential'] + 4 * 3)
        demon.potential.force = enemyData.readWord(locations['potential'] + 4 * 4)
        demon.potential.light = enemyData.readWord(locations['potential'] + 4 * 5)
        demon.potential.dark = enemyData.readWord(locations['potential'] + 4 * 6)
        demon.potential.almighty = enemyData.readWord(locations['potential'] + 4 * 7)
        demon.potential.ailment = enemyData.readWord(locations['potential'] + 4 * 8)
        demon.potential.recover = enemyData.readWord(locations['potential'] + 4 * 10)
        demon.potential.support = enemyData.readWord(locations['potential'] + 4 * 9)
        return demon
            
    '''
    Fills the array playerBossArr with data extracted from the Buffer NKMBaseTable.
    The end array contains data on the playable data of all demons who are normally enemy only.
        Parameters:
            NKMBaseTable (Table): the buffer to get the demon data from
    '''
    def fillPlayerBossArr(self, NKMBaseTable):
        for index in range(numbers.NORMAL_ENEMY_COUNT): #Dummy data for playable demons to match id's better
            self.playerBossArr.append(Compendium_Demon())
        #For all demons in the compendium...
        for index in range(numbers.NORMAL_ENEMY_COUNT, 1200):
            demon = self.createCompendiumDemon(NKMBaseTable, index, True)
            #Add read demon data to compendium
            self.playerBossArr.append(demon)

    '''
    Fills the Array bossArr with data for all special enemy demons.
        Parameters:
            enemyData (Table): the buffer to get the enemy data from 
    '''
    def fillBossArr(self, enemyData):
        for index in range(numbers.NORMAL_ENEMY_COUNT): #Dummy data for playable demons to match id's better
            self.bossArr.append(Enemy_Demon())
            self.staticBossArr.append(Enemy_Demon())
        #For all Enemy version of playable demon indeces
        for index in range(numbers.NORMAL_ENEMY_COUNT, 1200):
            demon = self.createEnemyDemon(enemyData, index)
            self.bossArr.append(demon)
            self.staticBossArr.append(copy.deepcopy(demon))
            
    '''
    Fills the erray encountSymbolArr with information regarding the encouners on the overworld you can run into, called symbols.
        Parameters:
            encounters (Table): buffer containing encounter data
    '''
    def fillEncountSymbolArr(self, encounters):

        start = 0x55
        size = 0x64

        #The tables standard size for symbols is 2081
        for index in range(2082):
            offset = start + size * index

            locations = {
                'flags': offset,
                'symbol': offset + 4,
                'encounter1': offset + 0x24,
                'encounter1Chance': offset + 0x26
            }

            #each symbol has 16 encounters with different chances attached
            possEnc = []
            for i in range(16):
                possEnc.append(encounters.readHalfword(locations['encounter1'] + 4 * i))
                
                #possEnc.append(Possible_Encounter(encId, self.encountArr[encId], encounters.readHalfword(locations['encounter1Chance'] + 4 * i)))

            ind = encounters.readHalfword(locations['symbol'])
            translation = "NO BASIC ENEMY" #Since non base demons arent saved anywhere currently use this filler name
            if (ind < len(self.compendiumArr)):
                translation = self.compendiumArr[encounters.readHalfword(locations['symbol'])].name
            symbol = Translated_Value(ind, translation)
            self.encountSymbolArr.append(Encounter_Symbol(
                index, symbol, locations, encounters.readWord(locations['flags']), possEnc
                ))

    '''
    Fills the array encountArr with data on all encounter battles.
        Parameters:
            encounters (Table): buffer containing encounter data
    '''
    def fillEncountArr(self, encounters):

        start = 0x32DB5
        size = 0x1C

        #Table in EncountData is of this size
        for index in range(3001):
            offset = start + size * index
            locations = {
                'flags': offset,
                'track': offset + 1,
                'demon': offset + 4
            }
            track = encounters.readByte(locations['track'])
            demons = [encounters.readHalfword(offset + 4), encounters.readHalfword(offset + 6), encounters.readHalfword(offset + 8),
                      encounters.readHalfword(offset + 10), encounters.readHalfword(offset + 12), encounters.readHalfword(offset + 14)]
            self.encountArr.append(Encounter(index, locations, encounters.readHalfword(offset), track, demons))
            
    '''
    Fills the nahobino object with data from the playerGrow file.
        Parameters:
            playerGrow (Table): table containing data on the main character
    '''
    def fillNahobino(self, playGrow):

        start = 0x1685
        size = 0x1C
        locations = {
            'startingSkill': 0x2C69,
            'statStart': start,
            'affStart': 0x2B15,
            'innate': 0x2D05
        }

        #Table in PlayerGrow is defined for level 0 until level 150
        for index in range(151):
            offset = start + size * index
            self.nahobino.stats.append(LevelStats(index,playGrow.readWord(offset + 4 * 0),playGrow.readWord(offset + 4 * 1),playGrow.readWord(offset + 4 * 2),playGrow.readWord(offset + 4 * 3),playGrow.readWord(offset + 4 * 4),playGrow.readWord(offset + 4 * 5),playGrow.readWord(offset + 4 * 6)))
        
        self.nahobino.offsetNumbers = locations
        
        self.nahobino.startingSkill = playGrow.readWord(locations['startingSkill'])
        self.nahobino.innate = playGrow.readWord(locations['innate'])

        self.nahobino.resist.physical = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 0),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 * 0)))
        self.nahobino.resist.fire = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 1),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *1)))
        self.nahobino.resist.ice = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 2),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *2)))
        self.nahobino.resist.elec = Translated_Value(playGrow.readWord(locations['affStart'] + 4 *3),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *3)))
        self.nahobino.resist.force = Translated_Value(playGrow.readWord(locations['affStart'] + 4 *4),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *4)))
        self.nahobino.resist.light = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 5),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *5)))
        self.nahobino.resist.dark = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 6),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *6)))
        self.nahobino.resist.almighty = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 7),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *7)))
        self.nahobino.resist.poison = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 8),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *8)))
        self.nahobino.resist.confusion = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 10),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *10)))
        self.nahobino.resist.charm = Translated_Value(playGrow.readWord(locations['affStart'] + 4  * 11),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *11)))
        self.nahobino.resist.sleep = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 12),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *12)))
        self.nahobino.resist.seal = Translated_Value(playGrow.readWord(locations['affStart'] + 4 * 13),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *13)))
        self.nahobino.resist.mirage = Translated_Value(playGrow.readWord(locations['affStart'] + 4  *20),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 * 20)))


    '''
    Fills the array essenceArr with data on all essence items.
        Parameters:
            items (Buffer) the buffer containing data on all items
    '''
    def fillEssenceArr(self,items):
        
        start = 0x6E59
        size = 0x18

        # ID of first essence is 311, last essence is 615
        for index in range(304):
            offset = start + size * index
            essence = Essence()
            essence.demon = Translated_Value(items.readWord(offset),self.getDemonsCurrentNameByID(items.readWord(offset)))
            essence.price = items.readWord(offset +12)
            essence.offset = offset
            essence.ind = 311 + index
            essence.name = self.itemNames[311 + index]
            
            self.essenceArr.append(essence)

    '''
    Fills the array shopArr with data on all buyable items.
        Parameters:
            shopData (Buffer) the buffer containing all shop data
    '''
    def fillShopArr(self, shopData):
        start = 0x55
        size = 16

        for index in range(116):
            offset = start + size * index
            entry = Shop_Entry()
            entry.offset = offset
            entry.item = Translated_Value(shopData.readHalfword(offset),translation.translateItem(shopData.readHalfword(offset),self.itemNames))
            entry.unlock = Translated_Value(shopData.readDblword(offset +4), translation.translateShopFlag(shopData.readDblword(offset+4)))

            self.shopArr.append(entry)
    '''
    Fills the array mimanRewardsArr with data on all buyable items.
        Parameters:
            shopData (Buffer) the buffer containing all shop data
    '''
    def fillMimanRewardArr(self, shopData):
        start = 0x7A5
        size = 72

        for index in range(40):
            offset = start + size * index
            entry = Miman_Reward()
            entry.offset = offset
            entry.miman = shopData.readWord(offset)
            entry.setMsgID = 0#To remove Set Names (to get set names: shopData.readWord(offset +4)
            for i in range(16):
                item = Reward_Item(shopData.readHalfword(offset + 8 + 4*i),shopData.readHalfword(offset + 10+4*i))
                entry.items.append(item)
            self.mimanRewardsArr.append(entry)
    
    def fillVendingMachineArr(self, buffer):
        start = 0x55
        size = 24

        for index in range(124):
            offset = start + size * index
            entry = Vending_Machine()
            entry.offset = offset

            entry.area = buffer.readHalfword(offset)
            entry.ind = index
            entry.relicID = buffer.readHalfword(offset +2)

            for i in range(3):
                item = Vending_Machine_Item()
                item.ind = buffer.readHalfword(offset +8 + i * 4)
                item.amount = buffer.readByte(offset +8 + 2 + i*4)
                item.rate = buffer.readByte(offset +8 + 3 + i * 4)
                item.name = self.itemNames[item.ind]
                entry.items.append(item)
            self.vendingMachineArr.append(entry)



    
    '''
    Fills the array eventEncountArr with data on all event (boss) encounters.
        Parameters:
            data (Buffer) the buffer containing all event encounter data
    '''
    def fillEventEncountArr(self, data):
        start = 0x45
        size = 0x60
        #encounterDebugData = []
        demonDict = {}
        for index in range(253):
            offset = start + size * index
            encounter = Event_Encounter()
            encounter.ind = data.readByte(offset + 0x20)
            encounter.nextEnc =  data.readByte(offset + 0x21)
            encounter.levelpath = data.read32chars(offset)
            encounter.offsets = {
                'demons': offset + 0x48,
                'track': offset + 0x2E,
                'levelpath': offset,
                'unknownDemon': offset + 0x38,
                '23Flag': offset + 0x23,
                'battlefield': offset + 0x24,
                'startingPhase': offset + 0x30,
            }
            encounter.unknown23Flag = data.readByte(offset + 0x23)
            encounter.battlefield = data.readByte(offset + 0x24)
            encounter.track = data.readHalfword(offset + 0x2E)
            encounter.unknownDemon = Translated_Value(data.readHalfword(offset + 0x38),self.enemyNames[data.readHalfword(offset + 0x38)])
            encounter.endEarlyFlag = data.readByte(offset + 0x3A)
            demons = []
            for number in range(8):
                demons.append(Translated_Value(data.readHalfword(offset + 0x48 + 2 * number),self.enemyNames[data.readHalfword(offset + 0x48 + 2 * number)]))

            encounter.demons = demons
            encounter.startingPhase = data.readByte(offset + 0x30)
            encounter.originalIndex = index
            #Check if encounter is a duplicate and store that information in bossDuplicateMap if so
            originalIndex = next((x for x, val in enumerate(self.eventEncountArr) if val.compareDemons(encounter)), -1)
            if originalIndex > -1:
                self.bossDuplicateMap[index] = originalIndex
                #print("Duplicate " + str(index) +" to " +str(originalIndex))

            self.eventEncountArr.append(encounter)
            self.staticEventEncountArr.append(copy.deepcopy(encounter))
            #print(str(index) + ": (" + str(demons[0].value) + ") " + self.enemyNames[demons[0].value] + " " + str(encounter.track) + " NEXT: " + str(encounter.nextEnc))
        
    '''
    Fills the array bossFlagArr with data on boss flags.
        Parameters:
            data (Buffer) the buffer containing all boss flag data
    '''
    def fillBossFlagArr(self, data):
        start = 0x45
        size = 0x24
        
        for index in range(134):
            offset = start + size * index
            bossFlags = Boss_Flags()
            bossFlags.offset = offset
            bossFlags.demonID = data.readHalfword(offset)
            flags = []
            for i in range(6):
                flags.append(data.readByte(offset + 4 * (i + 1)))
            bossFlags.flags = flags
            self.bossFlagArr.append(bossFlags)

    '''
    Fills the array missionArr with data on all missions.
        Parameters:
            data (Buffer) the buffer containing all mission data
    '''
    def fillMissionArr(self, data):

        df = pd.read_csv(paths.MISSION_REWARDS_CSV)
        missionNames = {}
        for index, row in df.iterrows():
            missionNames[row['ID']] = row['Name']

        start = 0x45
        entrySize = 372

        for index in range(224):
            offset = start + entrySize * index

            locations = {
                'ind': offset,
                'rewardID': offset +8,
                'rewardAmount': offset +10,
                'rewardMacca': offset + 24,
                'conditions': offset + 0x20
            }

            mission = Mission()
            mission.offsets = locations
            mission.ind = data.readHalfword(locations['ind'])
            mission.reward.amount = data.readHalfword(locations['rewardAmount'])
            mission.reward.ind = data.readHalfword(locations['rewardID'])
            mission.macca = data.readWord(locations['rewardMacca'])
            mission.experience = data.readWord(locations['rewardMacca'] + 4)
            mission.name =missionNames[mission.ind]
            if mission.name == "nan" or mission.name == "":
                mission.name = "Name missing " + str(mission.ind)
            
            for i in range(4):
                cType = data.readWord(locations['conditions'] + 0x10 * i)
                cID = data.readWord(locations['conditions'] + 0x10 * i + 4)
                cAmount = data.readWord(locations['conditions'] + 0x10 * i + 8)
                mission.conditions.append(Mission_Condition(cType, cID, cAmount))
            self.missionArr.append(mission)



    '''
    Fills the array battleEventArr with data on all battle events and in which encounters they occur.
        Parameters:
            data (Buffer) the buffer containing all battle event tabke data
    '''
    def fillBattleEventArr(self, data):

        start = 0x45
        size = 0x50

        for index in range(36):
            offset = start + size * index
            eventIndex = data.readByte(offset + 0x20)

            event = Battle_Event(eventIndex, offset)
            self.battleEventArr.append(event)

    '''
    Fills the array devilAssetArr with data on what assets are used by which demon.
        Parameters:
            data (Buffer) the buffer containing all demon asset table data
    '''
    def fillDevilAssetArr(self, data):

        start = 0x4E
        size = 0x1D2

        for index in range(1200):
            offset = start + size * index

            locations =  {
                'demon': offset,
                'classAssetID': offset + 0x1D,
                'DMAssetID': offset + 0x67,
                'validArea': offset + 0xBD,
                'verticalMax': offset + 0xDA,
                'horizontalMax': offset + 0xF7,
                'tallMax': offset + 0x114,
                'postChip': offset + 0x13D
            }

            entry = Asset_Entry()
            entry.demonID = data.readWord(offset)
            entry.classAssetID = data.readWord(locations['classAssetID'])
            entry.dmAssetID = data.readWord(locations['DMAssetID'])
            entry.validArea = data.readWord(locations['validArea'])
            entry.verticalMax = data.readWord(locations['verticalMax'])
            entry.horizontalMax = data.readWord(locations['horizontalMax'])
            entry.tallMax = data.readWord(locations['tallMax'])

            postChips = []
            for i in range(25):
                postChips.append(data.readWord(locations['postChip'] + i * 4))
            entry.postChips = postChips
            entry.locations = locations


            self.devilAssetArr.append(entry)
            
    '''
    Fills the array abscessArr with data on abscess encounters and miracles.
        Parameters:
            data (Buffer) the buffer containing all abcess data
    '''
    def fillAbscessArr(self, data):

        start = 0x45
        size = 0x20

        for index in range(83):
            offset = start + size * index

            locations =  {
                'encounter': offset + 0xc,
                'eventEncounter': offset + 0xe,
                'miracles': offset + 0x14
            }

            abscess = Abscess()
            abscess.offsetNumber = locations
            abscess.encounter = data.readHalfword(locations['encounter'])
            abscess.eventEncounter = data.readByte(locations['eventEncounter'])

            miracles = []
            for i in range(6):
                miracles.append(data.readByte(locations['miracles'] + i))
            abscess.miracles = miracles
            #if abscess.encounter > 0 and len(abscess.miracles) > 0:
            #    demons = self.encountArr[abscess.encounter].demons
            #    print(demons)

            self.abscessArr.append(abscess)

    '''
    Fills the array devilUIArr with data on the demons ui elements, like their face in the status menu.
        Parameters:
            data (Buffer) the buffer containing all data on which ui elements demons use
    '''
    def fillDevilUIArr(self, data):
        start = 0x45
        size = 44

        for index in range(numbers.TOTAL_DEMON_COUNT):
            offset = start + size * index

            locations = {
                'assetID': offset,
                'assetString': offset + 4,
            }

            entry = UI_Entry()
            entry.assetID = data.readWord(locations['assetID'])
            entry.assetString = data.read32chars(locations['assetString'])
            entry.offsetNumber = locations

            self.devilUIArr.append(entry)

    '''
    Fills the array mapSymbolArr with data on field demons including their speed and size
        Parameters:
            data (Buffer) the buffer containing all map demon data
    '''
    def fillMapSymbolArr(self, data):

        startingBytes = bytearray(bytes.fromhex('17000000000000003100000000000000'))
        last = 0
        while data.buffer.find(startingBytes,last) != -1:
            offset = data.buffer.find(startingBytes,last) +25
            last = data.buffer.find(startingBytes,last) +100
            locations = {
                'demonID': offset,
                'walkSpeed': offset + 0x1d,
                'scaleFactor': offset + 0x74,
                'encountCollisionX': offset + 0x91,
                'encountCollisionY': offset + 0xAE,
                'encountCollisionZ': offset + 0xCB,

            }
            demonID = data.readWord(offset)
            walkSpeed = data.readFloat(locations['walkSpeed'])
            scaleFactor = data.readFloat(locations['scaleFactor'])
            encountCollision = Position( data.readFloat(locations['encountCollisionX']),data.readFloat(locations['encountCollisionY']),data.readFloat(locations['encountCollisionZ']))
            
            mapDemon = Map_Demon()
            mapDemon.offsetNumbers = locations
            mapDemon.demonID = demonID
            mapDemon.walkSpeed = walkSpeed
            mapDemon.scaleFactor = scaleFactor
            mapDemon.encountCollision = encountCollision
            self.mapSymbolArr.append(mapDemon)
            
    '''
    Fills the array talkCameraOffsets with data regarding camera in the status menu in battle for all demons
        Parameters:
            data (Buffer) the buffer containing all data regarding camera in the status menu in battle for all demons
    '''
    def fillTalkCameraArr(self, data):
        start = 0x4E
        size = 0x132

        for index in range(numbers.TOTAL_DEMON_COUNT):
            offset = start + size * index

            locations = {
                'demonID': offset,
                'eyeOffset': offset + 29,
                'lookOffset': offset + 29 * 4,
                'dyingOffset': offset + 29 * 7
            }

            entry = Talk_Camera_Offset_Entry()
            entry.offsetNumber = locations
            entry.demonID = index
            entry.eyeOffset = Position(data.readFloat(locations['eyeOffset']),data.readFloat(locations['eyeOffset'] + 29), data.readFloat(locations['eyeOffset'] + 29 * 2))
            entry.lookOffset = Position(data.readFloat(locations['lookOffset']),data.readFloat(locations['lookOffset'] + 29), data.readFloat(locations['lookOffset'] + 29 * 2))
            entry.dyingOffset = Position(data.readFloat(locations['dyingOffset']),data.readFloat(locations['dyingOffset'] + 29), data.readFloat(locations['dyingOffset'] + 29 * 2))
            
            self.talkCameraOffsets.append(entry)

    '''
    Fills the array miracleArr with data on miracle prices.
        Parameters:
            data (Buffer) the buffer containing all miracle data
    '''
    def fillMiracleArr(self, data):

        start = 0x59
        size = 0x14
        
        self.miracleArr.append(Miracle(0, 0, 0)) #Dummy miracle to better align with abscess indexing

        for index in range(144):
            offset = start + size * index
            miracle = Miracle(offset, data.readHalfword(offset + 0xc), data.readByte(offset + 0x4))
            self.miracleArr.append(miracle)
            
    '''
    Fills the erray uniqueSymbolArr with information regarding unique encounters on the overworld like mitamas and punishing foes, called symbols.
        Parameters:
            encounters (Table): buffer containing unique symbol encounter data
    '''
    def fillUniqueSymbolArr(self, uniqueSymbols):

        start = 0x5d
        size = 0x18
        #The tables standard size for symbols is 2081
        for index in range(57):
            offset = start + size * index

            locations = {
                'id': offset,
                'encounterID': offset + 2,
                'eventEncounterID': offset + 4,
                'symbol': offset + 6
            }
            

            uniqueSymbol = Unique_Symbol_Encounter()
            uniqueSymbol.offsetNumber = locations
            uniqueSymbol.ind = uniqueSymbols.readByte(locations['id'])

            uniqueSymbol.encounterID = uniqueSymbols.readHalfword(locations['encounterID'])
            uniqueSymbol.eventEncounterID = uniqueSymbols.readHalfword(locations['eventEncounterID'])
            
            symbolInd = uniqueSymbols.readHalfword(locations['symbol'])
            if (symbolInd < len(self.compendiumArr)):
                translation = self.compendiumArr[symbolInd].name
            else:
                translation = self.bossArr[symbolInd].name
            
            #Turn Seth into Event Encounter to prevent duplicate Seth
            if symbolInd == numbers.SETH_DEMON_ID:
                uniqueSymbol.encounterID = 0
                uniqueSymbol.eventEncounterID = numbers.SETH_EVENT_ENCOUNTER_ID

            uniqueSymbol.symbol = Translated_Value(symbolInd, translation)
            self.uniqueSymbolArr.append(uniqueSymbol)
            self.staticUniqueSymbolArr.append(copy.deepcopy(uniqueSymbol))

    '''
    Fills the erray chestArr with chest reward data including items, essences, and macca.
        Parameters:
            encounters (Table): buffer containing chest data
    '''
    def fillChestArr(self, chests):

        start = 0x45
        size = 0x1c
        #The tables standard size for symbols is 2081
        for index in range(801):
            offset = start + size * index

            locations = {
                'map': offset,
                'chestID': offset + 2,
                'item': offset + 0x10,
                'amount': offset + 0x12,
                'macca': offset + 0x14
            }
            

            chest = Item_Chest()
            chest.offsetNumber = locations
            chest.map = chests.readHalfword(locations['map'])
            chest.chestID = chests.readHalfword(locations['chestID'])
            itemID = chests.readHalfword(locations['item'])
            chest.item = Translated_Value(itemID, self.itemNames[itemID])
            chest.amount = chests.readByte(locations['amount'])
            chest.macca = chests.readWord(locations['macca'])
            self.chestArr.append(chest)

    '''
    Fills the list consumableArr with data about consumable items.
        Parameters:
            items (Table): buffer containing item data
    '''
    def fillConsumableArr(self, items):
        start = 0x55
        size = 100

        self.consumableArr.append(Consumable_Item())#Dummy Item

        for index in range(numbers.CONSUMABLE_ITEM_COUNT):
            item = Consumable_Item()
            item.ind = index +1
            item.offset = start + size * index
            item.name = self.itemNames[index +1]
            item.buyPrice = items.readWord(item.offset + 0x5C)
            self.consumableArr.append(item)
    
    '''
    Fills a list with the requirements to use fusion skills.
        Parameters:
            binTable (Table): buffer containing skill data
    '''
    def fillFusionSkillReqs(self, binTable):
        start = 0x255D5
        size = 32

        for index in range(30):
            offset = start + size * index
            skill = Fusion_Requirements()
            skill.offset = offset
            skill.ind = binTable.readWord(offset)
            skill.itemID = binTable.readWord(offset +4)
            for i in range(5):
                skill.demons.append(binTable.readWord(offset + 8 + 4*i))
            for i in range(2):
                skill.alignments.append([binTable.readByte(offset + 28 + i * 2),binTable.readByte(offset + 28 + i * 2 +1)])
            self.fusionSkillReqs.append(skill)
    
    def fillMapEventArr(self, binTable: Table):
        start = 0x45
        size = 148

        for index in range(701):
            offset = start + size * index
            event = Map_Event()
            event.offset = offset
            event.ind = binTable.readWord(offset)
            event.activationFlag = binTable.readWord(offset +4)
            event.compFlag1 = binTable.readWord(offset + 0x14)
            event.compFlag2 = binTable.readWord(offset + 0x18)
            event.mapID = binTable.readWord(offset + 0x1C)
            event.levelUMap = binTable.read32chars(offset + 0x24)

            self.mapEventArr.append(event)

    '''
    Fills the array navigatorArr with data on demon navigaors.
        Parameters:
            data (Buffer) the buffer containing all navigator data
    '''
    def fillNavigatorArr(self, data):
        start = 0x2AD41
        size = 0xC
        
        for index in range(25):
            offset = start + size * index
            navi = Navigator()
            navi.offset = offset
            navi.demonID = data.readHalfword(offset)
            navi.itemBonus = data.readHalfword(offset + 2)
            navi.itemType = data.readByte(offset + 4)
            navi.openFlag = data.readHalfword(offset + 8)
            self.navigatorArr.append(navi)
            self.navigatorVoiceIDs.append(message_logic.normalVoiceIDForBoss(navi.demonID, self.enemyNames).zfill(3))

    '''
    Based on the skill id returns the object containing data about the skill from one of skillArr, passiveSkillArr or innateSkillArr.
        Parameters:
            ind (Number): the id of the skill to return
        Returns:
            The skill object with the given id
    '''
    def obtainSkillFromID(self, ind):
        #print(ind)
        if ind <= 400:
            return self.skillArr[ind]
        elif ind <= 530:
            return self.passiveSkillArr[ind - 401]
        elif ind <= 800:
            return self.innateSkillArr[ind - 531]
        else:
            return self.skillArr[ind - 400]
    
    '''
    Returns the correct player demon object for a demon ID.
    '''
    def getPlayerDemon(self, ind):
        if ind >= len(self.compendiumArr):
            return self.playerBossArr[ind]
        else:
            return self.compendiumArr[ind]
    
    '''
    Generate a list of the levels each skill is obtained at
        Returns:
            An array containing skill names, ids and the levels they are obtained at
            {name: n, id: i, level: [x,y,z,...]}
    '''
    def generateSkillLevelList(self):
        #For every Skill name create object containing name, id and empty level array
        skillLevels = []
        for i in range(len(self.skillNames)):
            skillLevels.append(Skill_Level(self.skillNames[i], i, level=[]))
        bonusSkills = numbers.getBonusSkills()
        if self.configSettings.fixUniqueSkillAnimations:
            bonusSkills = bonusSkills + numbers.getAnimationFixOnlySkills()
        if self.configSettings.includeEnemyOnlySkills:
            bonusSkills = bonusSkills + numbers.getEnemyOnlySkills()
        if self.configSettings.includeMagatsuhiSkills:
            magatsuhiSkills = []
            for skillID in numbers.MAGATSUHI_SKILLS: #add magatsuhi skills available at all levels
                if skillID in self.fusionSkillIDs: #do not add fusion skills, since they are demon dependent
                    continue
                try: #if the skill has a special level requirement use it
                    levels = numbers.MAGATSUHI_SKILLS_LEVEL_RESTRICTIONS[skillID]
                    minLevel = levels[0]
                    maxLevel = levels[1]
                except KeyError: #else do from 1 to 99
                    minLevel = 1
                    maxLevel = 99
                magatsuhiSkills.append([translation.translateSkillID(skillID, self.skillNames),skillID,minLevel,maxLevel])
            bonusSkills = bonusSkills + magatsuhiSkills
        def findBonusSkill(ind):
            goal = []
            for skill in bonusSkills:
                if skill[1] == ind:
                    goal = skill
            return goal
        #For every demon...
        for demon in self.compendiumArr:
            #Add the demons level to the array of its Innate Skill
            skillLevels[demon.innate.ind].level.append(demon.level.value)
            #Add the demons level to their initially learned skills
            for skill in demon.skills:
                skillLevels[skill.ind].level.append(demon.level.value)
            #Add the level the demons learns a skill at to the skills level list
            for skill in demon.learnedSkills:
                skillLevels[skill.ind].level.append(skill.level)
        for demonID in numbers.GUEST_IDS:
            if demonID > numbers.NORMAL_ENEMY_COUNT:
                demon = self.playerBossArr[demonID]
            else:
                demon = self.compendiumArr[demonID]
            #Add the demons level to the array of its Innate Skill
            skillLevels[demon.innate.ind].level.append(demon.level.value)
            #Add the demons level to their initially learned skills
            for skill in demon.skills:
                skillLevels[skill.ind].level.append(demon.level.value)
            #Add the level the demons learns a skill at to the skills level list
            for skill in demon.learnedSkills:
                skillLevels[skill.ind].level.append(skill.level)

                
        #For every skill determine the minimum and maximum level it is obtained at
        def mapSkillLevels(skill):
            minLevel = 99
            maxLevel = 1
            for element in skill.level:
                if element > maxLevel:
                    maxLevel = element
                if element < minLevel:
                    minLevel = element
            if len(skill.level) == 0:
                minLevel = 0
                maxLevel = 0
            if len(findBonusSkill(skill.ind)) > 0:
                tem = findBonusSkill(skill.ind)
                minLevel = tem[2]
                maxLevel = tem[3]
            return Skill_Level(skill.name, skill.ind, level=[minLevel, maxLevel])
        skillLevels = list(map(mapSkillLevels, skillLevels))
        return skillLevels

    '''
    Generate a list of each level and what skills can be obtained at that level.
    A skill is obtainable at a level when the level is not outside of the bounds set by the skills
    min and max level.
        Parameters:
            skillLevels (Array(Skill_Level)): [{name:n, id:i, level:[x,y,...]},{...}]
        Returns:
            Array of levels and the skills at that level in the following form [[id, id, id],...]
    '''
    def generateLevelSkillList(self, skillLevels):
        levelList = []
        #Rebuild Level Array
        for index in range(100):
            foundSkills = []
            '''
            For each skill, add it to the foundSkills Array if it fulfills the following conditions
                - not already in the array
                - not an innate skill
                - current level is in the bounds [min,max] set by skill
                - is not an unused or uneditable skill
            '''
            for skill in skillLevels:
                if (not any(a.ind == skill.ind for a in foundSkills)) and (skill.ind <= 530 or skill.ind >= 801) and skill.level[0] <= index and index <= skill.level[1] and not skill.name.startswith("//Don't edit or remove th") and not skill.name.startswith('NOT USED:'):
                    foundSkills.append(skill)
            #Build new sorted array from ids of skills of foundSkills Array
            skillIndeces = map(lambda x: x.ind, foundSkills)
            #Remove duplicates
            uniqueIndeces = list(set(skillIndeces))
            uniqueIndeces.sort()
            #Rebuild array with duplicates removed
            final = []
            for unique in uniqueIndeces:
                skill = next(val for x, val in enumerate(foundSkills) if val.ind == unique)
                name = translation.translateSkillID(skill.ind, self.skillNames)
                final.append(Skill_Level(name, skill.ind))
            levelList.append(final)
        return levelList

    '''
    Randomizes the requirements to use magatsuhi skills, either due to race, demon combination or alignment combination.
    Note: When Critical is randomized, fusion and race skills are not mixed with each other, since the first magatsuhi skill in skill table
    without races assigned to it, serves as criticals replacement.
    This also means that Omnipotent Succession can never be the replacement for critical.
    '''
    def randomizeMagatsuhiSkillReqs(self):
        magatsuhiSkillResults = []
        requiredFusionNumber = len(self.fusionSkillIDs)
        newFusionSkills = []
        availableRaces = []
        
        while len(newFusionSkills) < requiredFusionNumber: #get new fusion skills
            skill = random.choice(numbers.MAGATSUHI_SKILLS)
            if self.configSettings.includeOmagatokiCritical: #Due to how the universal magatsuhi skill is chosen, fusion skills and race skills cannot be mixed if this is randomized
                newFusionSkills = sorted(self.fusionSkillIDs,key=lambda x: random.random())
                break
            if skill in newFusionSkills or (skill == 60) or (skill == 928 and not self.configSettings.includeOmnipotentSuccession):
                #dont add skills that are already there or critical has to be tied to race and succession depends on setting
                continue
            newFusionSkills.append(skill)
            skill = self.obtainSkillFromID(skill)
            if skill.magatsuhi.race1.value > 0:
                availableRaces.append(skill.magatsuhi.race1.value) # gather races
                skill.magatsuhi.race1.value = 0 #set races to 0
            if skill.magatsuhi.race2.value > 0: #gather second race if it is there
                availableRaces.append(skill.magatsuhi.race2.value)
                skill.magatsuhi.race2.value = 0

        
        magaSkills = []
        for skillID in numbers.MAGATSUHI_SKILLS:
            if skillID in newFusionSkills: #if skill is already decided to be a fusion skill
                continue
            skill = self.obtainSkillFromID(skillID)
            if (skill.ind == 60 and not self.configSettings.includeOmagatokiCritical) or (skill.ind == 928 and not self.configSettings.includeOmnipotentSuccession) :
                #only add race and skill for omagatoki critical and succession when setting is set
                continue
            if skill.magatsuhi.race1.value > 0 or skill.ind == 60:
                availableRaces.append(skill.magatsuhi.race1.value) # gather races
                skill.magatsuhi.race1.value = 0 #set races to 0
            if skill.magatsuhi.race2.value > 0: #gather second race if it is there
                availableRaces.append(skill.magatsuhi.race2.value)
                skill.magatsuhi.race2.value = 0
            magaSkills.append(skill)
        if self.configSettings.includeOmagatokiCritical: #manual choosing of omagatoki criticals replacement
            success = True
            while success: #Since Succession can not replace critical repeat until chosen skill is not succession
                skill = random.choice(magaSkills)
                if skill.ind != 928:
                    success = False
            availableRaces.remove(0)
            magatsuhiSkillResults.append(skill)
            magaSkills.remove(skill)
        while len(availableRaces) > 0: #while there is a race to assign
            race = random.choice(availableRaces)
            skill = random.choice(magaSkills)
            availableRaces.remove(race)
            if skill.magatsuhi.race1.value == 0: #if first race has not been assigned yet
                if len(availableRaces) < len(magaSkills): #less races than skills means we need to remove skill to ensure each skill has at least one race assigned to it
                    magatsuhiSkillResults.append(skill)
                    magaSkills.remove(skill)
                skill.magatsuhi.race1.value = race
            else: #assign second race and remove skill since no races can be assigned to it
                magatsuhiSkillResults.append(skill)
                magaSkills.remove(skill)
                skill.magatsuhi.race2.value = race
            
        # for skillID in numbers.MAGATSUHI_SKILLS:
        #     if skillID in newFusionSkills:
        #         #print(str(skillID) + "FUSION")
        #         pass
        #     else:
        #         skill = self.obtainSkillFromID(skillID)
        #         print(str(skillID) + " " + RACE_ARRAY[skill.magatsuhi.race1.value]+ " " + RACE_ARRAY[skill.magatsuhi.race2.value])
        
        self.fusionSkillReqs = self.updateFusionSkillRequirements(newFusionSkills)
        self.fusionSkillIDs = newFusionSkills
        return magatsuhiSkillResults

    '''
    Updates the requirements for fusion skills by taking the a list of skill ids and replacing the ids of fusion skills with them.
    Also randomizes which demons are required to use fusion skills.
        Parameters:
            newFusionSkills (Int): list of skill ids to replace current fusion skill ids
    '''
    def updateFusionSkillRequirements(self,newFusionSkills):
        newFusionSkillReqs = []
        currentIndex = 0
        for skill in self.fusionSkillReqs:
            if skill.ind not in self.fusionSkillIDs: #skip empty entry and enemy only fusion skills (Annihilation Ray and another Qadistu Entropy)
                newFusionSkillReqs.append(skill)
                continue
            skill.ind = newFusionSkills[currentIndex]
            currentIndex += 1

            validDemonChoices = list(filter(lambda demon: 'NOT USED' not in demon.name and 'Mitama' not in demon.name and demon.ind not in numbers.BAD_IDS , self.compendiumArr))
            if skill.demons[0] != 0: #if fusion req slot has demons tied to it
                demonsNames = ""
                newDemons = []
                for demon in skill.demons:
                    if demon > 0: #if the demon slot is not empty, get a new demon
                        newDemon = random.choice(validDemonChoices)
                        demonID = newDemon.ind
                        validDemonChoices.remove(newDemon)
                    else: #else set demon to no demon
                        demonID = 0
                    newDemons.append(demonID)
                    demonsNames = demonsNames + self.enemyNames[demonID]
                #print(str(skill.ind) + demonsNames)
                skill.demons = newDemons
            #print(str(skill.ind) + " " + str(skill.alignments[0][0])+ " " + str(skill.alignments[0][1])+ " " + str(skill.alignments[1][0])+ " " + str(skill.alignments[1][1]))
            newFusionSkillReqs.append(skill)
        return newFusionSkillReqs

    '''
    Assigns every demon new skills randomized using weights based on the passed settings.
    The range of skills available can either be all or level ranges around the demons level.
    Additionally, the weights are either the same for every skill or adjusted based on level range or potential and stat of demon.
    Furthermore the process ensures that each demon starts with at least one active skill.
        Parameters: 
            comp (Array): The array of demons
            levelList (Array(Skill_Level)): The list of levels and their learnable skills
            settings (Settings): settings set in gui
            mask (Array(number)): An optional list of demon IDs to filter comp by, only randomizing skills of those demons
        Returns:
            The edited compendium
    '''
    def assignRandomSkills(self, comp, levelList, settings, mask=None):
        totalSkillAmount = 0
        #If the skills aren't supposed to be scaled based on level, assemble list where each valid skill appears exactly once
        
        levelAggregrate = []
        for index, level in enumerate(levelList):
            if index == 0:
                #Prevents Magatsuhi skills from being in demons skill pools
                continue
            for skill in level:
                levelAggregrate.append(skill)
        uniqueSkills = {skill.ind for skill in levelAggregrate}
        allSkills = []
        for ind in uniqueSkills:
                allSkills.append(next(skill for skill in levelAggregrate if skill.ind == ind))
        if not mask and (settings.scaledSkills or settings.levelWeightedSkills):
            sortedComp = sorted(comp, key=lambda demon: demon.level.value)
        elif not mask:
            sortedComp = sorted(comp,key=lambda x: random.random())
        else:
            sortedComp = comp

        #For every demon...
        for demon in sortedComp:     
            if (mask and demon.ind not in mask) or demon.ind in numbers.INACCESSIBLE_DEMONS or demon.name.startswith("NOT USED") :
                continue
            possibleSkills = []
            if settings.scaledSkills or settings.levelWeightedSkills:
                #get all skills that can be learned at the demons level
                if demon.level.value > 0:
                    possibleSkills = levelList[demon.level.value]
                #And add the skills learnable at up to 3 level below and above the demons level
                if demon.level.value < 99:
                    possibleSkills = possibleSkills + levelList[demon.level.value + 1]
                if demon.level.value > 1:
                    possibleSkills = possibleSkills + levelList[demon.level.value - 1]
                if demon.level.value > 2:
                    possibleSkills = possibleSkills + levelList[demon.level.value - 2]
                if demon.level.value > 3:
                    possibleSkills = possibleSkills + levelList[demon.level.value - 3]
                if demon.level.value < 98:
                    possibleSkills = possibleSkills + levelList[demon.level.value + 2]
                if demon.level.value < 97:
                    possibleSkills = possibleSkills + levelList[demon.level.value + 3]
                #Increase skill pool for demons above level 70 due to diminishing demon numbers
                if demon.level.value > 70:
                    possibleSkills = possibleSkills + levelList[demon.level.value - 4]
                    possibleSkills = possibleSkills + levelList[demon.level.value - 5]
                #Increase skill pool for demons above level 90 due to diminishing demon numbers
                if demon.level.value > 90:
                    possibleSkills = possibleSkills + levelList[demon.level.value - 6]
                    possibleSkills = possibleSkills + levelList[demon.level.value - 7]
                    possibleSkills = possibleSkills + levelList[demon.level.value - 8]
                #Increase skill pool for demons at level 1 due to low number of available skills
                if demon.level.value == 1:
                    possibleSkills = possibleSkills + levelList[demon.level.value + 4]
                    possibleSkills = possibleSkills + levelList[demon.level.value + 5]
            else:
                #No level scaling so copy list of all skilsl
                possibleSkills = allSkills.copy()
            if settings.levelWeightedSkills:
                #use both skills around current level and all skills
                levelWeightedSkills = copy.deepcopy(possibleSkills)
                possibleSkills = possibleSkills + allSkills.copy()
                weightedSkills = self.createWeightedSkillList(possibleSkills, allSkills,demon, levelWeightedSkills)
            else:
                #use just possible skills
                weightedSkills = self.createWeightedSkillList(possibleSkills, allSkills, demon)


            totalSkills = []

            #Makes sure at least 8 skills are available to be given to demon
            validSkills = 0
            for weight in weightedSkills.weights:
                if weight > 0:
                    validSkills += 1
            if validSkills < 8: #Tao/Yoko need at least 8 skills in pool, most other at least 7
                for weight in weightedSkills.weights:
                    weight += 1
            
            #If there are skills to be learned
            if len(weightedSkills.values) > 0:

                #For every skill...
                for index in range(len(demon.skills)):
                    foundSkill = False
                    if demon.skills[index].value == 0:
                        # Don't set empty skill slots 
                        continue
                    rng = 0
                    attempts = 100
                    while not foundSkill:
                        # until valid skill is found
                        rng = random.choices(weightedSkills.values, weightedSkills.weights)[0]
                        if attempts <= 0:
                            print("Something went wrong in skill rando at level " + str(demon.level.value))
                            weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                            foundSkill = True
                            break
                        # Ensure Demon has at least one active skill and no skill appears twice
                        if not any(e.ind == rng for e in totalSkills) and self.ensureAtLeastOneActive(totalSkills, demon, rng):
                            #Check if skill passes additional conditions or skip that check if skills are not supposed to be weighted by stats and potentials
                            if not settings.potentialWeightedSkills or (self.checkAdditionalSkillConditions(self.obtainSkillFromID(rng), totalSkills, demon)):
                                if self.checkUniqueSkillConditions(self.obtainSkillFromID(rng),demon,comp,settings):
                                    if rng in numbers.MAGATSUHI_SKILLS: #only 1 magatsuhi skill assigned to skill set
                                        for weightIndex,checkSkill in enumerate(weightedSkills.values):
                                            if checkSkill in numbers.MAGATSUHI_SKILLS:
                                                weightedSkills.weights[weightIndex] = 0
                                    foundSkill = True
                                    weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                                else:
                                #elif not (settings.freeInheritance or settings.randomInheritance):
                                    weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                        attempts -= 1
                    skillAddition = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
                    totalSkills.append(skillAddition)
                    self.alreadyAssignedSkills.add(rng)
                    demon.skills[index] = skillAddition
                    totalSkillAmount += 1
                #Randomly assign learnable skills; same justifications as starting skills
                for index in range(len(demon.learnedSkills)):
                    foundSkill = False
                    rng = 0
                    attempts = 100
                    while not foundSkill:
                        rng = random.choices(weightedSkills.values, weightedSkills.weights)[0]
                        if attempts <= 0:
                            print("Something went wrong in leanred skill rando at level " + str(demon.level.value) + "for demon " + str(demon.name))
                            weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                            foundSkill = True
                        if not any(e.ind == rng for e in totalSkills):
                            if not settings.potentialWeightedSkills or (self.checkAdditionalSkillConditions(self.obtainSkillFromID(rng), totalSkills, demon)):
                                if self.checkUniqueSkillConditions(self.obtainSkillFromID(rng),demon,comp,settings):
                                    if rng in numbers.MAGATSUHI_SKILLS: #only 1 magatsuhi skill assigned to skill set
                                        for weightIndex,checkSkill in enumerate(weightedSkills.values):
                                            if checkSkill in numbers.MAGATSUHI_SKILLS:
                                                weightedSkills.weights[weightIndex] = 0
                                    foundSkill = True
                                    weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                                else:
                                #elif not (settings.freeInheritance or settings.randomInheritance):
                                    weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                        attempts -= 1
                    skillAddition = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
                    totalSkills.append(skillAddition)
                    self.alreadyAssignedSkills.add(rng)
                    demon.learnedSkills[index] = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames), level=demon.learnedSkills[index].level)
                    totalSkillAmount += 1
        #print("TOTAL SKILL SLOTS USED " + str(totalSkillAmount))
        return comp
    
    '''
    Randomly assigns innate skills to all compendium demons. 
        Parameters:
            comp (Array(Compendium_Demon)) array of all demons
            mask (List(Number)) Optional list of demon IDs to filter comp by, only randomizing innates of those demons
    '''
    def assignRandomInnates(self, comp, mask=None):
        
        # These don't work besides on their original demons
        # Moirae Cutter, Moirae Spinner, Moirae Measurer
        limited = [573, 574, 575]
        possibleInnates = [s for s in self.innateSkillArr if s.ind not in numbers.BAD_INNATES and "NOT USED" not in s.name]
        
        try:
            demons = [d for d in comp if "Mitama" not in d.name]
        except TypeError:
            demons = comp

        for demon in demons:
            if mask and demon.ind not in mask:
                continue
            validSkill = False
            attempt = 0
            while not validSkill and attempt < 20:
                attempt += 1
                innate = random.choice(possibleInnates)
                if innate.ind in limited and not innate.ind == demon.innate.value:
                    continue
                # Prevents that useless innates are assigned to a demon
                if self.checkAdditionalSkillConditions(innate, [], demon):
                    validSkill = True
            demon.innate.value = innate.ind
            demon.innate.translation = innate.name

    '''
    Assigns a random innate skill to the nahobino.
        Parameters:
            naho (Nahobino)
    '''
    def assignRandomInnateToNahobino(self, naho):

        badInnates = numbers.BAD_INNATES + numbers.BAD_INNATES_NAHO

        possibleInnates = [s for s in self.innateSkillArr if s.ind not in badInnates and "NOT USED" not in s.name]

        innate = random.choice(possibleInnates)
        naho.innate = innate.ind

    '''
    Assigns the Nahobino a random starting skill, either completely random or a low level skill depending on value of scaled.
    Due to the combat tutorial the skill has to be active as well as cost at most 60 MP.
        Parameters:
            naho (Nahobino): Data of main character
            levelList (Array(SkillLevel)): list of which skills can be learned at which level
            scaled (Boolean): whether or not the random skill is forced to be a low level skill
    '''
    def assignRandomStartingSkill(self, naho, levelList, settings):
        if not settings.scaledSkills:
            allSkills = []
            for index,level in enumerate(levelList):
                if index == 0:
                    #Prevents Magatsuhi skills from being in demons skill pools
                    continue
                for skill in level:
                    allSkills.append(skill)
        else:
            allSkills = levelList[1] + levelList[2]  + levelList[3] + levelList[4]  +levelList[5]  +levelList[6]   
            
        uniqueSkills = {skill.ind for skill in allSkills}
        possibleSkills = []
        for ind in uniqueSkills:
            possibleSkills.append(next(skill for skill in allSkills if skill.ind == ind))
        ''' 
        No longer needed due to Tutorial Removal
        # Nahobino needs active skill due to Tutorial
        possibleSkills = [s for s in possibleSkills if self.determineSkillStructureByID(s.ind) == "Active"]
        
        
        # Cost needs to be not more than 60
        possibleSkills = [s for s in possibleSkills if self.obtainSkillFromID(s.ind).cost <= 60]
        '''   
        validity = False
        skill = self.obtainSkillFromID(random.choice(possibleSkills).ind)
        while not validity:
            skill = self.obtainSkillFromID(random.choice(possibleSkills).ind)
            if skill.ind in numbers.MAGATSUHI_SKILLS and random.random() > 0.5:
                #Reduce chance that the protagonist starts with magatsuhi skill
                continue
            if skill.owner.ind == -2:
                #next skill if skill is Demon Only (Inspiring Leader)
                continue
            if settings.multipleUniques:
            # Unique skill can appear twice
                # check if skill is unique skill
                if skill.owner.ind == 0:
                    validity = True
                elif settings.freeInheritance:
                    skill.owner.ind = 0
                    skill.owner.name = self.compendiumArr[0].name
                elif settings.randomInheritance and skill.owner.ind == skill.owner.original:
                    # if unique skills should be randomly reassigned and skill has not been already reassigned
                    skill.owner.ind = -1
                    skill.owner.name = "Nahobino"
                validity = True
            else:
                if skill.owner.ind == 0:
                    validity = True
                if settings.freeInheritance:
                    skill.owner.ind = 0
                    skill.owner.name = self.compendiumArr[0].name
                    validity = True
                elif settings.randomInheritance:
                     # if unique skills should be randomly reassigned and skill has not been already reassigned
                    skill.owner.ind = -1
                    skill.owner.name = "Nahobino"
                    validity = True

        naho.startingSkill = skill.ind
        self.alreadyAssignedSkills.add(skill.ind)
    
    '''
    Check to see if adding the skill with index skillIndex to the demons skill list would leave him with at least one active starting skill.
        Parameters:
            totalSkills (Array): list of skills currently assigned to the demon
            demon (Compendium_Demon): the demon for which the condition is checked
            skillIndex (Integer): the id of the skill
        Returns:
            false if adding this skill would leave the demon without an active starting skill and true otherwise
    '''
    def ensureAtLeastOneActive(self,totalSkills, demon, skillIndex):
        nonEmpty = [d for d in demon.skills if d.ind != 0] 
        #Magatsuhi Skills do not count for the active skill requirement
        if  (len(totalSkills) + 1 == len(nonEmpty)) and ( skillIndex in numbers.MAGATSUHI_SKILLS or ((self.determineSkillStructureByID(skillIndex) != "Active") and not any(self.determineSkillStructureByID(e.ind) == "Active" for e in totalSkills))):
            #Check if we are at last initial skill and we have at least one active or current one is active
            return False
        return True

    '''
    Checks if the passed skill can be assigned to the demon according to the rules set for unique skills.
    Should a non unique skill be passed, always returns true.
        Parameters:
            skill (): the skill in question, can be passive or active
            demon (Compendium_Demon): the demon on who the skill should be assigned to
            comp (Array(Compendium_Demon)): list of all demons
            settings (Settings): settings describing the unique skill inheritance rules
        Returns:
            if assigning the skill to the demon follows the set unique skill inheritance rules
    '''
    def checkUniqueSkillConditions(self, skill, demon, comp, settings):
        lunationCondition = (skill.ind == numbers.LUNATION_FLUX_ID) and settings.restrictLunationFlux
        
        if skill.owner.ind == -2:
            # Demon Only skills should stay Demon only (Inspiring Leader)
            return True

        #Revival Chant should stay nahobino only skill
        if skill.ind == numbers.REVIVAL_CHANT_ID and demon.ind in numbers.PROTOFIEND_IDS:
            return True
        elif skill.ind == numbers.REVIVAL_CHANT_ID:
            return False
        
        if settings.multipleUniques and not lunationCondition:
        # Unique skill can appear twice
            # check if skill is unique skill
            if skill.owner.ind == 0:
                return True
            if settings.freeInheritance:
                # if unique skills should be freely inheritable
                skill.owner.ind = 0
                skill.owner.name = comp[0].name
            elif settings.randomInheritance and skill.owner.ind == skill.owner.original:
                # if unique skills should be randomly reassigned and skill has not been already reassigned
                if demon.ind in numbers.PROTOFIEND_IDS:
                    skill.owner.ind = -1
                    skill.owner.name = "Nahobino"
                else:
                    skill.owner.ind = demon.ind
                    skill.owner.name = demon.name
            elif settings.randomInheritance and skill.owner.ind != skill.owner.original:
                if random.random() > 0.5:
                    return False
            return True  
        else:
        # Unique skills can not appear twice
            if skill.owner.ind != skill.owner.original:
                # skill has already been reassigned, or set to free inheritance
                return False
            if skill.owner.ind == 0:
                # Skill is not unique
                return True
            if settings.freeInheritance and not lunationCondition:
                # if unique skills should be freely inheritable
                skill.owner.ind = 0
                skill.owner.name = comp[0].name
            elif settings.randomInheritance or (settings.freeInheritance and lunationCondition):
                # if unique skills should be randomly reassigned
                if demon.ind in numbers.PROTOFIEND_IDS:
                    skill.owner.ind = -1
                    skill.owner.name = "Nahobino"
                else:
                    skill.owner.ind = demon.ind
                    skill.owner.name = demon.name
            elif lunationCondition and demon.ind in numbers.PROTOFIEND_IDS:
                # Lunation Flux can only be inherited by protofiends in vanilla inheritance when restrictLunationFlux is set
                return True
            elif skill.owner.original != demon.ind:
                # Vanilla inheritance and demon is not the original demon
                return False
        return True

    '''
    This function checks whether the given skill passes at least one of several conditions that are predefined before certain skills can be assigned to the demon.
    In order to check the conditions totalSkillList containing the currently assigned skills of the demon and the demon data itself is necessary.
    The functions returns true if the skill can be given to the demon and false otherwise.
        Parameters:
            skill (Object): The skill for which conditions are checked
            totalSkillList (Array): TotalSkillList The currently assigned skills to the demon
            demon (Compendium_Demon): The demon data itself
        Returns:
            True if the skill passes at least one condition and False otherwise
    '''
    def checkAdditionalSkillConditions(self, skill, totalSkillList, demon):
        conditionalSkills = ["Charge", "Critical Aura", "Concentrate", "Curse Siphon", "Great Curse Siphon", "Virus Carrier", "Bowl of Hygieia", "Heal Pleroma", "High Heal Pleroma", "Nation Founder", "Healing Hand", "Oath of Plenteousness",
            "Poison Adept", "Poison Master", "Sankosho", "Incendiary Stoning", "Roaring Mist", "Herkeios", "Carpet Bolting", "Catastrophic Gales", "Lighted Wheel", "Boon of Sloth", "Ceaseless Crucifixion", "Biondetta", "Nation Builder"
        ]

        #Return early if skill is not a skill for which special conditions apply.
        if skill.name not in conditionalSkills and "Pleroma" not in skill.name and "Enhancer" not in skill.name and "Gestalt" not in skill.name:
            return True

        if (skill.name == "Charge" or skill.name == "Critical Aura") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).skillType.value == 0 for e in totalSkillList) or demon.potential.physical > 0):
            #Check for Charge, Critical Aura when already assigned Str-Based Skill or Demon has positive Physical Potential
            return True
        elif skill.name == "Concentrate" and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).skillType.value == 1 for e in totalSkillList) or demon.stats.str.start <= demon.stats.mag.start):
            #Check for Concentrate when already assigned Mag-Based Skill or Demon has higher base mag than str
            return True
        elif (skill.name == "Curse Siphon" or skill.name == "Great Curse Siphon" or skill.name == "Virus Carrier") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).skillType.value == 2 for e in totalSkillList) or demon.potential.ailment > 0):
            #Check for Curse Siphon, Great Curse Siphon, Virus Carrier when already assigned ailment Skill or Demon has positive ailment Potential
            return True
        elif (skill.name == "Bowl of Hygieia" or skill.name == "Heal Pleroma" or skill.name == "High Heal Pleroma" or skill.name == "Nation Founder" or skill.name == "Healing Hand" or skill.name == "Oath of Plenteousness") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).skillType.value == 3 for e in totalSkillList) or demon.potential.recover > 0):
            #Check for Bowl of Hygieia, Heal Pleroma, High Heal Pleroma, Nation Founder, Healing Hand, Oath of Plenteousness when already assigned heal Skill or Demon has positive recover Potential
            return True
        elif (skill.name == "Poison Adept" or skill.name == "Poison Master") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).ailmentFlags.poison > 0 for e in totalSkillList) or demon.potential.ailment > 0):
            #Check for Poison Adept, Poison Master when already assigned poison-inflicting Skill or Demon has positive ailment Potential
            return True
        elif (skill.name == "Phys Pleroma" or skill.name == "High Phys Pleroma" or skill.name == "Phys Enhancer" or skill.name == "Phys Gestalt" or skill.name == "Sankosho") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 0 for e in totalSkillList) or demon.potential.physical > 0):
            #Check for Phys Pleroma, High Phys Pleroma, Phys Enhancer, Phys Gestalt, Sankosho when already assigned phys element Skill or Demon has positive Physical Potential
            return True
        elif (skill.name == "Fire Pleroma" or skill.name == "High Fire Pleroma" or skill.name == "Fire Enhancer" or skill.name == "Fire Gestalt" or skill.name == "Incendiary Stoning") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 1 for e in totalSkillList) or demon.potential.fire > 0):
            #Check for Fire Pleroma, High Fire Pleroma, Fire Enhancer, Fire Gestalt, Incendiary Stoning when already assigned fire element Skill or Demon has positive fire Potential
            return True
        elif (skill.name == "Ice Pleroma" or skill.name == "High Ice Pleroma" or skill.name == "Ice Enhancer" or skill.name == "Ice Gestalt" or skill.name == "Roaring Mist") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 2 for e in totalSkillList) or demon.potential.ice > 0):
            #Check for Ice Pleroma, High Ice Pleroma, Ice Enhancer, Ice Gestalt, Roaring Mist when already assigned ice element Skill or Demon has positive ice Potential
            return True
        elif (skill.name == "Elec Pleroma" or skill.name == "High Elec Pleroma" or skill.name == "Elec Enhancer" or skill.name == "Herkeios" or skill.name == "Elec Gestalt" or skill.name == "Carpet Bolting") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 3 for e in totalSkillList) or demon.potential.elec > 0):
            #Check for Elec Pleroma, High Elec Pleroma, Elec Enhancer, Herkeios, Elec Gestalt, Carpet Bolting when already assigned Elec element Skill or Demon has positive elec Potential
            return True
        elif (skill.name == "Force Pleroma" or skill.name == "High Force Pleroma" or skill.name == "Force Enhancer" or skill.name == "Force Gestalt" or skill.name == "Catastrophic Gales") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 4 for e in totalSkillList) or demon.potential.force > 0):
            #Check for Force Pleroma, High Force Pleroma, Force Enhancer, Force Gestalt, Catastrophic Gales when already assigned Force element Skill or Demon has positive Force Potential
            return True
        elif (skill.name == "Light Pleroma" or skill.name == "High Light Pleroma" or skill.name == "Light Enhancer" or skill.name == "Light Gestalt" or skill.name == "Lighted Wheel") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 5 for e in totalSkillList) or demon.potential.light > 0):
            #Check for Light Pleroma, High Light Pleroma, Light Enhancer, Light Gestalt, Lighted Wheel when already assigned Light element Skill or Demon has positive Light Potential
            return True
        elif (skill.name == "Dark Pleroma" or skill.name == "High Dark Pleroma" or skill.name == "Dark Enhancer" or skill.name == "Dark Gestalt" or skill.name == "Boon of Sloth") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 6 for e in totalSkillList) or demon.potential.dark > 0):
            #Check for Dark Pleroma, High Dark Pleroma, Dark Enhancer, Dark Gestalt, Boon of Sloth when already assigned Dark element Skill or Demon has positive Dark Potential
            return True
        elif (skill.name == "Almighty Pleroma" or skill.name == "High Almighty Pleroma" or skill.name == "Ceaseless Crucifixion") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).element.value == 7 for e in totalSkillList) or demon.potential.almighty > 0):
            #Check for Almighty Pleroma, High Almighty Pleroma, Ceaseless Crucifixion when already assigned Almighty element Skill or Demon has positive Almighty Potential
            return True
        elif (skill.name == "Biondetta") and (demon.race.value != 2 and demon.race.value != 3 and demon.race.value != 24 and demon.race.value != 28):
            #Check for Biondetta when demon does not belong to herald, megami, femme, lady race
            return True
        elif (skill.name == "Nation Builder") and (any(self.determineSkillStructureByID(e.ind) == "Active" and self.obtainSkillFromID(e.ind).skillType.value == 4 for e in totalSkillList) or demon.potential.support > 0):
            #Check for Nation Builder when already assigned support type skill or demon has positive support potential
            return True
        else:
            #Skill fullfills no additional skill conditions
            return False

    '''
    Returns the skill potential value based on the potential type indicated by a string.
        Parameters:
            name (String): The potential type to return the value of 
            potentials (Potentials): Contains data on the skill potential of a demon
        Returns:
            The skill potential described the given name
    '''
    def obtainPotentialByName(self, name, potentials):
        match name:
            case "Phys":
                return potentials.physical
            case "Fire":
                return potentials.fire
            case "Ice":
                return potentials.ice
            case "Elec":
                return potentials.elec
            case "Force":
                return potentials.force
            case "Light":
                return potentials.light
            case "Dark":
                return potentials.dark
            case "Almighty":
                return potentials.almighty
            case "Ailment":
                return potentials.ailment
            case "Recover":
                return potentials.recover
            case "Support":
                return potentials.support
            case _:
                return 0
    '''
    Scales the potentials of demons to their new level based on their original level.
        Parameters:
            comp (List(Compendium_Demon)): list of demons
    '''
    def scalePotentials(self,comp):
        def absSum(numbers):
            sum = 0
            for n in numbers:
                sum += abs(n)
            return sum

        for demon in comp:
            #Collect demons potentials
            potentials = []
            potentials.append(demon.potential.physical)
            potentials.append(demon.potential.fire)
            potentials.append(demon.potential.ice)
            potentials.append(demon.potential.elec)
            potentials.append(demon.potential.force)
            potentials.append(demon.potential.light)
            potentials.append(demon.potential.dark)
            potentials.append(demon.potential.almighty)
            potentials.append(demon.potential.ailment)
            potentials.append(demon.potential.support)
            potentials.append(demon.potential.recover)

            absolutePotentialSum = absSum(potentials)
            #Calculate absolute percentage of potentials
            percentages = []
            for pot in potentials:
                if pot != 0:
                    percentages.append(pot / absolutePotentialSum)
                else:
                    percentages.append(0)
            # scale potential to new level
            newAbsPotSum = round(numbers.POTENTIAL_SCALING_FACTOR * (demon.level.value - demon.level.original) + absolutePotentialSum)

            demon.potential.physical = math.ceil(max(-7,min(7,newAbsPotSum * percentages[0])))
            demon.potential.fire = math.ceil(max(-7,min(7,newAbsPotSum * percentages[1])))
            demon.potential.ice = math.ceil(max(-7,min(7,newAbsPotSum * percentages[2])))
            demon.potential.elec = math.ceil(max(-7,min(7,newAbsPotSum * percentages[3])))
            demon.potential.force = math.ceil(max(-7,min(7,newAbsPotSum * percentages[4])))
            demon.potential.light = math.ceil(max(-7,min(7,newAbsPotSum * percentages[5])))
            demon.potential.dark = math.ceil(max(-7,min(7,newAbsPotSum * percentages[6])))
            demon.potential.almighty = math.ceil(max(-7,min(7,newAbsPotSum * percentages[7])))
            demon.potential.ailment = math.ceil(max(-7,min(7,newAbsPotSum * percentages[8])))
            demon.potential.support = math.ceil(max(-4,min(4,newAbsPotSum * percentages[9])))
            demon.potential.recover = math.ceil(max(-4,min(4,newAbsPotSum * percentages[10])))

    '''
    Randomizes the potentials of demons. First defines how many potentials the demon should have and then assigns a percentage weight to them.
    These percentage weights are then used to assign potentials by first calculating the absolute potential sum via function that describes the trend of vanilla potentials.
        Parameters:
            comp (List(Compendium_Demon)): list of demons
            mask (List(Number)): Optional list of demon IDs to filter comp by, only randomizing potentials of those demons
    '''
    def randomizePotentials(self, comp, mask=None):
        

        for demon in comp:
            if mask and demon.ind not in mask:
                continue
            totalPercentage = 100
            if self.configSettings.betterSpecialFusions and demon.ind in self.specialFusionDemonIDs:
                totalPercentage = 200
            percentages = []
            for i in range(random.randint(3,9)):
                percentages.append(random.randint(0,int(totalPercentage/2)))

            while sum(percentages) != totalPercentage:
                randomN = random.randint(0,len(percentages)-1)
                if sum(percentages) < totalPercentage:
                    percentages[randomN] += 1
                else:
                    percentages[randomN] -= 1
            negatives = 1
            for index,percentage in enumerate(percentages):
                if random.randrange(0,totalPercentage) < (totalPercentage / negatives) and negatives < (len(percentages)/2):
                    percentages[index] = percentage * -1
                    negatives += 1

            while len(percentages) < 11:
                percentages.append(0)
            percentages = sorted(percentages, key=lambda x: random.random())
            newPotentials = []
            #follows rough trends of potentials in base demons
            absPotAmount = round(numbers.POTENTIAL_SCALING_FACTOR * demon.level.value + numbers.BASE_POTENTIAL_VALUE)
            for index,percentage in enumerate(percentages):
                percentage = percentage / totalPercentage
                # 7 is the base game max and min that occurs
                maxV = 7
                if(index > 8):
                    maxV = 4
                newPotentials.append(math.ceil(max(-1 * maxV,min(maxV,absPotAmount * percentage))))
            demon.potential.physical = newPotentials[0]
            demon.potential.fire = newPotentials[1]
            demon.potential.ice = newPotentials[2]
            demon.potential.elec = newPotentials[3]
            demon.potential.force = newPotentials[4]
            demon.potential.light = newPotentials[5]
            demon.potential.dark = newPotentials[6]
            demon.potential.almighty = newPotentials[7]
            demon.potential.ailment = newPotentials[8]
            demon.potential.support = newPotentials[9]
            demon.potential.recover = newPotentials[10]

    '''
    Randomizes the resistance profiles of demons. The process attempts to follow base game distribution of resistances and elemnents.
    The outcome is changed depending on what resistance settings are chosen.
        Parameters: 
            comp (List(Compendium_Demon)): List of demons
            mask (List(Number)): Optional list of demon IDs to filter comp by, only randomizing resitances of those demons
        #TODO: Not entirely happy with this, so consider completely rethinking this. Maybe taking base resist profiles and then shuffling
        either profiles or shuffle resists in profiles and then assign those randomly?
    '''
    def randomizeResistances(self, comp, mask = None):
        '''
        Adjust weights for the resistance level based on the potential of an element for a demon.
            Parameters:
                element(String): the potential to use for the element
                resistWeights(List): list of weights to modify
                demon(Compendium_Demon): demon to use potentials of
            Returns the modified list of weights
        '''
        def adjustResistWeightForPotential(element,resistWeights,demon):
            potential = demon.potential.__getattribute__(element)
            if potential == 0:
                #increase neutral chance
                resistWeights[4] = math.ceil(1.1 * resistWeights[4])
                return resistWeights
            elif potential < 0:
                #reduce resist chance, increase weakness chance
                multiplier = 1 - (potential / -10) 
                for i in range(4):
                    resistWeights[i] = math.ceil(resistWeights[i] * multiplier)
                #resistWeights[4] = math.ceil(multiplier  * resistWeights[4])
                multiplier = 1 - (potential / 10)
                resistWeights[5] = math.ceil(resistWeights[5] * multiplier)
            else:
                #reduce resist chance, increase weakness chance
                multiplier = 1 + potential / 10
                for i in range(4):
                    resistWeights[i] = math.ceil(resistWeights[i] * multiplier)
                #resistWeights[4] = math.ceil(multiplier  * resistWeights[4])
                multiplier = 1 + potential / -10
                resistWeights[5] = math.ceil(resistWeights[5] * multiplier)
            return resistWeights
        
        '''
        Adjust weights for the element based on the potential of that element for a demon.
            Parameters:
                element(String): the potential to use for the element
                elementWeights(List): list of weights to modify
                demon(Compendium_Demon): demon to use potentials of
                ailmentIndex(Number): optional index for ailments, which all use the same potential and thefore the same element name
            Returns the modified list of weights
        '''
        def adjustElementWeightForPotential(element,elementWeights,demon, ailmentIndex=None):
            potential = demon.potential.__getattribute__(element)
            if potential == 0:
                return elementWeights
            elif potential < 0:
                multiplier = 1 - potential / -10
            else:
                multiplier = 1 + potential / 10
            if ailmentIndex is not None:
                elementWeights[ailmentIndex] *= multiplier
            else:
                elementWeights[numbers.ELEMENT_RESIST_NAMES.index(element)] *= multiplier
            return elementWeights

        demonCount = 0
        
        if len(self.totalResistMap) == 0:
            for attr in vars(comp[0].resist):
                self.totalResistMap[attr] = {
                    -1.5: 0,
                    -1: 0,
                    0: 0,
                    0.5: 0,
                    1: 0,
                    1.5: 0
                }  
        resistProfiles = [] # will store the resistances of every demon, mostly for debug purposes

        #filter out all unused demons (unnamed and Old Lilith, Other Tao), mitamas
        if mask:
            filteredComp = [demon for demon in comp if demon.ind in mask]
        else:
            filteredComp = [demon for demon in comp if demon.ind not in numbers.INACCESSIBLE_DEMONS and not demon.name.startswith("NOT") and "Mitama" not in demon.name]
        filteredComp = sorted(filteredComp, key=lambda demon: demon.level.value)

        for demon in filteredComp:
            demon: Compendium_Demon
    
            
            demonCount += 1

            #calculate phys first
            if self.configSettings.scaledPhysResists:
                physWeights = copy.deepcopy(numbers.PHYS_RESIST_DISTRIBUTION[math.ceil(demon.level.value / 10)])
            else:
                physWeights = copy.deepcopy(numbers.PHYS_RESIST_DISTRIBUTION[0])
            
            if self.configSettings.potentialWeightedResists:
                #physical uses slightly differnt multipliers for potential weighting than other elements due to distribution
                if demon.potential.physical == 0:
                    physWeights[4] = math.ceil(1.1 * physWeights[4])
                elif demon.potential.physical < 0:
                    multiplier = 1 - demon.potential.physical / -20
                    for i in range(4):
                        physWeights[i] = math.ceil(physWeights[i] * multiplier)
                    multiplier = 1 - demon.potential.physical / 20
                    physWeights[5] = math.ceil(physWeights[5] * multiplier)
                else:
                    multiplier = 1 + demon.potential.physical / 20
                    for i in range(4):
                        physWeights[i] = math.ceil(physWeights[i] * multiplier)
                    multiplier = 1 + demon.potential.physical / -20
                    physWeights[5] = math.ceil(physWeights[5] * multiplier)
            
            
            validPhysResist = False
            while not validPhysResist: #reroll phys resist to be valid with diverseResists if enabled
                physResist = random.choices(numbers.SIMPLE_RESIST_VALUES,physWeights)[0]
                if self.configSettings.diverseResists and physResist != 1 and self.totalResistMap["physical"].get(physResist) > demonCount / numbers.DIVERSE_RESIST_FACTOR:
                    validPhysResist =False
                else:
                    validPhysResist = True
                    
            chosenResists = [1,1,1,1,1,1] #the element resist results will be saved here
            alreadyChosen = set() #will contain elements that have already been assigned
            
            allowedRange = 1.5 #this is the used to define the sum range in which the total resist sum is allowed to be

            if self.configSettings.scaledElementalResists:
                baselineSum=  round(numbers.calculateResistBase(demon.level.value) * 2) / 2 
            else:
                #base game sum is between roughly 1 and 11 here, so with 1.5 added ranges those end up the min/max values
                #sum is flat number or ends in .5
                baselineSum = round(random.uniform(3,10) * 2) / 2 
           
            if self.configSettings.betterSpecialFusions and demon.ind in self.specialFusionDemonIDs:
                #special fusions use lower allowed sum here
                baselineSum -= allowedRange
            
            #Phys is 1.5 because phys weakness/resists should have stronger impact than elemental ones
            currentSum = sum(chosenResists) + physResist * 1.5
            
            minRuns = 3 #minimum amount of elements for which a random resistance is generated

            #Stop choosing resistance values for elements if all elements are chosen or sum is breaking range limits
            while len(alreadyChosen) < len(numbers.ELEMENT_RESIST_NAMES) and (len(alreadyChosen) <= minRuns or baselineSum - allowedRange < currentSum < baselineSum + allowedRange):
                elementResistWeights = [] #these weights will be used to calculate which resist value is used
                
                #these weights are used to decide the elements based on the not already chosen ones
                elementWeights = [1 if numbers.ELEMENT_RESIST_NAMES[index] not in alreadyChosen else 0 for index,v in enumerate(chosenResists) ]
                element = random.choices(numbers.ELEMENT_RESIST_NAMES,elementWeights)[0]
                alreadyChosen.add(element)
                
                if self.configSettings.scaledElementalResists:
                    if element == "dark" or "light":
                        elementResistWeights = copy.deepcopy(numbers.LD_RESIST_DISTRIBUTION[math.ceil(demon.level.value / 10)])
                    else:
                        elementResistWeights = copy.deepcopy(numbers.FIEF_RESIST_DISTRIBUTION[math.ceil(demon.level.value / 10)])
                else:
                    if element == "dark" or "light":
                        elementResistWeights = copy.deepcopy(numbers.LD_RESIST_DISTRIBUTION[0])
                    else:
                        elementResistWeights = copy.deepcopy(numbers.FIEF_RESIST_DISTRIBUTION[0])
                
                if self.configSettings.potentialWeightedResists:
                    elementResistWeights = adjustResistWeightForPotential(element,elementResistWeights,demon)
                
                if self.configSettings.diverseResists:
                    for index, value in enumerate(self.totalResistMap[element].values()):
                        if 1 +value > demonCount / numbers.DIVERSE_RESIST_FACTOR and index != 4:# neutral resists are not subject to diverseResist setting
                            elementResistWeights[index] /= 2
                
                elementResist = random.choices(numbers.SIMPLE_RESIST_VALUES,elementResistWeights)[0]
                chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = elementResist
                currentSum = sum(chosenResists) + physResist * 1.5
                
            
            ailmentResists = [] #the ailment resist results will be saved here
            for _ in numbers.AILMENT_NAMES:
                ailmentResists.append(1)
            alreadyChosen = set()

            #ailments count half because they are should be worth less than elemental ones
            currentSum = sum(chosenResists) + physResist * 1.5 + sum(ailmentResists)/2
            
            if self.configSettings.scaledElementalResists:
                baselineSum = round(numbers.calculateTotalResistBase(demon.level.value) * 2) / 2
                if self.configSettings.betterSpecialFusions and demon.ind in self.specialFusionDemonIDs:
                    baselineSum -= allowedRange #since this is calculated again, needs to be applied again
            else:
                baselineSum += round(random.uniform(2,3) * 2) / 2 
            

            while len(alreadyChosen) < len(numbers.AILMENT_NAMES) and (len(alreadyChosen) <= minRuns or baselineSum - allowedRange < currentSum < baselineSum + allowedRange):
                ailmentResistWeights = []
                ailmentWeights = [1 if numbers.AILMENT_NAMES[index] not in alreadyChosen else 0 for index,v in enumerate(ailmentResists) ]
                ailment = random.choices(numbers.AILMENT_NAMES,ailmentWeights)[0]
                alreadyChosen.add(ailment)

                if self.configSettings.scaledElementalResists:
                    ailmentResistWeights = copy.deepcopy(numbers.AILMENT_RESIST_DISTRIBUTION[math.ceil(demon.level.value / 10)])
                else:
                    ailmentResistWeights = copy.deepcopy(numbers.AILMENT_RESIST_DISTRIBUTION[0])

                if self.configSettings.potentialWeightedResists:
                    ailmentResistWeights = adjustResistWeightForPotential("ailment",ailmentResistWeights,demon)
                
                if self.configSettings.diverseResists:
                    for index, value in enumerate(self.totalResistMap[ailment].values()):
                        if 1 +value > demonCount / numbers.DIVERSE_RESIST_FACTOR and index != 4:
                            ailmentResistWeights[index] /= 2

                ailmentResist = random.choices(numbers.SIMPLE_RESIST_VALUES,ailmentResistWeights)[0]
                ailmentResists[numbers.AILMENT_NAMES.index(ailment)] = ailmentResist
                currentSum = sum(chosenResists) + physResist * 1.5 + sum(ailmentResists)/2

            attempts = 100
            #try to make sum fit into range limits, to achieve somewhat balanced resist profiles
            while currentSum < baselineSum - allowedRange or currentSum > baselineSum + allowedRange:
                attempts -= 1
                if attempts <= 0:
                    print("Something went wrong in resist rando at level " + str(demon.level.value) + "for demon " + str(demon.name))
                    break
    
                if currentSum < baselineSum - allowedRange:
                    #add weaknesses/ make resist worse, Increase value
                    
                    randomTypes = {}
                    # types that only have weaknesses cannot be added, since no value to increase
                    if chosenResists.count(1.5) != len(chosenResists):
                        randomTypes.update({"Elements" : (numbers.FIEF_RESIST_DISTRIBUTION[0][5] + numbers.LD_RESIST_DISTRIBUTION[0][5])/2})
                    if ailmentResists.count(1.5) != len(ailmentResists):
                        randomTypes.update({"Ailments" : numbers.AILMENT_RESIST_DISTRIBUTION[0][5]})
                    if len(randomTypes) == 0: #not checking for phys weakness here, since physWeak would make it highly likely for this occur anyway
                        randomTypes.update({"Physical": numbers.PHYS_RESIST_DISTRIBUTION[0][5]})
                    if physResist == -1.5 and ailmentResists.count(1.5) != len(ailmentResists): #if phys is a drain add ailments with higher weights to reduce cases where most elements are weaknesses
                        randomTypes.update({"Ailments" : numbers.AILMENT_RESIST_DISTRIBUTION[0][5]* 2} )
                    changeType = random.choices(list(randomTypes.keys()), list(randomTypes.values()))[0]                  
                    
                    if changeType == "Ailments":
                        #weaks cannot be increased further
                        chooseAilmentWeights = [0 if r == 1.5 else 10 for r in ailmentResists]
                        if self.configSettings.potentialWeightedResists:
                            for ailmentIndex,_ in enumerate(numbers.AILMENT_NAMES):
                                chooseAilmentWeights = adjustElementWeightForPotential("ailment",chooseAilmentWeights,demon,ailmentIndex)
                        ailment = random.choices(numbers.AILMENT_NAMES,chooseAilmentWeights)[0]
                        ailmentResist = ailmentResists[numbers.AILMENT_NAMES.index(ailment)]
                        resistIndex = min(len(numbers.SIMPLE_RESIST_VALUES)-1,numbers.SIMPLE_RESIST_VALUES.index(ailmentResist)  +1)
                        ailmentResists[numbers.AILMENT_NAMES.index(ailment)] = numbers.SIMPLE_RESIST_VALUES[resistIndex]
                    elif changeType == "Physical":
                        element = "physical"
                        resistIndex = min(len(numbers.SIMPLE_RESIST_VALUES)-1,numbers.SIMPLE_RESIST_VALUES.index(physResist)  +1)
                        if self.configSettings.diverseResists:
                            
                            while resistIndex +1 < len(numbers.SIMPLE_RESIST_VALUES):
                                if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                    if self.totalResistMap[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > demonCount / numbers.DIVERSE_RESIST_FACTOR:
                                        resistIndex += 1
                                    else:
                                        break
                                else:
                                    break
                        physResist = numbers.SIMPLE_RESIST_VALUES[resistIndex]
                    else:
                        chooseElementWeights = [0 if r == 1.5 else 10 for r in chosenResists]
                        if self.configSettings.potentialWeightedResists:
                            for element in numbers.ELEMENT_RESIST_NAMES:
                                chooseElementWeights = adjustElementWeightForPotential(element,chooseElementWeights,demon)

                        element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
                        elementResist = chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)]
                        resistIndex = min(len(numbers.SIMPLE_RESIST_VALUES)-1,numbers.SIMPLE_RESIST_VALUES.index(elementResist)  +1)
                        # Avoid overpopulating resistances if diverseResists is enabled
                        if self.configSettings.diverseResists:
                            
                            while resistIndex +1 < len(numbers.SIMPLE_RESIST_VALUES):
                                if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                    if self.totalResistMap[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > demonCount / numbers.DIVERSE_RESIST_FACTOR:
                                        resistIndex += 1
                                    else:
                                        break
                                else:
                                    break
                        chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = numbers.SIMPLE_RESIST_VALUES[resistIndex]


                elif currentSum > baselineSum + allowedRange:
                    #add resists/make weakness worse, decrease value

                    randomTypes = {}
                    if chosenResists.count(-1.5) != len(chosenResists):
                        randomTypes.update({"Elements" : (numbers.FIEF_RESIST_DISTRIBUTION[0][5] + numbers.LD_RESIST_DISTRIBUTION[0][5])/2})
                    if ailmentResists.count(0) != len(ailmentResists): #ailments cannot have repel/drain
                        randomTypes.update({"Ailments" : numbers.AILMENT_RESIST_DISTRIBUTION[0][5]})
                    if len(randomTypes) == 0:
                        randomTypes.update({"Physical": numbers.PHYS_RESIST_DISTRIBUTION[0][5]})
                    changeType = random.choices(list(randomTypes.keys()), list(randomTypes.values()))[0]
                    
                    if changeType == "Ailments":
                        chooseAilmentWeights = [0 if r == 0 else 10  for r in ailmentResists]
                        if self.configSettings.potentialWeightedResists:
                            for ailmentIndex,_ in enumerate(numbers.AILMENT_NAMES):
                                chooseAilmentWeights = adjustElementWeightForPotential("ailment",chooseAilmentWeights,demon,ailmentIndex)
                        ailment = random.choices(numbers.AILMENT_NAMES,chooseAilmentWeights)[0]
                        ailmentResist = ailmentResists[numbers.AILMENT_NAMES.index(ailment)]
                        #ailments cannot have repel/drain
                        resistIndex = max(2,numbers.SIMPLE_RESIST_VALUES.index(ailmentResist) -1)
                        #TODO: Diversity?
                        ailmentResists[numbers.AILMENT_NAMES.index(ailment)] = numbers.SIMPLE_RESIST_VALUES[resistIndex]
                    elif changeType == "Physical":
                        element = "physical"
                        resistIndex = max(0,numbers.SIMPLE_RESIST_VALUES.index(physResist) -1)
                        if self.configSettings.diverseResists:
                            while resistIndex -1 > 0:
                                if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                    if self.totalResistMap[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > demonCount / numbers.DIVERSE_RESIST_FACTOR:
                                        resistIndex -= 1
                                    else:
                                        break
                                else:
                                    break

                        physResist = numbers.SIMPLE_RESIST_VALUES[resistIndex ]
                    else:
                        chooseElementWeights = [0 if r == -1.5 else 10  for r in chosenResists]
                        if self.configSettings.potentialWeightedResists:
                            for element in numbers.ELEMENT_RESIST_NAMES:
                                chooseElementWeights = adjustElementWeightForPotential(element,chooseElementWeights,demon)

                        element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
                        elementResist = chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)]
                        resistIndex = max(0,numbers.SIMPLE_RESIST_VALUES.index(elementResist) -1)
                        if self.configSettings.diverseResists:
                            while resistIndex -1 > 0:
                                if numbers.SIMPLE_RESIST_VALUES[resistIndex] == 1:
                                    if self.totalResistMap[element][numbers.SIMPLE_RESIST_VALUES[resistIndex]] > demonCount / numbers.DIVERSE_RESIST_FACTOR:
                                        resistIndex -= 1
                                    else:
                                        break
                                else:
                                    break

                        chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = numbers.SIMPLE_RESIST_VALUES[resistIndex ]
                currentSum = sum(chosenResists) + physResist * 1.5 + sum(ailmentResists) / 2
                
            allChosenResists = [physResist] + chosenResists
            if self.configSettings.alwaysOneWeak:
                weakAdded = False
                if not any(1.5 == r for r in allChosenResists): #Add random weakness
                    chooseElementWeights = [r + 3 for r in chosenResists] #neutrals have highest chance to become weak, drains the lowest
                    element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
                    chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = 1.5
                    allChosenResists = [physResist] + chosenResists
                    weakAdded = True
                if not any(r < 1 for r in allChosenResists): #Add random resistance for element that is not random weakness if it was added
                    weaknessCount = allChosenResists.count(1.5)
                    #null out weaknesses if there is only one, and prevent overwriting the potentially previously added one
                    chooseElementWeights = [ 0 if (weaknessCount < 2 and r==1.5 ) or (weakAdded and index == numbers.ELEMENT_RESIST_NAMES.index(element))else -(r - 3) for index,r in enumerate(chosenResists)]
                    element = random.choices(numbers.ELEMENT_RESIST_NAMES,chooseElementWeights)[0]
                    chosenResists[numbers.ELEMENT_RESIST_NAMES.index(element)] = 0.5
                    allChosenResists = [physResist] + chosenResists

            #Apply resist to demon and increase values in totalResistMap
            demon.resist.physical = Translated_Value(numbers.SIMPLE_RESIST_RESULTS[physResist],translation.translateResist(numbers.SIMPLE_RESIST_RESULTS[physResist]))
            self.totalResistMap["physical"][physResist] += +1

            for index, element in enumerate(numbers.ELEMENT_RESIST_NAMES):
                self.totalResistMap[element][chosenResists[index]] += 1
                demon.resist.__setattr__(element,Translated_Value(numbers.SIMPLE_RESIST_RESULTS[chosenResists[index]],translation.translateResist(numbers.SIMPLE_RESIST_RESULTS[chosenResists[index]])))
            resistProfiles.append([physResist] + chosenResists + ailmentResists)
            for index, ailment in enumerate(numbers.AILMENT_NAMES):
                self.totalResistMap[ailment][ailmentResists[index]] += 1
                demon.resist.__setattr__(ailment,Translated_Value(numbers.SIMPLE_RESIST_RESULTS[ailmentResists[index]],translation.translateResist(numbers.SIMPLE_RESIST_RESULTS[ailmentResists[index]])))
            #print(demon.name + " " + str(currentSum) + " ( " + str(baselineSum) + ")")
        #print(demonCount)
        #pprint(totalResistMap)
        #return totalResistMap, resistProfiles #Uncomment for debug printing potentially

    '''
    Based on array of skills creates a Weighted_List object where each skill is only included once.
    Weight depends of if skill has already been assigned in the randomization process and if they are a magatsuhi skill, as well as potentials, stat preferenrentials.
    Weight is also modified by seperate settings, to ensure all skills are weighted by level or minimizind duplicate skill assignments.
        Parameters:
            possiblSkills (Array): Array of skills
            allSkills (List): List of all skills that can be assigned
            demon (Compendium_Demon): the demon for whom the list is generated
            levelWeightedSkills(List): a list of skills that marks skills as level appropriate
        Returns:
            An object with an array of values and an array of weights and an array of names for the skills
    '''
    def createWeightedSkillList(self, possibleSkills, allSkills,demon: Compendium_Demon, levelWeightedSkills=None):
        potentials = demon.potential
        
        if levelWeightedSkills:
            levelWeightedSkills = [s.ind for s in levelWeightedSkills]
        if len(self.alreadyAssignedSkills) == len(allSkills):
            self.alreadyAssignedSkills = set()
        random.shuffle(possibleSkills) 
        ids = []
        prob = []
        names = []
        #for every skill...
        for skill in possibleSkills:
            if skill.name == 'Filler':
                continue #Exclude filler skill because it has Null values
            if skill.ind not in ids:               
                #else push value and base weight 
                ids.append(skill.ind)
                if skill.ind in numbers.MAGATSUHI_SKILLS:
                    probability = numbers.MAGATSUHI_SKILL_WEIGHT
                    #Magatsuhi skills are not effected by potential and keep their weight
                else:
                    probability = numbers.SKILL_WEIGHT
                    realSkill = self.obtainSkillFromID(skill.ind)
                    skillStructure = self.determineSkillStructureByID(skill.ind)
                    #Passive skills do not have a corresponding potential by default so we need to handle them seperately
                    if self.configSettings.potentialWeightedSkills and skillStructure == "Active":
                        potentialType = realSkill.potentialType.translation
                        potentialValue = self.obtainPotentialByName(potentialType, potentials)
                        if potentialType == "Phys":
                            bonus = (1 + (potentialValue / (numbers.POTENTIAL_WEIGHT_MULITPLIER * 1.5)))
                            if potentialValue > 0:
                                bonus += 0.55
                            elif potentialValue < 0:
                                bonus -= 0.25
                            probability *= bonus
                        else:
                            bonus = (1 + (potentialValue / numbers.POTENTIAL_WEIGHT_MULITPLIER ))
                            if potentialValue > 0:
                                bonus += 0.55
                            elif potentialValue < 0:
                                bonus -= 0.25
                            probability *= bonus
                        if realSkill.skillType.value == 0 and demon.stats.str.start < demon.stats.mag.start:
                            probability = probability * numbers.SKILL_STAT_PENALTY_MULTIPLIER
                        elif realSkill.skillType.value == 1 and demon.stats.str.start > demon.stats.mag.start:
                            probability = probability * numbers.SKILL_STAT_PENALTY_MULTIPLIER
                    if self.configSettings.limitSkillMPCost and skillStructure == "Active":
                        potentialType = realSkill.potentialType.translation
                        potentialValue = self.obtainPotentialByName(potentialType, potentials)
                        baseCost = realSkill.cost
                        if potentialType in ["Recovery","Ailment","Support"]:
                            baseCost *= numbers.NON_OFFENSIVE_POTENTIAL_COST_MULTIPLIERS[min(5,max(-5,potentialValue))]
                        else:
                            baseCost *= numbers.OFFENSIVE_POTENTIAL_COST_MULTIPLIERS[potentialValue]
                        if baseCost > demon.stats.MP.start:
                            probability = 0

                
                if skill.ind in self.alreadyAssignedSkills:
                    probability = probability * numbers.SKILL_APPEARANCE_PENALTY_MULTIPLIER
                if levelWeightedSkills and skill.ind in levelWeightedSkills:
                    probability *= numbers.LEVEL_SKILL_WEIGHT_MULTIPLIER
                if skill.ind not in self.alreadyAssignedSkills and self.configSettings.forceAllSkills:
                    #increase weight if skill are forced and skill not already assigned
                    #weight increase is higher the more skills have already been assigned
                    probability = probability * (1 + max(1,(len(self.alreadyAssignedSkills)/ 2))/10)
                    #probability = probability * numbers.FORCE_SKILL_MULTIPLIER

                prob.append(probability)
                names.append(skill.name)
        return Weight_List(ids, prob, names)
    
    '''
    Based on the skill id, returns which area of the skillTable the skill belongs to as a String.
        Parameters:
            ind (Number): ID of the skill
        Returns:
            Area of the skillTable the skill belongs to as a String
    '''
    def determineSkillStructureByID(self, ind):
        if ind < 401:
            return 'Active'
        elif ind < 531:
            return 'Pasive'
        elif ind < 801:
            return 'Innate'
        else:
            return 'Active'

    '''
    Writes the data from overlapCopies to the buffer, so that it can be used as the basis for future randomization.
        Paramters:
            overlapCopies (Duplicate): data from the overlapping demons and which dummy demon should get their data
            buffer (Table): buffer containing demon data
    '''
    def writeOverlapCopiesToBuffer(self, overlapCopies, buffer):
        compStart = 0x59
        enemyStart = 0x88139
        for overlap in overlapCopies:
            for i, word in enumerate(overlap.compData):
               buffer.writeWord(word,compStart + overlap.ind * 0x1D0 + i * 4)
            for i, word in enumerate(overlap.enemyData):
               buffer.writeWord(word,enemyStart + overlap.ind * 0x170 + i * 4)
        return buffer

    '''
    Write the values in newComp to the respective locations in the buffer
        Parameters:
            buffer (Table): Buffer of the Demon Table
            newComp (Array): Array containing data for all usable demons
        Returns
            The updated buffer
    '''
    def updateCompendiumBuffer(self, buffer, newComp):
        for demon in newComp:
            buffer.writeWord(demon.nameID,demon.offsetNumbers['nameID'])
            buffer.writeWord(demon.descriptionID,demon.offsetNumbers['descriptionID'])
            #Write stats of the demon to the buffer
            buffer.writeWord(demon.stats.HP.start,demon.offsetNumbers['HP'] + 4 * 0)
            buffer.writeWord(demon.stats.MP.start,demon.offsetNumbers['HP'] + 4 * 1)
            buffer.writeWord(demon.stats.str.start,demon.offsetNumbers['HP'] + 4 * 4)
            buffer.writeWord(demon.stats.vit.start,demon.offsetNumbers['HP'] + 4 * 5)
            buffer.writeWord(demon.stats.mag.start,demon.offsetNumbers['HP'] + 4 * 6)
            buffer.writeWord(demon.stats.agi.start,demon.offsetNumbers['HP'] + 4 * 7)
            buffer.writeWord(demon.stats.luk.start,demon.offsetNumbers['HP'] + 4 * 8)
            #Write stat growths of the demon to the buffer
            buffer.writeWord(demon.stats.HP.growth,demon.offsetNumbers['HP'] + 4 * 2)
            buffer.writeWord(demon.stats.MP.growth,demon.offsetNumbers['HP'] + 4 * 3)
            buffer.writeWord(demon.stats.str.growth,demon.offsetNumbers['HP'] + 4 * 9)
            buffer.writeWord(demon.stats.vit.growth,demon.offsetNumbers['HP'] + 4 * 10)
            buffer.writeWord(demon.stats.mag.growth,demon.offsetNumbers['HP'] + 4 * 11)
            buffer.writeWord(demon.stats.agi.growth,demon.offsetNumbers['HP'] + 4 * 12)
            buffer.writeWord(demon.stats.luk.growth,demon.offsetNumbers['HP'] + 4 * 13)
            #Write the id of the demons skills to the buffer
            for index, skill in enumerate(demon.skills):
                buffer.writeWord(skill.ind, demon.offsetNumbers['firstSkill'] + 4 * index)
            #Write the id and levels of the demons learnable skills to the buffer
            for index, skill in enumerate(demon.learnedSkills):
                buffer.writeWord(skill.ind, demon.offsetNumbers['firstLearnedLevel'] + 8 * index + 4)
                buffer.writeWord(skill.level, demon.offsetNumbers['firstLearnedLevel'] + 8 * index)
            for index in range(len(demon.learnedSkills),12 - len(demon.learnedSkills)):
                buffer.writeWord(0, demon.offsetNumbers['firstLearnedLevel'] + 8 * index + 4)
                buffer.writeWord(0, demon.offsetNumbers['firstLearnedLevel'] + 8 * index)
            #Write various attributes of the demon to the buffer
            buffer.writeWord(demon.level.value, demon.offsetNumbers['level'])
            buffer.writeByte(demon.race.value, demon.offsetNumbers['race'])
            buffer.writeByte(demon.tendency, demon.offsetNumbers['alignment'])
            buffer.writeByte(demon.alignment, demon.offsetNumbers['alignment'] + 1)
            buffer.writeWord(demon.innate.value, demon.offsetNumbers['innate'])
            buffer.writeHalfword(demon.fusability, demon.offsetNumbers['fusability'])
            buffer.writeByte(demon.unlockFlags[0], demon.offsetNumbers['unlockFlags'])
            buffer.writeByte(demon.unlockFlags[1], demon.offsetNumbers['unlockFlags'] +1)
            buffer.writeByte(demon.tone.value, demon.offsetNumbers['tone'])
            buffer.writeByte(demon.tone.secondary, demon.offsetNumbers['tone'] + 1)
            buffer.writeWord(demon.preventDeletionFlag,demon.offsetNumbers['encounterSpawn'] -8 )
            buffer.writeWord(demon.creationSpawn.mapNameID,demon.offsetNumbers['encounterSpawn'] )
            buffer.writeWord(demon.creationSpawn.zoneNameID,demon.offsetNumbers['encounterSpawn'] +4)
            buffer.writeWord(demon.vengeanceSpawn.mapNameID,demon.offsetNumbers['encounterSpawn'] +8)
            buffer.writeWord(demon.vengeanceSpawn.zoneNameID,demon.offsetNumbers['encounterSpawn'] +12)
            buffer.writeWord(demon.compCostModifier,demon.offsetNumbers['firstSkill'] -12)
            #write potentials
            buffer.writeWord(demon.potential.physical, demon.offsetNumbers['potential'] + 4 * 0)
            buffer.writeWord(demon.potential.fire, demon.offsetNumbers['potential'] + 4 * 1)
            buffer.writeWord(demon.potential.ice, demon.offsetNumbers['potential'] + 4 * 2)
            buffer.writeWord(demon.potential.elec, demon.offsetNumbers['potential'] + 4 * 3)
            buffer.writeWord(demon.potential.force, demon.offsetNumbers['potential'] + 4 * 4)
            buffer.writeWord(demon.potential.light, demon.offsetNumbers['potential'] + 4 * 5)
            buffer.writeWord(demon.potential.dark, demon.offsetNumbers['potential'] + 4 * 6)
            buffer.writeWord(demon.potential.almighty, demon.offsetNumbers['potential'] + 4 * 7)
            buffer.writeWord(demon.potential.ailment, demon.offsetNumbers['potential'] + 4 * 8)
            buffer.writeWord(demon.potential.support, demon.offsetNumbers['potential'] + 4 * 9)
            buffer.writeWord(demon.potential.recover, demon.offsetNumbers['potential'] + 4 * 10)
            #write resists
            buffer.writeWord(demon.resist.physical.value, demon.offsetNumbers['innate']+ 4 * 1)
            buffer.writeWord(demon.resist.fire.value, demon.offsetNumbers['innate']+ 4 * 2)
            buffer.writeWord(demon.resist.ice.value, demon.offsetNumbers['innate']+ 4 * 3)
            buffer.writeWord(demon.resist.elec.value, demon.offsetNumbers['innate']+ 4 * 4)
            buffer.writeWord(demon.resist.force.value, demon.offsetNumbers['innate']+ 4 * 5)
            buffer.writeWord(demon.resist.light.value, demon.offsetNumbers['innate']+ 4 * 6)
            buffer.writeWord(demon.resist.dark.value, demon.offsetNumbers['innate']+ 4 * 7)
            buffer.writeWord(demon.resist.poison.value, demon.offsetNumbers['innate']+ 4 * 9)
            buffer.writeWord(demon.resist.confusion.value, demon.offsetNumbers['innate']+ 4 * 11)
            buffer.writeWord(demon.resist.charm.value, demon.offsetNumbers['innate']+ 4 * 12)
            buffer.writeWord(demon.resist.sleep.value, demon.offsetNumbers['innate']+ 4 * 13)
            buffer.writeWord(demon.resist.seal.value, demon.offsetNumbers['innate']+ 4 * 14)
            buffer.writeWord(demon.resist.mirage.value, demon.offsetNumbers['innate']+ 4 * 21)
        return buffer
    
    '''
    Write the values in fusions to the respective locations in the buffer
        Parameters:
            buffer (Table): Buffer of the normal fusion table
            fusions (Array): contains data for all possible normal fusions
        Returns:
            The updated buffer
    '''
    def updateNormalFusionBuffer(self, buffer, fusions):
        for fusion in fusions:
            buffer.writeWord(fusion.firstDemon.value, fusion.offsetNumbers['firstDemon'])
            buffer.writeWord(fusion.secondDemon.value, fusion.offsetNumbers['secondDemon'])
            buffer.writeWord(fusion.result.value, fusion.offsetNumbers['result'])
        return buffer
    
    '''
    Write the values in fusions to the respective locations in the buffer
        Parameters:
            buffer (Table): Buffer of the other fusion table
            fusions (Array): contains data for all possible special fusions
        Returns:
            The updated buffer
    '''
    def updateOtherFusionBuffer(self, buffer, fusions):
        for index,fusion in enumerate(fusions):
            buffer.writeHalfword(index, fusion.baseOffset)
            buffer.writeHalfword(fusion.demon1.value, fusion.baseOffset + 2)
            buffer.writeHalfword(fusion.demon2.value, fusion.baseOffset + 4)
            buffer.writeHalfword(fusion.demon3.value, fusion.baseOffset + 6)
            buffer.writeHalfword(fusion.demon4.value, fusion.baseOffset + 8)
            buffer.writeHalfword(fusion.result.value, fusion.baseOffset + 10)
        return buffer
    '''
    Write the values in mapSymbolArr to the respective locations in the buffer
        Parameters:
            buffer (Table): Buffer of the other mapSymbolParam table
        Returns:
            The updated buffer
    '''
    def updateMapSymbolBuffer(self,buffer):
        for mapDemon in self.mapSymbolArr:
            offsets = mapDemon.offsetNumbers
            buffer.writeWord(mapDemon.demonID, offsets['demonID'])
            buffer.writeFloat(mapDemon.walkSpeed, offsets['walkSpeed'])
            buffer.writeFloat(mapDemon.scaleFactor, offsets['scaleFactor'])

            buffer.writeFloat(mapDemon.encountCollision.x, offsets['encountCollisionX'])
            buffer.writeFloat(mapDemon.encountCollision.y, offsets['encountCollisionY'])
            buffer.writeFloat(mapDemon.encountCollision.z, offsets['encountCollisionZ'])
        return buffer

    '''
    Write the values in foes to the respective locations in the buffer
        Parameters:
            buffer (Table): Buffer of the NKMBBase table
            foes (Array): Contains data on all basic enemies
        Returns:
            The updated buffer
    '''
    def updateBasicEnemyBuffer(self, buffer, foes):
        for foe in foes:
            offsets = foe.offsetNumbers
            buffer.writeWord(foe.nameID,offsets['nameID'])
            #Write stats of the enemy demon to the buffer
            buffer.writeWord(foe.stats.HP, offsets['HP'] + 4 * 0)
            buffer.writeWord(foe.stats.MP,offsets['HP'] + 4 * 1)
            buffer.writeWord(foe.stats.str,offsets['HP'] + 4 * 2)
            buffer.writeWord(foe.stats.vit,offsets['HP'] + 4 * 3)
            buffer.writeWord(foe.stats.mag,offsets['HP'] + 4 * 4)
            buffer.writeWord(foe.stats.agi,offsets['HP'] + 4 * 5)
            buffer.writeWord(foe.stats.luk,offsets['HP'] + 4 * 6)
            buffer.writeByte(foe.analyze, offsets['HP'] + 28)

            buffer.writeWord(foe.level, offsets['level'])
            buffer.writeByte(foe.pressTurns, offsets['pressTurns'])
            buffer.writeWord(foe.damageMultiplier, offsets['pressTurns'] + 9)
            for index, skill in enumerate(foe.skills):
                buffer.writeWord(skill.ind, offsets['firstSkill'] + 4 * index)
            buffer.writeWord(foe.experience, offsets['experience'])
            buffer.writeWord(foe.money, offsets['experience'] + 4)
            buffer.writeWord(foe.AI, offsets['experience'] + 12)
            buffer.writeByte(foe.recruitable, offsets['HP'] + 33)
            buffer.writeByte(foe.levelDMGCorrection, offsets['HP'] + 30)
            buffer.writeWord(foe.innate.value, offsets['innate'])
            buffer.writeByte(foe.instakillRate, offsets['item'] - 1)

            #write item drops
            buffer.writeWord(foe.drops.item1.value, offsets['item'])
            buffer.writeWord(foe.drops.item1.chance, offsets['item'] + 4)
            buffer.writeWord(foe.drops.item1.quest, offsets['item'] + 8)
            buffer.writeWord(foe.drops.item2.value, offsets['item'] +12)
            buffer.writeWord(foe.drops.item2.chance, offsets['item'] + 16)
            buffer.writeWord(foe.drops.item2.quest, offsets['item'] + 20)
            buffer.writeWord(foe.drops.item3.value, offsets['item'] +24)
            buffer.writeWord(foe.drops.item3.chance, offsets['item'] + 28)
            buffer.writeWord(foe.drops.item3.quest, offsets['item'] + 32)

            buffer.writeWord(foe.potential.physical,offsets['potential'] + 4 * 0)
            buffer.writeWord(foe.potential.fire,offsets['potential'] + 4 * 1)
            buffer.writeWord(foe.potential.ice,offsets['potential'] + 4 * 2)
            buffer.writeWord(foe.potential.elec,offsets['potential'] + 4 * 3)
            buffer.writeWord(foe.potential.force,offsets['potential'] + 4 * 4)
            buffer.writeWord(foe.potential.light,offsets['potential'] + 4 * 5)
            buffer.writeWord(foe.potential.dark,offsets['potential'] + 4 * 6)
            buffer.writeWord(foe.potential.almighty,offsets['potential'] + 4 * 7)
            buffer.writeWord(foe.potential.ailment,offsets['potential'] + 4 * 8)
            buffer.writeWord(foe.potential.recover,offsets['potential'] + 4 * 10)
            buffer.writeWord(foe.potential.support,offsets['potential'] + 4 * 9)

            buffer.writeWord(foe.resist.physical.value, offsets['innate']+ 4 * 1)
            buffer.writeWord(foe.resist.fire.value, offsets['innate']+ 4 * 2)
            buffer.writeWord(foe.resist.ice.value, offsets['innate']+ 4 * 3)
            buffer.writeWord(foe.resist.elec.value, offsets['innate']+ 4 * 4)
            buffer.writeWord(foe.resist.force.value, offsets['innate']+ 4 * 5)
            buffer.writeWord(foe.resist.light.value, offsets['innate']+ 4 * 6)
            buffer.writeWord(foe.resist.dark.value, offsets['innate']+ 4 * 7)
            buffer.writeWord(foe.resist.poison.value, offsets['innate']+ 4 * 9)
            buffer.writeWord(foe.resist.confusion.value, offsets['innate']+ 4 * 11)
            buffer.writeWord(foe.resist.charm.value, offsets['innate']+ 4 * 12)
            buffer.writeWord(foe.resist.sleep.value, offsets['innate']+ 4 * 13)
            buffer.writeWord(foe.resist.seal.value, offsets['innate']+ 4 * 14)
            buffer.writeWord(foe.resist.mirage.value, offsets['innate']+ 4 * 21)
        return buffer
    
    '''
    Write the values in symbolArr to the respective locations in the buffer, as well as updated boss encounters
        Parameters:
            buffer (Table): Buffer of the EncountData table
            symbolArr (Array): contains data on all symbol encounters and their encounter battles
        Returns:
            The updated buffer
    '''
    def updateEncounterBuffer(self, buffer, symbolArr, encountArr):
        #For each overworld encounter
        for symbolEntry in symbolArr:
            offsets = symbolEntry.offsetNumbers
            buffer.writeHalfword(symbolEntry.symbol.ind, offsets['symbol'])
            #go through its list of encounter battles
            # for encounterEntry in symbolEntry.encounters:
            #     enc = encounterEntry.encounter
            #     encOffsets = enc.offsetNumbers
            #     #and write the data for every demon
            #     for index, demon in enumerate(enc.demons):
            #         buffer.writeHalfword(demon, encOffsets['demon'] + 2 * index)
        for encounterEntry in encountArr:
                encOffsets = encounterEntry.offsetNumbers
                #and write the data for every demon
                buffer.writeByte(encounterEntry.track, encOffsets['track'])
                for index, demon in enumerate(encounterEntry.demons):
                    buffer.writeHalfword(demon, encOffsets['demon'] + 2 * index)
        for bossEncounter in self.updatedNormalEncounters:
            enc = self.encountArr[bossEncounter]
            encOffsets = enc.offsetNumbers
            #and write the data for every demon
            buffer.writeByte(enc.track, encOffsets['track'])
            for index, demon in enumerate(enc.demons):
                buffer.writeHalfword(demon, encOffsets['demon'] + 2 * index)
        return buffer
    
    '''
    Writes the values from the naho object to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            naho (Nahobino) 
    '''
    def updateMCBuffer(self, buffer, naho):
        offsets = naho.offsetNumbers
        buffer.writeWord(naho.startingSkill,offsets['startingSkill'])
        buffer.writeWord(naho.innate,offsets['innate'])
        for index,level in enumerate(naho.stats):
            buffer.writeWord(level.HP, 0x1685 + 0x1C * index + 4 * 0)
            buffer.writeWord(level.MP, 0x1685 + 0x1C * index + 4 * 1)
            buffer.writeWord(level.str, 0x1685 + 0x1C * index + 4 * 2)
            buffer.writeWord(level.vit, 0x1685 + 0x1C * index + 4 * 3)
            buffer.writeWord(level.mag, 0x1685 + 0x1C * index + 4 * 4)
            buffer.writeWord(level.agi, 0x1685 + 0x1C * index + 4 * 5)
            buffer.writeWord(level.luk, 0x1685 + 0x1C * index + 4 * 6)
        
        buffer.writeWord(naho.resist.physical.value,offsets['affStart'] + 4 * 0 )
        buffer.writeWord(naho.resist.fire.value,offsets['affStart'] + 4 * 1 )
        buffer.writeWord(naho.resist.ice.value,offsets['affStart'] + 4 * 2 )
        buffer.writeWord(naho.resist.elec.value,offsets['affStart'] + 4 * 3 )
        buffer.writeWord(naho.resist.force.value,offsets['affStart'] + 4 * 4 )
        buffer.writeWord(naho.resist.light.value,offsets['affStart'] + 4 * 5 )
        buffer.writeWord(naho.resist.dark.value,offsets['affStart'] + 4 * 6 )
        buffer.writeWord(naho.resist.almighty.value,offsets['affStart'] + 4 * 7 )
        buffer.writeWord(naho.resist.poison.value,offsets['affStart'] + 4 * 8 )
        buffer.writeWord(naho.resist.confusion.value,offsets['affStart'] + 4 * 10 )
        buffer.writeWord(naho.resist.charm.value,offsets['affStart'] + 4 * 11)
        buffer.writeWord(naho.resist.sleep.value,offsets['affStart'] + 4 * 12 )
        buffer.writeWord(naho.resist.seal.value,offsets['affStart'] + 4 * 13 )
        buffer.writeWord(naho.resist.mirage.value,offsets['affStart'] + 4 * 20 )
        
        return buffer

    '''
    Writes the values from the essences to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            essence (Array) 
    '''
    def updateEssenceData(self,buffer,essence):
        for e in essence:
            offset = e.offset
            buffer.writeWord(e.price, offset +12)
        return buffer

    '''
    Writes the values from the consumable items to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            consumables (Array) 
    '''
    def updateConsumableData(self, buffer, consumables):
        for index, item in enumerate(consumables):
            if index == 0:
                continue #skip dummy item
            buffer.writeWord(item.buyPrice, item.offset + 0x5C)
        return buffer

    '''
    Writes the values from the shop entries to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            entries (Array) 
    '''
    def updateShopBuffer(self, buffer, entries, mimans):
        for entry in entries:
            buffer.writeHalfword(entry.item.value, entry.offset)
            buffer.writeDblword(entry.unlock.value, entry.offset + 4)
        for reward in mimans:
            buffer.writeWord(reward.miman,reward.offset)
            buffer.writeWord(reward.setMsgID, reward.offset +4)
            for index, item in enumerate(reward.items):
                buffer.writeHalfword(item.ind, reward.offset + 8 + 4*index)
                buffer.writeHalfword(item.amount, reward.offset + 10 + 4*index)
        return buffer

    '''
    Writes the values from the event encounter array to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            evEncount (Array)
    '''
    def updateEventEncountBuffer(self,buffer,evEncount, uassetBuffer):
        sizeWord = buffer.readWord(0x10)
        totalSize = buffer.readWord(0x39)
        
        for ind, enc in enumerate(evEncount):
            #print(str(ind) + ": (" + str(enc.demons[0].value) + ") " + self.enemyNames[enc.demons[0].value] + " " + str(enc.track) + " NEXT: " + str(enc.nextEnc))
            if ind >= 253:
                for i in range (0,96,4):
                    buffer.buffer.insert(-16,0)
                    buffer.buffer.insert(-16,0)
                    buffer.buffer.insert(-16,0)
                    buffer.buffer.insert(-16,0)
                totalSize = totalSize + 96
                sizeWord = sizeWord + 96
            buffer.writeByte(enc.ind, enc.offsets['23Flag']-3)
            buffer.writeByte(enc.unknown23Flag, enc.offsets['23Flag'])
            buffer.writeByte(enc.battlefield, enc.offsets['battlefield'])
            buffer.writeHalfword(enc.track, enc.offsets['track'])
            buffer.write32chars(enc.levelpath, enc.offsets['levelpath'])
            buffer.writeHalfword(enc.unknownDemon.value, enc.offsets['unknownDemon'])
            buffer.writeByte(enc.endEarlyFlag,enc.offsets['levelpath'] + 0x3A)
            buffer.writeByte(enc.startingPhase,enc.offsets['startingPhase'])
            for index, demon in enumerate(enc.demons):
                buffer.writeHalfword(demon.value , enc.offsets['demons'] + 2 * index)
        
        buffer.writeWord(totalSize, 0x39)
        buffer.writeWord(sizeWord,0x10)
        buffer.writeWord(sizeWord -4, 0x21)
        uassetBuffer.writeWord(totalSize + 0x51, 0x251)
            
            
        return buffer
        
    '''
    Writes the position values from an event encouter or encounter array to their respective locations in the table uasset.
        Parameters:        
            file (General_UAsset): uasset file to overwrite positions in
            encountArr (List()): list of encounters to get the new positions from
    '''
    def updateEncountPostFile(self,file: General_UAsset,encountArr):
        encounterPositions = file.json['Exports'][0]['Table']['Data']
        for ind, enc in enumerate(encountArr):
            if ind >= len(encounterPositions):
                continue
            currentEncount = encounterPositions[ind]['Value']
            postArray = currentEncount[2]['Value']
            for index, pos in enumerate(enc.positions.demons):
                post = postArray[index]['Value'][0]['Value']
                post['X'] = pos.x
                post['Y'] = pos.y
            addPostArray = currentEncount[3]['Value']
            for index, pos in enumerate(enc.positions.addDemons):
                post = addPostArray[index]['Value'][0]['Value']
                post['X'] = pos.x
                post['Y'] = pos.y

        file.write()
        file = None
            

    '''
    Writes the values from the boss flag array to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
    '''
    def updateBossFlagBuffer(self,buffer):
        for bossFlags in self.bossFlagArr:
            buffer.writeHalfword(bossFlags.demonID, bossFlags.offset)
            for index in range(6):
                buffer.writeByte(bossFlags.flags[index], bossFlags.offset + 4 * (index + 1))
        return buffer
    
    '''
    Writes the values from the battle event array to their respective locations in the table buffer and increases the file size if necessary.
        Parameters:        
            buffer (Table)
            data (Array)
    '''
    def updateBattleEventsBuffer(self, buffer, data, uassetBuffer):
        #print(len(data))
        if len(data) > 36:
            sizeWord = buffer.readWord(0x10)
            

            totalSize = buffer.readWord(0x39)

            for index, event in enumerate(data):
                if index >= 36:
                    entry = []
                    for i in range (0,0x50,4):
                        entry.append(buffer.readWord(data[event.referenceID].offset + i))
                    for i, value in enumerate(entry):
                        buffer.buffer.insert(-16,0)
                        buffer.buffer.insert(-16,0)
                        buffer.buffer.insert(-16,0)
                        buffer.buffer.insert(-16,0)
                        buffer.writeWord(value,totalSize + 0x45 + i * 4)
                    totalSize = totalSize + 0x50
                    sizeWord = sizeWord + 0x50
            buffer.writeWord(totalSize, 0x39)
            buffer.writeWord(sizeWord,0x10)
            buffer.writeWord(sizeWord -4, 0x21)
            self.updateBattleEventUasset(uassetBuffer, totalSize + 0x51)
        for event in data:
            buffer.writeByte(event.encounterID, event.offset + 0x20)

        return buffer
    
    '''
    Updates the value for the size of the EventBattleTable.uexp in the buffer referring to the EventBattleTable.uasset.
    '''
    def updateBattleEventUasset(self, buffer, newSize):
        #updated = buffer.readWord(0x25A)+increase
        buffer.writeWord(newSize ,0x25A)

    '''
    Writes certain values from the devil asset array to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            data (List(Asset_Entry))
    '''
    def updateDevilAssetBuffer(self, buffer, data):
        for index, entry in enumerate(data):
            #buffer.writeWord(entry.demonID,entry.locations['demon'])
            buffer.writeWord(entry.classAssetID,entry.locations['classAssetID'])
            buffer.writeWord(entry.dmAssetID,entry.locations['DMAssetID'])
            buffer.writeWord(entry.validArea,entry.locations['validArea'])
            buffer.writeWord(entry.verticalMax,entry.locations['verticalMax'])
            buffer.writeWord(entry.horizontalMax,entry.locations['horizontalMax'])
            buffer.writeWord(entry.tallMax,entry.locations['tallMax'])
            for i in range(24):
                buffer.writeWord(entry.postChips[i],entry.locations['postChip'] + i *4)
        return buffer

    '''
    Writes certain values from the mission array to their respective locations in the table buffer
        Parameters:
            buffer (Table): buffer
            data (List(Mission)): list of missions
    '''
    def updateMissionBuffer(self,buffer,data):
        for mission in data:
            buffer.writeHalfword(mission.reward.amount, mission.offsets['rewardAmount'])
            buffer.writeHalfword(mission.reward.ind, mission.offsets['rewardID'])
            buffer.writeWord(mission.macca, mission.offsets['rewardMacca'])
            buffer.writeWord(mission.experience, mission.offsets['rewardMacca'] + 4)
            for i in range(4):
                buffer.writeWord(mission.conditions[i].type, mission.offsets['conditions'] + 0x10 * i)
                buffer.writeWord(mission.conditions[i].ind, mission.offsets['conditions'] + 0x10 * i + 4)
                buffer.writeWord(mission.conditions[i].amount, mission.offsets['conditions'] + 0x10 * i + 8)
        return buffer
    '''
    Writes certain values from the skill arrays to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            activeSkills (Array(Active_Skill))
            passiveSkills (Array(Passive_Skill))
    '''
    def updateSkillBuffer(self, buffer, activeSkills, passiveSkills, innates, fusionSkillReqs):
        for index,skill in enumerate(activeSkills):
            if index == 0:
                # skip filler entry
                continue
            buffer.writeWord(skill.owner.ind, skill.offsetNumber['owner'])
            buffer.write32chars(skill.animation, skill.offsetNumber['animation'])
            buffer.writeWord(skill.healing.flag, skill.offsetNumber['resistEnable'] + 8)
            buffer.writeByte(skill.healing.percent, skill.offsetNumber['resistEnable'] + 12)
            buffer.writeWord(skill.magatsuhi.race1.value, skill.offsetNumber['magatsuhiFlag'] + 1)
            buffer.writeWord(skill.magatsuhi.race2.value, skill.offsetNumber['magatsuhiFlag'] + 5)


        for skill in passiveSkills:
            buffer.writeWord(skill.owner.ind, skill.offsetNumber['owner'])


        for skill in innates:
            pass

        for skill in fusionSkillReqs:
            buffer.writeWord(skill.ind, skill.offset)
            for index,demonID in enumerate(skill.demons):
                buffer.writeWord(demonID, skill.offset + 8 + 4*index)
            for i,alignments in enumerate(skill.alignments):
                buffer.writeByte(alignments[0],skill.offset + 28 + i * 2)
                buffer.writeByte(alignments[1],skill.offset + 28 + i * 2 +1)
        
        return buffer

    '''
    Writes certain values from the devil ui list to their respective locations in the table buffer
        Parameters:
            buffer (Table): buffer
            data (List(UI_Entry)): list of ui entries
    '''
    def updateDevilUIBuffer(self, buffer, devilUITable):
        for entry in devilUITable:
            buffer.writeWord(entry.assetID, entry.offsetNumber['assetID'])
            buffer.write32chars(entry.assetString, entry.offsetNumber['assetString'])
        return buffer

    '''
    Writes certain values from the talk camera offset list to their respective locations in the table buffer
        Parameters:
            buffer (Table): buffer
            data (List(Talk_Camera_Offset_Entry)): list of talk camera offsets of demons
    '''
    def updateTalkCameraBuffer(self, buffer, data):
        for entry in data:
            buffer.writeFloat(entry.eyeOffset.x, entry.offsetNumber['eyeOffset'])
            buffer.writeFloat(entry.eyeOffset.y, entry.offsetNumber['eyeOffset'] + 29)
            buffer.writeFloat(entry.eyeOffset.z, entry.offsetNumber['eyeOffset'] + 29 * 2)
            buffer.writeFloat(entry.lookOffset.x, entry.offsetNumber['lookOffset'])
            buffer.writeFloat(entry.lookOffset.y, entry.offsetNumber['lookOffset'] + 29)
            buffer.writeFloat(entry.lookOffset.z, entry.offsetNumber['lookOffset'] + 29 * 2)
            buffer.writeFloat(entry.dyingOffset.x, entry.offsetNumber['dyingOffset'])
            buffer.writeFloat(entry.dyingOffset.y, entry.offsetNumber['dyingOffset'] + 29)
            buffer.writeFloat(entry.dyingOffset.z, entry.offsetNumber['dyingOffset'] + 29 * 2)
        return buffer


    '''
    Writes encounter and miracle information from the abscess array to their respective locations in the table buffer
        Parameters:
            buffer (Table): buffer
    '''
    def updateAbscessBuffer(self, buffer):
        for abscess in self.abscessArr:
            buffer.writeHalfword(abscess.encounter, abscess.offsetNumber['encounter'])
            buffer.writeByte(abscess.eventEncounter, abscess.offsetNumber['eventEncounter'])
            for i in range(6):
                buffer.writeByte(abscess.miracles[i], abscess.offsetNumber['miracles'] + i)
        return buffer
    
    '''
    Writes miracle updated costs from the miracle array to their respective locations in the table buffer
        Parameters:
            buffer (Table): buffer
    '''
    def updateMiracleBuffer(self, buffer):
        for miracle in self.miracleArr:
            if miracle.offsetNumber > 0: #Ignore Dummy miracle\
                buffer.writeByte(miracle.prerequisite, miracle.offsetNumber + 0x4)
                buffer.writeHalfword(miracle.cost, miracle.offsetNumber + 0xc)
        return buffer
    
    '''
    Writes updated punishing foe symbols and encounters from the unique symbol array to their respective locations in the table buffer
        Parameters:
            buffer (Table): buffer
    '''
    def updateUniqueSymbolBuffer(self, buffer):
        for uniqueSymbol in self.uniqueSymbolArr:
            buffer.writeHalfword(uniqueSymbol.encounterID, uniqueSymbol.offsetNumber['encounterID'])
            buffer.writeHalfword(uniqueSymbol.eventEncounterID, uniqueSymbol.offsetNumber['eventEncounterID'])
            buffer.writeHalfword(uniqueSymbol.symbol.value, uniqueSymbol.offsetNumber['symbol'])
        return buffer
    
    '''
    Writes updated chest rewards from the chest array to their respective locations in the table buffer
        Parameters:
            buffer (Table): buffer
    '''
    def updateChestBuffer(self, buffer):
        for chest in self.chestArr:
            buffer.writeHalfword(chest.item.value, chest.offsetNumber['item'])
            buffer.writeByte(chest.amount, chest.offsetNumber['amount'])
            buffer.writeWord(chest.macca, chest.offsetNumber['macca'])
        return buffer
    
    def updateMapEventBuffer(self, buffer):
        for event in self.mapEventArr:
            offset = event.offset
            buffer.writeWord(event.activationFlag, offset + 4)
            buffer.writeWord(event.compFlag1, offset + 0x14)
            buffer.writeWord(event.compFlag2, offset + 0x18)
        return buffer

    '''
    Writes updated demon navigator data to it's respective location in the table buffer
        Parameters:
            buffer (Table): buffer
    '''
    def updateNavigatorBuffer(self, buffer):
        for navi in self.navigatorArr:
            buffer.writeHalfword(navi.demonID, navi.offset)
            buffer.writeHalfword(navi.itemBonus, navi.offset + 2)
            buffer.writeByte(navi.itemType, navi.offset + 4)
            buffer.writeHalfword(navi.openFlag, navi.offset + 8)
        return buffer
    
    def updateVendingMachineBuffer(self,buffer):
        for vm in self.vendingMachineArr:
            offset = vm.offset
            for i, item in enumerate(vm.items):
                buffer.writeHalfword(item.ind, offset +8 + i * 4)
                buffer.writeByte(item.amount, offset +8 + 2+i * 4)
                buffer.writeByte(item.rate, offset +8 + 3+ i * 4)

        return buffer

    '''
    Check if a certain race of demons contains two demons of the same level
        Parameters:        
            comp (Array) 
    '''
    def checkRaceDoubleLevel(self, comp):
        raceLevels = ({'name': race, 'levels': []} for race in RACE_ARRAY)
        for demon in comp:
            if not demon.name.startswith("NOT USED"):
                raceLevels[demon.race.value - 1]['levels'].append(demon.level.value)
        print(raceLevels)
        
    '''
    Output the id of the demon with the given name to the console
        Parameters:
            name (String) 
            comp (Array) 
    '''
    def logDemonByName(self, name, comp):
        for demon in comp:
            if demon.name == name:
                print(demon)
                break
            
    '''
    Assign every demon a completely random level between 1 and 98.
    Also updates to the levels of the learnable skills to have the same difference as the in the original data when possible.
        Parameters:
            comp (Array): Array containing all demon data
        Returns:
            The demon data array with changed levels
    '''
    def assignCompletelyRandomLevels(self, comp):
        for element in comp:
            #Only up to 98 so level 99 demons can still learn their skills on a non godborn file
            newLevel = random.randInt(0, 98)
            for skill in element.learnedSkills:
                skillLevel = (skill.level - element.level.value) + newLevel
                if skillLevel > 99:
                    skillLevel = 99
                skill.level = skillLevel
            element.level.value = newLevel
        return comp

    '''
    Re-calculate the normal fusion result of every demon based on their race and level.
    In contrast to the normal game, does not remove fusion of two demons which also exist as ingredients to a special fusion
    Example: Normally Pixie + Angel does not create a normal fusion, since they are a special fusion for High Pixie. If their levels and races are unchanged they would result to Fortuna.
        Parameters:
            fusions (Array): The array of normal fusions to modify
            comp (Array): The array of demons 
    '''
    def adjustFusionTableToLevels(self, comp):
        normalFusionFile = General_UAsset("UniteCombineTable",paths.UNITE_COMBINE_TABLE_OUT)
        #Recreate the fusion array in its original form
        #Mostly as a way of testing 
        fusionCount = normalFusionFile.json['Exports'][0]['Data'][0]['Value'][0]['Value']
        fusionsData = normalFusionFile.json['Exports'][0]['Data'][1]['Value']
        fusions = []
        for entry in fusionsData:
            firstID = entry["Value"][0]["Value"]
            secondID = entry["Value"][1]["Value"]
            key = entry["Value"][2]["Value"]
            resultID = entry["Value"][3]["Value"]

            calculatedKey = firstID + secondID * 65536
            if calculatedKey != key:
                print("WRONG KEY CALCULATED")

            firstDemon = Translated_Value(firstID, comp[firstID].name)
            secondDemon = Translated_Value(secondID, comp[secondID].name)
            result = Translated_Value(resultID, comp[resultID].name)

            fusions.append(Normal_Fusion(None, firstDemon, secondDemon, result, key= calculatedKey))
        
        oldFusions = []
        for element in fusions:
            firstDemon = Translated_Value(element.firstDemon.value, comp[element.firstDemon.value].name)
            secondDemon = Translated_Value(element.secondDemon.value, comp[element.secondDemon.value].name)
            result = Translated_Value(element.result.value, comp[element.result.value].name)
            oldFusions.append(Normal_Fusion(None, firstDemon, secondDemon, result))

        raceTable = self.createRaceTables(comp)#lists of demon of each race in order
        specialFusions = self.listSpecialFusables() #list of demon IDs that cant be result


        #Filters out all demons that are obtainable via special fusion
        for index, race in enumerate(raceTable):
            newRace = list(filter(lambda demon: demon.ind not in specialFusions, race))
            raceTable[index] = newRace

        #Remove old Lilith as valid result. Index for Night is 31: Change this when implementing race rando
        raceTable[31].pop()

        #For each fusion...
        for fusion in fusions:
            demon1 = comp[fusion.firstDemon.value]
            demon2 = comp[fusion.secondDemon.value]
            demon1Race = demon1.race.value
            demon2Race = demon2.race.value
            #obtain the normal race of the resulting demon
            targetRace = next((val for x, val in enumerate(self.fusionChartArr) if (val.race1.value == demon1Race and val.race2.value == demon2Race) or (val.race1.value == demon2Race and val.race2.value == demon1Race)), None)
            #console.log(targetRace)
            #Check if the fusion results in a valid race && a demon of this race is available for fusion
            if targetRace and len(raceTable[targetRace.result.value]) > 0:
                #Check if the fusion results in an "Element"
                if RACE_ARRAY[targetRace.result.value] == "Element":
                    #Element fusions are doable by combining two demons of the same race
                    #Depending on the ingredients race, a different element is the result of the fusion
                    match RACE_ARRAY[demon1Race]:
                        case "Herald" | "Deity" | "Jaki" | "Kunitsu" | "Fallen" | "Snake" | "Tyrant" | "Drake":
                            fusion.result.value = self.elementals[0] #Flaemis id or replacements
                            fusion.result.translation = comp[self.elementals[0]].name
                        case "Megami" | "Vile" | "Avatar" | "Genma" | "Wilder" | "Femme" | "Brute" | "Haunt":
                            fusion.result.value = self.elementals[1] #Aquans id or replacements
                            fusion.result.translation = comp[self.elementals[1]].name
                        case "Avian" | "Divine" | "Yoma" | "Raptor" | "Holy" | "Fairy" | "Fury" | "Dragon":
                            fusion.result.value = self.elementals[2] #Aeros id or replacements
                            fusion.result.translation = comp[self.elementals[2]].name
                        case _:
                            fusion.result.value = self.elementals[3] #Erthrys id or replacements
                            fusion.result.translation = comp[self.elementals[3]].name
                else:
                    #if fusion is valid and targetRace is not element
                    #calculate the resulting demon and save it to the fusion
                    resultingDemon = self.determineNormalFusionResult(demon1.level.value, demon2.level.value, raceTable[targetRace.result.value])
                    fusion.result.value = resultingDemon.ind
                    fusion.result.translation = comp[resultingDemon.ind].name
            else:
                #if target race is not a valid fusion
                #first define what effects the element demons have on the result of each demon
                #Fusing elements with another demon results in a demon of the same race with either an decreased or increased base level
                #0 means unfusable, -1 reduces the level of the resulting demon, 1 increases it
                erthys = [0, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, 1, -1, -1, -1, 0, 0, 1, -1, 1, 0, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                aeros = [0, 0, -1, -1, 1, -1, 1, -1, 1, 0, -1, -1, -1, -1, -1, 0, 0, -1, 1, 1, 0, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                aquans = [0, 0, -1, 1, -1, 1, 1, 1, -1, 0, -1, -1, 1, -1, 1, 0, 0, 1, -1, -1, 0, -1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                flaemis = [0, 0, 1, -1, -1, 1, -1, -1, 1, 0, 1, -1, -1, 1, -1, 0, 0, -1, 1, -1, 0, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                #if the first demon ingredient is an element
                if demon1Race == 15:
                    #determine direction based on race of 2nd demon ingredient
                    direction = 0
                    if demon1.ind == self.elementals[3]:
                        direction = erthys[demon2Race]
                    elif demon1.ind == self.elementals[2]:
                            direction = aeros[demon2Race]
                    elif demon1.ind == self.elementals[1]:
                            direction = aquans[demon2Race]
                    elif demon1.ind == self.elementals[0]:
                            direction = flaemis[demon2Race]
                    foundResult = False
                    searchTable = raceTable[demon2Race] #sorted list of demons of a certain race sorted by ascending level
                    if direction > 0:
                        #Since we want to increase the level, start search at 0
                        for index, element in enumerate(searchTable):
                            if element.level.value > demon2.level.value and not foundResult:
                                fusion.result.value = element.ind
                                fusion.result.translation = element.name
                                foundResult = True
                        if not foundResult:
                            #if demon is highest level demon
                            fusion.result.value = 0
                            fusion.result.translation = "Empty"
                    elif direction < 0:
                        #Since we want to decrease the level, start search at end of array
                        for index, element in enumerate(searchTable[::-1]):
                            if element.level.value < demon2.level.value and not foundResult:
                                fusion.result.value = element.ind
                                fusion.result.translation = element.name
                                foundResult = True
                        if not foundResult:
                            #if demon is lowest level demon
                            fusion.result.value = 0
                            fusion.result.translation = "Empty"
                    else:
                        #if the second demon should not fusable with an element
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                elif demon2Race == 15:
                    #determine direction based on race of first demon ingredient
                    direction = 0
                    if demon2.ind == self.elementals[3]:
                        direction = erthys[demon1Race]
                    elif demon2.ind == self.elementals[2]:
                            direction = aeros[demon1Race]
                    elif demon2.ind == self.elementals[1]:
                            direction = aquans[demon1Race]
                    elif demon2.ind == self.elementals[0]:
                            direction = flaemis[demon1Race]
                    foundResult = False
                    searchTable = raceTable[demon1Race]
                    if direction > 0:
                        #Since we want to increase the level, start search at 0
                        for index, element in enumerate(searchTable):
                            if element.level.value > demon1.level.value and not foundResult:
                                fusion.result.value = element.ind
                                fusion.result.translation = element.name
                                foundResult = True
                        if not foundResult:
                            #f demon is highest level demon
                            fusion.result.value = 0
                            fusion.result.translation = "Empty"
                    elif direction < 0:
                        #Since we want to decrease the level, start search at end of array
                        for index, element in enumerate(searchTable[::-1]):
                            if element.level.value < demon1.level.value and not foundResult:
                                fusion.result.value = element.ind
                                fusion.result.translation = element.name
                                foundResult = True
                        if not foundResult:
                            #if demon is lowest level demon
                            fusion.result.value = 0
                            fusion.result.translation = "Empty"
                    else:
                        #if the second demon should not fusable with an element
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                else:
                    fusion.result.value = 0
                    fusion.result.translation = "Empty"
        self.printOutFusions(fusions)
        for index,fusion in enumerate(fusions):
            entry = fusionsData[index]

            entry["Value"][0]["Value"] = fusion.firstDemon.value
            entry["Value"][1]["Value"] = fusion.secondDemon.value
            if fusion.key > 0:
                entry["Value"][2]["Value"] = fusion.key
            entry["Value"][3]["Value"] = fusion.result.value
        normalFusionFile.write()
        normalFusionFile = None

    '''
    Adjusts the special fusions in specialFusionArr with the new fusions based on the randomization in shuffleLevel.
    Also sets the fusability flags accordingly.
        Parameters:
            fusions (Array) Array containing data on the new special fusions
            comp (Array) Array containing data on all playable demons
            expBuffer(Table): table for the special fusion buffer
    '''
    def adjustSpecialFusionTable(self,fusions,comp,expBuffer):
        self.specialFusionDemonIDs = []
        if len(fusions) > len(self.specialFusionArr):
            newEntries = len(fusions) - len(self.specialFusionArr)
            expBuffer = self.extendSpecialFusionTable(newEntries,expBuffer)

            startValue = 0xCC5
            fusionOffset = 0xC
            for index in range(newEntries): #add new special fusion dummies to array to replace with actual randomized data
                offset = startValue + (numbers.SPECIAL_FUSION_COUNT + index) * fusionOffset
                fusion = copy.deepcopy(self.specialFusionArr[0])
                fusion.ind = index + numbers.SPECIAL_FUSION_COUNT
                fusion.baseOffset = offset
                self.specialFusionArr.append(fusion)

        for index, fusion in enumerate(fusions):
            #Set original demons fusability to 0
            # seperate in case an og special fusion is still a special version
            replaced = self.specialFusionArr[index]
            comp[replaced.result.ind].fusability = 0 

        finalString = ""
        for index, fusion in enumerate(fusions):
            replaced = self.specialFusionArr[index]
            #Set new result demons fusability to 0
            comp[fusion.result.value].fusability = 257
            self.specialFusionDemonIDs.append(fusion.result.value)
            replaced.resultLevel = fusion.resultLevel
            replaced.demon1 = fusion.demon1
            replaced.demon2 = fusion.demon2
            replaced.demon3 = fusion.demon3
            replaced.demon4 = fusion.demon4
            replaced.result = fusion.result
        
            finalString = finalString + self.compendiumArr[fusion.demon1.value].name
            if fusion.demon2.value > 0:
                finalString = finalString + " + "+ self.compendiumArr[fusion.demon2.value].name
            if fusion.demon3.value > 0:
                finalString = finalString + " + " + self.compendiumArr[fusion.demon3.value].name
            if fusion.demon4.value > 0:
                finalString = finalString + " + " + self.compendiumArr[fusion.demon4.value].name
            finalString = finalString + "-> " + self.compendiumArr[fusion.result.value].name + "\n"
        
        with open(paths.FUSION_DEBUG, 'w', encoding="utf-8") as file:
            file.write("----- Special Fusions -----\n")
            file.write(finalString)
            file.write("----- Normal Fusions -----\n")
        return expBuffer

    '''
    Extend the special fusion table and write the corresponding uasset file
        Parameters:
            newEntries(Integer): how many entries should be added to the table
            expBuffer(Table): table for the special fusion buffer
    '''
    def extendSpecialFusionTable(self, newEntries, expBuffer):
        uassetBuffer = readBinaryTable(paths.UNITE_TABLE_UASSET_IN)
        additionalSize = 0xC * newEntries

        toUpdateInEXP = [0xCB9,0x45,0x49,0x4D,0x51,0x55,0x59,0x5D,0x21,0x10]

        for offset in toUpdateInEXP:
            old = expBuffer.readWord(offset)
            expBuffer.writeWord(old + additionalSize, offset)

        for j in range(additionalSize):
            expBuffer.buffer.insert(0xCC5 +numbers.SPECIAL_FUSION_COUNT * 0xC,0)

        toUpdateInUasset = [0x247,0xA9]
        for offset in toUpdateInUasset:
            old = uassetBuffer.readWord(offset)
            uassetBuffer.writeWord(old + additionalSize, offset)
        
        writeBinaryTable(uassetBuffer.buffer, paths.UNITE_TABLE_UASSET_OUT,paths.UNITE_FOLDER_OUT)

        return expBuffer
    
    '''
    Randomizes the races for all relevant demons in comp. Each race has at least 1 demon and makes sure all demons should still be fusable after level shuffling.
    Before randomizing races of all demons, decides 4 demons that are assigned as an element, that will be returned at the end.
    The distribution of races roughly follows the amount of times they appear as an result in the fusion chart.
    Parameters:
        comp List(Compendium_Demon): list of all compendium demons
    Returns: the ids of the 4 new demons of the Element race
    '''
    def randomizeRaces(self, comp):

        for demonInd in self.elementals:
            #Reset compendium costs for original elements
            comp[demonInd].compCostModifier = 100
        
        relevantDemons = [demon for demon in comp if demon.ind not in numbers.BAD_IDS and "Mitama" not in demon.name and not demon.name.startswith('NOT') ]

        raceAmounts = [ 0 for _ in range(len(RACE_ARRAY)) ] #Number of demons per Race
        raceResults = [ 0 for _ in range(len(RACE_ARRAY)) ] #How many fusion combinations result in this race
        elementals = [] 
        irrelevantRaces = [0,15,16] #Unused, Element, Mitama not relevant for Fusion Results

        for demon in relevantDemons:
            raceAmounts[demon.race.value] += 1
        for fusion in self.fusionChartArr:
            if not fusion.race1.value in irrelevantRaces and not fusion.race2.value in irrelevantRaces:
                raceResults[fusion.result.value] += 2
        baseRatios = []
        for index in range(len(RACE_ARRAY)):
            #Calculating ratio of number of demons to number of results for race in fusion
            value = 0
            if raceAmounts[index] > 0:
                value = raceResults[index] / raceAmounts[index]
            baseRatios.append(value)

        # New Randomized Information
        raceAssignments = [ 0 for _ in range(len(RACE_ARRAY)) ]
        newRatios = [0 for _ in range(len(RACE_ARRAY))]
        demonInds = []

        for index in range(4):
            #Decide Elementals
            demon = random.choice(relevantDemons)
            relevantDemons.remove(demon)
            demon.race = Translated_Value(15, "Element")
            demon.compCostModifier = 1000
            raceAssignments[15] += 1
            demonInds.append(demon.ind)
            elementals.append(demon.ind)
            comp[demon.ind] = demon #might be unneeded

        raceWeights = [int(value > 0)*10000 for value in baseRatios]
        raceWeights[15] = 0 #Elements have already been decided
        raceIndeces = [ i for i in range(len(RACE_ARRAY)) ]
        
        while len(relevantDemons) > 0:
            #Grab random race, that is valid to assign
            raceIndex = random.choices(raceIndeces, raceWeights)[0]
            if raceIndex == 0:
                continue
            if newRatios[raceIndex] == 0:
                #first assigned demon of race
                demon = random.choice(relevantDemons)
                relevantDemons.remove(demon)
                demon.race = Translated_Value(raceIndex, RACE_ARRAY[raceIndex])
                raceAssignments[raceIndex] += 1
                demonInds.append(demon.ind)
                newRatios[raceIndex] = raceResults[raceIndex] / raceAssignments[raceIndex]
                comp[demon.ind] = demon
                #Set weight to number of results to make some races more common
                raceWeights[raceIndex] = raceResults[raceIndex]
            elif raceResults[raceIndex] / (raceAssignments[raceIndex] + 1) < 2.5:
                #if assigning a new demon would put ratio too low set weights to 0
                raceWeights[raceIndex] = 0
            else:
                demon = random.choice(relevantDemons)
                relevantDemons.remove(demon)
                demon.race = Translated_Value(raceIndex, RACE_ARRAY[raceIndex])
                raceAssignments[raceIndex] += 1
                demonInds.append(demon.ind)
                newRatios[raceIndex] = raceResults[raceIndex] / raceAssignments[raceIndex]
                comp[demon.ind] = demon
            #print(str(demon.race.value) + "/" + demon.race.translation + " " +  demon.name)

        return elementals
    '''
    Randomizes the races for all relevant demons in comp. Each race has at least 1 demon and makes sure all demons are fusable by choosing races for
    10 base recruitable demons and then assembling the rest based on them. 
    Before randomizing races of all demons, decides 4 demons that are assigned as an element, that will be returned at the end.
    The distribution of races roughly follows the amount of times they appear as an result in the fusion chart.
    Parameters:
        comp List(Compendium_Demon): list of all compendium demons
        buffer(Table): table for the special fusion buffer
    Returns: the ids of the 4 new demons of the Element race
    '''
    def randomizeRacesFixedLevels(self, comp,buffer):

        for demonInd in self.elementals:
            #Reset compendium costs for original elements
            comp[demonInd].compCostModifier = 100

        relevantDemons = [demon for demon in comp if demon.ind not in numbers.BAD_IDS and "Mitama" not in demon.name and not demon.name.startswith('NOT') ]
        specialFusions = [demon.ind for demon in comp if demon.fusability > 256 and demon.tone.value != 0] #List of demon ids that are fused as a special fusion

        raceAmounts = [ 0 for _ in range(len(RACE_ARRAY)) ] #Number of demons per Race
        raceResults = [ 0 for _ in range(len(RACE_ARRAY)) ] #How many fusion combinations result in this race
        elementals = []
        irrelevantRaces = [0,15,16] #Unused, Element, Mitama not relevant for Fusion Results

        for demon in relevantDemons:
            raceAmounts[demon.race.value] += 1
        for fusion in self.fusionChartArr:
            if not fusion.race1.value in irrelevantRaces and not fusion.race2.value in irrelevantRaces:
                raceResults[fusion.result.value] += 2
        baseRatios = []
        for index in range(len(RACE_ARRAY)):
            #Calculating ratio of number of demons to number of results for race in fusion
            value = 0
            if raceAmounts[index] > 0:
                value = raceResults[index] / raceAmounts[index]
            baseRatios.append(value)

        # New Randomized Information
        raceAssignments = [ 0 for _ in range(len(RACE_ARRAY)) ]
        newRatios = [0 for _ in range(len(RACE_ARRAY))]
        demonInds = []

        for index in range(4):
            level = comp[self.elementals[index]].level.value
            demonsAtLevel = [demon for demon in relevantDemons if demon.level.value == level and demon.ind not in specialFusions]
            #Decide Elementals
            demon = random.choice(demonsAtLevel)
            relevantDemons.remove(demon)
            demon.race = Translated_Value(15, "Element")
            demon.compCostModifier = 1000
            raceAssignments[15] += 1
            demonInds.append(demon.ind)
            elementals.append(demon.ind)
            comp[demon.ind] = demon #might be unneeded
        
        raceWeights = [int(value > 0)*10000 for value in baseRatios]
        raceWeights[15] = 0 #Elements have already been decided
        raceIndeces = [ i for i in range(len(RACE_ARRAY)) ]

        #For each race build up new array with empty subarrays
        raceLevels = [ [] for _ in range(len(RACE_ARRAY)) ]

        base = [] #Will be the list of demons already assigned a race
        fusions = [] #Will be list of all possible fusions, regardless of if they actually result in an existing demon

        relevantDemons.sort(key = lambda demon: demon.level.value)
        index = 0
        #For the 10 lowest level demons (excluding the level 5 ones)
        while len(base) < 10:
            demon = relevantDemons[index]
            #get random race based on weight
            raceIndex = random.choices(raceIndeces, raceWeights)[0]
            if len(base) == 0 :
                #Remove chosen demon from future rounds
                relevantDemons.remove(demon)
                #set demons race to new race
                demon.race = Translated_Value(raceIndex, RACE_ARRAY[raceIndex])
                #increase race count by 1
                raceAssignments[raceIndex] += 1
                #add demon ind to list
                demonInds.append(demon.ind)
                #calculate new ratios
                newRatios[raceIndex] = raceResults[raceIndex] / raceAssignments[raceIndex]
                comp[demon.ind] = demon
                #add demon to base
                base.append(demon)
                # add level to the appropriate race level list
                raceLevels[demon.race.value].append(demon.level.value)
            elif (demon.level.value < 5 or 5 < demon.level.value) and demon.level.value not in raceLevels[raceIndex]:
                relevantDemons.remove(demon)
                #set demons race to new race
                demon.race = Translated_Value(raceIndex, RACE_ARRAY[raceIndex])
                #increase race count by 1
                raceAssignments[raceIndex] += 1
                #add demon ind to list
                demonInds.append(demon.ind)
                #calculate new ratios
                newRatios[raceIndex] = raceResults[raceIndex] / raceAssignments[raceIndex]
                comp[demon.ind] = demon
                #add fusions with demons already in base
                for b in base:
                    if(self.isValidFusion(demon,b)):
                        race1 = demon.race.translation
                        race2 = b.race.translation
                        target = next((f for x, f in enumerate(self.fusionChartArr) if (f.race1.translation == race1 and f.race2.translation == race2) or (f.race1.translation == race2 and f.race2.translation == race1)), None).result
                        dummy = Compendium_Demon()
                        dummy.ind = -1
                        dummy.name = "Fake"
                        dummy.race = target
                        dummy.level = Demon_Level(math.ceil((demon.level.value + b.level.value) / 2) +1, demon.level)
                        fusions.append([demon,b,dummy])
            
                #add demon to base
                base.append(demon)
                # add level to the appropriate race level list
                raceLevels[demon.race.value].append(demon.level.value)
            else:
                #skip level 5 demons due to Neko Shogun being unrecruitable 
                index += 1
            #Check if adding a demon would break ratios or set weight if first demon of race assigned
            for ratioIndex, ratio in enumerate(newRatios):
                if ratio == 0 and raceAssignments[ratioIndex] > 1:
                    raceWeights[ratioIndex] = raceResults[ratioIndex]
                elif raceResults[ratioIndex] / (raceAssignments[ratioIndex] + 1) < 2.5:
                    raceWeights[ratioIndex] = 0
        fusableDemonS = []
        #Check if demons in the base 10 can fuse into each other
        for b in base:
            possibleFusions = [f for f in fusions if f[2].race.translation == b.race.translation and f[2].ind == -1 and f[2].level.value <= b.level.value]
            for p in possibleFusions:
                p[2] = b
                fusableDemonS.append(b)

        attempts = 0
        #until no relevant demon left or no valid race assignment can be created
        while len(relevantDemons) > 0 and attempts < 300:
            # grab the next lowest level demon
            demon = relevantDemons[0]
            #Check which races can be assigned to the demon
            validRaces = list({fusion[2].race.value for fusion in fusions if fusion[2].ind == -1 and raceWeights[fusion[2].race.value] > 0 and fusion[2].level.value <= demon.level.value })
            validWeights = [weight for index, weight in enumerate(raceWeights) if index in validRaces]
            raceIndex = random.choices(validRaces,validWeights)[0] #random weighted race
            
            #Check if a demon of the same lavel is already assigned to race
            if demon.level.value in raceLevels[raceIndex]:
                attempts +=1
                continue
            #Check if demon is special fusion
            if demon.ind in specialFusions:
                raceIndex = random.choices(raceIndeces, raceWeights)[0]
                #Remove chosen demon from future rounds
                relevantDemons.remove(demon)
                #set demons race to new race
                demon.race = Translated_Value(raceIndex, RACE_ARRAY[raceIndex])
                #increase race count by 1
                raceAssignments[raceIndex] += 1
                #add demon ind to list
                demonInds.append(demon.ind)
                #calculate new ratios
                newRatios[raceIndex] = raceResults[raceIndex] / raceAssignments[raceIndex]
                comp[demon.ind] = demon
               
                #add fusions with demons already in base
                for b in base:
                    if(self.isValidFusion(demon,b)):
                        race1 = demon.race.translation
                        race2 = b.race.translation
                        target = next((f for x, f in enumerate(self.fusionChartArr) if (f.race1.translation == race1 and f.race2.translation == race2) or (f.race1.translation == race2 and f.race2.translation == race1)), None).result
                        dummy = Compendium_Demon()
                        dummy.ind = -1
                        dummy.name = "Fake"
                        dummy.race = target
                        dummy.level = Demon_Level(math.ceil((demon.level.value + b.level.value) / 2) +1, demon.level)
                        fusions.append([demon,b,dummy])
                #add demon to base
                base.append(demon)
                fusableDemonS.append(demon)
                # add level to the appropriate race level list
                raceLevels[demon.race.value].append(demon.level.value)
            else:
                #For all fusions that would result in demon and currently have dummy assigned, assign demon instead
                possibleFusions = [f for f in fusions if f[2].race.value == raceIndex and f[2].ind == -1 and f[2].level.value <= demon.level.value]
                for p in possibleFusions:
                    p[2] = demon
                if(len(possibleFusions) == 0):
                    # if no possible fusions exist, try again from start
                    attempts += 1
                    continue
                #Remove chosen demon from future rounds
                relevantDemons.remove(demon)
                #set demons race to new race
                demon.race = Translated_Value(raceIndex, RACE_ARRAY[raceIndex])
                #increase race count by 1
                raceAssignments[raceIndex] += 1
                #add demon ind to list
                demonInds.append(demon.ind)
                #calculate new ratios
                newRatios[raceIndex] = raceResults[raceIndex] / raceAssignments[raceIndex]
                comp[demon.ind] = demon
               
                #add fusions with demons already in base
                for b in base:
                    if(self.isValidFusion(demon,b)):
                        race1 = demon.race.translation
                        race2 = b.race.translation
                        target = next((f for x, f in enumerate(self.fusionChartArr) if (f.race1.translation == race1 and f.race2.translation == race2) or (f.race1.translation == race2 and f.race2.translation == race1)), None).result
                        dummy = Compendium_Demon()
                        dummy.ind = -1
                        dummy.name = "Fake"
                        dummy.race = target
                        dummy.level = Demon_Level(math.ceil((demon.level.value + b.level.value) / 2) +1, demon.level)
                        fusions.append([demon,b,dummy])
                #add demon to base
                base.append(demon)
                fusableDemonS.append(demon)
                # add level to the appropriate race level list
                raceLevels[demon.race.value].append(demon.level.value)
            #At end of while, check ratio eligibility for races and set their weights accordingly
            for ratioIndex, ratio in enumerate(newRatios):
                if ratio == 0 and raceAssignments[ratioIndex] > 1:
                    raceWeights[ratioIndex] = max(1,raceResults[ratioIndex] -raceAssignments[ratioIndex])
                elif raceResults[ratioIndex] / (raceAssignments[ratioIndex] + 1) < 2.5:
                    raceWeights[ratioIndex] = 0
        #do not continue if attempts elapse 300
        if attempts >= 300:
            print("Could not assign all races properly")
            return False
        
        notFusableCurrently = [demon for demon in base if demon not in fusableDemonS]
        #check if there isn't a fusion for current unfusable that was somehow missed
        for demon in notFusableCurrently:
            possibleFusions = [f for f in fusions if f[2].race.translation == demon.race.translation and f[2].ind == -1 and f[2].level.value <= demon.level.value]
            for p in possibleFusions:
                p[2] = demon
                fusableDemonS.append(demon)
        
        
        specialFusionDemonIDS = [comp[demon] for demon in specialFusions]
        specialFusions = []
        for demon in specialFusionDemonIDS:
            specialFusions.append(self.generateSpecialFusion(demon, [b for b in base if b.level.value < demon.level.value]))

        notFusableCurrently = [demon for demon in base if demon not in fusableDemonS and demon.race.translation in numbers.NO_DOWNFUSE_RACES]
        #for all other unfusables that also are not available via element fusion, add an extra special fusion
        for demon in notFusableCurrently:
            #print(demon.name + " " + str(demon.level.value))
            specialFusions.append(self.generateSpecialFusion(demon, [b for b in base if b.level.value < demon.level.value + 5 and b.level.value != demon.level.value]))
        
        buffer = self.adjustSpecialFusionTable(specialFusions,comp,buffer)

        return [elementals, buffer] 
        
    '''
    Randomize the tone of each playable demon that does not have a tone with talk data assigned.
        Parameters:
            comp (Array) Array containing data on all playable demons
    '''
    def assignTalkableTones(self, comp):
        workingTones = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19]
        for demon in comp:
            if 'Mitama' in demon.name or demon.ind in numbers.BAD_IDS:
                continue
            if demon.tone.value not in workingTones:
                if demon.ind in numbers.DEMON_HAUNT_QUESTGIVER_IDS:
                    demon.tone.value = 1 #Force a tone that functions in demon haunts, currently I only know tone 15 (Loup Garou) is broken
                else:
                    demon.tone.value = random.choice(workingTones)
            if demon.tone.secondary not in workingTones and demon.tone.secondary != 0:
                demon.tone.secondary = random.choice(workingTones)

    '''
    Adjusts the data of basic enemies to be in line with the data of playable demons.
    Each enemy has stat modifier based on the orignal enemy and player stats that is the applied to the new player stats.
    Skills are copied over from the player version as well as level. Level then is used to determine the new exp and macca values.
    Press Turns are random with a higher chance if the enemy originally had two.
        Parameters:
            enemies (Array(Enemy_Demon)): Array containing data on all basic enemies
            comp (Array(Compendium_Demon)): Array containing data on playable demons
        Returns:
            The array of basic enemies based on the data of playable demons
    '''
    def adjustBasicEnemyArr(self, enemies, comp):
        self.pressTurnChance = self.configSettings.pressTurnChance

        foes = []
        for index, enemy in enumerate(enemies):
            if 'Mitama' in enemy.name or index in numbers.BAD_IDS:
                foes.append(enemy)
                continue
            playableEqu = comp[index]
            #Copy level from player version
            newLevel = playableEqu.level.value
            #Based on original enemy and player version stats, later applied to replacement enemies
            statMods = Stats(enemy.stats.HP / playableEqu.stats.HP.og, enemy.stats.MP / playableEqu.stats.MP.og,  enemy.stats.str / playableEqu.stats.str.og,
                enemy.stats.mag / playableEqu.stats.mag.og, enemy.stats.vit / playableEqu.stats.vit.og,
                enemy.stats.agi / playableEqu.stats.agi.og, enemy.stats.luk / playableEqu.stats.luk.og)
            #new Stats just copies the values from the playable version, get adjusted later after it replacements are decided
            newStats = Stats(playableEqu.stats.HP.start, playableEqu.stats.MP.start, playableEqu.stats.str.start,
                playableEqu.stats.vit.start, playableEqu.stats.mag.start,
                playableEqu.stats.agi.start, playableEqu.stats.luk.start)
            newResist = copy.deepcopy(playableEqu.resist)
            newSkills = []
            for skill in playableEqu.skills:
                newID = skill.ind
                #Replace Healing Skills with enemy variant
                #if([97,98,100,101,266,909,279,855].includes(newID))
                if newID == 855:
                    newID = 856 #Sakuya Sakura
                elif newID == 909 or newID == 266:
                    newID = 887 #Suns Radiance
                elif newID == 270:
                    newID = 277 #Matriarchs Love
                elif newID == 101:
                    newID = 384 #Mediarama (Throne,Clotho)
                elif newID == 100:
                    newID = 383 #Media 
                elif newID == 98:
                    newID = 382 #Diarama
                elif newID == 97:
                    newID = 381 #Dia
                if skill.ind in numbers.MAGATSUHI_SKILLS:
                    try: #try to use enemy version of magatsuhi skill if possible
                        newID = numbers.MAGATSUHI_ENEMY_VARIANTS[skill.ind]
                    except KeyError:
                        pass
                skillName = translation.translateSkillID(newID, self.skillNames)
                newSkills.append(Translated_Value(newID, skillName))

                #check for resistance skills (those do not work on enemies) and apply resistance accordingly
                if skill.ind in numbers.RESIST_SKILLS.keys():
                    resistElement = numbers.RESIST_SKILLS[skill.ind][0]
                    value = numbers.RESIST_SKILLS[skill.ind][1]

                    oldValue = getattr(newResist, resistElement).value
                    if numbers.compareResistValues(oldValue,value) == 1: #if new value is smaller, use it
                        newResist.__setattr__(resistElement, Translated_Value(value,translation.translateResist(value)))



            newPressTurns = enemy.pressTurns
            if self.pressTurnChance != 0:
                newPressTurns = math.ceil(random.random() + (self.pressTurnChance * enemy.pressTurns))
            newExperience = self.expMod[newLevel]
            newMacca = self.maccaMod[newLevel]
            #In original data enemies with two press turns like Oni have multiplied EXP and Macca values
            if newPressTurns > 1:
                newExperience = newExperience * newPressTurns
                newMacca = newMacca * math.floor(newPressTurns * 1.5)
            #later overwritten for replacements
            newDrops = Item_Drops(enemy.drops.item1,enemy.drops.item2,enemy.drops.item3)
            
            newFoe = copy.deepcopy(enemy)
            #newFoe.ind = enemy.ind
            newFoe.name = playableEqu.name
            newFoe.nameID = playableEqu.nameID
            #newFoe.offsetNumbers = enemy.offsetNumbers
            newFoe.level = newLevel
            newFoe.originalLevel = enemy.level
            newFoe.stats = newStats
            newFoe.statMods = statMods
            newFoe.analyze = 1                   #I am not quite certain what this does, but all basic enemies in the original data have this
            newFoe.levelDMGCorrection = 1        #Influences damage calculation and also seems to be an requirement for recruitment
            newFoe.AI = 55                       #AI for random encounters
            newFoe.recruitable = 1               #Also required to be able to recruit the demon
            newFoe.pressTurns = newPressTurns
            newFoe.oldPressTurns = newPressTurns
            newFoe.damageMultiplier = 100
            newFoe.experience = newExperience
            newFoe.money = newMacca
            newFoe.skills = newSkills
            #newFoe.instakillRate = enemy.instakillRate
            newFoe.drops = newDrops
            newFoe.oldDrops = enemy.drops
            newFoe.innate = playableEqu.innate   #copy innate from player version
            newFoe.resist = newResist
            newFoe.potential = copy.deepcopy(playableEqu.potential)
            foes.append(newFoe)
        return foes
    
    '''
    Adjusts the data for all encounters and replaces the demons with demons around the same level.
        Parameters 
            symbolArr (Array(Encounter_Symbol)): Array of symbol encounters
            comp (Array(Compendium_Demon)): Array of all playable demons
            enemyArr (Array(Enemy_Demon)): Array of enemy counterparts for all playable demons
        Returns:
            The adjusted array of symbol encounters 
    '''
    def adjustEncountersToSameLevel(self, symbolArr, comp, enemyArr, encountArr):

        #will be in form [OG ID, NEW ID] #TODO: Rewrite this so it uses a dictionary in the first place
        replacements = []
        #Excluding unused, Old Lilith , Tao , Yoko, Mitama
        foes = list(filter(lambda e: e.ind not in numbers.BAD_IDS and 'Mitama' not in e.name and not e.name.startswith('NOT USED'), enemyArr))
        '''
        Returns the array of all enemies at the specified level
            Parameters:
                lv (Number): specified level
            Returns:
                Array of all enemies at the specified level
        '''
        def getEnemiesAtLevel(lv):
            return list(filter(lambda e: e.level == lv, foes))
        '''
        Returns the enemy with the specified id from the filtered enemy arrray
            Parameters:
                ind (Number): ID of enemy
                foes (Array(Enemy_Demon)): Array of enemy demons 
            Returns:
                The enemy with the specified id
        '''
        def getFoeWithID(ind, foes):
            return next(f for x, f in enumerate(foes) if f.ind == ind)

        #For every symbol encounter
        newSymbolArr = []
        for encount in symbolArr:
            #dont change symbol if unused, mitama, Old Lilith, Tao, Yoko or not an basic enemy
            if encount.symbol.ind in numbers.BAD_IDS  or encount.symbol.ind == 0 or encount.symbol.ind > numbers.NORMAL_ENEMY_COUNT or "Mitama" in encount.symbol.translation or encount.symbol.translation.startswith("NOT USED"):
                newSymbolArr.append(encount)
                continue
            replaceEnc = encount
            #ogEnc = copy.deepcopy(encount)
            symbolFoe = None
            currentLV = getFoeWithID(encount.symbol.ind, foes).originalLevel
            #get enemies at level which have not been featured as a replacement
            #ensures 1:1 replacement
            enemyAtLevel = getEnemiesAtLevel(currentLV)
            possibilities = [p for p in enemyAtLevel if not any(r[1] == p.ind for r in replacements)]
            '''
            Should not be needed with 1:1 replacements
            leeway = 1
            while not possibilities: #If no demons available try again at a different level
                possibilities = getEnemiesAtLevel(currentLV + random.randint(leeway * -1, leeway))
                leeway += 1
            '''
            #check if replacement for symbol already exists
            if not any(r[0] == encount.symbol.ind for r in replacements) and len(possibilities) > 0:#!replacements.some(r => r[0] == encount.symbol.ind)) {
                #if it doesnt generate random replacement
                enemy = random.choice(possibilities)

                replacements.append([encount.symbol.ind, enemy.ind])
                symbolFoe = enemy
            else:
                #if it does get replacement
                symbolFoe = getFoeWithID(next(r for x, r in enumerate(replacements) if r[0] == encount.symbol.ind)[1], foes)
            replaceEnc.symbol.ind = symbolFoe.ind
            replaceEnc.symbol.translation = symbolFoe.name
            #print("Replaced " + str(ogEnc.symbol.ind)  +" " +self.enemyNames[ogEnc.symbol.ind] + " with " + str(symbolFoe.ind)  +" " +symbolFoe.name + " at level " + str(currentLV))

            newSymbolArr.append(replaceEnc)

        
        replacementDict = {}
        for pair in replacements:
            replacementDict[pair[0]] = pair[1]

        for encount in encountArr:
            for index, demon in enumerate(encount.demons):
                if demon in replacementDict.keys():
                    encount.demons[index] = replacementDict[demon]


        #These need to be done before the we add the remaining demons so we know which demons cannot be encountered on the field
        self.adjustBasicEnemyDrops(replacementDict, enemyArr)
        self.adjustListedLocations(replacementDict, comp)

        for foe in foes:
            if foe.ind not in replacementDict.keys():#All demons that do not have a replacment yet
                currentLV = getFoeWithID(foe.ind, foes).originalLevel
                possibilities = [p for p in getEnemiesAtLevel(currentLV) if p.ind not in replacementDict.values()]
                enemy = random.choice(possibilities)
                replacementDict.update({foe.ind: enemy.ind})
         
        with open(paths.ENCOUNTERS_DEBUG, 'w', encoding="utf-8") as spoilerLog: #Create spoiler log
            for replaced, replacement in replacementDict.items():
                spoilerLog.write(self.enemyNames[replaced] + " replaced by " + self.getDemonsCurrentNameByID(replacement) + "\n")
            for replacement, replaced in self.guestReplacements.items():
                spoilerLog.write(self.enemyNames[replaced] + " swapped with " + self.enemyNames[replacement] + "\n") #Use enemy names hre since we need the old name
                  
        self.encounterReplacements = replacementDict


        self.adjustBasicEnemyStats(replacementDict, enemyArr)
        
        self.missionArr = self.adjustMissionsRequiringNormalDemons(replacementDict,enemyArr, self.missionArr)
        
        return newSymbolArr
    
    '''
    Based on the given pairs of replacements, moves item drops from the old to the new demon, while changing the essence to the
    new one. Also removes all drops from now non-encounterable demons.
        Parameters:
            replacements(List) list of pairs of demons [OGID, NEWID]
            foes(Array) containing all enemies
    '''
    def adjustBasicEnemyDrops(self, replacements, foes):
        for replacedID, replacementID in replacements.items():
            replaced = foes[replacedID]
            replacement = foes[replacementID]
            # for every pair of replacements copy item drops from replaced to replacement
            replacement.drops = Item_Drops(replaced.oldDrops.item1,replaced.oldDrops.item2,replaced.oldDrops.item3)
            #print(pair)
            #print("Replacement: " + replacement.name + " Replaced: " + replaced.name)

            #Adjust essence to belong to the replacement demon
            if "Essence" in replacement.drops.item2.translation:
                item = next(e for e in self.essenceArr if replacement.ind == e.demon.value)

                replacement.drops.item2.value = item.ind
                replacement.drops.item2.translation = item.name
            if "Essence" in replacement.drops.item3.translation:
                item = next(e for e in self.essenceArr if replacement.ind == e.demon.value)

                replacement.drops.item3.value = item.ind
                replacement.drops.item3.translation = item.name
        
        #TODO: Does this still work with Dictionary to delete overworld? Maybe rethink this in general
        replacedList = replacements.values()
        nonEncounter = [f for f in foes if f.ind not in replacedList and 'Mitama' not in f.name]
        # Delete item drops for demon who cannot be encountered on overworld
        for n in nonEncounter:
            #print(n.name)
            emptyItem = Item_Drop(0,"",0,0)
            n.drops = Item_Drops(emptyItem,emptyItem,emptyItem)
    

    '''
    Adjust the stats and listed locations of the enemies based on which enemy they replace as a symbol encounter
        Parameters:
            replacements (Array): Contains pairs of replacements [OGID, NEWID]
            foes (Array): List of basic enemies
    '''
    def adjustBasicEnemyStats(self, replacements, foes):
        for replacedID, replacementID in replacements.items():
            replaced = foes[replacedID]
            replacement = foes[replacementID]

            replacement.pressTurns = replaced.oldPressTurns

            statMods = replaced.statMods
            newStats = Stats(math.floor(replacement.stats.HP * statMods.HP), math.floor(replacement.stats.MP * statMods.MP), math.floor(replacement.stats.str * statMods.str),
                math.floor(replacement.stats.vit * statMods.vit), math.floor(replacement.stats.mag * statMods.mag),
                math.floor(replacement.stats.agi * statMods.agi), math.floor(replacement.stats.luk * statMods.luk))
            
            replacement.stats = newStats
    '''
    Switches the location listed in the menu of the new encounter demons to that of their replacements.
        Parameters:
        replacements(List): Contains pairs of replacements [OGID, NEWID]
        comp List(Compendium_Demon): list of all compendium demons
    '''
    def adjustListedLocations(self, replacements, comp):
        ogSpawns = []
        for replacedID in replacements.keys():
            replaced = comp[replacedID]
            ogSpawns.append([copy.deepcopy(replaced.creationSpawn),copy.deepcopy(replaced.vengeanceSpawn)])

        for index, replacementID in enumerate(replacements.values()):
            replacement = comp[replacementID]
            
            replacement.creationSpawn = ogSpawns[index][0]
            replacement.vengeanceSpawn = ogSpawns[index][1]
        
        #TODO: Does this still work with Dictionary to delete overworld? Maybe rethink this in general
        replacedList = replacements.values()
        nonEncounter = [f for f in comp if f.ind not in replacedList and 'Mitama' not in f.name]
        # Delete location data for demon who cannot be encountered on overworld
        for demon in nonEncounter:
            demon.creationSpawn.mapNameID = 120 #values for non encounterable demons
            demon.creationSpawn.zoneNameID = 0
            demon.vengeanceSpawn.mapNameID = 120
            demon.vengeanceSpawn.zoneNameID = 0
            
    '''
    Randomizes main story and sidequest bosses in eventEncountArr. The array is filtered to exclude problematic and duplicate encounters before shuffling
    '''
    def randomizeBosses(self):
        encountersWithBattleEvents = [x.encounterID for x in self.battleEventArr]
        encounterPools = bossLogic.createBossEncounterPools(self.eventEncountArr, self.encountArr, self.uniqueSymbolArr, self.abscessArr, self.bossDuplicateMap, self.configSettings)
        if not encounterPools:
            return
        with open(paths.BOSS_SPOILER, 'w', encoding="utf-8") as spoilerLog: #Create spoiler log
            for poolName, filteredEncounters in encounterPools.items():
                validForcedEventEncounter = False
                shuffledEncounters = []
                if "Vanilla" in poolName:
                    shuffledEncounters = filteredEncounters
                else:
                    while not validForcedEventEncounter: #until solution is found where event only bosses are replaced by event encounters
                        shuffledEncounters = sorted(filteredEncounters, key=lambda x: random.random()) #First filter the encounters and shuffle the ones to randomize
                        forcedEventEncounterIndeces = [i for i, e in enumerate(shuffledEncounters) if e.ind in bossLogic.EVENT_ONLY_BOSSES]
                        if all(filteredEncounters[i].isEvent for i in forcedEventEncounterIndeces):
                            validForcedEventEncounter = True
                        if self.configSettings.bossNoEarlyPhysImmunity and not self.configSettings.randomizeBossResistances:
                            earlyEncounterIndeces = [i for i,e in enumerate(filteredEncounters) if self.staticBossArr[e.demons[0]].level < numbers.EARLY_BOSS_LEVEL_LIMIT]
                            if any(any(demon in numbers.PHYS_IMMUNE_BOSSES for demon in shuffledEncounters[i].demons) for i in earlyEncounterIndeces):
                                validForcedEventEncounter = False
                shuffledEncounters = [copy.deepcopy(x) for x in shuffledEncounters] 
                for index, encounter in enumerate(filteredEncounters): #Write to spoiler log
                    spoilerLog.write(str(encounter.ind) + " (" + str(encounter.isEvent) +  ") " + "(" + str(encounter.demons[0]) + ") "+ self.enemyNames[encounter.demons[0]] + " replaced by " + str(shuffledEncounters[index].ind) + " (" + str(shuffledEncounters[index].isEvent)+ ") " + self.enemyNames[shuffledEncounters[index].demons[0]] + "\n")
                    self.bossReplacements[encounter.demons[0]] = shuffledEncounters[index].demons[0]
                    if encounter.demons[1] > 0 and encounter.demons[1] != encounter.demons[0]: #Add up to 2 additional boss demons for mission text purposes. TODO: maybe support summons not present in the demons array?
                        if shuffledEncounters[index].demons[1] > 0:
                            self.bossReplacements[encounter.demons[1]] = shuffledEncounters[index].demons[1]
                        else:
                            self.bossReplacements[encounter.demons[1]] = shuffledEncounters[index].demons[0]
                    if encounter.demons[2] > 0 and encounter.demons[2] != encounter.demons[1]:
                        if shuffledEncounters[index].demons[2] > 0:
                            self.bossReplacements[encounter.demons[2]] = shuffledEncounters[index].demons[2]
                        else:
                            self.bossReplacements[encounter.demons[2]] = self.bossReplacements[encounter.demons[1]]
                for index, encounter in enumerate(filteredEncounters): #Adjust demons and update encounters according to the shuffle
                    
                    bossLogic.balanceBossEncounter(encounter.demons, shuffledEncounters[index].demons, self.staticBossArr, self.bossArr, encounter.ind, shuffledEncounters[index].ind, self.configSettings, self.compendiumArr, self.playerBossArr, self.skillReplacementMap, self.guestReplacements)
                    #print("Old hp " + str(self.staticBossArr[encounter.demons[0]].stats.HP) + " of " + self.enemyNames[encounter.demons[0]] + " now is "  +
                    #      self.enemyNames[shuffledEncounters[index].demons[0]] + " with " + str(self.bossArr[shuffledEncounters[index].demons[0]].stats.HP) + " HP")
                    self.updateShuffledEncounterInformation(encounter, shuffledEncounters[index])
                    if encounter.isEvent:
                        self.eventEncountArr[encounter.ind] = encounter.eventEncounter
                    else:
                        self.encountArr[encounter.ind] = encounter.normalEncounter
                        self.updatedNormalEncounters.append(encounter.ind)
                        if encounter.ind == bossLogic.ILLUSION_AGRAT_ENCOUNTER: #Illusion Agrat needs the symbol updated so the correct demon spawns on overworld and prevents hard camera issues in battle
                            mainDemon = encounter.demons[0]
                            self.encountSymbolArr[bossLogic.ILLUSION_AGRAT_SYMBOL].symbol = Translated_Value(mainDemon, self.playerBossArr[mainDemon].name)

                    if shuffledEncounters[index].ind in encountersWithBattleEvents and shuffledEncounters[index].isEvent:
                        if encounter.isEvent:
                            #if new encounter needs event
                            eventInds = [jIndex for jIndex, e in enumerate(encountersWithBattleEvents) if e == shuffledEncounters[index].ind]
                            for ind in eventInds:
                                self.battleEventArr[ind].encounterID = encounter.ind
                        else:
                            #set event to an unused encounter
                            eventInds = [jIndex for jIndex, e in enumerate(encountersWithBattleEvents) if e == shuffledEncounters[index].ind]
                            for ind in eventInds:
                                self.battleEventArr[ind].encounterID = bossLogic.DUMMY_EVENT_ENCOUNTERS[-1]
                    

        encountersWithBattleEvents = [x.encounterID for x in self.battleEventArr]
        for index, encounter in enumerate(self.eventEncountArr): #Set duplicate encounters to use the same demons as their new counterparts
            if index in self.bossDuplicateMap.keys():
                self.updateShuffledEncounterInformation(bossLogic.formatBossEncounter(encounter), 
                                                        bossLogic.formatBossEncounter(self.eventEncountArr[self.bossDuplicateMap[index]]))

                # If duplicate has event
                if encounter.ind in encountersWithBattleEvents:
                    eventInds = [jIndex for jIndex,e in enumerate(encountersWithBattleEvents) if e == encounter.ind] 
                    for ind in eventInds:
                        self.battleEventArr[ind].encounterID = 255
                if self.eventEncountArr[self.bossDuplicateMap[index]].ind in encountersWithBattleEvents:
                #reference has event but not duplicate 
                    eventInds = [jIndex for jIndex,e in enumerate(encountersWithBattleEvents) if e == self.eventEncountArr[self.bossDuplicateMap[index]].ind] 
                    for ind in eventInds:
                        self.battleEventArr.append(Battle_Event(encounter.ind,(len(self.battleEventArr)) * 0x50 + 0x45))
                        self.battleEventArr[-1].referenceID = ind

    '''
    Replaces demons and important flags in an encounter with its randomized replacement.
    If converting between normal and event encounter format, the number of demons is different - 6 for normal, 8 for event
        Parameters:
            encounterToUpdate(Mixed_Boss_Encounter): The encounter to adjust
            referenceEncounter(Mixed_Boss_Encounter): The encounter to pull data from
    '''
    def updateShuffledEncounterInformation(self, encounterToUpdate, referenceEncounter):
        if not self.configSettings.checkBasedMusic and not self.configSettings.randomMusic:
                    encounterToUpdate.track = referenceEncounter.track
        for demon in referenceEncounter.demons: #Save bosses new Encounter ID
            if demon not in self.checkBossInfo.keys():
                self.checkBossInfo[demon] = []
            self.checkBossInfo[demon].append(encounterToUpdate.uniqueID)
        if encounterToUpdate.isEvent:
            if referenceEncounter.isEvent:
                # both encounters event encounters
                encounterToUpdate.demons = referenceEncounter.demons
                encounterToUpdate.eventEncounter.unknownDemon = referenceEncounter.eventEncounter.unknownDemon
                encounterToUpdate.eventEncounter.unknown23Flag = referenceEncounter.eventEncounter.unknown23Flag
                #print(str(encounterToUpdate.demons[0]) + " " + self.enemyNames[encounterToUpdate.demons[0]] + " uses flag " + str(encounterToUpdate.eventEncounter.unknown23Flag))
                encounterToUpdate.eventEncounter.levelpath = referenceEncounter.eventEncounter.levelpath
                encounterToUpdate.eventEncounter.positions.demons = referenceEncounter.eventEncounter.positions.demons
                encounterToUpdate.eventEncounter.positions.addDemons = referenceEncounter.eventEncounter.positions.addDemons
                encounterToUpdate.eventEncounter.endEarlyFlag = referenceEncounter.eventEncounter.endEarlyFlag
                if not self.configSettings.checkBasedMusic and not self.configSettings.randomMusic:
                    encounterToUpdate.eventEncounter.track = referenceEncounter.eventEncounter.track
                if self.configSettings.bossDependentAmbush:
                    if encounterToUpdate.eventEncounter.startingPhase != Ambush_Type.FIELD and referenceEncounter.eventEncounter.startingPhase != Ambush_Type.FIELD and encounterToUpdate.eventEncounter.startingPhase != Ambush_Type.UNKNOWN and referenceEncounter.eventEncounter.startingPhase != Ambush_Type.UNKNOWN:
                        encounterToUpdate.eventEncounter.startingPhase = referenceEncounter.eventEncounter.startingPhase
            else:
                # only the encounter to adjust is event encounter
                encounterToUpdate.demons = referenceEncounter.demons + [0, 0]
                encounterToUpdate.eventEncounter.unknown23Flag = 0 #so that it does not use custom camera stuff
                encounterToUpdate.eventEncounter.positions.demons = referenceEncounter.normalEncounter.positions.demons
                encounterToUpdate.eventEncounter.positions.addDemons = referenceEncounter.normalEncounter.positions.addDemons
                encounterToUpdate.eventEncounter.unknownDemon = Translated_Value(referenceEncounter.demons[0], self.enemyNames[referenceEncounter.demons[0]])
                encounterToUpdate.eventEncounter.endEarlyFlag = 0
                if self.configSettings.bossDependentAmbush and encounterToUpdate.eventEncounter.startingPhase != Ambush_Type.FIELD and encounterToUpdate.eventEncounter.startingPhase != Ambush_Type.UNKNOWN:
                    encounterToUpdate.eventEncounter.startingPhase = Ambush_Type.PLAYER
            encounterToUpdate.eventEncounter.track = encounterToUpdate.track
            encounterToUpdate.eventEncounter.demons = [Translated_Value(demon, self.enemyNames[demon]) for demon in encounterToUpdate.demons]
        else:
            if referenceEncounter.isEvent:
                if referenceEncounter.ind in bossLogic.EVENT_ONLY_BOSSES: #Reference boss must remain an event encounter, so use a DUMMY event encounter
                    bossLogic.assignDummyEventEncounter(encounterToUpdate, referenceEncounter, self.dummyEventIndex, self.eventEncountArr, self.abscessArr, self.uniqueSymbolArr)
                    self.dummyEventIndex = self.dummyEventIndex + 1
                    encounterToUpdate.eventEncounter.unknownDemon = referenceEncounter.eventEncounter.unknownDemon
                    encounterToUpdate.eventEncounter.unknown23Flag = referenceEncounter.eventEncounter.unknown23Flag
                    encounterToUpdate.eventEncounter.levelpath = referenceEncounter.eventEncounter.levelpath
                    encounterToUpdate.eventEncounter.positions.demons = referenceEncounter.eventEncounter.positions.demons
                    encounterToUpdate.eventEncounter.positions.addDemons = referenceEncounter.eventEncounter.positions.addDemons
                    encounterToUpdate.eventEncounter.endEarlyFlag = referenceEncounter.eventEncounter.endEarlyFlag
                    if self.configSettings.bossDependentAmbush and encounterToUpdate.eventEncounter.startingPhase != Ambush_Type.FIELD and referenceEncounter.eventEncounter.startingPhase != Ambush_Type.FIELD and encounterToUpdate.eventEncounter.startingPhase != Ambush_Type.UNKNOWN and referenceEncounter.eventEncounter.startingPhase != Ambush_Type.UNKNOWN:
                        encounterToUpdate.eventEncounter.startingPhase = Ambush_Type.PLAYER
                else:
                    # only the reference encounter is event encounter
                    encounterToUpdate.demons = referenceEncounter.demons[:6]
                    encounterToUpdate.normalEncounter.positions.demons = referenceEncounter.eventEncounter.positions.demons
                    encounterToUpdate.normalEncounter.positions.addDemons = referenceEncounter.eventEncounter.positions.addDemons
            else:
                # both encounters normal encounters
                encounterToUpdate.demons = referenceEncounter.demons
                encounterToUpdate.normalEncounter.positions.demons = referenceEncounter.normalEncounter.positions.demons
                encounterToUpdate.normalEncounter.positions.addDemons = referenceEncounter.normalEncounter.positions.addDemons
            if not encounterToUpdate.isEvent: #Need this check in case we switched to event encounter midway
                encounterToUpdate.normalEncounter.track = encounterToUpdate.track
                encounterToUpdate.normalEncounter.demons = encounterToUpdate.demons
            
            
    '''
    Fixes certain boss flags so that they work outside of their normal location
    Currently only snake Nuwa (ID 435) is patched to add flag 0x18.
    Also removes the Battle Events from the Nuwa (ID 435) Fights
    '''
    def patchBossFlags(self):
        #Set Encounter ID for battle events of snake nuwa fight(and simulator version) to no encounter
        self.battleEventArr[21].encounterID = 255
        self.battleEventArr[23].encounterID = 255

        nuwaFlags = next(r for  r in self.bossFlagArr if r.demonID == 435)
        for i, flag in enumerate(nuwaFlags.flags):
            if flag == 0:
                nuwaFlags.flags[i] = 0x18
                nuwaFlags.flags[i +1] = 0x1D
                break

    '''
    Increases the guest Yuzuru's stats for the Glasya-Labolas fight to avoid softlocking before unlocking fusion
        Parameters:
            buffer (Table): Compendium buffer that we will directly write to because we don't hold data past the normal compendium count
    '''
    def patchYuzuruGLStats(self, buffer):
        offset = 0x69 + 0x1d0 * numbers.FIRST_GUEST_YUZURU_ID
        buffer.writeWord(999, offset + 0x1c)
        buffer.writeWord(999,offset + 0x1c + 4 * 1)
        buffer.writeWord(99,offset + 0x1c + 4 * 4)
        buffer.writeWord(99,offset + 0x1c + 4 * 5)
        buffer.writeWord(99,offset + 0x1c + 4 * 6)
        buffer.writeWord(99,offset + 0x1c + 4 * 7)
        buffer.writeWord(99,offset + 0x1c + 4 * 8)
        buffer.writeWord(99, offset)
            
    '''
    Randomizes Boss music for all encounters in eventEncountArr, excluding regular battle theme and 'no bgm change' tracks
    Also includes entries in the normal encounter array used by abscesses and punishing foes
    '''
    def randomizeEventEncounterTracks(self):
        trackList = set()
        for encounter in self.eventEncountArr:
            if encounter.track not in [0, 255]:
                trackList.add(encounter.track)
        trackList = list(trackList)
        #print(trackList)
        for encounter in self.eventEncountArr:
            if encounter.track not in [0, 255]:
                encounter.track = random.choice(trackList)
        for encounterID in self.updatedNormalEncounters:
            encounter = self.encountArr[encounterID]
            if encounter.track not in [0, 255]:
                encounter.track = random.choice(trackList)
             
    '''
    Replaces the overworld models of punishing foes with their randomized counterparts
    '''
    def updateUniqueSymbolDemons(self):
        for symbolEncounter in self.uniqueSymbolArr:
            if symbolEncounter.symbol.value >= numbers.NORMAL_ENEMY_COUNT:
                if symbolEncounter.eventEncounterID > 0:
                    self.bossSymbolReplacementMap[symbolEncounter.symbol.value] = self.eventEncountArr[symbolEncounter.eventEncounterID].demons[0].value
                    symbolEncounter.symbol = self.eventEncountArr[symbolEncounter.eventEncounterID].demons[0]
                else:
                    demon = self.encountArr[symbolEncounter.encounterID].demons[0]
                    self.bossSymbolReplacementMap[symbolEncounter.symbol.value] = demon
                    symbolEncounter.symbol = Translated_Value(demon, self.enemyNames[demon])


    '''
    Shuffles the miracle rewards from abscesses, including endgame miracles
    : Guarantee certain miracles appear before a certain point in the game
    : Handle duplicate miracles
    : Mess with starting miracles
    '''
    def randomizeMiracleRewards(self):
        miracleList = []
        rewardCounts = []
        duplicateAbscesses = {}
        abscessMiracleList = []
        bannedMiracles = [0]
        if self.configSettings.vanillaRankViolation:
            bannedMiracles.append(numbers.RANK_VIOLATION_ID)
        vanillaAbscessArr = copy.deepcopy(self.abscessArr)
        for ind, abscess in enumerate(self.abscessArr): #First gather all the miracles in a list and the number of miracles each abscess gives
            if abscess.miracles in abscessMiracleList:
                rewardCounts.append(0) #Ignore second copy of area 3 abscess miracles
                duplicateAbscesses[abscessMiracleList.index(abscess.miracles)] = ind
                abscessMiracleList.append(abscess.miracles)
                continue
            rewardCount = 0
            for miracle in abscess.miracles:
                if miracle > 0 and miracle not in bannedMiracles:
                    rewardCount += 1
                    miracleList.append(miracle)
            rewardCounts.append(rewardCount)
            abscessMiracleList.append(abscess.miracles)
        for miracle in numbers.STARTING_MIRACLES:
            miracleList.append(miracle)
        newStartingMiracles = []
        for miracle in self.configSettings.forcedEarlyMiracles: #For now, force 'important' miracles to be in the starting list
            newStartingMiracles.append(miracle)
            miracleList.remove(miracle)
        shuffledMiracles = sorted(miracleList, key=lambda x: random.random())
        
        for dependentMiracles in numbers.MIRACLE_DEPENDENCIES: #For progressive miracles put them in order
            indices = []
            unused = []
            for miracle in dependentMiracles:
                try:
                    indices.append(shuffledMiracles.index(miracle))
                    unused.append(False)
                except ValueError:
                    indices.append(-1)
                    unused.append(True)
            for i in range(len(unused)-1,-1,-1): #Remove miracles that are not obtained from an abscess
                if unused[i]:
                    del indices[i]
                    del dependentMiracles[i]
            indices.sort()
            for smallIndex, largeIndex in enumerate(indices):
                shuffledMiracles[largeIndex] = dependentMiracles[smallIndex]
        while len(newStartingMiracles) < len(numbers.STARTING_MIRACLES): #Create the starting miracle list after sorting dependant miracles
            newStartingMiracles.append(shuffledMiracles.pop(0))
        while len(newStartingMiracles) > len(numbers.STARTING_MIRACLES): #If too many forced early miracles than can be starting, add to the first abscess
            random.shuffle(newStartingMiracles)
            shuffledMiracles.insert(0, newStartingMiracles.pop(0))

        #Add a deepcopy if we add a dedicated miracle class
        abscessIndex = 0
        miracleIndex = 0
        for miracle in shuffledMiracles: #Put the shuffled miracles in order to preserve the number of miracles per abscess and avoid DUMMY data
            while rewardCounts[abscessIndex] == 0:
                abscessIndex += 1
                miracleIndex = 0
            while self.abscessArr[abscessIndex].miracles[miracleIndex] in bannedMiracles: #Future proofing if we ban miracles other than rank violation
                miracleIndex += 1
            rewardCounts[abscessIndex] = rewardCounts[abscessIndex] - 1
            self.abscessArr[abscessIndex].miracles[miracleIndex] = miracle
            miracleIndex += 1
        #print(rewardCounts)
            
        #Sync miracles between area 3 abscesses
        for originalAbscess, duplicateAbscess in duplicateAbscesses.items():
            self.abscessArr[duplicateAbscess].miracles = self.abscessArr[originalAbscess].miracles
            
        if self.configSettings.randomMiracleCosts:
            self.randomizeMiracleCosts(originalAbscessArr=vanillaAbscessArr, startingMiracles=newStartingMiracles)

        #for abscess in self.abscessArr:
        #    print(abscess.miracles)
            
    '''
    Randomizes the cost of miracles constrained by the highest miracle cost seen by this point in the game
        Parameters:
            originalAbscessArr (List(Abscess)): The list of abscesses containing miracle rewards in vanilla in the event that miracle rewards were randomized
    '''
    def randomizeMiracleCosts(self, originalAbscessArr = None, startingMiracles = numbers.STARTING_MIRACLES):
        if not originalAbscessArr:
            originalAbscessArr = self.abscessArr
            
        originalMiracles = copy.deepcopy(self.miracleArr)
        minimumCost = 5 // 5 #Miracle costs are in increments of 5 so we'll work in the base unit and multiply back up at the end
        maximumCost = 35 // 5
        
        for startingMiracleIndex in startingMiracles: #Update starting miracle costs
            self.miracleArr[startingMiracleIndex].cost = random.randint(minimumCost, maximumCost) * 5
            
        for abscessIndex, originalAbscess in enumerate(originalAbscessArr):
            for miracleIndex in originalAbscess.miracles:
                if miracleIndex > 0 and originalMiracles[miracleIndex].cost // 5 > maximumCost:
                    maximumCost = originalMiracles[miracleIndex].cost // 5 #Update the maximum 'seen' glory cost
                
            updatedAbscess = self.abscessArr[abscessIndex]
            for miracleIndex in updatedAbscess.miracles:
                if miracleIndex > 0:
                    if miracleIndex in numbers.DIVINE_GARRISON_IDS:
                        self.miracleArr[miracleIndex].cost = random.randint(minimumCost, maximumCost // 2) * 5 #Make divine garrisons cheaper
                    elif random.random() > 0.5: #Make miracles a little cheaper on average
                        self.miracleArr[miracleIndex].cost = random.randint(minimumCost, maximumCost) * 5 #Update abscess reward miracle costs
                    else:
                        self.miracleArr[miracleIndex].cost = min(random.randint(minimumCost, maximumCost), random.randint(minimumCost, maximumCost)) * 5 
                        
        for dependentMiracles in numbers.MIRACLE_DEPENDENCIES: #For progressive miracles put their costs in order
            costs = []
            for miracle in dependentMiracles:
               costs.append(self.miracleArr[miracle].cost)
            costs.sort()
            for index, miracle in enumerate(dependentMiracles):
               self.miracleArr[miracle].cost = costs[index]
       
    '''
    Reverses the order of divine garrison miracles so you get the +3 stock ones first
    '''
    def reverseDivineGarrisons(self):
        costs = []
        abscessIndices = []
        for miracle in numbers.DIVINE_GARRISON_IDS:
            currIndices = []
            costs.append(self.miracleArr[miracle].cost)
            for outerIndex, abscess in enumerate(self.abscessArr):
                for innerIndex, abscessMiracle in enumerate(abscess.miracles):
                    if miracle == abscessMiracle:
                        currIndices.append((outerIndex, innerIndex))
            abscessIndices.append(currIndices)
        costs.reverse()
        abscessIndices.reverse()
        for index, miracle in enumerate(numbers.DIVINE_GARRISON_IDS):
            self.miracleArr[miracle].cost = costs[index]
            if index == len(numbers.DIVINE_GARRISON_IDS) - 1:
                self.miracleArr[miracle].prerequisite = 0
            else:
                self.miracleArr[miracle].prerequisite = numbers.DIVINE_GARRISON_IDS[index + 1]
            for abscessIndex in abscessIndices[index]:
                self.abscessArr[abscessIndex[0]].miracles[abscessIndex[1]] = miracle
            

    '''
    Adjust the clear conditions of all missions who usually require a event encounter to be defeated to instead require the shuffled results demon.
    For encounters with more than one demon only the first demon in the list is set as a clear condition.
    Parameters:
        shuffledEncounters (List(Event_Encounter)): list of new encounters to replace the original conditions
        originalEncounters (List(Event_Encounter)): list of original encounters to find missions belonging to them
    '''
    def adjustEventEncountMissionConditions(self, shuffledEncounters, originalEncounters):
        #Exceptions for A Gold Dragons Arrival
        fourHolyBeastEncounters = [130,131] #Qing Long, Zhuque
        fourHolyBeastMission = self.missionArr[48]
        #get all missions that require a boss to be killed
        eventEncountMissions = []
        for mission in self.missionArr:
                if any(mission.ind != 48 and mission.ind not in self.updatedMissionConditionIDs and (condition.type == 1 and condition.ind >= numbers.NORMAL_ENEMY_COUNT) for condition in mission.conditions):
                    eventEncountMissions.append([mission,mission.conditions[0].ind])
        for index, encounter in enumerate(originalEncounters):
            if encounter.demons[0] == shuffledEncounters[index].demons[0]:
                continue
            #go through all mission that require boss to be killed
            for pair in eventEncountMissions:
                if any(demon.value == pair[1] for demon in encounter.demons):
                #if a demon from old encounter appears as first mission condition
                    demonAmounts = {}
                    for demon in shuffledEncounters[index].demons:
                        #count how often demons in encounter appears
                        if demon.value == 0:
                            continue
                        if demon.value in demonAmounts.keys():
                            demonAmounts.update({demon.value: demonAmounts.get(demon.value) + 1})
                        else: 
                            demonAmounts.update({demon.value: 1})
                        # make sure we have not more than 4 demons as conditions
                    if len(demonAmounts) > 4:
                        while len(demonAmounts) > 4:
                            demonAmounts.popitem()
                            
                    #empty conditions
                    for i in range(4):
                        pair[0].conditions[i].type = 0
                        pair[0].conditions[i].ind = 0
                        pair[0].conditions[i].amount = 0
                    #replace conditions with first new demon
                    keyDemon = list(demonAmounts.keys())[0]
                    amounts = demonAmounts[keyDemon]
                    pair[0].conditions[0].type = 1
                    pair[0].conditions[0].ind = keyDemon
                    pair[0].conditions[0].amount = amounts
                    if pair[0].conditions[0].ind == bossLogic.LUCIFER_PHASES[0]: #Use last phase of lucifer for mission condition
                        pair[0].conditions[0].ind = bossLogic.LUCIFER_PHASES[2]
                    self.updatedMissionConditionIDs.append(pair[0].ind)

            if encounter.ind in fourHolyBeastEncounters:
                hBIndex = fourHolyBeastEncounters.index(encounter.ind)
                fourHolyBeastMission.conditions[hBIndex].ind = shuffledEncounters[index].demons[0].value
    '''
    Randomizes the tendencies (Light, Neutral, Dark) and alignment (Law, Neutral, Chaos) of playable demons.
        Parameters:
            comp (List(Compendium_Demon)): list of playable demons
    '''
    def randomizeDemonAlignment(self, comp):
        tendencies = [1,2,3]
        alignments = [1,4,5]
        for demon in comp:
            demon.tendency = random.choice(tendencies)
            demon.alignment = random.choice(alignments)

    '''
    Removes all fusion unlock flags from all demons.
    '''
    def removeFusionFlags(self):
        for demon in self.compendiumArr:
            if demon.unlockFlags[0] > 0:
                demon.unlockFlags[0] = 0
                demon.unlockFlags[1] = 0

    '''
    Adjust the clear conditions of all missions who usually require a punishing foe to be defeated to instead require the shuffled results demon.
    For encounters with more than one demon only the first demon in the list is set as a clear condition.
    Parameters:
        uniqueSymbolArr (List(Unique_Symbol_Encounter)): list of new encounters to replace the original conditions
        staticArr (List(Unique_Symbol_Encounter)): list of original encounters to find missions belonging to them
    '''
    def adjustNonEventPunishinFoeMissionConditions(self, uniqueSymbolArr, staticArr):
        #Exceptions for A Gold Dragons Arrival
        fourHolyBeastDemons = [854,855,856,857] #Qing Long, Zhuque, Baihu, Xuan Wu
        fourHolyBeastMission = self.missionArr[48]
        artemisQuestQuetz = 933
        artemisQuest = self.missionArr[83]
        #get all missions that require a boss to be killed
        symbolMissions = []
        for mission in self.missionArr:
                if any(mission.ind not in [48, 83] and mission.ind not in self.updatedMissionConditionIDs and (condition.type == 1 and condition.ind >= numbers.NORMAL_ENEMY_COUNT) for condition in mission.conditions):
                    symbolMissions.append([mission,mission.conditions[0].ind])
        #for mission in symbolMissions:
            #print(mission[0].reward.ind)
        for index, symbol in enumerate(uniqueSymbolArr):
            if staticArr[index].eventEncounterID > 0 or symbol.symbol.value == staticArr[index].symbol.value:
                #skip to next symbol if original was eventEncounter or unchanged
                continue
            #go through all mission that require boss to be killed
            for pair in symbolMissions:
                if staticArr[index].symbol.value == pair[1]:
                    #print(symbol.symbol.translation + " replaced " + staticArr[index].symbol.translation)
                    pair[0].conditions[0].type = 1
                    pair[0].conditions[0].ind = symbol.symbol.value
                    if pair[0].conditions[0].ind == bossLogic.LUCIFER_PHASES[0]: #Use last phase of lucifer for mission condition
                        pair[0].conditions[0].ind = bossLogic.LUCIFER_PHASES[2]
                    pair[0].conditions[0].amount = 1
            if staticArr[index].symbol.value == artemisQuestQuetz: #Artemis quest has Quetz as the second mission condition, not the first
                artemisQuest.conditions[1].ind = symbol.symbol.value
                if artemisQuest.conditions[1].ind == bossLogic.LUCIFER_PHASES[0]: #Use last phase of lucifer for mission condition
                         artemisQuest.conditions[1].ind = bossLogic.LUCIFER_PHASES[2]
            if staticArr[index].symbol.value in fourHolyBeastDemons:
                hBIndex = fourHolyBeastDemons.index(staticArr[index].symbol.value)
                fourHolyBeastMission.conditions[hBIndex].ind = symbol.symbol.value
                if fourHolyBeastMission.conditions[hBIndex].ind == bossLogic.LUCIFER_PHASES[0]: #Use last phase of lucifer for mission condition
                        fourHolyBeastMission.conditions[hBIndex].ind = bossLogic.LUCIFER_PHASES[2]
    '''
    Adds the data containing the positions of demon slots in event encounters to the respective Event_Encounter.
    Parameters:
        data (Table): binary table containing the positions of demon slots in event encounters.
        eventEncountArr (List(Event_Encounter)): list of event encounters to add positions to
    Returns: the list of event encounters with positions
    '''
    def addPositionsToEventEncountArr(self, data, eventEncountArr):
        start = 0xCE
        size = 0x18F

        for index, element in enumerate(eventEncountArr):
            offset = start + size * index
            locations = {
                'demon1': offset,
                'addDemon1': offset + 0xB6
            }
            for i in range(8):
                element.positions.demons.append(Position(data.readFloat(locations['demon1'] + 0xC * i),data.readFloat(locations['demon1'] + 4 + 0xC * i)))
            for i in range(4):
                element.positions.addDemons.append(Position(data.readFloat(locations['addDemon1'] + 0xC * i),data.readFloat(locations['addDemon1'] + 4 + 0xC * i)))
            element.positions.offsetNumber = locations
        return eventEncountArr

    '''
    Adds the data containing the positions of demon slots in encounters to the respective Encounter.
    Also adjusts the size so that every encounter can have the same amount of additional demons.
    Parameters:
        encountArr (List()): list of encounters to add positions to
        fileName (String): name of the uasset file that has the positions
        writePath (String): where the uasset file should be written to eventually
    Returns: the list of encounters with positions
    '''
    def addPositionsToEncountArr(self, encountArr, fileName, writePath):
        file = General_UAsset(fileName,writePath)
        
        encounterPositions = file.json['Exports'][0]['Table']['Data']
        for index, element in enumerate(encountArr):
                
                if index >= len(encounterPositions):
                    continue
                currentEncount = encounterPositions[index]['Value']
                postArray = currentEncount[2]['Value']
                for i in range(8):
                    post = postArray[i]['Value'][0]['Value']
                    element.positions.demons.append(Position(post['X'],post['Y']))
                addPostArray = currentEncount[3]['Value']
                addDemonAmount = len(addPostArray)
                while addDemonAmount < 4:
                    addDemonAmount += 1
                    newPostTop = copy.deepcopy(postArray[0])
                    newPost = newPostTop['Value'][0]['Value']
                    newPost['X'] = 0
                    newPost['Y'] = 0
                    addPostArray.append(newPostTop)
                for i in range(4):
                    post = addPostArray[i]['Value'][0]['Value']
                    element.positions.addDemons.append(Position(post['X'],post['Y']))
        return file

    '''
    Randomizes all non essence non dampener items in Gustave's Shop.
        Parameters:
            scaling (Boolean): whether the item should be scaled to the area where they unlock
    '''
    def randomizeShopItems(self, scaling):
        dampeners = [55, 63,64,65,66,67,68] #Spyglass(gets replaced seperately) + Elemental Dampeners stay the same
        itemsInShop = [113] + dampeners #New Testatement Tablet(gets added speerately)
        validItems = []

        if scaling: #Scale Rewards per map
            slotRewardAreas = numbers.getShopUnlockAreas() #To know which map the shop slot should scale with
            validItems = {}
            for key in numbers.AREA_SHOP_UNLOCKS: #Copy item list of map, because we need to remove items already in shop
                validItems[key] = copy.deepcopy(numbers.CONSUMABLE_MAP_SCALING[key])
        else:
            for itemID, itemName in enumerate(self.itemNames): 
                if itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                    validItems.append(itemID)
    	
        #remove dampeners from valid item list
        if scaling: #Remove dampeners from all lists of valid items per area
            for key in validItems.keys(): 
                for item in itemsInShop:
                    if item in validItems[key]:
                        validItems[key].remove(item)
        else:
            for item in itemsInShop:
                if item in validItems:
                    validItems.remove(item)

        for index, entry in enumerate(self.shopArr):
            if entry.item.value in dampeners or "Essence" in entry.item.translation:
                #skip essences and dampeners or item already in shop
                continue
            if scaling:
                itemID = random.choice(validItems[slotRewardAreas[index]])
            else:
                itemID = random.choice(validItems)
            item = Translated_Value(itemID, self.itemNames[itemID])
            entry.item = item
            itemsInShop.append(itemID)
            if scaling: #remove item from all map lists
                for key in validItems.keys():
                    if itemID in validItems[key]:
                        validItems[key].remove(itemID)
            else:
                validItems.remove(itemID)
    
    '''
    Replaces Spyglass with New Testament Tablet in Shop.
    '''
    def replaceSpyglassInShop(self):
        for entry in self.shopArr:
            if entry.item.value == 55: #Spyglass
                entry.item = Translated_Value(113, self.itemNames[113]) #New Testament Tablet
        
    '''
    Adjusts prices of items to be more reasonable.
    '''
    def adjustItemPrices(self):
        self.consumableArr[82].buyPrice = 80000 #Set shop price for gospel to same as grimoire
        self.consumableArr[98].buyPrice = 500000 #Set battle sutra price to slightly higher than others instead of max
        self.consumableArr[105].buyPrice = 500000 #Set destruction sutra price to slightly higher than others instead of max

    '''
    Based on the settings for redoable item check allowance, generate a list that contains item ids that cannot be part of a repeatable item check.
    '''
    def assembleNonRedoableItemIDs(self):
        if not self.configSettings.redoableGospel:
            self.nonRedoableItemIDs.append(82)
        if not self.configSettings.redoableGrimoire:
            self.nonRedoableItemIDs.append(83)
        if not self.configSettings.redoableWhittledGoat:
            self.nonRedoableItemIDs.append(60)
        if not self.configSettings.redoableIncensesBalmsSutras:
            self.nonRedoableItemIDs.extend([84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108])
    
    '''
    Generates a new "Item" object of a subclass of Base_Item (Macca,Essence,Key).
        Parameters:
            itemID: id of the item, 0 for Macca
            amount: how many of the many item should be obtained
    Returns the item as a subclass of Base_Item.
    '''
    def generateNewItem(self,itemID, amount):
        if itemID == 0:
            return Macca_Item(amount, scaling = self.configSettings.scaleMaccaPerArea)
        elif itemID > 656 and itemID < 856 or itemID in numbers.BANNED_ITEMS:
            return Key_Item(self.itemNames[itemID],itemID, allowedAreas = numbers.KEY_ITEM_AREA_RESTRICTIONS.get(itemID,[]))
        elif itemID > 310 and itemID < 616: #Essence Range
            essence = next(e for e in self.essenceArr if e.ind == itemID)
            demon = self.getPlayerDemon(essence.demon.value)
            return Essence_Item(self.itemNames[itemID],itemID,demon, scaling = self.configSettings.scaleItemsPerArea,allowRepeatable =self.configSettings.redoableEssencesAllowed)
        elif (itemID > 615 and itemID < 655) or itemID > 855:
            return Relic_Item(self.itemNames[itemID],itemID,amount,scaling = self.configSettings.scaleItemsPerArea) 
        else: #If all special condition fails the item is a Generic Item
            if itemID in self.nonRedoableItemIDs:
                allowRepeatable = False
            else:
                allowRepeatable = True
            return Generic_Item(self.itemNames[itemID],itemID,amount,scaling = self.configSettings.scaleItemsPerArea, allowRepeatable = allowRepeatable)

    def assembleValidityMaps(self):
        #Assemble "Validity" maps which show which areas allow which items
        
        for key, value in numbers.CONSUMABLE_MAP_SCALING.items():
            self.itemValidityMap[key] = value
        for key,value in numbers.RELIC_MAP_SCALING.items():
            self.relicValidityMap[key] = value
        for area in numbers.AREA_NAMES.keys():
            self.essenceValidityMap[area] = []
            #Grab all essences in the predefined level range for the area
            for essence in self.essenceArr:
                if essence.ind  in numbers.getBannedEssences():
                    continue
                demon = self.getPlayerDemon(essence.demon.value)
                if demon in self.compendiumArr and demon.level.value >= numbers.ESSENCE_MAP_SCALING[area][0] and demon.level.value <= numbers.ESSENCE_MAP_SCALING[area][1]:
                    self.essenceValidityMap[area].append(essence.ind)
        #Assemble a list with all items
        self.itemValidityMap[0] = []
        self.essenceValidityMap[0] = []
        self.relicValidityMap[0] = []
        #TODO: Am I happy with this? This is just copied from old code
        for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
            if 'Essence' in itemName and itemID not in numbers.getBannedEssences() and itemID not in self.essenceValidityMap[0]:
                self.essenceValidityMap[0].append(itemID)
            elif itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                self.itemValidityMap[0].append(itemID)
            elif (itemID > 615 and itemID < 655) or itemID > 855 and 'NOT USED' not in itemName:
                self.relicValidityMap[0].append(itemID)
        self.originalEssenceValidityMap = copy.deepcopy(self.essenceValidityMap)

    '''
    Randomizes the rewards for everything that can be considered a check (Treasure,Mission,Miman,Gift).
    The items can either be shuffled independtly, mixed or made up completely except key items which are always shuffled.
    Also returns the items to their respective data structure.
    Returns a list of fake missions.
    '''
    def randomizeItemRewards(self):
        #A category/pool is relevant if they are nor Vanilla
        relevantPools = self.configSettings.selfItemPools + self.configSettings.sharedItemPools
        
        rewardAreaMissions = copy.deepcopy(numbers.REWARD_AREA_MISSIONS)
        for key, value in scriptLogic.EXTRA_MISSION_REWARD_AREAS.items():
            #Add items from script rewards to dictionary
            rewardAreaMissions[key] = rewardAreaMissions[key] + value
        
        missionRewardAreas = {} #Dictionary to know which area should be used to scale the a missions reward
        for key, value in rewardAreaMissions.items():
            for id in value:
                missionRewardAreas[id] = key
        
        
        #Assemble "list" of checks and items
        items, checks = self.gatherItemChecks(relevantPools, missionRewardAreas)

        if DEV_CHEATS: 
            with open(paths.CHECK_LIST_CSV,"w",newline='',encoding='utf-8') as csvfile:
                checkWriter = csv.writer(csvfile)
                checkWriter.writerow(["Type","Index","Name","Area","Repeatable","Missable","HasDuplicate","AllowedCanons","MaccaAllowed","HasOdds","ItemOdds"])

                for check in checks:
                    checkWriter.writerow([check.type, check.ind, check.name, check.area, check.repeatable, check.missable, check.hasDuplicate, check.allowedCanons, check.maccaAllowed, check.hasOdds, check.odds])

        #Independent randomization for categories
        for category in self.configSettings.selfItemPools:
            if self.configSettings.shuffleExistingItems:
                currentType = Check_Type.getCheckType(category)
                relevantChecks = [check for check in checks if check.type == currentType and not check.isFull()]
                pools = self.assembleRandomlyGeneratedItemPools(relevantChecks, items, vanillaItems = True)
                self.shuffleChecks(relevantChecks, pools)
            else:
                currentType = Check_Type.getCheckType(category)
                relevantChecks = [check for check in checks if check.type == currentType and not check.isFull()]
                pools = self.assembleRandomlyGeneratedItemPools(relevantChecks, items, vanillaItems = False)
                self.shuffleChecks(relevantChecks,pools)
        #Mixed randomization for categories
        if self.configSettings.sharedItemPools and self.configSettings.shuffleExistingItems:
            currentCheckTypes = [Check_Type.getCheckType(category) for category in self.configSettings.sharedItemPools]
            relevantChecks = [check for check in checks if check.type in currentCheckTypes and not check.isFull()]
            pools = self.assembleRandomlyGeneratedItemPools(relevantChecks, items, vanillaItems = True)
            self.shuffleChecks(relevantChecks,pools)
        elif self.configSettings.sharedItemPools:
            currentCheckTypes = [Check_Type.getCheckType(category) for category in self.configSettings.sharedItemPools]
            relevantChecks = [check for check in checks if check.type in currentCheckTypes and not check.isFull()]
            pools = self.assembleRandomlyGeneratedItemPools(relevantChecks, items, vanillaItems = False)
            self.shuffleChecks(relevantChecks, pools)
        
        giftPool = self.setChecks(checks)
        
        if "Mission Rewards" in relevantPools:
            self.updateDuplicateMissionRewards(missionRewardAreas)
        if "NPC/Story Gifts" in relevantPools:
            scriptLogic.updateGiftScripts(giftPool,self.scriptFiles,self.itemReplacementMap)


        return scriptLogic.updateAndRemoveFakeMissions(self.missionArr, self.scriptFiles)

    '''
    Collect all item checks from various lists along with their items.
        Parameters:
            relevantPools(List(String)): Which item lists should the checks be gathered from
            missionRewardAreas(Dict()): dictionary that returns the reward area of a mission id
    Returns a list of items, and a list of checks
    '''
    def gatherItemChecks(self, relevantPools, missionRewardAreas):
        items = []
        checks = []

        if "Miman Rewards" in relevantPools:
            for index, entry in enumerate(self.mimanRewardsArr):
                entry: Miman_Reward
                nonZeroItems = [i for i in entry.items if i.ind != 0]
                newMimanAmount = (1+index) * self.configSettings.mimanPerReward
                newMimanArea = numbers.getMimanRewardArea(newMimanAmount)
                check = Item_Check(Check_Type.MIMAN, index, "Miman Reward #" + str(newMimanAmount),newMimanArea,maxAdditionalItems=len(nonZeroItems)-1)

                for ogItem in entry.items:
                    if ogItem.ind == 0:
                        continue
                    item = self.generateNewItem(ogItem.ind, ogItem.amount)

                    check.inputVanillaItem(item)
                    items.append(item)

                checks.append(check)

        if "Treasures" in relevantPools:
            for chest in self.chestArr:
                if chest.chestID in numbers.UNUSED_CHESTS:
                    continue

                if chest.chestID in numbers.CHEST_AREA_EXCEPTIONS.keys():
                    area = numbers.CHEST_AREA_EXCEPTIONS[chest.chestID]
                else:
                    area = chest.map
                
                check = Item_Check(Check_Type.TREASURE, chest.chestID, "Chest " + str(chest.chestID), area)
                if chest.chestID in numbers.MISSABLE_CHESTS:
                    check.missable = True
                if chest.macca > 0:
                    item = self.generateNewItem(0,chest.macca)
                else:
                    item = self.generateNewItem(chest.item.ind,chest.amount)
                
                check.inputVanillaItem(item)
                items.append(item)
                checks.append(check)
        
        
        if "Mission Rewards" in relevantPools:
            self.missionArr = self.missionArr + scriptLogic.createFakeMissionsForEventRewards(self.scriptFiles)

            for mission in self.missionArr:
                if mission.ind in numbers.BANNED_MISSIONS:
                    continue
                if any(mission.ind in dups for dups in numbers.MISSION_DUPLICATES.values()): #Duplicates get reward assigned later
                    continue
                if mission.macca <= 0 and mission.reward.ind <= 0:
                    continue

                check = Item_Check(Check_Type.MISSION,mission.ind,mission.name,missionRewardAreas[mission.ind])
                if mission.ind in numbers.REPEAT_MISSIONS:
                    check.repeatable = True
                if mission.ind in numbers.CREATION_EXLUSIVE_MISSIONS:
                    check.allowedCanons = [Canon.CREATION]
                elif mission.ind in numbers.VENGEANCE_EXLUSIVE_MISSIONS:
                    check.allowedCanons = [Canon.VENGEANCE]
                
                if mission.ind in numbers.MUTUALLY_EXCLUSIVE_MISSIONS:
                    check.missable = True
                
                if mission.ind in numbers.MACCALESS_MISSIONS or mission.ind < 0:#To indicate Fake-Mission additional reward
                    check.maccaAllowed = False
                
                if mission.ind in numbers.MISSION_DUPLICATES:
                    check.hasDuplicate = True

                
                if mission.macca > 0:
                    item = self.generateNewItem(0, mission.macca)
                else:
                    item = self.generateNewItem(mission.reward.ind, mission.reward.amount)

                if item.ind in numbers.BANNED_KEY_REWARDS:
                    item = self.generateRandomItemRewards(check)[0]

                check.inputVanillaItem(item)
                items.append(item)
                checks.append(check)

        if "NPC/Story Gifts" in relevantPools:
            giftIndex = 0
            giftRewardAreas =scriptLogic.getGiftRewardAreas()
            for script, itemID in scriptLogic.BASE_GIFT_ITEMS.items():
                if not self.configSettings.includeTsukuyomiTalismanAsGift and script == scriptLogic.TSUKUYOMI_TALISMAN_SCRIPT:
                    continue
                if not self.configSettings.includeEmpyreanKeysAsGifts and script in scriptLogic.EMPYREAN_KEY_SCRIPTS:
                    continue

                item = self.generateNewItem(itemID, 1)

                check = Item_Check(Check_Type.GIFT,giftIndex,scriptLogic.GIFT_NAMES[script],giftRewardAreas[script])

                if "NPC/Story Gifts" in self.configSettings.selfItemPools:
                    if script in scriptLogic.VENGEANCE_EXCLUSIVE_GIFTS or script in scriptLogic.NEWGAMEPLUS_GIFTS or script in scriptLogic.MISSABLE_GIFTS:
                        #No combined pools means that exclusive items stay normal due to otherwise having not enough gift slots
                        continue
            
                if script in scriptLogic.MISSABLE_GIFTS:
                    check.missable = True
                if script in scriptLogic.REPEATABLE_GIFTS:
                    check.repeatable = True
                if script in scriptLogic.VENGEANCE_EXCLUSIVE_GIFTS:
                    check.allowedCanons = [Canon.VENGEANCE]
                if script in scriptLogic.NEWGAMEPLUS_GIFTS:
                    check.missable = True
                if script in scriptLogic.GIFT_EQUIVALENT_SCRIPTS:
                    check.hasDuplicate = True
                
                giftIndex += 1
                check.inputVanillaItem(item)
                items.append(item)
                checks.append(check)
            
        if "Vending Machines" in relevantPools:
            for vm in self.vendingMachineArr:
                vmItems = []
                odds = []
                for vmItem in vm.items:
                    
                    item = self.generateNewItem(vmItem.ind, vmItem.amount)

                    vmItems.append(item)
                    odds.append(vmItem.rate)

                if vm.ind in numbers.VM_AREA_EXCEPTIONS.keys():
                    area = numbers.VM_AREA_EXCEPTIONS[vm.ind]
                else:
                    area = vm.area

                check = Item_Check(Check_Type.VENDING_MACHINE, vm.ind, "Vending Machine Type " + str(vm.ind), area, True, False, False, 2, True, odds)

                if check.ind in numbers.MISSABLE_VENDING_MACHINE:
                    check.missable = True

                for item in vmItems:
                    check.inputVanillaItem(item)
                    items.append(item)
                checks.append(check)
        
        if "Basic Enemy Drops" in relevantPools:
            if self.configSettings.randomizeMitamaDrops:
                dropEnemies = list(filter(lambda e: e.drops.item1.value > 0, self.enemyArr))
            else:
                dropEnemies = list(filter(lambda e: 'Mitama' not in e.name and e.drops.item1.value > 0, self.enemyArr))
            
            for enemy in dropEnemies:
                drops = enemy.drops
                for index, drop in enumerate(drops):
                    odds = []
                    if drop.value > 0:
                        item = self.generateNewItem(drop.value, 1)

                        if isinstance(item,Key_Item):
                            #Do not change Key_Items as they are quest related
                            continue
                        elif isinstance(item,Essence_Item):
                            #Making sure enemy drops their own essence happens elsewhere
                            continue
                        odds.append(drop.chance)
                        area = numbers.ENCOUNTER_LEVEL_AREAS[enemy.level]
                        allowedCanons = []
                        if enemy.ind in numbers.SHINJUKU_MITAMAS:
                            area = 64
                            allowedCanons.append(Canon.VENGEANCE)
                        elif enemy.ind in numbers.CHIYODA_MITAMAS:
                            area = 63
                            allowedCanons.append(Canon.CREATION)

                        check = Item_Check(Check_Type.BASIC_ENEMY_DROP,index*10000 + enemy.ind,enemy.name + " Drop " +str(index+1),area,True,False,False,0,True,odds)
                        check.allowedCanons = allowedCanons

                        
                        if index == 0 and isinstance(item,Generic_Item) and self.configSettings.lifestoneOrChakraDrop:
                            possibleIds = [1,2] #Lifestone / Chakra Drop
                            itemChoice = random.choice(possibleIds)
                            item = self.generateNewItem(itemChoice, 1)

                            check.inputItem(item,forced = True)
                        
                        check.inputVanillaItem(item)
                        checks.append(check)
                        items.append(item)
        if "Boss Drops" in relevantPools:
            #Read the data for encounter IDs
            df = pd.read_csv(paths.BOSS_ENCOUNTER_INFO_CSV)
            bossEncData = {}
            for index, row in df.iterrows():
                canonString = str(row['Canon']).strip()
                canon = Canon.getCanonFromString(canonString) if canonString else None
                canons = [canon] if canon else []
                bossEncData[int(row['ID'])] = {
                    'Name': row['Name'],
                    'Area': int(row['Area']),
                    'Repeatable': bool(row['Repeatable']),
                    'Missable': bool(row['Missable']),
                    'Canons': canons
                }


            for demonID in self.validBossDemons:
                enemy = self.bossArr[demonID]
                drops = enemy.drops
                enemyName = self.enemyNames[demonID]
                for index, drop in enumerate(drops):
                    odds = []
                    if drop.value > 0 and drop.chance > 0:
                        item = self.generateNewItem(drop.value, 1)

                        if isinstance(item,Key_Item):
                            #Do not change Key_Items as they are quest related
                            continue
                        elif isinstance(item,Essence_Item) and self.configSettings.shuffleExistingItems:
                            #Skip drop slots that usually drop their own essence when shuffled
                            continue
                        
                        
                        if demonID not in self.checkBossInfo.keys():
                            #print(str(demonID) +" " +enemyName + " is not in checkBossInfo? but drops " + self.itemNames[drop.value])
                            #If the boss in not in the list, see if the boss has a main demon that might be in the list
                            if demonID in bossLogic.MAIN_BOSS.keys():
                                mainDemonID = bossLogic.MAIN_BOSS[demonID]
                                if mainDemonID not in self.checkBossInfo.keys():
                                    continue
                                else:
                                    encID = self.checkBossInfo[mainDemonID][0]
                            else:
                                continue  
                        else:  
                            encID = self.checkBossInfo[demonID][0]
                        if encID not in bossEncData:
                            #print(str(encID) + " not in encounter data"+" " +enemyName)
                            continue
                        encData = bossEncData[encID]
                        allowedCanons = encData["Canons"]
                        area = encData["Area"]

                        odds.append(100) #Should always be 100 I think instead of drop.chance

                        check = Item_Check(Check_Type.BOSS_DROP,index*10000 + enemy.ind,"Boss Check: "+ encData["Name"],area,False,False,False,0,True,odds)
                        check.allowedCanons = allowedCanons

                        if encData['Missable'] or demonID in bossLogic.MAIN_BOSS.keys():#The second condition is for bosses who are not necessary to kill to end the fight, but still have a drop
                            check.missable = True
                        if encData['Repeatable']:
                            check.repeatable = True

                        if index == 0 and demonID not in self.essenceBannedBosses and not self.configSettings.shuffleExistingItems:
                            #Attempt for the boss to drop their own essence
                            if random.random() < numbers.BOSS_ESSENCE_ODDS:
                                try:
                                    essence = next(e for e in self.essenceArr if self.enemyNames[demonID] == e.demon.translation and e.ind not in numbers.getBannedEssences())
                                    item = self.generateNewItem(essence.ind, 1)
                                    check.inputItem(item,forced = True)
                                except StopIteration:
                                    pass

                            check.inputItem(item,forced = True)

                        check.inputVanillaItem(item)
                        checks.append(check)
                        items.append(item)

        return items, checks
    
    '''
    Shuffle the items from the relevantItemPools into the relevantChecks respecting rules.
    Parameters:
        relevantChecks(List(Item_Check)): list of item checks to assign items to
        relevantItemPools(list(Base_Item)): list of items to assign to checks
    '''
    def shuffleChecks(self,relevantChecks, relevantItemPools):
        checkPower = 2 #To which power valid checks are weight, used to make checks/items with low valid amounts even stronger weight-wise
        for relevantItemPool in relevantItemPools:
            while relevantItemPool and relevantChecks:
                forceItem = False
                filteredRelevantItems = [i for i in relevantItemPool if i.validChecks]
                if not filteredRelevantItems:
                    chosenItem = random.choice(relevantItemPool)
                    if isinstance(chosenItem, Key_Item):
                        print("WARNING: KEY ITEM has been forced")
                    forceItem = True
                    print("Forced Item " + chosenItem.name + " had no naturally available checks")
                else:
                    #Inverse weight of amount of valid checks for item to the power of checkPower
                    #wItem = [1 / (len(i.validChecks) ** checkPower) for i in filteredRelevantItems]
                    wItem = []
                    for i in filteredRelevantItems:
                        baseWeight =1 / (len(i.validChecks) ** checkPower)
                        wItem.append(baseWeight)
                    chosenItem = random.choices(
                        filteredRelevantItems,
                        wItem
                    )[0]

                filteredRelevantChecks = [c for c in chosenItem.validChecks if c.validItemAmount > 0]
                if not filteredRelevantChecks:
                    chosenCheck = random.choice(relevantChecks)
                    forceItem = True
                else:
                
                
                    #Is there any check that desperately needs an item
                    validItemAmounts = [check.validItemAmount for check in filteredRelevantChecks]
                    desperateCheck = any(a < 10 for a in validItemAmounts)

                    #Inverse weight of amount of valid items for check to the power of checkPower
                    wChecks = []
                    for check in filteredRelevantChecks:
                        baseWeight = 1 / (check.validItemAmount ** checkPower)
                        if not desperateCheck and self.configSettings.relicBiasVendingMachine and isinstance(chosenItem,Relic_Item) and check.type == Check_Type.VENDING_MACHINE:
                            baseWeight = baseWeight*4 #Treats check as if it only has half the amount of validItems
                        wChecks.append(baseWeight)
                
                    chosenCheck = random.choices(
                        filteredRelevantChecks,
                        wChecks
                    )[0]

                duplicateItem = None
                if chosenCheck.inputItem(chosenItem,forceItem):
                    #Item succesfully placed

                    for check in chosenItem.validChecks[:]:
                        #Reduce valid items for check by 1
                        check.validItemAmount = max(0, check.validItemAmount -1)
                    
                    if isinstance(chosenItem, Key_Item) and chosenCheck.type in [Check_Type.TREASURE, Check_Type.VENDING_MACHINE] and not chosenItem.hasBeenDuplicated and not chosenCheck.hasDuplicate and chosenCheck.area in numbers.AREA_MIRRORS:
                        #Duplicate item if necessary (Example: Chest that is route-locked)
                        duplicateItem = self.generateNewItem(chosenItem.ind, 1)
                        duplicateItem.allowedAreas = [numbers.AREA_MIRRORS[chosenCheck.area]]
                        duplicateItem.hasBeenDuplicated = True
                        duplicateItem.allowedCheckTypes = [chosenCheck.type]
                        
                        relevantItemPool.append(duplicateItem)
                        #print(chosenItem.name + " has been duplicated for " + chosenCheck.name + "in area " + numbers.AREAS[chosenCheck.area])
                    elif isinstance(chosenItem, Key_Item) and not chosenItem.hasBeenDuplicated and not chosenCheck.hasDuplicate and chosenCheck.area in numbers.AREA_MIRRORS:
                        #Debug to check duplication criteria
                        pass
                        #print(chosenCheck.name + " and " + chosenItem.name + " would meet area restrictions but are skipped")
                    
                    if isinstance(chosenItem, Key_Item) and chosenCheck.hasOdds and chosenCheck.odds[0]!= 100:
                        #If the check has odds but first item is now key item set odds for everything else to 0
                        chosenCheck.odds = [100] + [0 for i in chosenCheck.vanillaAdditionalItems]
                        chosenCheck.maxAdditionalItems = 0


                    #Remove item from item pool
                    relevantItemPool.remove(chosenItem)
                    chosenItem.validChecks = []
                    
                    if chosenCheck.isFull():
                        # if Check is full remove it
                        relevantChecks.remove(chosenCheck)
                        for pool in relevantItemPools:
                            for item in pool:
                                if chosenCheck in item.validChecks:
                                    item.validChecks.remove(chosenCheck)
                        chosenCheck.validItemAmount = 0

                    if duplicateItem:
                        #If a duplicate item has been made, need re-calculate valid checks
                        for check in relevantChecks:
                            check.validItemAmount = 0
                        for pool in relevantItemPools:
                            for item in pool:
                                item.calculateValidChecks(relevantChecks)

                    #print(chosenItem.name + " in " + chosenCheck.name)
                    if chosenItem.ind in numbers.KEY_ITEM_AREA_RESTRICTIONS.keys():
                        if chosenItem.ind in self.progressionItemNewChecks:
                            self.progressionItemNewChecks[chosenItem.ind].append(chosenCheck)
                        else:
                            self.progressionItemNewChecks[chosenItem.ind] = []
                            self.progressionItemNewChecks[chosenItem.ind].append(chosenCheck)

                else:
                    if chosenCheck.isFull():
                        # if Check is full remove it
                        relevantChecks.remove(chosenCheck)
                        for pool in relevantItemPools:
                            for item in pool:
                                if chosenCheck in item.validChecks:
                                    item.validChecks.remove(chosenCheck)
                        chosenCheck.validItemAmount = 0
        
    
    '''
    Assembles pools of item, a key item pool and a normal item pool.
    Parameters:
        relevantChecks(List(Item_Check)): list of item checks
        totalItems(list(Base_Item)): list of all items across total randomization effort
        vanillaItems(Boolean): whether we should use the vanilla items from the checks or make up our own
    Returns a list of item pools [keyItemPool, otherItemPool]
    '''
    def assembleRandomlyGeneratedItemPools(self, relevantChecks, totalItems, vanillaItems = True):
        relevantItems = []
        relevantKeyItems = []

        for check in relevantChecks:
            if check.vanillaItem:
                if isinstance(check.vanillaItem, Key_Item):
                    relevantKeyItems.append(check.vanillaItem)
                elif vanillaItems:
                    relevantItems.append(check.vanillaItem)
                    relevantItems.extend(check.vanillaAdditionalItems)
                else:
                    #Generate new items instead
                    relevantItems.extend(self.generateRandomItemRewards(check))

        # Reset check counts before calculating per-item valid checks (avoid double-counting)
        for check in relevantChecks:
            check.validItemAmount = 0

        for item in relevantItems:
            if item in totalItems:
                #TODO: Maybe remove after placement instead?
                totalItems.remove(item)
            item.calculateValidChecks(relevantChecks)
        for keyItem in relevantKeyItems:
            if keyItem in totalItems:
                #TODO: Maybe remove after placement instead?
                totalItems.remove(keyItem)
            keyItem.calculateValidChecks(relevantChecks) 
        
        relevantItemPools =[relevantKeyItems,relevantItems]
        return relevantItemPools
    
    '''
    Generate new items based on the given check.
    Parameters:
        check(Item_Check): check to generate items for
    Returns a list of items for the check
    '''
    def generateRandomItemRewards(self,check):
        check: Item_Check
        newItems = []
        oldItems = [check.vanillaItem]
        oldItems.extend(check.vanillaAdditionalItems)
        #CheckType decides what items could have been in the check
        if check.type == Check_Type.TREASURE:
            maccaOdds = numbers.CHEST_MACCA_ODDS
            maccaMax = numbers.CHEST_MACCA_MAX
            maccaMin = numbers.CHEST_MACCA_MIN
            if self.configSettings.scaleMaccaPerArea:
                maccaRange = numbers.CHEST_AREA_MACCA_RANGES[check.area]
                maccaMax = maccaRange[1]
                maccaMin = maccaRange[0]
                
            essenceOdds = numbers.CHEST_ESSENCE_ODDS
            relicOdds = numbers.CHEST_RELIC_ODDS 
            itemAmount = random.choices(list(numbers.CHEST_QUANTITY_WEIGHTS.keys()), list(numbers.CHEST_QUANTITY_WEIGHTS.values()))[0]
        elif check.type == Check_Type.MIMAN:
            maccaOdds = 0 #Can't have money
            maccaMax = 0
            maccaMin = 0

            essenceOdds = numbers.MIMAN_ESSENCE_ODDS
            relicOdds = numbers.MIMAN_RELIC_ODDS
            itemAmount = random.choices(list(numbers.MIMAN_ITEM_AMOUNT_WEIGHTS.keys()),list(numbers.MIMAN_ITEM_AMOUNT_WEIGHTS.values()))[0]

        elif check.type == Check_Type.MISSION:
            maccaOdds = numbers.MISSION_MACCA_ODDS
            maccaMax = numbers.MISSION_MACCA_MAX
            maccaMin = numbers.MISSION_MACCA_MIN
            if self.configSettings.scaleMaccaPerArea:
                maccaRange = numbers.MISSION_REWARD_AREA_MACCA_RANGES[check.area]
                maccaMax = maccaRange[1]
                maccaMin = maccaRange[0]

            essenceOdds = numbers.MISSION_ESSENCE_ODDS
            relicOdds = numbers.MISSION_RELIC_ODDS 
            itemAmount = random.choices(list(numbers.MISSION_QUANTITY_WEIGHTS.keys()), list(numbers.MISSION_QUANTITY_WEIGHTS.values()))[0]
        elif check.type == Check_Type.GIFT:
            maccaOdds = 0#Can't have money
            maccaMax = 0
            maccaMin = 0

            essenceOdds = scriptLogic.GIFT_ESSENCE_ODDS
            relicOdds = scriptLogic.GIFT_RELIC_ODDS 
            #Uses chest quantity weights since not enough data to make own one
            itemAmount = random.choices(list(numbers.CHEST_QUANTITY_WEIGHTS.keys()), list(numbers.CHEST_QUANTITY_WEIGHTS.values()))[0]
        elif check.type == Check_Type.VENDING_MACHINE:
            maccaOdds = 0#Can't have money
            maccaMax = 0
            maccaMin = 0

            essenceOdds = 0
            relicOdds = 1 #Vending Machines always have relic generated by default
            itemAmount = 1#Does not matter for now since relic logic is used 
        elif check.type == Check_Type.BASIC_ENEMY_DROP:
            maccaOdds = 0#Money drops are not a check!
            maccaMax = 0
            maccaMin = 0

            essenceOdds = 0 #Cant drop additional Essences
            relicOdds = numbers.CHEST_RELIC_ODDS #TODO: Calculate odds to use instead
            itemAmount = 1
        elif check.type == Check_Type.BOSS_DROP:
            maccaOdds = 0#Money drops are not a check!
            maccaMax = 0
            maccaMin = 0

            essenceOdds = 0 #Cant drop additional Essences
            relicOdds = numbers.CHEST_RELIC_ODDS #TODO: Calculate odds to use instead
            itemAmount = 1

        #Now for all items that were in the check, generate a new one
        for _ in oldItems:
            randomNumber = random.random()
            if randomNumber < maccaOdds:
                itemID = 0 #Macca needs ID 0
                amount = random.randint(maccaMin // 100, maccaMax // 100) * 100
                
            elif randomNumber < essenceOdds + maccaOdds:
                if self.configSettings.scaleItemsPerArea:
                    cArea = check.area
                else:
                    cArea = 0
                validItems = self.essenceValidityMap[cArea]
                itemID = random.choice(validItems)
                self.essenceValidityMap[cArea].remove(itemID)
                if len(self.essenceValidityMap[cArea]) == 0:
                    self.essenceValidityMap[cArea] = copy.deepcopy(self.originalEssenceValidityMap[cArea])
                
                amount = 1
            
            elif randomNumber < relicOdds + essenceOdds + maccaOdds:
                if self.configSettings.scaleItemsPerArea:
                    validItems = self.relicValidityMap[check.area]
                else:
                    validItems = self.relicValidityMap[0]
                itemID = random.choice(validItems)
                #Relics have their own quantity weights!
                amount = random.choices(list(numbers.VENDING_MACHINE_RELIC_QUANTITY_WEIGHTS.keys()), list(numbers.VENDING_MACHINE_RELIC_QUANTITY_WEIGHTS.values()))[0]
            else: #Generic Item aka Consumables
                if self.configSettings.scaleItemsPerArea:
                    validItems = self.itemValidityMap[check.area]
                else:
                    validItems = self.itemValidityMap[0]
                if check.repeatable:
                    validItems = [i for i in validItems if i not in self.nonRedoableItemIDs]

                itemID = random.choice(validItems)
                amount = itemAmount
                if itemID in numbers.ITEM_QUANTITY_LIMITS.keys():
                    amount = min(itemAmount, numbers.ITEM_QUANTITY_LIMITS[itemID])
            amount = min(check.maxItemQuantity,amount)
            newItems.append(self.generateNewItem(itemID, amount))
            #print(check.name +" New Item: " + newItems[-1].name + " x" + str(newItems[-1].amount))
        return newItems

    '''
    For every check sets the item in their correct list.
        Parameters:
            checks(List(Item_Check)): a list of item_checks
    Returns a list of check from type Check_Type.GIFT
    '''
    def setChecks(self,checks):
        #Put items from checks back into old format
        giftPool = []
        for check in checks:
            if not check.item:
                continue
            self.logItemCheck(check)
            if check.type == Check_Type.MIMAN:
                mimanReward = self.mimanRewardsArr[check.ind]
                mimanReward.miman = (1+check.ind) * self.configSettings.mimanPerReward
                mimanReward.items = []
                mimanReward.items.append(Reward_Item(check.item.ind,check.item.amount))
                for item in check.additionalItems:
                    mimanReward.items.append(Reward_Item(item.ind,item.amount))
            
            elif check.type == Check_Type.TREASURE:
                chest = self.chestArr[check.ind]
                if check.ind != chest.chestID:
                    raise ValueError('Chest Index Issue')
                if isinstance(check.item, Macca_Item):
                    chest.item = Translated_Value(0, "Macca")
                    chest.amount = 0
                    chest.macca = check.item.amount
                else:
                    chest.item = Translated_Value(check.item.ind, check.item.name)
                    chest.amount = check.item.amount
                    chest.macca = 0
            
            elif check.type == Check_Type.MISSION:
                mission = next(m for m in self.missionArr if m.ind == check.ind)
                if isinstance(check.item, Macca_Item):
                    mission.macca = check.item.amount
                    mission.reward.ind = 0
                    mission.reward.amount = 0
                else:
                    mission.macca = 0
                    mission.reward.ind = check.item.ind
                    mission.reward.amount = check.item.amount
            elif check.type == Check_Type.GIFT:
                check.script = list(scriptLogic.BASE_GIFT_ITEMS.keys())[check.ind]
                giftPool.append(check)
            elif check.type == Check_Type.VENDING_MACHINE:
                vm = next(vm for vm in self.vendingMachineArr if vm.ind == check.ind)
                vmItemList = []
                vmItem = Vending_Machine_Item()
                vmItem.ind = check.item.ind
                vmItem.amount = check.item.amount
                vmItem.rate = check.odds[0]
                vmItem.name = check.item.name
                vmItemList.append(vmItem)

                for index, item in enumerate(check.additionalItems):
                    vmItem = Vending_Machine_Item()
                    vmItem.ind = item.ind
                    vmItem.amount = item.amount
                    vmItem.rate = check.odds[index+1]
                    vmItem.name = item.name
                    vmItemList.append(vmItem)

                while len(vmItemList) < 1+check.originalMaxAddItems:
                    vmItem = Vending_Machine_Item()
                    vmItem.ind = 0
                    vmItem.amount = 0
                    vmItem.rate = 0
                    vmItem.name = "Filler Slot"
                    vmItemList.append(vmItem)
                
                vm.items = vmItemList
            elif check.type == Check_Type.BASIC_ENEMY_DROP:
                dropIndex = check.ind // 10000 #Check index is calculated like this: index*10000 + enemy.ind with index being the drop index
                enemyIndex = check.ind - dropIndex * 10000 #So this just reverses the information

                enemy = self.enemyArr[enemyIndex]
                drop = enemy.drops[dropIndex]
                drop.value = check.item.ind
                drop.translation = check.item.name
                drop.chance = check.odds[0]
            elif check.type == Check_Type.BOSS_DROP:
                dropIndex = check.ind // 10000 #Check index is calculated like this: index*10000 + enemy.ind with index being the drop index
                enemyIndex = check.ind - dropIndex * 10000

                enemy = self.bossArr[enemyIndex]
                drop = enemy.drops[dropIndex]
                drop.value = check.item.ind
                drop.translation = check.item.name
                drop.chance = check.odds[0]


            else:
                raise ValueError('Incorrect check type which should be impossible')

        return giftPool
    
    '''
    Assigns the updated rewards to missions which are duplicates and therefore share rewards.
    '''
    def updateDuplicateMissionRewards(self,rewardAreaMissions):
        for missionID, duplicateIDs in numbers.MISSION_DUPLICATES.items(): #set rewards of duplicates to be the same as the one they duplicate
            for duplicateID in duplicateIDs:
                if missionID < 0 or duplicateID < 0: #if mission or duplicate are fake missions
                    missionFound = False
                    duplicateFound = False
                    for index, mission in enumerate(self.missionArr): #find their index in the mission array
                        if missionFound and duplicateFound:
                            break
                        if mission.ind == missionID:
                            correctMissionInd = index
                            missionFound = True
                        if duplicateID == mission.ind:
                            correctDuplicateInd = index
                            duplicateFound = True
                    dupMission = self.missionArr[correctDuplicateInd]
                    realMission = self.missionArr[correctMissionInd]
                else:
                    dupMission = self.missionArr[duplicateID]
                    realMission = self.missionArr[missionID]
                dupMission.reward.ind = realMission.reward.ind
                dupMission.reward.amount = realMission.reward.amount
                dupMission.macca = realMission.macca

                check = Item_Check(Check_Type.MISSION,duplicateID,dupMission.name,rewardAreaMissions[duplicateID]) #For the reward area always use duplicate id
                if dupMission.macca >0:
                    itemReward = self.generateNewItem(0,dupMission.macca)
                else:
                    itemReward = self.generateNewItem(dupMission.reward.ind,dupMission.reward.amount)
                check.inputItem(itemReward, forced = True)
                if itemReward.ind > 0 and itemReward.ind in numbers.KEY_ITEM_AREA_RESTRICTIONS.keys():
                    if itemReward.ind in self.progressionItemNewChecks:
                        self.progressionItemNewChecks[itemReward.ind].append(check)
                    else:
                        self.progressionItemNewChecks[itemReward.ind] = []
                        self.progressionItemNewChecks[itemReward.ind].append(check)
                self.logItemCheck(check)
    
                    
    '''
        Fills the set validBossDemons with all the demon IDs of bosses that are included in the randomizer
        Adds demons from event encounters, summons, abscesses, and punishing foes
    '''
    def findValidBossDemons(self):
        #print("event")
        for eventEncount in self.eventEncountArr: #Event encounters
            if eventEncount.ind in bossLogic.BANNED_BOSSES or eventEncount.ind in self.bossDuplicateMap.keys():
                continue
            for demon in eventEncount.demons:
                self.addValidBossDemon(demon.value)
        #print('summon')
        for summonList in bossLogic.BOSS_SUMMONS.values(): #Boss summons
            for demon in summonList:
                self.addValidBossDemon(demon)
        #print('revival')
        for revivalList in bossLogic.REVIVED_DEMON_DUPLICATE_MAP.values(): #Boss summons that are 'revival duplicates'
            for demon in revivalList:
                self.addValidBossDemon(demon)
        #print('abscess')
        for abscess in self.abscessArr: #Abscesses
            if abscess.miracles[0] == 0 or abscess.encounter <= 0:
                continue
            abscessEncounter = self.encountArr[abscess.encounter]
            for demon in abscessEncounter.demons:
                self.addValidBossDemon(demon)
        #print('overworld')
        for symbol in self.uniqueSymbolArr: #Punishing foes
            if symbol.symbol.value < numbers.NORMAL_ENEMY_COUNT or symbol.encounterID <= 0:
                continue
            overworldEncounter = self.encountArr[symbol.encounterID]
            for demon in overworldEncounter.demons:
                self.addValidBossDemon(demon)
                
    '''
        Adds a demon to the validBossDemon set. If the set already contains the demon, add it to the essence banned list
        as you cannot get multiple essences at once.
            Parameters:
                demonID (number)
    '''
    def addValidBossDemon(self, demonID):
        if demonID <= 0:
            return
        if demonID in self.validBossDemons:
            self.essenceBannedBosses.add(demonID)
        else:
            self.validBossDemons.add(demonID)
            

    '''
    Adjusts the damage dealt multiplier of bosses based on the level difference between their original level and their new level
    Strong bosses fought earlier will do less damage while weak bosses fought later will deal more.
    '''
    def scaleBossDamage(self):
        for index, updatedBoss in enumerate(self.bossArr):
            if index < numbers.NORMAL_ENEMY_COUNT:
                continue
            oldLevel = self.staticBossArr[index].level
            newLevel = updatedBoss.level
            if newLevel > oldLevel:
                updatedBoss.damageMultiplier += (newLevel - oldLevel) * 2
                #print(self.enemyNames[index] + ": " + str(updatedBoss.damageMultiplier))
            elif newLevel < oldLevel:
                updatedBoss.damageMultiplier = max(10, updatedBoss.damageMultiplier + newLevel - oldLevel)
                #print(self.enemyNames[index] + ": " + str(updatedBoss.damageMultiplier))

    '''
    Randomizes the stats of normal demons.
        Parameters:
            comp (List(Compendium_Demon)): Optional list of demons to randomize
            mask (List(Number)): Optional list of demon IDs to filter comp by, only randomizing stats of those demons
            foes (List(Enemy_Demon)): Optional list of enemy version of demons to also adjusts stats for
    '''
    def randomizeDemonStats(self, comp, mask=None, foes=None):
        for demon in comp:
            if mask and demon.ind not in mask:
                continue
            if 'Mitama' in demon.name:
                #do not randomize mitama stats
                continue
            nahoLevel = self.nahobino.stats[demon.level.value]
            avgMin = 0.96 #Girimekhalas Stat Mod Average, lowest of normal demons
            avgMax = 1.35 #Pixies Stat Mod Average, highest of normal demons

            def averageCalc():
                sum = 0
                for n in randomNumbers: sum += n
                return sum/len(randomNumbers)
            
            ogRanges = [numbers.DEMON_HP_MOD_RANGE,numbers.DEMON_MP_MOD_RANGE, numbers.DEMON_STAT_MOD_RANGE, copy.deepcopy(numbers.DEMON_STAT_MOD_RANGE),copy.deepcopy(numbers.DEMON_STAT_MOD_RANGE),copy.deepcopy(numbers.DEMON_STAT_MOD_RANGE),copy.deepcopy(numbers.DEMON_STAT_MOD_RANGE)]
            ranges = copy.deepcopy(ogRanges)
            
            if self.configSettings.betterSpecialFusions and demon.ind in self.specialFusionDemonIDs:
                avgMin += 0.15 
                avgMax += 0.15

            #initialize random numbers
            randomNumbers = [
                random.randrange(ranges[0][0],ranges[0][1]) / 1000, #HP 
                random.randrange(ranges[1][0],ranges[1][1]) / 1000, #MP
                random.randrange(ranges[2][0],ranges[2][1]) / 1000, #Str
                random.randrange(ranges[3][0],ranges[3][1]) / 1000, #Vit
                random.randrange(ranges[4][0],ranges[4][1]) / 1000, #Mag
                random.randrange(ranges[5][0],ranges[5][1]) / 1000, #Agi
                random.randrange(ranges[6][0],ranges[6][1]) / 1000 #Luk
            ]
            average = averageCalc()
            index = random.randrange(0,6) #initialize random index to start stat ajustment with a random stat
            while not (avgMax >= average and avgMin <= average):
                #until average is in defined range
                if average > avgMax:
                    #reduce maximum modififer for stat
                    ranges[index][1] = max(min(math.floor(randomNumbers[index] * 1000 -10),ogRanges[index][1]),ogRanges[index][0] +1)
                else:
                    #increase minimum modifier for stat
                    ranges[index][0] = min(max(math.ceil(randomNumbers[index] * 1000 +10),ogRanges[index][0]),ogRanges[index][1] -1)
                randomNumbers[index] = random.randrange(ranges[index][0],ranges[index][1]) / 1000
                average = averageCalc()
                if index < 6:
                    index += 1
                else:
                    index = 0

            foe=None
            enemyModifiers = None
            if foes and any(demon.ind == foe.ind and 'NOT USED' not in foe.name for foe in foes):
                foe = next(foe for foe in foes if demon.ind == foe.ind)
                #Get basic enemy multipliers to preserve original enemy to player stat ratios 
                enemyModifiers = Stats(
                    foe.stats.HP / demon.stats.HP.og,
                    foe.stats.MP / demon.stats.MP.og,
                    foe.stats.str / demon.stats.str.og,
                    foe.stats.vit / demon.stats.vit.og,
                    foe.stats.mag / demon.stats.mag.og,
                    foe.stats.agi / demon.stats.agi.og,
                    foe.stats.luk / demon.stats.luk.og
                )
            if self.configSettings.betterSpecialFusions and demon.ind in self.specialFusionDemonIDs:
                for randomNumber in randomNumbers:
                    randomNumber += 0.15
            #Apply these multipliers to the nahobinos stats at new level to gain new level
            demon.stats.HP.og = math.floor(nahoLevel.HP * randomNumbers[0])
            demon.stats.MP.og = math.floor(nahoLevel.MP * randomNumbers[1])
            demon.stats.str.og = math.floor(nahoLevel.str * randomNumbers[2])
            demon.stats.vit.og = math.floor(nahoLevel.vit * randomNumbers[3])
            demon.stats.mag.og = math.floor(nahoLevel.mag * randomNumbers[4])
            demon.stats.agi.og = math.floor(nahoLevel.agi * randomNumbers[5])
            demon.stats.luk.og = math.floor(nahoLevel.luk * randomNumbers[6])
            
            #adjust enemy stats to match new stats with correct ratio if necessary
            if foe and enemyModifiers:
                foe.stats.HP = math.floor(demon.stats.HP.og * enemyModifiers.HP)
                foe.stats.MP = math.floor(demon.stats.MP.og * enemyModifiers.MP)
                foe.stats.str = math.floor(demon.stats.str.og * enemyModifiers.str)
                foe.stats.vit = math.floor(demon.stats.vit.og * enemyModifiers.vit)
                foe.stats.mag = math.floor(demon.stats.mag.og * enemyModifiers.mag)
                foe.stats.agi = math.floor(demon.stats.agi.og * enemyModifiers.agi)
                foe.stats.luk = math.floor(demon.stats.luk.og * enemyModifiers.luk)

            growthRanges = [#min,max based on base demon data
                [17,28],#HP 
                [13,27],#MP
                [3,33],#Str 
                [11,33],#Vit
                [10,38],#Mag
                [10,36],#Agi
                [12,29]#Luk
            ]

            sumRange = [138,148]#growth total sums obtained from vanilla data

            if self.configSettings.betterSpecialFusions and demon.ind in self.specialFusionDemonIDs:
                for value in sumRange:
                    value = int(value * 1.15)
                for growthRange in growthRanges:
                    growthRange[0] += 5
                    growthRange[1] += 5

            randomGrowths = []
            for index in range(7):
                if randomNumbers[index] > 1: #If modifier is higher than base nahobinos, growth is in upper range
                    rGrowth = random.randrange(math.floor((growthRanges[index][0] + growthRanges[index][1]) / 2),growthRanges[index][1])
                else: #otherwise growth is in lower range
                    rGrowth = random.randrange(growthRanges[index][0],math.floor((growthRanges[index][0] + growthRanges[index][1]) / 2))
                randomGrowths.append(rGrowth)

            sumGrowths = sum(randomGrowths)
            index = random.randrange(0,6)#initialize random index to start stat ajustment with a random stat
            while not (sumRange[0] <= sumGrowths and sumRange[1] >= sumGrowths):
                if sumGrowths > sumRange[1] and randomGrowths[index] > growthRanges[index][0]:
                    #reduce growth to reach desired total
                    randomGrowths[index] -= 1
                elif sumGrowths < sumRange[0] and randomGrowths[index] < growthRanges[index][1]:
                    #increase growth to reach desired total
                    randomGrowths[index] += 1
                sumGrowths = sum(randomGrowths)
                if index < 6:
                    index += 1
                else:
                    index = 0

            demon.stats.HP.growth = randomGrowths[0]
            demon.stats.MP.growth = randomGrowths[1]
            demon.stats.str.growth = randomGrowths[2]
            demon.stats.vit.growth = randomGrowths[3]
            demon.stats.mag.growth = randomGrowths[4]
            demon.stats.agi.growth = randomGrowths[5]
            demon.stats.luk.growth = randomGrowths[6]

    '''
    Based on the level of two demons and an array of demons of a race sorted by level ascending, determine which demon results in the normal fusion.
    Resulting demon is the demon with an level higher than the average of the two levels.
        Parameters:
            level1 (Number): Level of the first ingredient demon
            level2 (Number): Level of the second ingredient demon
            resultTable (Array): Array of demons of a race sorted by level ascending
        Returns:
            The demon that should result from the fusion
    '''
    def determineNormalFusionResult(self, level1, level2, resultTable):
        resultingLevel = math.ceil((level1 + level2) / 2) + 1
        foundDemon = False
        for element in resultTable:
            if element.level.value >= resultingLevel and not foundDemon:
                return element
        return resultTable[-1]
    
    '''
    Returns an array of ids of all demons that are the result of a special fusion.
        Returns:
            An array of ids of all demons that are the result of a special fusion.
    '''
    def listSpecialFusables(self):
        demons = list(map(lambda fusion: fusion.result.value, self.specialFusionArr))
        return demons

    '''
    Creates Arrays for each race containing the registerable demons of that race in ascending order based on their level.
        Parameters:
            comp (Array) The array containing the data of all demons
        Returns:
           Array containing an array for each race containing the registerable demons of that race in ascending order based on their level
    '''
    def createRaceTables(self, comp):
        #For every race...
        raceTable = []
        for race in RACE_ARRAY:
            demonList = []
            #go trough each demon
            for demon in comp:
                if race == demon.race.translation and not demon.name.startswith('NOT USED'):
                    #and add them to the array if they belong to the race and are used
                    demonList.append(demon)
            #Sort array in ascending order
            demonList.sort(key = lambda a: a.level.value)
            raceTable.append(demonList)
        return raceTable
    
    '''
    Defines how many demons start at each level.
        Parameters:
            comp (Array(Compendium_Demon)): Array containing data on all playable demons
    '''
    def defineLevelSlots(self, comp):
        slots = [0] * 100 
        for demon in comp:
            if not demon.name.startswith('NOT') and demon.ind not in numbers.BAD_IDS and 'Mitama' not in demon.name:
                slots[demon.level.value] = slots[demon.level.value] + 1
        return slots
    
    '''
    Changes the pixie in the talk tutorial to a level 2 demon.
        Parameters:
             comp (Array(Compendium_Demon)): Array containing data on all playable demons
             evEncount (Array(Event_Encounter)): Array containing data on all eventEncounter
    '''
    def adjustTutorialPixie(self, comp, evEncount):
        #Encounter with Event Pixie has id 7 in eventEncount table
        encounter = next(e for e in evEncount if e.ind == 7)

        possibilities = [d for d in comp if d.level.value == 2]

        demon = random.choice(possibilities)

        encounter.demons[0].value = demon.ind
        encounter.demons[0].translation = demon.name

    '''
    Adjusts the essence in the shop to demons of the same level as the original.
        Parameters:
            shop (Array(Shop_Entry)) shop entry array
            essences (Array(Essence)) essence array containing price and demon information
            comp (Array(Compendium_Demon)) array of demons with new and old levels
            scaling (Boolean): whether the essences scale to the level of the original shop essences
    '''
    def adjustShopEssences(self, shop, essences, comp, scaling):
        validDemons = list(filter(lambda demon: not demon.name.startswith('NOT') and demon.ind not in numbers.BAD_IDS and 'Mitama' not in demon.name, comp))
        newDemonEssences = []
        for entry in shop:
            if "Essence" in entry.item.translation and not "Aogami" in entry.item.translation and not "Tsukuyomi" in entry.item.translation:
                ogEssence = next(e for e in essences if e.ind == entry.item.value)
                if scaling:
                    level = comp[ogEssence.demon.value].level.original
                    possibilities = [d for d in validDemons if d.level.value == level and d.ind not in newDemonEssences]
                else:
                    possibilities = [d for d in validDemons if d.ind not in newDemonEssences]
                demon = random.choice(possibilities)
                newDemonEssences.append(demon.ind)
                essence = next(e for e in essences if demon.ind == e.demon.value)
                if scaling:
                    essence.price = ogEssence.price
                entry.item = Translated_Value(essence.ind, essence.name)
                

    '''
    Adds additional race fusion combinations to the fusionChartArr, to allow their normal fusion.    
    '''
    def addAdditionalFusionsToFusionChart(self,config):
        def getInd(race):
            return RACE_ARRAY.index(race)
        
        fusionCombo = [
            ["Herald","Drake","Primal"], #in reference Samael and Mastema being required for Satan
            ["Herald","Tyrant","Devil"], #in reference to Metatron + Beelzebub being the special fusion for Lucifer
            ["Beast","Kunitsu","UMA"], #a rabbit is a beast and Hare of Inaba supports the Kunitsu
            ["Kunitsu","Wilder","UMA"], #Wilder is similiar to Beast, but really just wanted a second one
            ["Lady","Megami","Enigma"], #both Enigma demons are female and Kinmamon is Megami in SoulHackers 2
            ["Femme","Megami","Enigma"], #same reasoning as above
            ["Vile","Lady","Qadistu"], # Qadistu are the wives or ladies of Samael, Vile in other games
            ["Drake","Lady","Qadistu"], # Qadistu are the wives or ladies of Samael who is a Drake
            ["Vile","Fury","Fiend"], #Vile for the connection to death and Fury to symbolize the strength of Fiend
            ["Foul","Wargod","Fiend"], #Foul for stench of death and many empty fusions, Wargod for battle prowess of Fiend
            ["Haunt","Wargod","Fiend"] #Haunt for the connection to death, Wargod for battle prowess of Fiend
        ]
        if config.randomRaces:
            fusionCombo.append(["Devil","Tyrant","Primal"]) #Lucifer + race with most results
            fusionCombo.append(["Devil","Herald","Primal"]) #Lucifer + Mastema in special fusion recipe
            fusionCombo.append(["Drake","Dragon","Primal"]) #Drake Samael + polar opposite Dragon
            fusionCombo.append(["Primal","Fiend","Devil"]) #I wanted a fiend into devil recipe
            fusionCombo.append(["Vile","Deity","Devil"]) #Vile (Tyrant), Deity (Herald)
            fusionCombo.append(["Vile","Herald","Devil"]) #Vile (Tyrant)
            fusionCombo.append(["Genma","Deity","Enigma"]) #Genma from Anansi + deity to lead onyankopon
            fusionCombo.append(["Raptor","Megami","Enigma"]) #Raptor had open fusions
            fusionCombo.append(["Holy","Lady","Enigma"]) #holy for onyankopon, lady for the other two enigma
            fusionCombo.append(["Kishin","Devil","Fiend"]) #Fiends as servants of devil
            fusionCombo.append(["Foul","Fury","Fiend"]) #Fury to symbolize the strength of Fiend + stench of death
            fusionCombo.append(["Kishin","Foul","Fiend"]) #Fiends as servants and stench of death
            fusionCombo.append(["Wargod","Tyrant","Fiend"]) #Wargod for battle prowess and Tyrant for status
            fusionCombo.append(["Holy","Tyrant","Fiend"]) #Open fusions
            fusionCombo.append(["Haunt","Genma","Fiend"]) #Dead demigods or something
            fusionCombo.append(["Haunt","Kishin","Fiend"]) #Fiends as servants and connection to death
            fusionCombo.append(["Wilder","Avatar","Fiend"]) #Wilder had open fusions
            fusionCombo.append(["Devil","Wargod","Fiend"]) #Wargod for battle prowess and relationship with devil Lucifer
            fusionCombo.append(["Genma","Foul","Fiend"]) #Dead demigods or something
            fusionCombo.append(["Raptor","Kunitsu","UMA"]) #Raptor had open fusions
            fusionCombo.append(["Beast","Avatar","UMA"]) #Two beast likes
            fusionCombo.append(["Vile","Snake","Qadistu"]) #Vile from Samael, snake from lilith
            fusionCombo.append(["Jaki","Megami","Qadistu"]) #Jaki had open fusions
            fusionCombo.append(["Jaki","Lady","Qadistu"]) #Jaki had open fusions
            fusionCombo.append(["Wilder","Femme","Qadistu"]) #only availabe femme fusion
            fusionCombo.append(["Tyrant","Lady","Qadistu"]) #Tyrant (Vile)
        
        
        if self.configSettings.swapGuestsWithDemons:
            fusionCombo.append(["Genma","Jaki","Human"])
            fusionCombo.append(["Haunt","Holy","Human"])
            fusionCombo.append(["Chaos","Fairy","Human"])
            fusionCombo.append(["Panagia","Qadistu","Human"])
            fusionCombo.append(["Foul","Herald","Human"])
            fusionCombo.append(["Kunitsu","Human","Panagia"])
            fusionCombo.append(["Qadistu","Human","Panagia"])
            fusionCombo.append(["Megami","Human","Panagia"])
            fusionCombo.append(["Holy","Snake","Panagia"])
            fusionCombo.append(["Fiend","Human","Chaos"])
            fusionCombo.append(["Devil","Human","Chaos"])
            fusionCombo.append(["Devil","Fury","Chaos"])

            #These are addeed so that Guest races can fuse into something more easily
            fusionCombo.append(["Human","Deity","Divine"])
            fusionCombo.append(["Human","Kishin","Divine"])
            fusionCombo.append(["Human","Holy","Divine"])
            fusionCombo.append(["Human","Herald","Divine"])
            fusionCombo.append(["Human","Avatar","Divine"])
            fusionCombo.append(["Human","Jirae","Yoma"])
            fusionCombo.append(["Human","Avian","Yoma"])
            fusionCombo.append(["Human","Enigma","Yoma"])
            fusionCombo.append(["Human","Fallen","Vile"])
            fusionCombo.append(["Human","Snake","Vile"])
            fusionCombo.append(["Human","Brute","Vile"])
            fusionCombo.append(["Human","Wargod","Vile"])
            fusionCombo.append(["Human","Raptor","Vile"])

            fusionCombo.append(["Panagia","Megami","Deity"])
            fusionCombo.append(["Panagia","Lady","Deity"])
            fusionCombo.append(["Panagia","Kunitsu","Deity"])
            fusionCombo.append(["Panagia","Genma","Deity"])
            fusionCombo.append(["Panagia","Human","Deity"])
            fusionCombo.append(["Panagia","Night","Femme"])
            fusionCombo.append(["Panagia","Herald","Femme"])
            fusionCombo.append(["Panagia","Drake","Femme"])
            fusionCombo.append(["Panagia","UMA","Kunitsu"])
            fusionCombo.append(["Panagia","Yoma","Kunitsu"])
        if self.configSettings.swapDemifiend:
            fusionCombo.append(["Chaos","Fury","Fiend"])
            fusionCombo.append(["Chaos","Kishin","Fiend"])
            fusionCombo.append(["Chaos","Wargod","Fiend"])
            fusionCombo.append(["Chaos","Devil","Fiend"])
            fusionCombo.append(["Chaos","Lady","Fairy"])
            fusionCombo.append(["Chaos","Night","Fairy"])
            fusionCombo.append(["Chaos","Femme","Fairy"])
            fusionCombo.append(["Chaos","Panagia","Fairy"])
            fusionCombo.append(["Chaos","Herald","Fallen"])
            fusionCombo.append(["Chaos","Divine","Fallen"])


        for fc in fusionCombo:
            if(fc not in self.fusionChartArr):
                self.fusionChartArr.append(Fusion_Chart_Node(None,Translated_Value(getInd(fc[0]),fc[0]),Translated_Value(getInd(fc[1]),fc[1]),Translated_Value(getInd(fc[2]),fc[2])))
                #self.fusionChartArr.append(Fusion_Chart_Node(None,Translated_Value(getInd(fc[1]),fc[1]),Translated_Value(getInd(fc[0]),fc[0]),Translated_Value(getInd(fc[2]),fc[2])))

    '''
    Shuffles the levels of all playable demons and does adjustments to data based on that shuffling.
    The shuffling process takes the fusions of demons into account by assembling the fusion tree from the bottom.
        Parameters:
            comp (Array(Compendium_Demon)): The array of playable demons
            buffer(Table): table for the special fusion buffer
        Returns:
            The array of playable demons with shuffled levels
    '''
    def shuffleLevel(self, comp, config,buffer):
        

        #Array that defines for each index=Level how many demons can have this level
        slots = self.defineLevelSlots(comp)   

        #Returns the highest free level in the slots array
        def getHighestFreeLevel():
            max = 1
            for lv, slot in enumerate(slots):
                if slot > 0:
                    max = lv
            return max

        #Returns the lowest free level in the slots array
        def getLowestFreeLevel():
            min = 99
            for lv, slot in enumerate(slots):
                if slot > 0 and lv < min:
                    min = lv
            return min

        #For each race build up new array with empty subarrays
        raceLevels = [ [] for _ in range(len(RACE_ARRAY)) ]

        #Valid demons are all demons whose level can be unconditionally randomized
        validDemons = list(filter(lambda demon:  demon.race.translation != 'Element' and not demon.name.startswith('NOT') and demon.ind not in numbers.BAD_IDS and 'Mitama' not in demon.name, comp))
        #elements contain all 4 demons of the element race
        elements = list(filter(lambda d: d.race.translation == 'Element' and d.ind not in numbers.BAD_IDS, comp))
        #Contains all demons who can only be fused after their fusion is unlocked via flag 
        flaggedDemons = list(filter(lambda demon: demon.unlockFlags[0] > 0, comp))
        flaggedDemons.sort(key = lambda a: a.minUnlock, reverse=True)
       
        #assign elemments levels between level 15 and 25
        for e in elements:
            validLevel = False
            while not validLevel:
                newLevel = self.getRandomLevel(slots, 25, 15)
                if slots[newLevel] > 0 and newLevel not in raceLevels[RACE_ARRAY.index(e.race.translation)]:
                    #make sure slot is available and no demon of the same race has the same level
                    validLevel = True
            slots[newLevel] = slots[newLevel] - 1
            comp[e.ind].level.value = newLevel
            raceLevels[RACE_ARRAY.index(e.race.translation)].append(newLevel)

        #Array containing the 10 base demons and every demon with a newly assigned level
        base = []
        # list of every fusion combination for demons in base
        fusions = []
        # list of all newly generated special fusions
        specialFusions = []
        # list of levels of all original special fusions
        specialFLevels = self.getMinLevelPerSpecialFusion() 
        #print(specialFLevels)


        for demon in validDemons:
            #changes fusion flags for Hare of Inaba, Kinmamon, Amabie
            if demon.fusability == 256:
                demon.fusability = 0

        
        levelCorrection = 0
        #until we have 10 base demons
        while len(base) < 10:
            #choose random demon
            demon = random.choice(validDemons)
            # get lowest level,
            curLevel = getLowestFreeLevel()

            if len(base) == 0 :
                #add demon to base
                base.append(demon)
                #set demons new level in compendium
                comp[demon.ind].level.value = curLevel
                #decrease slots for the assigned level
                slots[curLevel] -= 1
                #remove demon from validDemon list
                validDemons.pop(validDemons.index(demon))
                # add level to the appropriate race level list
                raceLevels[demon.race.value].append(curLevel)
            else:
                if curLevel in raceLevels[demon.race.value]:
                        # prevents two demons of the same race sharing the same level
                        continue
                if len(base) >= 4:
                    #levelCorrection is needed to skip the level 5 demons for the base 10
                    #Only one of the level 5 demons is normally recruitable, but base 10 need to be recruitable
                    levelCorrection = levelCorrection + 0.5
                    curLevel = getLowestFreeLevel() + math.ceil(levelCorrection)

                raceLevels[demon.race.value].append(curLevel)
                comp[demon.ind].level.value = curLevel
                slots[curLevel] = slots[curLevel] -1

                # This loop adds all fusions based on the newly added demon and demons in base
                # since resulting demon currently unclear creates dummy fusion result
                for b in base:
                    if(self.isValidFusion(demon,b)):
                        race1 = demon.race.translation
                        race2 = b.race.translation
                        target = next((f for x, f in enumerate(self.fusionChartArr) if (f.race1.translation == race1 and f.race2.translation == race2) or (f.race1.translation == race2 and f.race2.translation == race1)), None).result
                        dummy = Compendium_Demon()
                        dummy.ind = -1
                        dummy.name = "Fake"
                        dummy.race = target
                        dummy.level = Demon_Level(math.ceil((demon.level.value + b.level.value) / 2) +1, curLevel)
                        fusions.append([demon,b,dummy])
                # add demon to base and remove from valid demons
                base.append(demon)
                validDemons.pop(validDemons.index(demon))
        fusableDemonS = []
        #Check if demons in the base 10 can fuse into each other
        for b in base:
            possibleFusions = [f for f in fusions if f[2].race.translation == b.race.translation and f[2].ind == -1 and f[2].level.value <= b.level.value]
            for p in possibleFusions:
                p[2] = b
                fusableDemonS.append(b)

        attempts = 0
        #attempts usually average around 40 by my tests
        while len(validDemons) > 0 and attempts < 300:
            demon = random.choice(validDemons)
        
            curLevel = getLowestFreeLevel()
            #print(str(curLevel) + "/" + str(attempts))

            #check if demon of same race and level already exists, skip if yes
            if curLevel in raceLevels[demon.race.value]:
                attempts += 1
                continue
            #if special fusion
            if curLevel in specialFLevels:
                raceLevels[demon.race.value].append(curLevel)
                comp[demon.ind].level.value = curLevel
                slots[curLevel] = slots[curLevel] -1
                #generate new fusion add it to specialFusions list and remove special fusion level
                specialFusions.append(self.generateSpecialFusion(demon, [b for b in base if b.level.value < demon.level.value]))
                specialFLevels.pop(specialFLevels.index(curLevel))

                # also add combinations of special fusion result and base demons to fusions list
                for b in base:
                    if(self.isValidFusion(demon,b)):
                        race1 = demon.race.translation
                        race2 = b.race.translation
                        target = next((f for x, f in enumerate(self.fusionChartArr) if (f.race1.translation == race1 and f.race2.translation == race2) or (f.race1.translation == race2 and f.race2.translation == race1)), None).result
                        dummy = Compendium_Demon()
                        dummy.ind = -1
                        dummy.name = "Fake"
                        dummy.race = target
                        dummy.level = Demon_Level(math.ceil((demon.level.value + b.level.value) / 2) + 1, curLevel)
                        fusions.append([demon,b,dummy])
                
                base.append(demon)
                fusableDemonS.append(demon)
                validDemons.pop(validDemons.index(demon))
            else:
                #if no special fusion at this level available
                #determine fusions that could lead to demon of same race and lower level
                possibleFusions = [f for f in fusions if f[2].race.translation == demon.race.translation and f[2].ind == -1 and f[2].level.value <= curLevel]
                for p in possibleFusions:
                    p[2] = demon
                if(len(possibleFusions) == 0):
                    # if no possible fusions exist, try again from start
                    attempts += 1
                    continue
                raceLevels[demon.race.value].append(curLevel)
                comp[demon.ind].level.value = curLevel
                slots[curLevel] = slots[curLevel] -1
                
                for b in base:
                    if(self.isValidFusion(demon,b)):
                        race1 = demon.race.translation
                        race2 = b.race.translation
                        target = next((f for x, f in enumerate(self.fusionChartArr) if (f.race1.translation == race1 and f.race2.translation == race2) or (f.race1.translation == race2 and f.race2.translation == race1)), None).result
                        dummy = Compendium_Demon()
                        dummy.ind = -1
                        dummy.name = "Fake"
                        dummy.race = target
                        dummy.level = Demon_Level(math.ceil((demon.level.value + b.level.value) / 2) +1, curLevel)
                        fusions.append([demon,b,dummy])
                base.append(demon)
                fusableDemonS.append(demon)
                validDemons.pop(validDemons.index(demon))

        #do not continue if attempts elapse 300
        if attempts >= 300:
            print("Could not assign all levels properly")
            return False

        notFusableCurrently = [demon for demon in base if demon not in fusableDemonS]
        for demon in notFusableCurrently:
            possibleFusions = [f for f in fusions if f[2].race.translation == demon.race.translation and f[2].ind == -1 and f[2].level.value <= demon.level.value]
            for p in possibleFusions:
                p[2] = demon
                fusableDemonS.append(demon)
        
        notFusableCurrently = [demon for demon in base if demon not in fusableDemonS and demon.race.translation in numbers.NO_DOWNFUSE_RACES]
        for demon in notFusableCurrently:
            #print(demon.name + " " + str(demon.level.value))
            specialFusions.append(self.generateSpecialFusion(demon, [b for b in base if b.level.value < demon.level.value + 5 and b.level.value != demon.level.value]))
        
        #slots = self.defineLevelSlots(comp)
        #print(slots)
        self.adjustLearnedSkillLevels(comp)
        comp = self.adjustStatsToLevel(comp)
        self.adjustFusionFlagsToLevel(comp)
        self.adjustSpecialFusionTable(specialFusions,comp,buffer)
        
        return comp
    

    '''
    Randomly adjust the amount of skills a demon starts with based on their level.
        Parameters:
            comp (Array(Compendium_Demon)): Array containing data on all playable demons
    '''
    def adjustSkillSlotsToLevel(self,comp):
        for demon in comp:
            if demon.level.value != demon.level.original:
                minS = 4 * math.ceil(demon.level.value / 25)
                maxS = max(minS,min(16, 5 + math.ceil(demon.level.value / 6)))
                slots = math.ceil(random.randint(minS, maxS) /4)

                while len(demon.skills) < slots:
                    demon.skills.append(Translated_Value(1,translation.translateSkillID(1,self.skillNames)))
                if len(demon.skills) > slots:
                    for index, skill in enumerate(demon.skills):
                        if index >= slots:
                            demon.skills[index].value = 0
                            demon.skills[index].ind = 0
                            demon.skills[index].translation = translation.translateSkillID(0,self.skillNames)
            if demon.level.value != demon.level.original and demon.level.original == 99:
                demon.learnedSkills.append(Translated_Value(1,translation.translateSkillID(1,self.skillNames),level=demon.level.value +1))
                demon.learnedSkills.append(Translated_Value(1,translation.translateSkillID(1,self.skillNames),level=demon.level.value +2))
                demon.learnedSkills.append(Translated_Value(1,translation.translateSkillID(1,self.skillNames),level=demon.level.value +3))

    '''
    Checks if the the fusion of two demons results in a valid race.
        Parameters:
            demon1 (Compendium_Demon): first ingredient demon
            demon2 (Compendium_Demon): second ingredient demon
        Returns:
            Whether the two demons can be fused to obtain a demon or not
    '''
    def isValidFusion(self,demon1,demon2):
        r1 = demon1.race.translation
        r2 = demon2.race.translation
        return any((f.race1.translation == r1 and f.race2.translation == r2) or (f.race1.translation == r2 and f.race2.translation == r1) for f in self.fusionChartArr)

    '''
    Generates a new Special_Fusion object for demon as a result with ingrediens from base.
    Number of ingredients used is random between 2 and 4.
        Parameters:
            demon (Compendium_Demon): result of the assembled special fusion
            base (List(Compendium_Demon)): list of possible ingredients for demon
        Returns:
            The newly assembled special fusion
    '''
    def generateSpecialFusion(self, demon, base):
        availableDemons = copy.deepcopy(base)

        ingNumber = random.randint(2,4)
        ingredients = []

        fusion = Special_Fusion()
        fusion.resultLevel = demon.level.value
        fusion.result = Translated_Value(demon.ind, demon.name)

        for index in range(ingNumber):
            ing = random.choice(availableDemons)
            ingredients.append(Translated_Value(ing.ind, ing.name))
            availableDemons.remove(ing)
        
        fusion.demon1 = ingredients[0]
        fusion.demon2 = ingredients[1]
        if len(ingredients) > 2:
            fusion.demon3 = ingredients[2]
        else:
            fusion.demon3 = Translated_Value(0,self.compendiumArr[0].name)

        if len(ingredients) > 3:
            fusion.demon4 = ingredients[3]
        else:
            fusion.demon4 = Translated_Value(0,self.compendiumArr[0].name)


        return fusion

    '''
    Returns a random level that is free based on the array slots and between max and min.
        Parameters:
            slots (Array): Defines which level are still free to randomize into
            maximum (Number): The maximum generated level
            minimum (Number): The minimum generated level
        Returns:
            The randomly generated level under the constraints
    '''
    def getRandomLevel(self, slots, maximum, minimum):
        validLevels = []
        for i, s in enumerate(slots):
            if i >= minimum and i <= maximum and s > 0:
                validLevels.append(i)
        if validLevels:
            rng = random.choice(validLevels)
        else:
            rng = 1
        return rng
    
    '''
    Adjusts the fusion flags on demons based on their initial level pairing in comp
        Parameters:
            comp (List(Compendium_Demon)): Array containing data on all demons
    '''
    def adjustFusionFlagsToLevel(self,comp):
        flagPairs = []
        filtered = list(filter(lambda e: e.ind not in numbers.BAD_IDS and 'Mitama' not in e.name and not e.name.startswith('NOT USED'), comp))
        
        for demon in filtered:
            if demon.unlockFlags[0] > 1:
                flagPairs.append([[demon.unlockFlags[0],demon.unlockFlags[1]],demon.level.original])
                demon.unlockFlags[0] = 0
                demon.unlockFlags[1] = 0
        
        for demon in filtered:
            if any(l[1] == demon.level.value for l in flagPairs):
                pairs = [l for l in flagPairs if l[1] == demon.level.value]
                pair = random.choice(pairs)
                index = flagPairs.index(pair)

                demon.unlockFlags = pair[0]
                flagPairs.pop(index)

    
    '''
    Adjusts the stats of demons to their new level based on multipliers of the nahobinos stats at the original and new level
        Parameters:
            comp (Array(Compendium_Demon)): Array containing data on all demons
    '''
    def adjustStatsToLevel(self, comp):
        for demon in comp:
            #Get Nahobinos base stats at original and new level
            demon = self.recalculateDemonStatsToLevel(demon,demon.level.original,demon.level.value)
        return comp

    '''
    Adjusts the stats of demons to their new level based on multipliers of the nahobinos stats at the original and new level
        Parameters:
            demon (Compendium_Demon): the demon to calculate new stats for
            oldLevel (Integer): the demons original level
            newLevel (Integer): the demons new level
        Returns the demon with recalculated stats
    '''
    def recalculateDemonStatsToLevel(self,demon,oldLevel, newLevel):
        nahoOGLevel = self.nahobino.stats[oldLevel]
        nahoNewLevel = self.nahobino.stats[newLevel]


        #Define multipliers from nahobino stats at original level to og stats
        modifiers = Stats(
            demon.stats.HP.og / nahoOGLevel.HP,
            demon.stats.MP.og / nahoOGLevel.MP,
            demon.stats.str.og / nahoOGLevel.str,
            demon.stats.vit.og / nahoOGLevel.vit,
            demon.stats.mag.og / nahoOGLevel.mag,
            demon.stats.agi.og / nahoOGLevel.agi,
            demon.stats.luk.og / nahoOGLevel.luk
        )
        #Apply these multipliers to the nahobinos stats at new level to gain new level
        demon.stats.HP.start = math.floor(nahoNewLevel.HP * modifiers.HP)
        demon.stats.MP.start = math.floor(nahoNewLevel.MP * modifiers.MP)
        demon.stats.str.start = math.floor(nahoNewLevel.str * modifiers.str)
        demon.stats.vit.start = math.floor(nahoNewLevel.vit * modifiers.vit)
        demon.stats.mag.start = math.floor(nahoNewLevel.mag * modifiers.mag)
        demon.stats.agi.start = math.floor(nahoNewLevel.agi * modifiers.agi)
        demon.stats.luk.start = math.floor(nahoNewLevel.luk * modifiers.luk)
        return demon
        
    
    '''
    Adjust the levels of a demons learned skills to match their new level.
    If a demon is now level 99, moves the learned skills to the normal skill array.
        Parameters:
            comp (Array(Compendium_Demon)): Array containing data on all demons
    '''
    def adjustLearnedSkillLevels(self, comp):
        for demon in comp:
            if demon.level.original != demon.level.value:
                if len(demon.learnedSkills) > 0 and demon.level.value == 99:
                    demon.skills = demon.skills + demon.learnedSkills
                    demon.learnedSkills = []
                else:
                    for skill in demon.learnedSkills:
                        skillLevel = min(99, skill.level - demon.level.original + demon.level.value)
                        skill.level = skillLevel
                        
    '''
    Function that assembles an array with each special fusions level.
        Returns:
            An array with each special fusions resulting level.
    '''
    def getMinLevelPerSpecialFusion(self):
        return list(map(lambda fusion: fusion.resultLevel, self.specialFusionArr))

    '''
    Defines the minimum level belonging to each unlock flag.
    This value is later transferred when flags are randomized.
        Parameters: 
            comp (Array(Compendium_Demon)): Array of all playable demons
    '''
    def defineLevelForUnlockFlags(self, comp):
        for demon in comp:
            if demon.unlockFlags[0] > 0:
                demon.minUnlock = demon.level.original
                
    '''
        Determines which combination of starting races is able to fuse into every other race in the fusion chart and which race can only achieve this with additonal races added.
    '''
    def determineFusability(self):
        #Mark races that are not part of the fusion chart
        filteredArray = []
        for i, e in enumerate(RACE_ARRAY):
            special = False
            if i > len(RACE_ARRAY) - 14 or e.startswith('Element') or e.startswith('Chaos') or e.startswith('Fiend') or e.startsWith('Non') or e.startsWith('Unused') or e.startsWith('Mitama'):
                special = True
            filteredArray.append({'name': e, 'fusable': False, 'obtained': False, 'special': special, 'ind': i })

        #Filter out Races that are not part of the fusion chart
        races = filter(lambda e: e.special == False, filteredArray)
        #print(len(races) - len(RACE_ARRAY))

        #Due to filter index!= id, so new method is needed
        def returnRaceByID(ind):
            return next(f for x, f in enumerate(races) if f.ind == ind)
        OGraces = map(lambda e: { 'name': e.name, 'fusable': e.fusable, 'obtained': e.obtained, 'ind': e.ind }, races)

        for findex, first in enumerate(OGraces):
            for jindex in range(findex, len(OGraces)):
                #for each pair of races

                #these races get modified so we need to recopy them
                races = list(map(lambda e: { 'name': e.name, 'fusable': e.fusable, 'obtained': e.obtained, 'ind': e.ind }, OGraces))
                second = races[jindex];
                returnRaceByID(first.ind).obtained = True
                returnRaceByID(second.ind).obtained = True
                returnRaceByID(first.ind).fusable = True
                returnRaceByID(second.ind).fusable = True
                #print(first)
                #print(second)

                #print(races)

                unique = False

                demonCount = 2
                externalDemon = 2
                recruits = []
                recruits.append(first.name)
                recruits.append(second.name)
                currentRaces = []
                currentRaces.push(first)
                currentRaces.push(second)
                availableFusions = []
                #Finds the resulting race of a fusion between race1 and race2
                def calcfusionResult(self, race1, race2):
                    fusion = next((f for x, f in enumerate(self.fusionChartArr) if (f.race1.translation == race1.name and f.race2.translation == race2.name) or (f.race1.translation == race2.name and f.race2.translation == race1.name)), None)
                    if fusion:
                        if fusion.result.value == 0:
                            return fusion
                        else:
                            return next(f for x, f in enumerate(races) if f.ind == fusion.result.value)
                    else:
                        return fusion
                #while there is a race that is not fusable yet
                while any(lambda r: r.fusable == False, races):
                    #print(races.find((r, i) => r.fusable == false).name)
                    availableFusions = []
                    #add fusable races to availableFusions if they are not already obtained 
                    for i, race1 in enumerate(currentRaces):
                        for index in range(i+1, len(currentRaces)):
                            race2 = currentRaces[index]
                            fusionResult = calcfusionResult(race1, race2)
                            if fusionResult and fusionResult not in availableFusions and fusionResult.obtained == False:
                                availableFusions.append(fusionResult)
                    #For each available fusion, set the fused race to fusable and obtained
                    for fusion in availableFusions:
                        fusion.fusable = True
                        fusion.obtained = True
                        currentRaces.append(fusion)
                        demonCount += 1
                    #if there is no available fusionm radomly add another random race to obtained
                    if len(availableFusions) == 0:
                        unique = False
                        newRace = races[random.randrange(len(races) - 14)]
                        while not unique:
                            if newRace.obtained == True:
                                newRace = random.choice(races)
                            else:
                                unique = True
                                returnRaceByID(newRace.id).fusable = True
                                returnRaceByID(newRace.id).obtained = True
                                demonCount += 1
                                externalDemon += 1
                                currentRaces.push(newRace)
                                recruits.push(newRace.name)
                                #console.log("Recruit; " + newRace.name)
                #print(demonCount)
                #print(externalDemon)
                #print(recruits)

    '''
    Updates all missions that require the defeat of basic enemies with their replacements and missions that require you to bring a demon with a demon of the same level.
        Parameters:
            replacements (List([Integer,Integer])): list of which demon replaces which demon encounter wise
            foes (List(Enemy_Demon)): list of all basic enemies
            missionArr (List(Mission)): list of all missions
        Returns the adjusted mission list
    '''
    def adjustMissionsRequiringNormalDemons(self, replacements, foes, missionArr):
        replacementSources = list(replacements.keys())
        for mission in missionArr:
        #for every mission...    
            for condition in mission.conditions:
                #for every condition
                if (condition.type == 1 or condition.type == 5) and condition.ind < numbers.NORMAL_ENEMY_COUNT:
                #Condition requires demoon to kill or in party and that demon is a normal enemy
                    if condition.ind in replacementSources:
                        #use replacement if existent 
                        condition.ind = replacements[replacementSources[replacementSources.index(condition.ind)]]
                    else:
                        #else find demon of the same level as original demon
                        level = next(demon.level.original for demon in self.compendiumArr if demon.ind == condition.ind)
                        sameLevel = next(demon.ind for demon in self.compendiumArr if demon.level.value == level)
                        condition.ind = sameLevel
                if mission.ind == numbers.BRAWNY_AMBITIONS_ID and condition.type == 7 : #skill condition for Brawny Ambition II
                    #print("Mission:" + str(mission.ind) + " D: " + self.enemyNames[mission.conditions[0].ind] + " C: " + translation.translateSkillID(self.compendiumArr[mission.conditions[0].ind].learnedSkills[1].value, self.skillNames))
                    #print(str(self.compendiumArr[mission.conditions[0].ind].learnedSkills[1].value))
                    if(len(self.compendiumArr[mission.conditions[0].ind].learnedSkills) >= 2):
                       condition.ind = self.compendiumArr[mission.conditions[0].ind].learnedSkills[1].value
                    else:
                        condition.ind = self.compendiumArr[mission.conditions[0].ind].skills[1].value
                    self.brawnyAmbitions2SkillName = self.obtainSkillFromID(condition.ind).name

        return missionArr

    '''
    Logs all skills that are not normally assigned to a playable demon.
        Parameters:
            skillLevels  (Array(Skill_Level)): Array of skills and at what they are first and last available at
    '''
    def findUnlearnableSkills(self, skillLevels):
        for skill in skillLevels:
            if skill.level[0] == 0 and skill.level[1] == 0 and not skill.name.startswith("NOT USED") and self.determineSkillStructureByID(skill.id) != "Active":
                print(skill)

    '''
    Resets the level of each demon in the compendium to their original value.
        Parameters:
            comp (Array(Compendium_Demon))
    '''
    def resetLevelToOriginal(self,comp):
        for demon in comp:
            demon.level = Demon_Level(demon.level.original,demon.level.original)

    '''
    Sets the encounter ID for the tutorial battle events to not occur.
    '''
    def removeBattleTutorials(self):
        #Tutorial Daemon
        self.battleEventArr[1].encounterID = 255
        #Magatsuhi Tutorial Pretas
        self.battleEventArr[12].encounterID = 255
        #Guest Tutorial Glasya-Labolas
        self.battleEventArr[35].encounterID = 255

    '''
    Reduces the compendium cost modifier of demons.
    #TODO: I didn't have any luck reducing the costs of skills directly, so this is here instead
    '''
    def reduceCompendiumCosts(self):
        for demon in self.compendiumArr:
            demon.compCostModifier = demon.compCostModifier // 10

    '''
    Sets early story fights to not be ambushes.
    '''
    def preventEarlyAmbush(self):
        for id in numbers.EARLY_STORY_EVENT_ENCOUNTERS:
            self.eventEncountArr[id].startingPhase = Ambush_Type.PLAYER

    '''
    Patches tutorial Daemon's HP to be beatable without Zio
    '''
    def patchTutorialDaemon(self):
        daemon = self.bossArr[numbers.TUTORIAL_DAEMON_ID]
        daemon.stats.HP = 27 #Should die to 3 basic attacks always
        daemon.money = 5000 #Add starting funds for qol
        spyscopeDrop = Item_Drop(79, 'Spyscope', 100, 0) #Drop spyscope and chakra drop x2
        chakraDrop = Item_Drop(2, 'Chakra Drop', 100, 0)
        daemon.drops = Item_Drops(spyscopeDrop, chakraDrop, chakraDrop)
        daemon.damageMultiplier = int(0.5 * daemon.damageMultiplier)
    
    '''
    Sets the drops of bosses which are quest relevant to their replacements and in cases where a quest drop boss replaces a quest drop boss makes sure that the drops of all bosses are not lost in conversion.
    '''
    def patchQuestBossDrops(self):
        replacementDemons = []
        replacementEncounters = []
        replacementDemonIDs = []
        
        #Gather replacements
        for index, demonID in enumerate(numbers.QUEST_DROPS_BOSSES):
            if numbers.QUEST_DROPS_BOSS_ENCOUNTERS[index] < 253:
                replacementEncounter = self.eventEncountArr[numbers.QUEST_DROPS_BOSS_ENCOUNTERS[index]]
                replacementDemon = self.bossArr[replacementEncounter.demons[0].value]
            else:
                replacementEncounter = self.encountArr[numbers.QUEST_DROPS_BOSS_ENCOUNTERS[index]]
                replacementDemon = self.bossArr[replacementEncounter.demons[0]]
            replacementDemons.append(replacementDemon)
            replacementDemonIDs.append(replacementDemon.ind)
            replacementEncounters.append(replacementEncounter)
            
        #Set drops for replacements
        for index, demonID in enumerate(numbers.QUEST_DROPS_BOSSES):
            staticBoss = self.staticBossArr[demonID]
            replacementDemons[index].drops = Item_Drops(staticBoss.drops.item1,staticBoss.drops.item2,staticBoss.drops.item3)
            
        questBossIDs = copy.deepcopy(numbers.QUEST_DROPS_BOSSES)
        
        if questBossIDs == replacementDemonIDs:
            #Everyone is the same
            return

        #First set drops for quest bosses which aren't replaced by a quest boss or show up as replacement
        toRemove = []
        for index, demonID in enumerate(questBossIDs):
            if demonID not in replacementDemonIDs and replacementDemonIDs[index] not in questBossIDs:
                staticBoss = self.staticBossArr[replacementDemonIDs[index]]
                self.bossArr[demonID].drops = Item_Drops(staticBoss.drops.item1,staticBoss.drops.item2,staticBoss.drops.item3)
                toRemove.append(index)
        toRemove.sort(reverse=True)
        
        questBossEncounters = copy.deepcopy(numbers.QUEST_DROPS_BOSS_ENCOUNTERS)
        #Remove unproblematic pairings
        for index in toRemove:
            questBossIDs.pop(index)
            replacementDemons.pop(index)
            replacementDemonIDs.pop(index)
            replacementEncounters.pop(index)
            questBossEncounters.pop(index)
        
        questBossEncounters = copy.deepcopy(numbers.QUEST_DROPS_BOSS_ENCOUNTERS)
        #Remove bosses that appear in both
        questBossSet = set(questBossIDs)
        replacementSet = set(replacementDemonIDs)
        doubleOccurenceSet = questBossSet & replacementSet
        doubleOccurences = list(doubleOccurenceSet)
        for occ in doubleOccurences:
            index = questBossIDs.index(occ)
            questBossIDs.pop(index)
            questBossEncounters.pop(index)
            index = replacementDemonIDs.index(occ)
            replacementDemonIDs.pop(index)
            replacementDemons.pop(index)
            replacementEncounters.pop(index)

        #Set drops of remaining replacements to remaining original quest drops
        questBossIDs = list(questBossSet - doubleOccurenceSet)
        replacementDemonIDs = list(replacementSet - doubleOccurenceSet)
        for index, demonID in enumerate(questBossIDs):
            staticBoss = self.staticBossArr[replacementDemonIDs[index]]
            self.bossArr[demonID].drops = Item_Drops(staticBoss.drops.item1,staticBoss.drops.item2,staticBoss.drops.item3)

    '''
    Switches the item drops of chimera with the demon that replaces it to ensure the horn of plenty is dropped for Demeter's quest
    '''
    def patchHornOfPlenty(self):
        chimera = self.bossArr[numbers.CHIMERA_DEMON_ID]
        chimeraReplacementEncounter = self.eventEncountArr[numbers.CHIMERA_ENCOUNTER_ID]
        chimeraReplacementDemon = self.bossArr[chimeraReplacementEncounter.demons[0].value]
        if chimeraReplacementDemon != chimera:
            tempDrops = chimera.drops
            chimera.drops = Item_Drops(chimeraReplacementDemon.drops.item1,chimeraReplacementDemon.drops.item2,chimeraReplacementDemon.drops.item3)
            chimeraReplacementDemon.drops = Item_Drops(tempDrops.item1, tempDrops.item2, tempDrops.item3)
    
    '''
    Switches the item drops of giri with the demon that replaces it to ensure that giris head is dropped for Kelpie's quest
    '''
    def patchGirisHead(self):
        giri = self.bossArr[numbers.GIRI_DEMON_ID]
        giriReplacementEncounter = self.eventEncountArr[numbers.GIRI_ENCOUNTER_ID]
        giriReplacementDemon = self.bossArr[giriReplacementEncounter.demons[0].value]
        if giriReplacementDemon != giri:
            tempDrops = giri.drops
            giri.drops = Item_Drops(giriReplacementDemon.drops.item1,giriReplacementDemon.drops.item2,giriReplacementDemon.drops.item3)
            giriReplacementDemon.drops = Item_Drops(tempDrops.item1, tempDrops.item2, tempDrops.item3)

    '''
    Switches the item drops of horus with the demon that replaces it to ensure that horus' head is dropped for Isis's quest
    '''
    def patchHorusHead(self):
        horus = self.bossArr[numbers.HORUS_DEMON_ID]
        horusReplacementEncounter = self.encountArr[numbers.HORUS_ENCOUNTER_ID]
        horusReplacementDemon = self.bossArr[horusReplacementEncounter.demons[0]]
        if horusReplacementDemon != horus:
            tempDrops = horus.drops
            horus.drops = Item_Drops(horusReplacementDemon.drops.item1,horusReplacementDemon.drops.item2,horusReplacementDemon.drops.item3)
            horusReplacementDemon.drops = Item_Drops(tempDrops.item1, tempDrops.item2, tempDrops.item3)
            
    '''
    Caps the HP of bosses that can infinitely diarahan to 20,000
    '''
    def capDiarahanDemonHP(self):
        for demonID in numbers.DIARAHAN_BOSSES:
            demon = self.bossArr[demonID]
            demon.stats.HP = min(demon.stats.HP, 20000)

    '''
    Fixes the camera of event encounter Seth, who now uses a dummy demon ID due to being a duplicate with punishing foe Seth
    '''
    def patchSethCamera(self):
        sethEventEncounter = self.eventEncountArr[108]
        sethEventEncounter.unknown23Flag = 0
       
    '''
    Forces all versions of Ishtar to use the same boss, condensing the pool from 8 Ishtars to one
    Additionally sets the press turns for the Ishtar kept in the pool
    '''
    def removeIshtarCopies(self):
        for eventEncountID in numbers.EXTRA_ISHTAR_ENCOUNTERS:
            self.bossDuplicateMap[eventEncountID] = numbers.TRUE_ISHTAR_ENCOUNTER
        if self.configSettings.randomizeIshtarPressTurns:
            pressTurns = random.randint(1, 8)
            self.bossArr[numbers.TRUE_ISHTAR_DEMON].pressTurns = pressTurns
            self.staticBossArr[numbers.TRUE_ISHTAR_DEMON].pressTurns = pressTurns
        else:
            self.bossArr[numbers.TRUE_ISHTAR_DEMON].pressTurns = self.configSettings.ishtarPressTurns
            self.staticBossArr[numbers.TRUE_ISHTAR_DEMON].pressTurns = self.configSettings.ishtarPressTurns
    
    '''
    Make Punishing Foe Mara use the AI of the Virtual Trainer one, and replace the mara in the virtual trainer encounter with punishing mara.
    '''
    def syncMaras(self):
        self.bossArr[numbers.PUNISHING_MARA_DEMON].AI = self.bossArr[numbers.VIRTUAL_MARA_DEMON].AI
        self.staticBossArr[numbers.PUNISHING_MARA_DEMON].AI = self.staticBossArr[numbers.VIRTUAL_MARA_DEMON].AI
        self.eventEncountArr[numbers.VIRTUAL_MARA_ENCOUNTER].demons[0] = self.eventEncountArr[numbers.PUNISHING_MARA_ENCOUNTER].demons[0]
        self.staticEventEncountArr[numbers.VIRTUAL_MARA_ENCOUNTER].demons[0] = self.staticEventEncountArr[numbers.PUNISHING_MARA_ENCOUNTER].demons[0]
        self.eventEncountArr[numbers.VIRTUAL_MARA_ENCOUNTER].unknownDemon = self.eventEncountArr[numbers.PUNISHING_MARA_ENCOUNTER].unknownDemon
        self.staticEventEncountArr[numbers.VIRTUAL_MARA_ENCOUNTER].unknownDemon = self.staticEventEncountArr[numbers.PUNISHING_MARA_ENCOUNTER].unknownDemon
        self.bossDuplicateMap[numbers.VIRTUAL_MARA_ENCOUNTER] = numbers.PUNISHING_MARA_ENCOUNTER

    '''
    Adds entries to the MapSymbolScaleTable.
    '''
    def addEntriesToMapSymbolScaleTable(self):
        json = self.mapSymbolFile.json

        table = json["Exports"][0]["Table"]["Data"]

        for demonID in numbers.ADD_LARGE_MODEL_DEMONS.keys():
            entry = copy.deepcopy(BASE_MAPSYMBOLPARAMS)

            referenceEntry = next(entry for entry in table if entry["Value"][0]["Value"] == numbers.ADD_LARGE_MODEL_DEMONS[demonID])

            entry["Value"][4]["Value"] = 1.2
            entry["Value"][0]["Value"] = demonID
            entry["Value"][5]["Value"] = referenceEntry["Value"][5]["Value"]
            entry["Value"][6]["Value"] = referenceEntry["Value"][6]["Value"]
            entry["Value"][7]["Value"] = referenceEntry["Value"][7]["Value"]

            table.append(entry)

        originalJson = self.mapSymbolFile.originalJson
        table = originalJson["Exports"][0]["Table"]["Data"]

        for demonID in numbers.ADD_LARGE_MODEL_DEMONS.keys():
            entry = copy.deepcopy(BASE_MAPSYMBOLPARAMS)

            referenceEntry = next(entry for entry in table if entry["Value"][0]["Value"] == numbers.ADD_LARGE_MODEL_DEMONS[demonID])

            entry["Value"][4]["Value"] = 1.2
            entry["Value"][0]["Value"] = demonID
            entry["Value"][5]["Value"] = referenceEntry["Value"][5]["Value"]
            entry["Value"][6]["Value"] = referenceEntry["Value"][6]["Value"]
            entry["Value"][7]["Value"] = referenceEntry["Value"][7]["Value"]

            table.append(entry)
        
    '''
    Removes entries in the map symbol scale table that were added to aid in collision calculation in model swapping.
    '''
    def removeCalcOnlyMapSymbolScales(self):
        json = self.mapSymbolFile.json

        table = json["Exports"][0]["Table"]["Data"]
        #tableCopy = copy.deepcopy(table)
        
        for entry in table:
            demonID = entry["Value"][0]["Value"]
            if demonID in numbers.REMOVE_TEMP_MODEL_DEMONS:
                table.remove(entry)

    '''
    Changes the scaling of normal demon symbols with overly large scaling factors to the normal 1.2 factor.
    Parameters:
        buffer (Table): contains the bytearray of the MapSymbolParamTable
    Returns the changed buffer
    '''
    def scaleLargeSymbolDemonsDown(self):
        json = self.mapSymbolFile.json

        table = json["Exports"][0]["Table"]["Data"]

        for entry in table:
            demonID = entry["Value"][0]["Value"]
            if demonID in numbers.LARGE_SYMBOL_NORMAL_DEMONS:
                scaleGoal = 1.2
                downscaleFactor = scaleGoal / entry["Value"][4]["Value"]

                entry["Value"][4]["Value"] = scaleGoal
                baseCollision = Position(entry["Value"][5]["Value"],entry["Value"][6]["Value"],entry["Value"][7]["Value"])
                baseCollision.scale(downscaleFactor)
                entry["Value"][5]["Value"] = baseCollision.x
                entry["Value"][6]["Value"] = baseCollision.y
                entry["Value"][7]["Value"] = baseCollision.z
            if demonID in numbers.LARGE_MODEL_NORMAL_DEMONS.keys():
                scaleGoal = numbers.LARGE_MODEL_NORMAL_DEMONS[demonID]
                downscaleFactor = scaleGoal / entry["Value"][4]["Value"]
                entry["Value"][4]["Value"] = scaleGoal
                baseCollision = Position(entry["Value"][5]["Value"],entry["Value"][6]["Value"],entry["Value"][7]["Value"])
                baseCollision.scale(downscaleFactor)
                entry["Value"][5]["Value"] = baseCollision.x
                entry["Value"][6]["Value"] = baseCollision.y
                entry["Value"][7]["Value"] = baseCollision.z
        
        # for symbol in self.mapSymbolArr:
        #     if symbol.demonID in numbers.LARGE_SYMBOL_NORMAL_DEMONS:
        #         scaleGoal = 1.2
                
        #         downscaleFactor = scaleGoal / symbol.scaleFactor
                
        #         symbol.scaleFactor = scaleGoal
        #         symbol.encountCollision.scale(downscaleFactor)
                
        #     if symbol.demonID in numbers.LARGE_MODEL_NORMAL_DEMONS.keys():
        #         scaleGoal = numbers.LARGE_MODEL_NORMAL_DEMONS[symbol.demonID]
                
        #         downscaleFactor = scaleGoal / symbol.scaleFactor
                
        #         symbol.scaleFactor = scaleGoal
        #         symbol.encountCollision.scale(downscaleFactor)

    '''
    Scale replacement of adramelech so that it is not larger to prevent potential softlocks in Temple of Eternity.
    '''
    def patchAdramelechReplacementSize(self):
        json = self.mapSymbolFile.json

        table = json["Exports"][0]["Table"]["Data"]
        adramelech = next(d for x, d in enumerate(table) if d["Value"][0]["Value"] == 265)
        #adramelech = next(d for x, d in enumerate(self.mapSymbolArr) if d.demonID == 265)
        replacementID = self.encounterReplacements[265]
        try:
            replacement =  next(d for x, d in enumerate(table) if d["Value"][0]["Value"] == replacementID)
            #replacement =  next(d for x, d in enumerate(self.mapSymbolArr) if d.demonID == replacementID)
            adraColl = Position(adramelech["Value"][5]["Value"],adramelech["Value"][6]["Value"],adramelech["Value"][7]["Value"])
            replaceCollision = Position(replacement["Value"][5]["Value"],replacement["Value"][6]["Value"],replacement["Value"][7]["Value"])
            scalingFactor = adraColl.fitIntoBox(replaceCollision)
            #scalingFactor = adramelech.encountCollision.fitIntoBox(replacement.encountCollision)
            if scalingFactor != 0:
                replacement["Value"][4]["Value"] = replacement["Value"][4]["Value"]* scalingFactor
                #replacement.scaleFactor = replacement.scaleFactor * scalingFactor
                baseCollision = Position(replacement["Value"][5]["Value"],replacement["Value"][6]["Value"],replacement["Value"][7]["Value"])
                baseCollision.scale(scalingFactor)
                replacement["Value"][5]["Value"] = baseCollision.x
                replacement["Value"][6]["Value"] = baseCollision.y
                replacement["Value"][7]["Value"] = baseCollision.z
                #replacement.encountCollision.scale(scalingFactor)
        except StopIteration:
            pass

    '''
    Speeds up demons on the overworld that replace punishing foe birds with large movement cycles
    '''
    def adjustPunishingFoeSpeeds(self):
        json = self.mapSymbolFile.json

        table = json["Exports"][0]["Table"]["Data"]
        
        for birdID, walkSpeed in numbers.PUNISHING_FOE_BIRD_SPEEDS.items():
            replacementID = self.bossSymbolReplacementMap[birdID]
            try:
                replacementSymbol = next(d for x, d in enumerate(table) if d["Value"][0]["Value"] == replacementID)
                #replacementSymbol = next(d for x, d in enumerate(self.mapSymbolArr) if d.demonID == replacementID)
                replacementSymbol["Value"][1]["Value"] = walkSpeed
                #buffer.writeFloat(walkSpeed,replacementSymbol.offsetNumbers['walkSpeed'])
                    
            except StopIteration:
                try: 
                    normalDemonEquivalent = model_swap.MODEL_SYNC[replacementID]
                    copiedSymbol = copy.deepcopy(next(d for x, d in enumerate(table) if d["Value"][0]["Value"] == normalDemonEquivalent))
                    copiedSymbol["Value"][0]["Value"] = replacementID
                    copiedSymbol["Value"][1]["Value"] = walkSpeed
                    table.append(copiedSymbol)
                    #example case: Gabriel
                    print("No boss symbol for bird replacement " +str(replacementID))

                except (KeyError,StopIteration) as e:
                    birdSymbol = next(d for x, d in enumerate(table) if d["Value"][0]["Value"] == birdID)
                    #birdSymbol = next(d for x, d in enumerate(self.mapSymbolArr) if d.demonID == birdID)
                    birdSymbol["Value"][0]["Value"] = replacementID
                    #example case: Tsukuyomi
                    print("No normal symbol for bird replacement " +str(replacementID) +". Might cause slight issues")
                    #buffer.writeWord(replacementID, birdSymbol.offsetNumbers['demonID'])

        #return buffer

    '''
    Adds unused overworld demons with speed and hitbox data to the map symbol file
    '''
    def addAdditionalMapSymbols(self):
        json = self.mapSymbolFile.json

        table = json["Exports"][0]["Table"]["Data"]
        nameMap = json["NameMap"]

        extraSymbolDF = pd.read_csv(paths.EXTRA_SYMBOLS, sep='\t')
        
        for _ , row in extraSymbolDF.iterrows():
            entry = copy.deepcopy(next(entry for entry in table if entry["Value"][0]["Value"] == row['CollisionCopyID']))
            uniqueName = translation.getUniqueMapSymbolName(row['DemonID'])
            nameMap.append(uniqueName)
            entry["Name"] = uniqueName
            entry["Value"][4]["Value"] = 1.2
            entry["Value"][0]["Value"] = row['DemonID']
            entry["Value"][1]["Value"] = float(row['WalkSpeed'])
            entry["Value"][2]["Value"] = float(row['AssaultSpeed'])
            table.append(entry)

    '''
    Adds aggro and escape voice clips for unused overworld demons
    '''
    def addEscapeFindLines(self):
        json = self.voiceMapFile.json
        table = json["Exports"][1]["Data"][0]["Value"]
        extraDataDF = pd.read_csv(paths.EXTRA_VOICE_DATA)
        for _ , row in extraDataDF.iterrows():
            entry = next(e for e in table if e[0]["Value"] == row["DemonID"])
            voiceEnums = entry[1]["Value"][0]["Value"]
            findIndex = -1
            escapeIndex = -1
            attackIndex = -1
            for index, voiceEnum in enumerate(voiceEnums):
                enumType = voiceEnum[0]["Value"]
                if enumType == "EDevilVoiceType::Escape":
                    escapeIndex = index
                if enumType == "EDevilVoiceType::Find":
                    findIndex = index
                if enumType == "EDevilVoiceType::Attack":
                    attackIndex = index
            if isinstance(row["Escape"], str):
                if escapeIndex == -1:
                    voiceEnums = voiceEnums[:attackIndex + 1] + copy.deepcopy(VOICEMAP_ESCAPE) + voiceEnums[attackIndex + 1:]
                    escapeIndex = attackIndex + 1
                    if findIndex >= 0:
                        findIndex += 1;
                voiceEnums[escapeIndex][1]["Value"]["AssetPath"]["AssetName"] = row["Escape"]
            if isinstance(row["Find"], str):
                if findIndex == -1:
                    findIndex = attackIndex + 2
                    if escapeIndex == -1:
                        findIndex -= 1
                    voiceEnums = voiceEnums[:findIndex] + copy.deepcopy(VOICEMAP_FIND) + voiceEnums[findIndex:]
                voiceEnums[findIndex][1]["Value"]["AssetPath"]["AssetName"] = row["Find"]
            entry[1]["Value"][0]["Value"] = voiceEnums


    '''
    Shuffles demon voices around while preserving individual voice sets
    '''
    def randomizeVoiceSets(self):
        self.addDevilTalkLines()
        json = self.voiceMapFile.json
        table = json["Exports"][1]["Data"][0]["Value"]
        demonIDs = []
        for entry in table:
            demonIDs.append(entry[0]["Value"])
        random.shuffle(demonIDs)
        for entry in table:
            entry[0]["Value"] = demonIDs.pop()

    '''
    Adds negotiation/haunt lines to boss-only versions of demons for use in the voice randomizer
    '''
    def addDevilTalkLines(self):
        json = self.voiceMapFile.json
        table = json["Exports"][1]["Data"][0]["Value"]
        for bossDemon, normalDemon in numbers.VOICE_MAP_DEMON_ALTS.items():
            bossEntry = next(e for e in table if e[0]["Value"] == bossDemon)
            normalEntry = next(e for e in table if e[0]["Value"] == normalDemon)
            bossVoiceEnums = bossEntry[1]["Value"][0]["Value"]
            normalVoiceEnums = normalEntry[1]["Value"][0]["Value"]
            reachedTalks = False
            for voiceEnum in normalVoiceEnums:
                enumType = voiceEnum[0]["Value"]
                if enumType == "EDevilVoiceType::DevilTalk_Positive":
                    reachedTalks = True
                if reachedTalks:
                    bossVoiceEnums.append(copy.deepcopy(voiceEnum))

    '''
    Randomizes each individual demon voice line, allowing one demon to have lines from multiple demons
    '''
    def randomizeVoiceLines(self):
        json = self.voiceMapFile.json
        table = json["Exports"][1]["Data"][0]["Value"]
        voiceBank = {}
        for entry in table:
            voiceEnums = entry[1]["Value"][0]["Value"]
            for voiceEnum in voiceEnums:
                enumType = voiceEnum[0]["Value"]
                assetPath = voiceEnum[1]["Value"]["AssetPath"]["AssetName"]
                if enumType not in voiceBank.keys():
                    voiceBank[enumType] = []
                voiceBank[enumType].append(assetPath)
        for voiceType in voiceBank.values():
            random.shuffle(voiceType)
        for entry in table:
            voiceEnums = entry[1]["Value"][0]["Value"]
            for voiceEnum in voiceEnums:
                enumType = voiceEnum[0]["Value"]
                voiceEnum[1]["Value"]["AssetPath"]["AssetName"] = voiceBank[enumType].pop()

    '''
    Randomizes demon navigator chances to find items and type of items
    Guarantees at least one navigator can find each type of item, as well as the minimum and maximum chance of items vs demons
    '''
    def randomizeNavigatorAbilities(self):
        guaranteedTypeSample = random.sample(self.navigatorArr, k=5)
        guaranteedBonusSample = random.sample(self.navigatorArr, k=2)
        minBonus = -10
        maxBonus = 15
        for navi in self.navigatorArr:
            navi.itemType = random.randrange(1, 6)
            if random.randrange(0, 10) == 0: #Small chance to get any number between -10 and 15, otherwise limit to multiples of 5
                navi.itemBonus = random.randrange(minBonus, maxBonus + 1)
            else:
                navi.itemBonus = random.randrange(int(minBonus / 5), int(maxBonus / 5) + 1) * 5
        for index, navi in enumerate(guaranteedTypeSample):
            navi.itemType = index + 1
        guaranteedBonusSample[0].itemBonus = minBonus
        guaranteedBonusSample[1].itemBonus = maxBonus

    '''
    Changes the demon navigators to reflect what their respective enemy/boss replacements are
    '''
    def changeNavigatorDemons(self):
        json = self.naviParamFile.json
        table = json["Exports"][0]["Table"]["Data"]
        nameMap = json["NameMap"]
        mapJson = self.mapSymbolFile.json

        mapTable = mapJson["Exports"][0]["Table"]["Data"]
        tableIndex = 1 #First navigator entry is dummy data
        for navi in self.navigatorArr:
            entry = table[tableIndex]
            if navi.demonID in numbers.NAVIGATOR_BOSS_MAP.keys():
                replacementID = self.bossReplacements[numbers.NAVIGATOR_BOSS_MAP[navi.demonID]]
            else:
                replacementID = self.encounterReplacements[navi.demonID]
            #replacementID = 565 #Tiamat
            try:
                mapEntry = copy.deepcopy(next(e for e in mapTable if e["Value"][0]["Value"] == replacementID))
            except StopIteration:
                replacementID = self.enemyNames.index(self.enemyNames[replacementID])
                try:
                    mapEntry = copy.deepcopy(next(e for e in mapTable if e["Value"][0]["Value"] == replacementID))
                except StopIteration:
                    print("WARNING: No valid map table entry for demon ID " + str(replacementID))
            xCollision = mapEntry["Value"][5]["Value"] #Resize model within a random range of navigator sizes
            yCollision = mapEntry["Value"][6]["Value"] #Encounter collision isn't a great correlation to model collision but it seems to work well enough
            zCollision = mapEntry["Value"][7]["Value"]
            maxCollision = max(xCollision, yCollision, zCollision) #Only consider the largest collision dimension for calculating new model size
            maxCollision = maxCollision * numbers.BASE_NAVI_MODEL_SCALE_FACTOR / mapEntry["Value"][4]["Value"]
            targetSize = random.randrange(numbers.MIN_NAVI_SIZE, numbers.MAX_NAVI_SIZE)
            scaleFactor = targetSize / maxCollision
            if replacementID in numbers.GIANT_DEMON_MODELS:
                scaleFactor = scaleFactor / numbers.GIANT_MODEL_SCALE_FACTOR
            entry["Value"][1]["Value"] = scaleFactor
            entry["Value"][13]["Value"] = False #Fix issue with small models moving to navi spots on certain navi IDs
            entry["Value"][14]["Value"] = True
            entry["Value"][15]["Value"] = 30 
            entry["Value"][16]["Value"] = 50
            entry["Value"][17]["Value"] = 100
            #print(str(scaleFactor) + " for " + str(replacementID) + " to hit target size " + str(targetSize))
            if replacementID in self.guestReplacements.keys():
                replacementVoiceID = message_logic.normalVoiceIDForBoss(self.guestReplacements[replacementID], self.enemyNames).zfill(3) #Replace voices
            else:
                replacementVoiceID = message_logic.normalVoiceIDForBoss(replacementID, self.enemyNames).zfill(3) #Replace voices
            nameMap.append(message.getCuePath(replacementVoiceID, message_logic.DEMON_FILENAMES, isNameMap=True)[0])
            if replacementVoiceID in self.navigatorVoiceIDs:
                goVoice = "dev" + replacementVoiceID + "_vo_14" #There is also a find voice but that is a common sound effect to all navigators
            else:
                goVoice = "dev" + replacementVoiceID + "_vo_23" #Use support skill voice when there is no navigator go voice
            nameMap.append(message.getCuePath(replacementVoiceID, message_logic.DEMON_FILENAMES, voice=goVoice, isNameMap=True)[0])
            entry["Value"][3]["Value"]["AssetPath"]["AssetName"] = message.getCuePath(replacementVoiceID, message_logic.DEMON_FILENAMES, voice=goVoice)[0]
            self.naviReplacementMap[navi.demonID] = replacementID
            navi.demonID = replacementID
            tableIndex += 1
        message_logic.updateNavigatorVoiceAndText(self.naviReplacementMap, self.enemyNames, self.playerBossArr, self.compendiumArr, self.guestReplacements, self.configSettings)

    '''
    Sets tones of bosses to 0 to prevent bosses talking to the player if the battle starts as an ambush.
    '''
    def nullBossTones(self):
        #TODO: Do not do this for punishing foes so you can they can trigger ambush flee money event
        for index,demon in enumerate(self.playerBossArr):
            if index < numbers.NORMAL_ENEMY_COUNT:
                continue
            if demon.tone.value < 100 and demon.tone.value != 32: #so that Guest Tone is not changed
                demon.tone.value = 0

    '''
        Removes unique skill animations so they no longer cause the game to hang until pressing the skip animation button
    '''
    def removeUniqueSkillAnimations(self):
        skillMap = pd.read_csv(paths.SKILL_ANIMATION_MAP)
        for index, row in skillMap.iterrows():
            uniqueSkillID = row['Unique Skill ID']
            normalSkillID = row['Normal Skill ID']
            uniqueSkillName = row['Unique Skill']
            normalSkillName = row['Normal Skill']
            uniqueSkill = self.obtainSkillFromID(uniqueSkillID)
            normalSkill = self.obtainSkillFromID(normalSkillID)
            #print("Changing " + uniqueSkill.name + " to " + normalSkill.name)
            if self.skillNames[uniqueSkillID] != uniqueSkillName:
                print("Warning: skill ") + uniqueSkillName + " does not match " + self.skillNames[uniqueSkillID] + " at index " + str(index)
            if self.skillNames[normalSkillID] != normalSkillName:
                print("Warning: skill ") + normalSkillName + " does not match " + self.skillNames[normalSkillID] + " at index " + str(index)
            uniqueSkill.animation = normalSkill.animation
    
    '''
    Halves the heal power of all enemy-only healing skills
    '''
    def nerfBossHealing(self):
        for skillID in numbers.ENEMY_HEALING_SKILL_IDS:
            skill = self.obtainSkillFromID(skillID)
            skill.healing.flag = skill.healing.flag // 2
            skill.healing.percent = skill.healing.percent // 2

    '''
        Adds missing boss music back to Lilith, Tehom, and Mastema
        TODO: Add music to the school fights, maybe
    '''
    def patchMissingBossMusic(self):
        for eventEncountID, track in numbers.BOSS_TRACK_FIX_MAP.items():
            self.eventEncountArr[eventEncountID].track = track

    '''
        Scales the experience gained from demons and quest rewards according to the expMultiplier setting
    '''
    def scaleExpGains(self):
        for demon in self.enemyArr:
            demon.experience = round(demon.experience * self.configSettings.expMultiplier)
        for demon in self.bossArr[numbers.NORMAL_ENEMY_COUNT:]:
            demon.experience = round(demon.experience * self.configSettings.expMultiplier)
        for mission in self.missionArr:
            mission.experience = round(mission.experience * self.configSettings.expMultiplier)

    '''
    Creates a copy of the new entry with the binary offset data of the old entry.
        Parameters:
            newEntry (Asset_Entry): the new asset entry data to copy
            oldEntry (Asset_Entry): the old asset entry to get the location in the binary table from
        Returns: the copy of the new entry with the binary offset data of the old entry
    '''
    def copyAssetsToSlot(self, oldEntry, newEntry):
        copyEntry = Asset_Entry()
        copyEntry.demonID = oldEntry.demonID
        copyEntry.classAssetID = newEntry.classAssetID
        copyEntry.verticalMax = newEntry.verticalMax
        copyEntry.validArea = newEntry.validArea
        copyEntry.dmAssetID = newEntry.dmAssetID
        copyEntry.horizontalMax = newEntry.horizontalMax
        copyEntry.tallMax = newEntry.tallMax
        copyEntry.postChips = newEntry.postChips
        copyEntry.locations = oldEntry.locations

        return copyEntry
    
    '''
    Create copies of demons that appear in multiple non-duplicate event encounters that replace unused demons. Get the entire source player and enemy entries from NKMBaseTable to replace unused data.
    Adjust demons in encounters to reference the copies and adjust assets of copies to use the originals.
        Parameters:
            NKMBaseTable (Table): binary table containing all demon, both player and enemy, data
    '''
    def createOverlapCopies(self, NKMBaseTable):
        dummies = copy.deepcopy(numbers.DUMMY_DEMONS)
        for source, targetIDs in numbers.DUPLICATE_SOURCES.items():
        #for every demon and the encounters they appear in...

            #assemble demon data to copy
            duplicate = Duplicate()
            sourceCompData = []
            compStart = 0x59
            for i in range(0, 0x1D0 -4, 4):
                sourceCompData.append(NKMBaseTable.readWord(compStart + source * 0x1D0 + i))
            sourceEnemyData = []
            enemyStart = 0x88139
            #-4 to reflect size minus id bytes, -12 to not copy last 3 entries which seem to depend on id
            for i in range(0, 0x170 -4 -12, 4):
                sourceEnemyData.append(NKMBaseTable.readWord(enemyStart + source * 0x170 + i))

            duplicate.compData = sourceCompData
            duplicate.enemyData = sourceEnemyData
            duplicate.sourceInd = source

            for index, target in enumerate(targetIDs):
            #for every encounter the source demon appears in...

                #grab a new id to replace
                if index == len(targetIDs) -1 and len(targetIDs) > 1: #Seth is a special case with only one event encounter
                    continue
                newID = dummies[0]

                newDupe = copy.deepcopy(duplicate)
                newDupe.ind = newID
                self.overlapCopies.append(newDupe)

                #replace source demon with new id
                for index,demon in enumerate(self.eventEncountArr[target].demons):
                    if demon.value == source:
                        self.eventEncountArr[target].demons[index] = Translated_Value(newID,self.enemyNames[source])

                self.devilAssetArr[newID] = self.copyAssetsToSlot(self.devilAssetArr[newID], self.devilAssetArr[source])
                self.devilUIArr[newID].assetID = self.devilUIArr[source].assetID
                self.devilUIArr[newID].assetString = self.devilUIArr[source].assetString
                self.talkCameraOffsets[newID].demonID = self.talkCameraOffsets[source].demonID
                self.talkCameraOffsets[newID].eyeOffset = self.talkCameraOffsets[source].eyeOffset
                self.talkCameraOffsets[newID].lookOffset = self.talkCameraOffsets[source].lookOffset
                self.talkCameraOffsets[newID].dyingOffset = self.talkCameraOffsets[source].dyingOffset

                dummies.pop(0)
                self.enemyNames[newID] = self.enemyNames[source]
                self.validBossDemons.add(newID) #Add new duplicate demons to the list of boss demons
                self.essenceBannedBosses.add(newID) #These are all duplicates of another boss demon so they shouldn't drop their essence
    '''
    Swap a guest with a demon, swapping asset assignments, and most demon data.
        Parameters:
            demonID (Integer): id of the demon
            guestID (Integer): id of the guest
    '''
    def swapDemonWithGuest(self, demonID, guestID):
        #Get correct demon/guest
        if demonID > numbers.NORMAL_ENEMY_COUNT:
            demon = self.playerBossArr[demonID]
        else:
            demon = self.compendiumArr[demonID]
        
        if guestID > numbers.NORMAL_ENEMY_COUNT:
            guest = self.playerBossArr[guestID]
        else:
            guest = self.compendiumArr[guestID]

        guestCopy = copy.deepcopy(guest)
        

        #print("Guest " + str(guestID) +" "+ guest.name +" <-> Demon " + str(demonID) + " " + demon.name )


        #TODO: Tao (Guest) is weird, since demons always get her textures??

        
        '''
        Copy demon data and other attributes from the donor to the recipient demon.
            Parameters:
                recipient: demon to receive the attributes
                donor: demon to donate the attributes
        '''
        def obtainAttributes(recipient,donor):
            donor = copy.deepcopy(donor)

            #Rename Essence
            #self.itemNames = [f"{donor.name}'s Essence" if recipient.name in itemName and 'Essence' in itemName else itemName for itemName in self.itemNames]

            recipient.name = donor.name
            recipient.nameID = donor.nameID
            recipient.descriptionID = donor.ind
            recipient.race = donor.race
            #recipient.tone = donor.tone
            recipient.resist = donor.resist
            recipient.potential = donor.potential
            recipient.innate = donor.innate

            recipient.stats = donor.stats
            recipient = self.recalculateDemonStatsToLevel(recipient,donor.level.original,recipient.level.original)

            recipient.skills = donor.skills
            learnedLevel = [skill.level for skill in recipient.learnedSkills]
            recipient.learnedSkills = donor.learnedSkills
            for index,skill in enumerate(recipient.learnedSkills):
                if index < len(learnedLevel):
                    skill.level = learnedLevel[index]
                elif learnedLevel:
                    skill.level = learnedLevel[-1] + 1 + index - len(learnedLevel)
                else:
                    skill.level = recipient.level.value + index +1
            recipient.alignment = donor.alignment
            recipient.tendency = donor.tendency

            

            
        '''
        Copy the assets from one demonID slot to another.
            Parameters:
                recipient: demon to receive the assets
                donor: demon to donate the assets
        '''
        def obtainAssets(recipient,donor):
            recID = recipient.ind
            sourceID = donor.ind
            
            self.devilAssetArr[recID] = self.copyAssetsToSlot(self.devilAssetArr[recID], self.devilAssetArr[sourceID])
            self.devilUIArr[recID].assetID = self.devilUIArr[sourceID].assetID
            self.devilUIArr[recID].assetString = self.devilUIArr[sourceID].assetString
            self.talkCameraOffsets[recID].demonID = self.talkCameraOffsets[sourceID].demonID
            self.talkCameraOffsets[recID].eyeOffset = self.talkCameraOffsets[sourceID].eyeOffset
            self.talkCameraOffsets[recID].lookOffset = self.talkCameraOffsets[sourceID].lookOffset
            self.talkCameraOffsets[recID].dyingOffset = self.talkCameraOffsets[sourceID].dyingOffset

        
        #To temporarily store the guest data
        copyover = self.playerBossArr[numbers.COPYOVER_DEMON]
        obtainAssets(copyover,guest)

        #Copy from demon to guest
        obtainAttributes(guest,demon)
        obtainAssets(guest,demon)

        #Also copy demon data to other guest slots that are the same person
        for guestSyncID in numbers.GUEST_GROUPS.get(guestID):
            if guestID > numbers.NORMAL_ENEMY_COUNT:
                guestSync = self.playerBossArr[guestSyncID]
            else:
                guestSync = self.compendiumArr[guestSyncID]

            obtainAttributes(guestSync,demon)
            obtainAssets(guestSync,demon)

        #Copy from the holdover/guestCopy to the demon 
        obtainAttributes(demon,guestCopy)
        obtainAssets(demon,copyover)
        
    '''
    Swap guests with demons (or other guests), swapping data from their demon ids (including name) and asset assignments.
    '''
    def swapGuestsWithDemons(self):
        if self.configSettings.swapDemifiend:
            demiFiendEssenceName = self.itemNames[numbers.DEMIFIEND_ESSENCE_ID]
            numbers.GUEST_GROUPS[numbers.GUEST_DEMIFIEND] = []
        validInds = [demon.ind for demon in self.compendiumArr if demon.ind not in numbers.BAD_IDS and 'Mitama' not in demon.name and not demon.name.startswith('NOT USED')]
        #TODO: Currently guests cannot replace each other (essence name swap at least does not work)
        #validInds.extend(numbers.GUEST_GROUPS.keys())

        #Determine random pairing replacements
        swapPairings = {}
        guestList = copy.deepcopy(list(numbers.GUEST_GROUPS.keys()))
        random.shuffle(guestList)
        required = [] #For Debug Purposes! To force certain replacements
        for guest in guestList:
            if guest in validInds:
                validInds.remove(guest)
            
            choice = random.choice(validInds)
            if len(required) > 0:
                choice = required.pop(0)
            validInds.remove(choice)
            swapPairings[choice] = guest   
            
            
        #Swap lore entries
        profileFile = General_UAsset("DevilProfile",paths.CAMP_LN10_STATUS_FOLDER_OUT, readPath=paths.PROFILE_ASSET_IN)

        profileList = profileFile.json['Exports'][0]['Data'][0]['Value']
        originalList = profileFile.originalJson['Exports'][0]['Data'][0]['Value']

        for demonID, guestID in swapPairings.items():
            self.swapDemonWithGuest(demonID,guestID)
            ogProfile = profileList[demonID]
            guestProfile = profileList[guestID]

            demonString = originalList[demonID]['Value'][2]['Value'][0]['CultureInvariantString']
            guestString = originalList[guestID]['Value'][2]['Value'][0]['CultureInvariantString']
            guestStringCopy = copy.deepcopy(guestString)

            for guestSyncID in numbers.GUEST_GROUPS.get(guestID):
                syncProfile =profileList[guestSyncID]
                syncProfile['Value'][2]['Value'][0]['CultureInvariantString'] = demonString

            guestProfile['Value'][2]['Value'][0]['CultureInvariantString'] = demonString
            ogProfile['Value'][2]['Value'][0]['CultureInvariantString'] = guestStringCopy 

        profileFile.write()
        del profileFile

        self.guestReplacements = copy.deepcopy(swapPairings)

        #Contains Guest -> Demon and Demon -> Guest
        swapPairings = {**swapPairings, **{v: k for k, v in swapPairings.items()}}

        for guest, guestGroup in numbers.GUEST_GROUPS.items():
            if guest in guestList:
                for syncedGuest in guestGroup:
                    swapPairings[syncedGuest] = swapPairings[guest]

        if self.configSettings.swapDemifiend:
            numbers.DEMIFIEND_ESSENCE_ID = self.itemNames.index(demiFiendEssenceName)
        for r,d in self.guestReplacements.items():
            recipient = self.getPlayerDemon(r)
            donor = self.getPlayerDemon(d)

            for index,itemName in enumerate(self.originalItemNames):
                if itemName == f"{donor.name}'s Essence":
                    #print("Renaming " + itemName + " to " + f"{recipient.name}'s Essence")
                    self.itemNames[index] = f"{recipient.name}'s Essence"
                elif itemName == f"{recipient.name}'s Essence":
                    #print("Renaming " + itemName + " to " + f"{donor.name}'s Essence")
                    self.itemNames[index] = f"{donor.name}'s Essence"



        if self.configSettings.swapDemifiend:
            numbers.DEMIFIEND_ESSENCE_ID = self.itemNames.index(demiFiendEssenceName)

        #Update Unique skill ownership to new ids
        for skill in self.skillArr:

            if skill.owner and skill.owner.ind in swapPairings.keys():

                skill.owner = Skill_Owner(swapPairings[skill.owner.ind],self.getDemonsCurrentNameByID(swapPairings[skill.owner.ind]))
    '''
    Adds the items of a check to the item debug log.
    '''
    def logItemCheck(self,check):
        category = Check_Type.getCheckString(check.type)
        if category not in self.itemDebugList.keys():
            self.itemDebugList[category] = []
        self.itemDebugList[category].append(check)

            
    
    '''
    Generates a random seed if none was provided by the user and sets the random seed
    '''
    def createSeed(self):
        if self.textSeed == "":
            self.textSeed = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            print('Your generated seed is: {}\n'.format(self.textSeed))

            # Write seed to config.ini
            configur = ConfigParser()
            configur.read('config.ini')
            configur.set('Seed', 'lastSeed', self.textSeed)
            with open('config.ini', 'w') as f:
                configur.write(f)
        random.seed(self.textSeed)
         
         

         
    '''
    Makes the game easier for testing purposes. All enemy hp is set to 10 and Nahobino's stats are increased
    '''
    def applyCheats(self):
        for demon in self.enemyArr:
            demon.stats.HP = 10
            demon.stats.str = 2
            demon.stats.vit = 2
            demon.stats.mag = 2
            demon.stats.agi = 2
        for demon in self.bossArr[numbers.NORMAL_ENEMY_COUNT:]:
            demon.stats.HP = 10
            demon.stats.str = 2
            demon.stats.vit = 2
            demon.stats.mag = 2
            demon.stats.agi = 2
        for index, level in enumerate(self.nahobino.stats):
            self.nahobino.stats[index] = LevelStats(index,999,999,99,99,99,99,99)

    '''
        Compresses the output files using Unreal Pak into rando.pak
        TODO: Determine if this works for non-windows systems. Seemingly not.
    '''
    def applyUnrealPak(self):
        print("Applying Unreal Pak...")
        try:
            os.chdir(paths.UNREAL_PAK_FOLDER)
            os.system(paths.UNREAL_PAK_FILE_NAME + ' ' + paths.OUTPUT_FOLDER_RELATIVE_TO_UNREAL_PAK)
        except:
            print('Automatic Unreal Pak not supported for this system, please manually apply Unreal Pak to "rando" folder to generate rando.pak')

    '''
        Executes the full randomization process including level randomization.
        Parameters:
            config (Settings) 
    '''
    def fullRando(self, config: Settings, testing= False):
        if os.path.exists("rando"):
            shutil.rmtree("rando")
        
        shutil.copytree(paths.PRE_MODIFIED_FILES, paths.PRE_MODIFIED_FILES_OUT)

        writeFolder(paths.DEBUG_FOLDER)

        compendiumBuffer = readBinaryTable(paths.NKM_BASE_TABLE_IN)
        skillBuffer = readBinaryTable(paths.SKILL_DATA_IN)
        otherFusionBuffer = readBinaryTable(paths.UNITE_TABLE_IN)
        encountBuffer = readBinaryTable(paths.ENCOUNT_DATA_IN)
        playGrowBuffer = readBinaryTable(paths.MAIN_CHAR_DATA_IN)
        itemBuffer = readBinaryTable(paths.ITEM_DATA_IN)
        shopBuffer = readBinaryTable(paths.SHOP_DATA_IN)
        eventEncountBuffer = readBinaryTable(paths.EVENT_ENCOUNT_IN)
        missionBuffer = readBinaryTable(paths.MISSION_DATA_IN)
        bossFlagBuffer = readBinaryTable(paths.BOSS_FLAG_DATA_IN)
        battleEventsBuffer = readBinaryTable(paths.BATTLE_EVENTS_IN)
        battleEventUassetBuffer = readBinaryTable(paths.BATTLE_EVENT_UASSET_IN)
        devilAssetTableBuffer = readBinaryTable(paths.DEVIL_ASSET_TABLE_IN)
        abscessBuffer = readBinaryTable(paths.ABSCESS_TABLE_IN)
        devilUIBuffer = readBinaryTable(paths.DEVIL_UI_IN)
        talkCameraBuffer = readBinaryTable(paths.TALK_CAMERA_OFFSETS_IN)
        miracleBuffer = readBinaryTable(paths.MIRACLE_TABLE_IN)
        eventEncountUassetBuffer = readBinaryTable(paths.EVENT_ENCOUNT_UASSET_IN)
        uniqueSymbolBuffer = readBinaryTable(paths.UNIQUE_SYMBOL_DATA_IN)
        chestBuffer = readBinaryTable(paths.CHEST_TABLE_IN)
        mapSymbolParamBuffer = readBinaryTable(paths.MAP_SYMBOL_PARAM_IN)
        mapEventBuffer = readBinaryTable(paths.MAP_EVENT_DATA_IN)
        navigatorBuffer = readBinaryTable(paths.NAVIGATOR_DATA_IN)
        vendingMachineBuffer = readBinaryTable(paths.VENDING_MACHINE_IN)
        message_logic.initDemonModelData()
        bossLogic.initAdditionalBossSkillData()
        self.readDemonNames()
        self.readSkillNames()
        self.readItemNames()
        self.readDataminedEnemyNames()
        self.readEventFlagNames()
        self.fillCompendiumArr(compendiumBuffer)
        self.fillSkillArrs(skillBuffer)
        self.fillFusionChart(otherFusionBuffer)
        self.fillSpecialFusionArr(otherFusionBuffer)
        self.fillBasicEnemyArr(compendiumBuffer)
        self.fillEncountArr(encountBuffer)
        self.fillEncountSymbolArr(encountBuffer)
        self.fillEventEncountArr(eventEncountBuffer)
        self.fillBattleEventArr(battleEventsBuffer)
        self.fillDevilAssetArr(devilAssetTableBuffer)
        self.fillAbscessArr(abscessBuffer)
        self.fillDevilUIArr(devilUIBuffer)
        self.fillTalkCameraArr(talkCameraBuffer)
        self.fillMiracleArr(miracleBuffer)
        
        
        

        #Requires asset arr, eventEncounter and needs to be before bossArr
        self.createOverlapCopies(compendiumBuffer)
        compendiumBuffer = self.writeOverlapCopiesToBuffer(self.overlapCopies, compendiumBuffer)

        self.fillBossArr(compendiumBuffer)
        self.fillPlayerBossArr(compendiumBuffer)
        self.fillBossFlagArr(bossFlagBuffer)
        self.fillNahobino(playGrowBuffer)
            
        #These should be before guest swaps so their skills get assigned the correct level ranges
        skillLevels = self.generateSkillLevelList()
        levelSkillList = self.generateLevelSkillList(skillLevels)

        if config.swapGuestsWithDemons:
            #This needs to happen after playerBossArr and before essence Arr
            self.swapGuestsWithDemons()

        self.fillEssenceArr(itemBuffer)
        self.fillShopArr(shopBuffer)
        self.fillMissionArr(missionBuffer)
        self.fillUniqueSymbolArr(uniqueSymbolBuffer)
        self.fillChestArr(chestBuffer)
        self.fillMimanRewardArr(shopBuffer)
        self.fillVendingMachineArr(vendingMachineBuffer)
        self.fillMapSymbolArr(mapSymbolParamBuffer)
        self.fillConsumableArr(itemBuffer)
        self.fillFusionSkillReqs(skillBuffer)
        self.fillMapEventArr(mapEventBuffer)
        self.fillNavigatorArr(navigatorBuffer)
        
        scriptLogic.modifyEmpyreanKeyEvents(self.scriptFiles)
        
        #self.eventEncountArr = self.addPositionsToEventEncountArr(eventEncountPostBuffer, self.eventEncountArr)
        eventEncountPosFile = self.addPositionsToEncountArr(self.eventEncountArr,"EventEncountPostDataTable",paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_OUT)
        encountPosFile = self.addPositionsToEncountArr(self.encountArr,"EncountPostDataTable",paths.ENCOUNT_POST_DATA_TABLE_UASSET_OUT)
        
        self.findValidBossDemons()
        self.removeBattleTutorials()
        
        if config.fixUniqueSkillAnimations:
            self.removeUniqueSkillAnimations()
        
        self.fusionSkillIDs = list(filter(lambda skill: 800 < skill and skill < 900,numbers.MAGATSUHI_SKILLS))
        magatsuhiSkillsRaces = [self.obtainSkillFromID(skill) for skill in filter(lambda skill: 800 > skill or skill > 900, numbers.MAGATSUHI_SKILLS)]
        if self.configSettings.randomizeMagatsuhiSkillReq:
            magatsuhiSkillsRaces = self.randomizeMagatsuhiSkillReqs()
       
        if config.randomPotentials:
            # if config.fixUniqueSkillAnimations:
            #     self.randomizePotentials(self.compendiumArr, mask=numbers.GUEST_IDS_WORKING_ANIMS_ONLY)
            #     self.randomizePotentials(self.playerBossArr, mask=numbers.GUEST_IDS_WORKING_ANIMS_ONLY)
            # else:
            self.randomizePotentials(self.compendiumArr)
            self.randomizePotentials(self.playerBossArr, mask=numbers.GUEST_IDS)
        
        if self.configSettings.randomDemonStats:
            self.randomizeDemonStats(self.compendiumArr, foes=self.enemyArr)
            self.randomizeDemonStats(self.playerBossArr, mask=numbers.GUEST_IDS)

        self.addAdditionalFusionsToFusionChart(config)

        if config.randomRaces and config.randomDemonLevels:
            self.elementals = self.randomizeRaces(self.compendiumArr)
        elif config.randomRaces:
            result = self.randomizeRacesFixedLevels(self.compendiumArr,otherFusionBuffer)
            self.elementals= result[0]
            otherFusionBuffer = result[1]

        if config.randomDemonLevels:
            newComp = False
            attempts = 0
            while not newComp and attempts < 10:
                newComp = self.shuffleLevel(self.compendiumArr, config,otherFusionBuffer)
                if not newComp:
                    print("Lével resetting and retrying...")
                    self.resetLevelToOriginal(self.compendiumArr)
                    attempts += 1
            if attempts >= 10:
                print('Major issue with generating demon levels and fusions')
                return False
        else: newComp = self.compendiumArr
        
        if config.scaledPotentials:
            self.scalePotentials(newComp)

        if config.randomResists:
            #If we have random resists, we dont need to block demifiend's essence
            numbers.DEMIFIEND_ESSENCE_ID = 29 #Is Unused Item ID

            self.randomizeResistances(newComp)
            self.randomizeResistances(self.playerBossArr, mask=numbers.GUEST_IDS)
            self.randomizeResistances(self.playerBossArr, mask=numbers.PROTOFIEND_IDS)
            #Nahobino shares resistances with first aogami essence
            self.nahobino.resist = self.playerBossArr[numbers.PROTOFIEND_IDS[0]].resist
            #testing = True
            # stuff = []
            # stuff2 = []
            # for i in range(100):
            #     totalResistMap, resistProfiles = self.randomizeResistances(newComp)
            #     stuff.append(totalResistMap)
            #     stuff2.append(resistProfiles)
            
            # newDict = {}
            # for dictionary in stuff:
            #     for element, resists in dictionary.items():
            #         if element not in newDict.keys():
            #             newDict.update({element:resists})
            #         else:
            #             subDict = newDict[element]
            #             for resist,value in resists.items():
            #                 subDict[resist] += value
            # for element, resists in newDict.items():
            #     for resist, value in resists.items():
            #         resists[resist] = value / len(stuff)
            # pprint(newDict)
            # demonSums = []
            # for dlist in stuff2:
            #     for d in dlist:
            #         sumD = 0
            #         for index,value in enumerate(d):
            #             if index == 0:
            #                 sumD += 1.5* value
            #             elif index > 7:
            #                 sumD += value/2
            #             else:
            #                 sumD += value
            #         demonSums.append(sumD)
            # avgDSums = sum(demonSums) / len(demonSums)
            # print(avgDSums)


            

        if config.randomSkills:
            self.adjustSkillSlotsToLevel(newComp)
            self.assignRandomStartingSkill(self.nahobino, levelSkillList, config)
            newComp = self.assignRandomSkills(newComp,levelSkillList, config)
            self.assignRandomSkills(self.playerBossArr,levelSkillList, config, mask=numbers.PROTOFIEND_IDS)
            # if config.fixUniqueSkillAnimations:
            #     self.assignRandomSkills(self.playerBossArr, levelSkillList, config, mask=numbers.GUEST_IDS_WORKING_ANIMS_ONLY)
            # else:
            self.assignRandomSkills(self.playerBossArr, levelSkillList, config, mask=numbers.GUEST_IDS)
        if self.configSettings.forceAllSkills:
            self.debugPrintUnassignedSkills(levelSkillList)
        self.outputSkillSets()
        #self.outputSkillPotentialDist()

        if config.randomInnates:
            self.assignRandomInnates(newComp)
            self.assignRandomInnates(self.playerBossArr, mask=numbers.GUEST_IDS)
            self.assignRandomInnateToNahobino(self.nahobino)

        self.enemyArr = self.adjustBasicEnemyArr(self.enemyArr, newComp)
        if config.randomDemonLevels:
            newSymbolArr = self.adjustEncountersToSameLevel(self.encountSymbolArr, newComp, self.enemyArr, self.encountArr)
            self.adjustTutorialPixie(newComp,self.eventEncountArr)
            self.assignTalkableTones(newComp)
        else:
            newSymbolArr = self.encountSymbolArr
            for demon in self.compendiumArr:
                if demon.ind not in numbers.BAD_IDS and 'Mitama' not in demon.name and 'NOT_USED' not in demon.name:
                    self.encounterReplacements[demon.ind] = demon.ind
        
        
        if config.randomDemonLevels or config.randomRaces:
            self.adjustFusionTableToLevels(self.compendiumArr)
        
        
        if (config.selfRandomizeNormalBosses or config.mixedRandomizeNormalBosses) and not (config.randomMusic or config.checkBasedMusic):
            self.patchMissingBossMusic()
        self.removeIshtarCopies()
        self.syncMaras()
       
        bossLogic.prepareSkillRando(self.skillArr,self.passiveSkillArr, self.innateSkillArr,self.configSettings)
        self.randomizeBosses()

        
        if self.configSettings.swapGuestsWithDemons:
            for demon, guestID in self.guestReplacements.items():
                if guestID < numbers.NORMAL_ENEMY_COUNT:
                    self.encounterReplacements[guestID] = demon
                else:
                    self.bossReplacements[guestID] = demon

        #pprint(bossLogic.resistProfiles)
        if config.selfRandomizeNormalBosses or config.mixedRandomizeNormalBosses:
            self.patchBossFlags()
            bossLogic.patchSpecialBossDemons(self.bossArr, self.configSettings, self.compendiumArr,self.playerBossArr, self.skillReplacementMap, self.guestReplacements)
        elif config.randomizeBossResistances or config.randomizeBossSkills:
            bossLogic.patchSpecialBossDemons(self.bossArr, self.configSettings, self.compendiumArr,self.playerBossArr, self.skillReplacementMap, self.guestReplacements)
        
        self.updateUniqueSymbolDemons()
        if config.scaleBossDamage:
            self.scaleBossDamage()
        
        self.adjustEventEncountMissionConditions(self.eventEncountArr, self.staticEventEncountArr)
        
        if config.selfRandomizeOverworldBosses or config.mixedRandomizeOverworldBosses:
            self.adjustNonEventPunishinFoeMissionConditions(self.uniqueSymbolArr, self.staticUniqueSymbolArr)

        if config.randomMusic:
            self.randomizeEventEncounterTracks()
            
        if config.randomMiracleUnlocks:
            self.randomizeMiracleRewards()
        elif config.randomMiracleCosts: #If randomizing unlocks handle costs there as it is slightly more complicated
            self.randomizeMiracleCosts()
        if config.reverseDivineGarrisons:
            self.reverseDivineGarrisons()

        if config.randomAlignment:
            self.randomizeDemonAlignment(self.compendiumArr)
        
        if config.unlockFusions:
            self.removeFusionFlags()

        if self.configSettings.reduceCompendiumCosts:
            self.reduceCompendiumCosts()

        if self.configSettings.preventEarlyAmbush:
            self.preventEarlyAmbush()
        if self.configSettings.nerfBossHealing:
            self.nerfBossHealing()
        if self.configSettings.expMultiplier != 1:
            self.scaleExpGains()

        self.patchTutorialDaemon()
        
        #self.patchHornOfPlenty()
        #self.patchGirisHead()
        #self.patchHorusHead()
        self.capDiarahanDemonHP()
        self.nullBossTones()
        
        scriptLogic.randomizeDemonJoins(self.encounterReplacements,config.ensureDemonJoinLevel,self.scriptFiles)

        self.assembleNonRedoableItemIDs()
        self.assembleValidityMaps()
        fakeMissions = self.randomizeItemRewards()
        scriptLogic.adjustFirstMimanEventReward(self.scriptFiles)  

        if self.configSettings.randomShopItems:
            self.randomizeShopItems(self.configSettings.scaleItemsPerArea)
        if config.randomShopEssences:
            self.adjustShopEssences(self.shopArr, self.essenceArr, newComp, self.configSettings.scaleItemsPerArea)
        self.replaceSpyglassInShop()
        self.adjustItemPrices()

        if self.configSettings.selfRandomizeNormalBosses or self.configSettings.mixedRandomizeNormalBosses or self.configSettings.selfRandomizeOverworldBosses or self.configSettings.mixedRandomizeOverworldBosses:
            self.patchQuestBossDrops()

        with open(paths.ITEM_DEBUG, 'w', encoding="utf-8") as file:
            for category, checks in self.itemDebugList.items():
                sortedChecks = sorted( checks, key = lambda x : x.ind )
                for check in sortedChecks:
                    items = [check.item] + check.additionalItems
                    for index, item in enumerate(items):
                        if check.hasOdds:
                            line = "Category [" +category +"] CheckName ["+str(check.name) + "] Item [" +item.name + "] Amount [" +str(item.amount) +"] Area [" + numbers.AREA_NAMES[check.area] +"] Odds [" +str(check.odds[index])+"]"
                        else:
                            #self.itemDebugList.append("Category [" +Check_Type.getCheckString(check.type) +"] CheckName ["+str(check.name) + "] ItemType [" + type(item).__name__ +"] Item [" +item.name + "] Amount [" +str(item.amount) +"] Area [" + numbers.AREA_NAMES[check.area] +"]")
                            line = "Category [" +category +"] CheckName ["+str(check.name) + "] Item [" +item.name + "] Amount [" +str(item.amount) +"] Area [" + numbers.AREA_NAMES[check.area] +"]"
                        file.write(line + "\n")

        self.addEntriesToMapSymbolScaleTable()
        self.scaleLargeSymbolDemonsDown()
        self.patchAdramelechReplacementSize()
            
        if DEV_CHEATS:
            self.applyCheats()
        
        self.addAdditionalMapSymbols()
        
        if self.configSettings.randomizeNavigatorStats:
            self.randomizeNavigatorAbilities()
        if self.configSettings.navigatorModelSwap: #Create naviReplacementMap before updating event and mission text
            self.changeNavigatorDemons()
        message_logic.updateItemText(self.encounterReplacements, self.bossReplacements, self.enemyNames, self.compendiumArr,self.fusionSkillIDs, self.fusionSkillReqs, self.skillNames, magatsuhiSkillsRaces, self.configSettings, self.playerBossArr, self.itemNames)
        message_logic.updateSkillDescriptions([self.skillArr, self.passiveSkillArr, self.innateSkillArr],self.compendiumArr,self.enemyNames,self.configSettings)
        message_logic.updateMissionInfo(self.encounterReplacements, self.bossReplacements, self.enemyNames, self.brawnyAmbitions2SkillName, fakeMissions, self.itemNames, self.configSettings.ensureDemonJoinLevel, self.naviReplacementMap, self.playerBossArr, self.compendiumArr,self.progressionItemNewChecks)
        message_logic.updateMissionEvents(self.encounterReplacements, self.bossReplacements, self.enemyNames, self.configSettings.ensureDemonJoinLevel, self.brawnyAmbitions2SkillName, self.naviReplacementMap,self.itemReplacementMap, self.itemNames, self.playerBossArr, self.compendiumArr,self.progressionItemNewChecks, self.guestReplacements)
        #message_logic.addHintMessages(self.bossReplacements, self.enemyNames)
        
        #TODO: Maybe we should find a way to only write model swaps after to create two paks?
        #That way it is easier to switch once issues occur
        if self.configSettings.removeCutscenes or self.configSettings.skipTutorials:
            #Needs to be before cutsceneswap to handle scripts that get edited in both
            self.scriptFiles = scriptLogic.setCertainFlagsEarly(self.scriptFiles, self.mapEventArr, self.eventFlagNames, self.configSettings)

        if self.configSettings.swapCutsceneModels:
            model_swap.updateEventModels(self.encounterReplacements, self.bossReplacements, self.scriptFiles, self.mapSymbolFile, self.configSettings, self.naviReplacementMap, self.guestReplacements)

        self.removeCalcOnlyMapSymbolScales()
        
        
        self.adjustPunishingFoeSpeeds()
        self.addEscapeFindLines()
        if self.configSettings.randomizeVoicesNormal:
            self.randomizeVoiceSets()
        elif self.configSettings.randomizeVoicesChaos:
            self.randomizeVoiceLines()
        
        if len(self.skillReplacementMap) > 0:
            storedNkm = scriptLogic.aiUpdate(self.skillReplacementMap, self.bossArr, self.scriptFiles)
            self.debugSkillReplacements(storedNkm)
            if self.configSettings.allowContemptOfGod:
                self.obtainSkillFromID(numbers.CONTEMPT_OF_GOD_ID).skillType = Translated_Value(8,'')
            for skill in numbers.PHYSICAL_RATE_SKILLS:
                self.obtainSkillFromID(skill).skillType = Translated_Value(14,'')
        
        
        mapSymbolParamBuffer = self.updateMapSymbolBuffer(mapSymbolParamBuffer)
        compendiumBuffer = self.updateBasicEnemyBuffer(compendiumBuffer, self.enemyArr)
        compendiumBuffer = self.updateBasicEnemyBuffer(compendiumBuffer, self.bossArr[numbers.NORMAL_ENEMY_COUNT:])
        compendiumBuffer = self.updateCompendiumBuffer(compendiumBuffer, newComp)
        compendiumBuffer = self.updateCompendiumBuffer(compendiumBuffer, self.playerBossArr[numbers.NORMAL_ENEMY_COUNT:])
        if self.configSettings.buffGuestYuzuru:
            self.patchYuzuruGLStats(compendiumBuffer)
        skillBuffer = self.updateSkillBuffer(skillBuffer, self.skillArr, self.passiveSkillArr, self.innateSkillArr, self.fusionSkillReqs)
        otherFusionBuffer = self.updateOtherFusionBuffer(otherFusionBuffer, self.specialFusionArr)
        encountBuffer = self.updateEncounterBuffer(encountBuffer, newSymbolArr, self.encountArr)
        playGrowBuffer = self.updateMCBuffer(playGrowBuffer, self.nahobino)
        itemBuffer = self.updateEssenceData(itemBuffer,self.essenceArr)
        shopBuffer = self.updateShopBuffer(shopBuffer, self.shopArr, self.mimanRewardsArr)
        eventEncountBuffer = self.updateEventEncountBuffer(eventEncountBuffer,self.eventEncountArr, eventEncountUassetBuffer)
        self.updateEncountPostFile(eventEncountPosFile, self.eventEncountArr)
        bossFlagBuffer = self.updateBossFlagBuffer(bossFlagBuffer)
        battleEventsBuffer = self.updateBattleEventsBuffer(battleEventsBuffer, self.battleEventArr, battleEventUassetBuffer)
        devilAssetTableBuffer = self.updateDevilAssetBuffer(devilAssetTableBuffer, self.devilAssetArr)
        missionBuffer = self.updateMissionBuffer(missionBuffer, self.missionArr)
        devilUIBuffer = self.updateDevilUIBuffer(devilUIBuffer, self.devilUIArr)
        talkCameraBuffer = self.updateTalkCameraBuffer(talkCameraBuffer, self.talkCameraOffsets)
        abscessBuffer = self.updateAbscessBuffer(abscessBuffer)
        miracleBuffer = self.updateMiracleBuffer(miracleBuffer)
        uniqueSymbolBuffer = self.updateUniqueSymbolBuffer(uniqueSymbolBuffer)
        self.updateEncountPostFile(encountPosFile, self.encountArr)
        chestBuffer = self.updateChestBuffer(chestBuffer)
        itemBuffer = self.updateConsumableData(itemBuffer, self.consumableArr)        
        mapEventBuffer = self.updateMapEventBuffer(mapEventBuffer)
        navigatorBuffer = self.updateNavigatorBuffer(navigatorBuffer)
        vendingMachineBuffer = self.updateVendingMachineBuffer(vendingMachineBuffer)

        #self.printOutEncounters(newSymbolArr)
        #self.findUnlearnableSkills(skillLevels)

        writeFolder(paths.BLUEPRINTS_FOLDER_OUT)
        writeFolder(paths.GAMEDATA_FOLDER_OUT)
        writeFolder(paths.BINTABLE_FOLDER_OUT)
        writeFolder(paths.FACILITY_FOLDER_OUT)
        writeFolder(paths.BATTLE_FOLDER_OUT)
        writeFolder(paths.CAMP_FOLDER_OUT)
        writeFolder(paths.MIRACLE_TOP_FOLDER_OUT)
        writeFolder(paths.COMMON_TOP_FOLDER_OUT)
        writeFolder(paths.BLUEPRINTS_MAP_FOLDER_OUT)
        writeFolder(paths.MAP_ENCOUNT_FOLDER_OUT)
        writeFolder(paths.ENCOUNT_MOVER_FOLDER_OUT)
        writeFolder(paths.MOVER_PARAMTABLE_FOLDER_OUT)
        writeFolder(paths.TITLE_TEXTURE_FOLDER_OUT)

        
        self.scriptFiles.writeFiles()
        del self.scriptFiles

        writeBinaryTable(compendiumBuffer.buffer, paths.NKM_BASE_TABLE_OUT, paths.DEVIL_FOLDER_OUT)
        writeBinaryTable(skillBuffer.buffer, paths.SKILL_DATA_OUT, paths.SKILL_FOLDER_OUT)
        writeBinaryTable(otherFusionBuffer.buffer, paths.UNITE_TABLE_OUT, paths.UNITE_FOLDER_OUT)
        writeBinaryTable(encountBuffer.buffer, paths.ENCOUNT_DATA_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(playGrowBuffer.buffer, paths.MAIN_CHAR_DATA_OUT, paths.COMMON_FOLDER_OUT)
        writeBinaryTable(itemBuffer.buffer, paths.ITEM_DATA_OUT, paths.ITEM_FOLDER_OUT)
        writeBinaryTable(shopBuffer.buffer, paths.SHOP_DATA_OUT, paths.FACILITY_TABLE_FOLDER_OUT)
        writeBinaryTable(eventEncountBuffer.buffer, paths.EVENT_ENCOUNT_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(missionBuffer.buffer,paths.MISSION_DATA_OUT,paths.MISSION_FOLDER_OUT)
        writeBinaryTable(bossFlagBuffer.buffer, paths.BOSS_FLAG_DATA_OUT, paths.BOSS_FOLDER_OUT)
        writeBinaryTable(battleEventsBuffer.buffer, paths.BATTLE_EVENTS_OUT, paths.BATTLE_EVENT_FOLDER_OUT)
        writeBinaryTable(battleEventUassetBuffer.buffer,paths.BATTLE_EVENT_UASSET_OUT,paths.BATTLE_EVENTS_OUT)
        writeBinaryTable(devilAssetTableBuffer.buffer, paths.DEVIL_ASSET_TABLE_OUT, paths.ASSET_TABLE_FOLDER_OUT)
        writeBinaryTable(devilUIBuffer.buffer, paths.DEVIL_UI_OUT, paths.UI_GRAPHCIS_FOLDER_OUT)
        writeBinaryTable(talkCameraBuffer.buffer,paths.TALK_CAMERA_OFFSETS_OUT,paths.CAMP_STATUS_FOLDER_OUT)
        writeBinaryTable(abscessBuffer.buffer, paths.ABSCESS_TABLE_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(miracleBuffer.buffer, paths.MIRACLE_TABLE_OUT, paths.MIRACLE_FOLDER_OUT)
        #writeBinaryTable(eventEncountUassetBuffer.buffer, paths.EVENT_ENCOUNT_UASSET_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(uniqueSymbolBuffer.buffer, paths.UNIQUE_SYMBOL_DATA_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(chestBuffer.buffer, paths.CHEST_TABLE_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(mapSymbolParamBuffer.buffer, paths.MAP_SYMBOL_PARAM_OUT, paths.MOVER_PARAMTABLE_FOLDER_OUT)
        writeBinaryTable(mapEventBuffer.buffer, paths.MAP_EVENT_DATA_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(navigatorBuffer.buffer, paths.NAVIGATOR_DATA_OUT, paths.MAP_FOLDER_OUT)
        writeBinaryTable(vendingMachineBuffer.buffer,paths.VENDING_MACHINE_OUT, paths.MAP_FOLDER_OUT)
        #copyFile(paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_IN, paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_OUT, paths.ENCOUNT_POST_TABLE_FOLDER_OUT)
        copyFile(paths.TITLE_TEXTURE_IN, paths.TITLE_TEXTURE_OUT, paths.TITLE_TEXTURE_FOLDER_OUT)
        copyFile(paths.TITLE_TEXTURE_UASSET_IN, paths.TITLE_TEXTURE_UASSET_OUT, paths.TITLE_TEXTURE_FOLDER_OUT)
        
        self.mapSymbolFile.write()
        self.voiceMapFile.write()
        self.naviParamFile.write()
        if not testing:
            self.applyUnrealPak()

    '''
    Prints out a list of all symbol encounters and their encounter battles that do not contain the symbol demons id.
    Used for debugging purposes to prevent camera glitches in battle encounters.
        Parameters:
            newSymbolArr (Array): Array of symbol encounters
    '''
    def printOutEncounters(self, newSymbolArr):
        finalString = ""
        forArray = []
        for entry in newSymbolArr:
            if not entry.symbol.translation.startswith('NOT USED') and not entry.symbol.translation.startswith("NO BASIC ENEMY"):
                finalString = finalString + 'ID: ' + str(entry.ind) + ' ' + 'Symbol: ' + entry.symbol.translation + '\n'
                for ec in entry.encounters:
                    if ec.encounter.ind != 0 and ec.chance > 0 and entry.symbol.ind not in ec.encounter.demons:
                        forArray.append([ec.encounter.ind, ec.encounter.demons])
                        finalString = finalString + 'EID: ' + str(ec.encounter.ind)+ ' Demons: '
                        for demon in ec.encounter.demons:
                            finalString = finalString + demon + ' '
                        finalString = finalString + '\n'
        with open(paths.ENCOUNTERS_DEBUG, 'w', encoding="utf-8") as file:
            file.write(finalString)
            
    def findEncounterBattle(self, id2, symbolEncs):
        for symbol in symbolEncs:
            for ec in symbol.encounters:
                if(ec.encounter.ind == id2):
                    print(symbol)

    '''
    Prints out a list of all normal fusions.
    Used for debugging purposes.
        Parameters:
            fusions (Array): Array of normal fusions
    '''
    def printOutFusions(self, fusions):
        finalString = ""
        for fusion in fusions:
            finalString = finalString + self.compendiumArr[fusion.firstDemon.ind].race.translation + " " + fusion.firstDemon.translation + " + " + self.compendiumArr[fusion.secondDemon.ind].race.translation + " " + fusion.secondDemon.translation + " = " + self.compendiumArr[fusion.result.ind].race.translation + " " + fusion.result.translation + '\n'
            #finalString = finalString +fusion.firstDemon.translation + " + " + fusion.secondDemon.translation + " = " + fusion.result.translation + '\n'
        with open(paths.FUSION_DEBUG, 'a', encoding="utf-8") as file:
            file.write(finalString)
    
    '''
    Output all boss skill replacements to a csv.
    Parameters:
        storedNkm(Dictionary): dictionary of skill replacements for the additional AI files
    '''
    def debugSkillReplacements(self, storedNkm):
        with open(paths.SKILL_REPLACEMENTS, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Demon Name","Demon ID","Script File", "Original Skill ID", "New Skill ID","Old Skill Name","New Skill Name","Old Rank","New Rank"])  # Header

            for demon, replacements in self.skillReplacementMap.items():
                for old_skill, new_skill in replacements.items():
                    ai = str(self.bossArr[demon].AI).zfill(3)
                    fileNames = ["BtlAI_e" +ai]
                    for fileName in fileNames:
                        newRank = "PASSIVE"
                        if isinstance(self.obtainSkillFromID(new_skill),Active_Skill):
                            newRank = self.obtainSkillFromID(new_skill).rank
                        if old_skill >= 999:
                            writer.writerow([self.bossArr[demon].name,demon,fileName, old_skill, new_skill, "NEW", self.obtainSkillFromID(new_skill).name,"NONE",newRank])
                        else:
                            oldRank = "PASSIVE"
                            if isinstance(self.obtainSkillFromID(old_skill),Active_Skill):
                                oldRank = self.obtainSkillFromID(old_skill).rank
                            writer.writerow([self.bossArr[demon].name,demon,fileName, old_skill, new_skill, self.obtainSkillFromID(old_skill).name, self.obtainSkillFromID(new_skill).name,oldRank,newRank])
            for fileName, replacements in storedNkm.items():
                for old_skill, new_skill in replacements.items():
                    newRank = "PASSIVE"
                    if isinstance(self.obtainSkillFromID(new_skill),Active_Skill):
                        newRank = self.obtainSkillFromID(new_skill).rank
                    if old_skill >= 999:
                        writer.writerow([fileName,-1,fileName, old_skill, new_skill,"NEW", self.obtainSkillFromID(new_skill).name,"NONE",newRank])
                    else:
                        oldRank = "PASSIVE"
                        if isinstance(self.obtainSkillFromID(old_skill),Active_Skill):
                            oldRank = self.obtainSkillFromID(old_skill).rank
                        writer.writerow([fileName,-1,fileName, old_skill, new_skill, self.obtainSkillFromID(old_skill).name, self.obtainSkillFromID(new_skill).name,oldRank,newRank])
        
    def debugPrintUnassignedSkills(self, levelList):
        sortedDemons = sorted(self.compendiumArr, key=lambda demon: demon.level.value)
        levelAggregrate = []
        for index, level in enumerate(levelList):
            if index == 0:
                #Prevents Magatsuhi skills from being in demons skill pools
                continue
            for skill in level:
                levelAggregrate.append(skill)
        allSkillIDs = {skill.ind for skill in levelAggregrate}
        allSkills = []
        for ind in allSkillIDs:
                allSkills.append(next(skill for skill in levelAggregrate if skill.ind == ind))
        
        for demon in sortedDemons:
            if "NOT USED" in demon.name or demon.ind in numbers.INACCESSIBLE_DEMONS:
                continue
            for skill in demon.skills:
                if skill.ind in allSkillIDs:
                    allSkillIDs.remove(skill.ind)
            for skill in demon.learnedSkills:
                if skill.ind in allSkillIDs:
                    allSkillIDs.remove(skill.ind)
        
        skillID = self.nahobino.startingSkill
        if skillID in allSkillIDs:
                allSkillIDs.remove(skillID)
        for protoFiend in self.playerBossArr:
            if protoFiend.ind in numbers.PROTOFIEND_IDS:
                for skill in protoFiend.skills:
                    if skill.ind in allSkillIDs:
                        allSkillIDs.remove(skill.ind)
        for guest in self.playerBossArr:
            if guest.ind in numbers.GUEST_IDS:
                for skill in guest.skills:
                    if skill.ind in allSkillIDs:
                        allSkillIDs.remove(skill.ind)
                for skill in guest.learnedSkills:
                    if skill.ind in allSkillIDs:
                        allSkillIDs.remove(skill.ind)

        if len(allSkillIDs) > 0:
            print("At least one skill was not assigned to a demon")
        for skillID in allSkillIDs:
            print(translation.translateSkillID(skillID,self.skillNames) + " " + str(skillID))

    def outputSkillSets(self):
        sortedDemons = sorted(self.compendiumArr, key=lambda demon: demon.level.value)
        with open(paths.SKILL_SET_DEBUG, 'w', encoding="utf-8") as file:
            for demon in sortedDemons:
                if "NOT USED" in demon.name or demon.ind in numbers.INACCESSIBLE_DEMONS:
                    continue
                skillString = "[" + str(demon.ind) + "](" + str(demon.level.value) +") " + demon.name + ": "
                for skill in demon.skills:
                    if skill.ind == 0:
                        continue
                    skillString = skillString + translation.translateSkillID(skill.value, self.skillNames) + "/"
                for skill in demon.learnedSkills:
                    if skill.ind == 0:
                        continue
                    skillString = skillString + translation.translateSkillID(skill.value, self.skillNames)+ "(" + str(skill.level) + ")" + "/"
                file.write(skillString + "\n")
            for demon in self.playerBossArr:
                if demon.ind in numbers.GUEST_IDS:
                    skillString = "[" + str(demon.ind) + "](" + str(demon.level.value) +") " + demon.name + ": "
                    for skill in demon.skills:
                        if skill.ind == 0:
                            continue
                        skillString = skillString + translation.translateSkillID(skill.value, self.skillNames) + "/"
                    for skill in demon.learnedSkills:
                        if skill.ind == 0:
                            continue
                        skillString = skillString + translation.translateSkillID(skill.value, self.skillNames)+ "(" + str(skill.level) + ")" + "/"
                    file.write(skillString + "\n")
                if demon.ind in numbers.PROTOFIEND_IDS:
                    skillString = "[" + str(demon.ind) + "](" + str(demon.level.value) +") " + "Aogami/Tsukuyomi Essence" + ": "
                    for skill in demon.skills:
                        if skill.ind == 0:
                            continue
                        skillString = skillString + translation.translateSkillID(skill.value, self.skillNames) + "/"
                    for skill in demon.learnedSkills:
                        if skill.ind == 0:
                            continue
                        skillString = skillString + translation.translateSkillID(skill.value, self.skillNames)+ "(" + str(skill.level) + ")" + "/"
                    file.write(skillString + "\n")

    def outputSkillPotentialDist(self):
        skillDist = {}
        n = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
        for g in n:
            skillDist[g] = 0
        sortedDemons = sorted(self.compendiumArr, key=lambda demon: demon.level.value)
        for demon in sortedDemons:
            potentials = demon.potential
            if "NOT USED" in demon.name or demon.ind in numbers.INACCESSIBLE_DEMONS:
                continue
            for skill in demon.skills:
                if skill.ind == 0:
                    continue
                realSkill = self.obtainSkillFromID(skill.ind)
                skillStructure = self.determineSkillStructureByID(skill.ind)
                if skillStructure == "Active":
                    potentialType = realSkill.potentialType.translation
                    potentialValue = self.obtainPotentialByName(potentialType, potentials)
                    skillDist[potentialValue] += 1
                else:
                    skillDist[0] += 1
            for skill in demon.learnedSkills:
                if skill.ind == 0:
                    continue
                realSkill = self.obtainSkillFromID(skill.ind)
                skillStructure = self.determineSkillStructureByID(skill.ind)
                if skillStructure == "Active":
                    potentialType = realSkill.potentialType.translation
                    potentialValue = self.obtainPotentialByName(potentialType, potentials)
                    skillDist[potentialValue] += 1
                else:
                    skillDist[0] += 1
        total = 0
        for p,v in skillDist.items():
            total += v
        for p,v in skillDist.items():
            trueValue = v / total
            skillDist[p] = format(trueValue,'.2%')
        print(skillDist)

                    
if __name__ == '__main__':
    rando = Randomizer()
    print('Warning: This is an early build of the randomizer and some things may not work as intended. Performance will be somewhat worse than vanilla SMTVV')
    print('Welcome to the SMTVV Rando v1.052. This version was created with game version 1.03 and will likely not work with other versions of SMTVV')
    try:
        rando.configSettings, rando.textSeed = gui.createGUI(rando.configSettings)
        if rando.configSettings.swapCutsceneModels:
            print('Cutscene Model Swaps on. This may take up to an hour to finish running. Please wait...')
        rando.createSeed()
        
        rando.fullRando(rando.configSettings)
        if not rando.configSettings.fixUniqueSkillAnimations:
            print('"Fix unique skill animations" patch not applied. If the game appears to hang during a battle animation, press the skip animations button')
        print('\nRandomization complete! Place rando.pak in the Project/Content/Paks/~mods folder of your SMTVV game directory')
        print('BossSpoilerLog, encounterResults, fusionResults and itemLog can be found in the debug folder')
       
    except RuntimeError:
        print('GUI closed - randomization was canceled')
    except Exception as e:
        traceback.print_exc()
        print(e)
        print('Unexpected error occured, randomization failed.\nPlease retry with different settings or send a screenshot of this error to the SMT Rando Discord\n https://discord.gg/d25ZAha')
    input('Press [Enter] to exit')
