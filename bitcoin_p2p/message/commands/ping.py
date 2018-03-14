from bitcoin_lib.encoding import BytesReader
from .utils import get_nonce
from .message import Message


class PingMessage(Message):
    def __init__(self, nonce, *, options):
        super().__init__('ping', options = options)
        self.nonce = nonce or get_nonce()

    def get_payload(self):
        return self.nonce

    def set_payload(self, payload):
        reader = BytesReader(payload)
        self.nonce = reader.read(8)
        Message.check_finished(reader)
