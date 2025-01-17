// const int flexPin = A0;          // Pin connected to voltage divider output
// const float VCC = 5.0;           // Arduino supply voltage
// const float R_DIV = 22.0;        // Resistor in voltage divider
// const float flatResistance = 10.0;  // Resistance when flat
// const float bendResistance = 30.0;  // Resistance when bent

// void setup() {
//   Serial.begin(9600);
//   pinMode(flexPin, INPUT);
// }

// void loop() {
//   // Read analog value
//   int ADCflex = analogRead(flexPin);
  
//   // Calculate voltage
//   float Vflex = ADCflex * VCC / 1023.0;
  
//   // Calculate resistance
//   float Rflex = R_DIV * (VCC / Vflex - 1.0);
//   Serial.println("Resistance: " + String(Rflex) + " ohms");
  
//   // Map resistance to bend angle
//   float angle = map(Rflex, flatResistance, bendResistance, 0, 90.0);
//   Serial.println("Bend: " + String(angle) + " degrees");
//   Serial.println();
  
//   delay(500);
// }

int flexPin = A0;
int flexPin2 = A1;
int flexPin3 = A2;
int flexPin4 = A3;
//const int ledPin = 3;
void setup()
{
  //pinMode(ledPin,OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  // int value = analogRead(flexPin);
  // Serial.println(value);
  // //value=map(value,700,1000,0,255);
  // //analogWrite(ledPin,value);
  // //analogWrite(ledPin,255);
  // delay(100);
  int rawValue1 = analogRead(flexPin); // Read the raw analog value
  int rawValue2 = analogRead(flexPin2);
  int rawValue3 = analogRead(flexPin3);
  int rawValue4 = analogRead(flexPin4);
  //Serial.print("Raw Value: ");

  //Serial.println(String(rawValue1) +","+ String(rawValue2)+","+ String(rawValue3)+","+ String(rawValue4));
  int average = (rawValue1 + rawValue2 + rawValue3 + rawValue4) / 4;
  Serial.println(average);
  // Map the raw value (1014-1022) to 0-180
  int mappedValue1 = map(rawValue1, 760, 926, 0, 180);
  int mappedValue2 = map(rawValue2, 1010, 1021, 0, 180);
  int mappedValue3 = map(rawValue3, 794, 960, 0, 180);
  int mappedValue4 = map(rawValue4, 1010, 1021, 0, 180);

  // // Ensure the value stays within the range 0-180
  // mappedValue = constrain(mappedValue, 0, 180);

  // Serial.print("Mapped Value: ");
  // Serial.println(mappedValue);
  //Serial.println(String(mappedValue1) +","+ String(mappedValue2)+","+ String(mappedValue3)+","+ String(mappedValue4));

  delay(100);
}