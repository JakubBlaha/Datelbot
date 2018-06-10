from kivy.uix.popup import Popup
from kivy.app import App

class MaterialPopup(Popup):
    def __init__(self, **kw):
        super(MaterialPopup, self).__init__(**kw)

        prim = App.get_running_app().theme_cls.primary_color

        self.title_color = prim
        self.separator_color = prim
        self.background_color = 1, 1, 1, 1
        self.background = 'atlas://data/images/defaulttheme/checkbox_off'