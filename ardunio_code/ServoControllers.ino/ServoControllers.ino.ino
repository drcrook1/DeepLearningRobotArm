// Deep Learning Robotic Arm Project
// Kevin Leung @KSLHacks
// Hao Luo @howlowck

// include the servo library
#include <Servo.h>

Servo swivelServo;  // create a servo object
Servo liftServo;
Servo reachServo;
Servo clawServo;

bool trainMode = true; 
bool waiting = true;

//INPUT BUTTONS
const int stopButtonPin = A5;
const int modeButtonPin = 13;
const int startButtonPin = A4;

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

  pinMode(stopButtonPin, INPUT);
  pinMode(startButtonPin, INPUT);
  pinMode(modeButtonPin, INPUT);
  
  // set the servo pins
  swivelServo.attach(8); // attaches the servo on pin 8 to the servo object
  liftServo.attach(7);
  reachServo.attach(4);
  clawServo.attach(3);
  
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

void trainloop()
{
   //
  // read values from input controls
  potVal = analogRead(potPin); 
  stickXVal = analogRead(stickXPin);
  stickYVal = analogRead(stickYPin);
  stickSwitchVal = analogRead(stickSwitchPin);
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
  if(reachAngle > 180){
    reachAngle = 180;
  } 
  else if(reachAngle < -180)
  {
    reachAngle = -180;
  }
  

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
  int clawAngle = 45;
  if (openClaw == true) {
    clawServo.write(45);
  } else {
    clawServo.write(-90);
    clawAngle = -90;
  }

  //send data to pi
  Serial.println("swivel,"+String(swivelAngle)+",reach,"+String(reachAngle)+",lift,"+String(liftAngle)+",claw,"+String(clawAngle));
  // wait for the servo to get there
  delay(10);
  prevStickXVal = stickXVal;
  prevStickYVal = stickYVal;
}

void performloop()
{
  String controls = Serial.readString();
  int commaIndex = controls.indexOf(',');
  //  Search for the next comma just after the first
  int secondCommaIndex = controls.indexOf(',', commaIndex + 1);
  int thirdCommaIndex = controls.indexOf(',', secondCommaIndex + 1);
  swivelAngle = controls.substring(0, commaIndex).toInt();
  reachAngle = controls.substring(commaIndex + 1, secondCommaIndex).toInt();
  liftAngle = controls.substring(secondCommaIndex + 1, thirdCommaIndex).toInt();
  int clawAngle = controls.substring(thirdCommaIndex + 1).toInt(); // To the end of the string
  swivelServo.write(swivelAngle);
  reachServo.write(reachAngle);
  liftServo.write(liftAngle);
  clawServo.write(clawAngle);
  delay(10);
}

void loop() {
 
  //read values from buttons
  //float stopState = analogRead(stopButtonPin);
  float startState = analogRead(startButtonPin);
  int modeState = digitalRead(modeButtonPin);
  
  if(startState < 5.0 && waiting == true)
  {
    if(modeState == 1)
        {
          Serial.println("start,train");
          trainMode = true;
        }
        else{
          Serial.println("start,perform");
          trainMode = false;
        }
        waiting = false;
  }

  //if(stopState < 1.0 && waiting == false)
  //{
    //Serial.println("stop");
    //waiting = true;
  //}
  //Serial.print("stop: ");
  //Serial.println(stopState);
  //Serial.print("start: ");
  //Serial.println(startState);
  delay(10);

  if(!waiting){
    if(trainMode){
      trainloop();
    }
    else {
      performloop();
    }
  }
}


