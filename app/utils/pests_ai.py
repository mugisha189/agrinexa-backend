import tensorflow as tf
import numpy as np
import cv2
from fastapi import UploadFile
from PIL import Image, ImageOps
import random

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="./model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the labels
class_names = [line.strip() for line in open("labels.txt", "r").readlines()]

# Tips for each pest class
pest_tips = {
    "0 Gray mold": [
        "Keep plants spaced to promote good air circulation.",
        "Avoid overhead watering to keep foliage dry.",
        "Remove and discard infected plant parts.",
        "Use fungicides as needed, especially in wet conditions.",
        "Rotate crops to reduce disease recurrence.",
        "Sterilize garden tools to prevent disease spread.",
        "Mulch plants to prevent soil splash on leaves.",
        "Control humidity in greenhouses or indoor settings.",
        "Plant resistant varieties where possible.",
        "Ensure proper drainage to avoid waterlogging.",
        "Clean and disinfect plant containers regularly.",
        "Use organic compost to strengthen plant health.",
        "Limit nitrogen fertilizers that encourage soft, susceptible growth.",
        "Avoid planting too densely to prevent high humidity.",
        "Remove debris from around the plants to reduce fungal spores.",
        "Plant in areas with plenty of sunlight.",
        "Do not overwater plants, keeping soil just moist.",
        "Use a fan or ventilation system in greenhouses.",
        "Prune plants regularly to remove infected areas.",
        "Check plants frequently for early signs of infection.",
        "Increase the space between rows of plants for better air circulation.",
        "Apply copper-based fungicides as a preventive measure.",
        "Use organic sulfur fungicides if the problem persists.",
        "Water plants early in the day to allow them to dry before nightfall.",
        "Keep weeds under control, as they can harbor the disease.",
        "Dispose of infected plant material properly.",
        "Use crop rotation to reduce disease pressure.",
        "Encourage beneficial microorganisms in the soil.",
        "Avoid using the same garden tools on healthy and infected plants.",
        "Improve soil health by adding organic matter."
    ],
    "1 Leaf spot": [
        "Plant disease-resistant varieties when possible.",
        "Avoid overhead irrigation to keep leaves dry.",
        "Remove infected leaves to reduce disease spread.",
        "Space plants properly to promote air circulation.",
        "Apply a fungicide if leaf spots are severe.",
        "Clean up garden debris regularly.",
        "Rotate crops to prevent the buildup of pathogens.",
        "Sterilize gardening tools to avoid disease transmission.",
        "Water plants in the morning to allow leaves to dry by evening.",
        "Mulch plants to prevent soil from splashing onto leaves.",
        "Improve drainage in the garden to reduce humidity.",
        "Prune overcrowded plants to improve airflow.",
        "Dispose of infected plant material properly.",
        "Avoid handling plants when they are wet to prevent the spread of spores.",
        "Use organic copper-based fungicides if needed.",
        "Monitor plants regularly for early signs of infection.",
        "Incorporate compost into the soil to improve plant health.",
        "Avoid using high-nitrogen fertilizers that promote soft tissue.",
        "Ensure the garden area gets plenty of sunlight.",
        "Use resistant seeds or transplants to reduce risk.",
        "Keep plants healthy with proper nutrition and watering.",
        "Use natural remedies like neem oil to control fungal diseases.",
        "Reduce plant stress by keeping them well-watered during drought.",
        "Avoid planting susceptible crops in the same location each year.",
        "Create raised beds to improve drainage and prevent waterlogging.",
        "Avoid overcrowding plants to reduce humidity.",
        "Apply mulch to reduce splash-up of soilborne pathogens.",
        "Use a proper crop rotation system.",
        "Keep an eye on weather patterns and adjust watering accordingly.",
        "Remove any weeds that could be harboring the disease."
    ],
    "2 Powdery mildew": [
        "Ensure plants get plenty of sunlight to reduce humidity.",
        "Space plants properly to allow air circulation.",
        "Water plants at the base, avoiding wetting the foliage.",
        "Apply fungicides early to control spread.",
        "Use a sulfur-based spray to prevent powdery mildew.",
        "Plant mildew-resistant varieties.",
        "Prune plants to improve air circulation.",
        "Avoid high-nitrogen fertilizers that promote tender growth.",
        "Remove and destroy infected leaves and plant parts.",
        "Water plants in the morning to allow them to dry during the day.",
        "Keep humidity levels low in greenhouses.",
        "Use organic fungicides such as neem oil or baking soda solutions.",
        "Keep plants healthy with balanced fertilization.",
        "Apply a bicarbonate spray as a preventive measure.",
        "Maintain good garden hygiene by removing plant debris.",
        "Do not overcrowd plants, especially in shady areas.",
        "Use milk sprays to treat powdery mildew naturally.",
        "Increase ventilation in greenhouses or indoor growing areas.",
        "Avoid working with wet plants to prevent spreading the disease.",
        "Water plants deeply but less frequently.",
        "Apply potassium bicarbonate-based fungicides.",
        "Clean and disinfect garden tools regularly.",
        "Mulch plants to reduce soil splash.",
        "Remove weeds to reduce moisture retention around plants.",
        "Create barriers to prevent the spread of mildew spores.",
        "Rotate crops and avoid planting the same species year after year.",
        "Use fungicide treatments at the first sign of mildew.",
        "Reduce shade by trimming nearby trees or bushes.",
        "Avoid planting susceptible plants in mildew-prone areas.",
        "Treat plants with a copper fungicide spray as a preventive measure."
    ],
    "3 Rusty leaves": [
        "Plant disease-resistant varieties where possible.",
        "Ensure good air circulation around plants by proper spacing.",
        "Water plants at their base, avoiding the foliage.",
        "Remove and destroy infected plant material.",
        "Apply fungicides early in the growing season.",
        "Control weeds that can harbor rust spores.",
        "Avoid overhead watering to keep leaves dry.",
        "Ensure plants get full sunlight.",
        "Rotate crops to prevent rust build-up in the soil.",
        "Use neem oil or sulfur-based fungicides to control rust.",
        "Prune plants to improve airflow and reduce humidity.",
        "Improve drainage to prevent waterlogged soil.",
        "Clean and disinfect garden tools regularly.",
        "Apply copper-based fungicides to prevent rust.",
        "Mulch around plants to reduce soil splash.",
        "Use resistant plant varieties where available.",
        "Monitor plants frequently for early signs of infection.",
        "Encourage natural predators like ladybugs that eat rust spores.",
        "Water early in the morning to allow leaves to dry before night.",
        "Use organic fungicides to treat infected plants.",
        "Improve soil health by adding compost and organic matter.",
        "Avoid planting rust-prone crops in consecutive years.",
        "Keep the garden area free of plant debris.",
        "Remove any infected weeds to reduce rust transmission.",
        "Keep plants strong and healthy with balanced fertilization.",
        "Use crop rotation to prevent rust recurrence.",
        "Dispose of infected plant material away from the garden.",
        "Check plants regularly during humid weather conditions.",
        "Reduce nitrogen-rich fertilizers that promote soft growth.",
        "Avoid overcrowding plants, especially in shaded areas."
    ],
    "4 Healthy plant": [
        "Maintain a regular watering schedule for your plants.",
        "Ensure plants receive adequate sunlight for growth.",
        "Use compost to improve soil quality and provide nutrients.",
        "Remove weeds regularly to reduce competition for nutrients.",
        "Mulch your plants to retain moisture and suppress weeds.",
        "Test soil pH and nutrients to ensure proper growing conditions.",
        "Prune plants regularly to remove dead or diseased parts.",
        "Rotate crops to reduce the risk of soilborne diseases.",
        "Keep garden tools clean and sterilized to prevent disease spread.",
        "Provide plants with balanced fertilizers as needed.",
        "Ensure proper drainage to avoid root rot.",
        "Introduce beneficial insects to control harmful pests.",
        "Water plants early in the morning to reduce evaporation.",
        "Avoid overcrowding plants to ensure good air circulation.",
        "Plant disease-resistant varieties to reduce pest problems.",
        "Inspect plants frequently for signs of pests or diseases.",
        "Use natural or organic pest control methods.",
        "Monitor weather patterns and adjust care accordingly.",
        "Train plants to grow vertically to save space.",
        "Harvest plants regularly to encourage new growth.",
        "Use cover crops to improve soil structure and fertility.",
        "Support plants with stakes or trellises to prevent damage.",
        "Avoid using harsh chemicals that can harm beneficial insects.",
        "Increase ventilation in greenhouses to reduce humidity.",
        "Provide adequate spacing between plants for air circulation.",
        "Encourage biodiversity in the garden to prevent pest infestations.",
        "Keep the garden area clean and free of debris.",
        "Water plants consistently, avoiding extremes of drought or overwatering.",
        "Use natural mulches like straw or wood chips.",
        "Create an integrated pest management plan for long-term health."
    ]
}

async def process_image(image: UploadFile):
    # Read image file
    image_data = await image.read()
    
    # Convert binary data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    
    # Decode image
    processed_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Resize image to match the model input size
    size = (224, 224)
    processed_image_pil = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
    resized_image = ImageOps.fit(processed_image_pil, size, Image.Resampling.LANCZOS)

    # Turn the image into a numpy array
    image_array = np.asarray(resized_image)
    
    # Normalize the image as per model expectations
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Expand dimensions to match the model's input tensor shape (1, 224, 224, 3)
    input_data = np.expand_dims(normalized_image_array, axis=0)
    
    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # Run inference
    interpreter.invoke()
    
    # Get the output tensor (assumed to be a list of probabilities for each class)
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Convert output_data to a Python list
    predictions = output_data[0]
    
    # Create a list to store class names with their confidence scores rounded to 3 decimal places
    results = []
    for i in range(len(class_names)):
        confidence_score = round(float(predictions[i]), 3)
        result = {"class": class_names[i], "confidence_score": confidence_score}

        # If confidence is above 10%, select 5 random tips
        if confidence_score > 0.1:
            tips = random.sample(pest_tips[class_names[i]], 5)
            result["tips"] = tips

        results.append(result)

    # Return all the predictions and tips (if applicable)
    return {"predictions": results}