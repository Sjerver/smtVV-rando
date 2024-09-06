class Encounter_Symbol:
    def __init__(self, ind, symbol, offsetNumbers, flags, encounters):
        self.ind = ind
        self.symbol = symbol
        self.offsetNumbers = offsetNumbers
        self.flags = flags
        self.encounters = encounters
        

class Encounter:
    def __init__(self, ind, offsetNumbers, flags, track, demons):
        self.ind = ind
        self.updated = False
        self.offsetNumbers = offsetNumbers
        self.flags = flags
        self.track = track
        self.demons = demons
        self.positions = EventEncountPost()
        
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
        self.originalIndex = None
        self.positions = EventEncountPost()
        self.endEarlyFlag = None
        
    '''
    Tests if two encounters share identical demons, usually due to VR battles
        Parameters:
            other(Event_Encounter): The encounter to compare demons to
        Returns:
            True if all demons are identical between the two encounters, False otherwise.
    '''
    def compareDemons(self, other):
        for index, demon in enumerate(self.demons):
            if demon.value != other.demons[index].value:
                return False
        return True

class Battle_Event:
    def __init__(self, encounterID, offset):
        self.offset = offset
        self.encounterID = encounterID
        self.referenceID = -1

class EventEncountPost:
    def __init__(self):
        self.demons = []
        self.addDemons = []
        self.offsetNumber = None

class Unique_Symbol_Encounter(object):
    def __init__(self):
        self.ind = None
        self.offsetNumber = {}
        self.encounterID = None
        self.eventEncounterID = None
        self.symbol = None
        
class Mixed_Boss_Encounter(object):
    def __init__(self):
        self.ind = None
        self.isEvent = False
        self.normalEncounter = None
        self.eventEncounter = None
        self.demons = None
        self.track = None