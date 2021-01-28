import os

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from gui.main_screen import MainScreen
from gui.show_database import ShowDatabase
from settings import MAIN_SCREEN, SHOW_DATABASE, APP_HEIGHT, APP_WIDTH

Config.read(os.path.expanduser('~/.kivy/config.ini'))
Config.set('graphics', 'resizeable', '0')
Config.set('graphics', 'width', str(APP_WIDTH))
Config.set('graphics', 'height', str(APP_HEIGHT))
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('graphics', 'keyboard_mode', 'en_US')
Config.set('graphics', 'log_level', 'info')

Config.write()
Window.size = (int(APP_WIDTH), int(APP_HEIGHT))


class ButtCounterTool(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_screen = MainScreen(name=MAIN_SCREEN)
        self.show_database = ShowDatabase(name=SHOW_DATABASE)

        screens = [
            self.main_screen,
            self.show_database,
        ]

        self.sm = ScreenManager()
        for screen in screens:
            self.sm.add_widget(screen)

    def build(self):
        self.sm.current = MAIN_SCREEN

        return self.sm

    def on_stop(self):
        self.main_screen.db_ret = False
        self.main_screen.db_thread.join()
        Window.close()


if __name__ == '__main__':

    ButtCounterTool().run()
