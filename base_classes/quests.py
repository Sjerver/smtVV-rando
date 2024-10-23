class Mission:
    def __init__(self):
        self.ind = None
        self.reward = Mission_Reward()
        self.macca = 0
        self.experience = 0
        self.conditions = []
class Mission_Reward:
    def __init__(self, ind=None, amount=None):
        self.ind = ind
        self.amount = amount
class Mission_Condition:
    def __init__(self, type, id, amount):
        self.type = type
        self.ind = id
        self.amount = amount

class Fake_Mission(Mission):
    def __init__(self):
        Mission.__init__(self)
        self.json = None
        self.uasset = None
        self.originalReward = None
        self.script = None

class Mission_Container:
    def __init__(self):
        self.rewardingMissions = []
        self.uniqueRewards = []
        self.creationRewards = []
        self.vengeanceRewards = []