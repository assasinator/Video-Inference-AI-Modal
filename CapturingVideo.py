import cv2
import numpy as np

# download and load YOLOv3 weights using the link given in readme.md
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load names of classes
classes = None
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened(): 
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

while(True):
    ret, frame = cap.read()

    if ret: 
        # Display the resulting frame    
        #cv2.imshow('frame',frame)
        
        img = cv2.resize(frame, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
                cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 2)
        cv2.imshow("Image", img)

        # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break  
# Loading image



#cv2.waitKey(0)
cv2.destroyAllWindows()
