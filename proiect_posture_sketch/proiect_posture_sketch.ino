#define flex_pin A0

int threshold = 600; //modify this 

void setup() {
  Serial.begin(9600);
}

void loop() {
  int flex_value = analogRead(flex_pin);
  Serial.println(flex_value);
  delay(1000);
}