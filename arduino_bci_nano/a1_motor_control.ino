//Author: James Chen
//University of Calgary
//a1_motor_control.ino

//Contains functions related to driving the wheelchair motors

//for testing, 4 led's 2 green, 2 red for f/b on l/r sides.
#define TESTING_motors

//RIGHT MOTOR or DRIVE
#define IN1 2
#define IN2 3

//LEFT MOTOR or STEERING
#define IN3 4
#define IN4 5

void init_motors() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void drive_motor(String data) {
  //Requires: valid properly formatted data sting
  //Promises: outputs PWM for drive direction, NOTE 'l' means rotate left (CCW), 'r' means rotate right(CW)

  //TODO: code for output of direction of control.
  //      dependent on type of motor controller/wheelchair output

  int direc = data[2] + data[3];

//Code for two motor control, ie when device has one motor controling each side. 
#if defined(TWO_MOTOR)
  switch (direc) {
    case ('n'+'n'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      }
      break;
    case ('w'+'w'):
      if (ultrasonic_distance[3] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('s'+'s'):
      if (ultrasonic_distance[1] > 30) {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('e'+'e'):
      if (ultrasonic_distance[2] > 30) {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      }
      break;
    case ('n'+'w'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic_distance[2] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('n'+'e'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic_distance[3] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      }
      break;
    case ('s'+'e'):
      if (ultrasonic_distance[1] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('s'+'w'):
      if (ultrasonic_distance[1] > 30) {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('0'+'0'):
      digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
  }
#endif

//Code for Two Axis car control (if car has 2 axis, one for drive, one for steering)
#if defined(TWO_AXIS)
  switch (direc) {
    case ('n'+'n'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('w'+'w'):
      if (ultrasonic_distance[3] > 30) {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('s'+'s'):
      if (ultrasonic_distance[1] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      }
      break;
    case ('e'+'e'):
      if (ultrasonic_distance[2] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('n'+'w'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic_distance[2] > 30) {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('n'+'e'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic_distance[3] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
      }
      break;
    case ('s'+'e'):
      if (ultrasonic_distance[1] > 30) {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      }
      break;
    case ('s'+'w'):
      if (ultrasonic_distance[1] > 30) {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      }
      break;
    case ('0'+'0'):
      digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
  }
#endif
}
