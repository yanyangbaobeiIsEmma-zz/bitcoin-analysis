from enum import Enum
from bitcoin_lib.encoding import BytesReader, BytesWriter
from .message import Message


class RejectMessage(Message):
    def __init__(self, arg = {}, *, options):
        super().__init__('reject', options = options)
        self.message = arg.get('message')
        self.code = arg.get('code')
        self.reason = arg.get('reason')
        self.data = arg.get('data')

    def get_payload(self):
        writer = BytesWriter()
        writer.write_var(self.message.encode())
        writer.write_uint8(self.code)
        writer.write_var(self.reason.encode())
        writer.write(self.data)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.message = reader.read_var()
        self.code = reader.read_uint8()
        self.reason = reader.read_var()
        self.data = reader.read_all()

    class Code(Enum):
        REJECT_MALFORMED = 0x01
        REJECT_INVALID = 0x10
        REJECT_OBSOLETE = 0x11
        REJECT_DUPLICATE = 0x12
        REJECT_NONSTANDARD = 0x40
        REJECT_DUST = 0x41
        REJECT_INSUFFICIENTFEE = 0x42
        REJECT_CHECKPOINT = 0x43
