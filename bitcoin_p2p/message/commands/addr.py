from datetime import datetime
from bitcoin_lib.encoding import BytesReader, BytesWriter
from .utils import read_address, write_address
from .message import Message


class AddrMessage(Message):
    def __init__(self, addresses = [], *, options):
        super().__init__('addr', options = options)
        self.addresses = addresses

    def get_payload(self):
        writer = BytesWriter()
        writer.write_varint(len(self.addresses))
        for address in self.addresses:
            writer.write_uint32(int(address['time'].timestamp()))
            write_address(writer, address)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        address_count = reader.read_varint()
        self.addresses = []
        for i in range(address_count):
            time = datetime.fromtimestamp(reader.read_uint32())
            address = read_address(reader)
            address['time'] = time
            self.addresses.append(address)
        Message.check_finished(reader)
