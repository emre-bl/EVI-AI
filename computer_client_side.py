import requests
import base64
import time
import random

# Replace this with the URL of your server
server_url = "http://127.0.0.1:5000/upload_frame"

# List of image file paths
image_paths = ["image1.png", "image2.png", "image3.png"]

while True:
    # Choose a random image path
    random_image_path = random.choice(image_paths)
    
    # Read the selected image
    with open(random_image_path, "rb") as image_file:
        image_data = image_file.read()
    
    # Encode the image as base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    
    # Prepare the payload
    payload = {"frame_data": encoded_image}
    
    # Send the POST request to the server
    response = requests.post(server_url, json=payload)
    
    # Print the response
    print(response.json())
    
    # Sleep for 1 second
    time.sleep(1)

