from bitcoin_lib.encoding import BytesReader, BytesWriter
from .utils import sanitize_start_stop
from .message import Message


class HeadersMessage(Message):
    def __init__(self, headers = [], *, options):
        super().__init__('headers', options = options)
        self.headers = headers

    def get_payload(self):
        writer = BytesWriter()
        writer.write_varint(len(self.headers))
        for header in self.headers:
            writer.write(header.serialize())
            writer.write_uint8(0)

    def set_payload(self, payload):
        reader = BytesReader(payload)
        count = reader.read_varint()
        self.headers = []
        for i in range(count):
            self.headers.append(Header.deserialize(payload))
            transaction_count = reader.read_uint8()
            assert transaction_count == 0
        Message.check_finished(reader)
