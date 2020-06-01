//Author: James Chen
//University of Calgary

//Decomment to activate debugging mode. Will run 299 trials of instantaneous 
//frequency for LEDs. Eachy trail consitsts of LED switching from on to off, vice versa
//NOTE if LED's set at diffrent frequencies, will give diffrent frequencies in "random order"

//#define DEBUG


// set up Arrays
int LED_array [3][16];
double last_switch[16];

// global variables 
boolean delay_phase = true;
boolean begin_leds = false;
int number_LED = 0;

void setup() {
  Serial.begin(9600);
}

//degugging code
#if defined(DEBUG)
static double results [300];
static int results_index = 0;
#endif

void loop() {

  if (Serial.available() > 0) {
    //read data from serial
    String data = Serial.readStringUntil('\n');

    //check if stimulus input
    if (data[0] == 's'){
      //FORMAT: "s/001023090"----stimulus input data, pin 001, 23 hz, 90degree phase shift
        set_stimulus(data);
    }

    //add motor code
    if (data[0] == 'd'){
        //FORMAT: 'd/f' -- drive input data: go forwards; 'f'-forwards, 'r'-reverse, 'l' -left, 'r'-right
        drive_motor(data);
    }
  }

  if (begin_leds){
    run_leds();

    //debugging code
#if defined(DEBUG)
    if(results_index > 299){
      double sum = 0;
      Serial.println("Instantaneous Frequency:");
      for(int i=0; i<300; i++){
        Serial.println(500/results[i]);
        sum+= 500/results[i];
      }
      Serial.println("Average frequency over 300 samples:");
      Serial.println(sum/300);
      delay(100000);
    }
#endif
  }
}

void set_stimulus(String data) {
  //Requires: Properly formatted string data with frequencies to set from raspberry pi
  //          Properly declared last_switch and LED_array[2][i] arrays 
  //          In addition, a properly statically declared int begin_leds amd number_LED
  //Promises: Updates LED_array with new pins, frequencies, phase angles from from Raspberry Pi 

  //get number of active pins
  number_LED = 0;
  for (int i = 2; i < data.length(); i++){
    if (data[i] == ';')
      number_LED++;
  }
  
  delay_phase = true;
  int pin_num = 0;    //seperates pin#
  int data_num = 0;   //seperates data in each pin#

  //store sting of data, convert after
  char pin_char[2];         //store pin# char
  char freq_char[2];       //store freq chars
  char phase_char[3];       //store phase char

  //extract data out of serial
  int j = 0;
  for (int i = 2; i < data.length(); i++) {
    if(data[i]==','){
      data_num++;
    }
    else if(data[i]==';'){
      //convert string into int
      LED_array[0][pin_num]= (int(pin_char[0]) - 48) * 10 + (int(pin_char[1]) - 48);
      LED_array[1][pin_num]= (int(freq_char[0]) - 48) * 10 + (int(freq_char[1]) - 48);
      LED_array[2][pin_num]= (int(phase_char[0]) - 48) * 100 + (int(phase_char[1]) - 48) * 10 + (int(phase_char[2]) - 48);

      data_num = 0;
      pin_num++;

    }
    else if(data_num==0){
      pin_char[j] = data[i];
      if(j==1){
        j=0;
      }
      else{
        j++;
      }
    }
    else if(data_num==1){
      freq_char[j] = data[i];
      if(j==1){
        j=0;
      }
      else{
        j++;
      }
    }
    else if(data_num==2){
      phase_char[j] = data[i];
      if(j==2){
        j=0;
      }
      else{
        j++;
      }
    }
  }

  //begins the LED switching updates and initalizes all pins to output
  for (int i = 0; i < number_LED; i++) {
    last_switch[i] = micros()/1000.0;
    pinMode(LED_array[0][i], OUTPUT);
    digitalWrite(LED_array[0][i], HIGH);
  }
  begin_leds = true;

}

void run_leds() {
  //Requires: Properly formatted last_switch and LED_array[2][i] arrays with valid values
  //          and LED pins properly initiated.
  //Promises: Occilates LED's at the correct frequency in LED_array
  for (int i = 0; i < number_LED; i++) {
    if (delay_phase){
      last_switch[i] += LED_array[2][i]/360.0*1000/LED_array[1][i];
    }
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
  delay_phase = false;
}

void drive_motor(string data){
  //Requires: valid properly formatted data sting
  //Promises: outputs PWM for drive direction

  //TODO: code for output of direction of control.
  //      dependent on type of motor controller/wheelchair output

  char direction = data[2];
  switch (direction){
    case 'f':
      //code for forward direction
      break;
    case 'r':
      //code for reverse direction
      break;
    case 'l':
      //code for left direction
      break;
    case 'r':
      //code for right direction
      break;
  }
}