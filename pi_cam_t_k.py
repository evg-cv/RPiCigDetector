import os
import cv2
import time

# from picamera import PiCamera
from imutils.video import VideoStream


cap = VideoStream(usePiCamera=True).start()
# capture = PiCamera(framerate=30)
time.sleep(2)
cap.awb_mode = "incandescent"
# tmp_path = os.path.join('/tmp', 'temp.jpg')

while True:
    frame = cap.read()
    # capture.capture(tmp_path)
    # frame = cv2.imread(tmp_path)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cv2.destroyAllWindows()
