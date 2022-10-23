from enum import Enum

class MessageID(Enum):

    #Device Information
    DEVICE_SN = 0
    DEVICE_NAME = 1

    #Real-time Pose
    GET_POSE = 10
    RESET_POSE = 11

    #Alarm
    GET_ALARMS_STATE = 20
    CLEAR_ALL_ALARMS_STATE = 21
    #Homing Function
    HOME_PARAMS = 30
    HOME_CMD = 31

    #Handhold Teaching
    HHTTRIG_MODE = 40
    HHTTRIG_OUTPUT_ENABLED = 41
    GET_HHTTRIG_OUTPUT = 42

    #End Effector
    END_EFFECTOR_PARAMS = 60
    END_EFFECTOR_LAZER = 61
    END_EFFECTOR_SUCTION_CUP = 62
    END_EFFECTOR_GRIPPER = 63

    #JOG (jogging?)
    JOG_JOINT_PARAMS = 70
    JOG_COORDINATE_PARAMS = 71
    JOG_COMMON_PARAMS = 72

    #PTP (point to point)
    PTP_JOINT_PARAMS = 80
    PTP_COORDINATE_PARAMS = 81
    PTP_JUMP_PARAMS = 82
    PTP_COMMON_PARAMS = 83
    PTP_CMD = 84

    #CP (Continuous Path)
    CP_CMD = 91

    #ARC
    ARC_PARAMS = 100
    ARC_CMD = 101

    #EIO
    EIO = 131

    #Queued execution controll commands
    SET_QUEUED_CMD_START_EXEC = 240
    SET_QUEUED_CMD_STOP_EXEC = 241
    SET_QUEUED_CMD_CLEAR = 245
    GET_QUEUED_CMD_CURRENT_INDEX = 246


    SET_EMOTOR = 135 # conveyor belt
    COLOR_SENSOR = 137
    IR_SWITCH = 138

class PTP_MODE(Enum):

    JUMP_XYZ = 0x00
    MOVJ_XYZ = 0x01
    MOVL_XYZ = 0x02
    JUMP_ANGLE = 0x03
    MOVJ_ANGLE = 0x04
    MOVL_ANGLE = 0x05
    MOVJ_INC = 0x06
    MOVL_INC = 0x07
    MOVJ_XYZ_INC = 0x08
    JUMP_MOVL_XYZ = 0x09
