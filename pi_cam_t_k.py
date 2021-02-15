import os
import cv2
import time

from picamera import PiCamera


capture = PiCamera(framerate=30)
time.sleep(2)
capture.awb_mode = "sun"
tmp_path = os.path.join('/tmp', 'temp.jpg')

while True:
    capture.capture(tmp_path)
    frame = cv2.imread(tmp_path)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cv2.destroyAllWindows()
