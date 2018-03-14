from bitcoin_lib.encoding import BytesReader, BytesWriter
from .utils import sanitize_start_stop
from .message import Message


class GetBlocksMessage(Message):
    def __init__(self, arg = {}, *, options):
        super().__init__('getblocks', options = options)
        self.version = options.protocol_version
        arg = sanitize_start_stop(arg)
        self.starts = arg.starts
        self.stop = arg.stop

    def get_payload(self):
        writer = BytesWriter()
        writer.write_uint32(self.version)
        writer.write_varint(len(self.starts))
        for start in self.starts:
            writer.write(start)
        writer.write(stop)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.version = reader.read_uint32()
        start_count = reader.read_varint()
        self.starts = []
        for i in range(start_count):
            self.starts.append(reader.read(32))
        self.stop = reader.read(32)
        Message.check_finished(reader)
