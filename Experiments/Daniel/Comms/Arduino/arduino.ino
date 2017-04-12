#include "protocol.h"

//TODO
// Easy encode and decode errors


#define CHANNELS_IN_RATE 40 //hz

//state variables
bool connected = false;
uint8_t errors = 0;
long last_heartbeat_recv = 0;
uint8_t mode = MODE_FAILSAFE;


void setup() {
  Serial.begin(115200);
}

void loop() {

  if((millis() - last_heartbeat_recv)/1000 > HEARTBEAT_TIMEOUT){
    connected = false;
  }

  send_heartbeat();

  recv_msg();
  
  //send_channels_in();
}

void send_heartbeat(){
  //store state between iterations
  static long last_heartbeat_send = 0;
  
  //send at an interval
  if(millis() - last_heartbeat_send > 1000/HEARTBEAT_RATE){
    send_heartbeat(mode,errors);
    last_heartbeat_send = millis();
  }
}

void send_channels_in(){
  //store state between iterations
  static long last_channels_in_send = 0;
  
  //send at an interval
  if(millis() - last_channels_in_send > 1000/CHANNELS_IN_RATE){
    send_channels_in(1000,1200,1300,2000);
    last_channels_in_send = millis();
  }
}


void handle_heartbeat(uint8_t* payload){
  connected = true;
  last_heartbeat_recv = millis();
}

void handle_control(uint8_t* payload){
  msg_control_t control;
  decode_control(payload,&control);

  //echo it back as a channels_in msg
  //send_debug(control.throttle,control.steering,control.aux1);
  send_channels_in(control.throttle,control.steering,control.aux1,control.aux2);
}

void handle_set_mode(uint8_t* payload){
  msg_set_mode_t msg;
  decode_set_mode(payload,&msg);
  mode = msg.mode;
}

void recv_msg(){
  byte payload[32];
  static int dropped = 0;
  
  if(Serial.available()){
    //sync data stream
    while(true){
      while(!Serial.available()){delayMicroseconds(10);}
      byte b = Serial.peek();
      if(b == START){break;}
      else{
        Serial.read();       
       }
    }
    //discard start byte
    byte start = Serial.read();
    //read msg_id
    while(!Serial.available()){delayMicroseconds(10);}
    uint8_t msg_id = Serial.read();
    //read msg_payload
    int msg_length = msg_len[msg_id] -2;
    while(Serial.available() < msg_length){delayMicroseconds(10);}
    Serial.readBytes(payload,msg_length);
    //Handle message
    switch(msg_id){
      case MSG_HEARTBEAT:
        handle_heartbeat(payload);
      break;
      case MSG_CONTROL:
        handle_control(payload);
      break;
      case MSG_SET_MODE:
        handle_set_mode(payload);
      break;
    }
  }
}

