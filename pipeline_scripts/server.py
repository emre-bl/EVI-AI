import socket
import pickle
import cv2
from ultralytics import YOLO

ways = {tuple(list(range(-65,-45))): "left",
        tuple(list(range(-45,-25))): "half left",
        tuple(list(range(-25,-10))): "slightly left",
        tuple(list(range(-10,10))): "forward",
        tuple(list(range(10,25))): "slightly right",
        tuple(list(range(25,45))): "half right",
        tuple(list(range(45,65))): "right"}

# yolo_model = YOLO("yolov8s-seg.pt") # small YOLOv8 for segmentation
yolo_model = YOLO("../YOLO_scripts/yolov5s.pt") # small YOLOv5 for

# TODO: IMPORT FROM RELATIVE PATH
from ultralytics_YOLOs import *
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
    YOLO_out, bboxes = yolo_pass(yolo_model, image)
    return (YOLO_out, YOLO_out)
    DEPTH_out = depth_pass(depth_model, image, YOLO_out, bboxes, 0.7)

    merged_output = (YOLO_out, DEPTH_out)
    return merged_output


def generate_prompt(YOLO_and_DEPTH_out):
    if len(YOLO_and_DEPTH_out[0]) != 0:
        # YOLO detected something
        blocked_angles = [[way for way in ways.keys() if blocked_way in way][0] for blocked_way in [info[0][1] for info in YOLO_and_DEPTH_out[0]]]
        available_ways = [ways[available_way] for available_way in ways.keys() if available_way not in blocked_angles]
    else:
        # YOLO detected nothing
        available_ways = []
    return str(YOLO_and_DEPTH_out)
    # TODO: GENERATE THE PROMPT ACCORDING TO YOLO AND DEPTH MODEL OUTPUTS
    # READ THE READY PROMPTS FROM "LLM_prompts" directorty and return result prompt

# Function to pass vision models output to LLM API

def LLM_pass(prompt):
    return prompt
    LLM_out = LLM_model(prompt)
    return LLM_out

# Function to receive image data

def get_image_data():
    image_data = b""
    
    while True: # Loop until the entire data is received
        chunk = receiver_socket.recv(4096)
        if not chunk:
            break

        image_data += chunk
        if image_data[-14:] == "SENDERSIDEDONE".encode():
            image_data = image_data[:-14]
            break

    if not image_data:
        raise Exception("no image data")

    # Deserialize the image using pickle
    image = pickle.loads(image_data)
    return image


# Create a socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
server_address = ('localhost', 12345)
receiver_socket.connect(server_address)

try:
    while True:
        image = get_image_data()
        cv2.imshow("reveived_image", image)
        cv2.waitKey(1)
        YOLO_and_DEPTH_out = send_image_to_models(image)

        prompt = generate_prompt(YOLO_and_DEPTH_out)

        LLM_out = LLM_pass(prompt)

        response = LLM_out + "RECEIVERSIDEDONE"

        receiver_socket.send(response.encode())
finally:
    cv2.destroyAllWindows()
    print("receiverSide: terminating code.")
    receiver_socket.close()