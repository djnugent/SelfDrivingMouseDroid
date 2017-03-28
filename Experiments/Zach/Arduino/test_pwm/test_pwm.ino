#define pulse_width 333
#define output_pin 10
#define input_pin 3

int val = 0;
int read_val = 0;

void setup()
{
  pinMode(output_pin, OUTPUT);
  pinMode(input_pin, INPUT);
  Serial.begin(9600);
}

void loop()
{
  analogWrite(output_pin, val % 255);
  read_val = pulseIn(input_pin, HIGH);
  Serial.println(read_val);
  val++;
  delay(10);
}
