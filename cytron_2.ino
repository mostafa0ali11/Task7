const float alpha = 0.2; 

const int motorPin = 9; 

float filteredValue = 0.0; 
int speedValue = 0; 

void setup() {
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    speedValue = Serial.parseInt();
    Serial.print("Desired Speed: ");
    Serial.println(speedValue);
  }
  filteredValue = (alpha * speedValue) + ((1 - alpha) * filteredValue);
  int motorSpeed = map(filteredValue, 0, 1023, 0, 255);
  analogWrite(motorPin, motorSpeed);
}
