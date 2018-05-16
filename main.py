# coding: utf-8
import win32gui
import kivy
from clipboard import paste
from pyautogui import hotkey

import input
import resource

kivy.require('1.10.0')

from kivy import Config
Config.set('graphics', 'width', 300)
Config.set('graphics', 'height', 110)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'maxfps', 50)
Config.set('graphics', 'borderless', 1)

from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation, AnimationTransition
from kivy.utils import get_color_from_hex

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivymd.button import MaterialFlatButton, MaterialRaisedButton
from kivymd.label import MaterialLabel
from kivymd.theming import ThemeManager
from kivy.uix.popup import Popup


def get_app():
    return App.get_running_app()


class Emulator:
    def __init__(self):
        self.chars = ""

    def emulate(self):
        self.copy()
        self.extract_chars()
        self._emulate()

    def _emulate(self):
        input.write(self.chars)

    def copy(self):
        hotkey("ctrl", "a")
        hotkey("ctrl", "c")
        hotkey("ctrl", "shift", "home")

    def extract_chars(self):
        clip = paste()
        rows = clip.split("\n")
        to_type = max(rows, key=len)
        to_type = to_type.split("  ")

        final_str = ''
        for s in to_type:
            final_str += '\u0020' if s is '' or s is '\n' else s.strip()

        self.chars = final_str


class Switcher:
    def __init__(self):
        self.target = 'Cvičení | Nedatluj.cz - Google Chrome'

    def restore_app(self):
        f = lambda *args: Window.raise_window()
        Clock.schedule_once(f, 1)

    def switch_to_target(self):
        hwnd = win32gui.FindWindow(None, self.target)

        if hwnd == 0:
            return False

        win32gui.ShowWindow(hwnd, 3)
        win32gui.SetForegroundWindow(hwnd)

        return True


class InfoLabel(MaterialLabel):
    anim = None

    def update(self, text):
        if self.anim != None:
            self.anim.stop(self)

        self.text = text

        c = get_color_from_hex("442B69")

        self.anim = Animation(
            color=c,
            step=.04,
            duration=.1,
            transition=AnimationTransition.in_out_expo)
        self.anim.start(self)

        self.anim = Animation(color=self.theme_cls.bg_normal, step=.01)
        l = lambda *args: self.anim.start(self)
        Clock.schedule_once(l, 1)


class WindowDragBehavior:
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            datelbot.click(touch)
            self.drag_clock = Clock.schedule_interval(datelbot.drag, 1 / 60)

    def on_touch_up(self, touch):
        if hasattr(self, 'drag_clock'):
            self.drag_clock.cancel()


class Dragger(WindowDragBehavior, Widget):
    pass


class MaterialPopup(Popup):
    def __init__(self):
        Popup.__init__(self)

        prim = get_app().theme_cls.primary_color

        self.title_color = prim
        self.separator_color = prim
        self.background_color = 1, 1, 1, 1
        self.background = 'atlas://data/images/defaulttheme/checkbox_off'


class CustStackLayout(StackLayout):
    pass


class HeadLabel(WindowDragBehavior, MaterialLabel):
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
        self.b = CustStackLayout()

        Window.on_cursor_enter = self.on_enter
        Window.on_cursor_leave = self.on_leave

        f = lambda *args: self.info("Hey, use the help button!")
        Clock.schedule_once(f, 4)

        return self.b

    def on_leave(self, *args):
        anim = Animation(color=[.8, .8, .8, 1], duration=.1)
        anim.start(self.b.ids.header)

    def on_enter(self, *args):
        anim = Animation(color=self.theme_cls.primary_color, duration=.1)
        anim.start(self.b.ids.header)

    def info(self, text):
        self.b.ids.info.update(text)

    def help(self):
        self.b.ids.help_button.disabled = True

        self.help_popup = HelpPopup()

        anim = Animation(
            size=(Window.width, self.large_height + 6),
            transition=AnimationTransition.out_expo,
            duration=1)

        anim.start(Window)

        Clock.schedule_once(self.help_popup.open, .2)

        def fix_fuzz(*args):
            Window.size = (Window.width, self.large_height)

        Clock.schedule_once(fix_fuzz, .6)

    def dismiss_help(self):
        self.help_popup.dismiss()

        anim = Animation(
            size=(Window.width, self.small_height - 4),
            transition=AnimationTransition.out_expo,
            duration=1)

        anim.start(Window)

        def fix_fuzz(*args):
            Window.size = (Window.width, self.small_height)

        def enable_help(*args):
            self.b.ids.help_button.disabled = False

        Clock.schedule_once(fix_fuzz, .6)
        Clock.schedule_once(enable_help, 1)

    def click(self, touch):
        x = touch.x
        y = touch.y

        y = Window.height - y

        self.touch_x, self.touch_y = x, y

    def drag(self, *args):
        x, y = win32gui.GetCursorPos()

        x -= self.touch_x
        y -= self.touch_y

        Window.left = x
        Window.top = y

    def close(self):
        get_app().stop()
        Window.close()

    def run_emul(self):
        if switch.switch_to_target():
            emul.emulate()
            switch.restore_app()
            self.info("Completed")

        else:
            self.info("Failed to load browser tab!")


if __name__ == '__main__' or 'main':
    emul = Emulator()
    switch = Switcher()

    Window.set_icon(resource.resource_path('img/icon.ico'))
    Window.set_title("Datelbot")

    kivy.resources.resource_add_path(resource.resource_path())
    datelbot = DatelbotApp()
    datelbot.run()
