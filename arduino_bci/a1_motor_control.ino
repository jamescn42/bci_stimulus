//Author: James Chen
//University of Calgary
//a1_motor_control.ino

//Contains functions related to driving the wheelchair motors

void drive_motor(String data) {
  //Requires: valid properly formatted data sting
  //Promises: outputs PWM for drive direction, NOTE 'l' means rotate left (CCW), 'r' means rotate right(CW)

  //TODO: code for output of direction of control.
  //      dependent on type of motor controller/wheelchair output

  char direc = data[2];
  switch (direc) {
    case 'f':
      if(ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30){
        //code for forward direction
      }
      break;
    case 'b':
      if (ultrasonic_distance[3] >30){
        //code for back direction
      }
      break;
    case 'l':
      if (ultrasonic_distance[1] >30){
        //code for left direction
      }
      break;
    case 'r':
      if (ultrasonic_distance[2] >30){
        //code for right direction
      }
      break;
  }
}
