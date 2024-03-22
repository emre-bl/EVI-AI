import socket
import cv2
#import sys
import time

# TODO: IMPORT FROM RELATIVE PATH
from image_sender import *

# function to set image sending frequency
# >0:wait, 0:send manual, other:realtime
def wait_delay(WAIT_SECONDS):
    if WAIT_SECONDS > 0:
        time.sleep(WAIT_SECONDS)
    elif WAIT_SECONDS == 0:
        cv2.waitKey(0)
    else:
        pass

# Define server address and port
SERVER_HOST = '10.0.2.2'  # Change this to the server's IP address
SERVER_PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cap = cv2.VideoCapture(0)
BUFFER_SIZE = 1
cap.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)
if not cap.isOpened():
    exit(0)

client_socket.connect((SERVER_HOST, SERVER_PORT))

while True:
    for _ in range(BUFFER_SIZE+2):
        ret, image = cap.read()
    #image = cv2.imread(sys.argv[1])
    original_size = image.shape
    image = cv2.resize(image, (448, 448))
    image_base64_string = image_to_base64(image)
    
    closed = send_data(client_socket, image_base64_string, original_size)
    if closed:
        break
    
    response_json_dict = get_data(client_socket)
    print(response_json_dict)

    closed = process_data(response_json_dict)
    if closed:
        break

client_socket.close()
#cap.release()
