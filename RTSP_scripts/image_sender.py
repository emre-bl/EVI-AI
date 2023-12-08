import socket
import time
import pickle
import cv2


# Function to send image over the network
def send_image(conn, image, sleep_time):
    image_data = pickle.dumps(image)
    done_data = "DONE".encode()
    data_to_send = image_data + done_data

    conn.send(data_to_send)
    
    print("Server: data sent, waiting for client response...")
    response = conn.recv(1024).decode() # Wait for the client response
    print("Server: received client response:", response)

    if response == "DONE":
        print("Server: client processing is done, waiting", sleep_time, "seconds before next image.")
        time.sleep(sleep_time)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 12345) # Bind the socket to a specific address and port

while True:
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Server: double check the", server_address, "reconnect if any error happened.")
        server_socket.bind(server_address)
        break
    except OSError as e:
        print(e)
        if e.errno == 98:  # Address already in use
            print("Server:", server_address, "already in use. Closing the existing connection.")
            server_socket.close()
        else:
            raise

# Listen for incoming connections
server_socket.listen(1)

print("Server: listening for connections...")



video_path = '/home/ai/E/clean/E1/e1_right_long.ts'
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Server: Error: Could not open video file.")
    exit(0)


while True:
    print("Server: waiting for a connection...")
    connection, client_address = server_socket.accept()
    
    try:
        print("Server: connection from", client_address)
        while True:
            ret, image = cap.read()
            if not ret:
                break
            send_image(connection, image, 0.01)
            
    finally:
        print("Server: terminating code.")
        connection.close()
        server_socket.close()
