# BCI SSVEP Stimulus
Author: James Chen

Contains multiple different methods to control an SSVEP BCI wheelchair system

**SSVEP LED Control**

Python script opens a GUI that controls Arduino MEGA to flash up to 16 groups of LED's at 
integer frequencies between 1Hz and 100Hz, as well as at different phases. (0, 90, 180, 270)
 Actual Frequency will be slightly lower then desired. Around 99% accuracy
 
 **Keyboard Control of Wheelchair**
 
 `keyboard_control.py` will open a program to send control signals to the wheelchair
 with a keyboard connected to the raspberry pi. (in-progress)
 
 **Arduino Code**
 
 The directory `/arduino_bci` contains code to upload to the Arduino, this code can will
 run the the LED frequencies, drive the wheelchair control systems and can sense obstacles
 and drops around the wheelchair (in-progress)
 
 

# How to run this program
Upload `/arduino_bci` to Arduino MEGA and connect all peripherals to Arduino (see 
possible circuit implementation). Run `set_frequencies.py` on 
Raspberry Pi by navigating to the correct directory in the terminal, and running `python3 
set_frequencies.py`. Ensure that the USB cable (same one to program Arduino) is plugged in
 for serial connection. This will open a GUI to set the desired LED frequencies and phases.
Running `keyboard_control.py` will similarly open a window for control of the wheelchair 
with a keyboard.

# Frequency Setting GUI:
![Screenshot of example GUI](images/gui_screenshot.png)

# Keyboard Control Window
![Screenshot of Keyboard control window](images/keyboard_control_window.png)

# Possible Circuit Implementation for LED's:
![Screenshot of example GUI](images/SSVEP_arduino_circuit_diagram.png)