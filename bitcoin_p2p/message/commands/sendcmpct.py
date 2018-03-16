from bitcoin_lib.encoding import BytesReader, BytesWriter
from .message import Message


class SendCmpctMessage(Message):
    def __init__(self, *, options):
        super().__init__('sendcmpct', options = options)
        self.use_compact_block = False
        self.compact_block_version = 0

    def get_payload(self):
        writer = BytesWriter()
        writer.write_uint8(+self.use_compact_block)
        writer.write_uint64(self.compact_block_version)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.use_compact_block = bool(reader.read_uint8())
        self.compact_block_version = reader.read_uint64()
        Message.check_finished(reader)
