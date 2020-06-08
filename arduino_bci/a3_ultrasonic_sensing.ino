//Author: James Chen
//University of Calgary
//a3_ultrasonic_sensing.ino

//Contains functions related to ultrasonic object/drop detection


#define trigPin 22
#define echo0Pin 24 // front
#define echo1Pin 26 // front left
#define echo2Pin 28 // front right
#define echo3Pin 30 // back
#define echo4Pin 32 // drop

void init_ultrasonic() {
  // Requires:  defined echo and trig pins (see above)
  // Promises: To set up pins for 5 ultrasonic sensor setup seen here:

  pinMode(trigPin, OUTPUT);
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

  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin HIGH for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  //records time for signal to return
  long duration[5];
  duration[0] = pulseIn(echo0Pin, HIGH);
  duration[1] = pulseIn(echo1Pin, HIGH);
  duration[2] = pulseIn(echo2Pin, HIGH);
  duration[3] = pulseIn(echo3Pin, HIGH);
  duration[4] = pulseIn(echo4Pin, HIGH);

  //calculated distance based on duration in cm
  for (int i = 0; i < 5; i++) {
    ultrasonic_distance[i] = duration[i] * 0.0343 / 2;
  }
}
