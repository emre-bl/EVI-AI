import socket
import json
import cv2
import base64

def send_data(client_socket, message_data, original_size, end=1):
    message_json_dict = {"data": message_data, "original_size": (original_size[1], original_size[0]), "end": end}    
    # end:-1->close socket, 0->message not ended: 1->message ended

    # print("sent:", message_json_dict)
    message_json_data = json.dumps(message_json_dict)
    client_socket.send(message_json_data.encode())

    return message_json_dict["end"] == -1

def get_data(client_socket):
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
    print("received:", json_dict)
    if json_dict["end"] == 1:
        return False
    if json_dict["end"] == -1:
        # closing the connection because server said end=-1
        return True

def image_to_base64(image):
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode()


if __name__ == "__main__":
    # Define server address and port
    SERVER_HOST = '0.0.0.0'  # Change this to the server's IP address
    SERVER_PORT = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cap = cv2.VideoCapture(0)
    BUFFER_SIZE = 1
    cap.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)
    if not cap.isOpened():
        exit(0)

    client_socket.connect((SERVER_HOST, SERVER_PORT))

    while True:
        for _ in range(BUFFER_SIZE+1):
            ret, image = cap.read()
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
    cap.release()