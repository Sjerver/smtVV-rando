class Active_Skill:
    def __init__(self):
        self.ind = None
        self.name = None
        self.offsetNumber = {}
        self.owner = None
        self.cost = None
        self.rank = None
        self.skillType = None
        self.potentialType = None
        self.element = None
        self.skillIcon = None
        self.target = None
        self.minHits = None
        self.maxHits = None
        self.crit = None
        self.power = None
        self.hit = None
        self.ailmentFlags = Ailment_Flags()
        self.healing = Healing_Flags()
        self.pierce = None
        self.ailmentChance = None
        self.buff = Buffs()
        self.resists = Active_Resists()
        self.hpDrain = None
        self.mpDrain = None
        self.magatsuhi = Magatsuhi_Flags()
        self.modifiers = Skill_Modifiers()
        self.conditions = None
        self.animation = None
    
class Passive_Skill:
    def __init__(self):
        self.ind = None
        self.name = None
        self.owner = None
        self.skillType = None
        self.offsetNumber = {}
        self.hpIncrease = None
        self.mpIncrease = None
        self.counterChance = None
        self.survive = None
        self.element = None
        self.resists = Passive_Resists()
        self.effect1 = None
        self.effect1Amount = None
        self.effect2 = None
        self.effect2Amount = None
        
class Passive_Resists:
    def __init__(self):
        self.type = None
        self.physical = None
        self.fire = None
        self.ice = None
        self.elec = None
        self.force = None
        self.dark = None
        self.light = None
     
class Active_Resists:
    def __init__(self):
        self.enable = None
        self.physical = None
        self.fire = None
        self.ice = None
        self.elec = None
        self.force = None
        self.light = None
        self.dark = None
        
class Ailment_Flags:
    def __init__(self):
        self.instakill = None
        self.poison = None
        self.confusion = None
        self.charm = None
        self.sleep = None
        self.seal = None
        self.mirage = None
        self.mud = None
        self.shroud = None
        
class Healing_Flags:
    def __init__(self):
        self.overMaxHP = None
        self.effect = None
        self.flag = None
        self.percent = None
        
class Buffs:
    def __init__(self):
        self.timer = None
        self.physical = None
        self.magical = None
        self.defense = None
        self.accEva = None
        
class Magatsuhi_Flags:
    def __init__(self):
        self.enable = None
        self.race1 = None
        self.race2 = None
        
class Skill_Modifiers:
    def __init__(self):
        self.modifier1 = None
        self.modifier2 = None
        self.modifier3 = None
        self.modifier4 = None
        
class Skill_Condition:
    def __init__(self):
        self.value = None
        self.ailmentCondition = None
        self.effect = None
        self.amount = None
        
class Skill_Conditions:
    def __init__(self, condition1, condition2):
        self.condition1 = condition1
        self.condition2 = condition2
 
class Skill_Level:
    def __init__(self, name, ind, level=[]):
        self.name = name
        self.ind = ind
        self.level = level

class Skill_Owner:
    def __init__(self, ind, name):
        self.name = name
        self.ind = ind
        self.ogName = name
        self.original = ind

class Fusion_Requirements:
    def __init__(self):
        self.offset = None
        self.ind = None
        self.itemID = None
        self.demons = []
        self.alignments = []