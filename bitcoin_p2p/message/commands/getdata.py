from bitcoin_lib.encoding import BytesReader, BytesWriter
from .message import Message


class GetDataMessage(Message):
    def __init__(self, inventories, *, options):
        super().__init__('getdata', options = options)
        self.inventories = inventories

    def get_payload(self):
        writer = BytesWriter()
        write_inventories(writer, self.inventories)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        count = reader.read_varint()
        self.inventories = []
        for i in range(count):
            type = reader.read_uint32()
            hash = reader.read(32)
            self.inventories.append({'type': type, 'hash': hash})
        Message.check_finished(reader)
