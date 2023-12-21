import socket
import pickle
import cv2

# Function to get response over network
def receive_response(conn):
    response_data = ""
    
    while True: # Loop until the entire data is received            
        chunk = conn.recv(4096).decode()
        if not chunk:
            break

        response_data += chunk
        if response_data[-16:] == "RECEIVERSIDEDONE":
            response_data = response_data[:-16]
            break
    
    return response_data

# Function to send image and reveice the response over network
def send_image_get_response(conn, image):
    image = cv2.resize(image, (image.shape[0]//2,image.shape[1]//2))
    data_to_send = pickle.dumps(image) + "SENDERSIDEDONE".encode()
    conn.send(data_to_send)
    
    response_data = receive_response(conn)
    print(response_data)

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sender_address = ('localhost', 12345) # Bind the socket to a specific address and port
sender_socket.bind(sender_address)

# Listen for incoming connections
sender_socket.listen(1)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    sender_socket.close()    
    exit(0)

connection, client_address = sender_socket.accept()

try:
    ret, image = cap.read()
    while ret:
        send_image_get_response(connection, image)
        ret, image = cap.read()          
finally:
    print("senderSide: terminating code.")
    connection.close()
    sender_socket.close()