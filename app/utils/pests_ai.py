import tensorflow as tf
import numpy as np
import cv2
from fastapi import UploadFile

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="./model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

async def process_image(image: UploadFile):
    print("Processing image")
    image_data = await image.read()
    nparr = np.fromstring(image_data, np.uint8)
    processed_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Resize image to match expected input size
    resized_image = cv2.resize(processed_image, (224, 224))  
    
    # Convert to FLOAT32 and add batch dimension
    processed_image_float32 = np.expand_dims(resized_image.astype(np.float32), axis=0)
    
    interpreter.set_tensor(input_details[0]['index'], processed_image_float32)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(interpreter.get_tensor(output_details[0]))
    return output_data

