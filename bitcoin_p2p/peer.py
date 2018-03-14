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

    def __init__(self, event_loop, *, host, port = None, network):
        super().__init__()
        self.logger = logging.getLogger('Peer')
        self.receive_buffer = BytesBuffer()
        self.status = Peer.DISCONNECTED
        self.network = Network.get(network)
        self.host = host
        self.port = port or self.network.port
        self.messages = Messages({'network': self.network})
        self.best_height = 0
        self.version = 0
        self.subversion = None
        self.version_sent = False
        self.future = event_loop.create_connection(lambda: self, host = self.host, port = self.port)

        @self.on('ping')
        def on_ping(message):
            self.send_pong(message.nonce)

        @self.on('version')
        def on_version(message):
            self.version = message.version
            self.subversion = message.subversion
            self.best_height = message.start_height
            self.logger.info({
                'ip': self.transport.get_extra_info('peername'),
                'version': self.version,
                'subversion': self.subversion,
                'best_height': self.best_height
            })
            verack_response = self.messages.Verack()
            self.send_message(verack_response)
            if not self.version_sent:
                self.send_version()

        @self.on('verack')
        def on_verack(message):
            self.status = Peer.READY
            self.emit('ready')

    def connection_made(self, transport):
        self.transport = transport
        self.status = Peer.CONNECTED
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
        if self.transport.can_write_eof():
            self.transport.write_eof()
        self.disconnect()

    def connection_lost(self, error):
        if error:
            self.logger.exception(error)
        else:
            self.logger.debug('connection lost')
        super().connection_lost(error)

    def connect(self):
        asyncio.ensure_future(self.future)

    def disconnect(self):
        if self.status != Peer.DISCONNECTED:
            self.transport.close()
            self.status = Peer.DISCONNECTED

    def receive_data(self):
        if len(self.receive_buffer) > Peer.MAX_RECEIVE_BUFFER:
            self.connection_lost()
        else:
            self.read_message()

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
