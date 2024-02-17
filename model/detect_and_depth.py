import cv2
import torch
import numpy as np
from PIL import Image
from ultralytics import YOLO
from monodepth2.networks.resnet_encoder import ResnetEncoder
from monodepth2.networks.depth_decoder import DepthDecoder

from preprocess import preprocess_for_yolo, preprocess_for_monodepth

# Assuming `yolo_model` is your loaded YOLO model and `monodepth_model` is your MonoDepth2 model
# Also assuming `preprocess_for_yolo` and `preprocess_for_monodepth` are your preprocessing functions

def detect_objects_and_estimate_depth(image_path, yolo_model, monodepth_model):
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    yolo_input = preprocess_for_yolo(image)
    depth_input = preprocess_for_monodepth(image)

    # Object Detection with YOLO
    yolo_model.eval()  # Set model to evaluation mode
    with torch.no_grad():
        detections = yolo_model(yolo_input)
        # Apply non-maximum suppression and thresholding here to filter detections
        # Detections format: [x1, y1, x2, y2, confidence, class]

    # Depth Estimation with MonoDepth2
    monodepth_model.eval()  # Set model to evaluation mode
    with torch.no_grad():
        depth_output = monodepth_model(depth_input)
        depth_map = torch.nn.functional.interpolate(
            depth_output, size=image.size[::-1], mode="bilinear", align_corners=False
        )
        depth_map_np = depth_map.squeeze().cpu().numpy()

    # Mapping Depths to Detected Objects
    for detection in detections:
        x1, y1, x2, y2, _, _ = detection
        # Extract the depth of the detected object
        object_depth = depth_map_np[int(y1):int(y2), int(x1):int(x2)]
        avg_depth = np.mean(object_depth)  # Average depth within the bounding box

        print(f"Object detected with average depth: {avg_depth} units")

    return detections, depth_map_np

# YOLO
yolo_model = YOLO("yolov8n.pt")
#monodepth_model = torch.hub.load("nianticlabs/monodepth2", "monodepth2", trust_repo=True)

# MonoDepth2
checkpoint = torch.load('C:/GitHub/EVI-AI/model/mono_640x192/encoder.pth', map_location=torch.device('cpu'))
encoder = ResnetEncoder(num_layers=18, pretrained=False)

if 'state_dict' in checkpoint:
    encoder_state_dict = {k: v for k, v in checkpoint['state_dict'].items() if k.startswith('encoder')}
    encoder.load_state_dict(encoder_state_dict)
else:
    raise KeyError("No 'state_dict' key found in the checkpoint. Make sure you have the correct file.")

# Initialize the decoder
decoder = DepthDecoder(num_ch_enc=encoder.num_ch_enc, scales=range(4))
# Load the decoder weights, similar process as for the encoder
if 'state_dict' in checkpoint:
    decoder_state_dict = {k[len("decoder."):]: v for k, v in checkpoint['state_dict'].items() if k.startswith('decoder')}
    decoder.load_state_dict(decoder_state_dict)
else:
    raise KeyError("No 'state_dict' key found in the checkpoint. Make sure you have the correct file.")


"""encoder_path = 'C:/GitHub/EVI-AI/model/mono_640x192/encoder.pth'
encoder.load_state_dict(torch.load(encoder_path))

depth_decoder = DepthDecoder(num_ch_enc=encoder.num_ch_enc, scales=range(4))
decoder_path = 'C:/GitHub/EVI-AI/model/mono_640x192/depth.pth'
depth_decoder.load_state_dict(torch.load(decoder_path))"""


image_path = './image.jpg'
detections, depth_map = detect_objects_and_estimate_depth(image_path, yolo_model, decoder)
