import { read } from 'fs';
import * as fs from 'fs/promises';

const raceArray = ["None", "Unused", "Herald", "Megami", "Avian", "Divine", "Yoma", "Vile", "Raptor", "Unused9", "Deity", "Wargod", "Avatar", "Holy", "Genma", "Element", "Mitama", "Fairy", "Beast", "Jirae", "Fiend", "Jaki", "Wilder", "Fury", "Lady", "Dragon", "Kishin", "Kunitsu", "Femme", "Brute", "Fallen", "Night", "Snake", "Tyrant", "Drake", "Haunt", "Foul", "Chaos", "Devil", "Meta", "Nahobino", "Proto-fiend", "Matter", "Panagia", "Enigma", "UMA", "Qadistu", "Human", "Primal", "Void"]

var compendiumArr = []
var compendiumNames = []
var skillNames = []
var skillArr = []
var passiveSkillArr = []

var innateSkillArr = []
var normalFusionArr = []
var fusionChartArr = []
var specialFusionArr = []

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
 * 
 * @returns 
 */
async function readNormalFusionTables() {
    var fileContents = (await fs.readFile('./base/UniteCombineTable.uexp'))

    return fileContents
}

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

async function writeNormalFusionTable(result) {
    await fs.writeFile('./rando/Project/Content/Blueprints/Gamedata/BinTable/Unite/UniteCombineTable.uexp', result)
}

/**
 * Fills the array compendiumArr with data extracted from the Buffer NKMBaseTable.
 * The end array contains data on all demons which are registered in the compendium and usable by the player.
 * @param {Buffer} NKMBaseTable the buffer to get the demon data from
 */
function fillCompendiumArr(NKMBaseTable) {
    // let json = NKMBaseTable.toJSON()

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
            level: { value: readInt32LE(locations.level) },
            registerable : readInt32LE(locations.HP - 4),
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
 * 
 * @param {Buffer} skillData 
 */
function fillSkillArrs(skillData) {
    function read4(ofSet) {
        return skillData.readInt32LE(ofSet)
    }
    function read1(ofSet) {
        return skillData.readUInt8(ofSet)
    }
    function read2(ofSet) {
        return skillData.readInt16LE(ofSet)
    }

    let startValue = 0x85
    let passiveStartValue = 0x132E5
    let skillOffset = 0xC4
    let passiveOffset = 0x6C
    let secondBatchStart = 0x1E305

    let fillerObject = { id: 0, name: "Filler" }
    skillArr.push(fillerObject)

    for (let index = 0; index < 950; index++) {
        //check if skill is passive 
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

            if (index >= 530) {
                innateSkillArr.push(toPush)
            } else {
                passiveSkillArr.push(toPush)
            }

        } else {
            // console.log(index)
            let offset = startValue + skillOffset * index
            let skillID = index + 1
            let skillName = translateSkillID(index + 1)
            // if(index == 5) {console.log((startValue + skillOffset * index).toString(16))}
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

function fillNormalFusionArr(fusionData) {
    function read4(ofSet) {
        return fusionData.readInt32LE(ofSet)
    }

    let startValue = 0xC5
    let fusionOffset = 0x7C

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

    // console.log(normalFusionArr)
}

function fillFusionChart(fusionData) {
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

function fillSpecialFusionArr(fusionData) {
    function read1(ofSet) {
        return fusionData.readUInt8(ofSet)
    }

    function read4(ofSet) {
        return fusionData.readInt32LE(ofSet)
    }

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

function translateSkillType(value) {
    let results = ["StrBased", "MagBased", "Ailment", "Heal", "Support", "", "RevivalChant", "", "", "", "", "", "", "LevelBased"]
    return results[value]
}

function translateSkillElement(value) {
    let results = ["Physical", "Fire", "Ice", "Elec", "Force", "Light", "Dark", "Almighty", "", "", "", "", "Ailment", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "Heal"]
    return results[value]
}

function translatePassiveResist(value) {
    let results = ["None", "Resist", "Null", "Repel", "Drain"]
    return results[value]
}

function translateTarget(value) {
    let results = ["SingleFoe", "AllFoe", "SingleAlly", "AllyAll", "Self", "Foe+AllyAll", "Random", "AllyAndStockSingle", "Ally+StockAll"]
    return results[value]
}

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
        //Add the level the demons learns a skill to the skills level list
        for (let i = 0; i < demon.learnedSkills.length; i++) {
            let skill = demon.learnedSkills[i]
            skillLevels[skill.id].level.push(skill.level)
        }
    }
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
            return {name: name, id: id}
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
 * Assigns every demon new skills randomized based on weights by including the levels above and below them
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
            possibleSkills.push(e)})
        
        //And add the skills at learned at the level below and on top
        if (demon.level.value < 99) {
            levelList[demon.level.value + 1].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 1) {
            levelList[demon.level.value - 1].forEach(e => possibleSkills.push(e))
        }
        if (demon.level.value > 2) {
            levelList[demon.level.value - 2].forEach(e => possibleSkills.push(e))
        }
        if(demon.level.value < 98) {
            levelList[demon.level.value + 2].forEach(e => possibleSkills.push(e))
        }
        if(demon.level.value < 97) {
            levelList[demon.level.value + 3].forEach(e => possibleSkills.push(e))
        }
        // console.log("PUSHED TROUGH")
        // Create the weighted list of skills
        let weightedSkills = createWeightedList(possibleSkills)
        weightedSkills = updateWeightsWithPotential(weightedSkills, demon.potential)
        if (weightedSkills.values.length > 0) {
            // For every skill change the id to a random one that is not already assigned
            demon.skills = demon.skills.map((skill, index) => {
                let uniqueSkill = false
                let rng = 0
                while (uniqueSkill == false) {
                    rng = weightedRando(weightedSkills.values, weightedSkills.weights)
                    if (void (0) === demon.skills.find(e => e.id == rng)) {
                        uniqueSkill = true
                        weightedSkills.weights[weightedSkills.values.indexOf(rng)] = 0
                    }
                }
                return { id: rng, translation: translateSkillID(rng) }
            })
            //Randomly assign learnable skills
            demon.learnedSkills = demon.learnedSkills.map((skill, index) => {

                let uniqueSkill = false
                let rng = 0
                while (uniqueSkill == false) {
                    rng = weightedRando(weightedSkills.values, weightedSkills.weights)
                    if (void (0) === demon.skills.find(e => e.id == rng)) {
                        uniqueSkill = true
                        weightedSkills.weights[weightedSkills.values.indexOf(rng)] = 0
                    }
                }
                return { id: rng, translation: translateSkillID(rng), level:skill.level }
            })
        }
    }
    return comp
}

// function addDuplicateWeights(weightedList) {
//     let newValues = []
//     let newWeights
// }

function updateWeightsWithPotential(weightList, potentials) {
    // console.log(weightList)
    let newWeights = weightList.values.map((element, index) => {
        let newWeight = weightList.weights[index]

        let skill = obtainSkillFromID(element)
        let skillStructure = determineSkillStructureByID(skill.id)
        if (skillStructure == "Active") {
            let potentialType = skill.potentialType.translation
            let additionalWeight = 2 * obtainPotentialByName(potentialType, potentials)
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
 * Skills that were originally present more than once have increased weight
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
        demon.learnedSkills.forEach((skill, index) => {
            buffer.writeInt32LE(skill.id, demon.offsetNumbers.firstLearnedLevel + 8 * index + 4)
            buffer.writeInt32LE(skill.level, demon.offsetNumbers.firstLearnedLevel + 8 * index)
        })

        //Write the level of the demon to the buffer
        buffer.writeInt32LE(demon.level.value, demon.offsetNumbers.level)
    })
    return buffer
}

function updateNormalFusionBuffer(buffer, fusions) {
    fusions.forEach(fusion => {
        buffer.writeInt32LE(fusion.firstDemon.value, fusion.offsetNumbers.firstDemon)
        buffer.writeInt32LE(fusion.secondDemon.value, fusion.offsetNumbers.secondDemon)
        buffer.writeInt32LE(fusion.result.value, fusion.offsetNumbers.result)
    })
}

/**
 * Check if a certain race of demons contains two demons of the level
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
    // Generate random number with max being the totoal weight
    let rng = Math.ceil(Math.random() * total)

    let cursor = 0
    // Add weights together until we reach random number and then apply that value
    for (let i = 0; i < weights.length; i++) {
        cursor += weights[i]
        if (cursor >= rng) {
            return values[i]
        }
    }

}

function assignCompletelyRandomLevels(comp) {
    for (let index = 0; index < comp.length; index++) {
        const element = comp[index];
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

function adjustFusionTableToLevels(fusions, comp) {
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
    // console.log(specialFusions)

    //Filters out all demons that are obtainable via special fusion
    raceTable = raceTable.map(race => {
        let newRace = race.filter(demon => !specialFusions.includes(demon.id))
        return newRace
    })

    //Remove old Lilith as viable result
    raceTable[31].pop()

    // raceTable[31].forEach(e => console.log(e.name))
    var alternativeFusionCollect = true

    if (alternativeFusionCollect) {

        fusions.forEach(fusion => {
            let demon1 = comp[fusion.firstDemon.value]
            let demon2 = comp[fusion.secondDemon.value]
            let demon1Race = demon1.race.value
            let demon2Race = demon2.race.value
            let targetRace = fusionChartArr.find(element => (element.race1.value == demon1Race && element.race2.value == demon2Race) || (element.race1.value == demon2Race && element.race2.value == demon1Race))

            // console.log(targetRace)
            if (targetRace !== void (0)) {

                if (raceArray[targetRace.result.value] === "Element") {
                    // console.log("TROL")
                    switch (raceArray[demon1Race]) {
                        case "Herald":
                        case "Deity":
                        case "Jaki":
                        case "Kunitsu":
                        case "Fallen":
                        case "Snake":
                        case "Tyrant":
                        case "Drake":
                            fusion.result.value = 155
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
                            fusion.result.value = 156
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
                            fusion.result.value = 157
                            fusion.result.translation = comp[157].name
                            break;
                        default:
                            fusion.result.value = 158
                            fusion.result.translation = comp[158].name
                            break;
                    }

                } else {
                    let resultingDemon = determineNormalFusionResult(demon1.level.value, demon2.level.value, raceTable[targetRace.result.value])
                    fusion.result.value = resultingDemon.id
                    fusion.result.translation = comp[resultingDemon.id].name
                }

            } else {
                let erthys = [0, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, 1, -1, -1, -1, 0, 0, 1, -1, 1, 0, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                let aeros = [0, 0, -1, -1, 1, -1, 1, -1, 1, 0, -1, -1, -1, -1, -1, 0, 0, -1, 1, 1, 0, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                let aquans = [0, 0, -1, 1, -1, 1, 1, 1, -1, 0, -1, -1, 1, -1, 1, 0, 0, 1, -1, -1, 0, -1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                let flaemis = [0, 0, 1, -1, -1, 1, -1, -1, 1, 0, 1, -1, -1, 1, -1, 0, 0, -1, 1, -1, 0, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                if (demon1Race == 15) {
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
                    let searchTable = raceTable[demon2Race]
                    if (direction > 0) {
                        for (let index = 0; index < searchTable.length; index++) {
                            const element = searchTable[index];
                            if (element.level.value > demon2.level.value && !foundResult) {
                                fusion.result.value = element.id
                                fusion.result.translation = element.name
                                foundResult = true
                            }
                        }
                    } else if (direction < 0) {
                        for (let index = searchTable.length - 1; index >= 0; index--) {
                            const element = searchTable[index];
                            if (element.level.value < demon2.level.value && !foundResult) {
                                fusion.result.value = element.id
                                fusion.result.translation = element.name
                                foundResult = true
                            }
                        }
                        if (!foundResult) {
                            fusion.result.value = 0
                            fusion.result.translation = "Empty"
                        }
                    } else {
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                    }
                } else if (demon2Race == 15) {
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
                        for (let index = 0; index < searchTable.length; index++) {
                            const element = searchTable[index];
                            if (element.level.value > demon1.level.value && !foundResult) {
                                fusion.result.value = element.id
                                fusion.result.translation = element.name
                                foundResult = true
                            }
                        }
                    } else if (direction < 0) {
                        for (let index = searchTable.length - 1; index >= 0; index--) {
                            const element = searchTable[index];
                            if (element.level.value < demon1.level.value && !foundResult) {
                                fusion.result.value = element.id
                                fusion.result.translation = element.name
                                foundResult = true
                            }
                        }
                        if (!foundResult) {
                            fusion.result.value = 0
                            fusion.result.translation = "Empty"
                        }
                    } else {
                        fusion.result.value = 0
                        fusion.result.translation = "Empty"
                    }
                } else {
                    fusion.result.value = 0
                    fusion.result.translation = "Empty"
                }
            }
            // console.log(fusion.result)
        })

    }

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

function listSpecialFusables() {
    let demons = specialFusionArr.map(fusion => {
        return fusion.result.value
    })
    return demons
}

function createRaceTables(comp) {
    let raceTable = raceArray.map(race => {
        let demonList = []
        comp.forEach(demon => {
            if (race == demon.race.translation && !demon.name.startsWith('NOT USED')) {
                demonList.push(demon)
            }
        })
        demonList = demonList.sort((a, b) => a.level.value - b.level.value)
        return demonList
    })

    return raceTable
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


    let skillLevels = generateSkillLevelList()
    // console.log(skillLevels)
    let levelSkillList = generateLevelSkillList(skillLevels)
    // console.log(obtainSkillFromID(928))
    // console.log(skillArr[400].name)
    // console.log(skillArr[401].name)
    // console.log(skillArr.find(e=> e.id == 1))
    // console.log(specialFusionArr[specialFusionArr.length -1])
    let newComp = assignCompletelyRandomLevels(compendiumArr)

    adjustFusionTableToLevels(normalFusionArr, compendiumArr)

    // console.log(levelSkillList)
    // console.log(levelSkillList[1])
    // let newComp = assignCompletelyRandomSkills(compendiumArr,levelSkillList)
    // let newComp = assignCompletelyRandomWeightedSkills(compendiumArr, levelSkillList)
    newComp = assignRandomPotentialWeightedSkills(compendiumArr, levelSkillList)
    // // console.log(skillLevels[1])
    // let newComp = assignCompletelyRandomLevels(compendiumArr)
    // console.log(compendiumArr[155].name)
    // console.log(compendiumArr[155].race)
    // console.log(logDemonByName("Isis",compendiumArr))
    // console.log(compendiumArr.length)

    compendiumBuffer = updateCompendiumBuffer(compendiumBuffer, newComp)
    // compendiumBuffer.writeInt32LE(5,0x1B369)
    // console.log(raceArray.length)
    // console.log(compendiumArr[165])

    // console.log(normalFusionArr[normalFusionArr.length - 19])
    updateNormalFusionBuffer(normalFusionBuffer, normalFusionArr)
    // console.log(raceArray[6])
    // console.log(raceArray[23])
    // console.log(raceArray[31])
    // logDemonByName("Preta",compendiumArr)
    // console.log("END RESULT")
    console.log(newComp[115])
    // console.log(newComp[116].skills)
    // console.log(newComp[116].learnedSkills)
    // console.log(obtainSkillFromID(113))
    // compendiumBuffer.writeInt32LE(472,28201)
    // checkRaceDoubleLevel(compendiumArr)
    // raceArray.sort()


    // await writeNormalFusionTable(normalFusionBuffer)
    // await writeNKMBaseTable(compendiumBuffer)


}

main()

