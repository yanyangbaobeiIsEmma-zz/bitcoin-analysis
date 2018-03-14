from .message import Message


class SendHeadersMessage(Message):
    def __init__(self, *, options):
        super().__init__('sendheaders', options = options)
