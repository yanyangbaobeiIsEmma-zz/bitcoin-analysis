import struct
from bitcoin_lib.crypto.hash import sha256sha256
from bitcoin_lib.networks import Network
from .builder import builder
from .commands import message_map

MINIMUM_LENGTH = 20
PAYLOAD_START = 16


class Messages:
    def __init__(self, options):
        self.builder = builder(options)
        self.commands = {**self.builder['commands']}
        self.network = options['network'] or Network.get('mainnet')

    def __getattr__(self, name):
        return self.commands[name]

    def deserialize(self, data):
        if len(data) < MINIMUM_LENGTH:
            return
        elif not self._discard_until_next_message(data):
            return

        payload_length = struct.unpack_from('<I', bytes(data), PAYLOAD_START)[0]
        message_length = payload_length + 24
        if len(data) < message_length:
            return

        command = data[4:16].decode('ascii').replace('\x00', '')
        checksum = data[20:24]
        payload = data[24:message_length]
        checksum_confirm = sha256sha256(payload)[:4]
        data.skip(message_length)
        if checksum == checksum_confirm:
            return self._build(command, payload)

    def _discard_until_next_message(self, data):
        i = 0
        while True:
            if data[i : i + 4] == self.network.network_magic:
                data.skip(i)
                return True
            elif i > len(data) - 4:
                data.skip(i)
                return False

    def _build(self, command, payload):
        if command in self.builder['commands_map']:
            return message_map[command].deserialize(self.network, payload)

    def add(self, key, name, Command):
        self.builder.add(key, Command)
        self.commands[name] = self.builder['commands'][key]
