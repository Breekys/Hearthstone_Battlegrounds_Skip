import json
import ntpath
import os
import subprocess
import sys
import tkinter as tk
from threading import Timer
from tkinter import filedialog
from tkinter import font


def popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd.split(), startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    return process.stdout.read()


class Example(tk.Frame):
    APP_NAME = "HearthstoneBattlegroundsSkip"
    BASE_PATH = os.path.join(os.getenv('APPDATA'), APP_NAME)
    DEFAULT_CONFIG = {
        "outbound_rule_name": "HS Connexion Blocker",
        "hearthstone_path": "",
        "disconnected_time": 4
    }

    def __init__(self, parent):
        # Load config
        if self.APP_NAME not in os.listdir(os.getenv('APPDATA')):
            os.mkdir(self.BASE_PATH)
        if "config.json" not in os.listdir(self.BASE_PATH):
            json.dump(self.DEFAULT_CONFIG, open(os.path.join(self.BASE_PATH, "config.json"), "w"))
        self.config = json.load(open(os.path.join(self.BASE_PATH, "config.json"), "r"))

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
            if "Hearthstone.exe" in os.listdir(os.path.dirname(self.config["hearthstone_path"])):
                return
        # If wrong ask again 5 times or exit after
        initialdir = "C:/"
        if "Hearthstone" in os.listdir("C:/Program Files (x86)/"):
            initialdir = "C:/Program Files (x86)/Hearthstone"

        attempts = 0
        file_path = ""
        while ntpath.basename(file_path) != "Hearthstone.exe":
            # Ask for hearthstone path
            if attempts == 0:
                file_path = filedialog.askopenfilename(title="Select Hearthstone.exe", initialdir=initialdir)
            else:
                file_path = filedialog.askopenfilename(title="Wrong file, Select Hearthstone.exe", initialdir=initialdir)
            if file_path == "":
                sys.exit(1)
            attempts += 1
            if attempts >= 5:
                sys.exit(1)

        # Save config
        self.config["outbound_rule_name"] = self.DEFAULT_CONFIG["outbound_rule_name"]
        self.config["hearthstone_path"] = file_path.replace("/", "\\")
        json.dump(self.config, open(os.path.join(self.BASE_PATH, "config.json"), "w"))

        # Create rule
        self.create_rule()

    def skip(self):
        self.btn["state"] = "disabled"
        self.disconnect()
        r = Timer(self.config["disconnected_time"], self.connect, args=None, kwargs=None)
        r.start()
        self.refresh_visual(self.config["disconnected_time"])

    def refresh_visual(self, s):
        self.btn["text"] = str(int(s))
        if s > 0:
            s -= 1
            r = Timer(1, self.refresh_visual, args=[s], kwargs=None)
            r.start()
        else:
            self.btn["text"] = "SKIP"

    def create_rule(self):
        bashCommand = 'netsh advfirewall firewall add rule name="{}" dir=out action=block  program="{}" enable=no' \
            .format(self.config["outbound_rule_name"],
                    self.config["hearthstone_path"])
        popen(bashCommand)

    def disconnect(self):
        bashCommand = 'netsh advfirewall firewall set rule name="{}" new enable=yes'.format(
            self.config["outbound_rule_name"])
        popen(bashCommand)

    def connect(self):
        bashCommand = 'netsh advfirewall firewall set rule name="{}" new enable=no'.format(
            self.config["outbound_rule_name"])
        popen(bashCommand)
        self.btn["state"] = "normal"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hearthstone Battlegrounds Skip")
    try:
        root.iconbitmap(os.path.join(sys._MEIPASS, "data_files/next.ico"))
    except AttributeError:
        root.iconbitmap('data_files/next.ico')
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
