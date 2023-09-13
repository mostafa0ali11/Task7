/*
sketch belongs to this video: https://youtu.be/crw0Hcc67RY
write by Moz for YouTube changel logMaker360
4-12-2017
*/

#include <PID_v1.h>


double Setpoint = 90.0;  // Desired flow rate in CFM
double Input;            // Flow rate from the flow meter
double Output;           // Suction mechanism control
double Kp = 0.5;         // Proportional gain
double Ki = 0.2;         // Integral gain
double Kd = 0.1;         // Derivative gain
 
// Create PID instance
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
 
const int FLOW_METER_PIN = 2;
  
// Pin for the flow meter

void setup()
{
  Serial.begin(9600);

  // Initialize the flow meter
  pinMode(FLOW_METER_PIN, INPUT);

  // Turn on the PID
  myPID.SetMode(AUTOMATIC);

  //Adjust PID values
  myPID.SetTunings(Kp, Ki, Kd);

}

void loop()
{
  //Read the value from the light sensor. Analog input : 0 to 1024. We map is to a value from 0 to 255 as it's used for our PWM function.
  Input = map(analogRead(5), 0, 1024, 0, 255);  // photo senor is set on analog pin 5
  //PID calculation
  myPID.Compute();
  //Write the output as calculated by the PID function
  analogWrite(3,Output); //LED is set to digital 3 this is a pwm pin. 
  //Send data by serial for plotting 
  Serial.print("Input: ");
  Serial.print(Input);
  Serial.print(" CFM, Output: ");
  Serial.print(Output);
  Serial.println();
  Serial.println(Setpoint);

  // Delay for a suitable time before the next iteration
  delay(100);
} 
