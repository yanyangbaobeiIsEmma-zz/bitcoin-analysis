from bitcoin_lib.encoding import BytesReader, BytesWriter
from .message import Message


class FeeFilterMessage(Message):
    def __init__(self, fee_rate, *, options):
        super().__init__('feefilter', options = options)
        self.fee_rate = fee_rate

    def get_payload(self):
        writer = BytesWriter()
        writer.write_uint64(self.fee_rate)
        return writer.serialize()

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.fee_rate = reader.read_uint64()
        Message.check_finished(reader)
