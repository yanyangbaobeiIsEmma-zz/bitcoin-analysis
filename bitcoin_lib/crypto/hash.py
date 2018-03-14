import hashlib

_hash = lambda name, data: hashlib.new(name, data).digest()
sha256 = lambda data: _hash('sha256', data)
ripemd160 = lambda data: _hash('ripemd160', data)
sha256sha256 = lambda data: sha256(sha256(data))
sha256ripemd160 = lambda data: ripemd160(sha256(data))
