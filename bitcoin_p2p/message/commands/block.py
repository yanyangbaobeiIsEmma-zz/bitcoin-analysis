from .message import Message


class BlockMessage(Message):
    def __init__(self, block, *, options):
        super().__init__('block', options = options)
        self.block = block

    def get_payload(self):
        return self.block.serialize()

    def set_payload(self, payload):
        self.block = Block.deserialize(payload)
