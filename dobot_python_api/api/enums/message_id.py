from enum import IntEnum

class MessageID(IntEnum):

    #Device Information
    SET_GET_DEVICE_SN = 0
    SET_GET_DEVICE_NAME = 1

    #Real-time Pose
    GET_POSE = 10
    RESET_POSE = 11

    #Alarm
    GET_ALARMS_STATE = 20
    CLEAR_ALL_ALARMS_STATE = 21

    #Homing Function
    SET_GET_HOME_PARAMS = 30
    HOME_CMD = 31

    #Handhold Teaching
    HHTTRIG_MODE = 40
    HHTTRIG_OUTPUT_ENABLED = 41
    GET_HHTTRIG_OUTPUT = 42

    #End Effector
    SET_GET_END_EFFECTOR_PARAMS = 60
    SET_GET_END_EFFECTOR_LASER = 61
    SET_GET_END_EFFECTOR_SUCTION_CUP = 62
    SET_GET_END_EFFECTOR_GRIPPER = 63

    #JOG (jogging?)
    SET_GET_JOG_JOINT_PARAMS = 70
    SET_GET_JOG_COORDINATE_PARAMS = 71
    SET_GET_JOG_COMMON_PARAMS = 72
    JOG_CMD = 73

    #PTP (point to point)
    SET_GET_PTP_JOINT_PARAMS = 80
    SET_GET_PTP_COORDINATE_PARAMS = 81
    SET_GET_PTP_JUMP_PARAMS = 82
    SET_GET_PTP_COMMON_PARAMS = 83
    PTP_CMD = 84

    #CP (Continuous Path)
    CP_CMD = 91

    #ARC
    ARC_PARAMS = 100
    ARC_CMD = 101

    #WAIT
    SET_WAIT_CMD = 110

    #EIO
    EIO = 131

    SET_EMOTOR = 135 # conveyor belt
    SET_GET_COLOR_SENSOR = 137
    SET_GET_IR_SWITCH = 138

    #Queued execution controll commands
    SET_QUEUED_CMD_START_EXEC = 240
    SET_QUEUED_CMD_STOP_EXEC = 241
    SET_QUEUED_CMD_START_DOWNLOAD = 243
    SET_QUEUED_CMD_STOP_DOWNLOAD = 244
    SET_QUEUED_CMD_CLEAR = 245
    GET_QUEUED_CMD_CURRENT_INDEX = 246
