from util.binary_table import Table
from base_classes.demons import Compendium_Demon, Enemy_Demon, Stat, Stats, Item_Drop, Item_Drops, Demon_Level, Boss_Flags, Duplicate, Encounter_Spawn
from base_classes.skills import Active_Skill, Passive_Skill, Skill_Condition, Skill_Conditions, Skill_Level, Skill_Owner, Fusion_Requirements
from base_classes.fusions import Normal_Fusion, Special_Fusion, Fusion_Chart_Node
from base_classes.encounters import Encounter_Symbol, Encounter, Possible_Encounter, Event_Encounter, Battle_Event, Unique_Symbol_Encounter, Ambush_Type
from base_classes.base import Translated_Value, Weight_List
from base_classes.nahobino import Nahobino, LevelStats
from base_classes.item import Essence, Shop_Entry, Miman_Reward, Reward_Item, Item_Chest, Consumable_Item, Gift_Item, Gift_Pool
from base_classes.quests import Mission, Mission_Reward, Mission_Condition, Mission_Container
from base_classes.settings import Settings
from base_classes.miracles import Abscess, Miracle
from base_classes.demon_assets import Asset_Entry, Position, UI_Entry, Talk_Camera_Offset_Entry
from base_classes.map_demons import Map_Demon
import script_logic as scriptLogic
import message_logic as message_logic
import util.numbers as numbers
import util.paths as paths
import util.translation as translation
import boss_logic as bossLogic
import math
import os
import random
import gui
import string
import pandas as pd
import copy
import shutil
import traceback

RACE_ARRAY = ["None", "Unused", "Herald", "Megami", "Avian", "Divine", "Yoma", "Vile", "Raptor", "Unused9", "Deity", "Wargod", "Avatar", "Holy", "Genma", "Element", "Mitama", "Fairy", "Beast", "Jirae", "Fiend", "Jaki", "Wilder", "Fury", "Lady", "Dragon", "Kishin", "Kunitsu", "Femme", "Brute", "Fallen", "Night", "Snake", "Tyrant", "Drake", "Haunt", "Foul", "Chaos", "Devil", "Meta", "Nahobino", "Proto-fiend", "Matter", "Panagia", "Enigma", "UMA", "Qadistu", "Human", "Primal", "Void"]
DEV_CHEATS = False

class Randomizer:
    def __init__(self):
        self.maccaMod = numbers.getMaccaValues()
        self.expMod = numbers.getExpValues()

        self.compendiumNames = []
        self.skillNames = []
        self.itemNames = []

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
        self.protofiendArr = []
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
        self.bossSymbolReplacementMap = {}
        self.validBossDemons = set()
        self.essenceBannedBosses = set()
        self.updatedMissionConditionIDs = []
        self.encounterReplacements = {}
        self.bossReplacements = {}
        self.pressTurnChance = 0
        self.brawnyAmbitions2SkillName = "Puncture Punch"
        self.fusionSkillIDs = []
        self.fusionSkillReqs = []
        self.alreadyAssignedSkills = set()
        self.scriptFiles = scriptLogic.Script_File_List()

        self.nahobino = Nahobino()
        
        self.configSettings = Settings()
        self.textSeed = ""

        self.elementals = [155,156,157,158]
        
        self.dummyEventIndex = 0
        
        
    '''
    Reads a file containing game data into a Table with a bytearray
        Parameters:
            filePath (string): The path to the file to read.
        Returns: 
            The buffer containing file data as a Table
    '''
    def readBinaryTable(self, filePath):
        fileContents = Table(filePath)
        return fileContents
    
    '''
    Reads the text file containing Character Names and filters out just the names and saves all names in array compendiumNames.
        Returns: 
            The buffer containing CharacterNames
    '''
    def readDemonNames(self):
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
    Writes the given Buffer to the file specified by filePath
        Parameters:
            result (Buffer): The data to write
            filePath (string): The path to write the file at
            folderPath (string): The path the folder where the file is, used to check if the folder exists
    '''
    def writeBinaryTable(self, result, filePath, folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        with open(filePath, 'wb') as file:
            file.write(result)
    '''
    Creates the folder at the given path if it does not exist.
        Parameters:
            folderPath (string): The path of the folder
    '''
    def writeFolder(self, folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
    '''
    Copies a specified file to another location.
        Parameters:
            toCopy (string): The path for the file to copy
            pasteTo (string): The path to write the file at
            folderPath (string): The path the folder where the file is, used to check if the folder exists
    '''
    def copyFile(self, toCopy, pasteTo, folderPath):
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)
        if not os.path.exists(pasteTo):
            shutil.copy(toCopy,pasteTo)
            
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
            'encounterSpawn': offset + 0x1AC
        }
        if isBoss:
            locations['encounterSpawn'] = offset + 0x1CA #I'm not sure if one was a typo but there was a difference in how the player boss arr reads this
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
        elif isBoss:
            demon.name = self.enemyNames[demon.nameID]
        else:
            demon.name = self.compendiumNames[demon.nameID]
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
        demon.resist.electric = Translated_Value(NKMBaseTable.readWord(locations['innate'] + 4 * 4),
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
                if ownerID < 0:
                    ownerName = "Nahobino"
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
                if ownerID < 0:
                    ownerName = "Nahobino"
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
        for index in range(37401):
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
            demon.name = self.compendiumNames[demon.nameID]
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
        demon.resist.electric = Translated_Value(enemyData.readWord(locations['innate'] + 4 * 4),
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
        for index in range(2081):
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
                encId = encounters.readHalfword(locations['encounter1'] + 4 * i)
                possEnc.append(Possible_Encounter(encId, self.encountArr[encId], encounters.readHalfword(locations['encounter1Chance'] + 4 * i)))

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

        start = 0x32D55
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
            'affStart': 0x2B10,
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
        self.nahobino.resist.electric = Translated_Value(playGrow.readWord(locations['affStart'] + 4 *3),translation.translateResist(playGrow.readWord(locations['affStart'] + 4 *3)))
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
            essence.demon = Translated_Value(items.readWord(offset),self.compendiumNames[items.readWord(offset)])
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
            entry.unlock = Translated_Value(shopData.readDblword(offset +4), translation.translateFlag(shopData.readDblword(offset+4)))

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
        for index in range(252):
            offset = start + size * index
            encounter = Event_Encounter()
            encounter.ind = data.readByte(offset + 0x20) 
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

            self.eventEncountArr.append(encounter)
            self.staticEventEncountArr.append(copy.deepcopy(encounter))
        
    '''
    Fills the array bossFlagArr with data on boss flags.
        Parameters:
            data (Buffer) the buffer containing all boss flag data
    '''
    def fillBossFlagArr(self, data):
        start = 0x45
        size = 0x24
        
        for index in range(130):
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
    Fills the array protofiendArr with data on all protofiends that serve as the source for their essence data.
        Parameters:
            NKMBaseTable (Buffer) the buffer containing all playable demon data
    '''
    def fillProtofiendArr(self, NKMBaseTable):
        relevantIDs = numbers.PROTOFIEND_IDS

        
        demonOffset = 0x1D0
        startValue = 0x69 + relevantIDs[0] * demonOffset

        for index, demonID in enumerate(relevantIDs):
            offset = startValue + demonOffset * index
            locations = {
                'level': offset,
                'nameID': offset - 4,
                'firstSkill': offset + 0x70,
                'potential': offset + 0X174,
                'HP': offset + 0x1C
            }

            #Then read the list of initial skills learned
            listOfSkills = []
            for i in range(8):
                skillID = NKMBaseTable.readWord(locations['firstSkill'] + 4 * i)
                if skillID != 0:
                    listOfSkills.append(Translated_Value(skillID, translation.translateSkillID(skillID, self.skillNames)))
            
            demon = Compendium_Demon()
            demon.ind = demonID
            demon.nameID = NKMBaseTable.readWord(locations['nameID'])
            demon.name = self.compendiumNames[demon.nameID]
            demon.offsetNumbers = locations
            demon.level = Demon_Level(NKMBaseTable.readWord(locations['level']), NKMBaseTable.readWord(locations['level']))
            demon.skills = listOfSkills
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
            

            self.protofiendArr.append(demon)
    '''
    Fills the array missionArr with data on all missions.
        Parameters:
            data (Buffer) the buffer containing all mission data
    '''
    def fillMissionArr(self, data):

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
                'scaleFactor': offset + 0x74
            }
            demonID = data.readWord(offset)
            walkSpeed = data.readFloat(locations['walkSpeed'])
            scaleFactor = data.readFloat(locations['scaleFactor'])
            
            mapDemon = Map_Demon()
            mapDemon.offsetNumbers = locations
            mapDemon.demonID = demonID
            mapDemon.walkSpeed = walkSpeed
            mapDemon.scaleFactor = scaleFactor
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
                if skill != 928:
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
        self.fusionSkillIDs = newFusionSkills
        self.fusionSkillReqs = self.updateFusionSkillRequirements(newFusionSkills)
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
        #If the skills aren't supposed to be scaled based on level, assemble list where each valid skill appears exactly once
        if not settings.scaledSkills:
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
        if not mask:
            sortedComp = sorted(comp, key=lambda demon: demon.level.value)
        else:
            sortedComp = comp

        #For every demon...
        for demon in sortedComp:
            if mask and demon.ind not in mask:
                continue
            possibleSkills = []
            if settings.scaledSkills:
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
        
            #Create the weighted list of skills and update it with potentials if necessary
            weightedSkills = self.createWeightedList(possibleSkills)
            if settings.potentialWeightedSkills:
                weightedSkills = self.updateWeightsWithPotential(weightedSkills, demon.potential, demon)

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
                        rng = self.weightedRando(weightedSkills.values, weightedSkills.weights)
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
                        attempts -= 1
                    skillAddition = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
                    totalSkills.append(skillAddition)
                    self.alreadyAssignedSkills.add(rng)
                    demon.skills[index] = skillAddition
                #Randomly assign learnable skills; same justifications as starting skills
                for index in range(len(demon.learnedSkills)):
                    foundSkill = False
                    rng = 0
                    attempts = 100
                    while not foundSkill:
                        rng = self.weightedRando(weightedSkills.values, weightedSkills.weights)
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
                        attempts -= 1
                    skillAddition = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
                    totalSkills.append(skillAddition)
                    self.alreadyAssignedSkills.add(rng)
                    demon.learnedSkills[index] = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames), level=demon.learnedSkills[index].level)
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

    '''
    Assigns every protofiend new skills randomized using weights based on the passed settings.
    The range of skills available can either be all or level ranges around the protofiends level.
    Additionally, the weights are either the same for every skill or adjusted based on level range or potential and stat of demon.
    Furthermore the process ensures that each demon starts with at least one active skill.
        Parameters: 
            comp (Array): The array of demons
            levelList (Array(Skill_Level)): The list of levels and their learnable skills
            settings (Settings): settings set in gui
        Returns:
            The edited compendium
    '''
    def assignRandomSkillsToProtofiend(self, protofiends, levelList, settings):
         #If the skills aren't supposed to be scaled based on level, assemble list where each valid skill appears exactly once
        if not settings.scaledSkills:
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
        
        for protofiend in protofiends:
            possibleSkills = []
            if settings.scaledSkills:
                #get all skills that can be learned at the demons level
                if protofiend.level.value > 0:
                    possibleSkills = levelList[protofiend.level.value]
                #And add the skills learnable at up to 3 level below and above the demons level
                if protofiend.level.value < 99:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value + 1]
                if protofiend.level.value > 1:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 1]
                if protofiend.level.value > 2:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 2]
                if protofiend.level.value > 3:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 3]
                if protofiend.level.value < 98:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value + 2]
                if protofiend.level.value < 97:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value + 3]
                #Increase skill pool for demons above level 70 due to diminishing demon numbers
                if protofiend.level.value > 70:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 4]
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 5]
                #Increase skill pool for demons above level 90 due to diminishing demon numbers
                if protofiend.level.value > 90:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 6]
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 7]
                    possibleSkills = possibleSkills + levelList[protofiend.level.value - 8]
                #Increase skill pool for demons at level 1 due to low number of available skills
                if protofiend.level.value == 1:
                    possibleSkills = possibleSkills + levelList[protofiend.level.value + 4]
                    possibleSkills = possibleSkills + levelList[protofiend.level.value + 5]
            else:
                #No level scaling so copy list of all skilsl
                possibleSkills = allSkills.copy()

             #Create the weighted list of skills and update it with potentials if necessary
            weightedSkills = self.createWeightedList(possibleSkills)
            totalSkills = []
            #If there are skills to be learned
            if len(weightedSkills.values) > 0:

                #For every skill...
                for index in range(len(protofiend.skills)):
                    foundSkill = False
                    if protofiend.skills[index].value == 0:
                        # Don't set empty skill slots 
                        continue
                    rng = 0
                    attempts = 100
                    while not foundSkill:
                        # until valid skill is found
                        rng = self.weightedRando(weightedSkills.values, weightedSkills.weights)
                        if attempts <= 0:
                            print("Something went wrong in skill rando at level " + str(protofiend.level.value))
                            weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                            foundSkill = True
                            break
                        # Ensure Demon has at least one active skill and no skill appears twice
                        if not any(e.ind == rng for e in totalSkills) and self.ensureAtLeastOneActive(totalSkills, protofiend, rng):
                            #Check if skill passes additional conditions or skip that check if skills are not supposed to be weighted by stats and potentials
                            if not settings.potentialWeightedSkills or (self.checkAdditionalSkillConditions(self.obtainSkillFromID(rng), totalSkills, protofiend)):
                                if self.checkUniqueSkillConditions(self.obtainSkillFromID(rng),protofiend,self.compendiumArr,settings):
                                    if rng in numbers.MAGATSUHI_SKILLS: #only 1 magatsuhi skill assigned to skill set
                                        for weightIndex,checkSkill in enumerate(weightedSkills.values):
                                            if checkSkill in numbers.MAGATSUHI_SKILLS:
                                                weightedSkills.weights[weightIndex] = 0
                                    foundSkill = True
                                    weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                        attempts -= 1
                    skillAddition = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
                    totalSkills.append(skillAddition)
                    protofiend.skills[index] = skillAddition
    
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
    Update the weights in the weightList by applying the given skill potentials to the skills
        Parameters:
            weightList (Array): Array with sub-arrays weights and values
            potentials (Potentials): Object containing the data of skill potentials of a demon
        Returns:
            weightList updated with the potentials
    '''
    def updateWeightsWithPotential(self, weightList, potentials, demon):
        #For every skill in weight list
        newWeights = []
        for index, element in enumerate(weightList.values):
            newWeight = weightList.weights[index]
            skill = self.obtainSkillFromID(element)
            if skill.name == 'Filler':
                continue #Exclude filler skill because it has Null values
            if skill.ind in numbers.MAGATSUHI_SKILLS:
                newWeights.append(newWeight)
                continue  #Magatsuhi skills are not effected by potential and keep their weight
            skillStructure = self.determineSkillStructureByID(skill.ind)
            #Passive skills do not have a corresponding potential by default so we need to handle them seperately
            if skillStructure == "Active":
                potentialType = skill.potentialType.translation
                potentialValue = self.obtainPotentialByName(potentialType, potentials)
                if potentialType == "Phys":
                    additionalWeight = potentialValue
                else:
                    additionalWeight =  math.ceil(numbers.POTENTIAL_WEIGHT_MULITPLIER * potentialValue)
                #TODO: Maybe use a different multiplier for phys skills since there are so many?
                if skill.skillType.value == 0 and demon.stats.str.start < demon.stats.mag.start:
                    additionalWeight = additionalWeight - numbers.SKILL_STAT_PENALTY_WEIGHT
                elif skill.skillType.value == 1 and demon.stats.str.start > demon.stats.mag.start:
                    additionalWeight = additionalWeight - numbers.SKILL_STAT_PENALTY_WEIGHT
                
                if additionalWeight < 0:
                    newWeight = 0
                else:
                    newWeight = newWeight + additionalWeight
            else:
                #Placeholder in case I want to modify weights for passive skills
                pass
            newWeights.append(newWeight)

        return Weight_List(weightList.values, newWeights, weightList.names)

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
            percentages = []
            for i in range(random.randint(3,9)):
                percentages.append(random.randint(0,50))

            while sum(percentages) != 100:
                randomN = random.randint(0,len(percentages)-1)
                if sum(percentages) < 100:
                    percentages[randomN] += 1
                else:
                    percentages[randomN] -= 1
            negatives = 1
            for index,percentage in enumerate(percentages):
                if random.randrange(0,100) < (100 / negatives) and negatives < (len(percentages)/2):
                    percentages[index] = percentage * -1
                    negatives += 1

            while len(percentages) < 11:
                percentages.append(0)
            percentages = sorted(percentages, key=lambda x: random.random())
            newPotentials = []
            #follows rough trends of potentials in base demons
            absPotAmount = round(numbers.POTENTIAL_SCALING_FACTOR * demon.level.value + numbers.BASE_POTENTIAL_VALUE)
            for index,percentage in enumerate(percentages):
                percentage = percentage / 100
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
    Based on array of skills creates two arrays where each skill is only included once.
    Weight depends of if skill has already been assigned in the randomization process and if they are a magatsuhi skill.
        Parameters:
            possiblSkills (Array): Array of skills
        Returns:
            An object with an array of values and an array of weights and an array of names for the skills
    '''
    def createWeightedList(self, possibleSkills):
        ids = []
        prob = []
        names = []
        #for every skill...
        for skill in possibleSkills:
            if skill.ind not in ids:
                #else push value and base weight 
                ids.append(skill.ind)
                if skill.ind in numbers.MAGATSUHI_SKILLS:
                    probability = numbers.MAGATSUHI_SKILL_WEIGHT
                else:
                    probability = numbers.SKILL_WEIGHT
                if skill.ind in self.alreadyAssignedSkills:
                    probability = probability - numbers.SKILL_PENALTY_WEIGHT
                prob.append(probability)
                names.append(skill.name)
        # for skill in possibleSkills:
        #     if skill.ind in ids and skill.ind not in numbers.MAGATSUHI_SKILLS: #Magatsuhi Skills should always have weight of 1
        #         prob[ids.index(skill.ind)] += 1
        #     elif skill.ind not in ids:
        #         #else push value and base weight 
        #         ids.append(skill.ind)
        #         prob.append(1)
        #         names.append(skill.name)
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
        for fusion in fusions:
            buffer.writeHalfword(fusion.demon1.value, fusion.baseOffset + 2)
            buffer.writeHalfword(fusion.demon2.value, fusion.baseOffset + 4)
            buffer.writeHalfword(fusion.demon3.value, fusion.baseOffset + 6)
            buffer.writeHalfword(fusion.demon4.value, fusion.baseOffset + 8)
            buffer.writeHalfword(fusion.result.value, fusion.baseOffset + 10)
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
        return buffer
    
    '''
    Write the values in symbolArr to the respective locations in the buffer, as well as updated boss encounters
        Parameters:
            buffer (Table): Buffer of the EncountData table
            symbolArr (Array): contains data on all symbol encounters and their encounter battles
        Returns:
            The updated buffer
    '''
    def updateEncounterBuffer(self, buffer, symbolArr):
        #For each overworld encounter
        for symbolEntry in symbolArr:
            offsets = symbolEntry.offsetNumbers
            buffer.writeHalfword(symbolEntry.symbol.ind, offsets['symbol'])
            #go through its list of encounter battles
            for encounterEntry in symbolEntry.encounters:
                enc = encounterEntry.encounter
                encOffsets = enc.offsetNumbers
                #and write the data for every demon
                for index, demon in enumerate(enc.demons):
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
            if ind >= 252:
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
    Writes the position values from an event encouter or encounter array to their respective locations in the table buffer.
        Parameters:        
            buffer (Table): binary table
            evEncount (Array): list of encounters
    '''
    def updateEventEncountPostBuffer(self,buffer,evEncount):
        for ind, enc in enumerate(evEncount):
            if ind < 3000: #length of EncountPostBuffer is 3000
                for index, pos in enumerate(enc.positions.demons):
                    buffer.writeFloat(pos.x, enc.positions.offsetNumber['demon1'] + 0xC * index)
                    buffer.writeFloat(pos.y, enc.positions.offsetNumber['demon1'] + 4 + 0xC * index)
                for index, pos in enumerate(enc.positions.addDemons):
                    buffer.writeFloat(pos.x, enc.positions.offsetNumber['addDemon1'] + 0xC * index)
                    buffer.writeFloat(pos.y, enc.positions.offsetNumber['addDemon1'] + 4 + 0xC * index)
        return buffer
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
    Writes the values from the protofiend array to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            protofiends (Array)
    '''
    def updateProtofiendBuffer(self, buffer, protofiends):
        for demon in protofiends:
            #Write the id of the demons skills to the buffer
            for index, skill in enumerate(demon.skills):
                buffer.writeWord(skill.ind, demon.offsetNumbers['firstSkill'] + 4 * index)
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
    For a list of values and weights, outputs a random value taking the weight of values into account
        Parameters:
            values (Array): Array of numbers
            weights (Array) Array of numbers, weights belonging to values with the same index
        Returns:
            The randomly chosen value
    '''
    def weightedRando(self, values, weights):
        total = sum(weights)
        #Generate random number with max being the total weight
        rng = random.randint(0, total)

        cursor = 0
        #Add weights together until we reach random number and then apply that value
        for i in range(len(weights)):
            cursor += weights[i]
            if cursor >= rng:
                return values[i]
            
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
    def adjustFusionTableToLevels(self, fusions, comp):
        #Recreate the fusion array in its original form
        #Mostly as a way of testing
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

    '''
    Adjusts the special fusions in specialFusionArr with the new fusions based on the randomization in shuffleLevel.
    Also sets the fusability flags accordingly.
        Parameters:
            fusions (Array) Array containing data on the new special fusions
            comp (Array) Array containing data on all playable demons
    '''
    def adjustSpecialFusionTable(self,fusions,comp):
        for index, fusion in enumerate(fusions):
            #Set original demons fusability to 0
            # seperate in case an og special fusion is still a special version
            replaced = self.specialFusionArr[index]
            comp[replaced.result.ind].fusability = 0 

        for index, fusion in enumerate(fusions):
            replaced = self.specialFusionArr[index]
            #Set new result demons fusability to 0
            comp[fusion.result.value].fusability = 257

            replaced.resultLevel = fusion.resultLevel
            replaced.demon1 = fusion.demon1
            replaced.demon2 = fusion.demon2
            replaced.demon3 = fusion.demon3
            replaced.demon4 = fusion.demon4
            replaced.result = fusion.result
    
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
            raceIndex = self.weightedRando(raceIndeces, raceWeights)
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
    Returns: the ids of the 4 new demons of the Element race
    '''
    def randomizeRacesFixedLevels(self, comp):

        for demonInd in self.elementals:
            #Reset compendium costs for original elements
            comp[demonInd].compCostModifier = 100

        relevantDemons = [demon for demon in comp if demon.ind not in numbers.BAD_IDS and "Mitama" not in demon.name and not demon.name.startswith('NOT') ]
        specialFusions = [demon.ind for demon in comp if demon.fusability > 256] #List of demon ids that are fused as a special fusion

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
            raceIndex = self.weightedRando(raceIndeces, raceWeights)
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
        #Check if fusions of the base 10 demons can result in each other, and note the fusions as such
        for b in base:
            possibleFusions = [f for f in fusions if f[2].race.translation == b.race.translation and f[2].ind == -1 and f[2].level.value <= b.level.value]
            for p in possibleFusions:
                p[2] = b

        attempts = 0
        #until no relevant demon left or no valid race assignment can be created
        while len(relevantDemons) > 0 and attempts < 300:
            # grab the next lowest level demon
            demon = relevantDemons[0]
            #Check which races can be assigned to the demon
            validRaces = list({fusion[2].race.value for fusion in fusions if fusion[2].ind == -1 and raceWeights[fusion[2].race.value] > 0 and fusion[2].level.value <= demon.level.value })
            validWeights = [weight for index, weight in enumerate(raceWeights) if index in validRaces]
            raceIndex = self.weightedRando(validRaces,validWeights) #random weighted race
            
            #Check if a demon of the same lavel is already assigned to race
            if demon.level.value in raceLevels[raceIndex]:
                attempts +=1
                continue
            #Check if demon is special fusion
            if demon.ind in specialFusions:
                raceIndex = self.weightedRando(raceIndeces, raceWeights)
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
        return elementals      
        
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
                newSkills.append(Translated_Value(newID, translation.translateSkillID(newID, self.skillNames)))

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
            
            newFoe = Enemy_Demon()
            newFoe.ind = enemy.ind
            newFoe.name = enemy.name
            newFoe.offsetNumbers = enemy.offsetNumbers
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
            newFoe.instakillRate = enemy.instakillRate
            newFoe.drops = newDrops
            newFoe.oldDrops = enemy.drops
            newFoe.innate = playableEqu.innate   #copy innate from player version
            newFoe.resist = enemy.resist
            newFoe.potential = playableEqu.potential
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
    def adjustEncountersToSameLevel(self, symbolArr, comp, enemyArr):

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
            symbolFoe = None
            currentLV = getFoeWithID(encount.symbol.ind, foes).originalLevel
            #get enemies at level which have not been featured as a replacement
            #ensures 1:1 replacement
            possibilities = [p for p in getEnemiesAtLevel(currentLV) if not any(r[1] == p.ind for r in replacements)]
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

            #For every encounter battle for the current symbol encounter
            for form in replaceEnc.encounters:
                #That can actually appear
                if form.chance > 0:
                    formation = form.encounter
                    #and is not the basic dummy encounter
                    if formation.ind != 0:

                        #Check if this encounter has been updated already
                        if formation.updated:
                            #check if symbol demon isn't in encounter
                            if symbolFoe.ind not in formation.demons:
                                valid = False
                                #Is there a demon in encounter that has no replacement defined that can be replaced
                                for d in formation.demons:
                                    if d > 0 and any(r[0] == d for r in replacements) and 'Mitama' not in comp[d].name:
                                        valid = True
                                        d = symbolFoe.ind
                                #Is there a demon more than once in encounter battle that can be replaced
                                if not valid:
                                    counter = []
                                    for j, d in enumerate(formation.demons):
                                        if any(r[0] == d for r in counter):
                                            next(r for x, r in enumerate(counter) if r[0] == d)[1] += 1
                                        else:
                                            if d > 0 and 'Mitama' not in comp[d].name:
                                                counter.append([d, 1])
                                    if any(c[1] > 1 for c in counter):
                                        cID = counter.index(next(c for x, c in enumerate(counter) if c[1] > 1))
                                        valid = True
                                        formation.demons[cID] = symbolFoe.ind
                                #Replace symbolFoe with one of the demons in encounter
                                if not valid:
                                    symbolFoe = getFoeWithID(formation.demons[0], foes)
                        else:
                            #encounter has not been updated yet
                            #for each demon in encounter battle
                            for count, d in enumerate(formation.demons):
                                #dont replace empty slots or mitamas
                                if d > 0 and 'Mitama' not in comp[d].name:
                                    #insert replacement if defined, random demon else
                                    if any(r[0] == d for r in replacements):
                                        formation.demons[count] = next(r for x, r in enumerate(replacements) if r[0] == d)[1]
                                    # else:
                                    #     demonR = random.choice(possibilities)
                                    #     formation.demons[count] = demonR.ind
                        formation.updated = True
            replaceEnc.symbol.ind = symbolFoe.ind
            replaceEnc.symbol.translation = symbolFoe.name

            newSymbolArr.append(replaceEnc)

        
        replacementDict = {}
        for pair in replacements:
            replacementDict[pair[0]] = pair[1]

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
                spoilerLog.write(self.enemyNames[replaced] + " replaced by " + self.enemyNames[replacement] + "\n")
                  
        self.encounterReplacements = replacementDict


        self.adjustBasicEnemyStats(replacementDict, enemyArr)
        
        self.missionArr = self.adjustMissionsRequiringNormalDemons(replacementDict,enemyArr, self.missionArr)

        #Currently does not work yet
        #scriptLogic.replaceTutorialPixieModel(replacementDict[59])
        #scriptLogic.replaceTutorialPixieModel(75)
        
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
            for filteredEncounters in encounterPools:
                shuffledEncounters = sorted(filteredEncounters, key=lambda x: random.random()) #First filter the encounters and shuffle the ones to randomize
                shuffledEncounters = [copy.deepcopy(x) for x in shuffledEncounters] 
                for index, encounter in enumerate(filteredEncounters): #Write to spoiler log
                    spoilerLog.write(str(encounter.ind) + " (" + str(encounter.isEvent) +  ") " + self.enemyNames[encounter.demons[0]] + " replaced by " + str(shuffledEncounters[index].ind) + " (" + str(shuffledEncounters[index].isEvent)+ ") " + self.enemyNames[shuffledEncounters[index].demons[0]] + "\n")
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
                    
                    bossLogic.balanceBossEncounter(encounter.demons, shuffledEncounters[index].demons, self.staticBossArr, self.bossArr, encounter.ind, shuffledEncounters[index].ind, self.configSettings.scaleBossPressTurnsToCheck, self.configSettings.scaleBossInstakillRates)
                    #print("Old hp " + str(self.staticBossArr[encounter.demons[0]].stats.HP) + " of " + self.enemyNames[encounter.demons[0]] + " now is "  +
                    #      self.enemyNames[shuffledEncounters[index].demons[0]] + " with " + str(self.bossArr[shuffledEncounters[index].demons[0]].stats.HP) + " HP")
                    self.updateShuffledEncounterInformation(encounter, shuffledEncounters[index])
                    if encounter.isEvent:
                        self.eventEncountArr[encounter.ind] = encounter.eventEncounter
                    else:
                        self.encountArr[encounter.ind] = encounter.normalEncounter
                        self.updatedNormalEncounters.append(encounter.ind)

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
                    pair[0].conditions[0].amount = 1
            if staticArr[index].symbol.value == artemisQuestQuetz: #Artemis quest has Quetz as the second mission condition, not the first
                artemisQuest.conditions[1].ind = symbol.symbol.value
            if staticArr[index].symbol.value in fourHolyBeastDemons:
                hBIndex = fourHolyBeastDemons.index(staticArr[index].symbol.value)
                fourHolyBeastMission.conditions[hBIndex].ind = symbol.symbol.value
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
    Adds the data containing the positions of demon slots in normal encounters to the respective Event_Encounter.
    Also adjusts the size so that every encounter can have the same amount of additional demons.
    Parameters:
        data (Table): binary table containing the positions of demon slots in normal encounters.
        encountArr (List(Event_Encounter)): list of normal encounters to add positions to
        uassetBuffer (Table): binary table of the uasset needed to adjust the total size of file
    Returns: the list of encounters with positions
    '''
    def addPositionsToNormalEncountArr(self, data, encountArr, uassetBuffer):
        start = 0xCE
        size = 0x18F
        totalSize1 = uassetBuffer.readWord(0xA9)
        totalSize2 = uassetBuffer.readWord(len(uassetBuffer.buffer) - 0x60)
        for index, element in enumerate(encountArr):
            if index >= 3000: #there is one less entry than there are normal encounters
                continue
            offset = start + size * index
            locations = {
                'demon1': offset,
                'addDemon1': offset + 0xB6
            }
            for i in range(8):
                element.positions.demons.append(Position(data.readFloat(locations['demon1'] + 0xC * i),data.readFloat(locations['demon1'] + 4 + 0xC * i)))
            addDemonLength = data.readByte(offset + 0x70)
            addDemonAmount = data.readByte(offset + 0x81)
            addDemonLength2 = data.readByte(offset + 0x95)
            #make sure each encounter can have up to 4 additional demon positions
            while addDemonAmount < 4:
                for i in range(12):
                    data.buffer.insert(locations['addDemon1'],0)

                addDemonAmount += 1
                addDemonLength += 12
                addDemonLength2 += 12
                data.writeByte(addDemonLength,offset + 0x70)
                data.writeByte(addDemonAmount,offset + 0x81)
                data.writeByte(addDemonLength2,offset + 0x95)
                totalSize1 += 12
                totalSize2 += 12

            for i in range(4):
                element.positions.addDemons.append(Position(data.readFloat(locations['addDemon1'] + 0xC * i),data.readFloat(locations['addDemon1'] + 4 + 0xC * i)))
            element.positions.offsetNumber = locations
        uassetBuffer.writeWord(totalSize1,0xA9)
        uassetBuffer.writeWord(totalSize2,len(uassetBuffer.buffer) - 0x60)
        return encountArr

    '''
    Randomizes chest rewards including items, essences, and macca.
        Parameters:
            scaling (Boolean): Whether the rewards scale to the map the chest is in.
    '''
    def randomizeChests(self, scaling):
        validItems = []
        validEssences = []
        if scaling: #Valid Rewards are dependent on map
            validItems = {}
            validEssences = {}
            for key, value in numbers.CONSUMABLE_MAP_SCALING.items(): #Go through maps and valid items per map
                validItems[key] = value #Copy valid items per map 
                validEssences[key] = []
                #Gather all essences of dmeons in the level range for the map
                currentDemonNames = [demon.name + "'s Essence" for demon in self.compendiumArr if demon.level.value >= numbers.ESSENCE_MAP_SCALING[key][0] and demon.level.value <= numbers.ESSENCE_MAP_SCALING[key][1]]
                for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                    if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences[key] and itemName in currentDemonNames:
                        validEssences[key].append(itemID)
        else:
            for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences:
                    validEssences.append(itemID)
                elif itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                    validItems.append(itemID)
                
        for chest in self.chestArr:
            if (chest.item.value == 0 and chest.macca == 0) or chest.item.value >= numbers.KEY_ITEM_CUTOFF: #Skip unused chests and key item 'chests'
                continue
            if random.random() < numbers.CHEST_MACCA_ODDS: #Chest will contain macca
                if scaling: #Scaling makes macca range dependent on map
                    macca = random.randint(numbers.CHEST_AREA_MACCA_RANGES[chest.map][0] // 100, numbers.CHEST_AREA_MACCA_RANGES[chest.map][1] // 100) * 100 
                else:
                    macca = random.randint(numbers.CHEST_MACCA_MIN // 100, numbers.CHEST_MACCA_MAX // 100) * 100 #Completely random macca amount in increments of 100
                chest.item = Translated_Value(0, self.itemNames[0])
                chest.amount = 0
                chest.macca = macca
            else: #Chest will contain an item or essence
                if random.random() < numbers.CHEST_ESSENCE_ODDS:
                    if scaling and len(validEssences[chest.map]) > 1 : #Scaling chooses essence dependent on map
                        itemID = random.choice(validEssences[chest.map])
                        if itemID in validEssences[chest.map]:
                            #remove essence as valid choice for this map (not other maps to make sure Chiyoda/Shinjuku have enough Essences available)
                            validEssences[chest.map].remove(itemID)
                    elif scaling: #if no essence are available
                        emergencyEssences = []
                        currentDemonNames = [demon.name + "'s Essence" for demon in self.compendiumArr if demon.level.value >= numbers.ESSENCE_MAP_SCALING[chest.map][0] and demon.level.value <= numbers.ESSENCE_MAP_SCALING[chest.map][1]]
                        for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                            if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in emergencyEssences and itemName in currentDemonNames:
                                emergencyEssences.append(itemID)
                        itemID = random.choice(emergencyEssences)
                    else:  
                        itemID = random.choice(validEssences)
                        validEssences.remove(itemID) #Limit 1 chest per essence for diversity
                    amount = 1            
                else:
                    if scaling:#Scaling makes item dependent on map
                        itemID = random.choice(validItems[chest.map])
                    else:
                        itemID = random.choice(validItems)
                    amount = random.choices(list(numbers.CHEST_QUANTITY_WEIGHTS.keys()), list(numbers.CHEST_QUANTITY_WEIGHTS.values()))[0]
                item = Translated_Value(itemID, self.itemNames[itemID])
                if item.value in numbers.ITEM_QUANTITY_LIMITS.keys():
                    amount = min(amount, numbers.ITEM_QUANTITY_LIMITS[item.value])
                chest.item = item
                chest.amount = amount
                chest.macca = 0

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
    Randomizes the rewards for collecting Miman. Talismans are shuffled, and all else is replaced with a random number and amount of items.
        Parameters:
            scaling (Boolean): Whether the items are scaled per area
    '''
    def randomizeMimanRewards(self, scaling, keyItems):
        validItems = []
        validEssences = []

        if scaling: #scaling items per area
            validItems = {}
            validEssences = {}
            #copy valid items list
            validItems[60] = copy.deepcopy(numbers.CONSUMABLE_MAP_SCALING[60])
            validItems[61] = copy.deepcopy(numbers.CONSUMABLE_MAP_SCALING[61])
            validItems[62] = copy.deepcopy(numbers.CONSUMABLE_MAP_SCALING[62])
            validItems[63] = copy.deepcopy(numbers.CONSUMABLE_MAP_SCALING[63])

            for area in [60,61,62,63]: #for each of the 4 main areas, assemble essence list based on pre defined levels
                validEssences[area] = []
                currentDemonNames = [demon.name + "'s Essence" for demon in self.compendiumArr if demon.level.value >= numbers.ESSENCE_MAP_SCALING[area][0] and demon.level.value <= numbers.ESSENCE_MAP_SCALING[area][1]]
                for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                    if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences[area] and itemName in currentDemonNames:
                        validEssences[area].append(itemID)
        else:#no scaling items per area
            for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences:
                    validEssences.append(itemID)
                elif itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                    validItems.append(itemID)
        #Shuffle rewards to shuffle key item slots
        shuffledRewards = sorted(copy.deepcopy(self.mimanRewardsArr), key=lambda x: random.random())
        #
        for index,reward in enumerate(shuffledRewards):
            if scaling:
                areaChoices = [61,62,63,60] #Minato, Shinagawa, Chiyoda(same rewards list as Shinjuku), Taito
                rewardArea = areaChoices[index // 10] #10 miman rewards per area
            items = []
            if reward.items[0].ind >= numbers.KEY_ITEM_CUTOFF and len(keyItems) > 0: #originally key items (talismans)
                itemID = random.choice(keyItems)
                items.append(Reward_Item(itemID,1))
                keyItems.remove(itemID)
                #items.append(reward.items[0])
            elif random.random() < numbers.MIMAN_ESSENCE_ODDS:
                if scaling: 
                    itemID = random.choice(validEssences[rewardArea])
                    for key in validEssences.keys():
                        if itemID in validEssences[key]: #Remove essence from all applicable pools
                            validEssences[key].remove(itemID)
                else:
                    itemID = random.choice(validEssences)
                    validEssences.remove(itemID) #Limit 1 chest per essence for diversity
                items.append(Reward_Item(itemID,1))
            else:
                #decide how many items
                itemNumber = random.choices(list(numbers.MIMAN_ITEM_NUMBER_WEIGHTS.keys()),list(numbers.MIMAN_ITEM_NUMBER_WEIGHTS.values()))[0]
                itemAmount = random.choices(list(numbers.MIMAN_ITEM_AMOUNT_WEIGHTS.keys()),list(numbers.MIMAN_ITEM_AMOUNT_WEIGHTS.values()))[0]
                for _ in range(itemNumber):
                    #decide amount per item
                    if scaling: #scaling depends on area item list
                        itemID = random.choice(validItems[rewardArea])
                    else:
                        itemID = random.choice(validItems)
                    if itemID in numbers.ITEM_QUANTITY_LIMITS.keys():
                        items.append(Reward_Item(itemID,amount = min(itemAmount, numbers.ITEM_QUANTITY_LIMITS[itemID])))
                    else:
                       items.append(Reward_Item(itemID,itemAmount)) 
            while len(items) < 16: #fill rest with empty rewards
                items.append(Reward_Item(0,0))
            reward.items = items
            reward.miman = 5 * (index+1)
            reward.offset = self.mimanRewardsArr[index].offset
        shuffledRewards.sort(key=lambda x: x.miman)
        return shuffledRewards

    '''
    Randomizes the rewards of all missions that usually have rewards. Reusable consumable items and key items are classified as unique rewards, and are shuffled around, while all other rewards are completely random.
    '''
    def randomizeMissionRewards(self, scaling, missionContainer):
        validItems = []
        validEssences = []
        
        if scaling: #Rewards scale with map
            validItems = {}
            validEssences = {}
            for key, value in numbers.CONSUMABLE_MAP_SCALING.items():
                validItems[key] = value #Item list is defined per area

            rewardAreaMissions = copy.deepcopy(numbers.REWARD_AREA_MISSIONS)
            for key, value in scriptLogic.EXTRA_MISSION_REWARD_AREAS.items():
                #Add items from script rewards to dictionary
                rewardAreaMissions[key] = rewardAreaMissions[key] + value
            
            missionRewardAreas = {} #Dictionary to know which area should be used to scale the a missions reward
            for key, value in rewardAreaMissions.items():
                for id in value:
                    missionRewardAreas[id] = key #Turn this into MissionID -> MapID, for easier use
                validEssences[key] = []
                #Grab all essences in the predefined level range for the area
                currentDemonNames = [demon.name + "'s Essence" for demon in self.compendiumArr if demon.level.value >= numbers.ESSENCE_MAP_SCALING[key][0] and demon.level.value <= numbers.ESSENCE_MAP_SCALING[key][1]]
                for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                    if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences[key] and itemName in currentDemonNames:
                        validEssences[key].append(itemID)


        else: #Rewards do not scale with map
            for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences:
                    validEssences.append(itemID)
                elif itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                    validItems.append(itemID)

        
        rewardingMissions = missionContainer.rewardingMissions
        uniqueRewards = missionContainer.uniqueRewards
        creationRewards = missionContainer.creationRewards
        vengeanceRewards = missionContainer.vengeanceRewards

        
        validCreationMissions = list(filter(lambda mission: mission.ind in numbers.CREATION_EXLUSIVE_MISSIONS and mission.ind not in numbers.REPEAT_MISSIONS and mission.ind not in numbers.MUTUALLY_EXCLUSIVE_MISSIONS ,rewardingMissions))
        creationRewardMissions = random.sample(validCreationMissions, len(creationRewards))
        for index, mission in enumerate(creationRewardMissions):
            rewardingMissions.remove(mission)
            mission.macca = 0
            mission.reward = creationRewards[index]
        validVengeanceMissions = list(filter(lambda mission: mission.ind in numbers.VENGEANCE_EXLUSIVE_MISSIONS and mission.ind not in numbers.REPEAT_MISSIONS and mission.ind not in numbers.MUTUALLY_EXCLUSIVE_MISSIONS ,rewardingMissions))
        vengeanceRewardMissions = random.sample(validVengeanceMissions, len(vengeanceRewards))
        for index, mission in enumerate(vengeanceRewardMissions):
            rewardingMissions.remove(mission)
            mission.macca = 0
            mission.reward = vengeanceRewards[index]

        validUniqueMissions = list(filter(lambda mission: mission.ind not in numbers.REPEAT_MISSIONS and mission.ind not in numbers.MUTUALLY_EXCLUSIVE_MISSIONS,rewardingMissions)) #repeat missions shouldn't not reward unique rewards
        uniqueRewardMissions = random.sample(validUniqueMissions, len(uniqueRewards)) #randomly select missions to reward unique rewards
        for index, mission in enumerate(uniqueRewardMissions):
            #remove mission from general mission pool and set unique reward
            rewardingMissions.remove(mission)
            mission.macca = 0
            mission.reward = uniqueRewards[index]
        for mission in rewardingMissions:
            if scaling: #Set area if reward should scale
                rewardArea = missionRewardAreas[mission.ind]
            if random.random() < numbers.MISSION_MACCA_ODDS and mission.ind not in numbers.REPEAT_MISSIONS and mission.ind >= 0 and mission.ind not in numbers.MACCALESS_MISSIONS: #repeat missions should not have macca
                if scaling: #Scaled macca ranges depend on area
                    macca = random.randint(numbers.MISSION_REWARD_AREA_MACCA_RANGES[rewardArea][0] // 100, numbers.MISSION_REWARD_AREA_MACCA_RANGES[rewardArea][1] // 100) *100
                else:
                    macca = random.randint(numbers.MISSION_MACCA_MIN // 100, numbers.MISSION_MACCA_MAX // 100) *100#Completely random macca amount in increments of 100
                mission.reward.ind = 0
                mission.reward.amount = 0
                mission.macca = macca
            elif random.random() < numbers.MISSION_ESSENCE_ODDS:
                if scaling: #scaled essences depend on area
                    itemID = random.choice(validEssences[rewardArea])
                    for value in validEssences.values():
                        if itemID in value: #remove essence from all applicable areas
                            value.remove(itemID)
                else:  
                    itemID = random.choice(validEssences)
                    validEssences.remove(itemID) #Limit 1 chest per essence for diversity
                amount = 1
                mission.reward.ind = itemID
                mission.reward.amount = amount
                mission.macca =0
            else: #no essence and no macca means consumable item
                if scaling: #scaled items depend on area
                    itemID = random.choice(validItems[rewardArea])
                else:
                    itemID = random.choice(validItems)
                amount = random.choices(list(numbers.MISSION_QUANTITY_WEIGHTS.keys()), list(numbers.MISSION_QUANTITY_WEIGHTS.values()))[0]
                if itemID in numbers.ITEM_QUANTITY_LIMITS.keys(): #apply inventory limit to item amount
                    amount = min(amount, numbers.ITEM_QUANTITY_LIMITS[itemID])
                mission.reward.ind = itemID
                mission.reward.amount = amount
                mission.macca = 0
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
                    self.missionArr[correctDuplicateInd].reward.ind = self.missionArr[correctMissionInd].reward.ind
                    self.missionArr[correctDuplicateInd].reward.amount = self.missionArr[correctMissionInd].reward.amount
                    self.missionArr[correctDuplicateInd].macca = self.missionArr[correctMissionInd].macca
                else:
                    self.missionArr[duplicateID].reward.ind = self.missionArr[missionID].reward.ind
                    self.missionArr[duplicateID].reward.amount = self.missionArr[missionID].reward.amount
                    self.missionArr[duplicateID].macca = self.missionArr[missionID].macca
    
    '''
    Intializes mission pools for missions that have rewards, unique item rewards and rewards unique to a specific route.
    '''
    def initializeMissionPools(self):
        
        rewardingMissions = []
        uniqueRewards = []
        creationRewards = []
        vengeanceRewards = []
        for mission in self.missionArr:
            if (mission.macca > 0 or mission.reward.ind > 0) and not any(mission.ind in duplicates for duplicates in numbers.MISSION_DUPLICATES.values()) and mission.ind not in numbers.BANNED_MISSIONS:
                rewardingMissions.append(mission) #find missions with rewards that are not banned or a duplicate
                if mission.reward.ind > numbers.KEY_ITEM_CUTOFF or mission.reward.ind in numbers.BANNED_ITEMS:
                    if mission.ind not in numbers.CREATION_EXCLUSIVE_KEY_REWARDS and mission.ind not in numbers.VENGEANCE_EXCLUSIVE_KEY_REWARDS:
                        uniqueRewards.append(copy.deepcopy(mission.reward)) #add key items or reusable consumables to unique rewards
                    elif mission.ind in numbers.CREATION_EXCLUSIVE_KEY_REWARDS:
                        creationRewards.append(copy.deepcopy(mission.reward))
                    else:
                        vengeanceRewards.append(copy.deepcopy(mission.reward))

        #Remove unwanted rewards
        for reward in uniqueRewards:
            if reward.ind in numbers.BANNED_KEY_REWARDS:
                uniqueRewards.remove(reward)
        
        missionContainer = Mission_Container()
        missionContainer.rewardingMissions = rewardingMissions
        missionContainer.uniqueRewards = uniqueRewards
        missionContainer.creationRewards = creationRewards
        missionContainer.vengeanceRewards = vengeanceRewards
        
        return missionContainer
    '''
    Randomizes gift items using the pool to assign key items.
        Parameters:
            pool(Gift_Pool): Contains the pools of all gifts and the unique rewards to assign randomly
    '''
    def randomizeGiftItems(self, pool):
        randomizedGifts = []
        if not self.configSettings.combineKeyItemPools:#No combined pools means that exclusive items stay normal due to otherwise having not enough gift slots
            unchangedGifts = list(filter(lambda gift: gift.script in scriptLogic.VENGEANCE_EXCLUSIVE_GIFTS or gift.script  in scriptLogic.NEWGAMEPLUS_GIFTS, pool.allGifts))
            for gift in unchangedGifts:
                pool.uniqueRewards.remove(gift.reward)
                randomizedGifts.append(gift)
        #Filter out exclusive gifts that should not contain a unique item
        possibleGifts = list(filter(lambda gift: gift.script not in scriptLogic.VENGEANCE_EXCLUSIVE_GIFTS and gift.script not in scriptLogic.NEWGAMEPLUS_GIFTS, pool.allGifts))
        uniqueGifts = random.sample(possibleGifts, len(pool.uniqueRewards))
        for gift in uniqueGifts:
            reward = random.choice(pool.uniqueRewards)
            gift.item = reward
            pool.uniqueRewards.remove(reward)
            randomizedGifts.append(gift)
        
        

        
        #Assemble possible rewards
        if self.configSettings.scaleItemsToArea: #Rewards scale with map
            validItems = {}
            validEssences = {}
            for key, value in numbers.CONSUMABLE_MAP_SCALING.items():
                validItems[key] = value #Item list is defined per area
            
            scriptToArea = scriptLogic.getGiftRewardAreas()
            for area in scriptLogic.GIFT_AREAS.keys():
                validEssences[area] = []
                #Grab all essences in the predefined level range for the area
                currentDemonNames = [demon.name + "'s Essence" for demon in self.compendiumArr if demon.level.value >= numbers.ESSENCE_MAP_SCALING[area][0] and demon.level.value <= numbers.ESSENCE_MAP_SCALING[area][1]]
                for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                    if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences[area] and itemName in currentDemonNames:
                        validEssences[area].append(itemID)
        else: #Rewards do not scale with map
            validItems = []
            validEssences = []
            for itemID, itemName in enumerate(self.itemNames): #Include all essences in the pool except Aogami/Tsukuyomi essences and demi-fiend essence
                if 'Essence' in itemName and itemID not in numbers.BANNED_ESSENCES and itemID not in validEssences:
                    validEssences.append(itemID)
                elif itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                    validItems.append(itemID)
        
        #get Gifts that did not receive a unique item
        nonUniqueGifts = list(filter(lambda gift: gift not in randomizedGifts, pool.allGifts))
        for gift in nonUniqueGifts:
            if self.configSettings.scaleItemsToArea:#Set area to scale items after when necessary
                rewardArea = scriptToArea[gift.script]
            if random.random() < scriptLogic.GIFT_ESSENCE_ODDS:
                if self.configSettings.scaleItemsToArea: #scaled essences depend on area
                    itemID = random.choice(validEssences[rewardArea])
                    for value in validEssences.values():
                        if itemID in value: #remove essence from all applicable areas
                            value.remove(itemID)
                else:  
                    itemID = random.choice(validEssences)
                    validEssences.remove(itemID) #Limit 1 gift per essence for diversity
                gift.item.ind = itemID
            else:
                if self.configSettings.scaleItemsToArea: #scaled items depend on area
                    itemID = random.choice(validItems[rewardArea])
                else:
                    itemID = random.choice(validItems)
                gift.item.ind = itemID
            #print(gift.script + str(gift.item.ind))
        scriptLogic.updateGiftScripts(pool.allGifts,self.scriptFiles)

    '''
    Initializes the pools of all gifts and unique rewards from gifts.
    '''
    def initializeGiftPools(self):
        giftPool = Gift_Pool()
        for script,item in scriptLogic.BASE_GIFT_ITEMS.items():
            if not self.configSettings.includeTsukuyomiTalisman and script == scriptLogic.TSUKUYOMI_TALISMAN_SCRIPT:
                #Do not include Tsukuyomi Talisman or it's check in pool if setting isn't set
                continue
            gift = Gift_Item()
            gift.script = script
            reward = Reward_Item(item, 1)
            gift.item = reward
            giftPool.allGifts.append(gift)
            if reward.ind >= numbers.KEY_ITEM_CUTOFF:
                giftPool.uniqueRewards.append(reward)

        giftPool.uniqueRewardRatio = len(giftPool.uniqueRewards) / len(giftPool.allGifts)
        return giftPool
            
    '''
    Randomizes the miman and mission rewards, with a combined pool depending on the settings.
    '''
    def randomizeItemRewards(self):
        self.missionArr = self.missionArr + scriptLogic.createFakeMissionsForEventRewards(self.scriptFiles)
        missionPool = self.initializeMissionPools()
        giftPool = self.initializeGiftPools()
        if not self.configSettings.combineKeyItemPools:
            #Mission Pool get initialized regardless so just stays the same
            mimanPool = copy.deepcopy(numbers.MIMAN_BASE_KEY_ITEMS) #Use base pool
        else:
            combinedItemPool = []
            if self.configSettings.randomizeMissionRewards: #Add mission key item rewards to the combined pool
                missionKeyItemIDs = []
                for reward in missionPool.uniqueRewards:
                    missionKeyItemIDs.append(reward.ind)
                combinedItemPool = combinedItemPool + missionKeyItemIDs
            if self.configSettings.randomizeMimanRewards: #Add miman rewards to the combined pool
                combinedItemPool = numbers.MIMAN_BASE_KEY_ITEMS + combinedItemPool
            if self.configSettings.randomizeGiftItems: #Add unique gift rewards to the combined pool
                giftItemIDs = []
                for reward in giftPool.uniqueRewards:
                    giftItemIDs.append(reward.ind)
                combinedItemPool = giftItemIDs + combinedItemPool

            #Distribute combined pool, starting with sub pools of fixed or lower size
            if self.configSettings.randomizeMimanRewards:#Miman pool has fixed size
                mimanPool = random.sample(combinedItemPool, len(numbers.MIMAN_BASE_KEY_ITEMS))
                for itemID in mimanPool:
                    combinedItemPool.remove(itemID)
            
            if self.configSettings.randomizeGiftItems: #Gift pool has fixed size#TODO:Vary Size?
                tsukuyomiCorrection = 0 
                if not self.configSettings.includeTsukuyomiTalisman:
                    tsukuyomiCorrection = 1 #Increase unique item count by 1 to account for tsukuyomi talisman not being in pool
                itemIDs = random.sample(combinedItemPool, tsukuyomiCorrection + len(giftPool.uniqueRewards) - len(scriptLogic.VENGEANCE_EXCLUSIVE_GIFTS) - len(scriptLogic.NEWGAMEPLUS_GIFTS))
                giftPool.uniqueRewards = []
                for itemID in itemIDs:
                    giftPool.uniqueRewards.append(Reward_Item(itemID, 1))
                    combinedItemPool.remove(itemID)
            
            if self.configSettings.randomizeMissionRewards:#Largest pool and therefore last
                missionPool.uniqueRewards = []
                for itemID in combinedItemPool:
                    missionPool.uniqueRewards.append(Mission_Reward(itemID,1))

        if(self.configSettings.randomizeMimanRewards):
            self.mimanRewardsArr = self.randomizeMimanRewards(self.configSettings.scaleItemsToArea, mimanPool)
        
        scriptLogic.adjustFirstMimanEventReward(self.configSettings, self.compendiumArr, self.itemNames, self.encounterReplacements, self.essenceArr, self.scriptFiles)   

        if self.configSettings.randomizeGiftItems:
            self.randomizeGiftItems(giftPool)

        if self.configSettings.randomizeMissionRewards:
            self.randomizeMissionRewards(self.configSettings.scaleItemsToArea, missionPool)
        return scriptLogic.updateAndRemoveFakeMissions(self.missionArr, self.scriptFiles)
    
    '''
    Randomizes the drops of basic enemies, excluding key items and essences.
        Parameters:
            scaling (Boolean): whether the items are scaled to the level of the encounter
    '''
    def randomizeBasicEnemyDrops(self, scaling):
        validItems = []
        if scaling: #Rewards should scale on area
            validItems = {}
            for key, values in numbers.CONSUMABLE_MAP_SCALING.items():
                validItems[key] = values
        else: #Rewards are truly random
            for itemID, itemName in enumerate(self.itemNames): 
                if itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                    validItems.append(itemID)

        #Gather all non mitama basic enemies with drops
        dropEnemies = list(filter(lambda e: 'Mitama' not in e.name and e.drops.item1.value > 0, self.enemyArr))

        for enemy in dropEnemies: #For all enemies
            drop = enemy.drops
            if scaling: #Drops should scale based on area
                rewardArea = numbers.ENCOUNTER_LEVEL_AREAS[enemy.level] #Area to scale rewards with
                if drop.item1.value < numbers.CONSUMABLE_ITEM_COUNT: 
                    if random.random() < numbers.DROP1_LIFESTONE_ODDS: #First Drop has a chance to be forced life stone as per original game
                        drop.item1.value = 1
                    else:
                        drop.item1.value = random.choice(validItems[rewardArea])
                    drop.item1.chance = random.randrange(3,12)
                if drop.item2.value < numbers.CONSUMABLE_ITEM_COUNT:
                    drop.item1.value = random.choice(validItems[rewardArea])
                    drop.item2.chance = random.randrange(3,12)
                if drop.item3.value < numbers.CONSUMABLE_ITEM_COUNT:
                    drop.item1.value = random.choice(validItems[rewardArea])
                    drop.item3.chance = random.randrange(3,12)
            else: #non scaling random drops
                #Edit all drops that are not key items or essences
                if drop.item1.value < numbers.CONSUMABLE_ITEM_COUNT:
                    drop.item1.value = random.choice(validItems)
                    drop.item1.chance = random.randrange(3,12)
                if drop.item2.value < numbers.CONSUMABLE_ITEM_COUNT:
                    drop.item2.value = random.choice(validItems)
                    drop.item2.chance = random.randrange(3,12)
                if drop.item3.value < numbers.CONSUMABLE_ITEM_COUNT:
                    drop.item3.value = random.choice(validItems)
                    drop.item3.chance = random.randrange(3,12) 
                    
    '''
    Randomizes the drops of bosses, excluding key items.
        Parameters:
            scaling (Boolean): whether the items are scaled to the level of the encounter
    '''
    def randomizeBossDrops(self, scaling):
        validItems = []
        if scaling: #Rewards should scale on area
            validItems = {}
            for key, values in numbers.CONSUMABLE_MAP_SCALING.items():
                validItems[key] = values
        else: #Rewards are truly random
            for itemID, itemName in enumerate(self.itemNames): 
                if itemID < numbers.CONSUMABLE_ITEM_COUNT and itemID not in numbers.BANNED_ITEMS and 'NOT USED' not in itemName: #Include all consumable items
                    validItems.append(itemID)

        for demonID in self.validBossDemons: #For all bosses
            enemy = self.bossArr[demonID]
            drop = enemy.drops
            if drop.item1.value >= numbers.KEY_ITEM_CUTOFF or drop.item2.value >= numbers.KEY_ITEM_CUTOFF or drop.item3.value >= numbers.KEY_ITEM_CUTOFF:
                continue #Don't mess with key items
            if drop.item1.chance <= 0 and drop.item2.chance <= 0 and drop.item3.chance <= 0:
                continue #Bosses that drop nothing will continue to drop nothing (mostly minions and summons)
            if scaling: #Drops should scale based on area
                rewardArea = numbers.ENCOUNTER_LEVEL_AREAS[enemy.level] #Area to scale rewards with
                numDrops = random.choices(list(numbers.BOSS_DROP_QUANTITY_WEIGHTS.keys()), list(numbers.BOSS_DROP_QUANTITY_WEIGHTS.values()))[0]
                if demonID not in self.essenceBannedBosses and random.random() < numbers.BOSS_ESSENCE_ODDS: #Boss will drop its own essence
                    try:
                        essence = next(e for e in self.essenceArr if self.enemyNames[demonID] == e.demon.translation)
                        drop.item1 = Item_Drop(essence.ind, essence.name, 100, 0)
                    except StopIteration:
                        item = random.choice(validItems[rewardArea])
                        drop.item1 = Item_Drop(item, self.itemNames[item], 100, 0)
                else:
                    item = random.choice(validItems[rewardArea])
                    drop.item1 = Item_Drop(item, self.itemNames[item], 100, 0)
                if numDrops > 1:
                    item = random.choice(validItems[rewardArea])
                    drop.item2 = Item_Drop(item, self.itemNames[item], 100, 0)
                else:
                    drop.item2 = Item_Drop(0, self.itemNames[0], 0, 0)
                if numDrops > 2:
                    item = random.choice(validItems[rewardArea])
                    drop.item3 = Item_Drop(item, self.itemNames[item], 100, 0)
                else:
                    drop.item3 = Item_Drop(0, self.itemNames[0], 0, 0)
            else: #non scaling random drops
                numDrops = random.choices(list(numbers.BOSS_DROP_QUANTITY_WEIGHTS.keys()), list(numbers.BOSS_DROP_QUANTITY_WEIGHTS.values()))[0]
                if demonID not in self.essenceBannedBosses and random.random() < numbers.BOSS_ESSENCE_ODDS: #Boss will drop its own essence
                    try:
                        essence = next(e for e in self.essenceArr if self.enemyNames[demonID] == e.demon.translation)
                        drop.item1 = Item_Drop(essence.ind, essence.name, 100, 0)
                    except StopIteration:
                        item = random.choice(validItems)
                        drop.item1 = Item_Drop(item, self.itemNames[item], 100, 0)
                else:
                    item = random.choice(validItems)
                    drop.item1 = Item_Drop(item, self.itemNames[item], 100, 0)
                if numDrops > 1:
                    item = random.choice(validItems)
                    drop.item2 = Item_Drop(item, self.itemNames[item], 100, 0)
                else:
                    drop.item2 = Item_Drop(0, self.itemNames[0], 0, 0)
                if numDrops > 2:
                    item = random.choice(validItems)
                    drop.item3 = Item_Drop(item, self.itemNames[item], 100, 0)
                else:
                    drop.item3 = Item_Drop(0, self.itemNames[0], 0, 0)
                    
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


        for fc in fusionCombo:
            if(fc not in self.fusionChartArr):
                self.fusionChartArr.append(Fusion_Chart_Node(None,Translated_Value(getInd(fc[0]),fc[0]),Translated_Value(getInd(fc[1]),fc[1]),Translated_Value(getInd(fc[2]),fc[2])))
                #self.fusionChartArr.append(Fusion_Chart_Node(None,Translated_Value(getInd(fc[1]),fc[1]),Translated_Value(getInd(fc[0]),fc[0]),Translated_Value(getInd(fc[2]),fc[2])))

    '''
    Shuffles the levels of all playable demons and does adjustments to data based on that shuffling.
    The shuffling process takes the fusions of demons into account by assembling the fusion tree from the bottom.
        Parameters:
            comp (Array(Compendium_Demon)): The array of playable demons
        Returns:
            The array of playable demons with shuffled levels
    '''
    def shuffleLevel(self, comp, config):
        

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
        elements = list(filter(lambda d: d.race.translation == 'Element', comp))
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
        
        #Check if demons in the base 10 can fuse into each other
        for b in base:
            possibleFusions = [f for f in fusions if f[2].race.translation == b.race.translation and f[2].ind == -1 and f[2].level.value <= b.level.value]
            for p in possibleFusions:
                p[2] = b

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
                validDemons.pop(validDemons.index(demon))

        #do not continue if attempts elapse 300
        if attempts >= 300:
            print("Could not assign all levels properly")
            return False
            

        # #For all flagged demons...
        # for e in flaggedDemons:
        #     validLevel = False
        #     somethingWrong = False 
        #     attempts = 100 #Band-aid fix to stop infinite loop
        #     #assign new level based on highest free level as max and the minimum level unlock level based on flag
        #     while not validLevel:
        #         if getHighestFreeLevel() < e.minUnlock or somethingWrong:
        #             newLevel = self.getRandomLevel(slots, getHighestFreeLevel(), getLowestFreeLevel()) #Something went wrong, no levels are free above minUnlock
        #         else:
        #             newLevel = self.getRandomLevel(slots, getHighestFreeLevel(), e.minUnlock)
        #         if slots[newLevel] > 0 and newLevel not in raceLevels[RACE_ARRAY.index(e.race.translation)]:
        #             #make sure slot is available and no demon of the same race has the same level
        #             validLevel = True
        #         attempts -= 1
        #         if attempts < 0:
        #             somethingWrong = True
        #     slots[newLevel] = slots[newLevel] - 1
        #     comp[e.ind].level.value = newLevel
        #     raceLevels[RACE_ARRAY.index(e.race.translation)].append(newLevel)

        # for index, e in enumerate(validDemons):
        #     validLevel = False
        #     attempts = 100 #Band-aid fix to stop infinite loop
        #     while not validLevel:
        #         newLevel = self.getRandomLevel(slots, getHighestFreeLevel(), getLowestFreeLevel())
        #         if slots[newLevel] > 0 and newLevel not in raceLevels[RACE_ARRAY.index(e.race.translation)]:
        #             #make sure slot is available and no demon of the same race has the same level
        #             validLevel = True
        #         else:
        #             attempts -= 1
        #             if attempts <= 0:
        #                 validLevel = True
        #     slots[newLevel] = slots[newLevel] - 1
        #     comp[e.ind].level.value = newLevel
        #     raceLevels[RACE_ARRAY.index(e.race.translation)].append(newLevel)


        #slots = self.defineLevelSlots(comp)
        #print(slots)
        self.adjustLearnedSkillLevels(comp)
        comp = self.adjustStatsToLevel(comp)
        self.adjustFusionFlagsToLevel(comp)
        self.adjustSpecialFusionTable(specialFusions,comp)
        
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

        ingNumber = random.randint(2,4)
        ingredients = []

        fusion = Special_Fusion()
        fusion.resultLevel = demon.level.value
        fusion.result = Translated_Value(demon.ind, demon.name)

        for index in range(ingNumber):
            ing = random.choice(base)
            ingredients.append(Translated_Value(ing.ind, ing.name))
        
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
            nahoOGLevel = self.nahobino.stats[demon.level.original]
            nahoNewLevel = self.nahobino.stats[demon.level.value]

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
        return comp

        
    
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
            questBossEncounters.pop(index)
            index = replacementDemonIDs.index(occ)
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
    Changes the scaling of normal demon symbols with overly large scaling factors to the normal 1.2 factor.
    Parameters:
        buffer (Table): contains the bytearray of the MapSymbolParamTable
    Returns the changed buffer
    '''
    def scaleLargeSymbolDemonsDown(self, buffer):
        last = 0
        startingBytes = bytearray(bytes.fromhex('17000000000000003100000000000000'))
        while buffer.buffer.find(startingBytes,last) != -1:
            offset = buffer.buffer.find(startingBytes,last) +25
            last = buffer.buffer.find(startingBytes,last) +100

            demonID = buffer.readWord(offset)
            if demonID in numbers.LARGE_SYMBOL_DEMONS:
                buffer.writeFloat(1.2,offset + 116)
        return buffer
    
    '''
    Speeds up demons on the overworld that replace punishing foe birds with large movement cycles
    Parameters:
        buffer (Table): contains the bytearray of the MapSymbolParamTable
    Returns the changed buffer
    '''
    def adjustPunishingFoeSpeeds(self, buffer):
        
        for birdID, walkSpeed in numbers.PUNISHING_FOE_BIRD_SPEEDS.items():
            replacementID = self.bossSymbolReplacementMap[birdID]
            try:
                replacementSymbol = next(d for x, d in enumerate(self.mapSymbolArr) if d.demonID == replacementID)
                buffer.writeFloat(walkSpeed,replacementSymbol.offsetNumbers['walkSpeed'])
                    
            except StopIteration:
                birdSymbol = next(d for x, d in enumerate(self.mapSymbolArr) if d.demonID == birdID)
                buffer.writeWord(replacementID, birdSymbol.offsetNumbers['demonID'])

        return buffer

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

    def addEventEncounter(self):
        newEvEnc = copy.deepcopy(self.eventEncountArr[0])
        newEvEnc.ind = self.eventEncountArr[-1].ind +1
        offset = 0x45 + 0x60 * newEvEnc.ind
        newEvEnc.offsets = {
                'demons': offset + 0x48,
                'track': offset + 0x2E,
                'levelpath': offset,
                'unknownDemon': offset + 0x38,
                '23Flag': offset + 0x23,
                'battlefield': offset + 0x24
            }
        self.eventEncountArr.append(newEvEnc)

    '''
    Generates a random seed if none was provided by the user and sets the random seed
    '''
    def createSeed(self):
         if self.textSeed == "":
             self.textSeed = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
             print('Your generated seed is: {}\n'.format(self.textSeed))
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
        TODO: Determine if this works for non-windows systems
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
    def fullRando(self, config):

        

        self.writeFolder(paths.DEBUG_FOLDER)
        with open(paths.SEED_FILE, 'w', encoding="utf-8") as file:
                file.write(self.textSeed)

        compendiumBuffer = self.readBinaryTable(paths.NKM_BASE_TABLE_IN)
        skillBuffer = self.readBinaryTable(paths.SKILL_DATA_IN)
        normalFusionBuffer = self.readBinaryTable(paths.UNITE_COMBINE_TABLE_IN)
        otherFusionBuffer = self.readBinaryTable(paths.UNITE_TABLE_IN)
        encountBuffer = self.readBinaryTable(paths.ENCOUNT_DATA_IN)
        playGrowBuffer = self.readBinaryTable(paths.MAIN_CHAR_DATA_IN)
        itemBuffer = self.readBinaryTable(paths.ITEM_DATA_IN)
        shopBuffer = self.readBinaryTable(paths.SHOP_DATA_IN)
        eventEncountBuffer = self.readBinaryTable(paths.EVENT_ENCOUNT_IN)
        missionBuffer = self.readBinaryTable(paths.MISSION_DATA_IN)
        bossFlagBuffer = self.readBinaryTable(paths.BOSS_FLAG_DATA_IN)
        battleEventsBuffer = self.readBinaryTable(paths.BATTLE_EVENTS_IN)
        battleEventUassetBuffer = self.readBinaryTable(paths.BATTLE_EVENT_UASSET_IN)
        devilAssetTableBuffer = self.readBinaryTable(paths.DEVIL_ASSET_TABLE_IN)
        abscessBuffer = self.readBinaryTable(paths.ABSCESS_TABLE_IN)
        devilUIBuffer = self.readBinaryTable(paths.DEVIL_UI_IN)
        talkCameraBuffer = self.readBinaryTable(paths.TALK_CAMERA_OFFSETS_IN)
        eventEncountPostBuffer = self.readBinaryTable(paths.EVENT_ENCOUNT_POST_DATA_TABLE_IN)
        miracleBuffer = self.readBinaryTable(paths.MIRACLE_TABLE_IN)
        eventEncountUassetBuffer = self.readBinaryTable(paths.EVENT_ENCOUNT_UASSET_IN)
        uniqueSymbolBuffer = self.readBinaryTable(paths.UNIQUE_SYMBOL_DATA_IN)
        encountPostBuffer = self.readBinaryTable(paths.ENCOUNT_POST_DATA_TABLE_IN)
        encountPostUassetBuffer = self.readBinaryTable(paths.ENCOUNT_POST_DATA_TABLE_UASSET_IN)
        chestBuffer = self.readBinaryTable(paths.CHEST_TABLE_IN)
        mapSymbolParamBuffer = self.readBinaryTable(paths.MAP_SYMBOL_PARAM_IN)
        eventEncountPostUassetBuffer = self.readBinaryTable(paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_IN)
        self.readDemonNames()
        self.readSkillNames()
        self.readItemNames()
        self.readDataminedEnemyNames()
        self.fillCompendiumArr(compendiumBuffer)
        self.fillSkillArrs(skillBuffer)
        self.fillNormalFusionArr(normalFusionBuffer)
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
        self.fillEssenceArr(itemBuffer)
        self.fillShopArr(shopBuffer)
        self.fillProtofiendArr(compendiumBuffer)
        self.fillMissionArr(missionBuffer)
        self.fillUniqueSymbolArr(uniqueSymbolBuffer)
        self.fillChestArr(chestBuffer)
        self.fillMimanRewardArr(shopBuffer)
        self.fillMapSymbolArr(mapSymbolParamBuffer)
        self.fillConsumableArr(itemBuffer)
        self.fillFusionSkillReqs(skillBuffer)
        
        #self.eventEncountArr = self.addPositionsToEventEncountArr(eventEncountPostBuffer, self.eventEncountArr)
        self.eventEncountArr = self.addPositionsToNormalEncountArr(eventEncountPostBuffer, self.eventEncountArr, eventEncountPostUassetBuffer)
        self.encountArr = self.addPositionsToNormalEncountArr(encountPostBuffer, self.encountArr, encountPostUassetBuffer)
        
        self.findValidBossDemons()
        self.removeBattleTutorials()
        
        if config.fixUniqueSkillAnimations:
            self.removeUniqueSkillAnimations()
        
        self.fusionSkillIDs = list(filter(lambda skill: 800 < skill and skill < 900,numbers.MAGATSUHI_SKILLS))
        magatsuhiSkillsRaces = [self.obtainSkillFromID(skill) for skill in filter(lambda skill: 800 > skill or skill > 900, numbers.MAGATSUHI_SKILLS)]
        if self.configSettings.randomizeMagatsuhiSkillReq:
            magatsuhiSkillsRaces = self.randomizeMagatsuhiSkillReqs()
            

        skillLevels = self.generateSkillLevelList()
        levelSkillList = self.generateLevelSkillList(skillLevels)
       
        if config.randomPotentials:
            self.randomizePotentials(self.compendiumArr)
            if config.fixUniqueSkillAnimations:
                self.randomizePotentials(self.playerBossArr, mask=numbers.GUEST_IDS_WORKING_ANIMS_ONLY)
            else:
                self.randomizePotentials(self.playerBossArr, mask=numbers.GUEST_IDS)
        
        if self.configSettings.randomDemonStats:
            self.randomizeDemonStats(self.compendiumArr, foes=self.enemyArr)
            self.randomizeDemonStats(self.playerBossArr, mask=numbers.GUEST_IDS)

        self.addAdditionalFusionsToFusionChart(config)

        if config.randomRaces and config.randomDemonLevels:
            self.elementals = self.randomizeRaces(self.compendiumArr)
        elif config.randomRaces:
            self.elementals = self.randomizeRacesFixedLevels(self.compendiumArr)

        if config.randomDemonLevels:
            newComp = False
            attempts = 0
            while not newComp and attempts < 10:
                newComp = self.shuffleLevel(self.compendiumArr, config)
                if not newComp:
                    self.resetLevelToOriginal(self.compendiumArr)
                    attempts += 1
            if attempts >= 10:
                print('Major issue with generating demon levels and fusions')
                return False
            self.adjustSkillSlotsToLevel(newComp)
        else: newComp = self.compendiumArr

        
        if config.scaledPotentials:
            self.scalePotentials(newComp)

        #TODO: Consider case for potential weight or level dependency without random skills

        if config.randomSkills:
            self.assignRandomStartingSkill(self.nahobino, levelSkillList, config)
            self.assignRandomSkillsToProtofiend(self.protofiendArr, levelSkillList, config)
            newComp = self.assignRandomSkills(newComp,levelSkillList, config)
            if config.fixUniqueSkillAnimations:
                self.assignRandomSkills(self.playerBossArr, levelSkillList, config, mask=numbers.GUEST_IDS_WORKING_ANIMS_ONLY)
            else:
                self.assignRandomSkills(self.playerBossArr, levelSkillList, config, mask=numbers.GUEST_IDS)
        self.outputSkillSets() 
            

        if config.randomInnates:
            self.assignRandomInnates(newComp)
            self.assignRandomInnates(self.playerBossArr, mask=numbers.GUEST_IDS)
            self.assignRandomInnateToNahobino(self.nahobino)

        self.enemyArr = self.adjustBasicEnemyArr(self.enemyArr, newComp)
        if config.randomDemonLevels:
            newSymbolArr = self.adjustEncountersToSameLevel(self.encountSymbolArr, newComp, self.enemyArr)
            self.adjustTutorialPixie(newComp,self.eventEncountArr)
            self.assignTalkableTones(newComp)
        else:
            newSymbolArr = self.encountSymbolArr
            for demon in self.compendiumArr:
                if demon.ind not in numbers.BAD_IDS and 'Mitama' not in demon.name and 'NOT_USED' not in demon.name:
                    self.encounterReplacements[demon.ind] = demon.ind
        
        if config.randomDemonLevels or config.randomRaces:
            self.adjustFusionTableToLevels(self.normalFusionArr, self.compendiumArr)

        if config.randomShopEssences:
            self.adjustShopEssences(self.shopArr, self.essenceArr, newComp, self.configSettings.scaleItemsToArea)
        
        if (config.selfRandomizeNormalBosses or config.mixedRandomizeNormalBosses) and not (config.randomMusic or config.checkBasedMusic):
            self.patchMissingBossMusic()
        self.removeIshtarCopies()
        self.randomizeBosses()
        if config.selfRandomizeNormalBosses or config.mixedRandomizeNormalBosses:
            self.patchBossFlags()
            bossLogic.patchSpecialBossDemons(self.bossArr, self.configSettings)
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

        scriptLogic.randomizeDemonJoins(self.encounterReplacements,config.ensureDemonJoinLevel,self.scriptFiles)
            
        if config.randomChests:
            self.randomizeChests(self.configSettings.scaleItemsToArea)
        
        if self.configSettings.randomShopItems:
            self.randomizeShopItems(self.configSettings.scaleItemsToArea)
        self.replaceSpyglassInShop()
        self.adjustItemPrices()

        fakeMissions = self.randomizeItemRewards()
        
        if self.configSettings.selfRandomizeNormalBosses or self.configSettings.mixedRandomizeNormalBosses or self.configSettings.selfRandomizeOverworldBosses or self.configSettings.mixedRandomizeOverworldBosses:
            self.patchQuestBossDrops()
        if self.configSettings.randomEnemyDrops:
            self.randomizeBasicEnemyDrops(self.configSettings.scaleItemsToArea)
            self.randomizeBossDrops(self.configSettings.scaleItemsToArea)

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
        

        mapSymbolParamBuffer = self.scaleLargeSymbolDemonsDown(mapSymbolParamBuffer)
        self.adjustPunishingFoeSpeeds(mapSymbolParamBuffer)
            
        if DEV_CHEATS:
            self.applyCheats()


        message_logic.updateItemText(self.encounterReplacements, self.bossReplacements, self.enemyNames, self.compendiumArr,self.fusionSkillIDs, self.fusionSkillReqs, self.skillNames, magatsuhiSkillsRaces)
        message_logic.updateSkillDescriptions([self.skillArr, self.passiveSkillArr, self.innateSkillArr])
        message_logic.updateMissionInfo(self.encounterReplacements, self.bossReplacements, self.enemyNames, self.brawnyAmbitions2SkillName, fakeMissions, self.itemNames, self.configSettings.ensureDemonJoinLevel)
        message_logic.updateMissionEvents(self.encounterReplacements, self.bossReplacements, self.enemyNames, self.configSettings.ensureDemonJoinLevel)
        #message_logic.addHintMessages(self.bossReplacements, self.enemyNames)

        compendiumBuffer = self.updateBasicEnemyBuffer(compendiumBuffer, self.enemyArr)
        compendiumBuffer = self.updateBasicEnemyBuffer(compendiumBuffer, self.bossArr[numbers.NORMAL_ENEMY_COUNT:])
        compendiumBuffer = self.updateCompendiumBuffer(compendiumBuffer, newComp)
        compendiumBuffer = self.updateCompendiumBuffer(compendiumBuffer, self.playerBossArr[numbers.NORMAL_ENEMY_COUNT:])
        if self.configSettings.buffGuestYuzuru:
            self.patchYuzuruGLStats(compendiumBuffer)
        skillBuffer = self.updateSkillBuffer(skillBuffer, self.skillArr, self.passiveSkillArr, self.innateSkillArr, self.fusionSkillReqs)
        otherFusionBuffer = self.updateOtherFusionBuffer(otherFusionBuffer, self.specialFusionArr)
        normalFusionBuffer = self.updateNormalFusionBuffer(normalFusionBuffer, self.normalFusionArr)
        encountBuffer = self.updateEncounterBuffer(encountBuffer, newSymbolArr)
        playGrowBuffer = self.updateMCBuffer(playGrowBuffer, self.nahobino)
        itemBuffer = self.updateEssenceData(itemBuffer,self.essenceArr)
        shopBuffer = self.updateShopBuffer(shopBuffer, self.shopArr, self.mimanRewardsArr)
        eventEncountBuffer = self.updateEventEncountBuffer(eventEncountBuffer,self.eventEncountArr, eventEncountUassetBuffer)
        eventEncountPostBuffer = self.updateEventEncountPostBuffer(eventEncountPostBuffer, self.eventEncountArr)
        bossFlagBuffer = self.updateBossFlagBuffer(bossFlagBuffer)
        compendiumBuffer = self.updateProtofiendBuffer(compendiumBuffer, self.protofiendArr)
        battleEventsBuffer = self.updateBattleEventsBuffer(battleEventsBuffer, self.battleEventArr, battleEventUassetBuffer)
        devilAssetTableBuffer = self.updateDevilAssetBuffer(devilAssetTableBuffer, self.devilAssetArr)
        missionBuffer = self.updateMissionBuffer(missionBuffer, self.missionArr)
        devilUIBuffer = self.updateDevilUIBuffer(devilUIBuffer, self.devilUIArr)
        talkCameraBuffer = self.updateTalkCameraBuffer(talkCameraBuffer, self.talkCameraOffsets)
        abscessBuffer = self.updateAbscessBuffer(abscessBuffer)
        miracleBuffer = self.updateMiracleBuffer(miracleBuffer)
        uniqueSymbolBuffer = self.updateUniqueSymbolBuffer(uniqueSymbolBuffer)
        encountPostBuffer = self.updateEventEncountPostBuffer(encountPostBuffer, self.encountArr)
        chestBuffer = self.updateChestBuffer(chestBuffer)
        itemBuffer = self.updateConsumableData(itemBuffer, self.consumableArr)        


        #self.printOutEncounters(newSymbolArr)
        self.printOutFusions(self.normalFusionArr)
        #self.findUnlearnableSkills(skillLevels)

        self.writeFolder(paths.BLUEPRINTS_FOLDER_OUT)
        self.writeFolder(paths.GAMEDATA_FOLDER_OUT)
        self.writeFolder(paths.BINTABLE_FOLDER_OUT)
        self.writeFolder(paths.FACILITY_FOLDER_OUT)
        self.writeFolder(paths.BATTLE_FOLDER_OUT)
        self.writeFolder(paths.CAMP_FOLDER_OUT)
        self.writeFolder(paths.MIRACLE_TOP_FOLDER_OUT)
        self.writeFolder(paths.COMMON_TOP_FOLDER_OUT)
        self.writeFolder(paths.BLUEPRINTS_MAP_FOLDER_OUT)
        self.writeFolder(paths.MAP_ENCOUNT_FOLDER_OUT)
        self.writeFolder(paths.ENCOUNT_MOVER_FOLDER_OUT)
        self.writeFolder(paths.MOVER_PARAMTABLE_FOLDER_OUT)
        self.writeFolder(paths.TITLE_TEXTURE_FOLDER_OUT)

        self.writeBinaryTable(normalFusionBuffer.buffer, paths.UNITE_COMBINE_TABLE_OUT, paths.UNITE_FOLDER_OUT)
        self.writeBinaryTable(compendiumBuffer.buffer, paths.NKM_BASE_TABLE_OUT, paths.DEVIL_FOLDER_OUT)
        self.writeBinaryTable(skillBuffer.buffer, paths.SKILL_DATA_OUT, paths.SKILL_FOLDER_OUT)
        self.writeBinaryTable(otherFusionBuffer.buffer, paths.UNITE_TABLE_OUT, paths.UNITE_FOLDER_OUT)
        self.writeBinaryTable(encountBuffer.buffer, paths.ENCOUNT_DATA_OUT, paths.MAP_FOLDER_OUT)
        self.writeBinaryTable(playGrowBuffer.buffer, paths.MAIN_CHAR_DATA_OUT, paths.COMMON_FOLDER_OUT)
        self.writeBinaryTable(itemBuffer.buffer, paths.ITEM_DATA_OUT, paths.ITEM_FOLDER_OUT)
        self.writeBinaryTable(shopBuffer.buffer, paths.SHOP_DATA_OUT, paths.FACILITY_TABLE_FOLDER_OUT)
        self.writeBinaryTable(eventEncountBuffer.buffer, paths.EVENT_ENCOUNT_OUT, paths.MAP_FOLDER_OUT)
        self.writeBinaryTable(missionBuffer.buffer,paths.MISSION_DATA_OUT,paths.MISSION_FOLDER_OUT)
        self.writeBinaryTable(bossFlagBuffer.buffer, paths.BOSS_FLAG_DATA_OUT, paths.BOSS_FOLDER_OUT)
        self.writeBinaryTable(battleEventsBuffer.buffer, paths.BATTLE_EVENTS_OUT, paths.BATTLE_EVENT_FOLDER_OUT)
        self.writeBinaryTable(battleEventUassetBuffer.buffer,paths.BATTLE_EVENT_UASSET_OUT,paths.BATTLE_EVENTS_OUT)
        self.writeBinaryTable(devilAssetTableBuffer.buffer, paths.DEVIL_ASSET_TABLE_OUT, paths.ASSET_TABLE_FOLDER_OUT)
        self.writeBinaryTable(devilUIBuffer.buffer, paths.DEVIL_UI_OUT, paths.UI_GRAPHCIS_FOLDER_OUT)
        self.writeBinaryTable(talkCameraBuffer.buffer,paths.TALK_CAMERA_OFFSETS_OUT,paths.CAMP_STATUS_FOLDER_OUT)
        self.writeBinaryTable(abscessBuffer.buffer, paths.ABSCESS_TABLE_OUT, paths.MAP_FOLDER_OUT)
        self.writeBinaryTable(eventEncountPostBuffer.buffer, paths.EVENT_ENCOUNT_POST_DATA_TABLE_OUT, paths.ENCOUNT_POST_TABLE_FOLDER_OUT)
        self.writeBinaryTable(miracleBuffer.buffer, paths.MIRACLE_TABLE_OUT, paths.MIRACLE_FOLDER_OUT)
        #self.writeBinaryTable(eventEncountUassetBuffer.buffer, paths.EVENT_ENCOUNT_UASSET_OUT, paths.MAP_FOLDER_OUT)
        self.writeBinaryTable(uniqueSymbolBuffer.buffer, paths.UNIQUE_SYMBOL_DATA_OUT, paths.MAP_FOLDER_OUT)
        self.writeBinaryTable(encountPostBuffer.buffer, paths.ENCOUNT_POST_DATA_TABLE_OUT, paths.ENCOUNT_POST_TABLE_FOLDER_OUT)
        self.writeBinaryTable(encountPostUassetBuffer.buffer, paths.ENCOUNT_POST_DATA_TABLE_UASSET_OUT, paths.ENCOUNT_POST_TABLE_FOLDER_OUT)
        self.writeBinaryTable(chestBuffer.buffer, paths.CHEST_TABLE_OUT, paths.MAP_FOLDER_OUT)
        self.writeBinaryTable(mapSymbolParamBuffer.buffer, paths.MAP_SYMBOL_PARAM_OUT, paths.MOVER_PARAMTABLE_FOLDER_OUT)
        self.writeBinaryTable(eventEncountPostUassetBuffer.buffer, paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_OUT, paths.ENCOUNT_POST_TABLE_FOLDER_OUT)
        #self.copyFile(paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_IN, paths.EVENT_ENCOUNT_POST_DATA_TABLE_UASSET_OUT, paths.ENCOUNT_POST_TABLE_FOLDER_OUT)
        self.copyFile(paths.TITLE_TEXTURE_IN, paths.TITLE_TEXTURE_OUT, paths.TITLE_TEXTURE_FOLDER_OUT)
        self.copyFile(paths.TITLE_TEXTURE_UASSET_IN, paths.TITLE_TEXTURE_UASSET_OUT, paths.TITLE_TEXTURE_FOLDER_OUT)
        
        self.scriptFiles.writeFiles()

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
            #finalString = finalString + self.compendiumArr[fusion.firstDemon.ind].race.translation + " " + fusion.firstDemon.translation + " + " + self.compendiumArr[fusion.secondDemon.ind].race.translation + " " + fusion.secondDemon.translation + " = " + self.compendiumArr[fusion.result.ind].race.translation + " " + fusion.result.translation + '\n'
            finalString = finalString + fusion.firstDemon.translation + " + " + fusion.secondDemon.translation + " = " + fusion.result.translation + '\n'
        with open(paths.FUSION_DEBUG, 'w', encoding="utf-8") as file:
            file.write(finalString)
    
    def outputSkillSets(self):
        sortedDemons = sorted(self.compendiumArr, key=lambda demon: demon.level.value)
        with open(paths.SKILL_SET_DEBUG, 'w', encoding="utf-8") as file:
            for demon in sortedDemons:
                if "NOT USED" in demon.name:
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

                    
if __name__ == '__main__':
    rando = Randomizer()
    print('Warning: This is an early build of the randomizer and some things may not work as intended. Performance will be somewhat worse than vanilla SMTVV')
    print('Welcome to the SMTVV Rando v1.02. This version was created with game version 1.02 and will likely not work with other versions of SMTVV')
    try:
        rando.configSettings, rando.textSeed = gui.createGUI(rando.configSettings)
        rando.createSeed()
        
        rando.fullRando(rando.configSettings)
        if not rando.configSettings.fixUniqueSkillAnimations:
            print('"Fix unique skill animations" patch not applied. If the game appears to hang during a battle animation, press the skip animations button')
        print('\nRandomization complete! Place rando.pak in the Project/Content/Paks/~mods folder of your SMTVV game directory')
        print('CurrentSeed, bossSpoilerLog, encounterResults and fusionResults can be found in the debug folder')
       
    except RuntimeError:
        print('GUI closed - randomization was canceled')
    except Exception as e:
        traceback.print_exc()
        print(e)
        print('Unexpected error occured, randomization failed.\nPlease retry with different settings or send a screenshot of this error to the SMT Rando Discord\n https://discord.gg/d25ZAha')
    
    input('Press [Enter] to exit')
