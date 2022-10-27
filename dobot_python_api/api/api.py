#import struct
import serial
from typing import Optional
from serial.tools import list_ports
#from multiprocessing import RLock
import logging

from .enums import MessageID

from .message import *

#_lock = RLock()

def _get_coms_port() -> str:
    comports = list_ports.comports()

    if comports:
        devices = [comport.device for comport in comports]

        return str(devices[0])
    else:
        raise Exception('No device found!')

def connect(port: Optional[str] = None) -> serial.Serial | None:
    seri = serial.Serial(
        port if port != None else _get_coms_port(),
        baudrate = 115200,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
    )
    logging.info("Connecting to dobot on port ", seri.port)
    if not seri.is_open: seri.open()
    return seri

def disconnect(seri):
    logging.info("Disconnection dobot")
    if seri != None and seri.is_open:
        seri.close()
        logging.debug("Serial port closed")


def _send_message(msg_id: MessageID, ctrl: int, params: bytes, seri: serial.Serial):
    msg = msg_dict(msg_id, ctrl, params)
    frame = get_bytes(msg)
    seri.write(frame)

def _receive_message(seri: serial.Serial) -> Message:

    h1 = b''
    h2 = seri.read(1)

    while h1 + h2 != b'\xaa\xaa':
        h1 = h2
        h2 = seri.read(1)

    b = bytearray(b'\xaa\xaa' + seri.read(1))
    b.extend(seri.read(b[2] + 1))
    return bytes_to_dict(b)

def send_command(msg_id: MessageID, ctrl: int, params: bytes, seri: serial.Serial) -> Message:
    _send_message(msg_id, ctrl, params, seri)
    return _receive_message(seri)
