#ifndef PROTOCOL_H__
#define PROTOCOL_H__
#endif

#include <stdint.h>
#include <Arduino.h>


///////////////////////////////PROTOCOL DEFINITION///////////////////////////
#define START 0xAA

#define HEARTBEAT_RATE      2.0 //hz
#define HEARTBEAT_TIMEOUT   1.5 //sec

#define MSG_HEARTBEAT       0x00
#define MSG_CHANNELS_IN     0x01
#define MSG_CONTROL         0x02
#define MSG_SET_MODE        0x03
#define MSG_DEBUG           0x04

#define MODE_MANUAL         0x00
#define MODE_AUTO           0x01
#define MODE_FAILSAFE       0x02
#define MODE_INVALID        0xFF

#define HEARTBEAT_LEN     4
#define CHANNELS_IN_LEN   10
#define CONTROL_LEN       20
#define SET_MODE_LEN      3
#define DEBUG_LEN         14
const int msg_len[5] = {HEARTBEAT_LEN,CHANNELS_IN_LEN,CONTROL_LEN,SET_MODE_LEN,DEBUG_LEN };

//////////////////////////////////HEARTBEAT////////////////////////////////
typedef struct msg_heartbeat_t{
  uint8_t mode;
  uint8_t errors;
}msg_heartbeat_t;

void send_heartbeat(uint8_t mode, uint8_t errors);
void decode_heartbeat(uint8_t *payload, msg_heartbeat_t* msg);


//////////////////////////////////CHANNELS_IN////////////////////////////////
typedef struct msg_channels_in_t{
  uint16_t throttle;
  uint16_t steering;
  uint16_t aux1;
  uint16_t aux2;
}msg_channels_in_t;

void send_channels_in(uint16_t throttle, uint16_t steering, uint16_t aux1, uint16_t aux2);

//////////////////////////////////CONTROL////////////////////////////////
typedef struct msg_control_t{
  uint16_t throttle;
  uint16_t steering;
  uint16_t aux1;
  uint16_t aux2;
}msg_control_t;

void decode_control(uint8_t *payload, msg_control_t* msg);

//////////////////////////////////SET_MODE////////////////////////////////
typedef struct msg_set_mode_t{
  uint8_t mode;
}msg_set_mode_t;

void decode_set_mode(uint8_t *payload, msg_set_mode_t* msg);
//////////////////////////////////DEBUG////////////////////////////////
typedef struct msg_debug_t{
  float val0;
  float val1;
  float val2;
}msg_debug_t;

void float2Bytes(float val, uint8_t* bytes);
float bytes2Float(uint8_t* bytes);
void send_debug(float val0, float val1, float val);
void decode_debug(uint8_t *payload, msg_debug_t* msg);
