import builtins
from functools import reduce
import struct
from time import sleep
from typing import Any, Optional
from serial import Serial

import dobot_python_api.api as api

from dobot_python_api.api import MessageID, CTRL, JOG_CMD, JOG_MODE

from dobot_python_api.api.message_id import PTP_MODE

vector4 = tuple[float, float, float, float]

def create_connection(port: Optional[str] = None) -> Serial | None:
    seri = api.connect(port)
    print("connected")
    if seri != None and seri.is_open:

        _queued_cmd_start_exec(seri)
        _queued_cmd_clear(seri)
        set_ptp_joint_params(seri, (200, 200, 200, 200), (200, 200, 200, 200))
        set_ptp_coordinate_params(seri, 200, 200, 200, 200)
        set_ptp_jump_params(seri, 10, 200)
        set_ptp_common_params(seri, 100, 100)
        return seri

def _pack(params: tuple | list | bytes) -> bytes: #move to message?
    if type(params) == bytes: return bytes(params)
    t: str
    match type(params[0]):
        case builtins.int:
            t = 'i'
        case builtins.float:
            t = 'f'
    return reduce(lambda x, y: x + struct.pack(t, y), params, b'')

def _unpack(t: str, params: bytes): #move to message?
    part_len = struct.calcsize(t)
    return reduce(lambda x, y: x + struct.unpack(t, y), [params[i*part_len:i*part_len+part_len] for i in range(int(len(params)/part_len))], ())


def set_sn(serial, serial_number: str) -> None:
    api.send_command(MessageID.SET_GET_DEVICE_SN, CTRL.SET, bytes(serial_number, 'ascii'), serial)

def get_sn(serial) -> str:
    res = api.send_command(MessageID.SET_GET_DEVICE_SN, CTRL.GET, b'', serial)
    return str(res['params'], 'ascii')

def set_name(serial, name: str):
    api.send_command(MessageID.SET_GET_DEVICE_NAME, CTRL.SET, bytes(name, 'ascii'), serial)

def get_name(serial) -> str:
    res = api.send_command(MessageID.SET_GET_DEVICE_NAME, CTRL.GET, b'', serial)
    return str(res['params'], 'ascii')

def get_pose(serial) -> dict[str, float]:
    res = _unpack('f', api.send_command(MessageID.GET_POSE, CTRL.GET, b'', serial)['params'])
    return {
        'x': res[0],
        'y': res[1],
        'z': res[2],
        'r': res[3],
        'j1': res[4],
        'j2': res[5],
        'j3': res[6],
        'j4': res[7]
    }

def reset_pose(serial):
    api.send_command(MessageID.RESET_POSE, CTRL.SET, b'\x00' + _pack((0.0, 0.0)), serial)

def get_alarm_state(serial) -> bytes:
    return api.send_command(MessageID.GET_ALARMS_STATE, CTRL.GET, b'', serial)['params']

def clear_all_alarm_state(serial):
    api.send_command(MessageID.CLEAR_ALL_ALARMS_STATE, CTRL.SET, b'', serial)

def set_home(serial, x, y, z, r, queued: bool = True):
    api.send_command(MessageID.SET_GET_HOME_PARAMS, CTRL.SET_QUEUED if queued  else CTRL.SET, _pack((x, y, z, r)), serial)

def get_home(serial) -> vector4:
    return _unpack('f', api.send_command(MessageID.SET_GET_HOME_PARAMS, CTRL.GET, b'', serial)['params'])

def home(serial, queued: bool = True) -> int | None:
    res = api.send_command(MessageID.HOME_CMD, CTRL.SET_QUEUED if queued else CTRL.SET, b'\x00\x00\x00\x00', serial)
    return _unpack('Q', res['params'])[0] if res != None else None

def set_end_effector_params(serial, x: float, y: float, z: float, queued: bool = True) -> int | None:
    res = api.send_command(
        MessageID.SET_GET_END_EFFECTOR_PARAMS,
        CTRL.SET_QUEUED if queued else CTRL.SET,
        _pack((x, y, z)),
        serial
    )
    return _unpack('Q', res['params'])[0] if res != None else None

def get_end_effector_params(serial) -> tuple[float, float, float]:
    res = api.send_command(
        MessageID.SET_GET_END_EFFECTOR_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    return _unpack('f', res['params'])

def set_gripper(serial, enable: bool, queued: bool = True) -> int | None:
    res = api.send_command(MessageID.END_EFFECTOR_GRIPPER,
                           CTRL.SET_QUEUED if queued else CTRL.SET,
                           b'\x01' + (b'\x01' if enable else b'\x00'),
                           serial
                           )
    return _unpack('Q', res['params'])[0] if res != None else None

def get_gripper(serial) -> tuple[bool, bool]:
    res = api.send_command(MessageID.END_EFFECTOR_GRIPPER, CTRL.GET, b'', serial)
    return _unpack('?', res['params'])

def set_jog_joint_params(serial, velocity: vector4, acceleration: vector4, queued: bool = True) -> int | None:
   res = api.send_command(
       MessageID.SET_GET_JOG_JOINT_PARAMS,
       CTRL.SET_QUEUED if queued else CTRL.SET,
       _pack(velocity + acceleration),
       serial
   )
   return _unpack('Q', res['params'])[0] if res != None else None

def get_jog_joint_params(serial) -> dict[str, vector4]:
    res = api.send_command(
        MessageID.SET_GET_JOG_JOINT_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    unpacked = _unpack('f', res['params'])
    return {
        'velocity': unpacked[0:4],
        'acceleration': unpacked[4:8]
    }

def set_jog_coordinate_params(serial, velocity: vector4, acceleration: vector4, queued: bool = True) -> int | None:
   res = api.send_command(
       MessageID.SET_GET_JOG_COORDINATE_PARAMS,
       CTRL.SET_QUEUED if queued else CTRL.SET,
       _pack(velocity + acceleration),
       serial
   )
   return _unpack('Q', res['params'])[0] if res != None else None

def get_jog_coordinate_params(serial) -> dict[str, vector4]:
    res = api.send_command(
        MessageID.SET_GET_JOG_COORDINATE_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    unpacked = _unpack('f', res['params'])
    return {
        'velocity': unpacked[0:4],
        'acceleration': unpacked[4:8]
    }

def set_jog_common_params(serial, velocity_ratio: float, acceleration_ratio: float, queued: bool = True) -> int | None:
    res = api.send_command(
        MessageID.SET_GET_JOG_COMMON_PARAMS,
        CTRL.SET_QUEUED if queued else CTRL.SET,
        _pack((velocity_ratio, acceleration_ratio)),
        serial
    )
    return _unpack('Q', res['params'])[0] if res != None else None

def get_jog_common_params(serial) -> tuple[float, float]:
    res = api.send_command(
        MessageID.SET_GET_JOG_COMMON_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    return _unpack('f', res['params'])

def jog(serial, mode: JOG_MODE, cmd: JOG_CMD, queued: bool = True) -> int | None:
    res = api.send_command(
        MessageID.JOG_CMD,
        CTRL.SET_QUEUED if queued else CTRL.SET,
        _pack(struct.pack('B', mode) + struct.pack('B', cmd)),
        serial
    )
    return _unpack('Q', res['params'])[0] if res != None else None

def set_ptp_joint_params(serial, velocity: vector4, acceleration: vector4, queued: bool = True) -> int | None:
   res = api.send_command(
       MessageID.SET_GET_PTP_JOINT_PARAMS,
       CTRL.SET_QUEUED if queued else CTRL.SET,
       _pack(velocity + acceleration),
       serial
   )
   return _unpack('Q', res['params'])[0] if res != None else None



def get_ptp_joint_params(serial) -> dict[str, vector4]:
    res = api.send_command(
        MessageID.SET_GET_PTP_JOINT_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    unpacked = _unpack('f', res['params'])
    return {
        'velocity': unpacked[0:4],
        'acceleration': unpacked[4:8]
    }

def set_ptp_coordinate_params(serial, xyz_vel: float, r_vel: float, xyz_acc: float, r_acc: float, queued: bool = True) -> int | None:
   res = api.send_command(
       MessageID.SET_GET_PTP_COORDINATE_PARAMS,
       CTRL.SET_QUEUED if queued else CTRL.SET,
       _pack((xyz_vel, r_vel, xyz_acc, r_acc)),
       serial
   )
   return _unpack('Q', res['params'])[0] if res != None else None

def get_ptp_coordinate_params(serial) -> dict[str, tuple[float, float]]:
    res = api.send_command(
        MessageID.SET_GET_JOG_COORDINATE_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    unpacked = _unpack('f', res['params'])
    return {
        'velocity': unpacked[0:2],
        'acceleration': unpacked[2:4]
    }

def set_ptp_jump_params(serial, height: float, limit: float, queued: bool = True) -> int | None:
    res = api.send_command(
        MessageID.SET_GET_PTP_JUMP_PARAMS,
        CTRL.SET_QUEUED if queued else CTRL.SET,
        _pack((height, limit)),
        serial
    )
    return _unpack('Q', res['params'])[0] if res != None else None

def get_ptp_jump_params(serial) -> tuple[float, float]:
    res = api.send_command(
        MessageID.SET_GET_PTP_JUMP_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    return _unpack('f', res['params'])

def set_ptp_common_params(serial, velocity_ratio: float, acceleration_ratio: float, queued: bool = True) -> int | None:
    res = api.send_command(
        MessageID.SET_GET_PTP_COMMON_PARAMS,
        CTRL.SET_QUEUED if queued else CTRL.SET,
        _pack((velocity_ratio, acceleration_ratio)),
        serial
    )
    return _unpack('Q', res['params'])[0] if res != None else None

def get_ptp_common_params(serial) -> tuple[float, float]:
    res = api.send_command(
        MessageID.SET_GET_PTP_COMMON_PARAMS,
        CTRL.GET,
        b'',
        serial
    )
    return _unpack('f', res['params'])

def move(serial, destination: vector4, mode: PTP_MODE = PTP_MODE.MOVJ_XYZ, queued: bool = True) -> int | None:
    res = api.send_command(
        MessageID.PTP_CMD,
        CTRL.SET_QUEUED if queued else CTRL.SET,
        _pack(struct.pack('B', mode) + _pack(destination)),
        serial
    )
    return _unpack('Q', res['params'])[0] if res != None else None




def _queued_cmd_start_exec(seri: Serial):  #-> api.Message:
    api.send_command(MessageID.SET_QUEUED_CMD_START_EXEC, CTRL.SET, b'', seri)
    #return _unpack('f', api.receive_message(seri)['params'])

def _queued_cmd_clear(seri: Serial):
    api.send_command(MessageID.SET_QUEUED_CMD_CLEAR, CTRL.SET, b'', seri)
