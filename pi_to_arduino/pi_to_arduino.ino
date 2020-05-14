//Author: James Chen
//University of Calgary

int LED_array [3][4] = {
  {2, 3, 4, 5}
  , {1, 1, 1, 1}
  , {0, 0, 0, 0}
};

long last_switch[4] = {0, 0, 0, 0};
int begin_leds = 0;

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(LED_array[0][i], OUTPUT);
  };
  Serial.begin(9600);
}

void loop() {
  set_frequency();
  if (begin_leds)
    run_leds();

  Serial.print(LED_array[1][0]);
  Serial.print(",");
  Serial.print(LED_array[1][1]);
  Serial.print(",");
  Serial.print(LED_array[1][2]);
  Serial.print(",");
  Serial.println(LED_array[1][3]);
}

void set_frequency() {
  //Requires: Properly formatted last_switch and LED_array[2][i] arrays with valid values
  //          and LED pins properly initiated. In addition, a properly statically declared
  //          int begin_leds
  //Promises: Updates LED_array with new frequencies from serial data input (from Raspberry Pi)  
  
  if (Serial.available() > 0) {
    for (int i = 0; i < 4; i++) {
      LED_array[1][i] = 0;
    }

    String data = Serial.readStringUntil('\n');
    int k = 0;
    int j = 0;
    char freq[3];

    for (int i = 0; i < data.length(); i++) {
      if (data[i] != ',') {
        freq[ k] = data[i];
        k++;
      }
      else {
        k = 0;
        //convert freq str to int
        int final_freq = (int(freq[0]) - 48) * 100 + (int(freq[1]) - 48) * 10 + (int(freq[2]) - 48);
        LED_array[1][j] = final_freq;
        j++;
        freq[0] = '\0';
        freq[1] = '\0';
        freq[2] = '\0';
      }
    }

    for (int i = 0; i < 4; i++) {
      last_switch[i] = millis();
    }
  }
  begin_leds = 1;
}

void run_leds() {
  //Requires: Properly formatted last_switch and LED_array[2][i] arrays with valid values
  //          and LED pins properly initiated.
  //Promises: Occilates LED's at the correct frequency in LED_array
  for (int i = 0; i < 4; i++) {
    if (millis() - last_switch[i] > 1000 / LED_array[2][i]) {
      digitalWrite(LED_array[0][i], !digitalRead(LED_array[0][i]));
      last_switch[i] = millis();
    }
  }
}

