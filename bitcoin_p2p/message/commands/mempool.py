from .message import Message


class MempoolMessage(Message):
    def __init__(self, *, options):
        super().__init__('mempool', options = options)
