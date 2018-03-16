from bitcoin.bloom import CBloomFilter as BloomFilter
from bitcoin_lib.encoding import BytesReader, BytesWriter
from .message import Message


class FilterLoadMessage(Message):
    def __init__(self, filter = None, *, options):
        super().__init__('filteradd', options = options)
        self.filter = filter

    def get_payload(self):
        return self.filter and self.filter.stream_serialize() or b''

    def set_payload(self, payload):
        self.filter = BloomFilter.stream_deserialize(payload)
