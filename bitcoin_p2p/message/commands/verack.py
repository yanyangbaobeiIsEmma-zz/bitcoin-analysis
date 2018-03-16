from .message import Message


class VerackMessage(Message):
    def __init__(self, *, options):
        super().__init__('verack', options = options)
