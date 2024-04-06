from flask import Flask, jsonify
import subprocess
from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)
#last_mode_time = None

@app.route('/')
def home():
    return "Flask server is running without problems."

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


@app.route('/get_llm_output', methods=['GET'])
def get_llm_output():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path= os.path.join(script_dir, 'llm_output.txt')

        with open(txt_path, 'r') as file:
            llm_output = file.read()
            
        return jsonify({'LLM_out': llm_output}), 200
    except FileNotFoundError:
        return jsonify({'error': 'LLM_out not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)