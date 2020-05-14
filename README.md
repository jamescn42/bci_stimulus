# BCI SSVEP Stimulus
Author: James Chen

Python script controls Arduino MEGA to flash 4 LED's at frequencies between 1 and 999
Note: Acutal Frequency will be sleightly lower then desired. Around 99% accuracy

 

# How to run this program
Upload `pi_to_arduino.ino` to arduino MEGA and connect 4 LED's as well as resistors to corrosponding pins (2,3,4,5), see wiring diagram. Run `set_frequencies.py` on Raspberry Pi with USB cable (same one to program Arduino). To change frequencies, change values on line 24, in `set_frequencies.py` to desired frequencies. 


Wiring Diagram:
`to come!`