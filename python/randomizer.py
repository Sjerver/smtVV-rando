from util.binary_table import Table
from base_classes.demons import Compendium_Demon, Enemy_Demon, Stat, Stats, Item_Drop, Item_Drops, Demon_Level
from base_classes.skills import Active_Skill, Passive_Skill, Skill_Condition, Skill_Conditions, Skill_Level
from base_classes.fusions import Normal_Fusion, Special_Fusion, Fusion_Chart_Node
from base_classes.encounters import Encounter_Symbol, Encounter, Possible_Encounter
from base_classes.base import Translated_Value, Weight_List
from base_classes.nahobino import Nahobino, LevelStats
import util.numbers as numbers
import util.paths as paths
import util.translation as translation
import math
import os
import random

RACE_ARRAY = ["None", "Unused", "Herald", "Megami", "Avian", "Divine", "Yoma", "Vile", "Raptor", "Unused9", "Deity", "Wargod", "Avatar", "Holy", "Genma", "Element", "Mitama", "Fairy", "Beast", "Jirae", "Fiend", "Jaki", "Wilder", "Fury", "Lady", "Dragon", "Kishin", "Kunitsu", "Femme", "Brute", "Fallen", "Night", "Snake", "Tyrant", "Drake", "Haunt", "Foul", "Chaos", "Devil", "Meta", "Nahobino", "Proto-fiend", "Matter", "Panagia", "Enigma", "UMA", "Qadistu", "Human", "Primal", "Void"]


class Randomizer:
    def __init__(self):
        self.maccaMod = numbers.getMaccaValues()
        self.expMod = numbers.getExpValues()

        self.compendiumNames = []
        self.skillNames = []

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
        self.nahobino = Nahobino()
        
    '''
    Reads the file that contains the demon table.
        Returns: 
            The bytes of the demon table file as a buffer
    '''
    def readNKMBaseTable(self):
        fileContents = Table(paths.NKM_BASE_TABLE_IN)
        return fileContents
    
    '''
    Reads the file that contains the skill table.
        Returns: 
            The bytes of the skill table file as a buffer
    '''
    def readSkillData(self):
        fileContents = Table(paths.SKILL_DATA_IN)
        return fileContents
    
    '''
    Reads the file that contains the fusion recipe table.
        Returns: 
            The bytes of the fusion recipe table file as a buffer
    '''
    def readNormalFusionTables(self):
        fileContents = Table(paths.UNITE_COMBINE_TABLE_IN)
        return fileContents
    
    '''
    Reads the file that contains the Special Fusion Table and the Fusion Chart Table.
        Returns: 
            The buffer containing the Special Fusion Table and the Fusion Chart Table
    '''
    def readOtherFusionTables(self):
        fileContents = Table(paths.UNITE_TABLE_IN)
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
        with open(paths.SKILL_NAME_IN, 'r') as file:
            fileContents = file.read()   
            tempArray = fileContents.split("MessageLabel=")
            for element in tempArray:
                sliceStart = element.find("MessageTextPages_3=")
                sliceEnd = element.find("Voice=")
                self.skillNames.append(element[sliceStart + 19:sliceEnd - 7])
        return fileContents
    
    '''
    Reads the file that contains the encounter tables as a buffer.
        Returns: 
            The buffer containing the encounter tables.
    '''
    def readEncounterData(self):
        fileContents = Table(paths.ENCOUNT_DATA_IN)
        return fileContents
    
    '''
    Reads the file that contains the main character data as a buffer.
        Returns: 
            The buffer containing the main character data.
    '''
    def readMCData(self):
        fileContents = Table(paths.MAIN_CHAR_DATA_IN)
        return fileContents
    
    '''
    Writes the given Buffer to the file NKMBaseTable.uexp.
        Parameters:
            result (Buffer): The demon data to write 
    '''
    def writeNKMBaseTable(self, result):
        if not os.path.exists(paths.DEVIL_FOLDER_OUT):
            os.mkdir(paths.DEVIL_FOLDER_OUT)
        with open(paths.NKM_BASE_TABLE_OUT, 'wb') as file:
            file.write(result)
            
    '''
    Writes the given Buffer to the file SkillData.uexp.
        Parameters:
            result (Buffer): The skill data to write 
    '''
    def writeSkillData(self, result):
        if not os.path.exists(paths.SKILL_FOLDER_OUT):
            os.mkdir(paths.SKILL_FOLDER_OUT)
        with open(paths.SKILL_DATA_OUT, 'wb') as file:
            file.write(result)
            
    '''
    Writes the given Buffer to the file UniteCombineTable.uexp.
        Parameters:
            result (Buffer): The normal fusion data to write 
    '''
    def writeNormalFusionTable(self, result):
        if not os.path.exists(paths.UNITE_FOLDER_OUT):
            os.mkdir(paths.UNITE_FOLDER_OUT)
        with open(paths.UNITE_COMBINE_TABLE_OUT, 'wb') as file:
            file.write(result)
            
    '''
    Writes the given Buffer to the file UniteTable.uexp.
        Parameters:
            result (Buffer): The special fusion data to write 
    '''
    def writeOtherFusionTable(self, result):
        if not os.path.exists(paths.UNITE_FOLDER_OUT):
            os.mkdir(paths.UNITE_FOLDER_OUT)
        with open(paths.UNITE_TABLE_OUT, 'wb') as file:
            file.write(result)
            
    '''
    Writes the given Buffer to the file EncountData.uexp.
        Parameters:
            result (Buffer): The encounter data to write 
    '''
    def writeEncounterData(self, result):
        if not os.path.exists(paths.MAP_FOLDER_OUT):
            os.mkdir(paths.MAP_FOLDER_OUT)
        with open(paths.ENCOUNT_DATA_OUT, 'wb') as file:
            file.write(result)

    '''
    Writes the given Buffer to the file PlayerGrow.uexp.
        Parameters:
            result (Buffer): The main character data to write 
    '''
    def writeMCData(self, result):
        if not os.path.exists(paths.COMMON_FOLDER_OUT):
            os.mkdir(paths.COMMON_FOLDER_OUT)
        with open(paths.MAIN_CHAR_DATA_OUT, 'wb') as file:
            file.write(result)
            
    '''
    Fills the array compendiumArr with data extracted from the Buffer NKMBaseTable.
    The end array contains data on all demons which are registered in the compendium and usable by the player.
        Parameters:
            NKMBaseTable (Table): the buffer to get the demon data from
    '''
    def fillCompendiumArr(self, NKMBaseTable):

        startValue = 0x69
        raceOffset = 0x0C
        demonOffset = 0x1D0


        #For all demons in the compendium...
        for index in range(395):
            #First define all relevant offsets
            offset = startValue + demonOffset * index
            locations = {
                'race': offset - raceOffset,
                'level': offset,
                'HP': offset + 0x1C,
                'firstSkill': offset + 0x70,
                'firstLearnedLevel': offset + 0xA0,
                'fusability': offset + 0x56,
                'unlockFlags': offset + 0x60,
                'tone': offset + 0x58,
                'innate': offset + 0x100,
                'potential': offset + 0X174
            }
            #Then read the list of initial skills learned
            listOfSkills = []
            for i in range(8):
                skillID = NKMBaseTable.read_word(locations['firstSkill'] + 4 * i)
                if skillID != 0:
                    listOfSkills.append(Translated_Value(skillID, translation.translateSkillID(skillID, self.skillNames)))
            #Read the list of learnable skills 
            listOfLearnedSkills = []
            for i in range(8):
                #print(locations['firstLearnedLevel'])
                skillID = NKMBaseTable.read_word(locations['firstLearnedLevel'] + 8 * i + 4)
                if skillID != 0:
                    listOfLearnedSkills.append(Translated_Value(skillID, translation.translateSkillID(skillID, self.skillNames),
                                                                level=NKMBaseTable.read_word(locations['firstLearnedLevel'] + 8 * i)))
            demon = Compendium_Demon()
            demon.ind = index
            demon.name = self.compendiumNames[index]
            demon.offsetNumbers = locations
            demon.race = Translated_Value(NKMBaseTable.read_byte(locations['race']), RACE_ARRAY[NKMBaseTable.read_byte(locations['race'])])
            demon.level = Demon_Level(NKMBaseTable.read_word(locations['level']), NKMBaseTable.read_word(locations['level']))
            demon.registerable = NKMBaseTable.read_word(locations['HP'] - 4)
            demon.fusability = NKMBaseTable.read_halfword(locations['fusability'])
            demon.unlockFlags = [NKMBaseTable.read_byte(locations['unlockFlags']), NKMBaseTable.read_byte(locations['unlockFlags'] + 1)]
            demon.tone = Translated_Value(NKMBaseTable.read_byte(locations['tone']), '', secondary=NKMBaseTable.read_byte(locations['tone'] + 1))
            demon.resist.physical = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4)))
            demon.resist.fire = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 2),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 2)))
            demon.resist.ice = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 3),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 3)))
            demon.resist.electric = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 4),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 4)))
            demon.resist.force = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 5),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 5)))
            demon.resist.light = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 6),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 6)))
            demon.resist.dark = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 7),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 7)))
            demon.resist.almighty = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 8),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 8)))
            demon.resist.poison = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 9),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 9)))
            demon.resist.confusion = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 11),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 11)))
            demon.resist.charm = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 12),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 12)))
            demon.resist.sleep = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 13),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 13)))
            demon.resist.seal = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 14),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 14)))
            demon.resist.mirage = Translated_Value(NKMBaseTable.read_word(locations['innate'] + 4 * 21),
                                                     translation.translateResist(NKMBaseTable.read_word(locations['innate'] + 4 * 21)))
            demon.potential.physical = NKMBaseTable.read_word(locations['potential'])
            demon.potential.fire = NKMBaseTable.read_word(locations['potential'] + 4 * 1)
            demon.potential.ice = NKMBaseTable.read_word(locations['potential'] + 4 * 2)
            demon.potential.elec = NKMBaseTable.read_word(locations['potential'] + 4 * 3)
            demon.potential.force = NKMBaseTable.read_word(locations['potential'] + 4 * 4)
            demon.potential.light = NKMBaseTable.read_word(locations['potential'] + 4 * 5)
            demon.potential.dark = NKMBaseTable.read_word(locations['potential'] + 4 * 6)
            demon.potential.almighty = NKMBaseTable.read_word(locations['potential'] + 4 * 7)
            demon.potential.ailment = NKMBaseTable.read_word(locations['potential'] + 4 * 8)
            demon.potential.recover = NKMBaseTable.read_word(locations['potential'] + 4 * 10)
            demon.potential.support = NKMBaseTable.read_word(locations['potential'] + 4 * 9)
            demonHP = Stat(NKMBaseTable.read_word(locations['HP'] + 4 * 0), NKMBaseTable.read_word(locations['HP'] + 4 * 2), NKMBaseTable.read_word(locations['HP'] + 4 * 0))
            demonMP = Stat(NKMBaseTable.read_word(locations['HP'] + 4 * 1), NKMBaseTable.read_word(locations['HP'] + 4 * 3),  NKMBaseTable.read_word(locations['HP'] + 4 * 1))
            demonStr = Stat(NKMBaseTable.read_word(locations['HP'] + 4 * 4), NKMBaseTable.read_word(locations['HP'] + 4 * 9),  NKMBaseTable.read_word(locations['HP'] + 4 * 4))
            demonVit = Stat(NKMBaseTable.read_word(locations['HP'] + 4 * 5), NKMBaseTable.read_word(locations['HP'] + 4 * 10),  NKMBaseTable.read_word(locations['HP'] + 4 * 5))
            demonMag = Stat(NKMBaseTable.read_word(locations['HP'] + 4 * 6), NKMBaseTable.read_word(locations['HP'] + 4 * 11),  NKMBaseTable.read_word(locations['HP'] + 4 * 6))
            demonAgi = Stat(NKMBaseTable.read_word(locations['HP'] + 4 * 7), NKMBaseTable.read_word(locations['HP'] + 4 * 12),  NKMBaseTable.read_word(locations['HP'] + 4 * 7))
            demonLuk = Stat(NKMBaseTable.read_word(locations['HP'] + 4 * 8), NKMBaseTable.read_word(locations['HP'] + 4 * 13),  NKMBaseTable.read_word(locations['HP'] + 4 * 8))
            demon.stats = Stats(demonHP, demonMP, demonStr, demonVit, demonMag, demonAgi, demonLuk)
            demon.innate = Translated_Value(NKMBaseTable.read_word(locations['innate']),
                                            translation.translateSkillID(NKMBaseTable.read_word(locations['innate']), self.skillNames))
            demon.skills = listOfSkills
            demon.learnedSkills = listOfLearnedSkills
            #Add read demon data to compendium
            self.compendiumArr.append(demon)
        self.defineLevelForUnlockFlags(self.compendiumArr)
        
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
            if index >= 400 and index < 801:
                offset = passiveStartValue + passiveOffset * (index - 400)
                locations = {
                    'hpIncrease': offset,
                    'survive': offset + 15,
                    'element': offset + 17,
                    'physResist': offset + 34,
                    'effect': offset + 52,
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
                toPush.hpIncrease = skillData.read_byte(locations['hpIncrease'])
                toPush.mpIncrease = skillData.read_byte(locations['hpIncrease'] + 1)
                toPush.counterChance = skillData.read_byte(locations['hpIncrease'] + 3)
                toPush.survive = skillData.read_byte(locations['survive'])
                toPush.element = Translated_Value(skillData.read_byte(locations['element']),
                                                  translation.translatePassiveElementType(skillData.read_byte(locations['element'])))
                toPush.resists.type = Translated_Value(skillData.read_byte(locations['element'] + 1),
                                                       translation.translatePassiveResist(skillData.read_byte(locations['element'] + 1)))
                toPush.resists.physical = skillData.read_byte(locations['physResist'])
                toPush.resists.fire = skillData.read_byte(locations['physResist'] + 1)
                toPush.resists.ice = skillData.read_byte(locations['physResist'] + 2)
                toPush.resists.elec = skillData.read_byte(locations['physResist'] + 3)
                toPush.resists.force = skillData.read_byte(locations['physResist'] + 4)
                toPush.resists.dark = skillData.read_byte(locations['physResist'] + 5)
                toPush.resists.light = skillData.read_byte(locations['physResist'] + 6)
                toPush.effect1 = skillData.read_halfword(locations['effect'])
                toPush.effect1Amount = skillData.read_halfword(locations['effect'] + 2)
                toPush.effect2 = skillData.read_halfword(locations['effect'] + 4)
                toPush.effect2Amount = skillData.read_halfword(locations['effect'] + 6)
                #If skill is in the innate area push to innateSkillArr else push to passiveSkillArr
                if (index >= 530):
                    self.innateSkillArr.append(toPush)
                else:
                    self.passiveSkillArr.append(toPush)

            else:
                #console.log(index)
                offset = startValue + skillOffset * index
                #While the skillTable starts with id 1, I do not read the ID from the data (which I really should)
                skillID = index + 1
                skillName = translation.translateSkillID(index + 1, self.skillNames)

                #if skill is in the second batch of active skills, we calculate the offset a different way and index = id is working
                if (index >= 800):
                    skillName = translation.translateSkillID(index, self.skillNames)
                    skillID = index
                    offset = secondBatchStart + skillOffset * (index - 801)
                locations = {
                    'cost': offset + 8,
                    'skillType': offset + 10,
                    'element': offset + 12,
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
                    'condition1': offset + 140
                }
                toPush = Active_Skill()
                toPush.ind = skillID
                toPush.name = skillName
                toPush.offsetNumber = locations
                toPush.cost = skillData.read_halfword(locations['cost'])
                toPush.rank = skillData.read_byte(locations['hpDrain'] + 3)
                toPush.skillType = Translated_Value(skillData.read_byte(locations['skillType']),
                                                  translation.translateSkillType(skillData.read_byte(locations['skillType'])))
                toPush.potentialType = Translated_Value(skillData.read_byte(locations['icon'] + 1),
                                                        translation.translatePotentialType(skillData.read_byte(locations['icon'] + 1)))
                toPush.element = Translated_Value(skillData.read_byte(locations['element']),
                                                  translation.translateSkillElement(skillData.read_byte(locations['element'])))
                toPush.skillIcon = skillData.read_byte(locations['icon'])
                toPush.target = Translated_Value(skillData.read_byte(locations['target']),
                                                 translation.translateTarget(skillData.read_byte(locations['target'])))
                toPush.minHits = skillData.read_byte(locations['minHit'])
                toPush.maxHits = skillData.read_byte(locations['maxHit'])
                toPush.crit = skillData.read_byte(locations['critRate'])
                toPush.power = skillData.read_word(locations['power'])
                toPush.hit = skillData.read_byte(locations['hitRate'])
                toPush.ailmentFlags.instakill = skillData.read_byte(locations['ailmentFlag'])
                toPush.ailmentFlags.poison = skillData.read_byte(locations['ailmentFlag'] + 1)
                toPush.ailmentFlags.confusion = skillData.read_byte(locations['ailmentFlag'] + 3)
                toPush.ailmentFlags.charm = skillData.read_byte(locations['ailmentFlag'] + 4)
                toPush.ailmentFlags.sleep = skillData.read_byte(locations['ailmentFlag'] + 5)
                toPush.ailmentFlags.seal = skillData.read_byte(locations['ailmentFlag'] + 6)
                toPush.ailmentFlags.mirage = skillData.read_byte(locations['ailmentFlag'] + 9)
                toPush.ailmentFlags.mud = skillData.read_byte(locations['ailmentFlag'] + 14)
                toPush.ailmentFlags.shroud = skillData.read_byte(locations['ailmentFlag'] + 15)
                toPush.healing.overMaxHP = skillData.read_byte(locations['healing']['overMaxHP'])
                toPush.healing.effect = skillData.read_byte(locations['healing']['effect'])
                toPush.healing.flag = skillData.read_word(locations['resistEnable'] + 8)
                toPush.healing.percent = skillData.read_byte(locations['resistEnable'] + 12)
                toPush.pierce = skillData.read_byte(locations['pierce'])
                toPush.ailmentChance = skillData.read_byte(locations['ailmentChance'])
                toPush.buff.timer = skillData.read_byte(locations['buffstimer'])
                toPush.buff.physical = skillData.read_word(locations['buffstimer'] + 1)
                toPush.buff.magical = skillData.read_word(locations['buffstimer'] + 5)
                toPush.buff.defense = skillData.read_word(locations['buffstimer'] + 9)
                toPush.buff.accEva = skillData.read_word(locations['buffstimer'] + 13)
                toPush.resists.enable = skillData.read_byte(locations['resistEnable'])
                toPush.resists.physical = Translated_Value(skillData.read_byte(locations['resistEnable'] + 1),
                        translation.translatePassiveResist(skillData.read_byte(locations['resistEnable'] + 1)))
                toPush.resists.fire = Translated_Value(skillData.read_byte(locations['resistEnable'] + 2),
                        translation.translatePassiveResist(skillData.read_byte(locations['resistEnable'] + 2)))
                toPush.resists.ice = Translated_Value(skillData.read_byte(locations['resistEnable'] + 3),
                        translation.translatePassiveResist(skillData.read_byte(locations['resistEnable'] + 3)))
                toPush.resists.elec = Translated_Value(skillData.read_byte(locations['resistEnable'] + 4),
                        translation.translatePassiveResist(skillData.read_byte(locations['resistEnable'] + 4)))
                toPush.resists.force = Translated_Value(skillData.read_byte(locations['resistEnable'] + 5),
                        translation.translatePassiveResist(skillData.read_byte(locations['resistEnable'] + 5)))
                toPush.resists.light = Translated_Value(skillData.read_byte(locations['resistEnable'] + 6),
                        translation.translatePassiveResist(skillData.read_byte(locations['resistEnable'] + 6)))
                toPush.resists.dark = Translated_Value(skillData.read_byte(locations['resistEnable'] + 7),
                        translation.translatePassiveResist(skillData.read_byte(locations['resistEnable'] + 7)))
                toPush.hpDrain = skillData.read_byte(locations['hpDrain']),
                toPush.mpDrain = skillData.read_byte(locations['hpDrain'] + 1)
                toPush.magatsuhi.enable = skillData.read_byte(locations['magatsuhiFlag'])
                toPush.magatsuhi.race1 = Translated_Value(skillData.read_byte(locations['magatsuhiFlag'] + 1),
                        RACE_ARRAY[skillData.read_byte(locations['magatsuhiFlag'] + 1)])
                toPush.magatsuhi.race2 = Translated_Value(skillData.read_byte(locations['magatsuhiFlag'] + 3),
                        RACE_ARRAY[skillData.read_byte(locations['magatsuhiFlag'] + 3)])
                toPush.modifiers.modifier1 = Translated_Value(skillData.read_byte(locations['modifier1']),
                        translation.translateModifier(skillData.read_byte(locations['modifier1'])))
                toPush.modifiers.modifier2 = Translated_Value(skillData.read_byte(locations['modifier1'] + 1),
                        translation.translateModifier(skillData.read_byte(locations['modifier1'] + 1)))
                toPush.modifiers.modifier3 = Translated_Value(skillData.read_byte(locations['modifier1'] + 2),
                        translation.translateModifier(skillData.read_byte(locations['modifier1'] + 2)))
                toPush.modifiers.modifier4 = Translated_Value(skillData.read_byte(locations['modifier1'] + 3),
                        translation.translateModifier(skillData.read_byte(locations['modifier1'] + 3)))
                condition1 = Skill_Condition()
                condition1.value = skillData.read_byte(locations['condition1'])
                condition1.ailmentCondition = skillData.read_byte(locations['condition1'] + 1)
                condition1.effect = skillData.read_halfword(locations['condition1'] + 2)
                condition1.amount = skillData.read_halfword(locations['condition1'] + 4)
                condition2 = Skill_Condition()
                condition2.value = skillData.read_byte(locations['condition1'] + 8)
                condition2.ailmentCondition = skillData.read_byte(locations['condition1'] + 9)
                condition2.effect = skillData.read_halfword(locations['condition1'] + 11)
                condition2.amount = skillData.read_halfword(locations['condition1'] + 13)
                toPush.conditions = Skill_Conditions(condition1, condition2)
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
            firstDemon = Translated_Value(fusionData.read_word(locations['firstDemon']),
                self.compendiumArr[fusionData.read_word(locations['firstDemon'])].name)
            secondDemon = Translated_Value(fusionData.read_word(locations['secondDemon']),
                self.compendiumArr[fusionData.read_word(locations['secondDemon'])].name)
            result = Translated_Value(fusionData.read_word(locations['result']),
                self.compendiumArr[fusionData.read_word(locations['result'])].name)
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
            race1 = Translated_Value(fusionData.read_byte(offset), RACE_ARRAY[fusionData.read_byte(offset)])
            race2 = Translated_Value(fusionData.read_byte(offset + 1), RACE_ARRAY[fusionData.read_byte(offset + 1)])
            result = Translated_Value(fusionData.read_byte(offset + 2), RACE_ARRAY[fusionData.read_byte(offset + 2)])
            self.fusionChartArr.append(Fusion_Chart_Node(offset, race1, race2, result))
            
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
            fusion.ind = fusionData.read_halfword(offset)
            fusion.resultLevel = self.compendiumArr[fusionData.read_halfword(offset + 10)].level.original
            fusion.baseOffset = offset
            fusion.demon1 = Translated_Value(fusionData.read_halfword(offset + 2), self.compendiumArr[fusionData.read_halfword(offset + 2)].name)
            fusion.demon2 = Translated_Value(fusionData.read_halfword(offset + 4), self.compendiumArr[fusionData.read_halfword(offset + 4)].name)
            fusion.demon3 = Translated_Value(fusionData.read_halfword(offset + 6), self.compendiumArr[fusionData.read_halfword(offset + 6)].name)
            fusion.demon4 = Translated_Value(fusionData.read_halfword(offset + 8), self.compendiumArr[fusionData.read_halfword(offset + 8)].name)
            fusion.result = Translated_Value(fusionData.read_halfword(offset + 10), self.compendiumArr[fusionData.read_halfword(offset + 10)].name)
            self.specialFusionArr.append(fusion)
            
    '''
    Fills the Array enemyArr with data for all basic enemy versions of playable demons.
        Parameters:
            enemyData (Table): the buffer to get the enemy data from 
    '''
    def fillBasicEnemyArr(self, enemyData):

        startValue = 0x88139
        enemyOffset = 0x170

        #For all Enemy version of playable demon indeces
        for index in range(395):
            #First define all relevant offsets
            offset = startValue + enemyOffset * index
            locations = {
                'level': offset,
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
                skillID = enemyData.read_word(locations['firstSkill'] + 4 * i)
                if skillID != 0:
                    listOfSkills.append(Translated_Value(skillID, translation.translateSkillID(skillID, self.skillNames)))       
            demon = Enemy_Demon()
            demon.ind = index
            demon.name = self.compendiumNames[index]
            demon.offsetNumbers = locations
            demon.level = enemyData.read_word(locations['level'])
            demon.stats = Stats(enemyData.read_word(locations['HP']), enemyData.read_word(locations['HP'] + 4), enemyData.read_word(locations['HP'] + 8),
                                    enemyData.read_word(locations['HP'] + 12), enemyData.read_word(locations['HP'] + 16),
                                    enemyData.read_word(locations['HP'] + 20), enemyData.read_word(locations['HP'] + 24)) #HP, MP, str, vit, mag, agi, luk
            demon.analyze = enemyData.read_byte(locations['HP'] + 28)
            demon.levelDMGCorrection = enemyData.read_byte(locations['HP'] + 30)
            demon.AI = enemyData.read_word(locations['experience'] + 12) #55 for normal encounters
            demon.recruitable = enemyData.read_byte(locations['HP'] + 33)
            demon.pressTurns = enemyData.read_byte(locations['pressTurns'])
            demon.experience = enemyData.read_word(locations['experience'])
            demon.money = enemyData.read_word(locations['experience'] + 4)
            demon.skills = listOfSkills
            itemDrop1 = Item_Drop(enemyData.read_word(locations['item']), translation.translateItem(enemyData.read_word(locations['item'])),
                                                      enemyData.read_word(locations['item'] + 4), enemyData.read_word(locations['item'] + 8))
            itemDrop3 = Item_Drop(enemyData.read_word(locations['item'] + 12), translation.translateItem(enemyData.read_word(locations['item'] + 12)),
                                                      enemyData.read_word(locations['item'] + 16), enemyData.read_word(locations['item'] + 20))
            itemDrop2 = Item_Drop(enemyData.read_word(locations['item'] + 24), translation.translateItem(enemyData.read_word(locations['item'] + 24)),
                                                      enemyData.read_word(locations['item'] + 28), enemyData.read_word(locations['item'] + 32))
            demon.drops = Item_Drops(itemDrop1, itemDrop2, itemDrop3)
            demon.innate = Translated_Value(enemyData.read_word(locations['innate']), self.obtainSkillFromID(enemyData.read_word(locations['innate'])).name)
            demon.resist.physical = Translated_Value(enemyData.read_word(locations['innate'] + 4),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4)))
            demon.resist.fire = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 2),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 2)))
            demon.resist.ice = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 3),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 3)))
            demon.resist.electric = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 4),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 4)))
            demon.resist.force = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 5),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 5)))
            demon.resist.light = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 6),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 6)))
            demon.resist.dark = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 7),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 7)))
            demon.resist.almighty = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 8),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 8)))
            demon.resist.poison = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 9),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 9)))
            demon.resist.confusion = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 11),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 11)))
            demon.resist.charm = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 12),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 12)))
            demon.resist.sleep = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 13),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 13)))
            demon.resist.seal = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 14),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 14)))
            demon.resist.mirage = Translated_Value(enemyData.read_word(locations['innate'] + 4 * 21),
                                                     translation.translateResist(enemyData.read_word(locations['innate'] + 4 * 21)))
            demon.potential.physical = enemyData.read_word(locations['potential'])
            demon.potential.fire = enemyData.read_word(locations['potential'] + 4 * 1)
            demon.potential.ice = enemyData.read_word(locations['potential'] + 4 * 2)
            demon.potential.elec = enemyData.read_word(locations['potential'] + 4 * 3)
            demon.potential.force = enemyData.read_word(locations['potential'] + 4 * 4)
            demon.potential.light = enemyData.read_word(locations['potential'] + 4 * 5)
            demon.potential.dark = enemyData.read_word(locations['potential'] + 4 * 6)
            demon.potential.almighty = enemyData.read_word(locations['potential'] + 4 * 7)
            demon.potential.ailment = enemyData.read_word(locations['potential'] + 4 * 8)
            demon.potential.recover = enemyData.read_word(locations['potential'] + 4 * 10)
            demon.potential.support = enemyData.read_word(locations['potential'] + 4 * 9)
            self.enemyArr.append(demon)
            
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
                encId = encounters.read_halfword(locations['encounter1'] + 4 * i)
                possEnc.append(Possible_Encounter(encId, self.encountArr[encId], encounters.read_halfword(locations['encounter1Chance'] + 4 * i)))

            ind = encounters.read_halfword(locations['symbol'])
            translation = "NO BASIC ENEMY" #Since non base demons arent saved anywhere currently use this filler name
            if (ind < len(self.compendiumArr)):
                translation = self.compendiumArr[encounters.read_halfword(locations['symbol'])].name
            symbol = Translated_Value(ind, translation)
            self.encountSymbolArr.append(Encounter_Symbol(
                index, symbol, locations, encounters.read_word(locations['flags']), possEnc
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
                'demon': offset + 4,
            }
            demons = [encounters.read_halfword(offset + 4), encounters.read_halfword(offset + 6), encounters.read_halfword(offset + 8),
                      encounters.read_halfword(offset + 10), encounters.read_halfword(offset + 12), encounters.read_halfword(offset + 14)]
            self.encountArr.append(Encounter(index, locations, encounters.read_halfword(offset), demons))
            
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
            'affStart': 0x2B10
        }

        #Table in PlayerGrow is defined for level 0 until level 150
        for index in range(151):
            offset = start + size * index
            self.nahobino.stats.append(LevelStats(index,playGrow.read_word(offset + 4 * 0),playGrow.read_word(offset + 4 * 1),playGrow.read_word(offset + 4 * 2),playGrow.read_word(offset + 4 * 3),playGrow.read_word(offset + 4 * 4),playGrow.read_word(offset + 4 * 5),playGrow.read_word(offset + 4 * 6)))
        
        self.nahobino.offsetNumbers = locations
        
        self.nahobino.startingSkill = playGrow.read_word(locations['startingSkill'])
       
        self.nahobino.resist.physical = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 0),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 * 0)))
        self.nahobino.resist.fire = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 1),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *1)))
        self.nahobino.resist.ice = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 2),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *2)))
        self.nahobino.resist.electric = Translated_Value(playGrow.read_word(locations['affStart'] + 4 *3),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *3)))
        self.nahobino.resist.force = Translated_Value(playGrow.read_word(locations['affStart'] + 4 *4),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *4)))
        self.nahobino.resist.light = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 5),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *5)))
        self.nahobino.resist.dark = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 6),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *6)))
        self.nahobino.resist.almighty = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 7),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *7)))
        self.nahobino.resist.poison = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 8),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *8)))
        self.nahobino.resist.confusion = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 10),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *10)))
        self.nahobino.resist.charm = Translated_Value(playGrow.read_word(locations['affStart'] + 4  * 11),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *11)))
        self.nahobino.resist.sleep = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 12),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *12)))
        self.nahobino.resist.seal = Translated_Value(playGrow.read_word(locations['affStart'] + 4 * 13),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 *13)))
        self.nahobino.resist.mirage = Translated_Value(playGrow.read_word(locations['affStart'] + 4  *20),translation.translateResist(playGrow.read_word(locations['affStart'] + 4 * 20)))

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
    Assigns every demon a random skill that could be learned at their level
        Parameters:
            comp (Array): The array of demons
            levelList (Array(Skill_Level)): The list of levels and their learnable skills
        Returns:
            The edited compendium
    '''
    def assignCompletelyRandomSkills(self, comp, levelList):
        #For every demon
        for demon in comp:
            #get all skills that can be learned at the demons level
            possibleSkills = levelList[demon.level.value]
            #Replace every initially learned skill of the demon with a random skill of the possible skills
            for index in range(len(demon.skills)):
                newID = random.choice(possibleSkills).ind
                newName = translation.translateSkillID(newID, self.skillNames)
                demon.skills[index] = Translated_Value(newID, newName)
        return comp
    
    '''
    Assigns every demon new skills randomized based on weights by including the levels above and below them
        Parameters:
            comp (Array): The array of demons
            levelList (Array(Skill_Level)): The list of levels and their learnable skills
        Returns:
            The edited compendium
    '''
    def assignCompletelyRandomWeightedSkills(self, comp, levelList):
        #For every demon...
        for demon in comp:
            possibleSkills = []
            #get all skills that can be learned at the demons level
            possibleSkills = levelList[demon.level.value]
            #And add the skills at learned at the level below and on top
            if demon.level.value < 99:
                possibleSkills = possibleSkills + levelList[demon.level.value + 1]
            if demon.level.value > 1:
                possibleSkills = possibleSkills + levelList[demon.level.value - 1]
            #Create the weighted list of skills
            weightedSkills = self.createWeightedList(possibleSkills)
            if len(weightedSkills.values) > 0:
                #For every skill change the id to a random one that is not already assigned
                for index in range(len(demon.skills)):
                    uniqueSkill = False
                    rng = 0
                    while not uniqueSkill:
                        rng = self.weightedRando(weightedSkills.values, weightedSkills.weights)
                        if not any(e.ind == rng for e in demon.skills):
                            uniqueSkill = True
                    demon.skills[index] = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
            #if(demon.ind ==345) {console.log(demon.skills)}
        return comp

    '''
    Assigns every demon new skills randomized based on weights.
    The weights are compromised of the skills learnable at the demons level and up to 3 level below and above them.
    Additionally the weights are adjusted to match the skill potential of demons, making skills with positive potential more likely and negative potential less likely if not impossible.
        Parameters: 
            comp (Array): The array of demons
            levelList (Array(Skill_Level)): The list of levels and their learnable skills
        Returns:
            The edited compendium
    '''
    def assignRandomPotentialWeightedSkills(self, comp, levelList):
        #For every demon...
        for demon in comp:
            possibleSkills = []
        
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
        
            #Create the weighted list of skills and update it with potentials
            weightedSkills = self.createWeightedList(possibleSkills)
            weightedSkills = self.updateWeightsWithPotential(weightedSkills, demon.potential, demon)

            totalSkills = []
            #If there are skills to be learned
            if len(weightedSkills.values) > 0:
                #For every skill change the id to a random one that is not already assigned to this demon
                for index in range(len(demon.skills)):
                    uniqueSkill = False
                    rng = 0
                    attempts = 100
                    while not uniqueSkill:
                        rng = self.weightedRando(weightedSkills.values, weightedSkills.weights)
                        if attempts <= 0:
                            print("Something went wrong in skill rando at level " + str(demon.level.value))
                            weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                            uniqueSkill = True
                            break
                        if not any(e.ind == rng for e in totalSkills):
                            if self.checkAdditionalSkillConditions(self.obtainSkillFromID(rng), totalSkills, demon):
                                uniqueSkill = True
                                weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                        attempts -= 1
                    skillAddition = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
                    totalSkills.append(skillAddition)
                    demon.skills[index] = skillAddition
                #Randomly assign learnable skills
                for index in range(len(demon.learnedSkills)):
                    uniqueSkill = False
                    rng = 0
                    attempts = 100
                    while not uniqueSkill:
                        rng = self.weightedRando(weightedSkills.values, weightedSkills.weights)
                        if attempts <= 0:
                            print("Something went wrong in leanred skill rando at level " + str(demon.level.value) + "for demon " + str(demon.name))
                            weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                            uniqueSkill = True
                        if not any(e.ind == rng for e in totalSkills):
                            if self.checkAdditionalSkillConditions(self.obtainSkillFromID(rng), totalSkills, demon):
                                uniqueSkill = True
                                weightedSkills.weights[weightedSkills.values.index(rng)] = 0
                        attempts -= 1
                    skillAddition = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames))
                    totalSkills.append(skillAddition)
                    demon.learnedSkills[index] = Translated_Value(rng, translation.translateSkillID(rng, self.skillNames), level=demon.learnedSkills[index].level)
        return comp
    
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
        if (len(totalSkillList) + 1 == len(demon.skills)) and ((self.determineSkillStructureByID(skill.ind) != "Active") and any(self.determineSkillStructureByID(e.ind) == "Active" for e in totalSkillList)):
            #Check if we are at last initial skill and we have at least one active or current one is active
            return False

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
            skillStructure = self.determineSkillStructureByID(skill.ind)
            #Passive skills do not have a corresponding potential by default so we need to handle them seperately
            if skillStructure == "Active":
                potentialType = skill.potentialType.translation
                potentialValue = self.obtainPotentialByName(potentialType, potentials)
                if potentialValue > 100: #negative potential
                    potentialValue = -1 * (0x100000000 - potentialValue)
                additionalWeight = 2 * potentialValue
                if skill.skillType.value == 0 and demon.stats.str.start < demon.stats.mag.start:
                    additionalWeight = additionalWeight - 2
                elif skill.skillType.value == 1 and demon.stats.str.start > demon.stats.mag.start:
                    additionalWeight = additionalWeight - 2
                #if(skill.name == "Profaned Land") {additonalWeight = additionalWeight * additionalWeight}
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
    Based on array of skills creates two arrays where each skill is only included once.
    Skills that were originally present more than once have increased weight.
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
            if skill.ind in ids:
                prob[ids.index(skill.ind)] += 1
            else:
                #else push value and base weight 
                ids.append(skill.ind)
                prob.append(1)
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
            buffer.write_word(demon.stats.HP.start,demon.offsetNumbers['HP'] + 4 * 0)
            buffer.write_word(demon.stats.MP.start,demon.offsetNumbers['HP'] + 4 * 1)
            buffer.write_word(demon.stats.str.start,demon.offsetNumbers['HP'] + 4 * 4)
            buffer.write_word(demon.stats.vit.start,demon.offsetNumbers['HP'] + 4 * 5)
            buffer.write_word(demon.stats.mag.start,demon.offsetNumbers['HP'] + 4 * 6)
            buffer.write_word(demon.stats.agi.start,demon.offsetNumbers['HP'] + 4 * 7)
            buffer.write_word(demon.stats.luk.start,demon.offsetNumbers['HP'] + 4 * 8)
            #Write the id of the demons skills to the buffer
            for index, skill in enumerate(demon.skills):
                buffer.write_word(skill.ind, demon.offsetNumbers['firstSkill'] + 4 * index)
            #Write the id and levels of the demons learnable skills to the buffer
            for index, skill in enumerate(demon.learnedSkills):
                buffer.write_word(skill.ind, demon.offsetNumbers['firstLearnedLevel'] + 8 * index + 4)
                buffer.write_word(skill.level, demon.offsetNumbers['firstLearnedLevel'] + 8 * index)
            #Write various attributes of the demon to the buffer
            buffer.write_word(demon.level.value, demon.offsetNumbers['level'])
            buffer.write_halfword(demon.fusability, demon.offsetNumbers['fusability'])
            buffer.write_byte(demon.unlockFlags[0], demon.offsetNumbers['unlockFlags'])
            buffer.write_byte(demon.unlockFlags[1], demon.offsetNumbers['unlockFlags'] +1)
            buffer.write_byte(demon.tone.value, demon.offsetNumbers['tone'])
            buffer.write_byte(demon.tone.secondary, demon.offsetNumbers['tone'] + 1)
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
            buffer.write_word(fusion.firstDemon.value, fusion.offsetNumbers['firstDemon'])
            buffer.write_word(fusion.secondDemon.value, fusion.offsetNumbers['secondDemon'])
            buffer.write_word(fusion.result.value, fusion.offsetNumbers['result'])
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
            buffer.write_halfword(fusion.demon1.value, fusion.baseOffset + 2)
            buffer.write_halfword(fusion.demon2.value, fusion.baseOffset + 4)
            buffer.write_halfword(fusion.demon3.value, fusion.baseOffset + 6)
            buffer.write_halfword(fusion.demon4.value, fusion.baseOffset + 8)
            buffer.write_halfword(fusion.result.value, fusion.baseOffset + 10)
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
            buffer.write_word(foe.stats.HP, offsets['HP'] + 4 * 0)
            buffer.write_word(foe.stats.MP,offsets['HP'] + 4 * 1)
            buffer.write_word(foe.stats.str,offsets['HP'] + 4 * 2)
            buffer.write_word(foe.stats.vit,offsets['HP'] + 4 * 3)
            buffer.write_word(foe.stats.mag,offsets['HP'] + 4 * 4)
            buffer.write_word(foe.stats.agi,offsets['HP'] + 4 * 5)
            buffer.write_word(foe.stats.luk,offsets['HP'] + 4 * 6)

            buffer.write_word(foe.level, offsets['level'])
            buffer.write_byte(foe.pressTurns, offsets['pressTurns'])
            for index, skill in enumerate(foe.skills):
                buffer.write_word(skill.ind, offsets['firstSkill'] + 4 * index)
            buffer.write_word(foe.experience, offsets['experience'])
            buffer.write_word(foe.money, offsets['experience'] + 4)
            buffer.write_word(foe.AI, offsets['experience'] + 12)
            buffer.write_byte(foe.recruitable, offsets['HP'] + 33)
            buffer.write_byte(foe.levelDMGCorrection, offsets['HP'] + 30)
        return buffer
    
    '''
    Write the values in symbolArr to the respective locations in the buffer
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
            buffer.write_halfword(symbolEntry.symbol.ind, offsets['symbol'])
            #go through its list of encounter battles
            for encounterEntry in symbolEntry.encounters:
                enc = encounterEntry.encounter
                encOffsets = enc.offsetNumbers
                #and write the data for every demon
                for index, demon in enumerate(enc.demons):
                    buffer.write_halfword(demon, encOffsets['demon'] + 2 * index)
        return buffer
    
    '''
   Writes the values from the naho object to their respective locations in the table buffer
        Parameters:        
            buffer (Table)
            naho (Nahobino) 
    '''
    def updateMCBuffer(self, buffer, naho):
        offsets = naho.offsetNumbers
        #buffer.write_word(naho.startingSkill,offsets['startingSkill'])
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

        #Remove old Lilith as valid result
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
                            fusion.result.value = 155 #Flaemis id
                            fusion.result.translation = comp[155].name
                        case "Megami" | "Vile" | "Avatar" | "Genma" | "Wilder" | "Femme" | "Brute" | "Haunt":
                            fusion.result.value = 156 #Aquans id
                            fusion.result.translation = comp[156].name
                        case "Avian" | "Divine" | "Yoma" | "Raptor" | "Holy" | "Fairy" | "Fury" | "Dragon":
                            fusion.result.value = 157 #Aeros id
                            fusion.result.translation = comp[157].name
                        case _:
                            fusion.result.value = 158 #Erthrys id
                            fusion.result.translation = comp[158].name
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
                    match demon1.name:
                        case 'Erthys':
                            direction = erthys[demon2Race]
                        case 'Aeros':
                            direction = aeros[demon2Race]
                        case 'Aquans':
                            direction = aquans[demon2Race]
                        case 'Flaemis':
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
                    match demon2.name:
                        case 'Erthys':
                            direction = erthys[demon1Race]
                        case 'Aeros':
                            direction = aeros[demon1Race]
                        case 'Aquans':
                            direction = aquans[demon1Race]
                        case 'Flaemis':
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

    def adjustSpecialFusionTable(self,fusions, comp):
        pass
    
    '''
    Randomize the tone of each playable demon that does not have a tone with talk data assigned.
        Parameters:
            comp (Array) Array containing data on all playable demons
    '''
    def assignTalkableTones(self, comp):
        workingTones = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 22]
        for demon in comp:
            if demon.tone.value not in workingTones:
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
        foes = []
        for index, enemy in enumerate(enemies):
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
                newSkills.append(Translated_Value(newID, translation.translateSkillID(newID, self.skillNames)))
        
            newPressTurns = math.ceil(random.random() + (0.10 * enemy.pressTurns))
            newExperience = self.expMod[enemy.level]
            newMacca = self.maccaMod[enemy.level]
            #In original data enemies with two press turns like Oni have multiplied EXP and Macca values
            if newPressTurns > 1:
                newExperience = newExperience * newPressTurns
                newMacca = newMacca * math.floor(newPressTurns * 1.5)
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
            newFoe.experience = newExperience
            newFoe.money = newMacca
            newFoe.skills = newSkills
            newFoe.drops = enemy.drops
            newFoe.innate = playableEqu.innate   #copy innate from player version
            newFoe.resist = enemy.resist
            newFoe.potential = enemy.potential
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

        #will be in form [OG ID, NEW ID]
        replacements = []
        #Excluding unused, Old Lilith (id=71), Tao , Yoko, Mitama
        foes = list(filter(lambda e: e.ind != 71 and 'Mitama' not in e.name and not e.name.startswith('NOT USED') and e.ind != 364 and e.ind != 365 and e.ind != 366, enemyArr))
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
            Paramters:
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
            if encount.symbol.ind == 71 or encount.symbol.ind == 365 or encount.symbol.ind == 364 or encount.symbol.ind == 366 or encount.symbol.ind == 0 or encount.symbol.ind > 395 or "Mitama" in encount.symbol.translation or encount.symbol.translation.startswith("NOT USED"):
                newSymbolArr.append(encount)
                continue
            replaceEnc = encount
            symbolFoe = None
            currentLV = getFoeWithID(encount.symbol.ind, foes).originalLevel
            #get enemies at level which have not been featured as a replacement
            #ensures 1:1 replacement
            poss2 = getEnemiesAtLevel(currentLV)
            possibilities = [p for p in getEnemiesAtLevel(currentLV) if not any(r[1] == p.ind for r in replacements)]
            '''
            Should not be needed with 1:1 replacements
            leeway = 1
            while not possibilities: #If no demons available try again at a different level
                possibilities = getEnemiesAtLevel(currentLV + random.randint(leeway * -1, leeway))
                leeway += 1
            '''
            #check if replacement for symbol already exists
            if not any(r[0] == encount.symbol.ind for r in replacements):#!replacements.some(r => r[0] == encount.symbol.ind)) {
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

        self.adjustBasicEnemyStats(replacements, enemyArr)
        return newSymbolArr
    
    '''
    Adjust the stats of the enemies based on which enemy they replace as a symbol encounter
        Parameters:
            replacements (Array): Contains pairs of replacements [OGID, NEWID]
            foes (Array): List of basic enemies
    '''
    def adjustBasicEnemyStats(self, replacements, foes):
        for pair in replacements:
            replaced = foes[pair[0]]
            replacement = foes[pair[1]]

            statMods = replaced.statMods
            newStats = Stats(math.floor(replacement.stats.HP * statMods.HP), math.floor(replacement.stats.MP * statMods.MP), math.floor(replacement.stats.str * statMods.str),
                math.floor(replacement.stats.vit * statMods.vit), math.floor(replacement.stats.mag * statMods.mag),
                math.floor(replacement.stats.agi * statMods.agi), math.floor(replacement.stats.luk * statMods.luk))
            
            replacement.stats = newStats

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
        badIDs = [71, 365, 364, 366]
        for demon in comp:
            if not demon.name.startswith('NOT') and demon.ind not in badIDs and 'Mitama' not in demon.name:
                slots[demon.level.original] = slots[demon.level.original] + 1
        return slots
    
    '''
    Shuffles the levels of all playable demons and does adjustments to data based on that shuffling.
        Parameters:
            comp (Array(Compendium_Demon)): The array of playable demons
        Returns:
            The array of playable demons with shuffled levels
    '''
    def shuffleLevel(self, comp):
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

        #ids that should not be included in shuffling levels: Old Lilith, Yoko, Tao
        badIDs = [71, 365, 364, 366]

        #For each race build up new array with empty subarrays
        raceLevels = [ [] for _ in range(len(RACE_ARRAY)) ]

        #Valid demons are all demons whose level can be unconditionally randomized
        validDemons = list(filter(lambda demon: demon.unlockFlags[0] <= 0 and demon.race.translation != 'Element' and not demon.name.startswith('NOT') and demon.ind not in badIDs and 'Mitama' not in demon.name, comp))
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

        #For all flagged demons...
        for e in flaggedDemons:
            validLevel = False
            somethingWrong = False 
            attempts = 100 #Band-aid fix to stop infinite loop
            #assign new level based on highest free level as max and the minimum level unlock level based on flag
            while not validLevel:
                if getHighestFreeLevel() < e.minUnlock or somethingWrong:
                    newLevel = self.getRandomLevel(slots, getHighestFreeLevel(), getLowestFreeLevel()) #Something went wrong, no levels are free above minUnlock
                else:
                    newLevel = self.getRandomLevel(slots, getHighestFreeLevel(), e.minUnlock)
                if slots[newLevel] > 0 and newLevel not in raceLevels[RACE_ARRAY.index(e.race.translation)]:
                    #make sure slot is available and no demon of the same race has the same level
                    validLevel = True
                attempts -= 1
                if attempts < 0:
                    somethingWrong = True
            slots[newLevel] = slots[newLevel] - 1
            comp[e.ind].level.value = newLevel
            raceLevels[RACE_ARRAY.index(e.race.translation)].append(newLevel)

        for index, e in enumerate(validDemons):
            validLevel = False
            attempts = 100 #Band-aid fix to stop infinite loop
            while not validLevel:
                newLevel = self.getRandomLevel(slots, getHighestFreeLevel(), getLowestFreeLevel())
                if slots[newLevel] > 0 and newLevel not in raceLevels[RACE_ARRAY.index(e.race.translation)]:
                    #make sure slot is available and no demon of the same race has the same level
                    validLevel = True
                else:
                    attempts -= 1
                    if attempts <= 0:
                        validLevel = True
            slots[newLevel] = slots[newLevel] - 1
            comp[e.ind].level.value = newLevel
            raceLevels[RACE_ARRAY.index(e.race.translation)].append(newLevel)
        #print(slots)
        self.adjustLearnedSkillLevels(comp)
        comp = self.adjustStatsToLevel(comp)
        return comp
    
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
    Function that assembles an array containing arrays with each special fusions resulting demon id and their level.
        Returns:
            An array containing arrays with each special fusions resulting demon id and their level.
    '''
    def getMinLevelPerSpecialFusion(self):
        return list(map(lambda fusion: [fusion.resultLevel, fusion.result.value], self.specialFusionArr))

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
                            race2 = currentRaces[index];
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
                print(recruits)
                
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
        Executes the full randomization process including level randomization.
    '''
    def fullRando(self):
        compendiumBuffer = self.readNKMBaseTable()
        skillBuffer = self.readSkillData()
        normalFusionBuffer = self.readNormalFusionTables()
        otherFusionBuffer = self.readOtherFusionTables()
        encountBuffer = self.readEncounterData()
        playGrowBuffer = self.readMCData()
        self.readDemonNames()
        self.readSkillNames()
        self.fillCompendiumArr(compendiumBuffer)
        self.fillSkillArrs(skillBuffer)
        self.fillNormalFusionArr(normalFusionBuffer)
        self.fillFusionChart(otherFusionBuffer)
        self.fillSpecialFusionArr(otherFusionBuffer)
        self.fillBasicEnemyArr(compendiumBuffer)
        self.fillEncountArr(encountBuffer)
        self.fillEncountSymbolArr(encountBuffer)
        self.fillNahobino(playGrowBuffer)

        #print(encountSymbolArr[56].encounters)
        skillLevels = self.generateSkillLevelList()
        #print(skillLevels)
        levelSkillList = self.generateLevelSkillList(skillLevels)
        #print(obtainSkillFromID(928))
        #print(skillArr[400].name)
        #print(skillArr[401].name)
        #print(skillArr.find(e=> e.id == 1))
        #print(specialFusionArr[-1])
        #newComp = self.assignCompletelyRandomLevels(compendiumArr)
        newComp = self.shuffleLevel(self.compendiumArr)
        newComp = self.assignRandomPotentialWeightedSkills(self.compendiumArr, levelSkillList)
        newBasicEnemyArr = self.adjustBasicEnemyArr(self.enemyArr, newComp)
        newSymbolArr = self.adjustEncountersToSameLevel(self.encountSymbolArr, newComp, newBasicEnemyArr)

        self.adjustFusionTableToLevels(self.normalFusionArr, self.compendiumArr)
        #print(levelSkillList)
        #print(levelSkillList[1])
        #print(skillLevels[100])
        #newComp = assignCompletelyRandomSkills(compendiumArr,levelSkillList)
        #newComp = assignCompletelyRandomWeightedSkills(compendiumArr, levelSkillList)
        self.assignTalkableTones(newComp)
        #print(skillLevels[1])
        #print(compendiumArr[155].name)
        #print(compendiumArr[155].race)
        #print(logDemonByName("Isis",compendiumArr))
        #print(len(compendiumArr))
        compendiumBuffer = self.updateBasicEnemyBuffer(compendiumBuffer, newBasicEnemyArr)
        #compendiumBuffer = updateCompendiumBuffer(compendiumBuffer, compendiumArr)
        compendiumBuffer = self.updateCompendiumBuffer(compendiumBuffer, newComp)
        #compendiumBuffer.writeInt32LE(5,0x1B369)
        #print(len(RACE_ARRAY))
        otherFusionBuffer = self.updateOtherFusionBuffer(otherFusionBuffer, self.specialFusionArr)
        #print(normalFusionArr[-19])
        normalFusionBuffer = self.updateNormalFusionBuffer(normalFusionBuffer, self.normalFusionArr)
        #print(RACE_ARRAY[6])
        #print(RACE_ARRAY[23])
        #print(RACE_ARRAY[31])
        encountBuffer = self.updateEncounterBuffer(encountBuffer, newSymbolArr)
        playGrowBuffer = self.updateMCBuffer(playGrowBuffer, self.nahobino)
        #self.logDemonByName("Preta",compendiumArr)
        #print("END RESULT")
        #print(newComp[115])
        #print(newComp[116].skills)
        #print(newComp[116].learnedSkills)
        #print(obtainSkillFromID(113))
        #compendiumBuffer.writeInt32LE(472,28201)
        #checkRaceDoubleLevel(compendiumArr)
        #RACE_ARRAY.sort()
        #print(enemyArr[299])

        #self.printOutEncounters(newSymbolArr)


        self.writeNormalFusionTable(normalFusionBuffer.buffer)
        self.writeNKMBaseTable(compendiumBuffer.buffer)
        self.writeOtherFusionTable(otherFusionBuffer.buffer)
        self.writeEncounterData(encountBuffer.buffer)
        self.writeMCData(playGrowBuffer.buffer)
        #findUnlearnableSkills(skillLevels)
        #defineLevelSlots(newComp)
        #determineFusability()

    '''
        Executes the randomization process excluding level randomization.
    '''
    def noLevelRando(self):
        compendiumBuffer = self.readNKMBaseTable()
        skillBuffer = self.readSkillData()
        normalFusionBuffer = self.readNormalFusionTables()
        otherFusionBuffer = self.readOtherFusionTables()
        encountBuffer = self.readEncounterData()
        playGrowBuffer = self.readMCData()
        self.readDemonNames()
        self.readSkillNames()
        self.fillCompendiumArr(compendiumBuffer)
        self.fillSkillArrs(skillBuffer)
        self.fillNormalFusionArr(normalFusionBuffer)
        self.fillFusionChart(otherFusionBuffer)
        self.fillSpecialFusionArr(otherFusionBuffer)
        self.fillBasicEnemyArr(compendiumBuffer)
        self.fillEncountArr(encountBuffer)
        self.fillEncountSymbolArr(encountBuffer)
        self.fillNahobino(playGrowBuffer)
        skillLevels = self.generateSkillLevelList()
        levelSkillList = self.generateLevelSkillList(skillLevels)
        newComp = self.assignRandomPotentialWeightedSkills(self.compendiumArr, levelSkillList)

        newBasicEnemyArr = self.adjustBasicEnemyArr(self.enemyArr, newComp)
        newSymbolArr = self.adjustEncountersToSameLevel(self.encountSymbolArr, newComp, newBasicEnemyArr)
        self.adjustFusionTableToLevels(self.normalFusionArr, self.compendiumArr)
        self.assignTalkableTones(newComp)

        compendiumBuffer = self.updateBasicEnemyBuffer(compendiumBuffer, newBasicEnemyArr)
        compendiumBuffer = self.updateCompendiumBuffer(compendiumBuffer, newComp)
        otherFusionBuffer = self.updateOtherFusionBuffer(otherFusionBuffer, self.specialFusionArr)
        normalFusionBuffer = self.updateNormalFusionBuffer(normalFusionBuffer, self.normalFusionArr)
        encountBuffer = self.updateEncounterBuffer(encountBuffer, newSymbolArr)
        playGrowBuffer = self.updateMCBuffer(playGrowBuffer, self.nahobino)

        self.findEncounterBattle(1011,newSymbolArr)

        self.writeNormalFusionTable(normalFusionBuffer.buffer)
        self.writeNKMBaseTable(compendiumBuffer.buffer)
        self.writeOtherFusionTable(otherFusionBuffer.buffer)
        self.writeEncounterData(encountBuffer.buffer)
        self.writeMCData(playGrowBuffer.buffer)
        
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
        with open(paths.ENCOUNTERS_DEBUG, 'w') as file:
            file.write(finalString)
            
    def findEncounterBattle(self, id2, symbolEncs):
        for symbol in symbolEncs:
            for ec in symbol.encounters:
                if(ec.encounter.ind == id2):
                    print(symbol)
                    
if __name__ == '__main__':
    rando = Randomizer()
    print('Level randomization is currently not fully implemented. \n Type y to randomize levels and n to not randomized levels. \n')
    answer = input()
    if(answer == 'y'):
        rando.fullRando()
    elif(answer == 'n'):
        rando.noLevelRando()
    else:
        print('Invalid')
    input('Press [Enter] to exit')