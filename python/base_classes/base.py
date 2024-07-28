class Translated_Value:
    def __init__(self, value, translation, level=None, secondary=None):
        self.value = value
        self.translation = translation
        self.level = level
        self.secondary = secondary
        self.ind = value
        
class Weight_List:
    def __init__(self, values, weights, names):
        self.values = values
        self.weights = weights
        self.names = names