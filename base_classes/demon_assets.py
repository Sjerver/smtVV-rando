class Asset_Entry:
    def __init__(self):
        self.demonID = None
        self.classAssetID = None
        self.dmAssetID = None
        self.validArea = None
        self.verticalMax = None
        self.horizontalMax = None
        self.tallMax = None
        self.postChips = None

class UI_Entry:
    def __init__(self):
        self.assetID = None
        self.assetString = None
        self.offsetNumber = None

class Position:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    '''
    Scales coordinates by the given Factor.
    '''
    def scale(self,factor):
        self.x = self.x * factor
        self.y = self.y * factor
        self.z = self.z * factor

    '''
    Determines a factor to scale the box so that it fits completely inside this position.
    Parameters:
        box (Position): Position that should fit into this one
    Returns a factor to scale the box to fit into this one
    '''
    def fitIntoBox(self,box):
        strongestFactor = 0
        
        if box.x > self.x:
            strongestFactor = self.x / box.x
        if box.y > self.y and (strongestFactor == 0 or self.y / box.y < strongestFactor):
            strongestFactor = self.y / box.y
        if box.z > self.z and (strongestFactor == 0 or self.z / box.z < strongestFactor):
            strongestFactor = self.z / box.z
        
        return strongestFactor

    '''
    Determines a factor to scale this box so that it stretches the confines of the given box.
    Parameters:
        box (Position): Position to stretch this box to at maximum.
        ignoreY (Boolean): y coordinate can be ignored 
    Returns a factor to scale this box to still fit into the given one
    '''
    def stretchToBox(self,box,ignoreY = False):
        strongestFactor = 0
        if box.x > self.x:
            strongestFactor = box.x / self.x
        if not ignoreY and box.y > self.y and (strongestFactor == 0 or box.y / self.y > strongestFactor):
            strongestFactor = box.y / self.y
        if box.z > self.z and (strongestFactor == 0 or box.z / self.z > strongestFactor):
            strongestFactor = box.z / self.z
        return strongestFactor

    
    

class Talk_Camera_Offset_Entry:
    def __init__(self):
        self.demonID = None
        self.offsetNumber = None
        self.eyeOffset = None
        self.lookOffset = None
        self.dyingOffset = None

class Demon_Model:
    def __init__(self):
        self.modelName = None
        self.animations = []