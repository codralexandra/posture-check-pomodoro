#define flex_pin1 A0
#define flex_pin2 A1
#define flex_pin3 A2
#define flex_pin4 A3

int threshold = 600; //modify this 

void setup() {
  Serial.begin(9600);
}

void loop() {
  int flex_value1 = analogRead(flex_pin1);
  int flex_value2 = analogRead(flex_pin2);
  int flex_value3 = analogRead(flex_pin3);
  int flex_value4 = analogRead(flex_pin4);
  Serial.print(flex_value1);
  Serial.print(",");
  Serial.print(flex_value2);
  Serial.print(",");
  Serial.print(flex_value3);
  Serial.print(",");
  Serial.println(flex_value4);
  delay(200);
}