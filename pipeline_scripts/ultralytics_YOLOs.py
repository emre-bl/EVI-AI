import cv2

def get_id_and_bbox(image, result, draw_rectangle = True, draw_label_text = True, threshold= 0.8):
    """
    gets a YOLO result and returns the ids and bounding boxes for images
    """
    object_ids = []
    object_bboxes = []
    id_counter = 1

    for [a, b, c, d, conf, pred_id] in result[0].boxes.data:
        if conf.item() > threshold:
            lu, ru, ld, rd = int(a.item()), int(b.item()), int(c.item()), int(d.item())

            if draw_rectangle:
                cv2.rectangle(image, (lu, ru), (ld, rd), (0, 255, 0), 7)
                object_bboxes.append(((lu, ru), (ld, rd)))
            if draw_label_text:
                label_text = str(id_counter) + "-" + str(result[0].names[pred_id.item()]) + ": {:.2f}".format(conf.item())
                cv2.putText(image, label_text, (lu, ru - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 6)
            
            object_ids.append(id_counter)
            id_counter = id_counter + 1
        else:
            # -1 id means model is not confident enough
            object_ids.append(-1)

    return object_ids, object_bboxes

def calculate_angles(image, result):
    """
    gets a YOLO result and returns detected images angles respect to camera --> (up/down angle, left/right angle)
    """
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

def get_angle_label_id_and_bboxes(model, img, threshold=0.7, draw_rectangle=False, draw_label_text=False):
    """
    gets a YOLO model and an image, returns detected images angles, labels, ids and bounding boxes
    """
    result = model.predict(img)
    object_ids, object_bboxes = get_id_and_bbox(img, result, threshold=threshold, draw_rectangle=draw_rectangle, draw_label_text=draw_label_text)
    object_angles = calculate_angles(img, result)
    object_labels = [result[0].names[x.item()] for x in result[0].boxes.data[:, 5]]
    angle_label_id = list(zip(object_angles, object_labels, object_ids))
    
    angle_label_id = [info for info in angle_label_id if info[2] != -1]
    
    return angle_label_id, object_bboxes