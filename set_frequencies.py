# Author: James Chen
# University of Calgary

import serial
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog


class FrequencyConfig(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, padding=5)
        self.grid(sticky=tk.N+tk.S+tk.W+tk.E)
        self.makewidgets()

    def makewidgets(self):
        # title label
        ttk.Label(self, text='Set Frequencies for SSVEP',
                  font=("Verdana", 16)).grid(column=0, row=0, columnspan=2)

        self.freqs = [1, 1, 1, 1]
        self.boxes = []
        # frequency 1
        ttk.Label(self, text='Frequency for LED 1 (Hz):').grid(
            column=0, row=1)
        self.boxes.append(tk.Text(self, width=15, height=1))
        self.boxes[0].grid(column=1, row=1, sticky='W')

        # frequency 2
        ttk.Label(self, text='Frequency for LED 2 (Hz):').grid(
            column=0, row=2)
        self.boxes.append(tk.Text(self, width=15, height=1))
        self.boxes[1].grid(column=1, row=2, sticky='W')

        # frequency 3
        ttk.Label(self, text='Frequency for LED 3 (Hz):').grid(
            column=0, row=3)
        self.boxes.append(tk.Text(self, width=15, height=1))
        self.boxes[2].grid(column=1, row=3, sticky='W')

        # frequency 4
        ttk.Label(self, text='Frequency for LED 4 (Hz):').grid(
            column=0, row=4)
        self.boxes.append(tk.Text(self, width=15, height=1))
        self.boxes[3].grid(column=1, row=4, sticky='W')

        # set frequencies button
        ttk.Button(self, text='Set Frequencies', command=self.set_freq).grid(
            column=0, row=5, columnspan=2)

    def set_freq(self):
        for i in range(4):
            try:
                if(0 < int(self.boxes[i].get('1.0', tk.END+'-1c')) <= 100):
                    self.freqs[i] = int(self.boxes[i].get('1.0', tk.END+'-1c'))
                else:
                    messagebox.showinfo(
                        "Error", "That frequency is out of bounds! Please choose a diffrent frequency (0<freq<=100)")
            except:
                pass

        ser.flush()
        message = f'{self.freqs[0]:03}'+','+f'{self.freqs[1]:03}' + \
            ','+f'{self.freqs[2]:03}'+','+f'{self.freqs[3]:03}'+','
        ser.write(message.encode('utf-8'))


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    root = tk.Tk()
    FrequencyConfig(root)
    root.mainloop()
