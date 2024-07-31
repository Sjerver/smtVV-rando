SKILL_MODIFIERS = ["None", "Charge", "Concentrate"]
SKILL_TYPES = ["StrBased", "MagBased", "Ailment", "Heal", "Support", "", "RevivalChant", "", "", "", "", "", "", "LevelBased", "", ""] #Index 14+ unknown
SKILL_ELEMENTS = ["Physical", "Fire", "Ice", "Elec", "Force", "Light", "Dark", "Almighty", "", "", "", "", "Ailment", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "Heal"]
PASSIVE_RESISTS = ["None", "Resist", "Null", "Repel", "Drain"]
SKILL_TARGETS = ["SingleFoe", "AllFoe", "SingleAlly", "AllyAll", "Self", "Foe+AllyAll", "Random", "AllyAndStockSingle", "Ally+StockAll"]
POTENTIAL_TYPES = ["Phys", "Fire", "Ice", "Elec", "Force", "Light", "Dark", "Almighty", "Ailment", "Support", "Recover", "", "", "Magatsuhi"]
RESIST_MAP = {
    0x0: 'Null',
    0x0A: 'Resist Severe',
    0x14: 'Resist Heavy',
    0x28: 'Resist Medium',
    0x32: 'Resist',
    0x64: 'Normal',
    0x7D: 'Weak',
    0x2C01: 'Weak Medium',
    0xE803: 'Drain',
    0xE703: 'Repel',
    0x8403: 'Random'
}
ELEMENT_MAP = {
    0: 'Physical',
    1: 'Fire',
    2: 'Ice',
    3: 'Elec',
    4: 'Force',
    5: 'Light',
    6: 'Dark',
    7: 'Almighty',
    8: 'Poison',
    10: 'Confusion',
    11: 'Charm',
    12: 'Sleep',
    20: 'Mirage',
    29: 'Recovery',
    32: 'Physical'
}
FLAG_MAP = {
    0x2C0000003E01: 'Reaching Shinagawa',
    0x490000008B01: 'Reaching Taito',
    0x60040000E101: 'Defeat Surt / ',
    0x370000006201: 'Shingawa Clear',
    0x69000000A101: 'Got all Empyrean Keys',
    0x6C000000A601: 'Alignment Lock',
    0x210300000000: 'Godborn',
    0x0E000000F500: 'Defeat Hydra',
    0x300000005001: 'Defeat Fionn (Shinagawa)',
    0xFB1F: 'Tsukuyomi Essence Base',
    0xFC1F: 'Tsukuyomi Essence Median',
    0xFD1F: 'Tsukuyomi Essence Ultimus',
    0xE81E: 'Unlock Lucifer'
}

'''
This function translates the id of an item to its name.
    Paramters:
        ind (Number): id of an item
    Returns:
        The name of the item
'''
def translateItem(ind, itemNames):
    return itemNames[ind]
    
'''
INCOMPLETE
Translates the given value of a skill modifier to an understable description of its effect in game.
    Parameters:
        value (Number): the value of the modifier
    Returns:
        The description of the given modifier value
'''
def translateModifier(value):
    if value >= len(SKILL_MODIFIERS):
        return "Not Known Yet"
    else:
        return SKILL_MODIFIERS[value]
        
'''
Gives the name of the skill that has the given id
    Parameters:
        ind (Number): id of the skill
        skillNames (Array): the list of skill names
    Returns:
        The name of the skill of the given id
'''
def translateSkillID(ind, skillNames):
    return skillNames[ind]
    
'''
Returns a text description of the given skill type value.
    Parameters:
        value (Number)
    Returns:
        The text description of the given skill type value.
'''
def translateSkillType(value):
    if value >= len(SKILL_TYPES):
        return ""
    else:
        return SKILL_TYPES[value]
    
'''
Returns a text description of the given skill element value.
    Parameters:
        value (Number)
    Returns:
        The text description of the given skill element value.
'''
def translateSkillElement(value):
    return SKILL_ELEMENTS[value]
    
'''
Returns a text description of the given skill passive resist type value.
    Parameters:
        value (Number)
    Returns:
        The text description of the given given skill passive resist type value.
'''
def translatePassiveResist(value):
    return PASSIVE_RESISTS[value]

'''
Returns a text description of the given skill target value.
    Parameters:
        value (Number)
    Returns:
        The text description of the given skill target value.
'''
def translateTarget(value):
    return SKILL_TARGETS[value]
    
'''
Returns a text description of the given skill potential type value.
    Parameters:
        value (Number)
    Returns:
        The text description of the given skill potential type value.
'''
def translatePotentialType(value):
    return POTENTIAL_TYPES[value]

'''
Translates the number into what type of resist it describes
    Parameters:
        value (Number)
    Returns: 
        The type of resist value describes
'''
def translateResist(value):
    if value in RESIST_MAP:
        return RESIST_MAP[value]
    return ""
    
'''
Returns a text description of the given skill passive element type value.
    Parameters:
        value (Number)
    Returns:
        The text description of the given skill passive element type value.
'''
def translatePassiveElementType(value):
    if value in ELEMENT_MAP:
        return ELEMENT_MAP[value]
    return ""

def translateFlag(value):
    if value in FLAG_MAP:
        return FLAG_MAP[value]
    return ""