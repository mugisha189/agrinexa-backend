import tensorflow as tf
import numpy as np
import cv2
from fastapi import UploadFile

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="./model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

async def process_image(image: UploadFile) :
    image_data = await image.read()
    nparr = np.fromstring(image_data, np.uint8)
    processed_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    interpreter.set_tensor(input_details[0]['index'], processed_image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data
