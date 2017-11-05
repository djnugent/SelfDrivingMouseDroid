import struct

START = 0xAA

HEARTBEAT_RATE = 2.0 #hz
HEARTBEAT_TIMEOUT = 2.0 #sec

MSG_HEARTBEAT = 0x00
MSG_CHANNELS_IN = 0x01
MSG_CONTROL = 0x02
MSG_SET_MODE = 0x03
MSG_DEBUG = 0x04

msg_len =  {MSG_HEARTBEAT:2,\
            MSG_CHANNELS_IN:8,\
            MSG_CONTROL:8,\
            MSG_SET_MODE:1,\
            MSG_DEBUG:12}

MODE_MANUAL = 0x00
MODE_AUTO = 0x01
MODE_FAILSAFE = 0x02
MODE_INVALID = 0xFF



def decode(msg_id,payload):
    if msg_id == MSG_HEARTBEAT:
        return unpack_heartbeat(payload)
    elif msg_id == MSG_CHANNELS_IN:
        return unpack_channels_in(payload)
    elif msg_id == MSG_CONTROL:
        return unpack_control(payload)
    elif msg_id == MSG_SET_MODE:
        return unpack_set_mode(payload)
    elif msg_id == MSG_DEBUG:
        return unpack_debug(payload)
    else:
        return {'id':'invalid'}


################################################################
###################### UNPACK PAYLOADS #########################
################################################################
def unpack_heartbeat(raw):
    if len(raw) != msg_len[MSG_HEARTBEAT]:
        raise ValueError("Invalid packet length")

    payload = {'id':'heartbeat'}
    #decode mode
    payload['mode'] = decode_mode(raw[0])
    #decode error
    bitmask = decode_bitmask(raw[1])
    payload['invld_msg_id'] = bitmask[0]
    payload['invld_val'] = bitmask[1]
    payload['no_RC'] = bitmask[2]
    payload['no_heartbeat'] = bitmask[3]

    return payload

def unpack_channels_in(raw):
    if len(raw) != msg_len[MSG_CHANNELS_IN]:
        raise ValueError("Invalid packet length")

    payload = {'id':'channels_in'}
    #decode channels
    payload['throttle'] = decode_short(raw[0:2])
    payload['steering'] = decode_short(raw[2:4])
    payload['aux1'] = decode_short(raw[4:6])
    payload['aux2'] = decode_short(raw[6:8])

    return payload

def unpack_control(raw):
    if len(raw) != msg_len[MSG_CONTROL]:
        raise ValueError("Invalid packet length")

    payload = {'id':'control'}
    #decode channels
    payload['throttle'] = decode_short(raw[0:2])
    payload['steering'] = decode_short(raw[2:4])
    payload['aux1'] = decode_short(raw[4:6])
    payload['aux2'] = decode_short(raw[6:8])

    return payload

def unpack_set_mode(raw):
    if len(raw) != msg_len[MSG_SET_MODE]:
        raise ValueError("Invalid packet length")

    payload = {'id':'set_mode'}
    #decode mode
    payload['mode'] = decode_mode(raw[0])

    return payload

def unpack_debug(raw):
    if len(raw) != msg_len[MSG_DEBUG]:
        raise ValueError("Invalid packet length")

    payload = {'id':'debug'}
    #decode mode
    payload['val0'] = decode_float(raw[0:4])
    payload['val1'] = decode_float(raw[4:8])
    payload['val2'] = decode_float(raw[8:12])

    return payload

################################################################
######################## PACK PAYLOADS #########################
################################################################

def pack_heartbeat(mode='invalid',err_invld_msg_id = False,err_invld_val = False, err_no_RC= False, err_no_heartbeat = False):
    msg = struct.pack('BB',START,MSG_HEARTBEAT)
    msg += encode_mode(mode)
    msg += encode_bitmask([err_invld_msg_id,err_invld_val,err_no_RC,err_no_heartbeat,0,0,0,0])
    return msg

def pack_channels_in(throttle=1500,steering=1500,aux1=1500,aux2=1500):
    msg = struct.pack('BB',START,MSG_CHANNELS_IN)
    msg += encode_short(throttle)
    msg += encode_short(steering)
    msg += encode_short(aux1)
    msg += encode_short(aux2)
    return msg

def pack_control(throttle=1500,steering=1500,aux1=1500,aux2=1500):
    msg = struct.pack('BB',START,MSG_CONTROL)
    msg += encode_short(throttle)
    msg += encode_short(steering)
    msg += encode_short(aux1)
    msg += encode_short(aux2)
    return msg

def pack_set_mode(mode='invalid'):
    msg = struct.pack('BB',START,MSG_SET_MODE)
    msg += encode_mode(mode)
    return msg

def pack_debug(val0=0.0,val1=0.0,val2=0.0):
    msg = struct.pack('BB',START,MSG_DEBUG)
    msg += encode_float(val0)
    msg += encode_float(val1)
    msg += encode_float(val2)
    return msg

################################################################
##################### DESERIALIZING DATA #######################
################################################################
def decode_mode(_enum):
    if _enum == MODE_MANUAL:
        return 'manual'
    elif _enum == MODE_AUTO:
        return 'auto'
    elif _enum == MODE_FAILSAFE:
        return 'failsafe'
    else:
        return 'invalid'

def decode_bitmask(_byte):
    mask = list(range(0,8))
    for i in range(0,8):
        mask[i] = (_byte>>i)&(0x01)
    return mask

def decode_short(_bytes):
    return struct.unpack('H',_bytes)

def decode_long(_bytes):
    return struct.unpack('L',_bytes)

def decode_float(_bytes):
    return struct.unpack('f',_bytes)

################################################################
####################### SERIALIZING DATA #######################
################################################################
def encode_mode(_mode):
    if _mode == 'manual':
        return struct.pack('B',MODE_MANUAL)
    elif _mode == 'auto':
        return struct.pack('B',MODE_AUTO)
    elif _mode == 'failsafe':
        return struct.pack('B',MODE_FAILSAFE)
    else:
        return struct.pack('B',MODE_INVALID)

def encode_bitmask(_bits):
    byte = 0
    for i in range(0,8):
        byte = byte|(_bits[i]<<i)
    return struct.pack('B',byte)

def encode_short(_short):
    return struct.pack('H',_short)

def encode_long(_long):
    return struct.pack('L',_long)

def encode_float(_float):
    return struct.pack('f',_float)
