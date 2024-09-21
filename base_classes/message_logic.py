from base_classes.uasset import UAsset
from util.binary_table import Table
from base_classes.script_logic import readBinaryTable, writeBinaryTable, writeFolder

class Message_Uasset(UAsset):
    def __init__(self, binaryTable: Table):
        UAsset.__init__(self, binaryTable)
