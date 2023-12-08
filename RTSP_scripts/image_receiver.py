import socket
import pickle
import cv2


def process_image(image):
    cv2.namedWindow("Received Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Received Image", image)
    cv2.waitKey(1)
    #cv2.destroyAllWindows()


# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
client_socket.connect(server_address)

try:
    while True:
        image_data = b""
        
        while True: # Loop until the entire data is received
            if 0 < len(image_data) < 4097:
                print("ClientSide: receiving image...")
                
            chunk = client_socket.recv(4096)
            if not chunk:
                break

            image_data += chunk
            if image_data[-4:] == "DONE".encode():
                print("ClientSide: fully received image.")
                image_data = image_data[:-4]
                break

        if not image_data:
            break

        # Deserialize the image using pickle
        image = pickle.loads(image_data)
        process_image(image)

        # Send a signal back to the server indicating that processing is done
        client_socket.send("DONE".encode())

finally:
    print("ClientSide: terminating code.")
    client_socket.close()
