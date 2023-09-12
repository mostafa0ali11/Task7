const int softStartDuration = 2000; 
const float alpha = 0.2; 

const int motorPin = 9;

unsigned long startTime; 
float filteredValue = 0.0; 
int desiredValue = 0; 

void setup() {
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    desiredValue = Serial.parseInt();
    Serial.print("Desired Speed: ");
    Serial.println(desiredValue);
    startTime = millis(); 
  }
  unsigned long elapsedTime = millis() - startTime;

  float filterFactor = min(1.0, (float)elapsedTime/softStartDuration);
  float softStartValue = filterFactor * desiredValue;

  filteredValue = (alpha * softStartValue)+((1 - alpha) * filteredValue);

  int motorSpeed = map(filteredValue, 0, 1023, 0, 255);

  analogWrite(motorPin, motorSpeed);
}
