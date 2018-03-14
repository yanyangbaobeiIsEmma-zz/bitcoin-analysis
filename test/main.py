import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import logging
from bitcoin_p2p.peer import Peer
from bitcoin_p2p.pool import Pool


logging.basicConfig(
    level = logging.INFO,
    format = '%(name)s: %(message)s',
    stream = sys.stderr
)

settings = {
    'network': 'mainnet',
    'host': '127.0.0.1',
    'port': 8333
}

logger = logging.getLogger('Server')

def run():
    event_loop = asyncio.get_event_loop()
    pool = Pool(event_loop, network = 'mainnet', dns_seed = True)
    pool.connect()
    try:
        event_loop.run_forever()
    finally:
        logger.debug('closing event loop')
        event_loop.close()

if __name__ == '__main__':
    run()
