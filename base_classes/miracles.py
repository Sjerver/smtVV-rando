class Abscess(object):
    def __init__(self):
        self.offsetNumber = {}
        self.encounter = None
        self.eventEncounter = None
        self.miracles = []
        
class Miracle(object):
    def __init__(self, offsetNumber, cost):
        self.offsetNumber = offsetNumber
        self.cost = cost