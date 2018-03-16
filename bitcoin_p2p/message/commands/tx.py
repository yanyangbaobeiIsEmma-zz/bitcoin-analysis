from .message import Message


class TxMessage(Message):
    def __init__(self, transaction = None, *, options):
        super().__init__('transaction', options = options)
        self.transaction = transaction or Transaction()

    def get_payload(self):
        return self.transaction.serialize()

    def set_payload(self, payload):
        self.transaction = Transaction.deserialize(payload)
