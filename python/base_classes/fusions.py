class Normal_Fusion:
    def __init__(self, offsetNumbers, firstDemon, secondDemon, result):
        self.offsetNumbers = offsetNumbers
        self.firstDemon = firstDemon
        self.secondDemon = secondDemon
        self.result = result
        
class Fusion_Chart_Node:
    def __init__(self, offset, race1, race2, result):
        self.offset = offset
        self.race1 = race1
        self.race2 = race2
        self.result = result
        
class Special_Fusion:
    def __init__(self):
        self.ind = None
        self.resultLevel = None
        self.baseOffset = None
        self.demon1 = None
        self.demon2 = None
        self.demon3 = None
        self.demon4 = None
        self.result = None