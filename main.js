import { read } from 'fs';
import * as fs from 'fs/promises';

const raceArray = ["None", "Unused", "Herald", "Megami", "Avian", "Divine", "Yoma", "Vile", "Raptor", "Unused9", "Deity", "Wargod", "Avatar", "Holy", "Genma", "Element", "Mitama", "Fairy", "Beast", "Jirae", "Fiend", "Jaki", "Wilder", "Fury", "Lady", "Dragon", "Kishin", "Kunitsu", "Femme", "Brute", "Fallen", "Night", "Snake", "Tyrant", "Drake", "Haunt", "Foul", "Chaos", "Devil", "Meta", "Nahobino", "Proto-fiend", "Matter", "Panagia", "Enigma", "UMA", "Qadistu", "Human", "Primal", "Void"]

var compendiumNames = []
var skillNames = []

var compendiumArr = []
var skillArr = []
var passiveSkillArr = []
var innateSkillArr = []
var normalFusionArr = []
var fusionChartArr = []
var specialFusionArr = []
var enemyArr = []

/**
 * Reads the file that contains the Demon Table.
 * @returns the bytes of the Demon Table file as a buffer
 */
async function readNKMBaseTable() {
    var fileContents = (await fs.readFile('./base/NKMBaseTable.uexp'))

    return fileContents
}

/**
 * Reads the file that contains the Skill Table.
 * @returns the bytes of the Skill Table file as a buffer
 */
async function readSkillData() {
    var fileContents = (await fs.readFile('./base/SkillData.uexp'))

    return fileContents
}

/**
 * Reads the file that contains the fusion recipes table.
 * @returns the buffer containing the fusion recipe table
 */
async function readNormalFusionTables() {
    var fileContents = (await fs.readFile('./base/UniteCombineTable.uexp'))

    return fileContents
}

/**
* Reads the file that contains the Special Fusion Table and the Fusion Chart Table.
* @returns the buffer containing the Special Fusion Table and the Fusion Chart Table
*/
async function readOtherFusionTables() {
    var fileContents = (await fs.readFile('./base/UniteTable.uexp'))

    return fileContents
}

/**
 * Reads the text file containing Character Naems and filters out jst the names and saves all names in array
 * compendiumNames.
 * @returns the buffer containing CharacterNames
 */
async function readDemonNames() {
    var fileContents = (await fs.readFile('./CharacterName.uasset.txt')).toString()
    let tempArray = fileContents.split("MessageLabel=")
    for (let index = 1; index < tempArray.length; index++) {
        let sliceStart = tempArray[index].search("MessageTextPages_3=")
        let sliceEnd = tempArray[index].search("Voice=")
        compendiumNames.push(tempArray[index].slice(sliceStart + 19, sliceEnd - 9))
    }
    return fileContents
}

/**
 * Reads the text file containing Skill Names and filters out just the names and saves all names in array
 * skillNames.
 * @returns the buffer containing SkillNames
 */
async function readSkillNames() {
    var fileContents = (await fs.readFile('./SkillName.uasset.txt')).toString()
    let tempArray = fileContents.split("MessageLabel=")
    for (let index = 0; index < tempArray.length; index++) {
        let sliceStart = tempArray[index].search("MessageTextPages_3=")
        let sliceEnd = tempArray[index].search("Voice=")
        skillNames.push(tempArray[index].slice(sliceStart + 19, sliceEnd - 9))
    }
    return fileContents
}

/**
 * Writes the given Buffer to the file NKMBaseTable.uexp.
 * @param {Buffer} result 
 */
async function writeNKMBaseTable(result) {
    await fs.writeFile('./rando/Project/Content/Blueprints/Gamedata/BinTable/Devil/NKMBaseTable.uexp', result)
}

/**
 * Writes the given Buffer to the file SkillData.uexp.
 * @param {Buffer} result 
 */
async function writeSkillData(result) {
    await fs.writeFile('./rando/Project/Content/Blueprints/Gamedata/BinTable/Battle/Skill/SkillData.uexp', result)
}

/**
* Writes the given Buffer to the file UniteCombineTable.uexp.
* @param {Buffer} result
*/
async function writeNormalFusionTable(result) {
    await fs.writeFile('./rando/Project/Content/Blueprints/Gamedata/BinTable/Unite/UniteCombineTable.uexp', result)
}

/**
* Writes the given Buffer to the file UniteCombineTable.uexp.
* @param {Buffer} result
*/
async function writeOtherFusionTable(result) {
    await fs.writeFile('./rando/Project/Content/Blueprints/Gamedata/BinTable/Unite/UniteTable.uexp', result)
}

/**
 * Fills the array compendiumArr with data extracted from the Buffer NKMBaseTable.
 * The end array contains data on all demons which are registered in the compendium and usable by the player.
 * @param {Buffer} NKMBaseTable the buffer to get the demon data from
 */
function fillCompendiumArr(NKMBaseTable) {
    function readInt32LE(ofSet) {
        return NKMBaseTable.readInt32LE(ofSet)
    }

    let startValue = 0x69
    // let startValue = 0x1B369 Starting value for Abdiel testing
    let raceOffset = 0x0C
    let demonOffset = 0x1D0


    //For all demons in the compendium...
    for (let index = 0; index < 395; index++) {
        //First define all relevant offsets
        let offset = startValue + demonOffset * index
        let locations = {
            race: offset - raceOffset,
            level: offset,
            HP: offset + 0x1C,
            firstSkill: offset + 0x70,
            firstLearnedLevel: offset + 0xA0,
            fusability: offset + 0x56,
            unlockFlags: offset + 0x74,
            tone: offset + 0x6C,
            innate: offset + 0x100,
            potential: offset + 0X174
        }
        //Then read the list of initial skills learned
        let listOfSkills = []
        for (let index = 0; index < 8; index++) {
            let skillID = readInt32LE(locations.firstSkill + 4 * index)
            if (skillID != 0) {
                listOfSkills.push({ id: skillID, translation: translateSkillID(skillID) })
            }

        }
        //Read the list of learnable skills 
        let listOfLearnedSkills = []
        for (let index = 0; index < 8; index++) {
            // console.log(locations.firstLearnedLevel)
            let skillID = readInt32LE(locations.firstLearnedLevel + 8 * index + 4)
            if (skillID != 0) {
                listOfLearnedSkills.push({
                    id: skillID,
                    level: readInt32LE(locations.firstLearnedLevel + 8 * index),
                    translation: translateSkillID(skillID)
                })
            }

        }
        // Add read demon data to compendium
        compendiumArr.push({
            id: index,
            name: compendiumNames[index],
            offsetNumbers: locations,
            race: { value: NKMBaseTable.readUInt8(locations.race), translation: raceArray[NKMBaseTable.readUInt8(locations.race)] },
            oldlevel: readInt32LE(locations.level),
            level: { value: readInt32LE(locations.level) },
            registerable: readInt32LE(locations.HP - 4),
            fusability: NKMBaseTable.readInt16LE(locations.fusability), // 0101 means no, 0100 means accident only, 0000 means yes (providing recipe exists)
            unlockFlags: NKMBaseTable.readUInt8(locations.unlockFlags),
            tone: { value: NKMBaseTable.readUInt8(locations.tone), translation: "", additionalReadings: [NKMBaseTable.readUInt8(locations.tone) + 1, NKMBaseTable.readInt16LE(locations.tone)] },
            resist: {
                physical: { value: readInt32LE(locations.innate + 4), translation: translateResist(readInt32LE(locations.innate + 4)) },
                fire: { value: readInt32LE(locations.innate + 4 * 2), translation: translateResist(readInt32LE(locations.innate + 4 * 2)) },
                ice: { value: readInt32LE(locations.innate + 4 * 3), translation: translateResist(readInt32LE(locations.innate + 4 * 3)) },
                electric: { value: readInt32LE(locations.innate + 4 * 4), translation: translateResist(readInt32LE(locations.innate + 4 * 4)) },
                force: { value: readInt32LE(locations.innate + 4 * 5), translation: translateResist(readInt32LE(locations.innate + 4 * 5)) },
                light: { value: readInt32LE(locations.innate + 4 * 6), translation: translateResist(readInt32LE(locations.innate + 4 * 6)) },
                dark: { value: readInt32LE(locations.innate + 4 * 7), translation: translateResist(readInt32LE(locations.innate + 4 * 7)) },
                almighty: { value: readInt32LE(locations.innate + 4 * 8), translation: translateResist(readInt32LE(locations.innate + 4 * 8)) },
                poison: { value: readInt32LE(locations.innate + 4 * 9), translation: translateResist(readInt32LE(locations.innate + 4 * 9)) },
                confusion: { value: readInt32LE(locations.innate + 4 * 11), translation: translateResist(readInt32LE(locations.innate + 4 * 11)) },
                charm: { value: readInt32LE(locations.innate + 4 * 12), translation: translateResist(readInt32LE(locations.innate + 4 * 12)) },
                sleep: { value: readInt32LE(locations.innate + 4 * 13), translation: translateResist(readInt32LE(locations.innate + 4 * 13)) },
                seal: { value: readInt32LE(locations.innate + 4 * 14), translation: translateResist(readInt32LE(locations.innate + 4 * 14)) },
                mirage: { value: readInt32LE(locations.innate + 4 * 21), translation: translateResist(readInt32LE(locations.innate + 4 * 21)) }
            },
            potential: {
                physical: readInt32LE(locations.potential),
                fire: readInt32LE(locations.potential + 4 * 1),
                ice: readInt32LE(locations.potential + 4 * 2),
                elec: readInt32LE(locations.potential + 4 * 3),
                force: readInt32LE(locations.potential + 4 * 4),
                light: readInt32LE(locations.potential + 4 * 5),
                dark: readInt32LE(locations.potential + 4 * 6),
                almighty: readInt32LE(locations.potential + 4 * 7),
                ailment: readInt32LE(locations.potential + 4 * 8),
                recover: readInt32LE(locations.potential + 4 * 9),
                support: readInt32LE(locations.potential + 4 * 10)
            },
            stats: {
                HP: { start: readInt32LE(locations.HP + 4 * 0), growth: readInt32LE(locations.HP + 4 * 2) },
                MP: { start: readInt32LE(locations.HP + 4 * 1), growth: readInt32LE(locations.HP + 4 * 3) },
                str: { start: readInt32LE(locations.HP + 4 * 4), growth: readInt32LE(locations.HP + 4 * 9) },
                vit: { start: readInt32LE(locations.HP + 4 * 5), growth: readInt32LE(locations.HP + 4 * 10) },
                mag: { start: readInt32LE(locations.HP + 4 * 6), growth: readInt32LE(locations.HP + 4 * 11) },
                agi: { start: readInt32LE(locations.HP + 4 * 7), growth: readInt32LE(locations.HP + 4 * 12) },
                luk: { start: readInt32LE(locations.HP + 4 * 8), growth: readInt32LE(locations.HP + 4 * 13) },
            },
            innate: { id: readInt32LE(locations.innate), translation: translateSkillID(readInt32LE(locations.innate)) },
            skills: listOfSkills,
            learnedSkills: listOfLearnedSkills
        })

    }
}

/**
 * Fills the arrays skillArr, passiveSkillArr and innateSkillArr with data extracted from the Buffer skillData.
 * The end arrays contain data on all skills of their respective type.
 * @param {Buffer} skillData the buffer to get the skill data from
 */
function fillSkillArrs(skillData) {
    /**
    * Reads the next 4 bytes as a little endian Interger at the location ofSet of the Buffer skillData.
    * @param {Number} ofSet the location at which to start reading.
    * @return the read Integer
    */
    function read4(ofSet) {
        return skillData.readInt32LE(ofSet)
    }
    /**
    * Reads the next byte as an unsigned Interger at the location ofSet of the Buffer skillData.
    * @param {Number} ofSet the location at which to start reading.
    * @return the read Integer
    */
    function read1(ofSet) {
        return skillData.readUInt8(ofSet)
    }
    /**
    * Reads the next 2 bytes as a little endian Interger at the location ofSet of the Buffer skillData.
    * @param {Number} ofSet the location at which to start reading.
    * @return the read Integer
    */
    function read2(ofSet) {
        return skillData.readInt16LE(ofSet)
    }

    // Define start locations for batches of skills and how much data each skill has
    let startValue = 0x85
    let passiveStartValue = 0x132E5
    let skillOffset = 0xC4
    let passiveOffset = 0x6C
    let secondBatchStart = 0x1E305

    //Because the skill table starts with id=1, we need an filler object in the array to keep id & index consistent.
    let fillerObject = { id: 0, name: "Filler" }
    skillArr.push(fillerObject)

    //For every skill (there are 950 skills in Vanilla)...
    for (let index = 0; index < 950; index++) {
        //check if skill is in passive area 
        if (index >= 400 && index < 801) {
            let offset = passiveStartValue + passiveOffset * (index - 400)
            let locations = {
                hpIncrease: offset,
                survive: offset + 15,
                element: offset + 17,
                physResist: offset + 34,
                effect: offset + 52,
            }
            // check if innate
            var skillType2 = ""
            if (index >= 530) {
                skillType2 = "innate"
            } else {
                skillType2 = "passive"
            }
            //Create the object to push 
            let toPush = {
                id: index + 1,
                name: translateSkillID(index + 1),
                skillType: skillType2,
                offsetNumber: locations,
                hpIncrease: read1(locations.hpIncrease),
                mpIncrease: read1(locations.hpIncrease + 1),
                counterchance: read1(locations.hpIncrease + 3),
                survive: read1(locations.survive),
                element: { value: read1(locations.element), translation: translatePassiveElementType(read1(locations.element)) },
                resists: {
                    type: {
                        value: read1(locations.element + 1),
                        translation: translatePassiveResist(read1(locations.element + 1))
                    },
                    physical: read1(locations.physResist),
                    fire: read1(locations.physResist + 1),
                    ice: read1(locations.physResist + 2),
                    elec: read1(locations.physResist + 3),
                    force: read1(locations.physResist + 4),
                    dark: read1(locations.physResist + 5),
                    light: read1(locations.physResist + 6),
                },
                effect1: read2(locations.effect),
                effect1Amount: read2(locations.effect + 2),
                effect2: read2(locations.effect + 4),
                effect2Amount: read2(locations.effect + 6)
            }
            // If skill is in the innate area push to innateSkillArr else push to passiveSkillArr
            if (index >= 530) {
                innateSkillArr.push(toPush)
            } else {
                passiveSkillArr.push(toPush)
            }

        } else {
            // console.log(index)
            let offset = startValue + skillOffset * index
            //While the skillTable starts with id 1, I do not read the ID from the data (which I really should)
            let skillID = index + 1
            let skillName = translateSkillID(index + 1)

            //if skill is in the second batch of active skills, we calculate the offset a different way and index = id is working
            if (index >= 800) {
                skillName = translateSkillID(index)
                skillID = index
                offset = secondBatchStart + skillOffset * (index - 801)
            }
            let locations = {
                cost: offset + 8,
                skillType: offset + 10,
                element: offset + 12,
                icon: offset + 28,
                target: offset + 0x22,
                minHit: offset + 0x24,
                maxHit: offset + 0x25,
                critRate: offset + 0x26,
                power: offset + 0x28,
                hitRate: offset + 0x34,
                ailmentFlag: offset + 0x35,
                ailmentChance: offset + 0x48,
                healing: {
                    overMaxHP: offset + 0x45,
                    effect: offset + 0x49
                },
                pierce: offset + 0x46,
                buffstimer: offset + 75,
                resistEnable: offset + 0x60,
                hpDrain: offset + 109,
                magatsuhiFlag: offset + 115,
                modifier1: offset + 136,
                condition1: offset + 140
            }

            skillArr.push({
                id: skillID,
                name: skillName,
                offsetNumber: locations,
                cost: read2(locations.cost),
                rank: read1(locations.hpDrain + 3),
                skillType: {
                    value: read1(locations.skillType),
                    tranlsation: translateSkillType(read1(locations.skillType))
                },
                potentialType: {
                    value: read1(locations.icon + 1),
                    translation: translatePotentialType(read1(locations.icon + 1))
                },
                element: {
                    value: read1(locations.element),
                    translation: translateSkillElement(read1(locations.element))
                },
                skillIcon: read1(locations.icon),
                target: { value: read1(locations.target), translation: translateTarget(read1(locations.target)) },
                minHits: read1(locations.minHit),
                maxHits: read1(locations.maxHit),
                crit: read1(locations.critRate),
                power: read4(locations.power),
                hit: read1(locations.hitRate),
                ailmentFlags: {
                    instakill: read1(locations.ailmentFlag),
                    poison: read1(locations.ailmentFlag + 1),
                    confusion: read1(locations.ailmentFlag + 3),
                    charm: read1(locations.ailmentFlag + 4),
                    sleep: read1(locations.ailmentFlag + 5),
                    seal: read1(locations.ailmentFlag + 6),
                    mirage: read1(locations.ailmentFlag + 9),
                    mud: read1(locations.ailmentFlag + 14),
                    shroud: read1(locations.ailmentFlag + 15)
                },
                healing: {
                    overmaxHP: read1(locations.healing.overMaxHP),
                    effect: read1(locations.healing.effect),
                    flat: read4(locations.resistEnable + 8),
                    percent: read1(locations.resistEnable + 12)
                },
                pierce: read1(locations.pierce),
                ailmentChance: read1(locations.ailmentChance),
                buff: {
                    timer: read1(locations.buffstimer),
                    physical: read4(locations.buffstimer + 1),
                    magical: read4(locations.buffstimer + 5),
                    defense: read4(locations.buffstimer + 9),
                    accEva: read4(locations.buffstimer + 13),
                },
                resists: {
                    enable: read1(locations.resistEnable),
                    physical: {
                        value: read1(locations.resistEnable + 1),
                        translation: translatePassiveResist(read1(locations.resistEnable + 1))
                    },
                    fire: {
                        value: read1(locations.resistEnable + 2),
                        translation: translatePassiveResist(read1(locations.resistEnable + 2))
                    },
                    ice: {
                        value: read1(locations.resistEnable + 3),
                        translation: translatePassiveResist(read1(locations.resistEnable + 3))
                    },
                    elec: {
                        value: read1(locations.resistEnable + 4),
                        translation: translatePassiveResist(read1(locations.resistEnable + 4))
                    },
                    force: {
                        value: read1(locations.resistEnable + 5),
                        translation: translatePassiveResist(read1(locations.resistEnable + 5))
                    },
                    light: {
                        value: read1(locations.resistEnable + 6),
                        translation: translatePassiveResist(read1(locations.resistEnable + 6))
                    },
                    dark: {
                        value: read1(locations.resistEnable + 7),
                        translation: translatePassiveResist(read1(locations.resistEnable + 7))
                    },
                },
                hpDrain: read1(locations.hpDrain),
                mpDrain: read1(locations.hpDrain + 1),
                magatsuhi: {
                    enable: read1(locations.magatsuhiFlag),
                    race1: {
                        value: read1(locations.magatsuhiFlag + 1),
                        translation: raceArray[read1(locations.magatsuhiFlag + 1)]
                    },
                    race2: {
                        value: read1(locations.magatsuhiFlag + 3),
                        translation: raceArray[read1(locations.magatsuhiFlag + 3)]
                    }
                },
                modifiers: {
                    modifier1: {
                        value: read1(locations.modifier1),
                        translation: translateModifier(read1(locations.modifier1))
                    },
                    modifier2: {
                        value: read1(locations.modifier1 + 1),
                        translation: translateModifier(read1(locations.modifier1 + 1))
                    },
                    modifier3: {
                        value: read1(locations.modifier1 + 2),
                        translation: translateModifier(read1(locations.modifier1 + 2))
                    },
                    modifier4: {
                        value: read1(locations.modifier1 + 3),
                        translation: translateModifier(read1(locations.modifier1 + 3))
                    }
                },
                conditions: {
                    condition1: {
                        value: read1(locations.condition1),
                        ailmentCondition: read1(locations.condition1 + 1),
                        effect: read2(locations.condition1 + 2),
                        amount: read2(locations.condition1 + 4)
                    },
                    condition2: {
                        value: read1(locations.condition1 + 8),
                        ailmentCondition: read1(locations.condition1 + 9),
                        effect: read2(locations.condition1 + 11),
                        amount: read2(locations.condition1 + 13)
                    }
                }

            })
        }

    }

}

/**
 * Fills the array normalFusionArr with data extracted from the Buffer fusionData.
 * The end array contains data on all normal fusions between two registerable demons.
 * @param {Buffer} fusionData the buffer to get the fusion data from
 */
function fillNormalFusionArr(fusionData) {
    /**
    * Reads the next 4 bytes as a little endian Interger at the location ofSet of the Buffer fusionData.
    * @param {Number} ofSet the location at which to start reading.
    * @return the read Integer
    */
    function read4(ofSet) {
        return fusionData.readInt32LE(ofSet)
    }
    //Define Starting point and difference to next fsion
    let startValue = 0xC5
    let fusionOffset = 0x7C

    //For every fusion (37401 = ((n-1)*(n))/2 with n being the number of registerable demons)
    for (let index = 0; index < 37401; index++) {
        let offset = startValue + index * fusionOffset
        let locations = {
            firstDemon: offset,
            secondDemon: offset + 0x1D,
            result: offset + 0x57
        }
        normalFusionArr.push({
            offsetNumbers: locations,
            firstDemon: {
                value: read4(locations.firstDemon),
                translation: compendiumArr[read4(locations.firstDemon)].name
            },
            secondDemon: {
                value: read4(locations.secondDemon),
                translation: compendiumArr[read4(locations.secondDemon)].name
            },
            result: {
                value: read4(locations.result),
                translation: compendiumArr[read4(locations.result)].name
            }
        })
    }
}

/**
 * Fills the array fusionChartArray with data extracted from the Buffer fusionData.
 * The end array contains data on what the normal result of a fusion between two races should be.
 * @param {Buffer} fusionData the buffer to get the fusion chart data from
 */
function fillFusionChart(fusionData) {
    /**
    * Reads the next byte as an unsigned Interger at the location ofSet of the Buffer fusionData.
    * @param {Number} ofSet the location at which to start reading.
    * @return the read Integer
    */
    function read1(ofSet) {
        return fusionData.readUInt8(ofSet)
    }

    let startValue = 0x95

    for (let index = 0; index < 609; index++) {
        let offset = startValue + index * 4
        fusionChartArr.push({
            offset: offset,
            race1: {
                value: read1(offset),
                translation: raceArray[read1(offset)]
            },
            race2: {
                value: read1(offset + 1),
                translation: raceArray[read1(offset + 1)]
            },
            result: {
                value: read1(offset + 2),
                translation: raceArray[read1(offset + 2)]
            },

        })
    }
}

/**
 * Fills the array fusionChartArray with data extracted from the Buffer fusionData.
 * The end array contains data on the results and ingredients of all special fusions
 * @param {Buffer} fusionData the buffer to get the special fusion data from
 */
function fillSpecialFusionArr(fusionData) {
    /**
    * Reads the next byte as an unsigned Interger at the location ofSet of the Buffer skillData.
    * @param {Number} ofSet the location at which to start reading.
    * @return the read Integer
    */
    function read1(ofSet) {
        return fusionData.readUInt8(ofSet)
    }
    /**
    * Reads the next 4 bytes as a little endian Interger at the location ofSet of the Buffer fusionData.
    * @param {Number} ofSet the location at which to start reading. 
    * @return the read Integer
    */
    function read4(ofSet) {
        return fusionData.readInt32LE(ofSet)
    }
    /**
    * Reads the next 2 bytes as a little endian Interger at the location ofSet of the Buffer fusionData.
    * @param {Number} ofSet the location at which to start reading. 
    * @return the read Integer
    */
    function read2(ofSet) {
        return fusionData.readInt16LE(ofSet)
    }

    let startValue = 0xCC5
    let fusionOffset = 0xC

    for (let index = 0; index < 62; index++) {
        let offset = startValue + index * fusionOffset

        specialFusionArr.push({
            id: read2(offset),
            baseOffset: offset,
            demon1: {
                value: read2(offset + 2),
                translation: compendiumArr[read2(offset + 2)].name
            },
            demon2: {
                value: read2(offset + 4),
                translation: compendiumArr[read2(offset + 4)].name
            },
            demon3: {
                value: read2(offset + 6),
                translation: compendiumArr[read2(offset + 6)].name
            },
            demon4: {
                value: read2(offset + 8),
                translation: compendiumArr[read2(offset + 8)].name
            },
            result: {
                value: read2(offset + 10),
                translation: compendiumArr[read2(offset + 10)].name
            },
        })
    }
}

/**
 * 
 * @param {Buffer} enemyData 
 */
function fillBasicEnemyArr(enemyData) {
    function read4(ofSet) {
        return enemyData.readInt32LE(ofSet)
    }
    function read1(ofSet) {
        return enemyData.readUInt8(ofSet)
    }

    let startValue = 0x88139
    let enemyOffset = 0x170

    //For all Enemy version of demons in the compendium
    for (let index = 0; index < 395; index++) {
        //First define all relevant offsets
        let offset = startValue + enemyOffset * index
        let locations = {
            level: offset,
            HP: offset + 4,
            pressTurns: offset + 0x2B,
            experience: offset + 0x44,
            item: offset + 0x64,
            firstSkill: offset + 0x88,
            innate: offset + 0xB8,
            resist: offset + 0xBB,
            potential: offset + 0x12C
        }

        let listOfSkills = []
        for (let index = 0; index < 8; index++) {
            let skillID = read4(locations.firstSkill + 4*index)
            if (skillID != 0) {
                listOfSkills.push({ id: skillID, translation: translateSkillID(skillID) })
            }

        }

        

        enemyArr.push({
            id: index,
            name: compendiumNames[index],
            offsetNumbers: locations,
            level: read4(locations.level),
            stats: {
                HP: read4(locations.HP),
                MP: read4(locations.HP + 4),
                str: read4(locations.HP + 8),
                vit: read4(locations.HP + 12),
                mag: read4(locations.HP + 16),
                agi: read4(locations.HP + 20),
                luk: read4(locations.HP + 24),
            },
            analyze: read1(locations.HP + 28),
            levelDMGcorrection: read1(locations.HP + 30),
            AI: read4(locations.experience + 12), //55 for normal encounters
            recruitable: read1(locations.HP + 33),
            pressTurns: read1(locations.pressTurns),
            experience: read4(locations.experience),
            money: read4(locations.experience + 4),
            skills: listOfSkills,
            drops: {
                item1: {
                    value: read4(locations.item),
                    translation: translateItem(read4(locations.item)),
                    chance: read4(locations.item + 4),
                    quest: read4(locations.item + 8),
                },
                item3: {
                    value: read4(locations.item + 12),
                    translation: translateItem(read4(locations.item + 12)),
                    chance: read4(locations.item + 16),
                    quest: read4(locations.item + 20),
                },
                item2: {
                    value: read4(locations.item + 24),
                    translation: translateItem(read4(locations.item + 24)),
                    chance: read4(locations.item + 28),
                    quest: read4(locations.item + 32),
                },
            },
            innate: {
                value: read4(locations.innate),
                translation: obtainSkillFromID(read4(locations.innate)).name
            },
            resist: {
                physical: { value: read4(locations.innate + 4), translation: translateResist(read4(locations.innate + 4)) },
                fire: { value: read4(locations.innate + 4 * 2), translation: translateResist(read4(locations.innate + 4 * 2)) },
                ice: { value: read4(locations.innate + 4 * 3), translation: translateResist(read4(locations.innate + 4 * 3)) },
                electric: { value: read4(locations.innate + 4 * 4), translation: translateResist(read4(locations.innate + 4 * 4)) },
                force: { value: read4(locations.innate + 4 * 5), translation: translateResist(read4(locations.innate + 4 * 5)) },
                light: { value: read4(locations.innate + 4 * 6), translation: translateResist(read4(locations.innate + 4 * 6)) },
                dark: { value: read4(locations.innate + 4 * 7), translation: translateResist(read4(locations.innate + 4 * 7)) },
                almighty: { value: read4(locations.innate + 4 * 8), translation: translateResist(read4(locations.innate + 4 * 8)) },
                poison: { value: read4(locations.innate + 4 * 9), translation: translateResist(read4(locations.innate + 4 * 9)) },
                confusion: { value: read4(locations.innate + 4 * 11), translation: translateResist(read4(locations.innate + 4 * 11)) },
                charm: { value: read4(locations.innate + 4 * 12), translation: translateResist(read4(locations.innate + 4 * 12)) },
                sleep: { value: read4(locations.innate + 4 * 13), translation: translateResist(read4(locations.innate + 4 * 13)) },
                seal: { value: read4(locations.innate + 4 * 14), translation: translateResist(read4(locations.innate + 4 * 14)) },
                mirage: { value: read4(locations.innate + 4 * 21), translation: translateResist(read4(locations.innate + 4 * 21)) }
            },
            potential: {
                physical: read4(locations.potential),
                fire: read4(locations.potential + 4 * 1),
                ice: read4(locations.potential + 4 * 2),
                elec: read4(locations.potential + 4 * 3),
                force: read4(locations.potential + 4 * 4),
                light: read4(locations.potential + 4 * 5),
                dark: read4(locations.potential + 4 * 6),
                almighty: read4(locations.potential + 4 * 7),
                ailment: read4(locations.potential + 4 * 8),
                recover: read4(locations.potential + 4 * 9),
                support: read4(locations.potential + 4 * 10)
            }
        })
    }
}

/**
* Based on the skill id returns the object containing data about the skill from one of skillArr, passiveSkillArr or innateSkillArr.
* @param {Number} id the id of the skill to return
* @returns the skill object with the given id
*/
function obtainSkillFromID(id) {
    // let id = idO - 1
    // console.log(id)
    if (id <= 400) {
        return skillArr[id]
    } else if (id <= 530) {
        return passiveSkillArr[id - 401]
    } else if (id <= 800) {
        return innateSkillArr[id - 531]
    } else {
        return skillArr[id - 400]
    }
}

function translateItem(id) {
    return ""
}

/**
* Translates the given value of a skill modifier to its an understable description of its effect in game.
* //UNCOMPLETE
* @param {Number} value the value of the modifier
* @returns the description of the given modifier value
*/
function translateModifier(value) {
    let results = ["None", "Charge", "Concentrate"]
    if (value >= results.length) {
        return "Not Known Yet"
    } else {
        return results[value]
    }
}

/**
 * Gives the name of the skill that has the given id
 * @param {Number} id 
 * @returns the name of the skill of the given id
 */
function translateSkillID(id) {
    return skillNames[id]
}

/**
* Returns a text description of the given skill type value.
* @param {Number} value
* @returns the text description of the given skill type value.
*/
function translateSkillType(value) {
    let results = ["StrBased", "MagBased", "Ailment", "Heal", "Support", "", "RevivalChant", "", "", "", "", "", "", "LevelBased"]
    return results[value]
}

/**
* Returns a text description of the given skill element value.
* @param {Number} value
* @returns the text description of the given skill element value.
*/
function translateSkillElement(value) {
    let results = ["Physical", "Fire", "Ice", "Elec", "Force", "Light", "Dark", "Almighty", "", "", "", "", "Ailment", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "Heal"]
    return results[value]
}

/**
* Returns a text description of the given skill passive resist type value.
* @param {Number} value
* @returns the text description of the given given skill passive resist type value.
*/
function translatePassiveResist(value) {
    let results = ["None", "Resist", "Null", "Repel", "Drain"]
    return results[value]
}

/**
* Returns a text description of the given skill target value.
* @param {Number} value
* @returns the text description of the given skill target value.
*/
function translateTarget(value) {
    let results = ["SingleFoe", "AllFoe", "SingleAlly", "AllyAll", "Self", "Foe+AllyAll", "Random", "AllyAndStockSingle", "Ally+StockAll"]
    return results[value]
}

/**
* Returns a text description of the given skill potential type value.
* @param {Number} value
* @returns the text description of the given skill potential type value.
*/
function translatePotentialType(value) {
    let types = ["Phys", "Fire", "Ice", "Elec", "Force", "Light", "Dark", "Almighty", "Ailment", "Support", "Recover", "", "", "Magatsuhi"]
    return types[value]
}

/**
 * Translates the number into what type of resist it describes
 * @param {Number} value 
 * @returns the type of resist value describes
 */
function translateResist(value) {
    let result = ""
    switch (value) {
        case 0:
            result = "Null"
            break;
        case Number("0x0A"):
            result = "Resist Severe"
            break;
        case Number("0x14"):
            result = "Resist Heavy"
            break;
        case Number("0x28"):
            result = "Resist Medium"
            break;
        case Number("0x32"):
            result = "Resist"
            break;
        case Number("0x64"):
            result = "Normal"
            break;
        case Number("0x7D"):
            result = "Weak"
            break;
        case Number("0x2C01"):
            result = "Weak Medium"
            break;
        case Number("0xE803"):
            result = "Drain"
            break;
        case Number("0xE703"):
            result = "Repel"
            break;
        case Number("0x8403"):
            result = "Random"
            break;
        default:
            break;
    }
    return result
}

/**
* Returns a text description of the given skill passive element type value.
* @param {Number} value
* @returns the text description of the given skill passive element type value.
*/
function translatePassiveElementType(value) {
    let result = ""
    switch (value) {
        case 0:
            result = "Physical"
            break;
        case 1:
            result = "Fire"
            break;
        case 2:
            result = "Ice"
            break;
        case 3:
            result = "Elec"
            break;
        case 4:
            result = "Force"
            break;
        case 5:
            result = "Light"
            break;
        case 6:
            result = "Dark"
            break;
        case 7:
            result = "Almighty"
            break;
        case 8:
            result = "Poison"
            break;
        case 10:
            result = "Confusion"
            break;
        case 11:
            result = "Charm"
            break;
        case 12:
            result = "Sleep"
            break;
        case 20:
            result = "Mirage"
            break;
        case 29:
            result = "Recovery"
            break;
        case 32:
            result = "Physical"
            break;
        default:
            break;
    }
    return result
}

/**
 * Generate a list of the levels each skill is obtained at
 * @returns an array containing skill names, ids and the levels they are obtained at
 *          {name: n, id: i, level: [x,y,z,...]}
 */
function generateSkillLevelList() {
    // For every Skill name create object containing name, id and empty level array
    let skillLevels = skillNames.map((n, i) => {
        return { name: n, id: i, level: [] }
    })

    // For every demon...
    for (let index = 0; index < compendiumArr.length; index++) {
        let demon = compendiumArr[index]
        // Add the demons level to the array of its Innate Skill
        skillLevels[demon.innate.id].level.push(demon.level.value)
        // Add the demons level to their initially learned skills
        for (let i = 0; i < demon.skills.length; i++) {
            let skill = demon.skills[i]
            skillLevels[skill.id].level.push(demon.level.value)
        }
        //Add the level the demons learns a skill at to the skills level list
        for (let i = 0; i < demon.learnedSkills.length; i++) {
            let skill = demon.learnedSkills[i]
            skillLevels[skill.id].level.push(skill.level)
        }
    }
    //Define skills that should be available to learn despite not being available to demons
    let skipNeeded = [240, 284, 255, 283, 284, 292, 293, 294, 300, 301, 306, 307, 310, 298, 299, 320, 321, 335, 336, 342, 370, 390, 394, 395, 849, 863, 864, 865, 918, 924, 925, 927]
    let busted = [259, 277, 289, 343, 883, 884, 885]
    let flawless = [295, 312, 329, 330, 331, 332, 333, 334, 337, 338, 339, 340, 341, 372, 373, 392, 397, 398, 861, 902, 903, 904, 905, 906, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 926]
    //For every skill determine the minimum and maximum level it is obtained at
    skillLevels = skillLevels.map(skill => {
        let minLevel = 99
        let maxLevel = 1
        skill.level.forEach(element => {
            if (element > maxLevel) {
                maxLevel = element
            }
            if (element < minLevel) {
                minLevel = element
            }
        })
        if (skill.level.length == 0) {
            minLevel = 0
            maxLevel = 0
        }
        //TODO: Define Levels for each skill exception


        return { name: skill.name, id: skill.id, level: [minLevel, maxLevel] }
    })
    return skillLevels
}

/**
 * Generate a list of each level and what skills can be obtained at that level.
 * A skill is obtainable at a level when the level is not outside of the bounds set by the skills
 * min and max level.
 * @param {Array} skillLevels [{name:n, id:i, level:[x,y,...]},{...}]
 * @returns array of levels and the skills at that level in the following form [[id, id, id],...]
 */
function generateLevelSkillList(skillLevels) {
    let levelList = []
    //Populate the levelList array with empty arrays for each level
    for (let index = 0; index < 100; index++) {
        levelList.push([])
    }

    //Rebuild Level Array
    levelList = levelList.map((arr, index) => {
        let foundSkills = []
        /**
         * For each skill, add it to the foundSkills Array if it fulfills the following conditions
         * - not already in the array
         * - not an innate skill
         * - current level is in the bounds [min,max] set by skill
         * - is not an unused or uneditable skill
         */
        skillLevels.forEach(skill => {
            if ((void (0) === foundSkills.find((a) => a.id === skill.id)) && (skill.id <= 530 || skill.id >= 801) && skill.level[0] <= index && index <= skill.level[1] && !skill.name.startsWith("//Don't edit or remove th") && !skill.name.startsWith('NOT USED:')) {
                foundSkills.push(skill)
            }
        })
        //Build new sorted array from ids of skills of foundSkills Array
        let numbers = foundSkills.map((e, i) => {
            return e.id
        }).sort((a, b) => a > b)
        // Remove duplicates
        let uniqueIndeces = [...new Set(numbers)]
        // Rebuild array with duplicates removed
        let final = uniqueIndeces.map(unique => {
            let skill = foundSkills.find(skill => skill.id == unique)
            let id = skill.id
            let name = translateSkillID(id)
            return { name: name, id: id }
        })
        return final
    })

    return levelList
}

/**
 * Assigns every demon a random skill that could be learned at their level
 * @param {Array} comp the array of demon
 * @param {Array} levelList the list of levels and their learnable skills
 * @returns the edited compendium
 */
function assignCompletelyRandomSkills(comp, levelList) {
    //For every demon
    for (let index = 0; index < comp.length; index++) {
        let demon = comp[index];
        let possibleSkills = []
        //get all skills that can be learned at the demons level
        levelList[demon.level.value].forEach(e => possibleSkills.push(e))
        // Replace every initially learned skill of the demon with a random skill of the possible skills
        demon.skills = demon.skills.map(skill => {
            let newID = possibleSkills[Math.floor(Math.random() * possibleSkills.length)].id
            let newName = translateSkillID(newID)
            return { id: newID, translation: newName }
        })
    }
    return comp
}

/**
 * Assigns every demon new skills randomized based on weights by including the levels above and below them
 * @param {Array} the array of demon
 * @param {Array} levelList the list of levels and their learnable skills
 * @returns the edited compendium
 */
function assignCompletelyRandomWeightedSkills(comp, levelList) {
    //For every demon...
    for (let index = 0; index < comp.length; index++) {
        let demon = comp[index];
        let possibleSkills = []
        //get all skills that can be learned at the demons level
        levelList[demon.level.value].forEach(e => possibleSkills.push(e))
        //And add the skills at learned at the level below and on top
        if (demon.level.value < 99) {
            levelList[demon.level.value + 1].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 1) {
            levelList[demon.level.value - 1].forEach(e => possibleSkills.push(e))
        }
        // Create the weighted list of skills
        let weightedSkills = createWeightedList(possibleSkills)
        if (weightedSkills.values.length > 0) {
            // For every skill change the id to a random one that is not already assigned
            demon.skills = demon.skills.map(skill => {
                let uniqueSkill = false
                let rng = 0
                while (uniqueSkill == false) {
                    rng = weightedRando(weightedSkills.values, weightedSkills.weights)
                    if (void (0) === demon.skills.find(e => e.id == rng)) {
                        uniqueSkill = true
                    }
                }
                return { id: rng, translation: translateSkillID(rng) }
            })
        }
        // if(demon.id ==345) {console.log(demon.skills)}
    }
    return comp
}

/**
 * Assigns every demon new skills randomized based on weights.
 * The weights are compromised of the skills learnable at the demons level and up to 3 level below and above them.
 * Additionally the weights are adjusted to max the skill potential of demons, making skills with positive potential more likely and negative potential less likely if not impossible.
 * @param {Array} the array of demon
 * @param {Array} levelList the list of levels and their learnable skills
 * @returns the edited compendium
 */
function assignRandomPotentialWeightedSkills(comp, levelList) {
    //For every demon...
    for (let index = 0; index < comp.length; index++) {
        let demon = comp[index];
        let possibleSkills = []
        //get all skills that can be learned at the demons level

        levelList[demon.level.value].forEach(e => {
            // console.log(demon.name + "" + demon.level.value)
            // console.log(demon.level.value)
            possibleSkills.push(e)
        })

        //And add the skills learnable at up to 3 level below and above the demons level
        if (demon.level.value < 99) {
            levelList[demon.level.value + 1].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 1) {
            levelList[demon.level.value - 1].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 2) {
            levelList[demon.level.value - 2].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 3) {
            levelList[demon.level.value - 3].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value < 98) {
            levelList[demon.level.value + 2].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value < 97) {
            levelList[demon.level.value + 3].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 70) {
            levelList[demon.level.value - 4].forEach(e => possibleSkills.push(e))
            levelList[demon.level.value - 5].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 90) {
            levelList[demon.level.value - 6].forEach(e => possibleSkills.push(e))
            levelList[demon.level.value - 7].forEach(e => possibleSkills.push(e))
            levelList[demon.level.value - 8].forEach(e => possibleSkills.push(e))
        }
        // Create the weighted list of skills and update it with potentials
        let weightedSkills = createWeightedList(possibleSkills)
        weightedSkills = updateWeightsWithPotential(weightedSkills, demon.potential, demon)

        var totalSkills = []
        //If there are skills to be learned
        if (weightedSkills.values.length > 0) {
            // For every skill change the id to a random one that is not already assigned to this demon
            demon.skills = demon.skills.map((skill, index) => {
                let uniqueSkill = false
                let rng = 0
                while (uniqueSkill == false) {
                    rng = weightedRando(weightedSkills.values, weightedSkills.weights)
                    if (void (0) === demon.skills.find(e => e.id == rng)) {
                        if (checkAdditionalSkillConditions(obtainSkillFromID(rng), totalSkills, demon)) {
                            //if skill is unique set weight of skill to 0, so it cannot be result of randomization again
                            uniqueSkill = true
                            weightedSkills.weights[weightedSkills.values.indexOf(rng)] = 0
                        }

                    }
                }
                let skillAddition = { id: rng, translation: translateSkillID(rng) }
                totalSkills.push(skillAddition)
                return { id: rng, translation: translateSkillID(rng) }
            })
            //Randomly assign learnable skills
            demon.learnedSkills = demon.learnedSkills.map((skill, index) => {
                // For every skill change the id to a random one that is not already assigned to this demon
                let uniqueSkill = false
                let rng = 0
                while (uniqueSkill == false) {
                    rng = weightedRando(weightedSkills.values, weightedSkills.weights)
                    if (void (0) === demon.skills.find(e => e.id == rng) && void (0) === demon.learnedSkills.find(e => e.id == rng)) {
                        if (checkAdditionalSkillConditions(obtainSkillFromID(rng), totalSkills, demon)) {
                            //if skill is unique set weight of skill to 0, so it cannot be result of randomization again
                            uniqueSkill = true
                            weightedSkills.weights[weightedSkills.values.indexOf(rng)] = 0
                        }
                    }
                }
                let skillAddition = { id: rng, translation: translateSkillID(rng) }
                totalSkills.push(skillAddition)
                return { id: rng, translation: translateSkillID(rng), level: skill.level }
            })
        }
    }
    return comp
}

/**
* This function checks whether the given skill passes at least one of several conditions that are predefined before certain skills can be assigned to the demon.
* In order to check the conditions totalSkillList containing the currently assigned skills of the demon and the demon data itself is necessary.
* The functions returns true if the skill can be given to the demon and false otherwise.
* @param {Object} skill The skill for which conditions are checked
* @param {Array} totalSkillList The currently assigned skills to the demon
* @param {Object} demon The demon data itself
* @returns true if the skill passes at least one condition and else otherwise
*/
function checkAdditionalSkillConditions(skill, totalSkillList, demon) {
    let conditionalSkills = ["Charge", "Critical Aura", "Concentrate", "Curse Siphon", "Great Curse Siphon", "Virus Carrier", "Bowl of Hygieia", "Heal Pleroma", "High Heal Pleroma", "Nation Founder", "Healing Hand", "Oath of Plenteousness",
        "Poison Adept", "Poison Master", "Sankosho", "Incendiary Stoning", "Roaring Mist", "Herkeios", "Carpet Bolting", "Catastrophic Gales", "Lighted Wheel", "Boon of Sloth", "Ceaseless Crucifixion", "Biondetta", "Nation Builder"
    ]
    //Return early if skill is not a skill for which special conditions apply.
    if ((void (0) === conditionalSkills.find(e => e == skill.name) && !skill.name.includes("Pleroma") && !skill.name.includes("Enhancer") && !skill.name.includes("Gestalt"))) {
        return true
    }

    if ((skill.name == "Charge" || skill.name == "Critical Aura") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).skillType.value == 0)) || demon.potential.physical > 0)) {
        //Check for Charge, Critical Aura when already assigned Str-Based Skill or Demon has positive Physical Potential
        return true
    } else if (skill.name == "Concentrate" && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).skillType.value == 1)) || demon.stats.str.start <= demon.stats.mag.start)) {
        //Check for Concentrate when already assigned Mag-Based Skill or Demon has higher base mag than str
        return true
    } else if ((skill.name == "Curse Siphon" || skill.name == "Great Curse Siphon" || skill.name == "Virus Carrier") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).skillType.value == 2)) || demon.potential.ailment > 0)) {
        //Check for Curse Siphon, Great Curse Siphon, Virus Carrier when already assigned ailment Skill or Demon has positive ailment Potential
        return true
    } else if ((skill.name == "Bowl of Hygieia" || skill.name == "Heal Pleroma" || skill.name == "High Heal Pleroma" || skill.name == "Nation Founder" || skill.name == "Healing Hand" || skill.name == "Oath of Plenteousness") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).skillType.value == 3)) || demon.potential.recover > 0)) {
        //Check for Bowl of Hygieia, Heal Pleroma, High Heal Pleroma, Nation Founder, Healing Hand, Oath of Plenteousness when already assigned heal Skill or Demon has positive recover Potential
        return true
    } else if ((skill.name == "Poison Adept" || skill.name == "Poison Master") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).ailmentFlags.poison > 0)) || demon.potential.ailment > 0)) {
        //Check for Poison Adept, Poison Master when already assigned poison-inflicting Skill or Demon has positive ailment Potential
        return true
    } else if ((skill.name == "Phys Pleroma" || skill.name == "High Phys Pleroma" || skill.name == "Phys Enhancer" || skill.name == "Phys Gestalt" || skill.name == "Sankosho") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 0)) || demon.potential.physical > 0)) {
        //Check for Phys Pleroma, High Phys Pleroma, Phys Enhancer, Phys Gestalt, Sankosho when already assigned phys element Skill or Demon has positive Physical Potential
        return true
    } else if ((skill.name == "Fire Pleroma" || skill.name == "High Fire Pleroma" || skill.name == "Fire Enhancer" || skill.name == "Fire Gestalt" || skill.name == "Incendiary Stoning") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 1)) || demon.potential.fire > 0)) {
        //Check for Fire Pleroma, High Fire Pleroma, Fire Enhancer, Fire Gestalt, Incendiary Stoning when already assigned fire element Skill or Demon has positive fire Potential
        return true
    } else if ((skill.name == "Ice Pleroma" || skill.name == "High Ice Pleroma" || skill.name == "Ice Enhancer" || skill.name == "Ice Gestalt" || skill.name == "Roaring Mist") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 2)) || demon.potential.ice > 0)) {
        //Check for Ice Pleroma, High Ice Pleroma, Ice Enhancer, Ice Gestalt, Roaring Mist when already assigned ice element Skill or Demon has positive ice Potential
        return true
    } else if ((skill.name == "Elec Pleroma" || skill.name == "High Elec Pleroma" || skill.name == "Elec Enhancer" || skill.name == "Herkeios" || skill.name == "Elec Gestalt" || skill.name == "Carpet Bolting") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 3)) || demon.potential.elec > 0)) {
        //Check for Elec Pleroma, High Elec Pleroma, Elec Enhancer, Herkeios, Elec Gestalt, Carpet Bolting when already assigned Elec element Skill or Demon has positive elec Potential
        return true
    } else if ((skill.name == "Force Pleroma" || skill.name == "High Force Pleroma" || skill.name == "Force Enhancer" || skill.name == "Force Gestalt" || skill.name == "Catastrophic Gales") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 4)) || demon.potential.force > 0)) {
        //Check for Force Pleroma, High Force Pleroma, Force Enhancer, Force Gestalt, Catastrophic Gales when already assigned Force element Skill or Demon has positive Force Potential
        return true
    } else if ((skill.name == "Light Pleroma" || skill.name == "High Light Pleroma" || skill.name == "Light Enhancer" || skill.name == "Light Gestalt" || skill.name == "Lighted Wheel") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 5)) || demon.potential.light > 0)) {
        //Check for Light Pleroma, High Light Pleroma, Light Enhancer, Light Gestalt, Lighted Wheel when already assigned Light element Skill or Demon has positive Light Potential
        return true
    } else if ((skill.name == "Dark Pleroma" || skill.name == "High Dark Pleroma" || skill.name == "Dark Enhancer" || skill.name == "Dark Gestalt" || skill.name == "Boon of Sloth") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 6)) || demon.potential.dark > 0)) {
        //Check for Dark Pleroma, High Dark Pleroma, Dark Enhancer, Dark Gestalt, Boon of Sloth when already assigned Dark element Skill or Demon has positive Dark Potential
        return true
    } else if ((skill.name == "Almighty Pleroma" || skill.name == "High Almighty Pleroma" || skill.name == "Ceaseless Crucifixion") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).element.value == 7)) || demon.potential.almighty > 0)) {
        //Check for Almighty Pleroma, High Almighty Pleroma, Ceaseless Crucifixion when already assigned Almighty element Skill or Demon has positive Almighty Potential
        return true
    } else if ((skill.name == "Biondetta") && (demon.race.value != 2 && demon.race.value != 3 && demon.race.value != 24 && demon.race.value != 28)) {
        //Check for Biondetta when demon does not belong to herald, megami, femme, lady race
        return true
    } else if ((skill.name == "Nation Builder") && ((void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active" && obtainSkillFromID(e.id).skillType.value == 4)) || demon.potential.support > 0)) {
        //Check for Nation Builder when already assigned support type skill or demon has positive support potential
    } else if ((totalSkillList.length + 1 == demon.skills.length) && (determineSkillStructureByID(skill.id) == "Active" || void (0) !== totalSkillList.find(e => determineSkillStructureByID(e.id) == "Active"))) {
        //Check if we are at last initial skill and we have at least one active or current one is active
        return true
    } else {
        //Skill fullfills no additional skill conditions
        return false
    }
}

/**
* Update the weights in the weightList by applying the given skill potentials to the skills
* @param {Array} weightList Array with sub-arrays weights and values
* @param {Object} potentials Object containing the data of skill potentials of a demon
* @returns weightList updated with the potentials
*/
function updateWeightsWithPotential(weightList, potentials, demon) {
    // console.log(weightList)
    //For every skill in weight list
    let newWeights = weightList.values.map((element, index) => {
        //start with old weight
        let newWeight = weightList.weights[index]

        let skill = obtainSkillFromID(element)
        let skillStructure = determineSkillStructureByID(skill.id)
        //Passive skills do not have a corresponding potential by default so we need to handle them seperately
        if (skillStructure == "Active") {
            let potentialType = skill.potentialType.translation
            let additionalWeight = 2 * obtainPotentialByName(potentialType, potentials)
            if (potentialType == "Phys" && demon.stats.str.start < demon.stats.mag.start) {
                additionalWeight = additionalWeight - 2
            }
            // if(skill.name == "Profaned Land") {additonalWeight = additionalWeight * additionalWeight}
            if (additionalWeight < 0) {
                newWeight = 0
            } else {
                newWeight = newWeight + additionalWeight
            }
        } else {
            //Maybe do available passive logic here????
        }
        return newWeight
    })

    return { values: weightList.values, weights: newWeights }
}

/**
* Returns the skill potential value based on the potential type indicated by a string.
* @param {String} name the potential type to return the value of 
* @param {Object} potentials contains data on the skill potential of a demon
* @returns the skill potential described the given name
*/
function obtainPotentialByName(name, potentials) {
    switch (name) {
        case "Phys":
            return potentials.physical
            break;
        case "Fire":
            return potentials.fire
            break;
        case "Ice":
            return potentials.ice
            break;
        case "Elec":
            return potentials.elec
            break;
        case "Force":
            return potentials.force
            break;
        case "Light":
            return potentials.light
            break;
        case "Dark":
            return potentials.dark
            break;
        case "Almighty":
            return potentials.almighty
            break;
        case "Ailment":
            return potentials.ailment
            break;
        case "Recover":
            return potentials.recover
            break;
        case "Support":
            return potentials.support
            break;
        default:
            return 0
            break;
    }
}

/**
 * Based on array of skills creates two arrays where each skill is only included once.
 * Skills that were originally present more than once have increased weight.
 * @param {Array} possibleSkills Array of skills 
 * @returns an array of values and an array of weights
 */
function createWeightedList(possibleSkills) {
    let ids = []
    let prob = []
    //For every skill...
    possibleSkills.forEach(skill => {
        // if duplicate increase weight
        if (ids.includes(skill.id)) {
            prob[ids.indexOf(skill.id)] += 1
        } else {
            // else push value and base weight 
            ids.push(skill.id)
            prob.push(1)
        }
    })
    return { values: ids, weights: prob }
}

/**
* Based on the skill id, returns which area of the skillTable the skill belongs to as a String.
* @param {Number} id of the skill
* @returns area of the skillTable the skill belongs to as a String
*/
function determineSkillStructureByID(id) {
    if (id < 401) {
        return "Active"
    } else if (id < 531) {
        return "Pasive"
    } else if (id < 801) {
        return "Innate"
    } else {
        return "Active"
    }
}

/**
 * Write the values in newComp to the respective locations in the buffer
 * @param {Buffer} buffer of the Demon Table
 * @param {Array} newComp containing data for all usable demons
 * @returns the updated buffer
 */
function updateCompendiumBuffer(buffer, newComp) {
    newComp.forEach(demon => {
        // Write the id of the demons skills to the buffer
        demon.skills.forEach((skill, index) => {
            buffer.writeInt32LE(skill.id, demon.offsetNumbers.firstSkill + 4 * index)
        })
        // Write the id and levels of the demons learnable skills to the buffer
        demon.learnedSkills.forEach((skill, index) => {
            buffer.writeInt32LE(skill.id, demon.offsetNumbers.firstLearnedLevel + 8 * index + 4)
            buffer.writeInt32LE(skill.level, demon.offsetNumbers.firstLearnedLevel + 8 * index)
        })

        //Write the level of the demon to the buffer
        buffer.writeInt32LE(demon.level.value, demon.offsetNumbers.level)
    })
    return buffer
}

/**
 * Write the values in fusions to the respective locations in the buffer
 * @param {Buffer} buffer of the normal fusion table
 * @param {Array} fusions containing data for all possible normal fusions
 * @returns the updated buffer
 */
function updateNormalFusionBuffer(buffer, fusions) {
    fusions.forEach(fusion => {
        buffer.writeInt32LE(fusion.firstDemon.value, fusion.offsetNumbers.firstDemon)
        buffer.writeInt32LE(fusion.secondDemon.value, fusion.offsetNumbers.secondDemon)
        buffer.writeInt32LE(fusion.result.value, fusion.offsetNumbers.result)
    })
}

/**
 * Write the values in fusions to the respective locations in the buffer
 * @param {Buffer} buffer of the other fusion table
 * @param {Array} fusions containing data for all possible special fusions
 * @returns the updated buffer
 */
function updateOtherFusionArr(buffer, fusions) {
    fusions.forEach(fusion => {
        buffer.writeInt16LE(fusion.demon1.value, fusion.baseOffset + 2)
        buffer.writeInt16LE(fusion.demon2.value, fusion.baseOffset + 4)
        buffer.writeInt16LE(fusion.demon3.value, fusion.baseOffset + 6)
        buffer.writeInt16LE(fusion.demon4.value, fusion.baseOffset + 8)
        buffer.writeInt16LE(fusion.result.value, fusion.baseOffset + 10)
    })
}

/**
 * Check if a certain race of demons contains two demons of the same level
 * @param {Array} comp 
 */
function checkRaceDoubleLevel(comp) {
    let raceLevels = raceArray.map(race => {
        return { name: race, levels: [] }
    })
    comp.forEach(demon => {
        if (!demon.name.startsWith("NOT USED")) {
            raceLevels[demon.race.value - 1].levels.push(demon.level.value)
        }

    })
    console.log(raceLevels)
}

/**
 * Output the id of the demon with the given name to the consol
 * @param {String} name 
 * @param {Array} comp 
 */
function logDemonByName(name, comp) {
    let nameFound = true
    let index = 0
    while (nameFound) {
        if (comp[index].name === name) {
            console.log(comp[index])
            nameFound = false
        } else {
            index++
        }
    }
}

/**
 * For a list of values and weights, outputs a random value taking the weight of values into account
 * @param {Array} values array of numbers
 * @param {Array} weights array of numbers, weights belonging to values with the same index
 * @returns 
 */
function weightedRando(values, weights) {
    let total = 0
    weights.forEach(w => {
        total = total + w
    })
    // Generate random number with max being the total weight
    let rng = Math.floor(Math.random() * total)

    let cursor = 0
    // Add weights together until we reach random number and then apply that value
    for (let i = 0; i < weights.length; i++) {
        cursor += weights[i]
        if (cursor >= rng) {
            return values[i]
        }
    }

}

/**
* Assign every demon a completely random level between 1 and 98.
* Also updates to the levels of the learnable skills to have the same difference as the in the original data when possible.
* @param {Array} comp array containing all demon data
* @returns the demon data array with changed levels
*/
function assignCompletelyRandomLevels(comp) {
    for (let index = 0; index < comp.length; index++) {
        const element = comp[index];
        // Only up to 98 so level 99 demons can still learn their skills on a non godborn file
        let newLevel = Math.floor(Math.random() * 98 + 1)
        element.learnedSkills = element.learnedSkills.map(skill => {
            let skillLevel = (skill.level - element.level.value) + newLevel
            if (skillLevel > 99) { skillLevel = 99 }
            skill.level = skillLevel
            return skill
        })
        element.level.value = newLevel
    }

    return comp
}

/**
* Re-calculate the normal fusion result of every demon based on their race and level.
* In contrast to the normal game, does not remove fusion of two demons which also exist as ingredients to a special fusion
* Example: Normally Pixie + Angel does not create a normal fusion, since they are a special fusion for High Pixie. If their levels and races are unchanged they would result to Fortuna.
* @param {Array} fusions the array of normal fusions to modify
* @param {Array} comp the array of demons 
*/
function adjustFusionTableToLevels(fusions, comp) {
    //Recreate the fusion array in its original form
    //Mostly as a way of testing
    let oldFusions = fusions.map(element => {
        let firstDemon = {
            value: element.firstDemon.value,
            translation: comp[element.firstDemon.value].name
        }
        let secondDemon = {
            value: element.secondDemon.value,
            translation: comp[element.secondDemon.value].name
        }
        let result = {
            value: element.result.value,
            translation: comp[element.result.value].name
        }
        return { firstDemon: firstDemon, secondDemon: secondDemon, result: result }
    })

    let raceTable = createRaceTables(comp)//lists of demon of each race in order
    let specialFusions = listSpecialFusables() //list of demon IDs that cant be result


    //Filters out all demons that are obtainable via special fusion
    raceTable = raceTable.map(race => {
        let newRace = race.filter(demon => !specialFusions.includes(demon.id))
        return newRace
    })

    //Remove old Lilith as valid result
    raceTable[31].pop()


    //For each fusion...
    fusions.forEach(fusion => {
        let demon1 = comp[fusion.firstDemon.value]
        let demon2 = comp[fusion.secondDemon.value]
        let demon1Race = demon1.race.value
        let demon2Race = demon2.race.value
        //obtain the normal race of the resulting demon
        let targetRace = fusionChartArr.find(element => (element.race1.value == demon1Race && element.race2.value == demon2Race) || (element.race1.value == demon2Race && element.race2.value == demon1Race))

        // console.log(targetRace)
        //Check if the fusion results in a valid race
        if (targetRace !== void (0)) {
            // Check if the fusion results in an "Element"
            if (raceArray[targetRace.result.value] === "Element") {
                // Element fusions are doable by combining two demons of the same race
                // Depending on the ingredients race, a different element is the result of the fusion
                switch (raceArray[demon1Race]) {
                    case "Herald":
                    case "Deity":
                    case "Jaki":
                    case "Kunitsu":
                    case "Fallen":
                    case "Snake":
                    case "Tyrant":
                    case "Drake":
                        fusion.result.value = 155 //Flaemis id
                        fusion.result.translation = comp[155].name
                        break;
                    case "Megami":
                    case "Vile":
                    case "Avatar":
                    case "Genma":
                    case "Wilder":
                    case "Femme":
                    case "Brute":
                    case "Haunt":
                        fusion.result.value = 156 //Aquans id
                        fusion.result.translation = comp[156].name
                        break;
                    case "Avian":
                    case "Divine":
                    case "Yoma":
                    case "Raptor":
                    case "Holy":
                    case "Fairy":
                    case "Fury":
                    case "Dragon":
                        fusion.result.value = 157 //Aeros id
                        fusion.result.translation = comp[157].name
                        break;
                    default:
                        fusion.result.value = 158 //Erthrys id
                        fusion.result.translation = comp[158].name
                        break;
                }

            } else {
                //if fusion is valid and targetRace is not element
                // calculate the resulting demon and save it to the fusion
                let resultingDemon = determineNormalFusionResult(demon1.level.value, demon2.level.value, raceTable[targetRace.result.value])
                fusion.result.value = resultingDemon.id
                fusion.result.translation = comp[resultingDemon.id].name
            }

        } else {
            //if target race is not a valid fusion
            // first define what effects the element demons have on the result of each demon
            // Fusing elements with another demon results in a demon of the same race with either an decreased or increased base level
            // 0 means unfusable, -1 reduces the level of the resulting demon, 1 increases it
            let erthys = [0, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, 1, -1, -1, -1, 0, 0, 1, -1, 1, 0, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            let aeros = [0, 0, -1, -1, 1, -1, 1, -1, 1, 0, -1, -1, -1, -1, -1, 0, 0, -1, 1, 1, 0, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            let aquans = [0, 0, -1, 1, -1, 1, 1, 1, -1, 0, -1, -1, 1, -1, 1, 0, 0, 1, -1, -1, 0, -1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            let flaemis = [0, 0, 1, -1, -1, 1, -1, -1, 1, 0, 1, -1, -1, 1, -1, 0, 0, -1, 1, -1, 0, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            // if the first demon ingredient is an element
            if (demon1Race == 15) {
                //determine direction based on race of 2nd demon ingredient
                let direction
                switch (demon1.name) {
                    case "Erthys":
                        direction = erthys[demon2Race]
                        break;
                    case "Aeros":
                        direction = aeros[demon2Race]
                        break;
                    case "Aquans":
                        direction = aquans[demon2Race]
                        break;
                    case "Flaemis":
                        direction = flaemis[demon2Race]
                        break;
                    default:
                        break;
                }
                let foundResult = false
                let searchTable = raceTable[demon2Race] //sorted list of demons of a certain race sorted by ascending level
                if (direction > 0) {
                    //Since we want to increase the level, start search at 0
                    for (let index = 0; index < searchTable.length; index++) {
                        const element = searchTable[index];
                        if (element.level.value > demon2.level.value && !foundResult) {
                            fusion.result.value = element.id
                            fusion.result.translation = element.name
                            foundResult = true
                        }
                    }
                    if (!foundResult) {
                        // if demon is highest level demon
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                    }
                } else if (direction < 0) {
                    //Since we want to decrease the level, start search at end of array
                    for (let index = searchTable.length - 1; index >= 0; index--) {
                        const element = searchTable[index];
                        if (element.level.value < demon2.level.value && !foundResult) {
                            fusion.result.value = element.id
                            fusion.result.translation = element.name
                            foundResult = true
                        }
                    }
                    if (!foundResult) {
                        // if demon is lowest level demon
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                    }
                } else {
                    // if the second demon should not fusable with an element
                    fusion.result.value = 0
                    fusion.result.translation = "Empty"
                }
            } else if (demon2Race == 15) {
                //determine direction based on race of first demon ingredient
                let direction
                switch (demon2.name) {
                    case "Erthys":
                        direction = erthys[demon1Race]
                        break;
                    case "Aeros":
                        direction = aeros[demon1Race]
                        break;
                    case "Aquans":
                        direction = aquans[demon1Race]
                        break;
                    case "Flaemis":
                        direction = flaemis[demon1Race]
                        break;
                    default:
                        break;
                }
                let foundResult = false
                let searchTable = raceTable[demon1Race]
                if (direction > 0) {
                    //Since we want to increase the level, start search at 0
                    for (let index = 0; index < searchTable.length; index++) {
                        const element = searchTable[index];
                        if (element.level.value > demon1.level.value && !foundResult) {
                            fusion.result.value = element.id
                            fusion.result.translation = element.name
                            foundResult = true
                        }
                    }
                    if (!foundResult) {
                        // if demon is highest level demon
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                    }
                } else if (direction < 0) {
                    //Since we want to decrease the level, start search at end of array
                    for (let index = searchTable.length - 1; index >= 0; index--) {
                        const element = searchTable[index];
                        if (element.level.value < demon1.level.value && !foundResult) {
                            fusion.result.value = element.id
                            fusion.result.translation = element.name
                            foundResult = true
                        }
                    }
                    if (!foundResult) {
                        // if demon is lowest level demon
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                    }
                } else {
                    // if the second demon should not fusable with an element
                    fusion.result.value = 0
                    fusion.result.translation = "Empty"
                }
            } else {
                fusion.result.value = 0
                fusion.result.translation = "Empty"
            }
        }
    })



    //Piece of code logging which fusions were changed
    // oldFusions.forEach((old, index) => {
    //     if (
    //         //(comp[old.firstDemon.value].race.translation != "Element" && comp[old.result.value].race.translation != "Element" && comp[old.secondDemon.value].race.translation != "Element") && 
    //         (old.firstDemon.value != fusions[index].firstDemon.value ||
    //             old.secondDemon.value != fusions[index].secondDemon.value ||
    //             old.result.value != fusions[index].result.value
    //         )) {
    //         console.log("OLD")
    //         console.log(old)
    //         console.log("NEW")
    //         console.log(index)
    //         console.log(fusions[index])
    //     }
    // })
}

function adjustSpecialFusionTable(fusions, comp) {

}

function adjustBasicEnemyArr(enemies, comp) {
    let foes = enemies.map((enemy, index) => {
        let statMods = {
            
        }

        let newStats = {

        }
    })
}

/**
* Based on the level of two demons and an array of demons of a race sorted by level ascending, determine which demon results in the normal fusion.
* Resulting demon is the demon with an level higher than the average of the two levels.
* @param {Number} level1 level of the first ingredient demon
* @param {Number} level2 level of the second ingredient demon
* @param {Array} resultTable  array of demons of a race sorted by level ascending
* @returns the demon that should result from the fusion
*/
function determineNormalFusionResult(level1, level2, resultTable) {
    let resultingLevel = Math.ceil((level1 + level2) / 2) + 1
    let foundDemon = false
    for (let index = 0; index < resultTable.length; index++) {
        const element = resultTable[index];
        if (element.level.value >= resultingLevel && !foundDemon) {
            return element
        }
    }
    return resultTable[resultTable.length - 1]
}

/**
* Returns an array of ids of all demons that are the result of a special fusion.
* @returns an array of ids of all demons that are the result of a special fusion.
*/
function listSpecialFusables() {
    let demons = specialFusionArr.map(fusion => {
        return fusion.result.value
    })
    return demons
}

/**
* Creates Arrays for each race containing the registerable demons of that race in ascending order based on their level.
* @param {Array} comp the array containing the data of all demons
* @returns array containing an array for each race containing the registerable demons of that race in ascending order based on their level
*/
function createRaceTables(comp) {
    //For every race...
    let raceTable = raceArray.map(race => {
        let demonList = []
        // go trough each demon
        comp.forEach(demon => {
            if (race == demon.race.translation && !demon.name.startsWith('NOT USED')) {
                // and add them to the array if they belong to the race and are used
                demonList.push(demon)
            }
        })
        //Sort array in ascending order
        demonList = demonList.sort((a, b) => a.level.value - b.level.value)
        return demonList
    })

    return raceTable
}

/**
* Defines how many demons start at each level.
* @param {Array} comp Array containing data on all playable demons
*/
function defineLevelSlots(comp) {
    let slots = []
    for (let index = 0; index < 100; index++) {
        slots.push(0)
    }

    comp.forEach(demon => {
        if (!demon.name.startsWith('NOT')) {
            slots[demon.oldlevel]++
        }

    })
}

/**
* Determines which combination of starting races is able to fuse into every other race in the fusion chart and which race can only achieve this with additonal races added.
*/
function determineFusability() {
    // Mark races that are not part of the fusion chart
    let filteredArray = raceArray.map((e, i) => {
        let special = false
        if (i > (raceArray.length - 14) || e.startsWith("Element") || e.startsWith("Chaos") || e.startsWith("Fiend") || e.startsWith("Non") || e.startsWith("Unused") || e.startsWith("Mitama")) {
            special = true
        }
        return { name: e, fusable: false, obtained: false, special: special, id: i }
    })

    //Filter out Races that are not part of the fusion chart
    let races = filteredArray.filter(e => e.special == false)
    // console.log(races.length - raceArray.length)

    // Due to filter index!= id, so new method is needed
    function returnRaceByID(id) {
        return races.find(f => f.id == id)
    }
    let OGraces = races.map(e => {
        return { name: e.name, fusable: e.fusable, obtained: e.obtained, id: e.id }
    })

    OGraces.forEach((first, findex) => {
        for (let jindex = findex; jindex < OGraces.length; jindex++) {
            //for each pair of races

            //these races get modified so we need to recopy them
            races = OGraces.map(e => {
                return { name: e.name, fusable: e.fusable, obtained: e.obtained, id: e.id }
            })
            var second = races[jindex];
            returnRaceByID(first.id).obtained = true
            returnRaceByID(second.id).obtained = true
            returnRaceByID(first.id).fusable = true
            returnRaceByID(second.id).fusable = true
            // console.log(first)
            // console.log(second)

            // console.log(races)

            let unique = false

            let demonCount = 2
            let externalDemon = 2
            let recruits = []
            recruits.push(first.name)
            recruits.push(second.name)
            let currentRaces = []
            currentRaces.push(first)
            currentRaces.push(second)
            let availableFusions = []
            // Finds the resulting race of a fusion between race1 and race2
            function calcfusionResult(race1, race2) {
                let fusion = fusionChartArr.find(f => (f.race1.translation == race1.name && f.race2.translation == race2.name) || (f.race1.translation == race2.name && f.race2.translation == race1.name))
                if (fusion !== void (0)) {
                    if (fusion.result.value == 0) {
                        return fusion
                    } else {
                        return races.find(f => f.id == fusion.result.value)
                    }
                } else {
                    return fusion
                }

            }
            //while there is a race that is not fusable yet
            while (void (0) !== races.find((r, i) => r.fusable == false)) {
                // console.log(races.find((r, i) => r.fusable == false).name)
                availableFusions = []
                //add fusable races to availableFusions if they are not already obtained 
                currentRaces.forEach((race1, i) => {
                    for (let index = i + 1; index < currentRaces.length; index++) {
                        let race2 = currentRaces[index];
                        let fusionResult = calcfusionResult(race1, race2)
                        if (void (0) != fusionResult && !availableFusions.includes(fusionResult) && fusionResult.obtained == false) {
                            availableFusions.push(fusionResult)
                        }
                    }
                })
                //For each available fusion, set the fused race to fusable and obtained
                availableFusions.forEach(fusion => {
                    fusion.fusable = true
                    fusion.obtained = true
                    currentRaces.push(fusion)
                    demonCount++
                })
                //if there is no available fusionm radomly add another random race to obtained
                if (availableFusions.length == 0) {
                    unique = false
                    let newRace = races[Math.floor(Math.random() * (races.length - 14))]
                    while (!unique) {
                        if (newRace.obtained == true) {
                            newRace = races[Math.floor(Math.random() * (races.length))]
                        } else {
                            unique = true
                            returnRaceByID(newRace.id).fusable = true
                            returnRaceByID(newRace.id).obtained = true
                            demonCount++
                            externalDemon++
                            currentRaces.push(newRace)
                            recruits.push(newRace.name)
                            // console.log("Recruit; " + newRace.name)
                        }
                    }
                }
            }
            // console.log(demonCount)
            // console.log(externalDemon)
            console.log(recruits)
        }
    })

    // let first = races[Math.floor(Math.random() * (races.length - 14))]
    // let unique = false
    // let second = races[Math.floor(Math.random() * (races.length - 14))]
    // while (!unique) {
    //     if (second.name == first.name) {
    //         second = races[Math.floor(Math.random() * (races.length))]
    //     } else {
    //         unique = true
    //     }
    // }


}

/**
* Logs all skills that are not normally assigned to a playable demon.
* @param {Array} skillLevels array of skills and at what they are first and last available at
*/
function findUnlearnableSkills(skillLevels) {
    skillLevels.forEach(skill => {
        if (skill.level[0] == 0 && skill.level[1] == 0 && !skill.name.startsWith("NOT USED")
            && (determineSkillStructureByID(skill.id) == "Active" && obtainSkillFromID(skill.id).magatsuhi.enable == 0)
        ) {
            console.log(skill)
        }

    })
}

async function main() {
    let compendiumBuffer = await readNKMBaseTable()
    let skillBuffer = await readSkillData()
    let normalFusionBuffer = await readNormalFusionTables()
    let otherFusionBuffer = await readOtherFusionTables()
    await readDemonNames()
    await readSkillNames()
    fillCompendiumArr(compendiumBuffer)
    fillSkillArrs(skillBuffer)
    fillNormalFusionArr(normalFusionBuffer)
    fillFusionChart(otherFusionBuffer)
    fillSpecialFusionArr(otherFusionBuffer)
    fillBasicEnemyArr(compendiumBuffer)


    let skillLevels = generateSkillLevelList()
    // console.log(skillLevels)
    let levelSkillList = generateLevelSkillList(skillLevels)
    // console.log(obtainSkillFromID(928))
    // console.log(skillArr[400].name)
    // console.log(skillArr[401].name)
    // console.log(skillArr.find(e=> e.id == 1))
    // console.log(specialFusionArr[specialFusionArr.length -1])
    // let newComp = assignCompletelyRandomLevels(compendiumArr)
    let newComp = assignRandomPotentialWeightedSkills(compendiumArr, levelSkillList)



    adjustFusionTableToLevels(normalFusionArr, compendiumArr)
    // console.log(levelSkillList)
    // console.log(levelSkillList[1])
    // let newComp = assignCompletelyRandomSkills(compendiumArr,levelSkillList)
    // let newComp = assignCompletelyRandomWeightedSkills(compendiumArr, levelSkillList)

    // // console.log(skillLevels[1])
    // let newComp = assignCompletelyRandomLevels(compendiumArr)
    // console.log(compendiumArr[155].name)
    // console.log(compendiumArr[155].race)
    // console.log(logDemonByName("Isis",compendiumArr))
    // console.log(compendiumArr.length)
    // compendiumBuffer = updateCompendiumBuffer(compendiumBuffer, compendiumArr)
    compendiumBuffer = updateCompendiumBuffer(compendiumBuffer, newComp)
    // compendiumBuffer.writeInt32LE(5,0x1B369)
    // console.log(raceArray.length)
    // console.log(compendiumArr[365])
    updateOtherFusionArr(otherFusionBuffer, specialFusionArr)
    // console.log(normalFusionArr[normalFusionArr.length - 19])
    updateNormalFusionBuffer(normalFusionBuffer, normalFusionArr)
    // console.log(raceArray[6])
    // console.log(raceArray[23])
    // console.log(raceArray[31])
    // logDemonByName("Preta",compendiumArr)
    // console.log("END RESULT")
    // console.log(newComp[115])
    // console.log(newComp[116].skills)
    // console.log(newComp[116].learnedSkills)
    // console.log(obtainSkillFromID(113))
    // compendiumBuffer.writeInt32LE(472,28201)
    // checkRaceDoubleLevel(compendiumArr)
    // raceArray.sort()
    // console.log(enemyArr[299])


    await writeNormalFusionTable(normalFusionBuffer)
    await writeNKMBaseTable(compendiumBuffer)
    await writeOtherFusionTable(otherFusionBuffer)
    // findUnlearnableSkills(skillLevels)
    // defineLevelSlots(newComp)
    // determineFusability()
}

main()

