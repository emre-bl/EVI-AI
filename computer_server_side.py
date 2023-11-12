from flask import Flask, request, jsonify, send_file
import base64
import io
from PIL import Image

app = Flask(__name__)

@app.route('/upload_frame')
def upload_frame():
    try:
        frame_data = request.json.get('frame_data')
        
        if frame_data:
            # Decode base64-encoded image data
            image_data = base64.b64decode(frame_data)
            image = Image.open(io.BytesIO(image_data))
            
            # Process the image as needed (e.g., save to disk, perform analysis)
            # You can replace this part with your desired processing logic
            
            return jsonify({'status': 'success', 'message': 'Frame received and processed'})
        else:
            return jsonify({'status': 'error', 'message': 'No frame data received'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/display_image')
def display_image():
    try:
        image_path = 'image1.png'  # Path to the image file
        
        # Open and serve the image file
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

