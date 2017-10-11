#include "protocol.h"
#include "ServoTimer2.h"


//TODO
// Easy encode and decode errors

// Pin definitions
#define PPM_Pin 3  //this must be 2 or 3
#define PWM_channel_1 6
#define PWM_channel_2 5

// Channel Defintions
#define steering_channel 0 // l/r RIGHT STICK
#define throttle_channel 1 // up/dwn RIGHT STICK
#define mode_channel 5     // RIGHT SWITCH
#define aux1_channel 4     // LEFT SWITCH
#define aux2_channel 7     // MIDDLE SWITCH

uint16_t ppm[16];  //array for storing up to 16 servo signals

#define CHANNELS_IN_RATE 40 //hz

// Global state variables
float throttle_scale = 0.2;
bool RC_connected = false;
uint8_t errors = 0;
long last_heartbeat_recv = 0;
uint8_t mode = MODE_FAILSAFE;
uint16_t last_mode_us = 0;
uint16_t auto_steering_val = 1500;
uint16_t auto_throttle_val = 1500;
uint16_t auto_aux1_val = 1000;
uint16_t auto_aux2_val = 1000;

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

  // Extract and modify pulse data from global ppm array
  uint16_t throttle_val = (uint16_t) (1500 + (((float) (ppm[throttle_channel]) - 1500) * throttle_scale));
  uint16_t steering_val = ppm[steering_channel];
  uint16_t aux1_val = ppm[aux1_channel];
  uint16_t aux2_val = ppm[aux2_channel];
  
  // Send a heartbeat to odroid
  send_heartbeat();

  // Send values to odroid
  send_vals(throttle_val, steering_val, aux1_val, aux2_val);

  // Check for RC and Odroid Conntection
  detect_RC();
  detect_odroid();

  // Decode any messages sent from the odroid
  recv_msg();

  check_mode_change();

  if ((!odroid_connected && mode == MODE_AUTO) || !RC_connected) {
    mode = MODE_FAILSAFE;  
  }
  
  if (mode == MODE_FAILSAFE) {
    steering.write(1500);
    throttle.write(1500);
  } else if (mode == MODE_MANUAL) {
    steering.write(steering_val);
    throttle.write(throttle_val);
  } else if (mode == MODE_AUTO){
    steering.write(auto_steering_val);
    throttle.write(throttle_val);   // NOT USING AUTO THROTTLE
  }

}

// Change mode using RC switch
// But only rising and falling edges, not levels. 
// That way we don't override system failsafes
void check_mode_change(){
  uint16_t us_thresh = 490;
  uint16_t current_mode_us = ppm[mode_channel];
  // Check for rising or falling edge
  if(abs(current_mode_us - last_mode_us) > us_thresh){
    current_mode_us = ppm[mode_channel];
    // Auto
    if(current_mode_us > 1900){
      mode = MODE_AUTO;
      auto_steering_val = 1500;
      auto_throttle_val = 1500;
      auto_aux1_val = 1500;
      auto_aux2_val = 1500;
    }
    // Manual
    else if(current_mode_us > 1400){
      mode = MODE_MANUAL;
    }
    // Failsafe
    else{
      mode = MODE_FAILSAFE;
    }
    last_mode_us = ppm[mode_channel];
  }
}

// Check if odroid is still responding
void detect_odroid(){
  if((millis() - last_heartbeat_recv)/1000 > HEARTBEAT_TIMEOUT){
    odroid_connected = false;
  }
}

// Check if RC Controller is sending signals
void detect_RC() {
  if (ppm[1] < 930) {
    RC_connected = false;
  }
  else {
    RC_connected = true;
  }
}

// Handler function to receive heartbeat
void handle_heartbeat(uint8_t* payload){
  odroid_connected = true;
  last_heartbeat_recv = millis();
}

// Handler function to receive Control values
void handle_control(uint8_t* payload){
  msg_control_t control;
  decode_control(payload,&control);

  //echo it back as a channels_in msg
  //send_debug(control.throttle,control.steering,control.aux1);
  send_channels_in(control.throttle,control.steering,control.aux1,control.aux2);

  auto_steering_val = control.steering;
  auto_throttle_val = control.throttle;
  auto_aux1_val = control.aux1;
  auto_aux2_val = control.aux2;
}

// Handler function to receive setmode values
void handle_set_mode(uint8_t* payload){
  msg_set_mode_t msg;
  decode_set_mode(payload,&msg);
  //mode = msg.mode;
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
