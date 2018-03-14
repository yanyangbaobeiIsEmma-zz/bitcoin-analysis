from bitcoin_lib.encoding import BytesReader, BytesWriter
from .message import Message


class AlertMessage(Message):
    def __init__(self, arg = {}, *, options):
        super().__init__('alert', options = options)
        self.payload = arg.get('payload', bytes([0] * 32))
        self.signature = arg.get('payload', bytes([0] * 32))

    def get_payload(self):
        writer = BytesWriter()
        writer.write_var(self.payload)
        writer.write_var(self.signature)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.payload = reader.read_var()
        self.signature = reader.read_var()
        Message.check_finished(reader)
