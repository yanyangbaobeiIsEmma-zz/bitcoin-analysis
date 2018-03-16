from datetime import datetime
import time
from bitcoin_lib.encoding import BytesReader, BytesWriter
from .utils import get_nonce, read_address, write_address
from .message import Message


class VersionMessage(Message):
    def __init__(self, arg = {}, *, options):
        super().__init__('version', options = options)
        self.version = arg.get('version', options.get('protocol_version'))
        self.nonce = arg.get('nonce', get_nonce())
        self.services = arg.get('services', 13)
        self.timestamp = arg.get('timestamp', datetime.fromtimestamp(time.time()))
        self.subversion = arg.get('subversion', '/bitcoin_analysis:0.0.1/')
        self.start_height = arg.get('start_height', 0)
        self.relay = arg.get('relay', True)
        self.my_address = {}
        self.your_address = {}

    def get_payload(self):
        writer = BytesWriter()
        writer.write_int32(self.version)
        writer.write_uint64(self.services)
        writer.write_uint64(int(self.timestamp.timestamp()))
        write_address(writer, self.my_address)
        write_address(writer, self.your_address)
        writer.write(self.nonce)
        writer.write_var(self.subversion.encode('ascii'))
        writer.write_uint32(self.start_height)
        writer.write_uint8(+self.relay)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.version = reader.read_int32()
        self.services = reader.read_uint64()
        self.timestamp = datetime.fromtimestamp(reader.read_uint64())
        self.my_address = read_address(reader)
        self.your_address = read_address(reader)
        self.nonce = reader.read(8)
        self.subversion = reader.read_var().decode('ascii')
        self.start_height = reader.read_uint32()
        self.relay = reader.finished or not reader.read_uint8()
        Message.check_finished(reader)
