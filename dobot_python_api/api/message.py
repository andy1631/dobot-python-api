import struct
from functools import reduce
from typing import TypedDict, Any

from .message_id import MessageID

class Message(TypedDict):
    header: bytes
    len: int
    msg_id: MessageID
    ctrl: int
    params: bytes
    checksum: int



def _checksum(b) -> int:
    return (2**8 -(reduce(lambda x, y: x+y, b) % 256)) % 256

def msg_dict(msg_id: MessageID, ctrl: int, params: bytes) -> Message:
    return {
        'header': b'\xaa\xaa',
        'len': len(params) + 2,
        'msg_id': msg_id,
        'ctrl': ctrl,
        'params': params,
        'checksum': _checksum(bytes([msg_id, ctrl]) + params)
    }

def bytes_to_dict(b: bytes) -> Message:
    return {
        'header': b[0:2],
        'len': b[2],
        'msg_id': MessageID(b[3]),
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
def get_bytes(msg: Message ) -> bytes:
    values = [msg[k] for k in msg.keys()]
    return reduce(lambda x, y: x + bytes([y]) if isinstance(y, int) else x + y, values, b'')

def extract_cmd_index(response: Message) -> Any:
        return struct.unpack_from("I", response['params'], 0)[0]
