import win32gui
import tkinter as tk
import sys
import os
from clipboard import paste
from pyautogui import hotkey
from tkinter import ttk
from tkinter import messagebox

import keyinput


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS',
                        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Emulator:
    def __init__(self):
        self.chars = ""

    def emulate(self):
        self.__copy()
        self.__extract_chars()
        self.__emulate()

    def __emulate(self):
        # Internal function
        window.info("Emulating..")
        for ch in self.chars:
            keyinput.press(ch)

        window.info("Ready")

    def __copy(self):
        # Internal function
        window.info("Getting data..")
        
        hotkey("ctrl", "a")
        hotkey("ctrl", "c")
        hotkey("ctrl", "shift", "home")

    def __extract_chars(self):
        # Internal function
        window.info("Extracting characters..")
        
        clip = paste()
        rows = clip.split("\n")
        to_type = max(rows, key=len)
        to_type = to_type.split("  ")

        final_str = ""
        for s in to_type:
            final_str += '\u0020' if s is "" or s is "\n" else s.strip()

        self.chars = final_str


class App(tk.Tk):
    help_message = \
"""
How to use Datelbot:
1) Open new tab in any browser and navigate to nedatluj.cz
2) Select your exercise
3) Select your mode
4) Press Emulate button in Datelbot

Note: Datelbot may fail sometimes due to nedatluj.cz web unstability. In this case, please reload the page using f5 or reload button in your browser.

\u00a9Xtremeware 2018 All rights reserved
"""

    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)
        self.title("Datelbot")
        self.attributes("-topmost", True)
        self.config(padx=6, pady=4)
        self.resizable(False, False)
        self.iconbitmap(resource_path("img/icon.ico"))

        self.label = tk.Label(
            self,
            text="Welcome to Datelbot",
            font="Calibri 20",
            fg="#aaa",
            anchor="w")
        self.button_frm = tk.Frame()
        self.help_button = ttk.Button(
            self.button_frm,
            text="?",
            command=self.__help,
            takefocus=False,
            width=3,
            cursor="hand2")
        self.start = ttk.Button(
            self.button_frm,
            text="Emulate",
            command=self.__run_adv,
            takefocus=False,
            width=20,
            cursor="hand2")
        self.info_lb = ttk.Label(text="Ready")

        self.label.pack(anchor='w')
        self.button_frm.pack(fill='x')
        self.start.pack(side='left')
        self.help_button.pack(side='right')
        self.info_lb.pack(side='left')

    def __run_adv(self):
        # Internal function
        self.start.config(state='disabled')
        self.info("Switching applications..")

        if switch.switch_to_target():
            emul.emulate()
            self.info("Emulating finished")
        else:
            self.info("Error: Failed to load browser tab!")

        self.start.config(state='normal')

    def __help(self):
        # Internal function
        messagebox.showinfo(title="Datelbot | Help", message=self.help_message)

    def info(self, text):
        "Configures the info label"
        self.info_lb.config(text=text)
        self.info_lb.update()


class Switcher:
    def __init__(self):
        self.success = False
        self.top_windows = []
        self.target = "Cvičení | Nedatluj.cz"

    def switch_to_target(self):
        "Focuses hwnd of self.target"
        self.success = False
        win32gui.EnumWindows(self.__enum_handler, self.top_windows)

        return self.success

    def __enum_handler(self, hwnd, top_windows):
        # Internal function
        if self.target in win32gui.GetWindowText(hwnd):
            win32gui.ShowWindow(hwnd, 3)
            win32gui.SetForegroundWindow(hwnd)
            self.success = True


emul = Emulator()
window = App()
switch = Switcher()

window.mainloop()
