import os
import cv2
import numpy as np
import importlib.util

from settings import THRESHOLD, MODEL_DIR, TPU, INPUT_STD, INPUT_MEAN


pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if TPU:
        from tensorflow.lite.python.interpreter import load_delegate


class ButtDetector:
    def __init__(self):
        if TPU:
            self.interpreter = Interpreter(model_path=os.path.join(MODEL_DIR,
                                                                   'butt_detecter_quantized_edgetpu.tflite'),
                                           experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        else:
            self.interpreter = Interpreter(model_path=os.path.join(MODEL_DIR, 'butt_detecter_quantized.tflite'))
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)

        with open(os.path.join(MODEL_DIR, "labelmap.txt"), 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        self.butt_nums = 0
        self.detected_status = False

    def detect_butts(self, frame, count_ret=False):
        if count_ret:
            # st_time = time.time()
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im_h, im_w, _ = frame.shape
            image_resized = cv2.resize(image_rgb, (self.width, self.height))
            input_data = np.expand_dims(image_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if self.floating_model:
                input_data = (np.float32(input_data) - INPUT_MEAN) / INPUT_STD

            # Perform the actual detection by running the model with the image as input
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            detected_butts = 0
            for i in range(len(scores)):
                if (scores[i] > THRESHOLD) and (scores[i] <= 1.0):
                    detected_butts += 1

            if self.butt_nums == 0 and detected_butts > 0:
                self.butt_nums = detected_butts
                self.detected_status = True
            elif self.butt_nums != 0 and detected_butts != 0 and self.butt_nums != detected_butts:
                self.butt_nums = detected_butts
                self.detected_status = True
            elif self.butt_nums != 0 and detected_butts == 0:
                self.butt_nums = detected_butts
                self.detected_status = False
            elif self.butt_nums != 0 and self.butt_nums == detected_butts:
                self.detected_status = False
            # print(f"[INFO] Processing Time: {time.time() - st_time}")

        cv2.putText(frame, f"The number of Butts: {self.butt_nums}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2)

        return frame


if __name__ == '__main__':
    ButtDetector().detect_butts(frame=cv2.imread(""))
