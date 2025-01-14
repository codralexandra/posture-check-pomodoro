#define flex_pin A0

int threshold = 600; //modify this 

void setup() {
  Serial.begin(9600);
}

void loop() {
  int flex_value = analogRead(flex_pin);
  Serial.println(flexVal);
  delay(1000);
}
