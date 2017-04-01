#include <Servo.h>

/*This program puts the servo values into an array,
 reagrdless of channel number, polarity, ppm frame length, etc...
 You can even change these while scanning!*/

#define PPM_Pin 3  //this must be 2 or 3
#define PWM_channel_1 6
#define PWM_channel_2 5
int ppm[16];  //array for storing up to 16 servo signals

Servo steering;

void setup()
{
  Serial.begin(115200);
  Serial.println("ready");

  pinMode(PPM_Pin, INPUT);
  attachInterrupt(PPM_Pin - 2, read_ppm, CHANGE);

  //pinMode(PWM_channel_1, OUTPUT);
  steering.attach(PWM_channel_1, 990, 2015);
  pinMode(PWM_channel_2, OUTPUT);

  TCCR2A = 0;  //reset timer1
  TCCR2B = 0;
  TCCR2B |= (1 << CS11);  //set timer1 to increment every 0,5 us
}

void loop()
{
  //You can delete everithing inside loop() and put your own code here
  int count;

  while(ppm[count] != 0){  //print out the servo values
    //Serial.print(ppm[count]);
    //Serial.print("  ");
    count++;
  }
  //Serial.println("");
  delay(100);  //you can even use delays!!!

  //int channel_1 = map(ppm[0], 990, 2015, 0, 255);
  int channel_1 = ppm[0];
  int channel_2 = map(ppm[1], 985, 2015, 0, 255);

  //analogWrite(PWM_channel_1, channel_1);
  steering.writeMicroseconds(channel_1);
  analogWrite(PWM_channel_2, channel_2);
  Serial.println("");
  Serial.print(channel_1);
  Serial.print("   ");
  Serial.print(channel_2);
}



void read_ppm(){  //leave this alone
  static unsigned int pulse;
  static unsigned long counter;
  static byte channel;

  counter = TCNT2;
  TCNT2 = 0;

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

