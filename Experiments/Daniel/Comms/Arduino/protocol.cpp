#include "protocol.h"

///////////////////////////////////////HEARTBEAT////////////////////////////////////

void send_heartbeat(uint8_t mode, uint8_t errors){
  uint8_t bytes[HEARTBEAT_LEN];
  bytes[0] = START;
  bytes[1] = MSG_HEARTBEAT;
  bytes[2] = mode;
  bytes[3] = errors;
  Serial.write(bytes,HEARTBEAT_LEN);
}

void decode_heartbeat(uint8_t *payload, msg_heartbeat_t* msg){
  msg->mode = payload[0];
  msg->errors = payload[1];
}

////////////////////////////////////CHANNELS_IN/////////////////////////////////////

void send_channels_in(uint16_t throttle, uint16_t steering, uint16_t aux1, uint16_t aux2){
  uint8_t bytes[CHANNELS_IN_LEN];
  bytes[0] = START;
  bytes[1] = MSG_CHANNELS_IN;
  bytes[2] = throttle & 0x00FF;
  bytes[3] = (throttle & 0xFF00)>>8;
  bytes[4] = steering & 0x00FF;
  bytes[5] = (steering & 0xFF00)>>8;
  bytes[6] = aux1 & 0x00FF;
  bytes[7] = (aux1 & 0xFF00)>>8;
  bytes[8] = aux2 & 0x00FF;
  bytes[9] = (aux2 & 0xFF00)>>8;
  Serial.write(bytes,CHANNELS_IN_LEN);
}

///////////////////////////////////CONTROL///////////////////////////////////////

void decode_control(uint8_t *payload, msg_control_t* msg){
  msg->throttle = (payload[1] << 8) | payload[0];
  msg->steering = (payload[3] << 8) | payload[2];
  msg->aux1 = (payload[5] << 8) | payload[4];
  msg->aux2 = (payload[7] << 8) | payload[6];
}

/////////////////////////////////////SET_MODE///////////////////////////////////

void decode_set_mode(uint8_t *payload, msg_set_mode_t* msg){
  msg->mode = payload[0];
}


////////////////////////////////////DEBUG//////////////////////////////////////////

void float2Bytes(float val, uint8_t* bytes){
  // Create union of shared memory space
  union {
    float val;
    uint8_t bytes[4];
  } u;
  // Overite bytes of union with float variable
  u.val = val;
  // Assign bytes to input array
  memcpy(bytes, u.bytes, 4);
}


float bytes2Float(uint8_t* bytes){
  float val;
  // Create union of shared memory space
  union {
    float val;
    uint8_t bytes[4];
  } u;
  // Assign bytes to input array
  memcpy(u.bytes, bytes, 4);
  return u.val;
}

void send_debug(float val0,float val1, float val2){
  uint8_t bytes[DEBUG_LEN];
  bytes[0] = START;
  bytes[1] = MSG_DEBUG;
  float2Bytes(val0,bytes+2);
  float2Bytes(val1,bytes+6);
  float2Bytes(val2,bytes+10);
  Serial.write(bytes,DEBUG_LEN);
}

void decode_debug(uint8_t *payload, msg_debug_t* msg){
  msg->val0 = bytes2Float(payload);
  msg->val1 = bytes2Float(payload + 4);
  msg->val2 = bytes2Float(payload + 8);
}

