import struct
from bitcoin_lib.crypto.hash import sha256sha256
from bitcoin_lib.encoding import BytesReader, BytesWriter
from bitcoin_lib.networks import Network


class Message:
    def __init__(self, command, *, options):
        self.command = command
        self.network = options.get('network', Network.get('mainnet'))

    def get_payload(self):
        return b''

    def set_payload(self, payload):
        pass

    def serialize(self):
        command_bytes = self.command.encode('ascii')
        payload = self.get_payload()
        checksum = sha256sha256(payload)[:4]
        writer = BytesWriter()
        writer.write(self.network.network_magic)
        writer.write(struct.pack('12s', command_bytes))
        writer.write_uint32(len(payload))
        writer.write(checksum)
        writer.write(payload)
        return writer.serialize()

    @classmethod
    def deserialize(cls, payload):
        message = cls(options = {})
        message.set_payload(payload)
        return message

    @staticmethod
    def check_finished(payload):
        assert payload.finished, 'Data still available after parsing'

    @classmethod
    def for_block(cls, id):
        return cls([Inventory.for_block(id)])

    @classmethod
    def for_filtered_block(cls, id):
        return cls([Inventory.for_filtered_block(id)])

    @classmethod
    def for_transaction(cls, id):
        return cls([Inventory.for_transaction(id)])
