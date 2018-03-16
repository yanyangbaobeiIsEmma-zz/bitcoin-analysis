from bitcoin_lib.encoding import BytesReader, BytesWriter
from .message import Message


class FilterAddMessage(Message):
    def __init__(self, data = b'', *, options):
        super().__init__('filteradd', options = options)
        self.data = data

    def get_payload(self):
        writer = BytesWriter()
        writer.write_var(self.data)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.data = reader.read_var()
        Message.check_finished(reader)
