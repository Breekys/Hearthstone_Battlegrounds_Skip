import subprocess
from threading import Timer
import tkinter as tk
from tkinter import font
import json


def popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd.split(), startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process.stdout.read()


class Example(tk.Frame):
    DISCONNECTED_TIME = 4

    def __init__(self, parent):
        # Outbound rule name
        self.config = json.load(open("config", "r"))

        # VISUAL
        tk.Frame.__init__(self, parent, width=500, height=500)

        # button to do disconnect and reconnect afterwards
        helv36 = font.Font(family='Helvetica', size=36, weight='bold')
        self.btn = tk.Button(self, text="SKIP", command=self.skip, width=10, height=1, font=helv36)

        # lay the widgets out on the screen.
        self.btn.pack(fill="both")

    def skip(self):
        self.btn["state"] = "disabled"
        self.disconnect()
        r = Timer(Example.DISCONNECTED_TIME, self.connect, args=None, kwargs=None)
        r.start()
        self.refresh_visual(Example.DISCONNECTED_TIME)

    def refresh_visual(self, s):
        self.btn["text"] = str(int(s))
        if s > 0:
            s -= 1
            r = Timer(1, self.refresh_visual, args=[s], kwargs=None)
            r.start()
        else:
            self.btn["text"] = "SKIP"

    def disconnect(self):
        bashCommand = 'netsh advfirewall firewall set rule name="{}" new enable=yes'.format(self.config["outbound_rule_name"])
        popen(bashCommand)

    def connect(self):
        bashCommand = 'netsh advfirewall firewall set rule name="{}" new enable=no'.format(self.config["outbound_rule_name"])
        popen(bashCommand)
        self.btn["state"] = "normal"

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()