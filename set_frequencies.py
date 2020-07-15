# Author: James Chen
# University of Calgary

# import serial
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Checkbutton
from tkinter import Spinbox


# TODO: Manual pin selection interface


class StimulusConfig(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, padding=5)
        self.grid(sticky=tk.N + tk.S + tk.W + tk.E)
        self.makewidgets()

        # extracted data
        self.freqs = []
        self.pins = []
        self.phase_vals = []

    def makewidgets(self):
        # tk elements
        self.ckbox = []
        self.freqbox = []
        self.phases = []

        # title label
        ttk.Label(self, text='Set Frequencies for SSVEP',
                  font=("Verdana", 16)).grid(column=0, row=0, columnspan=4)

        # Table header
        ttk.Label(self, text='  Pin  ').grid(column=0, row=1)
        ttk.Label(self, text='ON/OFF').grid(column=1, row=1)
        ttk.Label(self, text='  Frequency (Hz)  ').grid(column=2, row=1)
        ttk.Label(self, text='  Phase Angle (°)').grid(column=3, row=1)

        for i in range(16):
            # pin numbers
            ttk.Label(self, text=str(i * 2 + 23)).grid(
                column=0, row=i + 2)

            # check boxes
            self.ckbox.append(tk.IntVar())
            Checkbutton(self, variable=self.ckbox[i]).grid(column=1, row=i + 2)

            # frequency boxes
            self.freqbox.append(tk.Text(self, width=10, height=1))
            self.freqbox[i].grid(column=2, row=i + 2)

            # phase angles
            self.phases.append(Spinbox(self, values=(
                '0', '90', '180', '270'), width='5'))
            self.phases[i].grid(column=3, row=i + 2)

        # set frequencies button
        ttk.Button(self, text='Set Frequencies', command=self.set_freq, width=15).grid(
            column=0, row=19, columnspan=4)

    def set_freq(self):

        self.freqs = []
        self.pins = []
        self.phase_vals = []

        # extract data
        for i in range(16):
            if self.ckbox[i].get() == 1:
                # get frequencies
                try:
                    if 0 < int(self.freqbox[i].get('1.0', tk.END + '-1c')) <= 100:
                        self.freqs.append(
                            int(self.freqbox[i].get('1.0', tk.END + '-1c')))
                    else:
                        messagebox.showinfo(
                            "Error",
                            "That frequency is out of bounds! Please choose a different frequency (0<freq<=100)")
                        return
                except:
                    messagebox.showinfo(
                        "Error", "That frequency is out of bounds! Please choose a different frequency (0<freq<=100)")
                    return

                # get phases
                self.phase_vals.append(self.phases[i].get())

                # get pin number
                self.pins.append(i * 2 + 23)

        message = 's/'
        for i in range(len(self.pins)):
            message = message + \
                      f'{int(self.pins[i]):02}' + ',' + f'{self.freqs[i]:02}' + \
                      ',' + f'{int(self.phase_vals[i]):03}' + ';'
        message = message + '\n'

        # ser.flush()
        # ser.write(message.encode('utf-8'))


if __name__ == '__main__':
    # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    # ser.flush()

    root = tk.Tk()
    StimulusConfig(root)
    root.mainloop()
