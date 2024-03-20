from predict import combined_predictor
from PIL import Image
from DepthModel import DepthEstimationModel
import torch
import sys

confidence_threshold = 0.5  # confidence threshold for YOLO


def main():
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    depth_model = DepthEstimationModel()
    yolo_model.max_det = 5
    yolo_model.conf = confidence_threshold
    while True:
        frame_path = input("Enter the path to the image: ")
        if frame_path == "exit":
            sys.exit()
        combined_predictor(frame_path, yolo_model, depth_model, confidence_threshold)
        print("----------------------")


if __name__ == '__main__':
    main()



