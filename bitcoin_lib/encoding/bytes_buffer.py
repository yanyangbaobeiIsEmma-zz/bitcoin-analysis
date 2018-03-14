class BytesBuffer:
    def __init__(self, data = b''):
        self.buffer = data

    def __bytes__(self):
        return self.buffer

    def __len__(self):
        return len(self.buffer)

    def __getitem__(self, key):
        return self.buffer[key]

    def __iadd__(self, data):
        self.buffer += data
        return self

    def skip(self, offset):
        self.buffer = self.buffer[offset:]
