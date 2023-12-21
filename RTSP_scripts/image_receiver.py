import socket
import pickle
import cv2

# Function to receive image data
def get_image_data():
    image_data = b""
    
    while True: # Loop until the entire data is received            
        chunk = receiver_socket.recv(4096)
        if not chunk:
            break

        image_data += chunk
        if image_data[-14:] == "SENDERSIDEDONE".encode():
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
        cv2.imshow("receier_image", image)
        cv2.waitKey(1)
    
        receiver_socket.send("RECEIVERSIDEDONE".encode())
finally:
    cv2.destroyAllWindows()
    receiver_socket.close()