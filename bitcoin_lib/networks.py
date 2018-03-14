class Network:
    networks = {}

    def __init__(self, name, **options):
        self.name = name
        self.pubkeyhash = options['pubkeyhash']
        self.privatekey = options['privatekey']
        self.scripthash = options['scripthash']
        self.xpubkey = options['xpubkey']
        self.xprivkey = options['xprivkey']
        self.network_magic = options['network_magic']
        self.port = options['port']
        self.dns_seeds = options['dns_seeds']
        Network.networks[name] = self

    @staticmethod
    def get(name):
        if isinstance(name, Network):
            return name
        else:
            return Network.networks[name]


Network(
    'mainnet',
    pubkeyhash = 0x00,
    privatekey = 0x80,
    scripthash = 0x05,
    xpubkey = 0x0488b21e,
    xprivkey = 0x0488ade4,
    network_magic = b'\xf9\xbe\xb4\xd9',
    port = 8333,
    dns_seeds = (
        'seed.bitcoin.sipa.be',
        'dnsseed.bluematt.me',
        'dnsseed.bitcoin.dashjr.org',
        'seed.bitcoinstats.com',
        'seed.bitnodes.io',
        'bitseed.xf2.org'
    )
)

Network(
    'testnet',
    pubkeyhash = 0x6f,
    privatekey = 0xef,
    scripthash = 0xc4,
    xpubkey = 0x043587cf,
    xprivkey = 0x04358394,
    network_magic = b'\x0b\x11\x09\x07',
    port = 18333,
    dns_seeds = (
        'seed.bitcoin.sipa.be',
        'dnsseed.bluematt.me',
        'dnsseed.bitcoin.dashjr.org',
        'seed.bitcoinstats.com',
        'seed.bitnodes.io',
        'bitseed.xf2.org'
    )
)
