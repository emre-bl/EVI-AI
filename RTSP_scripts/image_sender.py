import socket
import time
import pickle
import cv2

# Function to get response over network
def receive_response(conn):
    response_data = ""
    
    while True: # Loop until the entire data is received
        if 0 < len(response_data) < 4097:
            print("senderSide: receiving response...")
            
        chunk = conn.recv(4096).decode()
        if not chunk:
            break

        response_data += chunk
        if response_data[-16:] == "RECEIVERSIDEDONE":
            print("senderSide: fully received response.")
            response_data = response_data[:-16]
            break
    
    return response_data

# Function to send image and reveice the response over network
def send_image_get_response(conn, image, sleep_time):
    data_to_send = pickle.dumps(image) + "SENDERSIDEDONE".encode()
    conn.send(data_to_send)
    
    print("senderSide: data sent, waiting for client response...")
    response_data = receive_response(conn)

    print("senderSide: received client response:", response_data)
    print("senderSide: client processing is done, waiting", sleep_time, "seconds before next image.")
    time.sleep(sleep_time)

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sender_address = ('localhost', 12345) # Bind the socket to a specific address and port
sender_socket.bind(sender_address)

# Listen for incoming connections
sender_socket.listen(1)
print("senderSide: listening for connections...")

cap = cv2.VideoCapture('/home/ai/E/clean/E1/e1_right_long.ts')
if not cap.isOpened():
    print("senderSide: Error: Could not open video file.")
    sender_socket.close()    
    exit(0)

print("senderSide: waiting for a connection...")
connection, client_address = sender_socket.accept()
print("senderSide: connection from", client_address)

try:
    ret, image = cap.read()
    while ret:
        send_image_get_response(connection, image, 0.01)
        ret, image = cap.read()          
finally:
    print("senderSide: terminating code.")
    connection.close()
    sender_socket.close()