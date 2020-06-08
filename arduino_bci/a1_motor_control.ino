//Author: James Chen
//University of Calgary
//a1_motor_control.ino

//Contains fuctions related to driving the wheelchair motors

void drive_motor(String data) {
  //Requires: valid properly formatted data sting
  //Promises: outputs PWM for drive direction

  //TODO: code for output of direction of control.
  //      dependent on type of motor controller/wheelchair output

  char direc = data[2];
  switch (direc) {
    case 'f':
      //code for forward direction
      break;
    case 'b':
      //code for back direction
      break;
    case 'l':
      //code for left direction
      break;
    case 'r':
      //code for right direction
      break;
  }
}
