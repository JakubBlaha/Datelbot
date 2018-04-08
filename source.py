import win32clipboard
import win32gui
import tkinter as tk
import keyboard
import sys
import os
import pyautogui
from tkinter import ttk
from tkinter import messagebox
from time import sleep
from _thread import start_new

import keyinput

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Emulator:
    def __init__(self):
        self.clip = ""
        self.chars = ""

    def autoemulate(self):
        window.info("Getting data..")
        self.copy()

        window.info("Extracting characters..")
        self.chars = self.extract_chars(self.clip)

        window.info("Emulating..")
        self.emulate()

    def emulate(self):
        pyautogui.scroll(10)
        for ch in self.chars:
            keyinput.press(ch)

    def copy(self):
        # Copies text of currently active window to self.clip
        keyboard.press_and_release("ctrl+a")
        keyboard.press_and_release("ctrl+c")
        keyboard.press_and_release("ctrl+shift+home")

        win32clipboard.OpenClipboard()
        self.clip = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

    def extract_chars(self, string):
        rows = string.split("\n")
        to_type = max(rows, key=len)
        to_type = to_type.split("  ")

        final_str = ""
        for s in to_type:
            final_str += '\u0020' if s is "" or s is "\n" else s.strip()

        return final_str


class App(tk.Tk):
    help_message = \
"""
How to use Datelbot:
1) Open new tab in any browser and navigate to nedatluj.cz
2) Select your exercise
3) Press Emulate button in Datelbot

Note: Datelbot may fail sometimes due to nedatluj.cz web unstability. In this case, please reload the page using f5 or reload button in your browser.

\u00a9Xtremeware 2018 All rights reserved
"""

    def __init__(self, **kwargs):
        self.pasted_text = ""

        tk.Tk.__init__(self, **kwargs)
        self.title("Datelbot")
        self.attributes("-topmost", True)
        self.config(padx=10, pady=6)
        self.resizable(False, False)
        self.iconbitmap(resource_path("img/icon.ico"))

        self.abrunning = tk.BooleanVar()
        self.abrunning.set(False)

        self.label = tk.Label(
            self,
            text="Welcome to Datelbot",
            font="Calibri 20",
            fg="#bbb",
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

        start_new(self.__anim, ())

    def __anim(self):
        for i in range(230, 100, -1):
            self.label.config(fg=f"#{format(i, 'x')*3}")
            self.label.update()
            sleep(0.01)

    def __run_adv(self):
        # Internal function
        self.info("Switching applications..")
        if switch.switch_to_target():
            emul.autoemulate()
            self.info("Emulating finished")
        else:
            self.info("Error: Failed to load browser tab!")

        self.start.config(state=tk.NORMAL)

    def __help(self):
        # Internal function
        messagebox.showinfo(title="Datelbot | Help", message=self.help_message)

    def info(self, text):
        # Internal function
        self.info_lb.config(text=text)
        self.info_lb.update()


class Switcher:
    def __init__(self):
        self.success = False
        self.top_windows = []
        self.target = "Cvičení | Nedatluj.cz"

    def switch_to_target(self):
        self.success = False
        win32gui.EnumWindows(self._enum_handler, self.top_windows)
        # sleep(1)

        return self.success

    def _enum_handler(self, hwnd, top_windows):
        # Internal function
        if self.target in win32gui.GetWindowText(hwnd):
            win32gui.ShowWindow(hwnd, 3)
            win32gui.SetForegroundWindow(hwnd)
            self.success = True


emul = Emulator()
window = App()
switch = Switcher()

window.mainloop()
