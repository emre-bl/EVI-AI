import sys
import socket
import json
import cv2
import base64

def send_data(client_socket, message_data, original_size, end=1):
    """sends text data over internet

    Args:
        client_socket (socket): socket to send data to
        message_data (str): text data to send to client_socket
        original_size (tuple): _size of image to send
        end (int, optional): 1 means keep the connection open, -1 means close the socket. Defaults to 1.


    Returns:
        bool: True means connection is closed False means connection is left open
    """

    message_json_dict = {"data": message_data, "original_size": (original_size[1], original_size[0]), "end": end}    
    # end:-1->close socket, 0->message not ended: 1->message ended

    # print("sent:", message_json_dict)
    message_json_data = json.dumps(message_json_dict)
    client_socket.send(message_json_data.encode())

    return message_json_dict["end"] == -1

def get_data(client_socket):
    """retrieves data from socket

    Args:
        client_socket (socket): socket to listen for data

    Returns:
        dict: dictionary from retrieved json data
    """
    whole_data = ""

    while True:
        response_json_data = client_socket.recv(4096).decode()
        whole_data = whole_data + response_json_data
        if "\"end\": 1}" in whole_data:
                break
        if "\"end\": -1}" in whole_data:
            break

    response_json_dict = json.loads(whole_data)
    return response_json_dict

def process_data(json_dict):
    """processes retrieved dictionary data

    Args:
        json_dict (dict): dictionary that contains information about data

    Returns:
        bool: True means connection is closed False means connection is left open
    """
    # print("received:", json_dict)
    if json_dict["end"] == 1:
        return False
    if json_dict["end"] == -1:
        # closing the connection because server said end=-1
        return True

def image_to_base64(image):
    """converts image to base64 format

    Args:
        image (numpy.ndarray): image to turn to base64

    Returns:
        str: image in base64 format
    """
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode()


if __name__ == "__main__":
    # Define server address and port
    SERVER_HOST = '0.0.0.0'  # Change this to the server's IP address
    SERVER_PORT = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # # open a camera connection to get images from
    # cap = cv2.VideoCapture(0)
    # BUFFER_SIZE = 1 # how many frames should captured in queue
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)
    # if not cap.isOpened():
    #     exit(0)

    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    while True:
        # for _ in range(BUFFER_SIZE+1): # emptying the queue for getting newly captured image
        #     ret, image = cap.read()
        image = cv2.imread(sys.argv[1])
        original_size = image.shape
        image = cv2.resize(image, (448, 448))
        image_base64_string = image_to_base64(image)

        closed = send_data(client_socket, image_base64_string, original_size)
        if closed:
            break

        response_json_dict = get_data(client_socket)

        closed = process_data(response_json_dict)

        if closed:
            break

    client_socket.close()
    # cap.release()