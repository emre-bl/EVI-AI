import socket
import pickle
import cv2
from ultralytics import YOLO
import torch
import os
import numpy as np
import time

ways = {tuple(list(range(-65,-45))): "left",
        tuple(list(range(-45,-25))): "half left",
        tuple(list(range(-25,-10))): "slightly left",
        tuple(list(range(-10,10))): "forward",
        tuple(list(range(10,25))): "slightly right",
        tuple(list(range(25,45))): "half right",
        tuple(list(range(45,65))): "right"}

# model = YOLO("yolov8s-seg.pt") # small YOLOv8 for segmentation
os.chdir("../YOLO_scripts")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)




def draw_bbox_id_text_confidance(image, result, draw_rectangle = True, draw_label_text = True, threshold= 0.8):
    object_ids = []
    id_counter = 1

    for [a, b, c, d, conf, pred_id] in result[0].boxes.data:
        if conf.item() > threshold:
            lu, ru, ld, rd = int(a.item()), int(b.item()), int(c.item()), int(d.item())

            if draw_rectangle:
                cv2.rectangle(image, (lu, ru), (ld, rd), (0, 255, 0), 7)
            if draw_label_text:
                label_text = str(id_counter) + "-" + str(result[0].names[pred_id.item()]) + ": {:.2f}".format(conf.item())
                cv2.putText(image, label_text, (lu, ru - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 6)
            
            object_ids.append(id_counter)
            id_counter = id_counter + 1
        else:
            # -1 id means model is not confident enough
            object_ids.append(-1)

    return object_ids

def calculate_angles(image, result):
    # list of objects center pixels offsets according to images center point
    # negative: left/up
    # positive: right/down
    # X:row axis, determines how high or low an object is
    # Y:column axis, determines how left or right an object is
    im_s = image.shape

    # finding the angles of object according to camera, most left(y=-1):-50 degrees, most right(y=+1):+50 degrees
    object_angles = [(
                    round((((c[1] + c[3])/2 - im_s[0]/2) / (im_s[0]/2) * 5).item())*10,
                    round((((c[0] + c[2])/2 - im_s[1]/2) / (im_s[1]/2) * 5).item())*10)
                    for c in result[0].boxes.data[:,:4]]

    return object_angles

def yolo_pass(img, threshold=0.7, draw_rectangle=False, draw_label_text=False):
    result = model(img)
    return []
    object_ids = draw_bbox_id_text_confidance(img, result, threshold=threshold, draw_rectangle=draw_rectangle, draw_label_text=draw_label_text)
    object_angles = calculate_angles(img, result)
    object_labels = [result[0].names[x.item()] for x in result[0].boxes.data[:, 5]]
    angle_label_id = list(zip(object_angles, object_labels, object_ids))
    
    angle_label_id = [info for info in angle_label_id if info[2] != -1]
    
    return angle_label_id

depth_model = None
def depth_pass(image, angle_label_id,  closeness_threshold):
    depth_map = depth_model(image)
    if len(angle_label_id) == 0:
        pass
        # no object detected by YOLO
        # look for obstacles that are close to camera
    else:
        pass
        # get the mask/bounding box of objects and calculate the distance
        # return the informations of objects that are closer than closeness_threshold

# funtion to pass image to vision models
def send_image_to_models(image):
    cv2.imshow("g", image)
    cv2.waitKey(1)

    angle_label_id = yolo_pass(image)
    return angle_label_id

    DEPTH_out = depth_pass(image, angle_label_id, closeness_threshold)
    return merged_output


def generate_prompt(model_output, available_ways):
    return model_output + available_ways


# Function to pass vision models output to LLM API
def send_model_out_to_LLM(prompt):
    return prompt
    LLM_out = LLM_model(prompt)
    return LLM_out

# Function to receive image data
def get_image_data():
    image_data = b""
    
    while True: # Loop until the entire data is received
        if 0 < len(image_data) < 4097:
            print("receiverSide: receiving image...")
            
        chunk = receiver_socket.recv(4096)
        if not chunk:
            break

        image_data += chunk
        if image_data[-14:] == "SENDERSIDEDONE".encode():
            print("receiverSide: fully received image.")
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

        model_output = send_image_to_models(image)

        blocked_angles = [[way for way in ways.keys() if blocked_way in way][0] for blocked_way in [info[0][1] for info in model_output]]
        available_ways = [ways[available_way] for available_way in ways.keys() if available_way not in blocked_angles]

        prompt = generate_prompt(model_output, available_ways)

        LLM_out = send_model_out_to_LLM(prompt)

        response = LLM_out + "RECEIVERSIDEDONE"

        receiver_socket.send(response.encode())
finally:
    
    cv2.destroyAllWindows()
    print("receiverSide: terminating code.")
    receiver_socket.close()