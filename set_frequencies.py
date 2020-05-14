#Author: James Chen
#University of Calgary
import serial
import time
        
def set_freq(freq1, freq2, freq3, freq4):
    """Sets the frequency what the lights flash at
    freq<numb> (int): a positive 3 digit integer frequency 

    """
    if not (0<freq1<999 or 0<freq2<999 or 0<freq3<999 or 0<freq4<999):
        print("That frequency is out of bounds! Please choose a diffrent frequency (0<freq<999)")
        return
    
    ser.flush()
    message = f'{freq1:03}'+','+f'{freq2:03}'+','+f'{freq3:03}'+','+f'{freq4:03}'+','
    ser.write(message.encode('utf-8'))
    

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    
    set_freq(13, 17, 19, 23)
