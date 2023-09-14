/*
Team:11
Task:7.2
*/

#include <PID_v1.h>

double Setpoint ; // will be the desired value
double Input; // Water Flow sensor
double Output ; //Water pump
//PID parameters
double Kp=0, Ki=10, Kd=0; 
 
//create PID instance 
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
 
void setup()
{
  
  Serial.begin(9600);   
  //Hardcode the brigdness value
  Setpoint = 90; /*90 CFM*/
  //Turn the PID on
  myPID.SetMode(AUTOMATIC);
  //Adjust PID values
  myPID.SetTunings(Kp, Ki, Kd);
}
 
void loop()
{
  //Read the value from the Water Flow sensor. Analog input : 0 to 1024. We map is to a value from 0 to 255 as it's used for our PWM function.
  Input = map(analogRead(5), 0, 1024, 0, 255);  // Water Flow sensor is set on analog pin 5
  //PID calculation
  myPID.Compute();
  //Write the output as calculated by the PID function
  analogWrite(3,Output); //Water pump driver is set to digital 3 this is a pwm pin. 
  //Send data by serial for plotting 
  Serial.print(Input);
  Serial.print(" ");
  Serial.println(Output);
  Serial.print(" ");  
  Serial.println(Setpoint);
//  delay(100); 
}
