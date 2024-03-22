import socket
import cv2
#import sys
import time
import requests

# TODO: IMPORT FROM RELATIVE PATH
from image_sender import *

from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/process_image', methods=['POST'])
def process_image():
    app.logger.info('Data received: %s', request.data)  # Log raw request data
    if request.is_json:
        data = request.get_json()
        app.logger.info('JSON data: %s', data)  # Log JSON data
        image_data = data.get('image')

        # Decode the Base64 string, convert to a NumPy array
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

        # Save the image for later use
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_dir, 'received_image.jpg')
        cv2.imwrite(save_path, img)

        return jsonify({'message': 'Image processed successfully'}), 200
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# function to set image sending frequency
# >0:wait, 0:send manual, other:realtime
def wait_delay(WAIT_SECONDS):
    if WAIT_SECONDS > 0:
        time.sleep(WAIT_SECONDS)
    elif WAIT_SECONDS == 0:
        cv2.waitKey(0)
    else:
        pass

# Define server address and port
SERVER_HOST = '0.0.0.0'  # Change this to the server's IP address
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cap = cv2.VideoCapture(0)
BUFFER_SIZE = 1
cap.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)
if not cap.isOpened():
    exit(0)

client_socket.connect((SERVER_HOST, SERVER_PORT))

while True:
    for _ in range(BUFFER_SIZE+2):
        ret, image = cap.read()
    #image = cv2.imread(sys.argv[1])
    original_size = image.shape
    image = cv2.resize(image, (448, 448))
    image_base64_string = image_to_base64(image)
    
    closed = send_data(client_socket, image_base64_string, original_size)
    if closed:
        break
    
    response_json_dict = get_data(client_socket)
    print(response_json_dict)

    closed = process_data(response_json_dict)
    if closed:
        break

client_socket.close()
cap.release()
