import os
import cv2
import time
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

    def detect_butts(self, images):
        for image_path in images:
            st_time = time.time()
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            im_h, im_w, _ = image.shape
            image_resized = cv2.resize(image_rgb, (self.width, self.height))
            input_data = np.expand_dims(image_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if self.floating_model:
                input_data = (np.float32(input_data) - INPUT_MEAN) / INPUT_STD

            # Perform the actual detection by running the model with the image as input
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()

            # Retrieve detection results
            # Bounding box coordinates of detected objects
            boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            # Class index of detected objects
            classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
            # Confidence of detected objects
            scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
            # num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (
            # inaccurate and not needed)

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if (scores[i] > THRESHOLD) and (scores[i] <= 1.0):
                    # Get bounding box coordinates and draw box Interpreter can return coordinates that are outside
                    # of image dimensions, need to force them to be within image using max() and min()
                    y_min = int(max(1, (boxes[i][0] * im_h)))
                    x_min = int(max(1, (boxes[i][1] * im_w)))
                    y_max = int(min(im_h, (boxes[i][2] * im_h)))
                    x_max = int(min(im_w, (boxes[i][3] * im_w)))
                    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (10, 255, 0), 2)

                    # Draw label
                    object_name = self.labels[int(classes[i])]
                    # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                    label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(y_min, label_size[1] + 10)
                    # Make sure not to draw label too close to top of window
                    cv2.rectangle(image, (x_min, label_ymin - label_size[1] - 10),
                                  (x_min + label_size[0], label_ymin + base_line - 10), (255, 255, 255),
                                  cv2.FILLED)  # Draw white box to put label text in
                    cv2.putText(image, label, (x_min, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                                2)  # Draw label text

            # All the results have been drawn on the image, now display the image
            cv2.imshow('Object detector', image)
            print(f"[INFO] Processing Time: {time.time() - st_time}")

            # Press any key to continue to next image, or press 'q' to quit
            if cv2.waitKey(0) == ord('q'):
                break

        # Clean up
        cv2.destroyAllWindows()


if __name__ == '__main__':
    ButtDetector().detect_butts(
        images=["/media/main/Data/Task/RPiCigDetector/training_data/cig_butts/images/image0.jpg",
                "/media/main/Data/Task/RPiCigDetector/training_data/cig_butts/images/image4.jpg",
                "/media/main/Data/Task/RPiCigDetector/training_data/cig_butts/images/image6.jpg"])
