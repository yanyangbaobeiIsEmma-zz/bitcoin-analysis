from enum import Enum
from bitcoin_lib.encoding import BytesReader, BytesWriter


class Inventory:
    class Type(Enum):
        ERROR = 0
        TX = 1
        BLOCK = 2
        FILTERED_BLOCK = 3
        CMPCT_BLOCK = 4

    def __init__(inv_type, data):
        self.type = inv_type
        self.data = data

    @staticmethod
    def for_item(inv_type, data):
        if isinstance(data, str):
            data = data.encode()[::-1]
        return Inventory(inv_type, data)

    @staticmethod
    def for_transaction(data):
        return Inventory.for_item(Inventory.Type.TX, data)

    @staticmethod
    def for_block(data):
        return Inventory.for_item(Inventory.Type.BLOCK, data)

    @staticmethod
    def for_filtered_block(data):
        return Inventory.for_item(Inventory.Type.FILTERED_BLOCK, data)

    def serialize(self):
        writer = BytesWriter()
        writer.write_uint32(self.type)
        writer.write(self.data)
        return writer.serialize()

    @staticmethod
    def deserialize(reader):
        inv_type = reader.read_uint32()
        data = reader.read(32)
        return Inventory(inv_type, data)
