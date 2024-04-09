import socket
import threading
import cv2
from ultralytics import YOLO
from langchain_community.llms import Ollama
from DepthModel import DepthEstimationModel

# TODO: IMPORT FROM RELATIVE PATH
from ultralytics_YOLOs import *
from image_receiver import *

ways = {}
angles = [list(range(-65,-45)),list(range(-45,-25)),list(range(-25,-10)),list(range(-10,10)),list(range(10,25)),list(range(25,45)),list(range(45,65))]
directions = ["full left","half left","slightly left","forward","slightly right","half right","full right"]
for l,w in zip(angles,directions):
    ways.update({k:w for k in l})

# yolo_model = YOLO("yolov8s-seg.pt") # small YOLOv8 for segmentation
yolo_model = YOLO("../YOLO_scripts/yolov5s.pt") # small YOLOv5 for
LLM_model = Ollama(model="llama2")

depth_model = DepthEstimationModel()

def yolo_pass(yolo_model, image):
    return get_angle_label_id_and_bboxes(yolo_model, image)


def depth_pass(depth_model, image, YOLO_out, bboxes, closeness_threshold):
    depth_out = depth_model.calculate_depthmap(image)
    if len(YOLO_out) == 0: 
        depth_map_middle = depth_out[depth_out.shape[0]//3:2*depth_out.shape[0]//3, :]
        column_width = depth_map_middle.shape[1] // 5
        objects = []
        for i in range(5):
            column = depth_map_middle[:, i*column_width:(i+1)*column_width]
            min_value = np.min(column)
            if min_value < 5: # 5 metreden daha yakın bir şey varsa
                # get the angle of the column
                angle = (i*column_width + (i+1)*column_width) // 2
                objects.append((min_value, angle, i))
        return objects

        # no object detected by YOLO
        # look for obstacles that are close to camera
        # return format: depth, angle, id --> (7, 40, id=2)
    else:
        # get the mask/bounding box of objects and calculate the distance
        # return the informations of objects that are closer than closeness_threshold
        # return format is depth, angle, id, label --> (7, 40, id=2, "Table")
        close_objects = []

        for i, (angle_label_id, bbox) in enumerate(zip(YOLO_out, bboxes)):
            center_x = (bbox[0][0] + bbox[1][0]) // 2
            center_y = (bbox[0][1] + bbox[1][1]) // 2

            depth_value = depth_out[center_y, center_x]

            if depth_value < closeness_threshold:
                # Object is considered close
                angle, label, obj_id = angle_label_id
                close_objects.append((depth_value, angle, obj_id, label))

        return close_objects


# funtion to pass image to vision models
def send_image_to_models(image):
    """
    send received image to first YOLO and then DEPTH model, merges outputs of models and returns
    """
    YOLO_out, bboxes = yolo_pass(yolo_model, image)
    
    merged_out = depth_pass(depth_model, image, YOLO_out, bboxes, 7)
    return merged_out
    
# generates prompt by merging infos from models outputs
def generate_prompt(model_out):
    if len(model_out) == 0:
        return "no obstacle detected, go forward"

    state_str = ""
    closed_directions = set()
    
    if len(model_out[0]) == 3: # yolo didnt detect anything
        for i in model_out:
            closed_directions.add(ways[i[1]])
            state_str = state_str + ("obstacle at " + str(i[0]) + " meters ahead at " + str(ways[i[1]])) + "\n"
    else: # yolo detected something
        for i in model_out:
            closed_directions.add(ways[i[1]])
            state_str = state_str + (i[3] + " at " + str(i[0]) + " meters ahead at " + str(ways[i[1]])) + "\n"

    if "forward" not in closed_directions:
        recommended_direction = "user should go forward"
    else:
        recommended_direction = "user should change direction"

    with open("../LLM_prompts/ready_prompt", 'r') as file:
        ready_prompy = file.read()
    state_str = ready_prompy + state_str + recommended_direction
    state_str = state_str + "\n\nNow write a short sentence to guide the user."

    return state_str


# Function to pass vision models output to LLM API
def LLM_pass(LLM_model, prompt):
    if prompt == "no obstacle detected, go forward":
        LLM_out = prompt
    else:
        LLM_out = LLM_model(prompt)
    return LLM_out


# Define server address and port
SERVER_HOST = '0.0.0.0'  # This allows connections from any network interface
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT)) # Bind the socket to the address and port


def handle_client(client_socket, client_address):
    while True:
        message_json_dict = get_data(client_socket)
        closed = process_data(message_json_dict)
        if closed:
            break

        image = message_json_dict["image"]
        #cv2.imshow("server received this:", image)
        #cv2.waitKey(1)

        YOLO_and_DEPTH_out = send_image_to_models(image)
                
        prompt = generate_prompt(YOLO_and_DEPTH_out)

        LLM_out = LLM_pass(LLM_model, prompt)

        closed = send_data(client_socket, LLM_out, end=1)
        if closed:
            break

    cv2.destroyAllWindows()
    client_socket.close()

while True:
    server_socket.listen(1) # Listen for incoming connections
    client_socket, client_address = server_socket.accept() # wait and accept incoming connection 

    threading.Thread(target=handle_client, args=(client_socket, client_address,)).start()
