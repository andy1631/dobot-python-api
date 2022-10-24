#import struct
import serial
from typing import Optional
from serial.tools import list_ports
#from multiprocessing import RLock
import logging

from .message_id import MessageID

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


def send_message(msg_id: MessageID, ctrl: int, params: bytes, seri: serial.Serial):
    msg = msg_dict(msg_id, ctrl, params)
    frame = get_bytes(msg)
    seri.write(frame)

def receive_message(seri: serial.Serial) -> Message:
    b = bytearray(seri.read(3))
    b.extend(seri.read(b[2] + 1))
    return bytes_to_dict(b)
