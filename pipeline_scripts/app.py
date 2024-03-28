from flask import Flask, jsonify
import subprocess
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


"""@app.route('/runscript', methods=['GET'])
def run_script():
    try:
        # Replace 'python' with 'python3' if required by your environment
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, 'user.py')  # Ensure 'user.py' is in the same directory
        result = subprocess.run(['python', script_path], stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        return jsonify({'success': True, 'output': output}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'error': str(e)}), 400"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

