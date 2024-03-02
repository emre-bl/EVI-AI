import socket
import pickle
import cv2
from ultralytics import YOLO

# TODO: IMPORT FROM RELATIVE PATH
from ultralytics_YOLOs import *
from image_receiver import *

# TODO: USE WAYS BEFORE PASSING TEXT TO LLM FOR REPLACING ANGLES WITH WORDS
ways = {tuple(list(range(-65,-45))): "left",
        tuple(list(range(-45,-25))): "half left",
        tuple(list(range(-25,-10))): "slightly left",
        tuple(list(range(-10,10))): "forward",
        tuple(list(range(10,25))): "slightly right",
        tuple(list(range(25,45))): "half right",
        tuple(list(range(45,65))): "right"}

# yolo_model = YOLO("yolov8s-seg.pt") # small YOLOv8 for segmentation
yolo_model = YOLO("../YOLO_scripts/yolov5s.pt") # small YOLOv5 for


def yolo_pass(yolo_model, image):
    return get_angle_label_id_and_bboxes(yolo_model, image)


def depth_pass(depth_model, image, YOLO_out, bboxes, closeness_threshold):
    depth_map = depth_model(image)
    if len(YOLO_out) == 0:
        pass
        # no object detected by YOLO
        # look for obstacles that are close to camera
        # return format: depth, angle, id --> (7, 40, id=2)
    else:
        pass
        # get the mask/bounding box of objects and calculate the distance
        # return the informations of objects that are closer than closeness_threshold
        # return format is depth, angle, id, label --> (7, 40, id=2, "Table")

# funtion to pass image to vision models
def send_image_to_models(image):
    """
    send received image to first YOLO and then DEPTH model, merges outputs of models and returns
    """
    YOLO_out, bboxes = yolo_pass(yolo_model, image)
    return (YOLO_out, YOLO_out)
    DEPTH_out = depth_pass(depth_model, image, YOLO_out, bboxes, 0.7)

    merged_output = (YOLO_out, DEPTH_out)
    return merged_output

# generates prompt by merging infos from models outputs
def generate_prompt(YOLO_and_DEPTH_out):
    """
    gets outputs of YOLO and DEPTH model and merges them into one list of information about obstacles in scene
    """
    # TODO: GENERATE THE PROMPT FROM YOLO AND DEPTH MODEL OUTPUTS
    # MERGE THEM IN WANTED ORDER
    # READ THE READY PROMPTS FROM "LLM_prompts" directorty and return result prompt

    if len(YOLO_and_DEPTH_out[0]) != 0:
        # YOLO detected something
        blocked_angles = [[way for way in ways.keys() if blocked_way in way][0] for blocked_way in [info[0][1] for info in YOLO_and_DEPTH_out[0]]]
        available_ways = [ways[available_way] for available_way in ways.keys() if available_way not in blocked_angles]
    else:
        # YOLO detected nothing
        available_ways = []
    return str(YOLO_and_DEPTH_out)


# Function to pass vision models output to LLM API
def LLM_pass(prompt):
    return prompt
    LLM_out = LLM_model(prompt)
    return LLM_out


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

        image = message_json_dict["image"]
        cv2.imshow("server received this:", image)
        cv2.waitKey(1)

        YOLO_and_DEPTH_out = send_image_to_models(image)

        prompt = generate_prompt(YOLO_and_DEPTH_out)

        LLM_out = LLM_pass(prompt)

        closed = send_data(client_socket, LLM_out, end=-1)
        if closed:
            break

    cv2.destroyAllWindows()
    client_socket.close()
    break