import os
import time
import threading
import cv2

from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from picamera import PiCamera
from utils.frame_buf import frame_to_buf
from kivy.uix.image import Image
from kivy.logger import Logger
from src.rpi.camera import ButtDetector
from settings import BAD_FRAME_PATH


class VideoWidget(Image):
    """:class:`KioskVideoWidget` is an implementation of the video live feed.

    Call `start()` function to start live video feed on this widget,
    and call `pause()` function to pause.

    Attention: Make sure to call `stop()` function before moving to other screen!!!
               e.g. If this widget is used in a `Screen` widget, make use to
               add `stop()` function in its `on_leave()` function!
    """

    _event_take_video = None

    _capture = None

    port_num = ObjectProperty(0, allownone=True)
    thresh_value = ObjectProperty(-1, allownone=True)
    """Port number of video source.
    When using camera directly, this should be a numeric value.
    When getting video feed from REDIS, a string value should be used.
    :attr:`port_num` is an :class:`~kivy.properties.ObjectProperty` and defaults to -1.
    """

    camera_width = NumericProperty(640)
    """Pixel width of camera.
    :attr:`camera_width` is an :class:`~kivy.properties.NumericProperty` and defaults to 1280. (720p)
    """

    camera_height = NumericProperty(480)
    """Pixel height of camera.
    :attr:`camera_height` is an :class:`~kivy.properties.NumericProperty` and defaults to 720. (720p)
    """

    is_running = BooleanProperty(False)

    _frame = None

    def __init__(self, **kwargs):
        self._egg_counter_ret = None
        self.butt_detector = ButtDetector()
        self.count_ids = 0
        self._capture = PiCamera(framerate=30)
        time.sleep(2)
        super(VideoWidget, self).__init__(**kwargs)

    def on_port_num(self, *args):
        """
        This function should be called once this widget is created.
        If we call this function in self.__init__() function, height & width will have default value.
        :param args:
        :return:
        """
        try:
            # self._capture = cv2.VideoCapture(self.port_num)
            self._capture.awb_mode = "incandescent"
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            # self._frame = None
        except Exception as e:
            Logger.error('KioskVideoWidget: Failed to assign port number - {}'.format(e))
            self._capture = None

    def start(self):
        """
        Start live video feed
        :return:
        """
        if self.is_running:
            return

        if self.port_num is not None:
            if self._capture is None:
                self.on_port_num()

            if self._event_take_video is None:
                self._event_take_video = Clock.schedule_interval(lambda dt: self._take_video(), 1.0 / 30.0)
            else:
                self._event_take_video()
            self.is_running = True
        else:
            self.source = BAD_FRAME_PATH
            Logger.warning('KioskVideo: Port is not set yet')

    def pause(self):
        if self._event_take_video and self._event_take_video.is_triggered:
            self._event_take_video.cancel()
            self._event_take_video = None
        self.is_running = False

    def _take_video(self):
        """
        Capture video frame and update image widget
        :return:
        """
        tmp_path = os.path.join('/tmp', 'temp.jpg')
        try:
            if type(self.port_num) == int:
                self._capture.capture(tmp_path)
                frame = cv2.imread(tmp_path)
            else:
                frame = None
            if self.count_ids % 20 == 0:
                counted_frame = self.butt_detector.detect_butts(frame=frame, count_ret=True)
            else:
                counted_frame = self.butt_detector.detect_butts(frame=frame)
            # counted_frame = frame
        except (cv2.error, AttributeError, ConnectionError):
            counted_frame = None
        self._update_video(origin_frame=counted_frame)
        self.count_ids += 1
        if self.count_ids >= 1000:
            self.count_ids = 0

    def _update_video(self, origin_frame, *args):
        """
        Display captured image to the widget
        :return:
        """
        texture = frame_to_buf(frame=origin_frame)
        if texture is None:
            self.source = BAD_FRAME_PATH
        else:
            self.texture = texture
            self._frame = origin_frame

    def get_frame(self):
        return self._frame

    def save_to_file(self, filename):
        if self._frame is not None:
            try:
                cv2.imwrite(filename, self._frame)
                return filename
            except Exception as e:
                Logger.error('KioskVideoWidget: Failed to save to file, reason - {}'.format(e))
        else:
            Logger.error('KioskVideoWidget: Tried to save to file, but current frame is none!')

    def stop(self):
        self.pause()
        try:
            if self._capture is not None:
                self._capture.release()
                self._capture = None
        except AttributeError:
            pass


class VideoFileWidget(Image):

    path = StringProperty()

    def __init__(self, **kwargs):
        super(VideoFileWidget, self).__init__(**kwargs)
        self._b_stop = threading.Event()
        self._b_stop.clear()
        self.frame_thread = None

    def start(self, *args):
        threading.Thread(target=self._read_file).start()

    def _read_file(self):
        cap = cv2.VideoCapture(0)
        cnt = 0
        while not self._b_stop.is_set():
            print("running")
            s_time = time.time()
            ret, frame = cap.read()
            cnt += 1
            if cnt == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cnt = 0
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            Clock.schedule_once(lambda dt: self._update_frame(frame))
            time.sleep(max(0., 1 / 30. - time.time() + s_time))

        cap.release()

    def _update_frame(self, frame):
        texture = frame_to_buf(frame=frame)
        self.texture = texture

    def stop(self):
        self._b_stop.set()
        self.frame_thread.join()
