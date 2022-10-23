from functools import reduce

def _checksum(b) -> int:
    return (2**8 -(reduce(lambda x, y: x+y, b) % 256)) % 256

def msg_dict(msg_id: int, ctrl: int, params: bytes):
    return {
        'header': b'\xaa\xaa',
        'len': len(params) + 2,
        'id': msg_id,
        'ctrl': ctrl,
        'params': params,
        'checksum': _checksum(bytes([msg_id, ctrl]) + params)
    }

def bytes_to_dict(b: bytes) -> dict:
    return {
        'header': b[0:2],
        'len': b[2],
        'id': b[3],
        'ctrl': b[4],
        'params': b[5:-1],
        'checksum': _checksum(b[3:-1])
    }

"""def _get_bytes(d: dict) -> bytes: #simple version
    b: bytearray = bytearray(b'')
    for item in d:
        if isinstance(item, int):
           b.append(item)
        else:
            b.extend(item)
    return b
"""
def get_bytes(d: dict) -> bytes:
    return reduce(lambda x, y: x + bytes([y]) if isinstance(y, int) else x + y, d.values(), b'')
