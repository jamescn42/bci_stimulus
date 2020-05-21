# BCI SSVEP Stimulus
Author: James Chen

Python script opens a GUI that controls Arduino MEGA to flash upto 16 groups of LED's at integer frequencies between 1Hz and 100Hz, as well as at diffrent phases. (0, 90, 180, 270)

Note: Acutal Frequency will be sleightly lower then desired. Around 99% accuracy

# How to run this program
Upload `pi_to_arduino.ino` to arduino MEGA and connect LED's as well as resistors to corrosponding pins (see possible circuit implementation). Run `set_frequencies.py` on Raspberry Pi by navigating to the correct directory in the terminal, and running `python3 set_frequencies.py`. Ensure that the USB cable (same one to program Arduino) is plugged in for serial connection. This will open a GUI to set the desired LED frequencies and phases.

# Frequency Setting GUI:
![Screenshot of example GUI](gui_screenshot.png)

# Possible Circuit Implementation:
![Screenshot of example GUI](SSVEP_arduino_circuit_diagram.png)

Notes:
R1 should be selected so that it drops the rest of the voltage after the 3 LED's: R1 = (9V-3*[LED_Voltage]/0.02A)
NPN transistor should have a 5V Emitter-Base Voltage