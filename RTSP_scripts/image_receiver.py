import socket
import pickle
import cv2

# funtion to pass image to vision models
def send_image_to_models(image):
    cv2.imshow("g", image)
    cv2.watKey(1)
    return "yoloout ve depth out"
    YOLO_out = yolo_model(image)
    DEPTH_out = depth_model(image)

    # merge YOLO_out, DEPTH_out
    return YOLO_out, DEPTH_out

# Function to pass vision models output to LLM API
def send_model_out_to_LLM(out):
    return "LLMout"
    LLM_out = LLM_model(out)
    return LLM_out

# Function to receive image data
def get_image_data():
    image_data = b""
    
    while True: # Loop until the entire data is received
        if 0 < len(image_data) < 4097:
            print("receiverSide: receiving image...")
            
        chunk = receiver_socket.recv(4096)
        if not chunk:
            break

        image_data += chunk
        if image_data[-14:] == "SENDERSIDEDONE".encode():
            print("receiverSide: fully received image.")
            image_data = image_data[:-14]
            break

    if not image_data:
        raise Exception("no image data")

    # Deserialize the image using pickle
    image = pickle.loads(image_data)
    return image


# Create a socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
receiver_socket.connect(server_address)

try:
    while True:
        image = get_image_data()

        model_output = send_image_to_models(image)

        LLM_out = send_model_out_to_LLM(model_output)

        response = LLM_out + "RECEIVERSIDEDONE"

        receiver_socket.send(response.encode())
finally:
    
    print("receiverSide: terminating code.")
    receiver_socket.close()