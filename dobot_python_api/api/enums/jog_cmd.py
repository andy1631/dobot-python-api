
from enum import IntEnum


class JOG_CMD(IntEnum):
    IDEL = 0    #Void
    AP = 1      #X+/J1+
    AN = 2      #X-/J1-
    BP = 3      #Y+/J2+
    BN = 4      #Y-/J2-
    CP = 5      #Z+/J3+
    CN = 6      #Z-/J3-
    DP = 7      #R+/J4+
    DN = 8      #R-/J4-

class JOG_MODE(IntEnum):
    COORDINATE = 0
    JOINT = 1
