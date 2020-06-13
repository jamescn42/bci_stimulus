//Author: James Chen
//University of Calgary
//b1_loop.ino

//setup and loops for arduino (compile last)

void setup() {
  init_motors();
  init_ultrasonic();
  Serial.begin(9600);
}

void loop() {
  
  record_distances();
  
  if (Serial.available() > 0) {
    //read data from serial
    String data = Serial.readStringUntil('\n');

    //check if stimulus input
    if (data[0] == 's') {
      //FORMAT: "s/001023090"----stimulus input data, pin 001, 23 hz, 90degree phase shift
      set_stimulus(data);
    }

    //add motor code
    if (data[0] == 'd') {
      //FORMAT: 'd/nn' -- drive input data: go north; nn, nw, ne, se,ss,sw,ee,ww
      drive_motor(data);
    }
  }

  if (begin_leds) {
    run_leds();

    //debugging code
#if defined(DEBUG_freq)
    if (results_index > 299) {
      double sum = 0;
      Serial.println("Instantaneous Frequency:");
      for (int i = 0; i < 300; i++) {
        Serial.println(500 / results[i]);
        sum += 500 / results[i];
      }
      Serial.println("Average frequency over 300 samples:");
      Serial.println(sum / 300);
      delay(100000);
    }
#endif
  }
}
