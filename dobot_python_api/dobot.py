from functools import reduce
import struct
from time import sleep
from typing import Iterable, List, Tuple, Optional
from serial import Serial

from dobot_python_api.api.message_id import MessageID

import api

def create_connection(port: Optional[str] = None) -> Serial | None:
    seri = api.connect(port)
    if seri != None and seri.is_open:
        _queued_cmd_start_exec(seri)
        _queued_cmd_clear(seri)
        _set_ptp_joint_params(seri, (200, 200, 200, 200), (200, 200, 200, 200))
        #_set_ptp_coordinate_params(seri, 200, 200)
        #_set_ptp_jump_params(seri, 10, 200)
        #_set_ptp_common_params(seri, 100, 100)
    return seri

def _pack(t: str, params: Iterable): #move to message?
    return reduce(lambda x, y: x + struct.pack(t, y), params, b'')

def _unpack(t: str, params: bytes): #move to message?
    return struct.unpack(t, params)

def _queued_cmd_start_exec(seri: Serial):  #-> api.Message:
    api.send_message(MessageID.SET_QUEUED_CMD_START_EXEC, 0x01, b'', seri)
    return api.receive_message(seri)

def _queued_cmd_clear(seri: Serial):
    api.send_message(MessageID.SET_QUEUED_CMD_CLEAR, 0x01, b'', seri)

def _set_ptp_joint_params(seri: Serial, velocity : Tuple[float, float, float, float], acceleration : Tuple[float, float, float, float]):
    params = _pack('f', velocity + acceleration)
    api.send_message(MessageID.SET_PTP_JOINT_PARAMS, 0x01, params, seri)

def _set_ptp_coordinate_params(seri: Serial, velocity: float, acceleration: float):
    params = struct.pack('f', [velocity, acceleration])
    api.send_message(MessageID.SET_PTP_COORDINATE_PARAMS, 0x01, params, seri)

def _set_ptp_jump_params(seri: Serial, velocity: float, acceleration: float):
    params = struct.pack('f', [velocity, acceleration])
    api.send_message(MessageID.SET_PTP_JUMP_PARAMS, 0x01, params, seri)

def _set_ptp_common_params(seri: Serial, velocity: float, acceleration: float):
    params = struct.pack('f', [velocity, acceleration])
    api.send_message(MessageID.SET_PTP_COMMON_PARAMS , 0x01, params, seri)

#def
