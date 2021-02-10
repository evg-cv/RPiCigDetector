import os
import glob
import tensorflow as tf
import cv2
import numpy as np

from imutils import paths
from settings import MODEL_DIR, TRAINING_IMAGES_DIR, CUR_DIR


def convert_quantized_tflite_model(frozen_graph_file, tflite_file_path):
    """
    Please use RPiCigDetector/utils/model/mobilenet_v1_1.0_224_frozen.tgz model for testing conversion to TFLite.
    :return:
    """
    # Convert the model.
    converter = tf.contrib.lite.TFLiteConverter.from_frozen_graph(
        graph_def_file=frozen_graph_file,
        input_arrays=["normalized_input_image_tensor"],
        input_shapes={"normalized_input_image_tensor": [1, 300, 300, 3]},
        output_arrays=['TFLite_Detection_PostProcess',
                       'TFLite_Detection_PostProcess:1',
                       'TFLite_Detection_PostProcess:2',
                       'TFLite_Detection_PostProcess:3'],
    )
    converter.allow_custom_ops = True

    converter.quantized_input_stats = {"normalized_input_image_tensor": (0., 1.)}
    # mean, std_dev (input range is [-1, 1])
    converter.inference_type = tf.lite.constants.QUANTIZED_UINT8  # this is the recommended type.
    # converter.inference_input_type = tf.uint8  # optional
    # converter.inference_output_type = tf.uint8  # optional
    tflite_model = converter.convert()

    # Save the model.
    with open(tflite_file_path, 'wb') as f:
        f.write(tflite_model)


def convert_from_frozen_graph():
    """
    Please use RPiCigDetector/utils/model/mobilenet_v1_1.0_224_frozen.tgz model for testing conversion to TFLite.
    :return:
    """
    input_arrays = ["input"]
    converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
        graph_def_file='/media/main/Data/Task/RPiCigDetector/utils/test_model/frozen_inference_graph.pb',
        # both `.pb` and `.pbtxt` files are accepted.
        input_arrays=['input'],
        input_shapes={'input': [1, 224, 224, 3]},
        output_arrays=['MobilenetV1/Predictions/Softmax']
    )
    converter.allow_custom_ops = True
    # converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
    # converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_type = tf.lite.constants.QUANTIZED_UINT8
    converter.quantized_input_stats = {input_arrays[0]: (128, 128)}
    tflite_model = converter.convert()

    # Save the model.
    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)


def convert_tflitepb_to_tflite(frozen_graph_file, tflite_file_path):
    input_arrays = ["normalized_input_image_tensor"]
    output_arrays = ['TFLite_Detection_PostProcess',
                     'TFLite_Detection_PostProcess:1',
                     'TFLite_Detection_PostProcess:2',
                     'TFLite_Detection_PostProcess:3']
    input_shapes = {"normalized_input_image_tensor": [1, 300, 300, 3]}
    converter = tf.lite.TFLiteConverter.from_frozen_graph(frozen_graph_file,
                                                          input_arrays=input_arrays,
                                                          output_arrays=output_arrays,
                                                          input_shapes=input_shapes)
    converter.allow_custom_ops = True
    # converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_quant_model = converter.convert()
    with open(tflite_file_path, "wb") as tflite_file:
        tflite_file.write(tflite_quant_model)


def convert_quantized_tflite_for_tpu(frozen_graph_file, tflite_file_path):
    input_arrays = ["normalized_input_image_tensor"]
    output_arrays = ['TFLite_Detection_PostProcess',
                     'TFLite_Detection_PostProcess:1',
                     'TFLite_Detection_PostProcess:2',
                     'TFLite_Detection_PostProcess:3']
    input_shapes = {"normalized_input_image_tensor": [1, 300, 300, 3]}
    converter = tf.lite.TFLiteConverter.from_frozen_graph(frozen_graph_file, input_arrays,
                                                          output_arrays, input_shapes)
    converter.allow_custom_ops = True
    # converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
    # converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_type = tf.lite.constants.QUANTIZED_UINT8
    converter.quantized_input_stats = {input_arrays[0]: (128, 128)}
    # converter.inference_input_type = tf.uint8
    # converter.inference_output_type = tf.uint8
    # converter.representative_dataset = _representative_dataset_gen
    tflite_model_quant = converter.convert()
    with open(tflite_file_path, "wb") as tflite_file:
        tflite_file.write(tflite_model_quant)

    return


def _representative_dataset_gen():
    images_path = glob.glob(os.path.join(TRAINING_IMAGES_DIR, "*.jpg"))[:100]
    if images_path is None:
        raise Exception(
            "Image directory is None, full integer quantization requires images directory!"
        )
    image_paths = list(paths.list_images(images_path))
    for p in image_paths:
        image = cv2.imread(p)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (300, 300))
        image = image.astype("float")
        image = np.expand_dims(image, axis=1)
        image = image.reshape(1, 300, 300, 3)

        yield [image.astype("float32")]


if __name__ == '__main__':
    convert_quantized_tflite_model(frozen_graph_file="/media/main/Data/Task/RPiCigDetector/utils/test_model"
                                                     "/tflite_graph.pb",
                                   tflite_file_path=os.path.join(CUR_DIR, "utils", "test_model",
                                                                 "quantized.tflite"))
