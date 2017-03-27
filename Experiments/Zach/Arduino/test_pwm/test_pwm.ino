#define pulse_width 333
#define output_pin 10

void setup()
{
  pinMode(output_pin, OUTPUT);
}

void loop()
{
  digitalWrite(output_pin, HIGH);
  delay(pulse_width); //  10% duty cycle @ 1KHz
  digitalWrite(output_pin, LOW);
  delay(1000 - pulse_width);
}
