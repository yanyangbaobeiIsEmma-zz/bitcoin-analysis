import functools
from bitcoin_lib.networks import Network
from .commands import message_map


def builder(options):
    options['network'] = options.get('network', Network.get('mainnet'))
    options['protocol_version'] = options.get('protocol_version', 70015)

    commands_map = {
        'addr': 'Address',
        'alert': 'Alert',
        'block': 'Block',
        'feefilter': 'FeeFilter',
        'filteradd': 'FilterAdd',
        'filterclear': 'FilterClear',
        'filterload': 'FilterLoad',
        'getaddr': 'GetAddr',
        'getblocks': 'GetBlocks',
        'getdata': 'GetData',
        'getheaders': 'GetHeaders',
        'headers': 'Headers',
        'inv': 'Inventory',
        'mempool': 'MemPool',
        'merkleblock': 'MerkleBlock',
        'notfound': 'NotFound',
        'ping': 'Ping',
        'pong': 'Pong',
        'reject': 'Reject',
        'sendcmpct': 'SendCmpct',
        'sendheaders': 'SendHeaders',
        'tx': 'Transaction',
        'verack': 'Verack',
        'version': 'Version'
    }

    commands = {
        commands_map[command]: functools.partial(message_map[command], options = options)
        for command in commands_map
    }

    return {
        'commands': commands,
        'commands_map': commands_map
    }
