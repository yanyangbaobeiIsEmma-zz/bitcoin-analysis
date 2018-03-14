import binascii
import random
import struct

def get_nonce():
    return struct.pack('<Q', random.randrange(1 << 64))

def write_ip(writer, ip):
    words = ip['v6'].split(':')
    for word in words:
        writer.write(binascii.unhexlify(word))

def write_address(writer, address):
    if not address:
        writer.write(bytes([0] * 26))
    else:
        writer.write_uint64(address['services'])
        write_ip(writer, address['ip'])
        writer.write_uint16(address['port'], big_endian = True)

def write_inventories(writer, inventories):
    write.write_varint(len(inventories))
    for inventory in inventories:
        writer.write_uint32(inventory['type'])
        writer.write(inventory['hash'])

def read_ip(reader):
    ipv6 = []
    for i in range(8):
        word = reader.read(2)
        ipv6.append(binascii.hexlify(word).decode())
    return {'v6': ':'.join(ipv6)}

def read_address(reader):
    services = reader.read_uint64()
    ip = read_ip(reader)
    port = reader.read_uint16(big_endian = True)
    return {
        'services': services,
        'ip': ip,
        'port': port
    }

def sanitize_start_stop(obj = {}):
    starts = obj['starts']
    stop = obj['stop']
    if starts:
        for i in range(len(starts)):
            if isinstance(starts[i], str):
                starts[i] = binascii.unhexlify(starts[i])[::-1]
    else:
        starts = []
    if isinstance(stop, str):
        stop = stop.encode('hex')[::-1]
    else:
        stop = bytes([0] * 32)

    return {'starts': starts, 'stop': stop}
