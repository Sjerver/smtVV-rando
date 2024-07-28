from base_classes.demons import Affinities

class Nahobino:
    def __init__(self):
        self.startingSkill = None
        self.resist = Affinities()
        self.stats = []
        self.offsetNumbers = {}

class LevelStats:
    def __init__(self, level, HP, MP, strength, vit, mag, agi, luk):
        self.level = level
        self.HP = HP
        self.MP = MP
        self.str = strength
        self.vit = vit
        self.mag = mag
        self.agi = agi
        self.luk = luk