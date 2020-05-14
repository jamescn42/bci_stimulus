//Author: James Chen
//University of Calgary

//Decomment to activate debugging mode. Will run 299 trials of instantaneous 
//frequency for LEDs. Eachy trail consitsts of LED switching from on to off, vice versa
//NOTE if LED's set at diffrent frequencies, will give diffrent frequencies in "random order"

//#define DEBUG

//First row gives Pin number, second row gives frequency (default 1)
int LED_array [2][4] = {
  {
    2, 3, 4, 5            }
  , {
    1, 1, 1, 1            }
};

double last_switch[4] = {
  0, 0, 0, 0};
boolean begin_leds = false;

void setup() {
  //initalize pins to output and begin serial data stream
  for(int i=0; i<4; i++){
    pinMode(LED_array[0][i], OUTPUT);
  }
  Serial.begin(9600);
  
}

//degugging code
#if defined(DEBUG)
  static double results [300];
  static int results_index = 0;
#endif

void loop() {
  set_frequency();
  if (begin_leds){
    run_leds();

//debugging code
#if defined(DEBUG)
    if(results_index > 299){
      Serial.println("the results are below:");
      for(int i=0; i<299; i++){
        Serial.println(500/results[i]);
      }
      delay(100000);

    }
#endif
  }
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

    //need to extract each frequency String
    for (int i = 0; i < data.length(); i++) {
      if (data[i] != ',') {
        freq[ k] = data[i];
        k++;
      }
      else {
        k = 0;
        //to do math, we must convert Frequency stirng to an int
        int final_freq = (int(freq[0]) - 48) * 100 + (int(freq[1]) - 48) * 10 + (int(freq[2]) - 48);
        LED_array[1][j] = final_freq;
        j++;
      }
    }
    
    //begins the LED switching updates
    for (int i = 0; i < 4; i++) {
      last_switch[i] = micros()/1000.0;
    }
    begin_leds = true;
  }
}

void run_leds() {
  //Requires: Properly formatted last_switch and LED_array[2][i] arrays with valid values
  //          and LED pins properly initiated.
  //Promises: Occilates LED's at the correct frequency in LED_array
  
  for (int i = 0; i < 4; i++) {
    if (micros()/1000.0 - last_switch[i] >= 500.0 / LED_array[1][i]) {

      //debugging code
#if defined(DEBUG)
      results[results_index] = micros()/1000.0 - last_switch[i];
      results_index++;
#endif

      //toggle LED on/off and update the last switched time
      digitalWrite(LED_array[0][i], !digitalRead(LED_array[0][i]));
      last_switch[i] = micros()/1000.0;
    }
  }
}
