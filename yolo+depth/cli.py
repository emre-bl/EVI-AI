from predict import combined_predictor
import argparse 
import cv2
from PIL import Image
from DepthModel import DepthEstimationModel
import torch
from models.experimental import attempt_load
import numpy as np
import os
import sys


class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


confidence_threshold = 0.5 # confidence threshold for YOLO 

def main():
    parser = argparse.ArgumentParser(description='Vision + Depth')
    parser.add_argument('frame', type=str, help='Path to the input frame')
    args = parser.parse_args()

    with SuppressOutput():
        yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        
    with SuppressOutput():
        depth_model = DepthEstimationModel()
        yolo_model.max_det = 5
        yolo_model.conf = confidence_threshold

    combined_predictor(args.frame, yolo_model, depth_model, confidence_threshold)


if __name__ == '__main__':
    main()
    
    