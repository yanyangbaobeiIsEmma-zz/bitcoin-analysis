from .message import Message


class MerkleBlockMessage(Message):
    def __init__(self, merkle_block, *, options):
        super().__init__('merkleblock', options = options)
        self.merkle_block = merkle_block

    def get_payload(self):
        if self.merkle_block:
            return self.merkle_block.serialize()
        else:
            return b''

    def set_payload(self, payload):
        self.merkleblock = MerkleBlock.deserialize(payload)
