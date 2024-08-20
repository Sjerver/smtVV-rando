class Essence:
    def __init__(self):
        self.demon = None
        self.price = None
        self.offset = None
        self.name = None
        self.ind = None

class Shop_Entry:
    def __init__(self):
        self.item = None
        self.unlock = None
        self.offset = None

class Miman_Reward:
    def __init__(self):
        self.items = []
        self.miman = None
        self.offset = None

class Reward_Item:
    def __init__(self):
        self.item = None
        self.amount = None
        
class Item_Chest:
    def __init__(self):
        self.map = None
        self.offsetNumber = {}
        self.chestID = None
        self.item = None
        self.amount = None
        self.macca = None