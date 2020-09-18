import subprocess
from threading import Timer
import tkinter as tk
from tkinter import font
from tkinter import filedialog
import json
import ntpath
import sys, os


def popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd.split(), startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process.stdout.read()


class Example(tk.Frame):
    DISCONNECTED_TIME = 4
    DEFAULT_CONFIG = {
        "outbound_rule_name": "HS_Connexion_Blocker",
        "hearthstone_path": ""
    }

    def __init__(self, parent):
        # Load config
        if "config.json" not in os.listdir():
            json.dump(self.DEFAULT_CONFIG, open("config.json", "w"))
        self.config = json.load(open("config.json", "r"))

        self.setup()

        # VISUAL
        tk.Frame.__init__(self, parent, width=500, height=500)
        # button to do disconnect and reconnect afterwards
        helv36 = font.Font(family='Helvetica', size=36, weight='bold')
        self.btn = tk.Button(self, text="SKIP", command=self.skip, width=10, height=1, font=helv36)
        # lay the widgets out on the screen.
        self.btn.pack(fill="both")

    def setup(self):
        if self.config["hearthstone_path"] != "":
            return
        # Ask for hearthstone path
        file_path = filedialog.askopenfilename(title="Select Hearthstone.exe")
        # If wrong ask again 5 times or exit after
        attempts = 0
        while ntpath.basename(file_path) != "Hearthstone.exe":
            file_path = filedialog.askopenfilename(title="Wrong file, Select Hearthstone.exe")
            attempts += 1
            if attempts >= 5:
                sys.exit(1)

        # Save config
        self.config["outbound_rule_name"] = self.DEFAULT_CONFIG["outbound_rule_name"]
        self.config["hearthstone_path"] = file_path
        json.dump(self.config, open("config.json", "w"))

        # Create rule
        self.create_rule()

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

    def create_rule(self):
        bashCommand = 'netsh advfirewall firewall add rule name="{}" dir=out action=block  program="{}" enable=no'\
            .format(self.config["outbound_rule_name"],
                    self.config["hearthstone_path"])
        popen(bashCommand)

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