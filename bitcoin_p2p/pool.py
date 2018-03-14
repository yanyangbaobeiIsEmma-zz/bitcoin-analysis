from datetime import datetime
import functools
import socket
import time
from pyee import EventEmitter
from bitcoin_lib.networks import Network
from .peer import Peer
from .message.commands import message_map


class Pool(EventEmitter):
    MAX_CONNECTED_PEERS = 8
    RETRY_SECONDS = 30
    PEER_EVENTS = tuple(message_map.keys())

    def __init__(self, event_loop, *,
        network,
        addresses = [],
        listen_address = False,
        dns_seed = False,
        max_size = None
    ):
        super().__init__()
        self.event_loop = event_loop
        self.keepalive = False
        self.connected_peers = {}
        self.addresses = []
        self.listen_address = listen_address
        self.dns_seed = dns_seed
        self.max_size = max_size or Pool.MAX_CONNECTED_PEERS
        self.network = Network.get(network)
        for address in addresses:
            self.add_address(address)

        if listen_address:
            @self.on('peer.address')
            def on_peer_address(peer, message):
                for address in message.addresses:
                    if time.time() + 1000 * 60 * 10 < address['time'].timestamp() < 10 ** 11:
                        address['time'] = datetime.fromtimestamp(time.time() - 1000 * 60 * 60 * 24 * 5)
                    self.add_address(address)

        @self.on('seed')
        def on_seed(ips):
            for ip in ips:
                self.add_address({'ip': {'v4': ip}})
            if self.keepalive:
                self.fill_connections()

        @self.on('peer.disconnect')
        def on_peer_disconnect(self, peer, address):
            self.deprioritize_address(address)
            self.remove_connected_peer(address)
            if self.keepalive:
                self.fill_connections()

    def connect(self):
        self.keepalive = True
        if self.dns_seed:
            self.add_addresses_from_seeds()
        else:
            self.fill_connections()

    def disconnect(self):
        self.keepalive = False
        for peer in self.connected_peers.values():
            peer.disconnect()

    @property
    def connections(self):
        return len(self.connected_peers)

    def fill_connections(self):
        for address in self.addresses:
            if self.connections >= self.max_size:
                break
            if 'retry_time' not in address or address['retry_time'] < time.time():
                self.connect_peer(address)

    def remove_connected_peer(self, address):
        code = address['id']
        if self.connected_peers[code].status != Peer.DISCONNECTED:
            self.connected_peers[code].disconnect()
        else:
            del self.connected_peers[code]

    def connect_peer(self, address):
        if address['id'] in self.connected_peers:
            return
        port = address.get('port', self.network.port)
        ip = address['ip'].get('v4') or address['ip'].get('v6')
        peer = Peer(self.event_loop, host = ip, port = port, network = self.network)

        @peer.on('connect')
        def on_peer_connect():
            self.emit('peer.connect', peer, address)

        @peer.on('disconnect')
        def on_peer_disconnect():
            self.emit('peer.disconnect', peer, address)

        @peer.on('ready')
        def on_peer_ready():
            self.emit('peer.ready', peer, address)

        for event in Pool.PEER_EVENTS:
            @peer.on(event)
            def on_peer_event(message):
                self.emit('peer.' + event, peer, message)

        peer.connect()
        self.connected_peers[address['id']] = peer

    def deprioritize_address(self, peer, address):
        try:
            index = self.addresses.index(address)
            del self.addresses[index]
            address['retry_time'] = time.time() + Pool.RETRY_SECONDS
            self.addresses.append(address)
        except ValueError:
            pass

    def add_address(self, address):
        if 'port' not in address:
            address['port'] = self.network.port
        address['id'] = address['ip'].get('v6', '') + address['ip'].get('v4', '') + str(address['port'])
        if all(address['id'] != x['id'] for x in self.addresses):
            self.addresses = [address] + self.addresses

    def add_addresses_from_seed(self, seed):
        try:
            self.emit('seed', socket.gethostbyname_ex(seed)[2])
        except socket.gaierror as error:
            self.emit('seed.error', error)

    def add_addresses_from_seeds(self):
        for seed in self.network.dns_seeds:
            self.add_addresses_from_seed(seed)

    def send_message(self, message):
        for peer in self.connected_peers.values():
            peer.send_message(message)
