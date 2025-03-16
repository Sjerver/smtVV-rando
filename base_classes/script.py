from enum import IntEnum, StrEnum
from base_classes.uasset_custom import UAsset_Custom
from util.binary_table import Table

#List of attributes of expressions that contain expressions
SUBEXPRESSION_LIST = ['Value', 'New', 'Expression', 'Variable', 'AssignmentExpression', 'ContextExpression']

class Script_Function_Type(IntEnum):
    IMPORT = 0
    NAME = 1

class Script_Join_Type(StrEnum):
    CODE = ""
    ENTRYDEVILID = 'EntryDevilID'
    ENTRYNKMID = 'EntryNkmID'
    MASAKADO = 'MasakadoId'
    NKMID = 'NkmID'
    MEPHISTO = 'em1769_0721'
    CLEOPATRA = 'em1769_0722'
    DAGDA = 'em1769_0723'

#OUTDATED
class Script_Uasset(UAsset_Custom):
    def __init__(self, binaryTable: Table):
        UAsset_Custom.__init__(self, binaryTable)
    
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
    
class Bytecode:
    def __init__(self,jsonForm):
        self.json = jsonForm
    
    '''
    Returns all occurences of the searched expression in the bytecode.
    Optional are extra things that narrow down the occurences of search expression.
        Parameters:
            searchExpression(String): The expression to search for
            stackNode(Int): optional value for stackNode integer of imported functions
            virtualFunctionName(String): optional name for the name of the virtual function to search for
            localVariable(String): name of a local variable that should be searched for
            instanceVariable(String): name of a instance variable that should be searched for
            structMemberContext(String): name of a member struct variable that should be searched for
            array(String): name of an array variable that should be searched for
            localOutVariable(String): name of a local output variable that should be searched for
        Returns list of occurences of the searched expression in bytecode
    '''
    def findExpressionUsage(self,searchExpression, stackNode = None, virtualFunctionName = None, localVariable = None, instanceVariable = None, structMemberContext = None, array = None, localOutVar = None):
        foundExpressions = []
        
        searchCriteria = { 
            key: value for key, value in {
                "stackNode": stackNode,
                "virtualFunctionName": virtualFunctionName, 
                "localVariable": localVariable,
                "instanceVariable": instanceVariable,
                "structMemberContext": structMemberContext,
                "array": array,
                "localOutVar": localOutVar,
            }.items() if value is not None
        }
        for expression in self.json:
            foundExpressions.extend(self.expressionCheck(expression, searchExpression, searchCriteria))
        return foundExpressions

    '''
    Recursively goes through expression and its subexpression to find occurences of searchExpression.
    Further restrictions to searchExpressions can be added to optional Parameters.
        Parameters:
            expression(Dict): The expression to check and check subexpression of
            searchExpression(String): The expression to search for
            searchCriteria(Dict): dictionary of types and values to search for
        Returns list of occurences of the searched expression in bytecode
    '''
    def expressionCheck(self,expression, searchExpression, searchCriteria = None):
        if not expression or not isinstance(expression, dict):
            #No expression given so return empty list
            return []

        
        if searchCriteria is not None and searchExpression in expression['$type']:
            if "stackNode" in searchCriteria and expression['StackNode'] == searchCriteria["stackNode"]:
                return [expression]
            elif "virtualFunctionName" in searchCriteria and expression['VirtualFunctionName'] == searchCriteria["virtualFunctionName"]:
                return [expression]
            elif "instanceVariable" in searchCriteria and expression["Variable"]["$type"] == "UAssetAPI.Kismet.Bytecode.Expressions.EX_InstanceVariable, UAssetAPI" and expression["Value"]["New"]["Path"][0] == searchCriteria["instanceVariable"]:
                return [expression]
            elif "localVariable" in searchCriteria and expression["Variable"]["$type"] == "UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalVariable, UAssetAPI" and expression["Value"]["New"]["Path"][0] == searchCriteria["localVariable"]:
                return [expression]
            elif "structMemberContext" in searchCriteria and expression["Variable"]["$type"] =="UAssetAPI.Kismet.Bytecode.Expressions.EX_StructMemberContext, UAssetAPI" and expression["Value"]["New"]["Path"][0] == searchCriteria["structMemberContext"]:
                return [expression]
            elif "array" in searchCriteria and expression["AssigningProperty"]["Variable"]["New"]["Path"][0] == searchCriteria["array"]:
                return [expression]
            elif "localOutVar" in searchCriteria and expression["Variable"]["$type"] == "UAssetAPI.Kismet.Bytecode.Expressions.EX_LocalOutVariable, UAssetAPI" and expression["Value"]["New"]["Path"][0] == searchCriteria["localOutVar"]:
                return [expression]
            else:
                foundExpressions = []
                for key in SUBEXPRESSION_LIST:
                    if expression.get(key):
                        foundExpressions.extend(self.expressionCheck(expression.get(key), searchExpression, searchCriteria))
                return foundExpressions
        else:
            #go through potential subexpressions and add all to list and return that
            foundExpressions = []
            for key in SUBEXPRESSION_LIST:
                if expression.get(key):
                    foundExpressions.extend(self.expressionCheck(expression.get(key), searchExpression, searchCriteria))
            return foundExpressions

    '''
    Returns the expression in the main bytecode expression array at the next index from the given expression.
    '''
    def getNextExpression(self,expression):
        index = self.getIndex(expression)
        return self.json[index +1]

    '''
    Returns the index of the expression in the main bytecode expression array.
    '''
    def getIndex(self,expression):
        try:
            index = self.json.index(expression)
        except ValueError:
            foundExp = False
            for index,topExp in enumerate(self.json):
                
                foundExp = self.checkSubExpressions(topExp,expression)
                
                
                if foundExp:
                    break
            if not foundExp:
                index = None
            #Also occurs if lines are already moved around or replaced
            #print("Nested in another expression")
            #return None
        return index

    def checkSubExpressions(self,expression,searchExpression):
        if not expression or not isinstance(expression, dict):
            #No expression given so return empty list
            return False
        if expression == searchExpression:
            return True
        for key in SUBEXPRESSION_LIST:
            subExpression = expression.get(key)
            if self.checkSubExpressions(subExpression, searchExpression):
                return True
        return False

    '''
    Replaces the current expression with the newExpression. If followInserts is given, the expression after is removed and in it's place
    the expressions in that list are inserted.
    '''
    def replace(self, expression, newExpression, followInserts = None):
        try:
            index = self.json.index(expression)
            self.json[index] = newExpression
            if followInserts:
                #self.json.pop(index +1)#Remove pop execution flow as well
                for exp in followInserts:
                    #self.json.insert(index +1,exp)
                    self.json.insert(index +1,exp)
        except ValueError:
            print("Nested in another expression")

class Serialized_Bytecode_Expression:
    def __init__(self,exp, currentSI, nextSI, imp):
        self.exp = exp
        self.currentStatementIndex = currentSI
        self.nextStatementIndex = nextSI
        self.statementLength = nextSI - currentSI
        self.imp = imp