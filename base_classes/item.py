from enum import Enum
from util.numbers import COMBINED_MACCA_AREA_RANGES, ESSENCE_MAP_SCALING, CONSUMABLE_MAP_SCALING, RELIC_MAP_SCALING
from base_classes.demons import Compendium_Demon

'''
Build a map that goes itemID -> allowed areas.
'''
def buildConsumableAllowedAreas(consumableMapScaling):
    itemAllowedAreas = {}

    for area, itemIDs in consumableMapScaling.items():
        for itemID in itemIDs:
            if itemID not in itemAllowedAreas:
                itemAllowedAreas[itemID] = []
            itemAllowedAreas[itemID].append(area)

    return itemAllowedAreas

CONSUMABLE_ALLOWED_AREAS = buildConsumableAllowedAreas(CONSUMABLE_MAP_SCALING)
RELIC_ALLOWED_AREAS = buildConsumableAllowedAreas(RELIC_MAP_SCALING)


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
        self.setMsgID = None

class Reward_Item:
    def __init__(self, ind, amount):
        self.ind = ind
        self.amount = amount
        
class Item_Chest:
    def __init__(self):
        self.map = None
        self.offsetNumber = {}
        self.chestID = None
        self.item = None
        self.amount = None
        self.macca = None

class Consumable_Item:
    def __init__(self):
        self.ind = None
        self.buyPrice = None
        self.offset = None
        self.name = None

class Vending_Machine:
    def __init__(self):
        self.offset = None
        self.area = None
        self.ind = None
        self.relicID = None
        self.items = []

class Vending_Machine_Item:
    def __init__(self):
        self.ind = None
        self.amount = None
        self.rate = None
        self.name = ""

class Gift_Item:
    def __init__(self):
        self.script = None
        self.item = None

class Gift_Pool:
    def __init__(self):
        self.uniqueRewards = []
        self.allGifts = []

class Check_Type(Enum):
    TREASURE = 0
    MIMAN = 1
    MISSION = 2
    GIFT = 3
    VENDING_MACHINE = 4
    BASIC_ENEMY_DROP = 5
    BOSS_DROP = 6

    @staticmethod
    def getCheckType(stringValue):
        match stringValue:
            case "NPC/Story Gifts":
                return Check_Type.GIFT
            case "Miman Rewards":
                return Check_Type.MIMAN
            case "Treasures":
                return Check_Type.TREASURE
            case "Mission Rewards":
                return Check_Type.MISSION
            case "Vending Machines":
                return Check_Type.VENDING_MACHINE
            case "Basic Enemy Drops":
                return Check_Type.BASIC_ENEMY_DROP
            case "Boss Drops":
                return Check_Type.BOSS_DROP

    @staticmethod
    def getCheckString(Check_Type):
        match Check_Type:
            case Check_Type.GIFT:
                return "NPC/Story Gifts"
            case Check_Type.MIMAN:
                return "Miman Rewards"
            case Check_Type.TREASURE:
                return "Treasures"
            case Check_Type.MISSION:
                return "Mission Rewards"
            case Check_Type.VENDING_MACHINE:
                return "Vending Machines"
            case Check_Type.BASIC_ENEMY_DROP:
                return "Basic Enemy Drops"
            case Check_Type.BOSS_DROP:
                return "Boss Drops"

class Item_Check:
    def __init__(self, type, ind, name, area, repeatable = False, missable = False, duplicate = False, maxAdditionalItems = 0, hasOdds = False, odds = []):
        self.type = type
        self.ind = ind
        self.name = name
        self.area = area
        
        self.item = None
        self.vanillaItem = None
        self.vanillaAdditionalItems = []
        self.additionalItems = []
        self.maxAdditionalItems = maxAdditionalItems
        self.originalMaxAddItems = maxAdditionalItems

        self.maxItemQuantity = 999999999999
        if type in [Check_Type.BASIC_ENEMY_DROP,Check_Type.BOSS_DROP]:
            self.maxItemQuantity = 1

        self.repeatable = repeatable
        self.missable = missable
        self.hasDuplicate = duplicate

        self.allowedCanons = []
        if type in [Check_Type.TREASURE,Check_Type.MISSION]:
            self.maccaAllowed = True
        else:
            self.maccaAllowed = False
        
        self.validItemAmount = 0

        self.hasOdds = hasOdds
        self.odds = odds


    '''
    Input the item as a vanilla item to the check.
    '''
    def inputVanillaItem(self, item):
        #We do not check if the item is allowed since this only represents the vanilla state which may break our rules
        if self.vanillaItem == None:
            self.vanillaItem = item
        elif len(self.vanillaAdditionalItems) < self.maxAdditionalItems:
            self.vanillaAdditionalItems.append(item)
        else:
            return False
        return True
    
    '''
    Checks if the item can be in the check and adds it to the check if possible.
        Parameters:
            item(Base_Item): the item in question
            forced(Boolean): if the item is forced into the main slot, ignoring everything else
    Returns whether the item can be assigned to the check.
    '''
    def inputItem(self,item, forced = False):
        if forced:
            self.item = item
            return True
        if item.itemAllowedInCheck(self):
            if self.item == None:
                self.item = item
            elif len(self.additionalItems) < self.maxAdditionalItems:
                self.additionalItems.append(item)
            else:
                return False
            return True
        return False

    '''
    Returns whether another item can be assigned to the check.
    '''
    def isFull(self):
        if self.item == None:
            return False
        elif len(self.additionalItems) < self.maxAdditionalItems:
            return False
        else:
            return True 

class Base_Item():
    def __init__(self,name, amount,allowedAreas = []):
        self.amount = amount
        self.name = name
        self.allowedAreas = allowedAreas
        self.validChecks = []

    '''
    Returns true if the item is allowed in the check.
    '''
    def itemAllowedInCheck(self,check):
        if check.isFull():
            return False
        if self.amount > check.maxItemQuantity:
            return False
        if len(self.allowedAreas) == 0:
            return True
        for area in self.allowedAreas:
            if area == check.area:
                return True
        return False
    
    '''
    For the given list of checks: add the checks to validChecks and increase the validItemAmount inside checks if this item could be assigned to the check.
    '''
    def calculateValidChecks(self,checkList):
        self.validChecks = []
        for check in checkList:
            if self.itemAllowedInCheck(check):
                self.validChecks.append(check)
                check.validItemAmount += 1

class Macca_Item(Base_Item):
    def __init__(self, amount,allowedAreas = [], scaling = False):
        super().__init__("Macca " + str(amount), amount, allowedAreas)
        self.ind = 0 #Macca ind is always 0, because it is just easier to handle for most things
        if scaling:
            self.allowedAreas = self.calculateAllowedAreasForMacca(self.amount)

    '''
    Returns true if the item is allowed in the check.
    '''
    def itemAllowedInCheck(self,check):
            if self.amount > check.maxItemQuantity:
                return False
            #Macca cannot have more than one reward
            if check.maxAdditionalItems > 0:
                return False
            if check.maccaAllowed: #Additionally macca needs to be allowed in the check
                if len(self.allowedAreas) == 0:
                    return True
                for area in self.allowedAreas:
                    if area == check.area:
                        return True
                return False
            return False
    
    '''
    Returns a list of areas this macca amount is allowed in.
    '''
    def calculateAllowedAreasForMacca(self,amount):
        allowed = set()

        for table in COMBINED_MACCA_AREA_RANGES.values():
            for area, (low, high) in table.items():
                if low <= amount <= high:
                    allowed.add(area)

        return list(allowed)

class Key_Item(Base_Item):
    def __init__(self, name, ind, allowedAreas = []):
        super().__init__(name, 1, allowedAreas)
        self.ind = ind
        self.hasBeenDuplicated = False
        self.allowedCheckTypes = []
        

    '''
    Returns true if the item is allowed in the check.
    '''
    def itemAllowedInCheck(self,check):
        if self.amount > check.maxItemQuantity:
            return False
        #Do not allow missable or canon-exclusive 
        if check.missable or len(check.allowedCanons) > 0:
            return False
        #Do not allow checks with more than one item
        if (check.hasOdds and check.item != None) or (not check.hasOdds and check.maxAdditionalItems > 0):
            return False
        #If we have a check type limitation follow it
        if len(self.allowedCheckTypes) > 0 and check.type not in self.allowedCheckTypes:
            return False
        if len(self.allowedAreas) == 0:
            return True
        for area in self.allowedAreas:
            if area == check.area:
                return True
        return False

class Essence_Item(Base_Item):
    def __init__(self,name,ind, demon: Compendium_Demon, scaling= False, allowedAreas = [], allowRepeatable = False):
        super().__init__(name, 1, allowedAreas)
        self.demon = demon
        self.ind = ind
        self.allowRepeatable = allowRepeatable
        if scaling:
            self.allowedAreas = self.calculateAllowedAreasForLevel()
        else:
            self.allowedAreas = allowedAreas
    
    '''
    Returns true if the item is allowed in the check.
    '''
    def itemAllowedInCheck(self,check):
        if self.amount > check.maxItemQuantity:
            return False
        if not self.allowRepeatable and check.repeatable:
            return False
        if len(self.allowedAreas) == 0:
            return True
        for area in self.allowedAreas:
            if area == check.area:
                return True
        return False

    '''
    Calculates the allowed areas based on the level of the corresponding demon.
    '''
    def calculateAllowedAreasForLevel(self):
        allowed = []
        level = self.demon.level.value
        for area, (low, high) in ESSENCE_MAP_SCALING.items():
            if low <= level <= high:
                allowed.append(area)
        return allowed



class Generic_Item(Base_Item):
    def __init__(self, name, ind, amount, scaling = False, allowedAreas = [], allowRepeatable = False):
        super().__init__(name, amount, allowedAreas)
        self.ind = ind
        self.allowRepeatable = allowRepeatable
        if scaling:
            self.allowedAreas = CONSUMABLE_ALLOWED_AREAS.get(ind, [])

    '''
    Returns true if the item is allowed in the check.
    '''
    def itemAllowedInCheck(self,check):
        if self.amount > check.maxItemQuantity:
            return False
        if not self.allowRepeatable and check.repeatable:
            return False
        if len(self.allowedAreas) == 0:
            return True
        for area in self.allowedAreas:
            if area == check.area:
                return True
        return False
    
class Relic_Item(Base_Item):
    def __init__(self,name,ind, amount,scaling = False,allowedAreas = []):
        super().__init__(name, amount, allowedAreas)
        self.ind = ind
        if scaling:
            self.allowedAreas = RELIC_ALLOWED_AREAS.get(ind, [])

    '''
    Returns true if the item is allowed in the check.
    '''
    def itemAllowedInCheck(self,check):
        if self.amount > check.maxItemQuantity:
            return False
        if len(self.allowedAreas) == 0:
            return True
        for area in self.allowedAreas:
            if area == check.area:
                return True
        return False


    
