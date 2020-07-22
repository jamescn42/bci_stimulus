//Author: James Chen
//University of Calgary
//a3_ultrasonic_sensing.ino

//Contains functions related to ultrasonic object/drop detection


#if defined(ENABLE_ULTRASONIC)

#define trig0Pin 12
#define trig1Pin 13
#define trig2Pin A0
#define trig3Pin A1
#define trig4Pin A2

#define echo0Pin A3 // front
#define echo1Pin A4 // front left
#define echo2Pin A5 // front right
#define echo3Pin A6 // back
#define echo4Pin A7 // drop

void init_ultrasonic() {
  // Requires:  defined echo and trig pins (see above)
  // Promises: To set up pins for 5 ultrasonic sensor setup seen here:

  pinMode(trig0Pin, OUTPUT);
  pinMode(trig1Pin, OUTPUT);
  pinMode(trig2Pin, OUTPUT);
  pinMode(trig3Pin, OUTPUT);
  pinMode(trig4Pin, OUTPUT);

  pinMode(echo0Pin, INPUT);
  pinMode(echo1Pin, INPUT);
  pinMode(echo2Pin, INPUT);
  pinMode(echo3Pin, INPUT);
  pinMode(echo4Pin, INPUT);
}

void record_distances() {
  // Requires:  ultrasonic_distance array to store detected distances in
  // Promises:  Detects the distances the ultrasonic arrays are sencing, puts values into
  //            ultrasonic_distance array in cm

  ultrasonic_distance[0] = sonar_pin(trig0Pin, echo0Pin);//f
  ultrasonic_distance[1] = sonar_pin(trig1Pin, echo1Pin);//fl
  ultrasonic_distance[2] = sonar_pin(trig2Pin, echo2Pin);//fr
  ultrasonic_distance[3] = sonar_pin(trig3Pin, echo3Pin);//b
  ultrasonic_distance[4] = sonar_pin(trig4Pin, echo4Pin);//drop

  Serial.println("***************");
  for (int i = 0; i < 5; i++) {
    Serial.print(i);
    Serial.println(ultrasonic_distance[i]);
  }
}

double sonar_pin(int trig, int echo) {
  // Clears the trigPin
  digitalWrite(trig, LOW);
  delayMicroseconds(2);

  // Sets the trigPin HIGH for 10 microseconds
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH);
  return duration * 0.0343 / 2;
}

#endif
