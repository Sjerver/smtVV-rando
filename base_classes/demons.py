class Compendium_Demon:
    def __init__(self):
        self.ind = None
        self.name = None
        self.offsetNumbers = {}
        self.race = None
        self.level = None
        self.registerable = None
        self.fusability = None
        self.unlockFlags = []
        self.tone = None
        self.resist = Affinities()
        self.potential = Potentials()
        self.stats = None
        self.innate = None
        self.skills = []
        self.learned_skills = []
    
class Enemy_Demon:
    def __init__(self):
        self.ind = None
        self.name = None
        self.offsetNumbers = {}
        self.level = None
        self.stats = None
        self.statMods = None
        self.analyze = None
        self.levelDMGCorrection = None
        self.AI = None
        self.recruitable = None
        self.pressTurns = None
        self.experience = None
        self.money = None
        self.skills = []
        self.drops = None
        self.innate = None
        self.resist = Affinities()
        self.potential = Potentials()
        
class Affinities:
    def __init__(self):
        self.physical = None
        self.fire = None
        self.ice = None
        self.electric = None
        self.force = None
        self.light = None
        self.dark = None
        self.almighty = None
        self.poison = None
        self.confusion = None
        self.charm = None
        self.sleep = None
        self.seal = None
        self.mirage = None
        
class Potentials:
    def __init__(self):
        self.physical = None
        self.fire = None
        self.ice = None
        self.elec = None
        self.force = None
        self.light = None
        self.dark = None
        self.almighty = None
        self.ailment = None
        self.recover = None
        self.support = None
        
class Stat:
    def __init__(self, start, growth, og):
        self.start = start
        self.growth = growth
        self.og = og
        
class Stats:
    def __init__(self, HP, MP, strength, vit, mag, agi, luk):
        self.HP = HP
        self.MP = MP
        self.str = strength
        self.vit = vit
        self.mag = mag
        self.agi = agi
        self.luk = luk
        
class Item_Drops:
    def __init__(self, item1, item2, item3):
        self.item1 = item1
        self.item2 = item2
        self.item3 = item3
        
class Item_Drop:
    def __init__(self, value, translation, chance, quest):
        self.value = value
        self.translation = translation
        self.chance = chance
        self.quest = quest
        
class Demon_Level:
    def __init__(self, value, original):
        self.value = value
        self.original = original