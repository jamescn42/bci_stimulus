//Author: James Chen
//University of Calgary
//arduino_bci_nano.ino

//Declaration and initialization of global variables

//Uncomment to activate debugging mode. Will run 299 trials of instantaneous
//frequency for LEDs. Each trail consists of LED switching from on to off, vice versa
//NOTE if LED's set at different frequencies, will give different frequencies in "random order"

//#define DEBUG_freq

//Uncomment to activate ultrasonic sensing, note this may effect accuracy of SSVEP led
//frequencies

//#define ENABLE_ULTRASONIC

//Comment/Uncomment to switch between motor configurations type, Two_AXIS defined when
//Car has one drive motor, one steering, else will assume 1 motor per side.

#define TWO_AXIS
//define TWO_MOTOR




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
