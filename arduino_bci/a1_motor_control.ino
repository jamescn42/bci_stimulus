//Author: James Chen
//University of Calgary
//a1_motor_control.ino

//Contains functions related to driving the wheelchair motors

//for testing, 4 led's 2 green, 2 red for f/b on l/r sides. 
#define TESTING_motors

#define forwards_left 2
#define backwards_left 3
#define forwards_right 4
#define backwards_right 5

void init_motors(){
  pinMode(forwards_left, OUTPUT);
  pinMode(forwards_right, OUTPUT);
  pinMode(backwards_left, OUTPUT);
  pinMode(backwards_right, OUTPUT);
}

void drive_motor(String data) {
  //Requires: valid properly formatted data sting
  //Promises: outputs PWM for drive direction, NOTE 'l' means rotate left (CCW), 'r' means rotate right(CW)

  //TODO: code for output of direction of control.
  //      dependent on type of motor controller/wheelchair output

  int direc= data[2]+ data[3];
  switch (direc) {
    case ('n'+'n'):
      if(ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30){
        digitalWrite(forwards_left, HIGH);
        digitalWrite(forwards_right, HIGH);
      }
      break;
    case ('w'+'w'):
      if (ultrasonic_distance[3] >30){
        digitalWrite(backwards_left, HIGH);
        digitalWrite(forwards_right, HIGH);
      }
      break;
    case ('s'+'s'):
      if (ultrasonic_distance[1] >30){
        digitalWrite(backwards_left, HIGH);
        digitalWrite(backwards_right, HIGH);
      }
      break;
    case ('e'+'e'):
      if (ultrasonic_distance[2] >30){
        digitalWrite(forwards_left, HIGH);
        digitalWrite(backwards_right, HIGH);
      }
      break;
    case ('n'+'w'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic_distance[2] >30){
        analogWrite(forwards_left, 128);
        digitalWrite(forwards_right, HIGH);
      }
      break;
    case ('n'+'e'):
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic_distance[3] >30){
        digitalWrite(forwards_left, HIGH);
        analogWrite(forwards_right, 128);
      }
      break;
    case ('s'+'e'):
      if (ultrasonic_distance[1] >30){
        digitalWrite(backwards_left, HIGH);
        analogWrite(backwards_right, 128);
      }
      break;
    case ('s'+'w'):
      if (ultrasonic_distance[1] >30){
        analogWrite(backwards_left, 128);
        digitalWrite(backwards_right, HIGH);
      }
      break;
    case ('0'+'0'):
      digitalWrite(forwards_left, LOW);
      digitalWrite(forwards_right, LOW);
      digitalWrite(backwards_left, LOW);
      digitalWrite(backwards_right, LOW);
  }
}
