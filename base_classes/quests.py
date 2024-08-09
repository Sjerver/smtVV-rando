class Mission:
    def __init__(self):
        self.ind = None
        self.reward = Mission_Reward()
        self.macca = 0
        self.conditions = []
class Mission_Reward:
    def __init___(self, ind, amount):
        self.ind = ind
        self.amount = amount
class Mission_Condition:
    def __init__(self, type, id, amount):
        self.type = type
        self.ind = id
        self.amount = amount