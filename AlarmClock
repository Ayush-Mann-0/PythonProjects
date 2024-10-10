import tkinter as tk
from datetime import datetime
import os
import platform

# Setting initial global values
start_printed = False
stop_printed = True
done = False
finished = False
stop_clicked = False

class AlarmApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alarm Clock")
        self.resizable(width=False, height=False)

        # Set up variables
        self.hr = tk.IntVar(self)
        self.min = tk.IntVar(self)
        self.ampm = tk.StringVar(self)
        
        # Set initial values
        self.hr.set(12)
        self.min.set(0)
        self.ampm.set("AM")

        # Create dropdown lists
        hours = list(range(1, 13))
        minutes = [f"{y:02d}" for y in range(60)]
        ampmlist = ["AM", "PM"]

        self.popmenuhours = tk.OptionMenu(self, self.hr, *hours)
        self.popmenuminutes = tk.OptionMenu(self, self.min, *minutes)
        self.popmenuAMPM = tk.OptionMenu(self, self.ampm, *ampmlist)

        # Pack dropdowns
        self.popmenuhours.pack(side="left")
        tk.Label(text=":").pack(side="left")
        self.popmenuminutes.pack(side="left")
        self.popmenuAMPM.pack(side="left")

        # Set up buttons
        self.alarmbutton = tk.Button(self, text="Set Alarm", command=self.start_clock)
        self.cancelbutton = tk.Button(self, text="Cancel Alarm", command=self.stop_clock, state="disabled")
        self.stopalarmbutton = tk.Button(self, text="Stop Alarm", command=self.stop_audio, state="disabled")

        self.alarmbutton.pack()
        self.cancelbutton.pack()
        self.stopalarmbutton.pack()

    def start_clock(self):
        global done, start_printed, stop_printed, stop_clicked
        if not done:
            self.cancelbutton.config(state="active")
            self.alarmbutton.config(state="disabled")

            if not start_printed:
                print("Alarm set for {}:{}{}".format(self.hr.get(), f"{self.min.get():02d}", self.ampm.get()))
                start_printed = True
                stop_printed = False

            hour_value = self.hr.get() + (12 if self.ampm.get() == "PM" and self.hr.get() != 12 else 0)
            hour_value %= 24  # Normalize hour value
            self.Alarm(f"{hour_value:02d}", f"{self.min.get():02d}")

        if stop_clicked:
            done = False
            start_printed = False
            stop_clicked = False

    def stop_clock(self):
        global done, stop_clicked
        print("Alarm set for {}:{}{} has been cancelled".format(self.hr.get(), f"{self.min.get():02d}", self.ampm.get()))
        stop_clicked = True
        done = True
        self.cancelbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def stop_audio(self):
        # No audio to stop in this implementation, just reset buttons
        self.stopalarmbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def play_alarm_sound(self):
        """Play a simple beep sound depending on the OS."""
        if platform.system() == "Windows":
            os.system("echo ^G")  # Terminal beep
        elif platform.system() == "Linux":
            os.system("play -nq -t alsa synth 1 sine 440")  # Requires sox
        elif platform.system() == "Darwin":
            os.system("afplay /System/Library/Sounds/Glass.aiff")  # Use a built-in sound

    def Alarm(self, myhour, myminute):
        global done, start_printed, finished
        if not done:
            current_time = datetime.now().strftime("%H:%M")
            if current_time == f"{myhour}:{myminute}":
                self.play_alarm_sound()  # Play the alarm sound
                print("Alarm is ringing!")
                done = True
                finished = True
                self.cancelbutton.config(state="disabled")
                self.stopalarmbutton.config(state="active")
            else:
                self.after(1000, self.start_clock)  # Check every second
        if finished:
            start_printed = False
            finished = False

def main():
    app = AlarmApp()
    app.mainloop()
