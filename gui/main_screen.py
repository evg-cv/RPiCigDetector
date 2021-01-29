import threading
import datetime
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from src.db.manager import DatabaseManager
from gui.popup import WarningPopup
from settings import MAIN_SCREEN_PATH, MAX_BUTT_NUMS


Builder.load_file(MAIN_SCREEN_PATH)


class MainScreen(Screen):
    capture = None
    event_take_video = None
    texture = None

    def __init__(self, **kwargs):

        super(MainScreen, self).__init__(**kwargs)
        self.db_manager = DatabaseManager()
        self.db_ret = False
        self.db_thread = None

    def on_enter(self, *args):
        self.ids.video.start()
        self.db_ret = True
        self.db_thread = threading.Thread(target=self.save_butt_number)
        self.db_thread.start()

    def on_leave(self, *args):
        self.ids.video.stop()
        super(MainScreen, self).on_leave(*args)

    def save_butt_number(self):
        while True:
            if not self.db_ret:
                break
            if self.ids.video.butt_detector.detected_status:
                butt_nums = self.ids.video.butt_detector.butt_nums
                if butt_nums >= MAX_BUTT_NUMS:
                    self.ids.warn_txt.text = "Detected More than Max Butts!"
                else:
                    self.ids.warn_txt.text = ""
                current_tstamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.ids.butt_num.text = str(butt_nums)
                self.ids.time_stamp.text = str(current_tstamp)
                self.db_manager.insert_data(butt_num=butt_nums, t_stamp=current_tstamp)
                time.sleep(2)
            time.sleep(0.02)

    def close_window(self):
        self.db_ret = False
        self.db_thread.join()
        App.get_running_app().stop()

    def on_close(self):
        pass
