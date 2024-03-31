import socket
import cv2
import time
import os

# TODO: IMPORT FROM RELATIVE PATH
from image_sender import *

# Define server address and port
SERVER_HOST = '0.0.0.0'  # Change this to the server's IP address
SERVER_PORT = 12345

def read_saved_image(image_path):
    img = cv2.imread(image_path)
    if img is not None:
        resized_img = cv2.resize(img, (448, 448))
        return resized_img
    else:
        print("Failed to load the image")
        return None


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, 'received_image.jpg')
    last_mod_time = None  # Track the last modification time of the image
    counter = 0

    try:
        while True:
            # Check if the image file has been updated
            try:
                mod_time = os.path.getmtime(image_path)
                if mod_time != last_mod_time:
                    last_mod_time = mod_time
                    image = read_saved_image(image_path)
                    if image is not None:
                        image_base64_string = image_to_base64(image)
                        closed = send_data(client_socket, image_base64_string, image.shape)
                        if closed:
                            break

                        response_json_dict = get_data(client_socket)
                        print(response_json_dict)

                        closed = process_data(response_json_dict)
                        if closed:
                            break
                        
                        LLM_out = response_json_dict["data"] # Get LLM output
                        counter += 1
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        with open(script_dir + '/llm_output.txt', 'w') as file: # Save LLM output to a text file
                            file.write(LLM_out + f',{counter}')

            except OSError:
                print("Image file not found. Waiting for the file...")
            
            time.sleep(10)  # Check for a new image every 10 seconds
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()