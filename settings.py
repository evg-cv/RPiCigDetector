import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_IMAGES_DIR = os.path.join(CUR_DIR, 'training_data', 'cig_butts', 'images')
MODEL_DIR = os.path.join(CUR_DIR, 'utils', 'model')

MAIN_SCREEN_PATH = os.path.join(CUR_DIR, "gui", 'kiv', "main_screen.kv")
SHOW_DATABASE_SCREEN_PATH = os.path.join(CUR_DIR, 'gui', 'kiv', 'show_database.kv')
WARNING_SCREEN_PATH = os.path.join(CUR_DIR, 'gui', 'kiv', 'warning.kv')
BAD_FRAME_PATH = os.path.join(CUR_DIR, 'utils', 'img', 'bad_camera.png')

THRESHOLD = 0.5
INPUT_MEAN = 127.5
INPUT_STD = 127.5
MAX_BUTT_NUMS = 2
APP_WIDTH = '1280'
APP_HEIGHT = '900'
MAIN_SCREEN = "main_screen"
SHOW_DATABASE = "show_database"
TPU = False

HOST_NAME = 'localhost'
USER_NAME = 'root'
PASSWORD = 'password'
DATABASE_NAME = 'butt_counter'
