import os
import glob
import cv2

from settings import TRAINING_IMAGES_DIR


def rename_images():
    images = glob.glob(os.path.join(TRAINING_IMAGES_DIR, "*.*"))
    for i, img in enumerate(images):
        new_img_path = os.path.join(TRAINING_IMAGES_DIR, f'image{i}.jpg')
        frame = cv2.imread(img)
        cv2.imwrite(new_img_path, frame)
        os.remove(img)


if __name__ == '__main__':
    rename_images()
