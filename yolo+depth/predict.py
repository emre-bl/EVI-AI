import cv2
from PIL import Image
from DepthModel import DepthEstimationModel
import torch
from models.experimental import attempt_load
import numpy as np

yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

depth_model = DepthEstimationModel()

def combined_predictor(image_path):
    # Load image
    image = cv2.imread(image_path)
    
    # Step 1: Object Detection with YOLO
    # Convert the image from BGR to RGB as YOLO model might expect RGB images
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    yolo_results = yolo_model(rgb_image)  # Adjust this line according to your YOLO model's prediction method
    yolo_results.print()  # Print the results to see the structure

    # Extract detection results
    detections = yolo_results.xyxy[0]

    # Check if any objects are detected
    if len(detections) > 0:
        for *xyxy, conf, cls in detections:
            # Extract bounding box coordinates as integers
            x_min, y_min, x_max, y_max = map(int, xyxy)
            bbox = [(x_min, y_min), (x_max, y_max)]
            label = yolo_model.names[int(cls)]  # Get label name from class index

            # Draw bounding box and label on the image
            cv2.rectangle(image, bbox[0], bbox[1], (0, 255, 0), 2)
            cv2.putText(image, f'{label} ({conf:.2f})', (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            
            # Depth Estimation within the bounding box
            pil_image = Image.fromarray(rgb_image)
            cropped_image = pil_image.crop((x_min, y_min, x_max, y_max))
            depth_result = depth_model.calculate_depthmap(cropped_image, "output.png")  # Assuming this function returns a depth map

            # Process and display depth information
            average_depth = np.mean(depth_result)  # Calculate average depth
            print(f'Average depth for {label}: {average_depth:.2f}')
    
    # Step 3: Show final image with bounding boxes, labels, and depth information
    cv2.imshow('Combined YOLO and Depth Estimation', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
combined_predictor('test6.png')
