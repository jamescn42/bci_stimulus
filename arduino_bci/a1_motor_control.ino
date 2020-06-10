//Author: James Chen
//University of Calgary
//a1_motor_control.ino

//Contains functions related to driving the wheelchair motors

void drive_motor(String data) {
  //Requires: valid properly formatted data sting
  //Promises: outputs PWM for drive direction, NOTE 'l' means rotate left (CCW), 'r' means rotate right(CW)

  //TODO: code for output of direction of control.
  //      dependent on type of motor controller/wheelchair output

  char direc[] = {data[2], data[3], '\0'};
  switch (direc) {
    case "nn":
      if(ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30){
        //code for n direction
      }
      break;
    case "ww":
      if (ultrasonic_distance[3] >30){
        //code for w direction
      }
      break;
    case "ss":
      if (ultrasonic_distance[1] >30){
        //code for s direction
      }
      break;
    case "ee":
      if (ultrasonic_distance[2] >30){
        //code for e direction
      }
      break;
    case "nw":
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic distance[2] >30){
        //code for nw direction
      }
      break;
    case "ne":
      if (ultrasonic_distance[0] > 30 && ultrasonic_distance[4] < 30 && ultrasonic distance[3] >30){
        //code for ne direction
      }
      break;
    case "se":
      if (ultrasonic_distance[1] >30){
        //code for se direction
      }
      break;
    case "sw":
      if (ultrasonic_distance[1] >30){
        //code for sw direction
      }
      break;
  }
}
