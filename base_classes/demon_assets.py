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

class Talk_Camera_Offset_Entry:
    def __init__(self):
        self.demonID = None
        self.offsetNumber = None
        self.eyeOffset = None
        self.lookOffset = None
        self.dyingOffset = None