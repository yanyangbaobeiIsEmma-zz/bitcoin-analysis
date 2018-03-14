import struct

class BytesWriter:
    def __init__(self):
        self.buffer = []

    def serialize(self):
        return b''.join(self.buffer)

    def write(self, data):
        self.buffer.append(data)

    def write_var(self, data):
        self.write_varint(len(data))
        self.write(data)

    def write_int8(self, n):
        self.buffer.append(struct.pack('b', n))

    def write_uint8(self, n):
        self.buffer.append(struct.pack('B', n))

    def write_int16(self, n, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        self.buffer.append(struct.pack(indicator + 'h', n))

    def write_uint16(self, n, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        self.buffer.append(struct.pack(indicator + 'H', n))

    def write_int32(self, n, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        self.buffer.append(struct.pack(indicator + 'i', n))

    def write_uint32(self, n, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        self.buffer.append(struct.pack(indicator + 'I', n))

    def write_int64(self, n, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        self.buffer.append(struct.pack(indicator + 'q', n))

    def write_uint64(self, n, *, big_endian = False):
        indicator = {False: '<', True: '>'}[big_endian]
        self.buffer.append(struct.pack(indicator + 'Q', n))

    def write_varint(self, n):
        if n < 0xfd:
            self.buffer.append(struct.pack('B', n))
        elif n < 1 << 16:
            self.buffer.append(struct.pack('<BH', 0xfd, n))
        elif n < 1 << 32:
            self.buffer.append(struct.pack('<BI', 0xfe, n))
        else:
            self.buffer.append(struct.pack('<BQ', 0xff, n))
