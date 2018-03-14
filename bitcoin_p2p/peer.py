import asyncio
import logging
from pyee import EventEmitter
from bitcoin_lib.encoding import BytesBuffer
from bitcoin_lib.networks import Network
from .message import Messages


class Peer(asyncio.Protocol, EventEmitter):
    DISCONNECTED = 'disconnected'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    READY = 'ready'
    MAX_RECEIVE_BUFFER = 10000000

    def __init__(self, *, host, port, network, future):
        super().__init__()
        self.logger = logging.getLogger('Node')
        self.receive_buffer = BytesBuffer()
        self.status = self.DISCONNECTED
        self.network = Network.get(network)
        self.host = host
        self.port = port or self.network.port
        self.messages = Messages({'network': self.network})
        self.best_height = 0
        self.version = 0
        self.subversion = None
        self.version_sent = False
        self.future = future
        self.on('ping', self.on_ping)
        self.on('version', self.on_version)
        self.on('verack', self.on_verack)

    def connection_made(self, transport):
        self.logger.info('connection made')
        self.transport = transport
        self.status = self.CONNECTED
        self.emit('connect')
        self.send_version()

    def data_received(self, data):
        try:
            self.receive_buffer += data
            if not self.receive_buffer:
                raise ValueError
        except (IOError, ValueError) as error:
            errno, errstr = error.args
            self.logger.error('Data received error: ' + errstr)
            self.connection_lost(error)
            return
        self.receive_data()

    def eof_received(self):
        self.logger.debug('eof received')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)

    def connection_lost(self, error):
        if error:
            self.logger.exception(error)
        else:
            self.logger.debug('connection lost')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)
        super().connection_lost(error)

    def receive_data(self):
        if len(self.receive_buffer) > self.MAX_RECEIVE_BUFFER:
            self.connection_lost()
        else:
            self.read_message()

    def on_ping(self, message):
        self.send_pong(message.nonce)

    def on_verack(self, message):
        self.status = self.READY
        self.emit('ready')

    def on_version(self, message):
        self.version = message.version
        self.subversion = message.subversion
        self.best_height = message.start_height
        verack_response = self.messages.Verack()
        self.send_message(verack_response)
        if not self.version_sent:
            self.send_version()

    def send_message(self, message):
        self.transport.write(message.serialize())

    def read_message(self):
        message = self.messages.deserialize(self.receive_buffer)
        if message:
            self.emit(message.command, message)
            self.read_message()

    def send_pong(self, nonce):
        message = self.messages.Pong(nonce)
        self.send_message(message)

    def send_version(self):
        message = self.messages.Version()
        self.version_sent = True
        self.send_message(message)
