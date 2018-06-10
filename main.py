# coding: utf-8
import win32gui
import kivy
from clipboard import paste
from pyautogui import hotkey
from KivyOnTop import register_topmost

import input
from resource import resource_path

kivy.require('1.10.0')

from kivy import Config
Config.set('graphics', 'width', 300)
Config.set('graphics', 'height', 110)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', 1)

from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.stacklayout import StackLayout
from kivymd.label import MaterialLabel
from kivymd.theming import ThemeManager
from material_popup import MaterialPopup


class Emulator:
    @staticmethod
    def emulate():
        Emulator.copy()
        chars = Emulator.get_chars()
        input.write(chars)

    @staticmethod
    def copy():
        hotkey("ctrl", "a")
        hotkey("ctrl", "c")
        hotkey("ctrl", "shift", "home")

    @staticmethod
    def get_chars():
        clip = paste()
        rows = clip.split("\n")
        to_type = max(rows, key=len)
        to_type = to_type.split("  ")

        final_str = ''
        for s in to_type:
            final_str += '\u0020' if s is '' or s is '\n' else s.strip()

        return final_str


class Switcher:
    target = 'Cvičení | Nedatluj.cz - Google Chrome'

    @staticmethod
    def switch_to_target():
        hwnd = win32gui.FindWindow(None, Switcher.target)

        if hwnd == 0:
            return False

        win32gui.ShowWindow(hwnd, 3)
        win32gui.SetForegroundWindow(hwnd)

        return True


class InfoLabel(MaterialLabel):
    def update(self, text):
        Animation.stop_all(self)

        self.text = text

        anim_1 = Animation(opacity=1, d=.1, t='out_expo')
        anim_2 = Animation(opacity=0)

        anim_1.bind(on_complete=lambda *args: anim_2.start(self))
        anim_1.start(self)


class CustStackLayout(StackLayout):
    pass


class HelpPopup(MaterialPopup):
    pass


class DatelbotApp(App):
    theme_cls = ThemeManager()
    help_text = """
How to use [color=442B69]Datelbot[/color]:
1) Open new tab in any browser and navigate to nedatluj.cz
2) Select your exercise
3) Press Emulate button in [color=442B69]Datelbot[/color]

[i][color=444]Note: Datelbot works only with Chrome web browser at the moment[/color][/i]

\u00a9[color=442B69]Xtremeware[/color] 2018 All rights reserved
Created by: [color=442B69]Jakub Bláha[/color]
"""
    small_height = 110
    large_height = 300

    def __init__(self):
        super(DatelbotApp, self).__init__()

        self.theme_cls.primary_palette = 'Purple'

    def build(self):
        Window.on_cursor_enter = self.on_enter
        Window.on_cursor_leave = self.on_leave

        foo = lambda *args: self.info("Hey, use the help button!")
        Clock.schedule_once(foo, 4)

        return CustStackLayout()

    def on_leave(self, *args):
        anim = Animation(color=[.8, .8, .8, 1], d=.1)
        anim.start(self.root.ids.header)

    def on_enter(self, *args):
        anim = Animation(color=self.theme_cls.primary_color, d=.1)
        anim.start(self.root.ids.header)

    def info(self, text):
        self.root.ids.info.update(text)

    def help(self):
        self.root.ids.help_button.disabled = True

        self.help_popup = HelpPopup()

        anim = Animation(
            size=(Window.width, self.large_height + 6), t='out_expo', d=1)

        anim.start(Window)

        Clock.schedule_once(self.help_popup.open, .2)

    def dismiss_help(self):
        self.help_popup.dismiss()

        anim = Animation(
            size=(Window.width, self.small_height - 4), t='out_expo', d=1)

        anim.start(Window)

        def fix_fuzz(*args):
            Window.size = (Window.width, self.small_height)

        def enable_help(*args):
            self.root.ids.help_button.disabled = False

        Clock.schedule_once(fix_fuzz, .6)
        Clock.schedule_once(enable_help, 1)

    def run_emul(self):
        if Switcher.switch_to_target():
            Emulator.emulate()
            self.info("Completed")

        else:
            self.info("Failed to load browser tab!")

    def on_start(self, *args):
        register_topmost(Window, TITLE)


TITLE = 'Datelbot'

if __name__ == '__main__' or 'main':
    Window.set_icon(resource_path('img/icon.ico'))
    Window.set_title(TITLE)

    kivy.resources.resource_add_path(resource_path())
    datelbot = DatelbotApp()
    datelbot.run()
