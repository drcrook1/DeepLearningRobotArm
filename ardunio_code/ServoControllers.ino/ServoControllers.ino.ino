// Deep Learning Robotic Arm Project
// Kevin Leung @KSLHacks
// Hao Luo @howlowck

// include the servo library
#include <Servo.h>

Servo swivelServo;  // create a servo object
Servo liftServo;
Servo reachServo;
Servo clawServo;

int const potPin = A0; // analog pin used to connect the potentiometer

int const stickXPin = A1;
int const stickYPin = A2;
int const stickSwitchPin = A3;

  //Potentiometer for lift
  /**********************
   *   ||  ||  ||
   *   ------------ 
   *  |            |
   *  | 0     1000 |
   *  |            |
   *  |____________|
   */
int potVal;  // variable to read the value from the analog pin
  // Joy Stick for swivel and reach
  /******************
   *    ||  ||  ||
   *    ||  ||  ||
   *   ------------ 
   *  |     0x     |
   *  |            |
   *  | 1000y    0y|
   *  |            |
   *  |    1000x   |
   *  |____________|
   */
int stickXVal;
int stickYVal;
int stickSwitchVal;
int middleXVal;
int middleYVal;

int prevStickXVal;
int prevStickYVal;

int swivelAngle;   // variable to hold the angle for the servo motor
int liftAngle;
int reachAngle;
bool openClaw;

void setup() {
  int prevStickXVal = 500;
  int prevStickYVal = 500;
  reachAngle = 90;
  liftAngle = 90;
  openClaw = false;
  
  // set the servo pins
  swivelServo.attach(8); // attaches the servo on pin 8 to the servo object
  liftServo.attach(7);
  reachServo.attach(4);
  clawServo.attach(2);
  
  // set starting position 
  swivelServo.write(90);
  delay(500);
  reachServo.write(90);
  delay(500);
  clawServo.write(-90);
  delay(500);

  middleXVal = analogRead(stickXPin);
  middleYVal = analogRead(stickYPin);
  
  Serial.begin(9600); // open a serial connection to your computer
}

void loop() {
  //
  // read values from input controls
  potVal = analogRead(potPin); 
  stickXVal = analogRead(stickXPin);
  stickYVal = analogRead(stickYPin);
  stickSwitchVal = analogRead(stickSwitchPin);

  //
  // print out the value to the serial monitor
  Serial.print("potVal: ");
  Serial.print(potVal);

  Serial.print("  stickXVal: ");
  Serial.print(stickXVal);
  
  Serial.print("  stickYVal: ");
  Serial.print(stickYVal);

  Serial.print("  stickSwitchVal: ");
  Serial.println(stickSwitchVal);

  //
  // scale the numbers from the inputs and set angles
  //swivelAngle = map(potVal, 0, 1023, 0, 179);
  swivelAngle = swivelAngle + 2*(map((middleYVal - stickYVal), -500, 500, -5, 5));
  if (swivelAngle < 0) {
    swivelAngle = 0;
  }
  if (swivelAngle > 180) {
    swivelAngle = 180;
  }

  // prevStickXVal = 500 stickXVal = 0 (joystick moves up) (arm reachs out)
  reachAngle = reachAngle + 2*(map((middleXVal - stickXVal), -500, 500, -5, 5));
  liftAngle = map(potVal, 0, 1023, 0, 179);

  //
  // check if joystick button is clicked
  // if so, change state of the boolean value
  if (stickSwitchVal == 0) {
    openClaw = !openClaw;
  }

  //
  // set the servo position
  swivelServo.write(swivelAngle);
  reachServo.write(reachAngle);
  liftServo.write(liftAngle);
  if (openClaw == true) {
    clawServo.write(45);
  } else {
    clawServo.write(-90);
  }

  Serial.print("liftAngle: ");
  Serial.print(liftAngle);

  Serial.print("  reachAngle: ");
  Serial.print(reachAngle);
  
  Serial.print("  swivelAngle: ");
  Serial.print(swivelAngle);

  Serial.print("  openClaw: ");
  Serial.println(openClaw);
  Serial.println();

  // wait for the servo to get there
  delay(10);
  prevStickXVal = stickXVal;
  prevStickYVal = stickYVal;

}


