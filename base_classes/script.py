from enum import IntEnum
from base_classes.uasset import UAsset
from util.binary_table import Table

class Script_Function_Type(IntEnum):
    IMPORT = 0
    NAME = 1

class Script_Uasset(UAsset):
    def __init__(self, binaryTable: Table):
        UAsset.__init__(self, binaryTable)
    
    '''
    Returns a list of offsets for all function calls in uexp of the given function where the specified parameter is passed.
        Parameter:
            uexp (Table): the uexp binary data where the function calls are searched in
            functionName (String): the name of the function to search for
            type (Script_Function_Type): in which mapping the functions id is located in
            paramNumber (Integer): which parameter of the function call to return the offset off
            bonusBytes (Integer): extra bytes to add on the offset
        Returns a list of offsets where the specified parameter is in a call of the function
    '''    
    def getOffsetsForParamXFromFunctionCalls(self, uexp: Table, functionName, type, paramNumber, bonusBytes = 0):
        additionalBytes = paramNumber * 5 + bonusBytes
        
        result = []

        #TODO: Decide if it's fine like this or remove type and just check import first and then names
        if type == Script_Function_Type.NAME and functionName in self.nameMap.keys():
            additionalBytes = additionalBytes + 4
            functionIndex = self.nameMap[functionName]
        elif type == Script_Function_Type.IMPORT and functionName in self.reverseImportMap.keys():
            functionIndex = self.reverseImportMap[functionName]
        else:
            return result
        
        result = uexp.findWordOffsets(functionIndex)

        for index, value in enumerate(result):
            result[index] = result[index] + additionalBytes
        return result
    
    '''
    Returns a list of offsets for all rows in the data table in the uexp where the given nameEntry appears.
        Parameter:
            uexp (Table): the uexp binary data where the nameEntry is searched in
            nameEntry (String): the name of a nameEntry to search for
            type (Script_Function_Type): in which mapping the functions id is located in
            bonusBytes (Integer): How many bytes later the desired column value is stored
        Returns a list of offsets where the specified parameter is in a call of the function
    '''  
    def getOffsetsForRowInNPCDataTable(self, uexp: Table, nameEntry,type , bonusBytes = 0):
        additionalBytes = bonusBytes
        
        result = []

        #TODO: Decide if it's fine like this or remove type and just check import first and then names
        if type == Script_Function_Type.NAME and nameEntry in self.nameMap.keys():
            functionIndex = self.nameMap[nameEntry]
        elif type == Script_Function_Type.IMPORT and nameEntry in self.reverseImportMap.keys():
            functionIndex = self.reverseImportMap[nameEntry]
        else:
            return result
        
        result = uexp.findWordOffsets(functionIndex)

        for index, value in enumerate(result):
            result[index] = result[index] + additionalBytes
        return result