import cv2

from picamera import PiCamera


capture = PiCamera(framerate=30)
capture.awb_mode = "fluorescent"

while True:
    _, frame = capture.capture()
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cv2.destroyAllWindows()
