from logging import getLogger
from time import sleep


from .message import Message
from .api import *

_log = getLogger(__name__)

def connect() -> bool:
    _log.info('Connecting to Robot on port: ' + port)
    isOpen = initialize_api()

    return isOpen

"""def ir_toggle(self, enable: bool = True, port: GPIO = GPIO.PORT_GP4) -> Any:
    "Turn the IR sensor on or off"

    msg = Message()
    msg.id = 138
    msg.ctrl = 0x03
    msg.params = bytearray([])
    msg.params.extend(bytearray([int(enable)]))
    msg.params.extend(bytearray([port]))
    msg.params.extend(bytearray([0x1]))  # Version1=0, Version2=1
    return self._extract_cmd_index(self._send_command(msg))

def get_ir(self, port: GPIO = GPIO.PORT_GP4) -> bool:
    "Check if IR sensor is triggered"

    msg = Message()
    msg.id = 138
    msg.ctrl = 0x00
    msg.params = bytearray([])
    msg.params.extend(bytearray([port]))
    msg.params.extend(bytearray([0x01]))
    msg.params.extend(bytearray([0x1]))  # Version1=0, Version2=1
    response = self._send_command(msg)
    logger.debug(str(response))
    state = struct.unpack_from("?", response.params, 0)[0]
    return state
"""
