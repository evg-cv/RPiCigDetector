import cv2
import time

from imutils.video import VideoStream


cap = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
cap.awb_mode = "fluorescent"

while True:
    frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cv2.destroyAllWindows()
