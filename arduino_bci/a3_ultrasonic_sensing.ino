//Author: James Chen
//University of Calgary
//a3_ultrasonic_sensing.ino

//Contains functions related to ultrasonic object/drop detection

#define trig0Pin 22
#define trig1Pin 24
#define trig2Pin 26
#define trig3Pin 28
#define trig4Pin 30

#define echo0Pin 32 // front
#define echo1Pin 34 // front left
#define echo2Pin 36 // front right
#define echo3Pin 38 // back
#define echo4Pin 40 // drop

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

  ultrasonic_distance[0] = sonar_pin(trig0Pin, echo0Pin);
  ultrasonic_distance[1] = sonar_pin(trig1Pin, echo1Pin);
  ultrasonic_distance[2] = sonar_pin(trig2Pin, echo2Pin);
  ultrasonic_distance[3] = sonar_pin(trig3Pin, echo3Pin);
  ultrasonic_distance[4] = sonar_pin(trig4Pin, echo4Pin);
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
