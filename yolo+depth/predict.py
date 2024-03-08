import cv2

def combined_predictor(image_path, yolo_model, depth_model, confidence_threshold=0.5):
    image_width = 800      
    image_height = 600
    
    image = cv2.imread(image_path)
    image = cv2.resize(image, (image_width, image_height))

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    yolo_results = yolo_model(rgb_image)  # Adjust this line according to your YOLO model's prediction method

    # Extract detection results
    detections = yolo_results.xyxy[0] 

    # Check if any objects are detected
    if len(detections) > 0:
        depth_map = depth_model.calculate_depthmap(image, "output.png")
        for *xyxy, conf, cls in detections:
            
            if conf < confidence_threshold: # Skip detections with low confidence
                continue
            
            # Extract bounding box coordinates as integers
            x_min, y_min, x_max, y_max = map(int, xyxy) # Doğru çalışıyor. Testleri yapıldı.
            #bbox = [(x_min, y_min), (x_max, y_max)]
            label = yolo_model.names[int(cls)]  # Get label name from class index

            # Draw bounding box and label on the image
            #cv2.rectangle(image, bbox[0], bbox[1], (0, 255, 0), 2)
            #cv2.putText(image, f'{label} ({conf:.2f})', (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cropped_depth = depth_map[y_min:y_max, x_min:x_max] #Doğru çalışıyor. Testleri yapıldı. 
            
            # calculate depth for the center of the bounding box -> burayı değiştirebiliriz.
            depth = depth_map[int((y_min+y_max)/2), int((x_min+x_max)/2)]
            print(f'Depth for {label}: {depth:.2f}')
    
    #cv2.imshow('Combined YOLO and Depth Estimation', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
