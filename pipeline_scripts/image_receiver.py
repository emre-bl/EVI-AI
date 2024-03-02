import socket
import json
import cv2
import numpy as np
import base64

def send_data(client_socket, response_data, end=1):
    """sends text data over internet

    Args:
        client_socket (socket): socket to send data to
        response_data (str): text data to send to client_socket
        end (int, optional): 1 means keep the connection open, -1 means close the socket. Defaults to 1.

    Returns:
        bool: True means connection is closed False means connection is left open
    """
    response_json_dict = {"data": response_data, "end": end}
    
    # print("sent", response_json_dict)
    response_json_data = json.dumps(response_json_dict)
    client_socket.send(response_json_data.encode())

    return response_json_dict["end"] == -1

def get_data(client_socket):
    """retrieves data from socket

    Args:
        client_socket (socket): socket to listen for data

    Returns:
        dict: dictionary from retrieved json data
    """
    whole_data = ""

    while True:
        message_json_data = client_socket.recv(4096).decode()
        whole_data = whole_data + message_json_data
        # checks if message package is complated(better check can be done)
        if "\"end\": 1}" in whole_data:
            break
        if "\"end\": -1}" in whole_data:
            break

    message_json_dict = json.loads(whole_data)
    return message_json_dict

def process_data(json_dict):
    """processes retrieved dictionary data

    Args:
        json_dict (dict): dictionary that contains information about data

    Returns:
        bool: True means connection is closed False means connection is left open
    """
    # print("received:", json_dict)
    if json_dict["end"] == 1:
        image = base64_to_image(json_dict["data"])
        image = cv2.resize(image, json_dict["original_size"])
        json_dict["image"] = image
        return False
    if json_dict["end"] == -1:
        # closing the connection beacuse client said end=-1
        return True

def base64_to_image(base64_string):
    """converts base64 to an image

    Args:
        base64_string (str): base64 string of image

    Returns:
        numpy.ndarray: result array
    """
    buffer = base64.b64decode(base64_string)
    image = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), -1)
    return image


if __name__ == "__main__":
    # Define server address and port
    SERVER_HOST = '0.0.0.0'  # This allows connections from any network interface
    SERVER_PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT)) # Bind the socket to the address and port
    
    while True:
        server_socket.listen(1) # Listen for incoming connections
        client_socket, client_address = server_socket.accept() # wait and accept incoming connection 

        while True:
            message_json_dict = get_data(client_socket)
            closed = process_data(message_json_dict)
            if closed:
                break
            
            closed = send_data(client_socket, "response")
            if closed:
                break
            continue

        client_socket.close()