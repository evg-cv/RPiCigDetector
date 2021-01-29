from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from settings import WARNING_SCREEN_PATH

Builder.load_file(WARNING_SCREEN_PATH)


class WarningPopup(Popup):

    label = StringProperty()

    def __init__(self, label, **kwargs):
        super(WarningPopup, self).__init__(**kwargs)
        self.set_description(label)

    def set_description(self, label):
        self.label = label
