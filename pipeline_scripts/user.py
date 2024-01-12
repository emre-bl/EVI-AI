import socket
import cv2
import time

from image_sender import send_image_get_response

# function to set image sending frequency
# >0:wait, 0:send manual, other:realtime
def wait_delay(WAIT_SECONDS):
    if WAIT_SECONDS > 0:
        time.sleep(WAIT_SECONDS)
    elif WAIT_SECONDS == 0:
        cv2.waitKey(0)
    else:
        pass


sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sender_address = ('localhost', 12345) # Bind the socket to a specific address and port
sender_socket.bind(sender_address)

# Listen for incoming connections
sender_socket.listen(1)
connection, client_address = sender_socket.accept()

BUFFER_SIZE = 1 # number of frames to store before current frame in queue
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)
if not cap.isOpened():
    sender_socket.close()    
    exit(0)
    
WAIT_SECONDS = 3
try:
    ret, image = cap.read()
    while ret:
        send_image_get_response(connection, image)
        wait_delay(WAIT_SECONDS)
        
        for _ in range(BUFFER_SIZE + 1):
            # throw stacked past images and get current image
            ret, image = cap.read()          
finally:
    print("senderSide: terminating code.")
    connection.close()
    sender_socket.close()