class Encounter_Symbol:
    def __init__(self, ind, symbol, offsetNumbers, flags, encounters):
        self.ind = ind
        self.symbol = symbol
        self.offsetNumbers = offsetNumbers
        self.flags = flags
        self.encounters = encounters
        

class Encounter:
    def __init__(self, ind, offsetNumbers, flags, demons):
        self.ind = ind
        self.updated = False
        self.offsetNumbers = offsetNumbers
        self.flags = flags
        self.demons = demons
        
class Possible_Encounter:
    def __init__(self, encounterID, encounter, chance):
        self.encounterID = encounterID
        self.encounter = encounter #This links to the encounter battle where the list of demons is located.
        self.chance = chance

class Event_Encounter:
    def __init__(self):
        self.ind = None
        self.levelpath = None
        self.track = None
        self.demons = None
        self.offsets = {}
        self.unknownDemon = None
        self.unknown23Flag = None