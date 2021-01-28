import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_IMAGES_DIR = os.path.join(CUR_DIR, 'training_data', 'cig_butts', 'images')
MODEL_DIR = os.path.join(CUR_DIR, 'utils', 'model')

THRESHOLD = 0.5
INPUT_MEAN = 127.5
INPUT_STD = 127.5

TPU = True
