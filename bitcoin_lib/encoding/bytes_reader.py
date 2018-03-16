import struct

class BytesReader:
    def __init__(self, data):
        self.data = data
        self.position = 0

    def read(self, length):
        result = self.data[self.position : self.position + length]
        self.position += length
        return result

    def read_all(self):
        result = self.data[self.position:]
        self.position = len(self.data)
        return result

    def read_var(self):
        length = self.read_varint()
        return self.read(length)

    def read_int8(self):
        result = struct.unpack_from('b', self.data, self.position)[0]
        self.position += 1
        return result

    def read_uint8(self):
        result = struct.unpack_from('B', self.data, self.position)[0]
        self.position += 1
        return result

    def read_int16(self, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        result = struct.unpack_from(indicator + 'h', self.data, self.position)[0]
        self.position += 2
        return result

    def read_uint16(self, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        result = struct.unpack_from(indicator + 'H', self.data, self.position)[0]
        self.position += 2
        return result

    def read_int32(self, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        result = struct.unpack_from(indicator + 'i', self.data, self.position)[0]
        self.position += 4
        return result

    def read_uint32(self, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        result = struct.unpack_from(indicator + 'I', self.data, self.position)[0]
        self.position += 4
        return result

    def read_int64(self, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        result = struct.unpack_from(indicator + 'q', self.data, self.position)[0]
        self.position += 8
        return result

    def read_uint64(self, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        result = struct.unpack_from(indicator + 'Q', self.data, self.position)[0]
        self.position += 8
        return result

    def read_varint(self):
        first = struct.unpack_from('B', self.data, self.position)[0]
        self.position += 1
        if first < 0xfd:
            return first
        elif first == 0xfd:
            result = struct.unpack_from('<H', self.data, self.position)[0]
            self.position += 2
            return result
        elif first == 0xfe:
            result = struct.unpack_from('<I', self.data, self.position)[0]
            self.position += 4
            return result
        else:
            result = struct.unpack_from('<Q', self.data, self.position)[0]
            self.position += 8
            return result

    @property
    def finished(self):
        return self.position >= len(self.data)
