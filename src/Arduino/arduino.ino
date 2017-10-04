#include "protocol.h"
#include <ServoTimer2.h>


//TODO
// Easy encode and decode errors

#define PPM_Pin 3  //this must be 2 or 3
#define PWM_channel_1 6
#define PWM_channel_2 5
uint16_t ppm[16];  //array for storing up to 16 servo signals

#define CHANNELS_IN_RATE 40 //hz

//state variables
bool connected = false;
uint8_t errors = 0;
long last_heartbeat_recv = 0;
uint8_t mode = MODE_FAILSAFE;

// Setup our pwm outputs
ServoTimer2 steering;
ServoTimer2 throttle;

void setup() {
  // Open serial connection at baudrate 115200
  Serial.begin(115200);

  // Open PPM interrupt pin
  pinMode(PPM_Pin, INPUT);
  attachInterrupt(PPM_Pin - 2, read_ppm, CHANGE);

  // Start PWM output
  steering.attach(PWM_channel_1);
  throttle.attach(PWM_channel_2);

  // timer1 stuff for PPM decode
  TCCR1A = 0;  //reset timer1
  TCCR1B = 0;
  TCCR1B |= (1 << CS11);  //set timer1 to increment every 0,5 us
}

void loop() {

  // Extract pulse data from global ppm array
  uint16_t throttle_val = ppm[1];
  uint16_t steering_val = ppm[0];
  uint16_t aux1_val = ppm[2];
  uint16_t aux2_val = ppm[3];

  // Send those values to odroid
  send_vals(throttle_val, steering_val, aux1_val, aux2_val);

  // Update PWM output
  steering.write(steering_val);
  throttle.write(throttle_val);

  // Check if odroid is still responding
  if((millis() - last_heartbeat_recv)/1000 > HEARTBEAT_TIMEOUT){
    connected = false;
  }

  // Send a heartbeat to odroid
  send_heartbeat();

  // Decode any messages sent from the odroid
  recv_msg();

}


// Wrapper function to send heartbeat at a fixed rate
void send_heartbeat(){
  //store state between iterations
  static long last_heartbeat_send = 0;
  
  //send at an interval
  if(millis() - last_heartbeat_send > 1000/HEARTBEAT_RATE){
    send_heartbeat(mode,errors);
    last_heartbeat_send = millis();
  }
}

// Wrapper function to send RC vals at a fixed rate
void send_vals(uint16_t throttle_val, uint16_t steering_val, uint16_t aux1_val, uint16_t aux2_val){
  //store state between iterations
  static long last_channels_in_send = 0;
  
  //send at an interval
  if(millis() - last_channels_in_send > 1000/CHANNELS_IN_RATE){
    send_channels_in(throttle_val,steering_val,aux1_val,aux2_val);
    //send_debug(throttle_val,steering_val,aux1_val);
    last_channels_in_send = millis();
  }
}

// Handler function to receive heartbeat
void handle_heartbeat(uint8_t* payload){
  connected = true;
  last_heartbeat_recv = millis();
}

// Handler function to receive Control values
void handle_control(uint8_t* payload){
  msg_control_t control;
  decode_control(payload,&control);

  //echo it back as a channels_in msg
  //send_debug(control.throttle,control.steering,control.aux1);
  send_channels_in(control.throttle,control.steering,control.aux1,control.aux2);
}

// Handler function to receive setmode values
void handle_set_mode(uint8_t* payload){
  msg_set_mode_t msg;
  decode_set_mode(payload,&msg);
  mode = msg.mode;
}

// Receive function to handle incoming packets
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


// interrupt routine to read PPM
void read_ppm(){  //leave this alone
  static uint16_t pulse;
  static uint32_t counter;
  static uint8_t channel;

  counter = TCNT1;
  TCNT1 = 0;

  if(counter < 1020){  //must be a pulse if less than 510us
    pulse = counter;
  }
  else if(counter > 3820){  //sync pulses over 1910us
    channel = 0;
  }
  else{  //servo values between 510us and 2420us will end up here
    ppm[channel] = (counter + pulse)/2;
    channel++;
  }

  
}

