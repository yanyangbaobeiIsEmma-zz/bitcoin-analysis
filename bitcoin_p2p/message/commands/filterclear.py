from .message import Message


class FilterClearMessage(Message):
    def __init__(self, *, options):
        super().__init__('filterclear', options = options)
