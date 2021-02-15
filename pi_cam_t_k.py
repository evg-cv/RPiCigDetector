import cv2

from picamera import PiCamera


capture = PiCamera(framerate=30)
capture.awb_mode = "fluorescent"

while True:
    _, frame = capture.read()
    cv2.imshow("Frame", frame)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
