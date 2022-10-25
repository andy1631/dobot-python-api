from enum import IntEnum


class CTRL(IntEnum):
    SET = 0x01
    SET_QUEUED = 0x03
    GET = 0x00
    GET_QUEUED = 0x02 #unused?
