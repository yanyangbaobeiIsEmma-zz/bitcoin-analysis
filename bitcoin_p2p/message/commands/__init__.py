from .addr import AddrMessage
from .alert import AlertMessage
from .block import BlockMessage
from .feefilter import FeeFilterMessage
from .filteradd import FilterAddMessage
from .filterclear import FilterClearMessage
from .filterload import FilterLoadMessage
from .getaddr import GetAddrMessage
from .getblocks import GetBlocksMessage
from .getdata import GetDataMessage
from .getheaders import GetHeadersMessage
from .headers import HeadersMessage
from .inv import InvMessage
from .mempool import MempoolMessage
from .merkleblock import MerkleBlockMessage
from .notfound import NotFoundMessage
from .ping import PingMessage
from .pong import PongMessage
from .reject import RejectMessage
from .sendcmpct import SendCmpctMessage
from .sendheaders import SendHeadersMessage
from .tx import TxMessage
from .verack import VerackMessage
from .version import VersionMessage

message_map = {
    'addr': AddrMessage,
    'alert': AlertMessage,
    'block': BlockMessage,
    'feefilter': FeeFilterMessage,
    'filteradd': FilterAddMessage,
    'filterclear': FilterClearMessage,
    'filterload': FilterLoadMessage,
    'getaddr': GetAddrMessage,
    'getblocks': GetBlocksMessage,
    'getdata': GetDataMessage,
    'getheaders': GetHeadersMessage,
    'headers': HeadersMessage,
    'inv': InvMessage,
    'mempool': MempoolMessage,
    'merkleblock': MerkleBlockMessage,
    'notfound': NotFoundMessage,
    'ping': PingMessage,
    'pong': PongMessage,
    'reject': RejectMessage,
    'sendcmpct': SendCmpctMessage,
    'sendheaders': SendHeadersMessage,
    'tx': TxMessage,
    'verack': VerackMessage,
    'version': VersionMessage
}
