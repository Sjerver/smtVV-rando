import struct
from io import BytesIO

# Wrapper class around low level reads/writes
# code modified from https://github.com/samfin/mmbn3-random/tree/cleanup
class Table(object):
    def __init__(self, table_file_path):
        self.buffer = bytearray(self.loadFile(table_file_path).read())
        self.w_offset = 0
        self.r_offset = 0
        self.stack = []

    def seekr(self, offset):
        self.r_offset = offset
    def seekw(self, offset):
        self.w_offset = offset
    def seek(self, offset):
        self.seekr(offset)
        self.seekw(offset)
    def saveOffsets(self):
        self.stack.append((self.r_offset, self.w_offset))
    def loadOffsets(self):
        self.r_offset, self.w_offset = self.stack.pop()

    # Generally, providing an offset = don't change the state
    # Not providing an offset = use the stored offset and increment it
    # Also changes the write offset, careful!!
    def read(self, n, offset = -1):
        if offset == -1:
            offset = self.r_offset
            self.w_offset = self.r_offset
            self.r_offset += n
        assert(offset >= 0)
        # assert(offset + n <= len(self.rom_data))
        # return self.rom_data[offset : offset + n]
        assert(offset + n <= len(self.buffer))
        return self.buffer[offset : offset + n]

    def readByte(self, offset = -1):
        return ord(self.read(1, offset))
    def readHalfword(self, offset = -1):
        return struct.unpack('<h', self.read(2, offset))[0]
    def readWord(self, offset = -1):
        return struct.unpack('<i', self.read(4, offset))[0]
    def readDblword(self, offset = -1):
        return struct.unpack('<q', self.read(8, offset))[0]
    def read32chars(self, offset = -1):
        return struct.unpack('32s', self.read(32, offset))[0]
    def readFloat(self, offset = -1):
        return struct.unpack('<f', self.read(4, offset))[0]
    def readXChars(self, x, offset = -1):
        return struct.unpack(str(x) + 's', self.read(x, offset))[0]
    def readUnsignedWord(self, offset = -1):
        return struct.unpack('<I', self.read(4, offset))[0]

    def write(self, data, offset = -1):
        if offset == -1:
            offset = self.w_offset
            self.w_offset += len(data)
        assert(offset >= 0)
        # assert(offset + len(data) <= len(self.rom_data))
        assert(offset + len(data) <= len(self.buffer))
        for i in range(len(data)):
            self.buffer[offset + i] = data[i]

    def writeByte(self, x, offset = -1):
        return self.write(struct.pack('<B', x), offset)
    def writeHalfword(self, x, offset = -1):
        return self.write(struct.pack('<h', x), offset)
    def writeWord(self, x, offset = -1):
        return self.write(struct.pack('<i', x), offset)
    def writeUnsignedWord(self, x, offset = -1):
        return self.write(struct.pack('<I', x), offset)
    def writeDblword(self, x, offset = -1):
        return self.write(struct.pack('<q', x), offset)
    def write32chars(self, x, offset = -1):
        return self.write(struct.pack('32s', x), offset)
    def writeFloat(self, x, offset = -1):
        return self.write(struct.pack('<f', x), offset)
    def writeXChars(self, toWrite, x, offset = -1):
        return self.write(struct.pack(str(x) + 's', toWrite), offset)
    
    def loadFile(self, file_path):
        return open(file_path, 'rb')
    
    '''
    Finds all occurences of the given word (4 bytes) in the tables buffer.
        Parameter:
            word (Integer): 4 byte word as integer form
        Returns the offsets where the word is in found in the table buffer
    '''
    def findWordOffsets(self, word):
        result = []
        searchBytes = struct.pack('<i', word)
        currentOffset = 0
        while self.buffer.find(searchBytes, currentOffset) != -1:
            offset = self.buffer.find(searchBytes, currentOffset)
            currentOffset = offset +1

            result.append(offset)
        return result

    '''
    Reads characters until an empty byte is encountered including the empty byte.
    '''
    def readUntilEmptyByte(self,offset):
        searchBytes = struct.pack('c', b'\x00')
        endOfString = self.buffer.find(searchBytes, offset)
        length = endOfString - offset +1
        return self.readXChars(length, offset)

