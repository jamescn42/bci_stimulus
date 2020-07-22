//Author: James Chen
//University of Calgary
//arduino_bci.ino

//Declaration and initalization of global variables

//Uncomment to activate debugging mode. Will run 299 trials of instantaneous
//frequency for LEDs. Each trail consists of LED switching from on to off, vice versa
//NOTE if LED's set at different frequencies, will give different frequencies in "random order"

//#define DEBUG_freq

//uncomment to activate ultrasonic sencing, note this may effect accuracy of SSVEP led
//frequencies

//#define ENABLE_ULTRASONIC


// set up Arrays
int LED_array [3][16];      //LED data array
double last_switch[16];     //Time of last switch

double ultrasonic_distance[5] = {100, 100, 100, 100, 10};

// global variables
boolean delay_phase = true;
boolean begin_leds = false;
int number_LED = 0;

//debugging code
#if defined(DEBUG_freq)
static double results [300];
static int results_index = 0;
#endif
