from .message import Message


class GetAddrMessage(Message):
    def __init__(self, *, options):
        super().__init__('getaddr', options = options)
