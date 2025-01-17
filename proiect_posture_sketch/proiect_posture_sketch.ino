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
  int rawValue = analogRead(flexPin); // Read the raw analog value
  //Serial.print("Raw Value: ");
  Serial.println(rawValue);

  // Map the raw value (1014-1022) to 0-180
  // int mappedValue = map(rawValue, 1014, 1022, 0, 180);

  // // Ensure the value stays within the range 0-180
  // mappedValue = constrain(mappedValue, 0, 180);

  // Serial.print("Mapped Value: ");
  // Serial.println(mappedValue);

  delay(100);
}